from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import numpy as np

# Define the input model for the API
class InputModel(BaseModel):
    humidity: float
    temperature: float
    rainfall: float
    risk_factor: float
    altitude: float
# uvicorn main:app --reload
# Initialize the FastAPI app
app = FastAPI()

# Allow CORS for all origins, so the API can be called from the frontend
origins = [
    "*"
]

# Load the pre-trained flood prediction model
model = joblib.load('flood_classification_model.pkl')

# Add CORS middleware to allow cross-origin requests
app.add_middleware(CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the prediction route
@app.post('/predict')
async def predict_fn(input: InputModel):
    # Extract input values from the request and prepare them for prediction
    input_data = [[
        input.humidity, 
        input.temperature, 
        input.rainfall, 
        input.risk_factor, 
        input.altitude
    ]]
    
    # Convert input data into a numpy array (if necessary)
    input_array = np.array(input_data)
    # print(input_array)
    
    # Predict the flood probability using the model (0: No Flood, 1: Flood)
    flood_probabilities = model.predict_proba(input_array)
    
    # Extract probabilities for both 'No Flood' and 'Flood'
    no_flood_prob = flood_probabilities[0][0]
    flood_prob = flood_probabilities[0][1]
    
    # Return the prediction result as a JSON response
    return {
        "Probability of No Flood": no_flood_prob,
        "Probability of Flood": flood_prob
    }
