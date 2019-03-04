"""This application demonstrates how to perform basic operations on prediction
with the Google AutoML Vision API.
For more information, the documentation at
https://cloud.google.com/vision/automl/docs.
"""

import argparse
import os
import time
import picamera

class predecirEmocion:
    
    global emocion
    
    def fotografiar(self):
        camara = picamera.PiCamera()
        camara.resolution = (2592, 1944)
        camara.sharpness = 100
        camara.capture('bebe.jpg')
        camara.close()

    def predict(self, ruido):
        """Make a prediction for an image."""
        project_id = 'incubadora-46527'
        compute_region = 'us-central1'
        model_id = 'ICN990830527828411926'
        file_path = '/home/pi/Scripts/Incubadora-master/bebe.jpg'
        score_threshold = '0.0'

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
        #print("Resultado:")
        for result in response.payload:
            if 'Bienestar' in result.display_name:
                bienestar=result.classification.score
            else:
                llanto=result.classification.score
            
        total=bienestar+llanto
        porcentajeB=bienestar*60/total
        porcentajeL=llanto*60/total
        
        if(ruido > 60):
                porcentajeL=porcentajeL+40
        else:
                porcentajeL=porcentajeL-40
    
        if(porcentajeL > porcentajeB):
            #print("El bebe esta llorando")
            emocion = "Llanto"
        else:
            #print("El bebe se encuentra en un estado de bienestar")
            emocion = "Bienestar"
            
        return emocion
        
    # [END automl_vision_predict]



       
        
