conda_setup: # For all the work that will be completed in the notebook
	@if conda env list | grep -q "mlops-zoomcamp"; then \
		echo "Environment exists"; \
	else \
		conda create -n mlops-zoomcamp python=3.9.7 -y; \
	fi
	. $$(conda info --base)/etc/profile.d/conda.sh && \
		conda activate mlops-zoomcamp && \
		pip install -r conda_env/requirements.txt
	@echo "Run 'conda activate mlops-zoomcamp' to use the environment."

pipenv_setup:
	pipenv install mlflow==2.22.0  scikit-learn==1.5.0  --python=3.9
	pipenv install --dev pytest black isort pre-commit

quality_checks: pipenv_setup
	pipenv run isort .
	pipenv run black .
