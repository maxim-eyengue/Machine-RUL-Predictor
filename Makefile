conda_env:
	conda create -n mlops-zoomcamp python=3.9.7
	conda activate mlops-zoomcamp
	conda install numpy pandas scikit-learn seaborn jupyter

setup_pipelines:
	pip install -r requirements.txt
