# Usa una imagen base de Python
FROM python:3.11

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos de dependencias (pyproject.toml y poetry.lock) al contenedor
COPY pyproject.toml poetry.lock ./

# Instala Poetry
RUN pip install poetry

# Configura Poetry para crear el entorno virtual en el directorio del proyecto e instala las dependencias
# Configura Poetry para crear el entorno virtual en el directorio del proyecto
RUN poetry config virtualenvs.create false
# Instala las dependencias sin instalar el propio proyecto (--no-root)
RUN poetry install --no-root --no-interaction --no-ansi

# Copia el resto del código de la aplicación
COPY . .

# Exponer el puerto 8000 para la aplicación
EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "app:app", "--host=0.0.0.0", "--port=8000"]
