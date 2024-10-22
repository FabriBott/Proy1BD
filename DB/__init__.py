from postgres import init_postgres
from redis import init_redis
from mongo import init_mongo

# Inicializar todas las bases de datos
def init_databases():
    postgres = init_postgres()
    redis = init_redis()
    mongo = init_mongo()
    return {"Postgres": postgres, "Redis": redis, "Mongo": mongo}
