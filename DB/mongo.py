import os
from pymongo import MongoClient

# Inicializar MongoDB
def init_mongo():
    try:
        mongo_client = MongoClient(
            f"mongodb://{os.getenv('MONGO_INITDB_ROOT_USERNAME', 'root')}:{os.getenv('MONGO_INITDB_ROOT_PASSWORD', 'root')}@{os.getenv('MONGO_HOST', 'mongo')}:27017"
        )
        db = mongo_client["red_social_viajes"]
        print("Conectado exitosamente a MongoDB")
        return db
    except Exception as e:
        print(f"Error al conectar a MongoDB: {e}")
