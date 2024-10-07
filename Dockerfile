FROM python:3.11

WORKDIR  /app


RUN pip install poetry

COPY . .

RUN poetry install  

EXPOSE 8000

# Command to run the application
CMD [ "poetry","run","uvicorn","app:app","--host=0.0.0.0" ]