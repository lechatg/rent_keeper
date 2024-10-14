FROM python:3.11

RUN mkdir /fastapi_app_rent_keeper

WORKDIR /fastapi_app_rent_keeper

COPY requirements/requirements_for_docker.txt .

RUN pip install -r requirements_for_docker.txt

COPY . .

RUN chmod +x alembic_app.sh

# CMD ["gunicorn", "src.main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]

