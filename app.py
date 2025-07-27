from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field, field_validator
from typing import Literal, Annotated
import pickle
import pandas as pd
from schema.user_input import UserInput
from model.predict import predict_output, model, MODEL_VERSION
from schema.prediction_response import PredictionResponse


app = FastAPI()    
@app.get('/')
def home():
    return {'message':'Insurance premium predictor'}

@app.get('/health')
def health_check():
    return{ 'status': 'OK',
           'version': MODEL_VERSION,
           'model_loaded': model is not None}

@app.post('/predict', response_model= PredictionResponse) #model validate the reponse of the output using this function predictionresponse
def predict_premium(data : UserInput):
    user_input = {
        'bmi': data.bmi,
        'age_group':data.age_group,
        'lifestyle_risk' : data.lifestyle_risk,
        'income_lpa': data.income_lpa,
        'occupation' : data.occupation ,
        'city_tier' :data.get_city_tier
    }


    try : 
        prediction = predict_output(user_input)

        return JSONResponse(status_code=200, content={'final prediction': prediction} )
    
    except Exception as e:
        
        return JSONResponse(status_code= 500, content=str(e))




    

        
    






