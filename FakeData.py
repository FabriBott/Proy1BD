import app
from faker import Faker
import random
from datetime import timedelta

from models.createUser import UserCreate
from models.lugar_schema import LugarCreate
from models.viaje_lugar_schema import ViajeLugarCreate
from models.viaje_schema import ViajeCreate
fake = Faker()


#Modificando estas constantes se cambia la cantidad de datos iniciales
USERSCOUNT = 5000
PLACESCOUNT = 1000
POSTSCOUNT = 10000
COMMENTSCOUNT = 50000
REACTIONSCOUNT = 100000


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
    return LugarCreate(
        usuarioId = random.randint(1, USERSCOUNT),
        nombre = nombre,
        descripcion = fake.sentence(),
        ciudad = nombre,
        pais = fake.country()
    )

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


#Hacer un loop que invoque la funcion, NO EL ENDPOINT para la insercion del dato que se ocupe
for i in range(USERSCOUNT):
    app.create_user(generar_usuario())
    
for i in range(PLACESCOUNT):
    app.crear_lugar_endpoint(generarLugar())
    for j in range(random.randint(3,10)):
        app.asociar_viaje_lugar_endpoint(asociarViajeLugar(i))
    

for i in range(POSTSCOUNT):
    app.crear_viaje_endpoint(generarViaje())
    

for i in range(COMMENTSCOUNT):
    
    pass