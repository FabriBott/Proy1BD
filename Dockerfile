# Usa una imagen base de Python
FROM python:3.11

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos de dependencias (pyproject.toml y poetry.lock) al contenedor
COPY pyproject.toml poetry.lock ./

# Instala Poetry
RUN pip install poetry

# Configura Poetry para crear el entorno virtual en el directorio del proyecto e instala las dependencias
RUN poetry config virtualenvs.create false
RUN poetry install --no-root --no-interaction --no-ansi

# Copia el resto del código de la aplicación
COPY . .

# Copiar el script de arranque y darle permisos de ejecución
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Exponer el puerto 8000 para la aplicación
EXPOSE 8000

# Usar el script de arranque como el comando principal del contenedor
ENTRYPOINT ["/entrypoint.sh"]
