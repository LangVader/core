#!/usr/bin/env python3
"""
Código Python generado para interactuar con SQLite
"""

import sqlite3
from datetime import datetime
from typing import List, Dict, Optional

class DatabaseManager:
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.connection = None
    
    def connect(self):
        """Conectar a la base de datos"""
        try:
            self.connection = sqlite3.connect(self.connection_string)
            self.connection.row_factory = sqlite3.Row
            print(f"✅ Conectado a {database_type}")
        except Exception as e:
            print(f"❌ Error conectando a la base de datos: {e}")
            raise
    
    def disconnect(self):
        """Desconectar de la base de datos"""
        if self.connection:
            self.connection.close()
            print("🔌 Desconectado de la base de datos")
    
    def execute_query(self, query: str, params: tuple = None) -> List[Dict]:
        """Ejecutar consulta SELECT"""
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params or ())
            
            # Obtener nombres de columnas
            columns = [description[0] for description in cursor.description]
            
            # Obtener resultados
            rows = cursor.fetchall()
            
            # Convertir a lista de diccionarios
            results = []
            for row in rows:
                results.append(dict(zip(columns, row)))
            
            cursor.close()
            return results
            
        except Exception as e:
            print(f"❌ Error ejecutando consulta: {e}")
            raise
    
    def execute_command(self, command: str, params: tuple = None) -> int:
        """Ejecutar comando INSERT, UPDATE, DELETE"""
        try:
            cursor = self.connection.cursor()
            cursor.execute(command, params or ())
            
            affected_rows = cursor.rowcount
            self.connection.commit()
            cursor.close()
            
            return affected_rows
            
        except Exception as e:
            print(f"❌ Error ejecutando comando: {e}")
            self.connection.rollback()
            raise


class UsuariosManager(DatabaseManager):
    """Gestor para la tabla usuarios"""
    
    def crear_usuarios(self, nombre: str, descripcion: str = None) -> int:
        """Crear nuevo registro en usuarios"""
        query = """
        INSERT INTO usuarios (nombre, descripcion, fecha_creacion, activo)
        VALUES (?, ?, ?, ?)
        """
        params = (nombre, descripcion, datetime.now(), True)
        return self.execute_command(query, params)
    
    def obtener_usuarios(self, id: int = None) -> List[Dict]:
        """Obtener registros de usuarios"""
        if id:
            query = "SELECT * FROM usuarios WHERE id = ?"
            params = (id,)
        else:
            query = "SELECT * FROM usuarios WHERE activo = ?"
            params = (True,)
        
        return self.execute_query(query, params)
    
    def actualizar_usuarios(self, id: int, nombre: str = None, descripcion: str = None) -> int:
        """Actualizar registro en usuarios"""
        updates = []
        params = []
        
        if nombre:
            updates.append("nombre = ?")
            params.append(nombre)
        
        if descripcion:
            updates.append("descripcion = ?")
            params.append(descripcion)
        
        if not updates:
            return 0
        
        params.append(id)
        query = f"UPDATE usuarios SET {', '.join(updates)} WHERE id = ?"
        
        return self.execute_command(query, tuple(params))
    
    def eliminar_usuarios(self, id: int, soft_delete: bool = True) -> int:
        """Eliminar registro de usuarios"""
        if soft_delete:
            query = f"UPDATE usuarios SET activo = ? WHERE id = ?"
            params = (False, id)
        else:
            query = f"DELETE FROM usuarios WHERE id = ?"
            params = (id,)
        
        return self.execute_command(query, params)

class ProductosManager(DatabaseManager):
    """Gestor para la tabla productos"""
    
    def crear_productos(self, nombre: str, descripcion: str = None) -> int:
        """Crear nuevo registro en productos"""
        query = """
        INSERT INTO productos (nombre, descripcion, fecha_creacion, activo)
        VALUES (?, ?, ?, ?)
        """
        params = (nombre, descripcion, datetime.now(), True)
        return self.execute_command(query, params)
    
    def obtener_productos(self, id: int = None) -> List[Dict]:
        """Obtener registros de productos"""
        if id:
            query = "SELECT * FROM productos WHERE id = ?"
            params = (id,)
        else:
            query = "SELECT * FROM productos WHERE activo = ?"
            params = (True,)
        
        return self.execute_query(query, params)
    
    def actualizar_productos(self, id: int, nombre: str = None, descripcion: str = None) -> int:
        """Actualizar registro en productos"""
        updates = []
        params = []
        
        if nombre:
            updates.append("nombre = ?")
            params.append(nombre)
        
        if descripcion:
            updates.append("descripcion = ?")
            params.append(descripcion)
        
        if not updates:
            return 0
        
        params.append(id)
        query = f"UPDATE productos SET {', '.join(updates)} WHERE id = ?"
        
        return self.execute_command(query, tuple(params))
    
    def eliminar_productos(self, id: int, soft_delete: bool = True) -> int:
        """Eliminar registro de productos"""
        if soft_delete:
            query = f"UPDATE productos SET activo = ? WHERE id = ?"
            params = (False, id)
        else:
            query = f"DELETE FROM productos WHERE id = ?"
            params = (id,)
        
        return self.execute_command(query, params)

class UsuariosManager(DatabaseManager):
    """Gestor para la tabla usuarios"""
    
    def crear_usuarios(self, nombre: str, descripcion: str = None) -> int:
        """Crear nuevo registro en usuarios"""
        query = """
        INSERT INTO usuarios (nombre, descripcion, fecha_creacion, activo)
        VALUES (?, ?, ?, ?)
        """
        params = (nombre, descripcion, datetime.now(), True)
        return self.execute_command(query, params)
    
    def obtener_usuarios(self, id: int = None) -> List[Dict]:
        """Obtener registros de usuarios"""
        if id:
            query = "SELECT * FROM usuarios WHERE id = ?"
            params = (id,)
        else:
            query = "SELECT * FROM usuarios WHERE activo = ?"
            params = (True,)
        
        return self.execute_query(query, params)
    
    def actualizar_usuarios(self, id: int, nombre: str = None, descripcion: str = None) -> int:
        """Actualizar registro en usuarios"""
        updates = []
        params = []
        
        if nombre:
            updates.append("nombre = ?")
            params.append(nombre)
        
        if descripcion:
            updates.append("descripcion = ?")
            params.append(descripcion)
        
        if not updates:
            return 0
        
        params.append(id)
        query = f"UPDATE usuarios SET {', '.join(updates)} WHERE id = ?"
        
        return self.execute_command(query, tuple(params))
    
    def eliminar_usuarios(self, id: int, soft_delete: bool = True) -> int:
        """Eliminar registro de usuarios"""
        if soft_delete:
            query = f"UPDATE usuarios SET activo = ? WHERE id = ?"
            params = (False, id)
        else:
            query = f"DELETE FROM usuarios WHERE id = ?"
            params = (id,)
        
        return self.execute_command(query, params)

# Ejemplo de uso
if __name__ == '__main__':
    # Configurar conexión
    db_path = "mi_base_datos.db"
    
    try:
        # Gestor para usuarios
        usuarios_manager = UsuariosManager(db_path)
        usuarios_manager.connect()
        
        # Crear registro
        nuevo_id = usuarios_manager.crear_usuarios("Ejemplo", "Descripción de ejemplo")
        print(f"Nuevo usuarios creado con ID: {nuevo_id}")
        
        # Obtener registros
        registros = usuarios_manager.obtener_usuarios()
        print(f"Registros en usuarios: {len(registros)}")
        
        usuarios_manager.disconnect()
        
        # Gestor para productos
        productos_manager = ProductosManager(db_path)
        productos_manager.connect()
        
        # Crear registro
        nuevo_id = productos_manager.crear_productos("Ejemplo", "Descripción de ejemplo")
        print(f"Nuevo productos creado con ID: {nuevo_id}")
        
        # Obtener registros
        registros = productos_manager.obtener_productos()
        print(f"Registros en productos: {len(registros)}")
        
        productos_manager.disconnect()
        
        # Gestor para usuarios
        usuarios_manager = UsuariosManager(db_path)
        usuarios_manager.connect()
        
        # Crear registro
        nuevo_id = usuarios_manager.crear_usuarios("Ejemplo", "Descripción de ejemplo")
        print(f"Nuevo usuarios creado con ID: {nuevo_id}")
        
        # Obtener registros
        registros = usuarios_manager.obtener_usuarios()
        print(f"Registros en usuarios: {len(registros)}")
        
        usuarios_manager.disconnect()
        
    except Exception as e:
        print(f"Error: {e}")
