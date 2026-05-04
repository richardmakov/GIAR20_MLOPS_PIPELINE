import joblib
import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel
from mangum import Mangum

app = FastAPI(title="Iris Classifier API", version="1.0.0")
handler = Mangum(app, lifespan="off")

model = joblib.load("models/random_forest_model.joblib")

CLASS_NAMES = ["setosa", "versicolor", "virginica"]
class IrisFeatures(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

@app.get("/")
def root():
    return {"status": "ok", "service": "iris-classifier"}

@app.post("/predict")
def predict(features: IrisFeatures):
    X =  np.array([[features.sepal_length, features.sepal_width, features.petal_length, features.petal_width]])

    prediction = model.predict(X)[0]

    class_name = CLASS_NAMES[prediction]

    return {
        "prediction": int(prediction),
        "class_name": class_name,
    }