from time import sleep
import app
from faker import Faker
import random
from datetime import timedelta

from models.createUser import UserCreate
from models.lugar_schema import LugarCreate
from models.publicacion_schema import PublicacionCreate
from models.viaje_lugar_schema import ViajeLugarCreate
from models.viaje_schema import ViajeCreate
fake = Faker()


#Modificando estas constantes se cambia la cantidad de datos iniciales
USERSCOUNT = 50
PLACESCOUNT = 10
POSTSCOUNT = 100
COMMENTSCOUNT = 500
REACTIONSCOUNT = 100


#Crear una funcion que haga el dato sintetico
def generar_usuario() -> UserCreate:
    return UserCreate(
        username=fake.user_name(),
        email=fake.email(),
        password=fake.password(),
        firstname=fake.first_name(),
        lastname=fake.last_name()
        )

def generarLugar():
    nombre = fake.city()
    lugar =  LugarCreate(
        usuarioId = random.randint(1, USERSCOUNT),
        nombre = nombre,
        descripcion = fake.sentence(),
        ciudad = nombre,
        pais = fake.country()
    )
    return lugar

def generarViaje():
    inicio = fake.date_time_this_decade()
    fin = inicio + timedelta(days=fake.random_int(min=1, max=10))
    return ViajeCreate(
        usuarioId = random.randint(1, USERSCOUNT),
        fechaInicio=inicio,
        fechaFinal=fin
    )
    
def asociarViajeLugar(idViaje):
    return ViajeLugarCreate(
        viajeId=idViaje,
        lugaresId=random.randint(1, PLACESCOUNT)
    )

from datetime import datetime

def generar_publicacion() -> PublicacionCreate:
    return PublicacionCreate(
        usuarioId=str(random.randint(1, USERSCOUNT)),  # Convertir a string
        titulo=fake.sentence(),
        descripcion=fake.paragraph(),  # Añadir descripción
        imageLinks=[fake.image_url() for _ in range(3)],  # Lista de URLs de imágenes simuladas
        videoLinks=[fake.url() for _ in range(2)],  # Lista de URLs de videos simulados
        fechaPublicacion=datetime.now().isoformat(),  # Fecha de publicación en formato ISO
        comentarios=[fake.sentence() for _ in range(5)],  # Lista de comentarios simulados
        reacciones=[fake.word() for _ in range(3)]  # Lista de reacciones simuladas
    )


def generar_comentario():
    return {
        "usuarioId":random.randint(1, USERSCOUNT),
        "contenido":fake.sentence()
    }

def generar_reaccion(post_id) -> dict:
    return {
        "usuarioId": random.randint(1, USERSCOUNT),
        "postId": post_id,
        "tipoReaccion": random.choice(["like", "love", "haha", "wow", "sad", "angry"])
    }


print("Started to generate data...")

#Hacer un loop que invoque la funcion, NO EL ENDPOINT para la insercion del dato que se ocupe
for i in range(USERSCOUNT):
    app.create_user(generar_usuario())
    sleep(1)

print("Usuarios generados")
        
for i in range(PLACESCOUNT):
    app.crear_lugar_endpoint(generarLugar())

print("Lugares generados")
    

for i in range(POSTSCOUNT):
    # Crear una publicación
    post_data = generar_publicacion()
    post_id = app.crear_publicacion_mongo_endpoint(post_data)
    
    # Agregar comentarios a la publicación
    #for _ in range(random.randint(1, 10)):
    #    app.agregar_comentarioM(post_id, generar_comentario())
    
    # Agregar reacciones a la publicación
    #for _ in range(random.randint(1, 20)):
    #    app.agregar_reaccionM(generar_reaccion(post_id))
