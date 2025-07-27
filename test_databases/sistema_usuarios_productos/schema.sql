-- Esquema generado desde código Vader
-- Base de datos: SQLite
-- Generado el: 2025-07-27 15:05:02


-- Tabla: usuarios
CREATE TABLE usuarios (
    id INTEGER PRIMARY KEY ,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    activo BOOLEAN DEFAULT TRUE
);


-- Tabla: productos
CREATE TABLE productos (
    id INTEGER PRIMARY KEY ,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    activo BOOLEAN DEFAULT TRUE
);


-- Tabla: usuarios
CREATE TABLE usuarios (
    id INTEGER PRIMARY KEY ,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    activo BOOLEAN DEFAULT TRUE
);

