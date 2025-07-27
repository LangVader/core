# sistema_usuarios_productos

Proyecto de base de datos generado con Vader Database Manager usando SQLite.

## Código Vader original:
```
# Sistema de gestión de usuarios y productos
crear tabla usuarios con campos:
    - campo nombre tipo texto
    - campo email tipo texto
    - campo edad tipo número
    - campo activo tipo booleano

crear tabla productos con campos:
    - campo nombre tipo texto
    - campo descripcion tipo texto
    - campo precio tipo decimal
    - campo categoria tipo texto

# Operaciones CRUD
crear nuevo usuario con nombre "Juan" y email "juan@email.com"
leer todos los usuarios activos
actualizar usuario con id 1 cambiar nombre a "Juan Carlos"
eliminar usuario con id 2

# Consultas
buscar productos donde categoria es igual a "electrónicos"
obtener usuarios donde edad es mayor que 18
crear índice en tabla usuarios para campo email
```

## Instalación:

1. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

2. Configurar base de datos:
   - SQLite se crea automáticamente al ejecutar el código

## Uso:

```python
python3 database_manager.py
```

## Generado el: 2025-07-27 15:05:02

---
Creado con ❤️ usando Vader Database Manager
