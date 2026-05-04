# Imagen base con Python
FROM python:3.12-slim

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar primero solo requirements.txt
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código fuente
COPY src/ ./src/

# Copiar el modelo entrenado
COPY models/ ./models/

# Declara el puerto que usa la app
EXPOSE 8000

# Comando para arrancar la API
CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000"]