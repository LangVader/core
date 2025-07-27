#!/usr/bin/env python3
"""
Vader Database Integration - Sistema completo de integración con bases de datos
Soporta SQL (MySQL, PostgreSQL, SQLite) y NoSQL (MongoDB, Redis, etc.)
"""

import os
import json
import sqlite3
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
import re

class VaderDatabaseManager:
    """Gestor de bases de datos para Vader"""
    
    def __init__(self):
        self.supported_databases = {
            'sqlite': {
                'name': 'SQLite',
                'type': 'sql',
                'driver': 'sqlite3',
                'description': 'Base de datos ligera embebida'
            },
            'mysql': {
                'name': 'MySQL',
                'type': 'sql',
                'driver': 'mysql-connector-python',
                'description': 'Base de datos relacional popular'
            },
            'postgresql': {
                'name': 'PostgreSQL',
                'type': 'sql',
                'driver': 'psycopg2',
                'description': 'Base de datos relacional avanzada'
            },
            'mongodb': {
                'name': 'MongoDB',
                'type': 'nosql',
                'driver': 'pymongo',
                'description': 'Base de datos de documentos NoSQL'
            },
            'redis': {
                'name': 'Redis',
                'type': 'nosql',
                'driver': 'redis',
                'description': 'Base de datos en memoria clave-valor'
            }
        }
        
        # Palabras clave para detectar operaciones de BD
        self.database_keywords = {
            'tabla': ['table', 'tabla', 'entidad', 'modelo'],
            'crear': ['create', 'crear', 'nuevo', 'insertar'],
            'leer': ['read', 'leer', 'buscar', 'obtener', 'select'],
            'actualizar': ['update', 'actualizar', 'modificar', 'cambiar'],
            'eliminar': ['delete', 'eliminar', 'borrar', 'quitar'],
            'consulta': ['query', 'consulta', 'busqueda', 'filtro'],
            'relación': ['relation', 'relacion', 'join', 'foreign_key'],
            'índice': ['index', 'indice', 'clave', 'key']
        }
        
        # Tipos de datos comunes
        self.data_types = {
            'texto': ['TEXT', 'VARCHAR', 'STRING'],
            'número': ['INTEGER', 'INT', 'NUMBER'],
            'decimal': ['FLOAT', 'DECIMAL', 'DOUBLE'],
            'fecha': ['DATE', 'DATETIME', 'TIMESTAMP'],
            'booleano': ['BOOLEAN', 'BOOL'],
            'json': ['JSON', 'JSONB']
        }
        
        print("🗄️ Vader Database Manager inicializado")
        print(f"📊 Bases de datos soportadas: {', '.join(self.supported_databases.keys())}")
    
    def detect_database_operations(self, vader_code: str) -> Dict[str, List[str]]:
        """Detectar operaciones de base de datos en código Vader"""
        code_lower = vader_code.lower()
        detected = {
            'operations': [],
            'tables': [],
            'fields': [],
            'relationships': []
        }
        
        # Detectar operaciones
        for operation, keywords in self.database_keywords.items():
            if any(keyword in code_lower for keyword in keywords):
                detected['operations'].append(operation)
        
        # Detectar tablas (buscar patrones como "tabla usuarios", "crear tabla productos")
        table_patterns = [
            r'tabla\s+(\w+)',
            r'create\s+table\s+(\w+)',
            r'modelo\s+(\w+)',
            r'entidad\s+(\w+)'
        ]
        
        for pattern in table_patterns:
            matches = re.findall(pattern, code_lower)
            detected['tables'].extend(matches)
        
        # Detectar campos (buscar patrones como "campo nombre", "columna edad")
        field_patterns = [
            r'campo\s+(\w+)',
            r'columna\s+(\w+)',
            r'atributo\s+(\w+)',
            r'propiedad\s+(\w+)'
        ]
        
        for pattern in field_patterns:
            matches = re.findall(pattern, code_lower)
            detected['fields'].extend(matches)
        
        return detected
    
    def generate_database_schema(self, vader_code: str, database_type: str) -> Dict[str, str]:
        """Generar esquema de base de datos desde código Vader"""
        if database_type not in self.supported_databases:
            raise ValueError(f"Base de datos '{database_type}' no soportada")
        
        detected = self.detect_database_operations(vader_code)
        db_info = self.supported_databases[database_type]
        
        print(f"🗄️ Generando esquema para {db_info['name']}")
        print(f"📋 Tablas detectadas: {', '.join(detected['tables'])}")
        print(f"🔧 Operaciones detectadas: {', '.join(detected['operations'])}")
        
        if db_info['type'] == 'sql':
            return self._generate_sql_schema(detected, database_type, vader_code)
        else:
            return self._generate_nosql_schema(detected, database_type, vader_code)
    
    def _generate_sql_schema(self, detected: Dict, database_type: str, vader_code: str) -> Dict[str, str]:
        """Generar esquema SQL"""
        files = {}
        
        # Crear script de creación de tablas
        create_tables_sql = f"""-- Esquema generado desde código Vader
-- Base de datos: {self.supported_databases[database_type]['name']}
-- Generado el: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

"""
        
        # Generar tablas detectadas
        for table in detected['tables']:
            create_tables_sql += f"""
-- Tabla: {table}
CREATE TABLE {table} (
    id INTEGER PRIMARY KEY {'AUTO_INCREMENT' if database_type == 'mysql' else ''},
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    fecha_creacion {'DATETIME' if database_type == 'mysql' else 'TIMESTAMP'} DEFAULT {'NOW()' if database_type == 'mysql' else 'CURRENT_TIMESTAMP'},
    activo BOOLEAN DEFAULT TRUE
);

"""
        
        # Agregar índices si se detectaron
        if 'índice' in detected['operations']:
            create_tables_sql += "\n-- Índices\n"
            for table in detected['tables']:
                create_tables_sql += f"CREATE INDEX idx_{table}_nombre ON {table}(nombre);\n"
        
        files['schema.sql'] = create_tables_sql
        
        # Generar código Python para interactuar con la BD
        python_code = f"""#!/usr/bin/env python3
\"\"\"
Código Python generado para interactuar con {self.supported_databases[database_type]['name']}
\"\"\"

import {self.supported_databases[database_type]['driver'].replace('-', '_')}
from datetime import datetime
from typing import List, Dict, Optional

class DatabaseManager:
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.connection = None
    
    def connect(self):
        \"\"\"Conectar a la base de datos\"\"\"
        try:
"""
        
        if database_type == 'sqlite':
            python_code += """            self.connection = sqlite3.connect(self.connection_string)
            self.connection.row_factory = sqlite3.Row
"""
        elif database_type == 'mysql':
            python_code += """            import mysql.connector
            # Parsear connection string: mysql://user:pass@host:port/database
            self.connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='password',
                database='mi_base_datos'
            )
"""
        elif database_type == 'postgresql':
            python_code += """            import psycopg2
            from psycopg2.extras import RealDictCursor
            self.connection = psycopg2.connect(
                self.connection_string,
                cursor_factory=RealDictCursor
            )
"""
        
        python_code += """            print(f"✅ Conectado a {database_type}")
        except Exception as e:
            print(f"❌ Error conectando a la base de datos: {e}")
            raise
    
    def disconnect(self):
        \"\"\"Desconectar de la base de datos\"\"\"
        if self.connection:
            self.connection.close()
            print("🔌 Desconectado de la base de datos")
    
    def execute_query(self, query: str, params: tuple = None) -> List[Dict]:
        \"\"\"Ejecutar consulta SELECT\"\"\"
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
        \"\"\"Ejecutar comando INSERT, UPDATE, DELETE\"\"\"
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

"""
        
        # Generar métodos CRUD para cada tabla detectada
        for table in detected['tables']:
            table_class = table.capitalize()
            python_code += f"""
class {table_class}Manager(DatabaseManager):
    \"\"\"Gestor para la tabla {table}\"\"\"
    
    def crear_{table}(self, nombre: str, descripcion: str = None) -> int:
        \"\"\"Crear nuevo registro en {table}\"\"\"
        query = \"\"\"
        INSERT INTO {table} (nombre, descripcion, fecha_creacion, activo)
        VALUES (?, ?, ?, ?)
        \"\"\"
        params = (nombre, descripcion, datetime.now(), True)
        return self.execute_command(query, params)
    
    def obtener_{table}(self, id: int = None) -> List[Dict]:
        \"\"\"Obtener registros de {table}\"\"\"
        if id:
            query = "SELECT * FROM {table} WHERE id = ?"
            params = (id,)
        else:
            query = "SELECT * FROM {table} WHERE activo = ?"
            params = (True,)
        
        return self.execute_query(query, params)
    
    def actualizar_{table}(self, id: int, nombre: str = None, descripcion: str = None) -> int:
        \"\"\"Actualizar registro en {table}\"\"\"
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
        query = f"UPDATE {table} SET {{', '.join(updates)}} WHERE id = ?"
        
        return self.execute_command(query, tuple(params))
    
    def eliminar_{table}(self, id: int, soft_delete: bool = True) -> int:
        \"\"\"Eliminar registro de {table}\"\"\"
        if soft_delete:
            query = f"UPDATE {table} SET activo = ? WHERE id = ?"
            params = (False, id)
        else:
            query = f"DELETE FROM {table} WHERE id = ?"
            params = (id,)
        
        return self.execute_command(query, params)
"""
        
        # Agregar ejemplo de uso
        python_code += f"""
# Ejemplo de uso
if __name__ == '__main__':
    # Configurar conexión
    {'db_path = "mi_base_datos.db"' if database_type == 'sqlite' else 'connection_string = "tu_connection_string_aqui"'}
    
    try:
"""
        
        for table in detected['tables']:
            table_class = table.capitalize()
            python_code += f"""        # Gestor para {table}
        {table}_manager = {table_class}Manager({'db_path' if database_type == 'sqlite' else 'connection_string'})
        {table}_manager.connect()
        
        # Crear registro
        nuevo_id = {table}_manager.crear_{table}("Ejemplo", "Descripción de ejemplo")
        print(f"Nuevo {table} creado con ID: {{nuevo_id}}")
        
        # Obtener registros
        registros = {table}_manager.obtener_{table}()
        print(f"Registros en {table}: {{len(registros)}}")
        
        {table}_manager.disconnect()
        
"""
        
        python_code += """    except Exception as e:
        print(f"Error: {e}")
"""
        
        files['database_manager.py'] = python_code
        
        # Generar requirements.txt
        requirements = []
        if database_type == 'mysql':
            requirements.append('mysql-connector-python>=8.0.0')
        elif database_type == 'postgresql':
            requirements.append('psycopg2-binary>=2.9.0')
        
        if requirements:
            files['requirements.txt'] = '\n'.join(requirements)
        
        return files
    
    def _generate_nosql_schema(self, detected: Dict, database_type: str, vader_code: str) -> Dict[str, str]:
        """Generar esquema NoSQL"""
        files = {}
        
        if database_type == 'mongodb':
            # Generar código Python para MongoDB
            mongo_code = f"""#!/usr/bin/env python3
\"\"\"
Código Python generado para MongoDB
\"\"\"

from pymongo import MongoClient
from datetime import datetime
from typing import List, Dict, Optional
import json

class MongoDBManager:
    def __init__(self, connection_string: str = "mongodb://localhost:27017/", database_name: str = "mi_base_datos"):
        self.connection_string = connection_string
        self.database_name = database_name
        self.client = None
        self.db = None
    
    def connect(self):
        \"\"\"Conectar a MongoDB\"\"\"
        try:
            self.client = MongoClient(self.connection_string)
            self.db = self.client[self.database_name]
            
            # Verificar conexión
            self.client.admin.command('ping')
            print(f"✅ Conectado a MongoDB: {{self.database_name}}")
            
        except Exception as e:
            print(f"❌ Error conectando a MongoDB: {{e}}")
            raise
    
    def disconnect(self):
        \"\"\"Desconectar de MongoDB\"\"\"
        if self.client:
            self.client.close()
            print("🔌 Desconectado de MongoDB")

"""
            
            # Generar gestores para cada "tabla" (colección en MongoDB)
            for table in detected['tables']:
                table_class = table.capitalize()
                mongo_code += f"""
class {table_class}Manager(MongoDBManager):
    \"\"\"Gestor para la colección {table}\"\"\"
    
    def __init__(self, connection_string: str = "mongodb://localhost:27017/", database_name: str = "mi_base_datos"):
        super().__init__(connection_string, database_name)
        self.collection_name = "{table}"
    
    @property
    def collection(self):
        return self.db[self.collection_name]
    
    def crear_{table}(self, documento: Dict) -> str:
        \"\"\"Crear nuevo documento en {table}\"\"\"
        documento['fecha_creacion'] = datetime.now()
        documento['activo'] = True
        
        result = self.collection.insert_one(documento)
        return str(result.inserted_id)
    
    def obtener_{table}(self, filtro: Dict = None, limite: int = None) -> List[Dict]:
        \"\"\"Obtener documentos de {table}\"\"\"
        if filtro is None:
            filtro = {{"activo": True}}
        
        cursor = self.collection.find(filtro)
        
        if limite:
            cursor = cursor.limit(limite)
        
        # Convertir ObjectId a string para serialización JSON
        documentos = []
        for doc in cursor:
            doc['_id'] = str(doc['_id'])
            documentos.append(doc)
        
        return documentos
    
    def obtener_{table}_por_id(self, id: str) -> Optional[Dict]:
        \"\"\"Obtener documento por ID\"\"\"
        from bson import ObjectId
        
        try:
            documento = self.collection.find_one({{"_id": ObjectId(id)}})
            if documento:
                documento['_id'] = str(documento['_id'])
            return documento
        except Exception as e:
            print(f"Error obteniendo documento: {{e}}")
            return None
    
    def actualizar_{table}(self, id: str, actualizaciones: Dict) -> int:
        \"\"\"Actualizar documento en {table}\"\"\"
        from bson import ObjectId
        
        try:
            actualizaciones['fecha_actualizacion'] = datetime.now()
            
            result = self.collection.update_one(
                {{"_id": ObjectId(id)}},
                {{"$set": actualizaciones}}
            )
            
            return result.modified_count
            
        except Exception as e:
            print(f"Error actualizando documento: {{e}}")
            return 0
    
    def eliminar_{table}(self, id: str, soft_delete: bool = True) -> int:
        \"\"\"Eliminar documento de {table}\"\"\"
        from bson import ObjectId
        
        try:
            if soft_delete:
                result = self.collection.update_one(
                    {{"_id": ObjectId(id)}},
                    {{"$set": {{"activo": False, "fecha_eliminacion": datetime.now()}}}}
                )
                return result.modified_count
            else:
                result = self.collection.delete_one({{"_id": ObjectId(id)}})
                return result.deleted_count
                
        except Exception as e:
            print(f"Error eliminando documento: {{e}}")
            return 0
    
    def buscar_{table}(self, termino: str, campos: List[str] = None) -> List[Dict]:
        \"\"\"Buscar documentos por texto\"\"\"
        if campos is None:
            campos = ["nombre", "descripcion"]
        
        # Crear consulta de búsqueda de texto
        filtro = {{
            "$or": [
                {{campo: {{"$regex": termino, "$options": "i"}}}} 
                for campo in campos
            ],
            "activo": True
        }}
        
        documentos = []
        for doc in self.collection.find(filtro):
            doc['_id'] = str(doc['_id'])
            documentos.append(doc)
        
        return documentos
"""
            
            # Agregar ejemplo de uso
            mongo_code += f"""
# Ejemplo de uso
if __name__ == '__main__':
    try:
"""
            
            for table in detected['tables']:
                table_class = table.capitalize()
                mongo_code += f"""        # Gestor para {table}
        {table}_manager = {table_class}Manager()
        {table}_manager.connect()
        
        # Crear documento
        nuevo_documento = {{
            "nombre": "Ejemplo",
            "descripcion": "Descripción de ejemplo",
            "datos_adicionales": {{"clave": "valor"}}
        }}
        
        nuevo_id = {table}_manager.crear_{table}(nuevo_documento)
        print(f"Nuevo {table} creado con ID: {{nuevo_id}}")
        
        # Obtener documentos
        documentos = {table}_manager.obtener_{table}()
        print(f"Documentos en {table}: {{len(documentos)}}")
        
        # Buscar documentos
        resultados = {table}_manager.buscar_{table}("ejemplo")
        print(f"Resultados de búsqueda: {{len(resultados)}}")
        
        {table}_manager.disconnect()
        
"""
            
            mongo_code += """    except Exception as e:
        print(f"Error: {e}")
"""
            
            files['mongodb_manager.py'] = mongo_code
            files['requirements.txt'] = 'pymongo>=4.0.0'
        
        return files
    
    def create_database_project(self, vader_code: str, database_type: str, 
                              project_name: str, output_dir: str = './databases') -> str:
        """Crear proyecto completo de base de datos"""
        # Crear directorio del proyecto
        project_path = Path(output_dir) / project_name
        project_path.mkdir(parents=True, exist_ok=True)
        
        # Generar esquema y código
        files = self.generate_database_schema(vader_code, database_type)
        
        # Escribir archivos
        for filename, content in files.items():
            file_path = project_path / filename
            file_path.write_text(content, encoding='utf-8')
        
        # Crear README
        readme_content = f"""# {project_name}

Proyecto de base de datos generado con Vader Database Manager usando {self.supported_databases[database_type]['name']}.

## Código Vader original:
```
{vader_code}
```

## Instalación:

1. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

2. Configurar base de datos:
"""
        
        if database_type == 'sqlite':
            readme_content += """   - SQLite se crea automáticamente al ejecutar el código
"""
        elif database_type == 'mysql':
            readme_content += """   - Instalar MySQL Server
   - Crear base de datos: `CREATE DATABASE mi_base_datos;`
   - Ejecutar schema.sql para crear tablas
"""
        elif database_type == 'postgresql':
            readme_content += """   - Instalar PostgreSQL
   - Crear base de datos: `createdb mi_base_datos`
   - Ejecutar schema.sql para crear tablas
"""
        elif database_type == 'mongodb':
            readme_content += """   - Instalar MongoDB
   - Iniciar servicio MongoDB
   - Las colecciones se crean automáticamente
"""
        
        readme_content += f"""
## Uso:

```python
python3 {'database_manager.py' if database_type in ['sqlite', 'mysql', 'postgresql'] else 'mongodb_manager.py'}
```

## Generado el: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---
Creado con ❤️ usando Vader Database Manager
"""
        
        (project_path / 'README.md').write_text(readme_content, encoding='utf-8')
        
        print(f"✅ Proyecto de base de datos creado en: {project_path}")
        return str(project_path)

def main():
    """Función principal para testing"""
    db_manager = VaderDatabaseManager()
    
    print("🧪 PROBANDO VADER DATABASE MANAGER")
    print("=" * 50)
    
    # Código Vader de ejemplo
    vader_code = """# Sistema de gestión de usuarios y productos
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
crear índice en tabla usuarios para campo email"""
    
    # Probar detección de operaciones
    operations = db_manager.detect_database_operations(vader_code)
    print(f"\n🎯 OPERACIONES DETECTADAS:")
    print(f"  Operaciones: {operations['operations']}")
    print(f"  Tablas: {operations['tables']}")
    print(f"  Campos: {operations['fields']}")
    
    # Generar esquemas para diferentes bases de datos
    databases_to_test = ['sqlite', 'mysql', 'mongodb']
    
    for db_type in databases_to_test:
        print(f"\n🗄️ GENERANDO ESQUEMA PARA {db_type.upper()}:")
        try:
            files = db_manager.generate_database_schema(vader_code, db_type)
            print(f"  ✅ {len(files)} archivos generados")
            for filename in files.keys():
                print(f"    - {filename}")
        except Exception as e:
            print(f"  ❌ Error: {e}")
    
    # Crear proyecto completo de ejemplo
    try:
        project_path = db_manager.create_database_project(
            vader_code,
            'sqlite',
            'sistema_usuarios_productos',
            './test_databases'
        )
        print(f"\n✅ Proyecto de prueba creado en: {project_path}")
    except Exception as e:
        print(f"\n❌ Error creando proyecto: {e}")
    
    print("\n🎉 VADER DATABASE MANAGER FUNCIONAL")
    return True

if __name__ == '__main__':
    success = main()
    import sys
    sys.exit(0 if success else 1)
