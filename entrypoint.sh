#!/bin/bash

# Arrancar uvicorn en segundo plano
poetry run uvicorn app:app --host=0.0.0.0 --port=8000 &

# Esperar un par de segundos para asegurarse de que uvicorn ha levantado correctamente
sleep 70

# Ejecutar el script de generación de datos falsos
poetry run python FakeData.py

# Esperar para siempre para mantener el contenedor corriendo
wait
