"""Module for Prefect Orchestration Pipeline."""

import zipfile # to unzip the data file
import mlflow # for experiment tracking
import pandas as pd # for dataframes

from sklearn.feature_extraction import DictVectorizer # for One-Hot Encoding
from sklearn.model_selection import train_test_split # for cross-validation techniques
from sklearn.pipeline import make_pipeline
from sklearn.ensemble import RandomForestRegressor # for decision trees
from sklearn.metrics import root_mean_squared_error

from evidently import DataDefinition
from evidently import Dataset
from evidently import Report
from evidently.metrics import ValueDrift, DriftedColumnsCount, MissingValueCount

from prefect import task, flow

# Local tracking URI
MLFLOW_TRACKING_URI = 'http://127.0.0.1:5000'
# Set the tracking URI as local server
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
# Set a Machine Learning experiment
mlflow.set_experiment("rul-machine-component")

@task(retries = 3, retry_delay_seconds = 2)
def read_dataframe() -> pd.DataFrame:
    """
    Function to download the dataset and return it as a Pandas
    dataframe.

    """
    # Unzip the `machine-rul-data.zip` file
    with zipfile.ZipFile("machine-rul-data.zip", "r") as rul_data:
        rul_data.extractall("data") # extract all files to the data directory
    # Fetch the records and put them in a DataFrame
    df = pd.read_csv("data/construction_machine_data.csv")
    # return the dataframe
    return df

@task
def prepare_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Function to preprocess the data and return a dataframe.
    ---
    df: input dataset
        pd.Dataframe
    """
    # Normalisation of column names
    df.columns = df.columns.str.lower()
    # drop component ids
    df.drop(columns = "component_id", inplace = True)

    # list of categorical feature variables
    categorical = df.select_dtypes("object").columns.to_list()
    # For each categorical variable
    for cat in categorical:
        # Format string values
        df[cat] = df[cat].str.lower().str.replace(" ", "_")

    # return dataframe
    return df

@task(log_prints=True)
def train_model(train_dicts, y_train, val_dicts, y_val):
    """
    Train the model for predicting the remaining useful life
    of components, register the model and return a run id.
    ---
    train_dicts: training data dictionnaries
    y_train: training true rul values
    val_dicts: validation data dictionnaries
    y_val: validation true rul values
    
    """
    # Start a new experiment run
    with mlflow.start_run() as run_exp:
         # Set model parameters
        params = dict(max_depth = 20, n_estimators = 100, min_samples_leaf = 10,
                    random_state = 0)
        # Log the model parameters
        mlflow.log_params(params)

        # Build a model pipeline
        pipeline = make_pipeline(
            DictVectorizer(),
            RandomForestRegressor(**params, n_jobs = -1)
        )

        # Model training
        pipeline.fit(train_dicts, y_train)
        # Prediction on validation data
        y_pred = pipeline.predict(val_dicts)

        # RMSE score
        rmse = round(root_mean_squared_error(y_pred, y_val), 3)
        # Print parameters and rmse score
        print(params, rmse)
        # Log the model rmse
        mlflow.log_metric('rmse', rmse)

        # Log the model
        mlflow.sklearn.log_model(pipeline, artifact_path = "model")
        # Model name
        model_name = 'machine-rul-predictor'
    # Register the model
    mlflow.register_model(
        model_uri = f"runs:/{run_exp.info.run_id}/models",
        name = model_name
    )
    # Inform that the model is saved
    print("model saved to the MLFlow registry")

    # Return the id of the experiment run
    return run_exp.info.run_id

@flow
def monitoring(df_val, df_test, numerical, categorical):
    """
    Function for monitoring by returning 
    an alert in cased there is a drift between reference data
    and current data.
    ---
    df_val: validation data considered reference data.
    df_test: test data considered current data.
    numerical: list of numerical features.
    categorical: list of categorical features.
    """
    # Set the data definition for column mapping
    data_definition = DataDefinition(numerical_columns = numerical + ["remaining_useful_life"],
                                     categorical_columns = categorical)
    # Prepare the data for reporting
    val_dataset = Dataset.from_pandas(df_val, data_definition)
    test_dataset = Dataset.from_pandas(df_test, data_definition)
    # Create a report
    report = Report(metrics = [
        ValueDrift(column ='remaining_useful_life'),
        DriftedColumnsCount(),
        MissingValueCount(column = 'remaining_useful_life'),
    ])
    # Run the report
    snapshot = report.run(reference_data = val_dataset,
                          current_data = test_dataset)
    # Save the report as dictionary
    result = snapshot.dict()
    # Send an alert if there is a value drift
    if result['metrics'][0]['value'] > 0.5:
        print("There is a prediction drift. Need some adjustment!!!")
    else:
        print("all good...")


@flow
def run():
    """
    The main Training Pipeline.
    ---
    url: url address of the zip data set.
        str
    """
    # Download the data set
    machine_df = read_dataframe()
    # Prepare the data
    machine_df = prepare_dataframe(machine_df)

    # Features lists
    numerical = machine_df.drop(
        columns = "remaining_useful_life"
    ).select_dtypes("number").columns.to_list()
    categorical = machine_df.select_dtypes("object").columns.to_list()


    # Data Splitting
    # Splitting into full train and test
    df_full_train, df_test = train_test_split(machine_df,
                                              test_size = 0.2, random_state = 42)
    # Splitting into train and test
    df_train, df_val = train_test_split(df_full_train,
                                        test_size = 0.25, random_state = 42)
    # Reset indexes
    df_train = df_train.reset_index(drop = True)
    df_test = df_test.reset_index(drop = True)
    df_val = df_val.reset_index(drop = True)

    # Get dictionnaries
    train_dicts = df_train[numerical + categorical].to_dict(orient = 'records')
    val_dicts = df_val[numerical + categorical].to_dict(orient = 'records')
    # Get the target values
    y_train = df_train.remaining_useful_life.values
    y_val = df_val.remaining_useful_life.values

    # Experiment tracking and Model saving to the registry
    run_id = train_model(train_dicts, y_train, val_dicts, y_val)
    # Print the obtained run experiment id
    print(f"MLflow run_id: {run_id}")
    # Model Monitoring
    monitoring(df_val, df_test, numerical, categorical)
    # return the run experiment id
    return run_id

# If the script is executed
if __name__ == "__main__":
    # Run the main flow
    model_run_id = run()
    # Open a text file
    with open("run_id.txt", "w", encoding="utf-8") as f:
        # Write the experiment run id
        f.write(model_run_id)
