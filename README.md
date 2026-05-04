# GIAR20 MLOps Pipeline — Iris Classifier

Pipeline MLOps de extremo a extremo que entrena un modelo de clasificación, lo empaqueta como contenedor y lo despliega como API REST pública en AWS Lambda. Realizado como trabajo final de la asignatura *Metodologías de Desarrollo y Despliegue de Aplicaciones para Ciencia de Datos* (Grado en Ciencia de datos e IA, VIU, edición Abril 2026).

---

## Arquitectura

```
┌─────────────┐     git push     ┌──────────────────┐
│Desarrollador│ ───────────────► │  GitHub (main)   │
└─────────────┘                  └────────┬─────────┘
                                          │
                          ┌───────────────┴───────────────┐
                          │                               │
                          ▼                               ▼
                ┌─────────────────┐             ┌─────────────────┐
                │  Workflow CI    │             │  Workflow CD    │
                │  - pytest       │             │  - entrena      │
                │  - cobertura 70%│             │  - docker build │
                └─────────────────┘             │  - push a ECR   │
                                                │  - update Lambda│
                                                └────────┬────────┘
                                                         │
                                                         ▼
                                                ┌─────────────────┐
                                                │   AWS ECR       │
                                                │ (registro de    │
                                                │  imágenes)      │
                                                └────────┬────────┘
                                                         │
                                                         ▼
                                                ┌─────────────────┐
                                                │  AWS Lambda     │
                                                │  (FastAPI +     │
                                                │   Mangum)       │
                                                └────────┬────────┘
                                                         │
                                                         ▼
                                                ┌─────────────────┐
                                                │ Function URL    │
                                                │ (HTTPS público) │
                                                └─────────────────┘
```

---

## Stack tecnológico

| Capa | Herramientas |
|-------|-------|
| ML | scikit-learn 1.5, joblib |
| API | FastAPI, Mangum, Pydantic |
| Contenedor | Docker, AWS Lambda base image |
| CI/CD | GitHub Actions |
| Cloud | AWS (Lambda, ECR, IAM, CloudWatch) |
| IaC | Terraform |
| Testing | pytest, pytest-cov |

---

## Estructura del repositorio

```
GIAR20_MLOPS_PIPELINE/
├── .github/workflows/
│   ├── ci.yml              # tests + cobertura en push/PR
│   └── cd.yml              # build, push a ECR, update Lambda
├── infra/                  # Terraform IaC
│   ├── main.tf             # ECR + Lambda + IAM + Function URL
│   ├── variables.tf
│   ├── outputs.tf
│   └── versions.tf
├── src/
│   ├── train.py            # script de entrenamiento del modelo
│   └── api.py              # app FastAPI + handler Lambda
├── tests/
│   ├── test_train.py
│   └── test_api.py
├── models/                 # artefactos generados (gitignored)
├── Dockerfile              # imagen contenedor para Lambda
├── requirements.txt
└── README.md
```

---

## Desarrollo local

### Requisitos previos
- Python 3.12
- Docker Desktop
- AWS CLI (configurada con `aws configure`)
- Terraform >= 1.5

### Configurar el entorno

```bash
git clone https://github.com/<tu-usuario>/GIAR20_MLOPS_PIPELINE.git
cd GIAR20_MLOPS_PIPELINE
python -m venv .venv
source .venv/bin/activate         # macOS/Linux
.venv\Scripts\Activate.ps1        # Windows PowerShell
pip install -r requirements.txt
```

### Entrenar el modelo

```bash
python src/train.py
```

Genera `models/random_forest_model.joblib`. Accuracy esperada en el conjunto de test de Iris: 1.0.

### Ejecutar la API en local

```bash
uvicorn src.api:app --reload
```

Luego abre:
- `http://127.0.0.1:8000/` — health check
- `http://127.0.0.1:8000/docs` — interfaz interactiva Swagger UI

### Ejecutar los tests

```bash
pytest --cov=src --cov-report=term-missing
```

Cobertura actual: **85%** (requisito: ≥70%).

---

## Contenedorización

La imagen se basa en `public.ecr.aws/lambda/python:3.12` para que el mismo artefacto funcione en local y en Lambda.

```bash
docker build -t iris-classifier:latest .
```

El contenedor lo construye automáticamente el workflow CD; el build manual solo se necesita para depuración local.

---

## Despliegue en la nube

Toda la infraestructura está declarada en `infra/` y se aprovisiona con Terraform.

### Configuración inicial

```bash
cd infra
terraform init
terraform apply
```

Crea: repositorio ECR, rol IAM, función Lambda (basada en contenedor) y Function URL pública.

### Despliegue continuo

Cada push a `main` dispara el workflow `CD`, que:

1. Entrena el modelo en un entorno limpio (reproducibilidad).
2. Construye la imagen Docker.
3. Sube la imagen a ECR con dos etiquetas: `latest` y el SHA del commit.
4. Actualiza la función Lambda para usar la nueva imagen.

Trazabilidad: la etiqueta SHA permite rastrear cualquier contenedor en ejecución hasta el commit exacto que lo originó.

### Destruir la infraestructura

Para evitar costes en AWS tras la demo:

```bash
cd infra
terraform destroy
```

---

## Uso de la API

```bash
curl -X POST https://<tu-function-url>/predict \
     -H "Content-Type: application/json" \
     -d '{"sepal_length": 5.1, "sepal_width": 3.5, "petal_length": 1.4, "petal_width": 0.2}'
```

Respuesta:
```json
{ "prediction": 0, "class_name": "setosa" }
```

Endpoints:

| Método | Ruta       | Descripción                          |
|--------|------------|--------------------------------------|
| GET    | `/`        | Health check                         |
| POST   | `/predict` | Predicción de especie de Iris        |
| GET    | `/docs`    | Documentación OpenAPI auto-generada  |

---

## Decisiones de diseño

**Dataset Iris y Random Forest**: el foco del proyecto es el pipeline MLOps, no el modelo. Un dataset trivial con un baseline fuerte mantiene la complejidad baja y permite que las prácticas de ingeniería sean las protagonistas.

**FastAPI + Mangum**: FastAPI aporta soporte asíncrono, validación automática vía Pydantic y una Swagger UI gratuita. Mangum adapta la app ASGI al contrato de invocación de Lambda sin reescribir lógica de negocio.

**Lambda en lugar de App Runner**: AWS App Runner dejó de aceptar nuevos clientes el 30 de abril de 2026. Lambda con imágenes de contenedor se eligió como alternativa moderna y totalmente gestionada — ofrece HTTPS por defecto vía Function URLs y entra en el free tier de AWS.

**Terraform en lugar de configuración manual**: la infraestructura es reproducible. Cualquiera puede ejecutar `terraform apply` y obtener un entorno idéntico.

**Dos workflows separados (CI y CD)**: CI corre en cada push y pull request; CD solo en push a `main`. Esto mantiene el feedback rápido para desarrollo y desacopla los quality gates del despliegue.

**El artefacto del modelo no se versiona en Git**: el `.joblib` es un artefacto derivado regenerado por el pipeline de CI/CD. La fuente de verdad es el código de entrenamiento.

---

## Mejoras futuras

- Migrar a autenticación OIDC para GitHub Actions en lugar de claves de acceso de larga duración.
- Usar build Docker multi-stage para reducir el tamaño final de la imagen (~250MB frente a ~580MB actuales).
- Sustituir los `principal = "*"` por restricciones IAM más estrictas.
- Reemplazar `requirements.txt` por `pip-compile` para separar dependencias directas y transitivas.
- Añadir observabilidad: logging estructurado, métricas y trazas.
- Cambiar `image_tag_mutability` del ECR a `IMMUTABLE` y usar despliegues con SHA fijado.

---

## Autor

Richard Makov — Grado en Ciecnia de Datos e IA, Universidad Internacional de Valencia (VIU), 2025–2026.
