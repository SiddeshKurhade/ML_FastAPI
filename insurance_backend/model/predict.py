#load the model
import pickle
import pandas as pd

with open('model/model.pkl','rb') as f:
    model = pickle.load(f)

#right now we take our own version 
#but ML gives us the model version from MLFLow 
MODEL_VERSION = '1.0.0'

#Get class labels from model (important for matching probabilities to class names)
class_labels = model.classes_.tolist()

def predict_output(user_input:dict):

    input_df = pd.DataFrame([user_input])
    output = model.predict(input_df)[0]

    #Get probabilities for all classes 
    probabilities = model.predict_proba(input_df)[0]
    confidence  = max(probabilities)

    #create mapping: {class_name : probability}
    class_probs = dict(zip(class_labels,map(lambda p : round(p,4),probabilities)))
    
    return {
        'predicted_category':output,
        'confidence':round(confidence,4),
        'class_probabilities':class_probs
    }