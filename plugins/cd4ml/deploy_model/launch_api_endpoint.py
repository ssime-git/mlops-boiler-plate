from asyncio.log import logger
import subprocess
import os
import argparse

import logging

logger = logging.getLogger(__name__)


def launch_api_endpoint(model=None):
    """Launches the REST API endpoint through a docker container. 

    Args:
        model (_type_, optional): A model name in mlflow. If model is set the latest model with production tag is taken. Defaults to None.

    Raises:
        ValueError: If model is empty.
    """

    if model is not None:
        model_env = "-e MLFLOW_MODEL={}".format(model)
    else:
        raise ValueError("model must be set")

    bashCommand = "docker run -p 5001:5000 " + \
        model_env + " " + \
        "-e MLFLOW_TRACKING_URI={} ".format(os.environ.get("MLFLOW_TRACKING_URI", "http://mlflow-webserver:5000")) + \
        "-e MLFLOW_S3_ENDPOINT_URL={} ".format(os.environ.get("MLFLOW_S3_ENDPOINT_URL", "http://s3-artifact-storage:9000")) + \
        "-e AWS_ACCESS_KEY_ID={} ".format(os.environ.get("AWS_ACCESS_KEY_ID", "mlflow_access")) + \
        "-e AWS_SECRET_ACCESS_KEY={} ".format(os.environ.get("AWS_SECRET_ACCESS_KEY", "mlflow_secret")) + \
        "--network mlops-boiler-plate_default " + \
        "-d " + \
        "deployed_model"

    logger.info(f"Executing: {bashCommand}")
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    
    if error:
        logger.error(f"Error launching container: {error}")
    else:
        logger.info(f"Container launched successfully: {output}")


if __name__ == "__main__":
    argparser = argparse.ArgumentParser(description='Launches REST Endpoint')
    argparser.add_argument('model', type=str, help='model name to deploy')
    args = argparser.parse_args()
    launch_api_endpoint(args.model)
