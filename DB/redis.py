import os
import redis

class RedisClient:
    def __init__(self):
        self.redis_client = None
        self._connect()

    def _connect(self):
        try:
            # Cargar configuraciones de entorno con valores por defecto
            host = os.getenv("REDIS_HOST", "redis")
            port = int(os.getenv("REDIS_PORT", 6379))
            db = int(os.getenv("REDIS_DB", 0))  # Puedes usar varios DBs en Redis
            self.redis_client = redis.StrictRedis(
                host=host,
                port=port,
                db=db,
                decode_responses=True,
                socket_timeout=5  # Tiempo máximo de espera para conectar
            )
            self.redis_client.ping()  # Verificar si la conexión está activa
            print(f"Conectado exitosamente a Redis en {host}:{port}")
        except redis.ConnectionError as e:
            print(f"Error de conexión a Redis: {e}")
        except Exception as e:
            print(f"Error inesperado al conectar a Redis: {e}")

    def get_client(self):
        if not self.redis_client:
            self._connect()
        return self.redis_client
