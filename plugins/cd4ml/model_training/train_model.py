# Description: Use this script to train a new ML model from scratch. The algorithm
#              is defined in 'get_model'. The trained model will be tracked in
#              MLflow and is available for further steps in the pipeline via model 
#              uri
# ================================================================================

import os
import mlflow
import mlflow.sklearn
import time
import pandas as pd
import pickle
import tempfile
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import GradientBoostingClassifier
import logging

logger = logging.getLogger(__name__)


def _check_keys(dict_, required_keys):
    """checks if a dict contains all expected keys"""
    for key in required_keys:
        if key not in dict_:
            raise ValueError(f'input argument "data_files" is missing required key "{key}"')


def get_model():
    """define and return the multi-classication model"""
    # DEFINE YOUR IMPROVED MODEL HERE:
    C = 1.0
    iterations = 50
    model = LogisticRegression(C=C, max_iter=iterations)
    return model
    

def train_model(data_files, experiment_name="experiment", **kwargs):
    """
    Loads x_train.csv and y_train.csv from data_dir, trains a model and tracks
    it with MLflow

    Args:
        data_files (dict): contains the following keys:
          'transformed_x_train_file': location of the training input data
          'transformed_y_train_file': location of the training data labels
        experiment_name (str): name of the MLflow experiment
    """
    required_keys = [
        'transformed_x_train_file',
        'transformed_y_train_file',
    ]
    _check_keys(data_files, required_keys)
    
    start = time.time()
        
    mlflow.set_experiment(experiment_name)
    
    x_train = pd.read_csv(data_files['transformed_x_train_file'])
    y_train = pd.read_csv(data_files['transformed_y_train_file'])
    
    with mlflow.start_run() as active_run:
        run_id = active_run.info.run_id
        # add the git commit hash as tag to the experiment run
        git_hash = os.popen("git rev-parse --verify HEAD").read()[:-2]
        mlflow.set_tag("git_hash", git_hash)
        
        clf = get_model()
        
        # Log parameters
        if hasattr(clf, 'C'):
            mlflow.log_param("C", clf.C)
        if hasattr(clf, 'max_iter'):
            mlflow.log_param("max_iter", clf.max_iter)
        
        # Train the model
        clf.fit(x_train, y_train)
        
        # Save model as pickle file and log as artifact
        # This avoids the MLflow model registry complications with --serve-artifacts
        with tempfile.TemporaryDirectory() as temp_dir:
            model_path = os.path.join(temp_dir, 'model.pkl')
            with open(model_path, 'wb') as f:
                pickle.dump(clf, f)
            
            # Log the model file as an artifact
            mlflow.log_artifact(model_path, 'model')
            
            # Also log model metadata
            mlflow.log_param("model_type", type(clf).__name__)
        
        # Get the model URI - this will now point to the actual artifact location
        model_uri = mlflow.get_artifact_uri("model")
       
    logger.info(f"completed script in {round(time.time() - start, 3)} seconds)") 
    
    return run_id, model_uri
    
    
