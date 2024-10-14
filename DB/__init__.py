from .postgres import init_postgres
from .redis import init_redis
from .mongo import init_mongo

# Inicializar todas las bases de datos
def init_databases():
    init_postgres()
    init_redis()
    init_mongo()
