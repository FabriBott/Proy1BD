import os
import redis

# Inicializar Redis
def init_redis():
    try:
        # Cargar configuraciones de entorno con valores por defecto
        host = os.getenv("REDIS_HOST", "redis")
        port = int(os.getenv("REDIS_PORT", 6379))
        db = int(os.getenv("REDIS_DB", 0))  # Puedes usar varios DBs en Redis

        # Crear el cliente de Redis
        redis_client = redis.StrictRedis(
            host=host,
            port=port,
            db=db,
            decode_responses=True,
            socket_timeout=5  # Tiempo máximo de espera para conectar
        )
        
        # Verificar si la conexión está activa
        redis_client.ping()  
        print(f"Conectado exitosamente a Redis en {host}:{port}")
        return redis_client
    except redis.ConnectionError as e:
        print(f"Error de conexión a Redis: {e}")
    except Exception as e:
        print(f"Error inesperado al conectar a Redis: {e}")
        return None

