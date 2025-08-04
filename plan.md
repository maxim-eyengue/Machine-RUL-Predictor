First activate the mlops-zoomcamp conda environment that was created for the course:
```sh
conda activate mlops-zoomcamp
```
If you have not create any conda environment, you can create and activate it:
```sh
conda create -n mlops-zoomcamp python=3.9.7
conda activate mlops-zoomcamp
```


Now use the [capstone project notebook](./capstone_project.ipynb) for building the model, tracking experiments and model monitoring. For completing this notebook successfully, make sure that MLFlow is running locally for experiment tracking:
```sh
mlflow server \
    --backend-store-uri sqlite:///mlflow.db \
    --default-artifact-root ./mlflow-models
```