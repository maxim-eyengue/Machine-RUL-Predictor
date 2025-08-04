# Plan
- [x] Problem description: The problem is well described and it's clear what the problem the project solves
- [ ] Cloud
- [x] Experiment tracking and model registry
: Both experiment tracking and model registry are used
- [x] Workflow orchestration: Fully deployed workflow orchestration with deployment runs and workpools.
- [ ] Model deployment
- [x] Model monitoring: Comprehensive model monitoring that sends an alert if prediction drift is detected
- [x] Reproducibility: Instructions are clear, it's easy to run the code, and it works. The data is provided and versions for dependencies are specified.

- [ ] Testing the code: unit tests with pytest
- [ ] Integration tests with docker-compose
- [ ] Code quality: linting and formatting
- [x] There is a Makefile
- [ ] Git pre-commit hooks
- [ ] There's a CI/CD pipeline
---

### Environment 
First activate the mlops-zoomcamp conda environment that was created for the course:
```sh
conda activate mlops-zoomcamp
```
If you have not create any conda environment, you can create and activate it:
```sh
conda create -n mlops-zoomcamp python=3.9.7
conda activate mlops-zoomcamp
```
You can then install common packages:
```sh
conda install numpy pandas scikit-learn seaborn jupyter
```

You need to install some more dependencies for experiment tracking and workflow orchestration:
```sh
pip install -r requirements.txt
```

### End-to-end notebook with experiment tracking and model monitoring
Now use the [capstone project notebook](./capstone_project.ipynb) for building the model, tracking experiments and model monitoring. For completing this notebook successfully, make sure that MLFlow is running locally for experiment tracking:
```sh
mlflow server \
    --backend-store-uri sqlite:///mlflow.db \
    --default-artifact-root ./mlflow-models
```

### Building pipelines
Now we can convert our notebook into a script and make the necessary changes for pipeline orchestration with prefect.

To convert the jupyter notebook into a script:
```sh
jupyter nbconvert --to=script capstone_project.ipynb
```

To rename a script:
```sh
mv capstone_project.py orchestrate_prefect.py
```
Now we will perform some refactoring on the obtained script to get a fully functionning [orchestration pipeline](./orchestrate_prefect.py) for experiment tracking, model management and also for monitoring. Once done we can test it.


### Orchestration pipeline
For running our orchestration pipeline:

- First we run mlflow:
```sh
mlflow server \
    --backend-store-uri sqlite:///mlflow.db \
    --default-artifact-root ./mlflow-models
```
- We launch `Prefect`:
```sh
prefect server start
```
- We configure Prefect locally:
```sh
prefect config set PREFECT_API_URL=http://127.0.0.1:4200/api
```
- We can now run the orchestration script:
```sh
python orchestrate_prefect.py
```
Here is a snapshot:
![Orchestration](./images/orchestration.png)

### For a full deployment of our orchestration file:
We will first do some refactoring and obtain a new [orchestration file](./orchestrate_full_deploy_.py). This refactoring is for making a local deployment. Then:
- First we run mlflow:
```sh
mlflow server \
    --backend-store-uri sqlite:///mlflow.db \
    --default-artifact-root ./mlflow-models
```

- Initialize the prefect project:
```sh
prefect init
```
We choose `local filesystem` for our testing case. This will create essential files:
    - `.prefectignore`: prevents automatic code pushes from Prefect to Git repositories.
    - `prefect.yaml`: the main configuration file for the project and deployment build, pull, and push steps.

- We launch `Prefect`:
```sh
prefect server start
```
- We configurate Prefect locally:
```sh
prefect config set PREFECT_API_URL=http://127.0.0.1:4200/api
```
- We can then start a worker that polls our work pool:
```sh
prefect worker start --pool "capstonepool"
```
- Deployment can be created using the CLI command:
```bash
prefect deploy orchestrate_full_deploy.py:run --name Rul --pool capstonepool 
```
Note that:
  - `orchestrate_full_deploy.py:run` specifies the flow entry point.
  - `--name` assigns a deployment name.
  - `--pool` specifies the pool from which workers will pull tasks.

- Run the full deployment:
```sh
prefect deployment run 'run/Rul'
```
We can see the deployement launch:
![Deployment run](./images/deployment_run.png)

Here the working pool with monitoring message:
![Working pool](./images/pool_working.png)

Finally, we can visualize Prefect UI:
![Prefect UI for full deployment](./images/full_deploy_ui.png)

For de