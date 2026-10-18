

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from schemas.prediction_response import PredictionResponse
from model.predict import MODEL_VERSION, predict_output , model
from schemas.user_schema import UserInput

app = FastAPI()

#human readable 
@app.get('/')
def home():
    return {'message':'Insurance Premium Prediction API'}

#machine readable
#it is used in cloud platforms like azure , aws. cloud services firstly hit this API to ensure API is working or not 
@app.get('/health')
def health():
    return {
        'status':'Ok',
        'version':MODEL_VERSION,
        'model_loaded': model is not None
    }

@app.post('/predict',response_model=PredictionResponse)
def predict_premium(data:UserInput):

    user_input = {
        'bmi':data.bmi,
        'age_group':data.age_group,
        'lifestyle_risk':data.lifestyle_risk,
        'city_tier':data.city_tier,
        'income_lpa':data.income_lpa,
        'occupation':data.occupation
    }

    try:
        prediction = predict_output(user_input)
        return JSONResponse(
            status_code=200,
            content={'predicted_category':prediction}
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                'error':str(e)
            }
        )