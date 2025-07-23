-- CÓDIGO GENERADO POR VADER 7.0 UNIVERSAL DATABASE
-- Archivo .vdr ejecutado nativamente para SQL

-- Crear base de datos
CREATE DATABASE IF NOT EXISTS vader_database;
USE vader_database;

-- Crear tabla usuarios
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    activo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Crear tabla posts
CREATE TABLE IF NOT EXISTS posts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    contenido TEXT,
    usuario_id INT,
    publicado BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

-- Insertar datos de ejemplo
INSERT INTO usuarios (nombre, email, activo) VALUES
    ('Usuario Vader', 'usuario@vader.dev', TRUE),
    ('Admin Vader', 'admin@vader.dev', TRUE);

INSERT INTO posts (titulo, contenido, usuario_id, publicado) VALUES
    ('Introducción a Vader', 'Vader es el lenguaje universal', 1, TRUE),
    ('Bases de datos con Vader', 'Gestionar datos nunca fue tan fácil', 1, TRUE);

-- Consultas de ejemplo
SELECT * FROM usuarios WHERE activo = TRUE;
SELECT u.nombre, COUNT(p.id) as total_posts 
FROM usuarios u 
LEFT JOIN posts p ON u.id = p.usuario_id 
GROUP BY u.id;

-- Crear índices
CREATE INDEX idx_usuarios_email ON usuarios(email);
CREATE INDEX idx_posts_usuario_id ON posts(usuario_id);
