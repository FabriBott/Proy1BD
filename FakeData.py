from faker import Faker
from models.adminToken import adminToken

import app
from models.createUser import UserCreate
fake = Faker()

def generar_usuario() -> UserCreate:
    return UserCreate(
        username=fake.user_name(),
        email=fake.email(),
        password=fake.password(),
        firstname=fake.first_name(),
        lastname=fake.last_name()
        )


for i in range(5):
    app.create_user(generar_usuario())