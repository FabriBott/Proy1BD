CREATE DATABASE RedSocial
    WITH 
    ENCODING = 'UTF8'
    LC_COLLATE = 'es_ES.UTF-8'
    LC_CTYPE = 'es_ES.UTF-8'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;

CREATE TABLE "Usuarios" (
  "identificador" SERIAL PRIMARY KEY,
  "nombre" VARCHAR(25),
  "apellidos" VARCHAR(40),
  "username" VARCHAR(20),
  "password" VARCHAR(255),
  "fechaRegistro" TIMESTAMP
);

CREATE TABLE "Publicaciones" (
  "identificador" SERIAL PRIMARY KEY,
  "usuarioId" INTEGER,
  "titulo" VARCHAR(100),
  "descripcion" TEXT,
  "fechaPublicacion" TIMESTAMP,
  CONSTRAINT "FK_Publicaciones_usuarioId"
    FOREIGN KEY ("usuarioId")
      REFERENCES "Usuarios"("identificador") ON DELETE CASCADE
);

CREATE TABLE "Lugares" (
  "identificador" SERIAL PRIMARY KEY,
  "usuarioId" INTEGER,
  "nombre" VARCHAR(100),
  "descripcion" TEXT,
  "ciudad" VARCHAR(100),
  "pais" VARCHAR(75),
  "fechaCreacion" TIMESTAMP,
  CONSTRAINT "FK_Lugares_usuarioId"
    FOREIGN KEY ("usuarioId")
      REFERENCES "Usuarios"("identificador") ON DELETE CASCADE
);

CREATE TABLE "Viajes" (
  "identificador" SERIAL PRIMARY KEY,
  "usuarioId" INTEGER,
  "fechaInicio" DATE,
  "fechaFinal" DATE,
  CONSTRAINT "FK_Viajes_usuarioId"
    FOREIGN KEY ("usuarioId")
      REFERENCES "Usuarios"("identificador") ON DELETE CASCADE
);

CREATE TABLE "Viajes_Lugares" (
  "identificador" SERIAL PRIMARY KEY,
  "viajeId" INTEGER,
  "lugaresId" INTEGER,
  CONSTRAINT "FK_Viajes_Lugares_viajeId"
    FOREIGN KEY ("viajeId")
      REFERENCES "Viajes"("identificador") ON DELETE CASCADE,
  CONSTRAINT "FK_Viajes_Lugares_lugaresId"
    FOREIGN KEY ("lugaresId")
      REFERENCES "Lugares"("identificador") ON DELETE CASCADE
);