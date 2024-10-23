# PY01 DockerRestAPI

# Red Social de Viajes
## Descripción general

Este proyecto consiste en el desarrollo del backend de una red social orientada a compartir experiencias de viaje. Los usuarios podrán realizar publicaciones sobre sus viajes, agregar destinos a sus listas de objetivos de viaje, y otros usuarios podrán interactuar mediante comentarios, likes y reacciones. Los usuarios también podrán crear y seguir listas de destinos turísticos y asociar varios lugares a sus viajes.

El proyecto utiliza una arquitectura de microservicios desplegada con Docker y Docker Compose, con bases de datos Postgres, MongoDB y Redis. Redis se emplea como caché para optimizar el rendimiento y gestionar sesiones de usuario. La autenticación se maneja con tokens de Keycloak. Además, el pipeline de CI/CD garantiza que las pruebas unitarias cubran al menos el 85% de las funcionalidades clave antes de crear las imágenes de Docker.

## Funcionalidades clave

1. **Publicaciones de viaje**:
   - Los usuarios pueden crear publicaciones con:
     - Texto: Descripción del viaje, tips, experiencias.
     - Enlaces a imágenes y videos (contenido externo).
     - Interacciones: Comentarios, likes y reacciones.

2. **Lugares de viaje**:
   - Los usuarios pueden agregar destinos turísticos que desean visitar, con:
     - Nombre, descripción, ubicación (ciudad y país).
     - Enlaces a imágenes representativas.
     - Comentarios y likes.

3. **Listas de objetivos de viaje**:
   - Los usuarios pueden crear listas de destinos que deseen visitar en el futuro, permitiendo que otros usuarios las sigan y marquen destinos propios.

4. **Sistema de comentarios**:
   - Comentarios en publicaciones y destinos.
   - Likes y reacciones en los comentarios.

5. **Viajes y lugares asociados**:
   - Los usuarios pueden crear viajes y asociar varios destinos a ellos.

## Requisitos Técnicos

1. **Modelo de datos**:
   - El modelo de datos incluye usuarios, viajes, lugares de interés, listas de objetivos de viaje, comentarios y reacciones.
   - Redis se usa como caché para posts populares y comentarios frecuentes, además de gestionar sesiones.

2. **Autenticación**:
   - La autenticación se implementa con **Keycloak**, usando tokens para manejar el acceso seguro a los servicios.

3. **Docker**:
   - El backend está contenido completamente en Docker.
   - El archivo `docker-compose.yml` incluye los servicios para el backend y las bases de datos (Postgres, MongoDB, Redis).

4. **Testing**:
   - Pruebas unitarias e integradas con una cobertura mínima del 85%.
   - Herramientas recomendadas: `pytest`, `pytest-cov`, `unittest`.
   - Cobertura para la creación y autenticación de usuarios, gestión de posts, comentarios, reacciones y listas de destinos.

5. **CI/CD**:
   - Pipeline automatizado con GitHub Actions o GitLab CI/CD que incluye:
     - Ejecución de tests en cada `push` al repositorio.
     - Verificación de cobertura mínima de 85%.
     - Creación de imágenes Docker solo si todos los tests son exitosos.
     - Publicación de la imagen en un registro como DockerHub o GitHub Container Registry.

# Comandos

### Construye y ejecuta el contenedor de Docker
```bash
docker-compose up --build
```
### Ejecuta el módulo correspondiente para las pruebas unitarias
```bash
poetry run pytest
```

# Funciones

## Usuario

### Crear usuario

**Endpoint:**
```bash
POST http://localhost:8000/usuarios/
```
**Formato del body:**
```bash
{
    "nombre": "Juan",
    "apellidos": "Perez",
    "username": "juanperez",
    "password": "securepassword",
    "fechaRegistro": "2024-10-23"
}

```
### Inicio de sesión

**Endpoint:**

```bash
POST http://localhost:8000/token/
```
**Formato del body:**
```bash

   {
    "username": "juanperez",
    "password": "securepassword"
  }

```
**Respuesta exitosa:**

```bash

{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer"
}

```

### Cerrar sesión

**Endpoint:**

```bash

POST http://localhost:8000/logout/

```

**Header:**

```bash

Authorization: Bearer <access_token>

```

## Lugares

### Crear lugar

**Endpoint:**

```bash

POST http://localhost:8000/crear_lugar/

```
**Formato del body:**
```bash

   {
    "username": "juanperez",
    "password": "securepassword"
  }

```

### Obtener lugares

**Endpoint:**

```bash

GET http://localhost:8000/lugares/


```

## Viajes

### Asociar viaje con un lugar

**Endpoint:**

```bash

POST http://localhost:8000/asociar_viaje_lugar/

```
**Formato del body:**
```bash

{
    "viajeId": 1,
    "lugaresId": [2, 3]
}

```

### Obtener viajes

**Endpoint:**

```bash

GET http://localhost:8000/viajes/

```

## Publicaciones

### Crear publicación

**Endpoint:**

```bash

POST http://localhost:8000/crear_publicacion/

```
**Formato del body:**
```bash

{
    "usuarioId": 1,
    "titulo": "Mi primer post",
    "descripcion": "Descripción de mi primera publicación",
    "fechaPublicacion": "2024-10-23"
}

```
### Obtener todas las publicaciones

**Endpoint:**

```bash

GET http://localhost:8000/publicaciones/

```
### Obtener publicación en específico 

**Endpoint:**

```bash

GET http://localhost:8000/publicaciones/{publicacion_id}


```

### Reaccionar a una publicación 

**Endpoint:**

```bash

POST http://localhost:8000/mongo/publicaciones/{publicacion_id}/reaccionar/

```
**Formato del body:**
```bash

{
    "reaccion": "Like"
}

```

### Comentar una publicación 
**Endpoint:**

```bash

POST http://localhost:8000/mongo/publicaciones/{publicacion_id}/comentar/

```
**Formato del body:**
```bash

{
    "comentario": "¡Qué gran publicación!"
}

```

