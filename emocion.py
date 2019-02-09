"""This application demonstrates how to perform basic operations on prediction
with the Google AutoML Vision API.
For more information, the documentation at
https://cloud.google.com/vision/automl/docs.
"""

import argparse
import os


def predict():
    """Make a prediction for an image."""
    project_id = ''
    compute_region = ''
    model_id = ''
    file_path = ''
    score_threshold = ''

    from google.cloud import automl_v1beta1 as automl

    automl_client = automl.AutoMlClient()

    # Get the full path of the model.
    model_full_id = automl_client.model_path(
        project_id, compute_region, model_id
    )

    # Create client for prediction service.
    prediction_client = automl.PredictionServiceClient()

    # Read the image and assign to payload.
    with open(file_path, "rb") as image_file:
        content = image_file.read()
    payload = {"image": {"image_bytes": content}}

    # params is additional domain-specific parameters.
    # score_threshold is used to filter the result
    # Initialize params
    params = {}
    if score_threshold:
        params = {"score_threshold": score_threshold}

    response = prediction_client.predict(model_full_id, payload, params)
    print("Resultado:")
    for result in response.payload:
        if 'Bienestar' in result.display_name:
            bienestar=result.classification.score
        else:
            llanto=result.classification.score
    if(llanto > bienestar):
        print("El bebe esta llorando")
    else:
        print("El bebe se encuentra en un estado de bienestar")
        
    # [END automl_vision_predict]


if __name__ == "__main__":
    
        predict()
