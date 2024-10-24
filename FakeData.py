import app
from faker import Faker

from models.createUser import UserCreate
fake = Faker()


#Modificando estas constantes se cambia la cantidad de datos iniciales
USERSCOUNT = 5000
PLACESCOUNT = 1
POSTSCOUNT = 1
COMMENTSCOUNT = 1
REACTIONSCOUNT = 1


#Crear una funcion que haga el dato sintetico
def generar_usuario() -> UserCreate:
    return UserCreate(
        username=fake.user_name(),
        email=fake.email(),
        password=fake.password(),
        firstname=fake.first_name(),
        lastname=fake.last_name()
        )



#Hacer un loop que invoque la funcion, NO EL ENDPOINT para la insercion del dato que se ocupe
for i in range(USERSCOUNT):
    app.create_user(generar_usuario())