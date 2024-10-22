import os
import redis

# Inicializar Redis
def init_redis():
    try:
        redis_client = redis.StrictRedis(
            host=os.getenv("REDIS_HOST", "redis"),
            port=os.getenv("REDIS_PORT", 6379),
            decode_responses=True
        )
        redis_client.ping()
        print("Conectado exitosamente a Redis")
        return redis_client
    except Exception as e:
        print(f"Error al conectar a Redis: {e}")
        return None
