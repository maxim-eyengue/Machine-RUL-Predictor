![Component Illustration](./images/hydraulic_cylender.png)

# Machine-RUL-Predictor
An application designed to predict the remaining useful life of critical components in construction machinery by using machine data.

## ❓ Problem Description

The goal of this project is to **predict the Remaining Useful Life (RUL)** of components of a machine  by analyzing **IoT** and **operations data**. This can be useful for predictive maintenance tasks where we decide on the maintenance to perform on asset data depending on what is the most critical. For example, we can prioritize components with the lower remaining useful life.

### 📊 Dataset Overview

<h3>Machine RUL Dataset</h3>

<p>The <a href="https://www.kaggle.com/datasets/sasakitetsuya/machine-rul-data">dataset</a> was created to simulate data related to the predictive maintenance of critical components in construction machinery, such as cranes, excavators, and bulldozers. It contains 1,000 records, each representing a unique component.

</p>

<h3>Features Description:</h3>
<ul>
    <li><strong>Component_ID</strong>: A unique identifier for each component, formatted as CMP0001 to CMP1000 [Text]</li>
    <li><strong>Component_Type</strong>: The type of component [Engine, Hydraulic Cylinder, Gear]</li>
    <li><strong>Vibration</strong>: The vibration level of the component, measured between 0.1 and 5.0
        [Numeric: arbitrary units ]</li>
    <li><strong>Temperature</strong>: The operating temperature of the component, ranging from 40 to 100
        [Numeric: degrees Celsius]</li>
    <li><strong>Pressure</strong>: The pressure exerted on the component, ranging from 50 to 300. [Numeric: psi]</li>
    <li><strong>Operating_Hours</strong>: The total time the component has been in operation, ranging from 0 to 5,000.
        [Numeric: hours]</li>
    <li><strong>Remaining_Useful_Life (RUL)</strong>: The estimated time left before the component fails, randomly assigned within a range of 50 to 1,000.
        [Numeric: hours]</li>
</ul>

### **Disclaimer** 🛑
The dataset used in this project is **synthetic** and has been generated rather than collected from real-world sources. ⚠️ Due to the lack of transparency in the data synthesis process, the exact methods and criteria used are **unknown** 🤷‍♂️. As a result, the patterns and relationships within the data may not accurately reflect real-world phenomena 🌍.

## 📁 Directory Structure

```plaintext
Machine-RUL-Predictor/
│
├── data/                         # Contains the dataset used for training
├── env/                          # Contains a requirements file that helps setting up the environment.
├── images/                       # Illustrations and deployment screenshots
├── mlflow-models/                # Contains experiments run srtifacts
├── machine-rul-data.zip          # .zip data file
├── .gitignore                    # Combines the files to ignore during Git operations
├── .pre-commit-config.yaml       # Configuration file for Git pre-commit hooks
├── prefect.yaml                  # Configuration file for prefect project
├── .prefectignore                # Combines the files to ignore during prefect full deployment
├── capstone_project.ipynb        # End-to-End Jupyter Notebook with data preparation, analysis, experiment tracking and model monitoring
├── orchestrate_prefect.py        # Prefect simple orchestration script
├── orchestrate_full_deploy.py    # Prefect orchestration script for full deployment
├── mlflow.db                     # backend-store sqlite file for saving metadata during experiment tracking
├── Makefile                      # Makefile to run faster some commands
├── run_id.txt                    # Text file containing the experiment run id of the saved model
├── Pipfile                       # Dependencies for pipenv
├── Pipfile.lock                  # Locked versions of dependencies
├── plan.md                       # Detailed plan for building the project
├── LICENSE                       # Project MIT License
└── README.md                     # Project description and instructions
```

## ⚙️ Usage

**Requirements**: Python 3.9

Make sure to clone the repository:
```bash
git clone https://github.com/maxim-eyengue/Machine-RUL-Predictor.git
cd Machine-RUL-Predictor
```
You can then check the [plan](#project-plan) and [makefile instructions](#makefile).

## Project plan
Detailed instructions have been provided [here](./plan.md).
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
- [x] Code quality: linting with the VSCode pylint extension and formatting with black and isort
- [x] There is a Makefile
- [x] Git pre-commit hooks
- [ ] There's a CI/CD pipeline

## Makefile
There is also a [makefile](./Makefile) that can help setting the environment. `Make` is installed by deault on Mac but can also be installed online. To run a command, write:
```sh
make "add the corresponding command"
```
For example, for creating a conda environment:
```sh
make conda_env
```
For setting the environment:
```sh
make setup
```
For improving code quality:
```sh
make quality_checks
```

## 🤝 Contributing

Contributions are welcome! To contribute:
- Fork the repository.
- Create a branch for your feature or bug fix.
- Submit a pull request with a detailed explanation of your changes.

---

## 📜 License

This project is licensed under the [MIT License](LICENSE.txt). Make sure to add this [license](LICENSE.txt) in any of your copy, specifying me as the right owner of the work.


---
