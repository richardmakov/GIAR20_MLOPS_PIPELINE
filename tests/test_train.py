from src.train import load_data, train_model, evaluate_model
from sklearn.model_selection import train_test_split

def test_load_data_returns_correct_shapes():
    """Iris debe tener 150 muestras y 4 features."""
    X, y = load_data()
    assert X.shape[0] == 150, "X debe tener 150 filas"
    assert X.shape[1] == 4, "X debe tener 4 columnas"
    assert y.shape[0] == 150, "y debe tener 150 elementos"

def test_train_model_returns_fitted_model():
    """El modelo entrenado debe poder hacer predicciones."""
    X, y = load_data()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    assert len(predictions) == len(X_test)

def test_evaluate_model_returns_high_accuracy():
    """En Iris debemos sacar al menos 0.9 de accuracy."""
    X, y = load_data()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = train_model(X_train, y_train)
    accuracy = evaluate_model(model, X_test, y_test)
    assert accuracy >= 0.9, f"Accuracy debe ser >= 0.9, pero es {accuracy}"
    assert accuracy <= 1.0, f"Accuracy debe ser <= 1.0, pero es {accuracy}"