from fastapi.testclient import TestClient
from src.api import app

client = TestClient(app)


def test_root_endpoint():
    """El endpoint raíz debe responder con status ok."""
    response = client.get("/")
    assert response.status_code == 200, f"Status code debe ser 200, pero es {response.status_code}"
    assert response.json()["status"] == "ok", f'Status debe ser "ok", pero es {response.json()["status"]}'

def test_predict_setosa():
    """Con valores típicos de setosa, debe predecir clase 0."""
    payload = {
        "sepal_length": 5.1,
        "sepal_width": 3.5,
        "petal_length": 1.4,
        "petal_width": 0.2,
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200, f"Status code debe ser 200, pero es {response.status_code}"
    assert response.json()["prediction"] == 0, f'Prediction debe ser 0, pero es {response.json()["prediction"]}'
    assert response.json()["class_name"] == "setosa", f'Class name debe ser "setosa", pero es {response.json()["class_name"]}'


def test_predict_virginica():
    """Con valores típicos de virginica, debe predecir clase 2."""
    payload = {
        "sepal_length": 6.3,
        "sepal_width": 3.3,
        "petal_length": 6.0,
        "petal_width": 2.5,
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200, f"Status code debe ser 200, pero es {response.status_code}"
    assert response.json()["prediction"] == 2, f'Prediction debe ser 2, pero es {response.json()["prediction"]}'
    assert response.json()["class_name"] == "virginica", f'Class name debe ser "virginica", pero es {response.json()["class_name"]}'

def test_predict_invalid_input():
    """Si falta un campo, debe devolver error 422."""
    payload = {
        "sepal_length": 5.1,
        "sepal_width": 3.5,
        "petal_length": 1.4,
        # "petal_width" falta
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 422, f"Status code debe ser 422, pero es {response.status_code}"