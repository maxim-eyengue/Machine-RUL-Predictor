conda_env:
	conda create -n mlops-zoomcamp python=3.9.7
	conda activate mlops-zoomcamp
	conda install numpy pandas scikit-learn seaborn jupyter

setup:
	pip install -r env/requirements.txt
	pipenv install mlflow==2.22.0  scikit-learn==1.5.0  --python=3.9
	pipenv install --dev pytest black isort pre-commit

quality_checks: setup
	pipenv run isort .
	pipenv run black .
