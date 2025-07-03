# Description: Use this script to push the model of the current pipeline run to
#              the MLflow server and label it as 'production'
# ================================================================================

import mlflow
import mlflow.sklearn
import pickle
import tempfile
from mlflow.tracking.client import MlflowClient
import logging

logger = logging.getLogger(__name__)


def push_model(model="LR", **kwargs):
    """
    Push the model to the mlflow server and labels it as production. Tags all other models
    currently in production as archived.

    Args:
        model (str): name of the model in mlflow to push
        kwargs (dict): any other kwargs should contain the task_instance from the airflow task.

    Error handling:
        ValueError: If the kwargs does not contain the task_instance.
    """

    task_instance = kwargs.get('task_instance')

    if task_instance is None:
        raise ValueError(
            "task_instance is required, ensure you are calling this function from an airflow task and after a training run.")

    run_id, model_uri = task_instance.xcom_pull(task_ids='model_training')
    logger.info(f"run_id: {run_id}")

    # Archive current production model(s)
    client = MlflowClient()
    try:
        prod_model_versions = client.get_latest_versions(
            model, stages=["Production"])
    except:
        prod_model_versions = []
        
    for prod_model_version in prod_model_versions:
        logger.info(f"archiving model: {prod_model_version}")
        client.transition_model_version_stage(
            name=model,
            version=prod_model_version.version,
            stage="Archived"
        )

    # Load the pickled model and re-register it as a proper MLflow model
    with tempfile.TemporaryDirectory() as temp_dir:
        # Download the pickle file
        pickle_path = client.download_artifacts(run_id, "model/model.pkl", temp_dir)
        
        # Load the model
        with open(pickle_path, 'rb') as f:
            loaded_model = pickle.load(f)
        
        # Re-register the model properly
        with mlflow.start_run(run_id=run_id):
            # Log the model using sklearn.log_model to create a proper MLflow model
            model_info = mlflow.sklearn.log_model(
                sk_model=loaded_model,
                artifact_path="production_model",
                registered_model_name=model
            )
            
            model_version = model_info.registered_model_version
    
    # Promote current model to production
    logger.info(f"promoting model: {run_id} as version: {model_version}")
    client.transition_model_version_stage(
        name=model,
        version=model_version,
        stage="Production"
    )
