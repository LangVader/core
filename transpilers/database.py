# Sistema Universal de Bases de Datos para Vader
# Permite interactuar con cualquier base de datos usando sintaxis natural en español

import re

class DatabaseTranspiler:
    """Transpilador universal para operaciones de base de datos"""
    
    def __init__(self, target_language='python', db_type='mysql'):
        self.target_language = target_language
        self.db_type = db_type.lower()
        self.imports = set()
        self.connection_code = []
        self.setup_code = []
        
    def transpile_database_operations(self, code):
        """Transpila operaciones de base de datos a código específico del lenguaje"""
        lines = code.split('\n')
        result = []
        
        # Agregar imports necesarios
        result.extend(self._get_imports())
        result.append('')
        
        # Procesar cada línea
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            if line.startswith('conectar base_datos'):
                connection_lines, i = self._process_connection(lines, i)
                result.extend(connection_lines)
                
            elif line.startswith('crear tabla'):
                table_lines, i = self._process_create_table(lines, i)
                result.extend(table_lines)
                
            elif line.startswith('insertar en'):
                insert_lines, i = self._process_insert(lines, i)
                result.extend(insert_lines)
                
            elif line.startswith('buscar') and ('en' in line or 'desde' in line):
                select_lines, i = self._process_select(lines, i)
                result.extend(select_lines)
                
            elif line.startswith('actualizar'):
                update_lines, i = self._process_update(lines, i)
                result.extend(update_lines)
                
            elif line.startswith('eliminar de'):
                delete_lines, i = self._process_delete(lines, i)
                result.extend(delete_lines)
                
            else:
                i += 1
                
        return '\n'.join(result)
    
    def _get_imports(self):
        """Retorna los imports necesarios según el lenguaje y tipo de BD"""
        imports = []
        
        if self.target_language == 'python':
            if self.db_type == 'mysql':
                imports.extend([
                    "import mysql.connector",
                    "from mysql.connector import Error",
                    "import logging"
                ])
            elif self.db_type == 'postgresql' or self.db_type == 'postgres':
                imports.extend([
                    "import psycopg2",
                    "from psycopg2 import Error",
                    "import logging"
                ])
            elif self.db_type == 'sqlite':
                imports.extend([
                    "import sqlite3",
                    "import logging"
                ])
            elif self.db_type == 'mongodb':
                imports.extend([
                    "from pymongo import MongoClient",
                    "from pymongo.errors import ConnectionFailure",
                    "import logging"
                ])
                
        elif self.target_language == 'javascript':
            if self.db_type == 'mysql':
                imports.extend([
                    "const mysql = require('mysql2/promise');",
                    "const fs = require('fs');"
                ])
            elif self.db_type == 'postgresql':
                imports.extend([
                    "const { Pool } = require('pg');",
                    "const fs = require('fs');"
                ])
            elif self.db_type == 'mongodb':
                imports.extend([
                    "const { MongoClient } = require('mongodb');",
                    "const fs = require('fs');"
                ])
                
        return imports
    
    def _process_connection(self, lines, start_index):
        """Procesa líneas de conexión a base de datos"""
        line = lines[start_index].strip()
        result = []
        
        # Extraer información de conexión
        parts = line.split()
        if len(parts) < 4:
            return [f"# Error: Sintaxis de conexión inválida"], start_index + 1
            
        db_type = parts[2]
        connection_string = parts[3].strip('"\'')
        
        # Extraer parámetros adicionales
        params = {}
        for part in parts[4:]:
            if '=' in part:
                key, value = part.split('=', 1)
                params[key] = value.strip('"\'')
        
        if self.target_language == 'python':
            result.extend(self._generate_python_connection(db_type, connection_string, params))
        elif self.target_language == 'javascript':
            result.extend(self._generate_js_connection(db_type, connection_string, params))
            
        return result, start_index + 1
    
    def _generate_python_connection(self, db_type, connection_string, params):
        """Genera código de conexión Python"""
        result = []
        
        if db_type == 'mysql':
            result.extend([
                "# Configuración de conexión MySQL",
                "try:",
                f"    connection = mysql.connector.connect(",
                f"        host='{params.get('host', 'localhost')}',",
                f"        database='{params.get('base', 'test')}',",
                f"        user='{params.get('usuario', 'root')}',",
                f"        password='{params.get('password', '')}'",
                "    )",
                "    if connection.is_connected():",
                "        cursor = connection.cursor()",
                "        print('✅ Conectado exitosamente a MySQL')",
                "except Error as e:",
                "    print(f'❌ Error conectando a MySQL: {e}')",
                "    connection = None",
                ""
            ])
            
        elif db_type in ['postgresql', 'postgres']:
            result.extend([
                "# Configuración de conexión PostgreSQL",
                "try:",
                f"    connection = psycopg2.connect(",
                f"        host='{params.get('host', 'localhost')}',",
                f"        database='{params.get('base', 'postgres')}',",
                f"        user='{params.get('usuario', 'postgres')}',",
                f"        password='{params.get('password', '')}'",
                "    )",
                "    cursor = connection.cursor()",
                "    print('✅ Conectado exitosamente a PostgreSQL')",
                "except Error as e:",
                "    print(f'❌ Error conectando a PostgreSQL: {e}')",
                "    connection = None",
                ""
            ])
            
        elif db_type == 'sqlite':
            result.extend([
                "# Configuración de conexión SQLite",
                "try:",
                f"    connection = sqlite3.connect('{connection_string}')",
                "    cursor = connection.cursor()",
                "    print('✅ Conectado exitosamente a SQLite')",
                "except sqlite3.Error as e:",
                "    print(f'❌ Error conectando a SQLite: {e}')",
                "    connection = None",
                ""
            ])
            
        elif db_type == 'mongodb':
            result.extend([
                "# Configuración de conexión MongoDB",
                "try:",
                f"    client = MongoClient('{connection_string}')",
                "    # Verificar conexión",
                "    client.admin.command('ismaster')",
                f"    db = client['{params.get('base', 'test')}']",
                "    print('✅ Conectado exitosamente a MongoDB')",
                "except ConnectionFailure as e:",
                "    print(f'❌ Error conectando a MongoDB: {e}')",
                "    client = None",
                ""
            ])
            
        return result
    
    def _generate_js_connection(self, db_type, connection_string, params):
        """Genera código de conexión JavaScript/Node.js"""
        result = []
        
        if db_type == 'mysql':
            result.extend([
                "// Configuración de conexión MySQL",
                "const pool = mysql.createPool({",
                f"    host: '{params.get('host', 'localhost')}',",
                f"    user: '{params.get('usuario', 'root')}',",
                f"    password: '{params.get('password', '')}',",
                f"    database: '{params.get('base', 'test')}',",
                "    waitForConnections: true,",
                "    connectionLimit: 10,",
                "    queueLimit: 0",
                "});",
                "",
                "// Verificar conexión",
                "pool.getConnection((err, connection) => {",
                "    if (err) {",
                "        console.error('❌ Error conectando a MySQL:', err);",
                "        return;",
                "    }",
                "    console.log('✅ Conectado exitosamente a MySQL');",
                "    connection.release();",
                "});",
                ""
            ])
            
        elif db_type == 'mongodb':
            result.extend([
                "// Configuración de conexión MongoDB",
                f"const uri = '{connection_string}';",
                "const client = new MongoClient(uri);",
                "",
                "async function connectMongoDB() {",
                "    try {",
                "        await client.connect();",
                "        console.log('✅ Conectado exitosamente a MongoDB');",
                f"        const db = client.db('{params.get('base', 'test')}');",
                "        return db;",
                "    } catch (error) {",
                "        console.error('❌ Error conectando a MongoDB:', error);",
                "        return null;",
                "    }",
                "}",
                ""
            ])
            
        return result
    
    def _process_create_table(self, lines, start_index):
        """Procesa creación de tablas"""
        result = []
        table_name = lines[start_index].split()[-1]
        
        columns = []
        i = start_index + 1
        
        while i < len(lines) and not lines[i].strip().startswith('fin tabla'):
            line = lines[i].strip()
            if line.startswith('columna'):
                column_def = self._parse_column_definition(line)
                columns.append(column_def)
            i += 1
        
        # Generar SQL CREATE TABLE
        if self.target_language == 'python':
            result.extend(self._generate_python_create_table(table_name, columns))
        elif self.target_language == 'javascript':
            result.extend(self._generate_js_create_table(table_name, columns))
            
        return result, i + 1
    
    def _parse_column_definition(self, line):
        """Parsea definición de columna"""
        parts = line.split()
        column_name = parts[1]
        column_type = parts[2]
        
        # Mapear tipos de Vader a SQL
        type_mapping = {
            'texto': 'VARCHAR(255)',
            'numero': 'INT',
            'decimal': 'DECIMAL(10,2)',
            'fecha': 'DATE',
            'tiempo': 'DATETIME',
            'booleano': 'BOOLEAN'
        }
        
        sql_type = type_mapping.get(column_type, 'VARCHAR(255)')
        
        # Procesar modificadores
        constraints = []
        for part in parts[3:]:
            if part == 'primary_key':
                constraints.append('PRIMARY KEY')
            elif part == 'auto_increment':
                constraints.append('AUTO_INCREMENT')
            elif part == 'required' or part == 'not_null':
                constraints.append('NOT NULL')
            elif part == 'unique':
                constraints.append('UNIQUE')
            elif part.startswith('default='):
                default_val = part.split('=')[1]
                constraints.append(f'DEFAULT {default_val}')
        
        return {
            'name': column_name,
            'type': sql_type,
            'constraints': constraints
        }
    
    def _generate_python_create_table(self, table_name, columns):
        """Genera código Python para CREATE TABLE"""
        result = [
            f"# Crear tabla {table_name}",
            "try:",
            f"    create_table_query = '''",
            f"    CREATE TABLE IF NOT EXISTS {table_name} ("
        ]
        
        column_definitions = []
        for col in columns:
            col_def = f"        {col['name']} {col['type']}"
            if col['constraints']:
                col_def += " " + " ".join(col['constraints'])
            column_definitions.append(col_def)
        
        result.append(",\n".join(column_definitions))
        result.extend([
            "    );",
            "    '''",
            "    cursor.execute(create_table_query)",
            "    connection.commit()",
            f"    print('✅ Tabla {table_name} creada exitosamente')",
            "except Error as e:",
            f"    print(f'❌ Error creando tabla {table_name}: {{e}}')",
            ""
        ])
        
        return result
    
    def _generate_js_create_table(self, table_name, columns):
        """Genera código JavaScript para CREATE TABLE"""
        result = [
            f"// Crear tabla {table_name}",
            "async function createTable() {",
            "    try {",
            f"        const createTableQuery = `",
            f"        CREATE TABLE IF NOT EXISTS {table_name} ("
        ]
        
        column_definitions = []
        for col in columns:
            col_def = f"            {col['name']} {col['type']}"
            if col['constraints']:
                col_def += " " + " ".join(col['constraints'])
            column_definitions.append(col_def)
        
        result.append(",\n".join(column_definitions))
        result.extend([
            "        );",
            "        `;",
            "        await pool.execute(createTableQuery);",
            f"        console.log('✅ Tabla {table_name} creada exitosamente');",
            "    } catch (error) {",
            f"        console.error('❌ Error creando tabla {table_name}:', error);",
            "    }",
            "}",
            ""
        ])
        
        return result
    
    def _process_insert(self, lines, start_index):
        """Procesa operaciones INSERT"""
        line = lines[start_index].strip()
        table_name = line.split('en')[1].strip()
        
        # Recoger datos a insertar
        data = {}
        i = start_index + 1
        while i < len(lines) and not lines[i].strip().startswith('fin insertar'):
            data_line = lines[i].strip()
            if ':' in data_line:
                key, value = data_line.split(':', 1)
                data[key.strip()] = value.strip().strip('"\'')
            i += 1
        
        if self.target_language == 'python':
            return self._generate_python_insert(table_name, data), i + 1
        elif self.target_language == 'javascript':
            return self._generate_js_insert(table_name, data), i + 1
            
        return [], i + 1
    
    def _generate_python_insert(self, table_name, data):
        """Genera código Python para INSERT"""
        columns = list(data.keys())
        values = list(data.values())
        placeholders = ', '.join(['%s'] * len(values))
        
        return [
            f"# Insertar datos en {table_name}",
            "try:",
            f"    insert_query = '''INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})'''",
            f"    cursor.execute(insert_query, {values})",
            "    connection.commit()",
            f"    print('✅ Datos insertados en {table_name} exitosamente')",
            "except Error as e:",
            f"    print(f'❌ Error insertando en {table_name}: {{e}}')",
            ""
        ]
    
    def _generate_js_insert(self, table_name, data):
        """Genera código JavaScript para INSERT"""
        columns = list(data.keys())
        values = list(data.values())
        placeholders = ', '.join(['?'] * len(values))
        
        return [
            f"// Insertar datos en {table_name}",
            "async function insertData() {",
            "    try {",
            f"        const insertQuery = `INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})`;",
            f"        await pool.execute(insertQuery, {values});",
            f"        console.log('✅ Datos insertados en {table_name} exitosamente');",
            "    } catch (error) {",
            f"        console.error('❌ Error insertando en {table_name}:', error);",
            "    }",
            "}",
            ""
        ]
    
    def _process_select(self, lines, start_index):
        """Procesa operaciones SELECT"""
        line = lines[start_index].strip()
        
        # Parsear consulta SELECT
        if line.startswith('buscar todos en'):
            table_name = line.split('en')[1].split('donde')[0].strip()
            columns = '*'
        elif line.startswith('buscar en'):
            table_name = line.split('en')[1].split('donde')[0].strip()
            columns = '*'
        else:
            # Buscar con columnas específicas
            parts = line.split('desde')
            columns = parts[0].replace('buscar', '').strip()
            table_name = parts[1].split('donde')[0].strip() if len(parts) > 1 else ''
        
        # Extraer condición WHERE si existe
        where_clause = ''
        if 'donde' in line:
            where_clause = line.split('donde')[1].strip()
        
        if self.target_language == 'python':
            return self._generate_python_select(table_name, columns, where_clause), start_index + 1
        elif self.target_language == 'javascript':
            return self._generate_js_select(table_name, columns, where_clause), start_index + 1
            
        return [], start_index + 1
    
    def _generate_python_select(self, table_name, columns, where_clause):
        """Genera código Python para SELECT"""
        result = [
            f"# Consultar datos de {table_name}",
            "try:"
        ]
        
        query = f"SELECT {columns} FROM {table_name}"
        if where_clause:
            # Convertir condición de español a SQL
            sql_where = self._convert_where_clause(where_clause)
            query += f" WHERE {sql_where}"
        
        result.extend([
            f"    select_query = '''{query}'''",
            "    cursor.execute(select_query)",
            "    resultados = cursor.fetchall()",
            "    for fila in resultados:",
            "        print(fila)",
            "except Error as e:",
            f"    print(f'❌ Error consultando {table_name}: {{e}}')",
            ""
        ])
        
        return result
    
    def _generate_js_select(self, table_name, columns, where_clause):
        """Genera código JavaScript para SELECT"""
        query = f"SELECT {columns} FROM {table_name}"
        if where_clause:
            sql_where = self._convert_where_clause(where_clause)
            query += f" WHERE {sql_where}"
        
        return [
            f"// Consultar datos de {table_name}",
            "async function selectData() {",
            "    try {",
            f"        const selectQuery = `{query}`;",
            "        const [rows] = await pool.execute(selectQuery);",
            "        console.log('📊 Resultados:', rows);",
            "        return rows;",
            "    } catch (error) {",
            f"        console.error('❌ Error consultando {table_name}:', error);",
            "        return [];",
            "    }",
            "}",
            ""
        ]
    
    def _convert_where_clause(self, where_clause):
        """Convierte condición WHERE de español a SQL"""
        # Reemplazos básicos
        sql_where = where_clause
        sql_where = sql_where.replace(' = ', ' = ')
        sql_where = sql_where.replace(' y ', ' AND ')
        sql_where = sql_where.replace(' o ', ' OR ')
        sql_where = sql_where.replace(' no ', ' NOT ')
        
        return sql_where
    
    def _process_update(self, lines, start_index):
        """Procesa operaciones UPDATE"""
        line = lines[start_index].strip()
        parts = line.split('donde')
        
        # Extraer tabla y campos a actualizar
        update_part = parts[0].replace('actualizar', '').strip()
        table_name = update_part.split('establecer')[0].strip()
        set_clause = update_part.split('establecer')[1].strip() if 'establecer' in update_part else ''
        
        where_clause = parts[1].strip() if len(parts) > 1 else ''
        
        if self.target_language == 'python':
            return self._generate_python_update(table_name, set_clause, where_clause), start_index + 1
        elif self.target_language == 'javascript':
            return self._generate_js_update(table_name, set_clause, where_clause), start_index + 1
            
        return [], start_index + 1
    
    def _generate_python_update(self, table_name, set_clause, where_clause):
        """Genera código Python para UPDATE"""
        query = f"UPDATE {table_name} SET {set_clause}"
        if where_clause:
            sql_where = self._convert_where_clause(where_clause)
            query += f" WHERE {sql_where}"
        
        return [
            f"# Actualizar datos en {table_name}",
            "try:",
            f"    update_query = '''{query}'''",
            "    cursor.execute(update_query)",
            "    connection.commit()",
            f"    print(f'✅ {{cursor.rowcount}} filas actualizadas en {table_name}')",
            "except Error as e:",
            f"    print(f'❌ Error actualizando {table_name}: {{e}}')",
            ""
        ]
    
    def _generate_js_update(self, table_name, set_clause, where_clause):
        """Genera código JavaScript para UPDATE"""
        query = f"UPDATE {table_name} SET {set_clause}"
        if where_clause:
            sql_where = self._convert_where_clause(where_clause)
            query += f" WHERE {sql_where}"
        
        return [
            f"// Actualizar datos en {table_name}",
            "async function updateData() {",
            "    try {",
            f"        const updateQuery = `{query}`;",
            "        const [result] = await pool.execute(updateQuery);",
            f"        console.log(`✅ ${{result.affectedRows}} filas actualizadas en {table_name}`);",
            "        return result;",
            "    } catch (error) {",
            f"        console.error('❌ Error actualizando {table_name}:', error);",
            "    }",
            "}",
            ""
        ]
    
    def _process_delete(self, lines, start_index):
        """Procesa operaciones DELETE"""
        line = lines[start_index].strip()
        parts = line.split('donde')
        
        table_name = parts[0].replace('eliminar de', '').strip()
        where_clause = parts[1].strip() if len(parts) > 1 else ''
        
        if self.target_language == 'python':
            return self._generate_python_delete(table_name, where_clause), start_index + 1
        elif self.target_language == 'javascript':
            return self._generate_js_delete(table_name, where_clause), start_index + 1
            
        return [], start_index + 1
    
    def _generate_python_delete(self, table_name, where_clause):
        """Genera código Python para DELETE"""
        query = f"DELETE FROM {table_name}"
        if where_clause:
            sql_where = self._convert_where_clause(where_clause)
            query += f" WHERE {sql_where}"
        
        return [
            f"# Eliminar datos de {table_name}",
            "try:",
            f"    delete_query = '''{query}'''",
            "    cursor.execute(delete_query)",
            "    connection.commit()",
            f"    print(f'✅ {{cursor.rowcount}} filas eliminadas de {table_name}')",
            "except Error as e:",
            f"    print(f'❌ Error eliminando de {table_name}: {{e}}')",
            ""
        ]
    
    def _generate_js_delete(self, table_name, where_clause):
        """Genera código JavaScript para DELETE"""
        query = f"DELETE FROM {table_name}"
        if where_clause:
            sql_where = self._convert_where_clause(where_clause)
            query += f" WHERE {sql_where}"
        
        return [
            f"// Eliminar datos de {table_name}",
            "async function deleteData() {",
            "    try {",
            f"        const deleteQuery = `{query}`;",
            "        const [result] = await pool.execute(deleteQuery);",
            f"        console.log(`✅ ${{result.affectedRows}} filas eliminadas de {table_name}`);",
            "        return result;",
            "    } catch (error) {",
            f"        console.error('❌ Error eliminando de {table_name}:', error);",
            "    }",
            "}",
            ""
        ]

def transpilar_base_datos(code, target_language='python', db_type='mysql'):
    """Función principal para transpilar operaciones de base de datos"""
    transpiler = DatabaseTranspiler(target_language, db_type)
    return transpiler.transpile_database_operations(code)
