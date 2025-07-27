#!/usr/bin/env python3
"""
Transpilador Java COMPLETO para Vader
Convierte código Vader en español natural a Java válido y funcional
Versión: COMPLETA con todas las características avanzadas
"""

import re

class JavaTranspiler:
    def __init__(self):
        self.indent_level = 0
        self.class_name = "VaderProgram"
        self.declared_vars = set()
        self.declared_functions = set()
        self.declared_classes = set()
        self.imports = set([
            'java.util.Scanner',
            'java.util.ArrayList',
            'java.util.HashMap',
            'java.util.List',
            'java.util.Map',
            'java.io.*',
            'java.math.*'
        ])
        self.in_class = False
        self.current_class = None
    
    def transpile(self, vader_code):
        """Transpile Vader code to Java - VERSIÓN COMPLETA"""
        lines = vader_code.split('\n')
        java_lines = []
        
        # Agregar imports necesarios
        for import_stmt in sorted(self.imports):
            java_lines.append(f'import {import_stmt};')
        java_lines.append('')
        
        # Clase principal
        java_lines.extend([
            f'public class {self.class_name} {{',
            '    private static Scanner scanner = new Scanner(System.in);',
            ''
        ])
        
        # Procesar líneas para detectar clases y funciones
        self.indent_level = 1
        self.declared_vars = set()
        
        # Separar funciones, clases y código main
        functions_code, classes_code, main_code = self.separate_code_sections(lines)
        
        # Generar funciones primero
        if functions_code:
            for line in functions_code:
                if line.strip():  # Solo procesar líneas no vacías
                    java_line = self.transpile_line(line.strip())
                    if java_line is not None:
                        if isinstance(java_line, list):
                            java_lines.extend(java_line)
                        else:
                            java_lines.append(java_line)
            java_lines.append('')
        
        # Generar clases
        if classes_code:
            for line in classes_code:
                java_line = self.transpile_line(line.strip())
                if java_line is not None:
                    if isinstance(java_line, list):
                        java_lines.extend(java_line)
                    else:
                        java_lines.append(java_line)
            java_lines.append('')
        
        # Generar main
        java_lines.append('    public static void main(String[] args) {')
        self.indent_level = 2
        
        for line in main_code:
            line = line.strip()
            
            # Preservar líneas vacías y comentarios
            if not line:
                java_lines.append('')
                continue
            if line.startswith('#'):
                java_lines.append(self.indent() + '//' + line[1:])
                continue
                
            java_line = self.transpile_line(line)
            if java_line is not None:
                if isinstance(java_line, list):
                    java_lines.extend(java_line)
                else:
                    java_lines.append(java_line)
        
        # Cerrar main y clase
        java_lines.extend([
            '        scanner.close();',
            '    }',
            '}'
        ])
        
        return '\n'.join(java_lines)
    
    def separate_code_sections(self, lines):
        """Separa el código en funciones, clases y main basado en sintaxis Vader original"""
        functions = []
        classes = []
        main_code = []
        
        in_function = False
        in_class = False
        current_block = []
        
        for line in lines:
            stripped = line.strip()
            
            # Detectar inicio de función en sintaxis Vader
            if stripped.startswith('funcion ') or stripped.startswith('función '):
                if current_block:
                    main_code.extend(current_block)
                    current_block = []
                in_function = True
                in_class = False
                current_block = [line]
                continue
            
            # Detectar inicio de clase en sintaxis Vader
            elif stripped.startswith('clase '):
                if current_block:
                    main_code.extend(current_block)
                    current_block = []
                in_class = True
                in_function = False
                current_block = [line]
                continue
            
            # Detectar fin de bloques
            elif stripped in ['fin', 'fin funcion', 'fin función']:
                if in_function:
                    current_block.append(line)
                    functions.extend(current_block)
                    functions.append('')
                    in_function = False
                    current_block = []
                    continue
            
            elif stripped == 'fin clase':
                if in_class:
                    current_block.append(line)
                    classes.extend(current_block)
                    classes.append('')
                    in_class = False
                    current_block = []
                    continue
            
            # Agregar líneas al bloque actual
            if in_function or in_class:
                current_block.append(line)
            else:
                current_block.append(line)
        
        # Agregar código restante a main
        if current_block:
            main_code.extend(current_block)
        
        return functions, classes, main_code

    def transpile_line(self, line):
        """Transpile a single line"""
        # Remover comentarios inline
        if '#' in line:
            code_part = line.split('#')[0].strip()
            comment_part = '//' + '#'.join(line.split('#')[1:])
            if code_part:
                return self.process_code_line(code_part) + '  ' + comment_part
            else:
                return self.indent() + '//' + line[1:]
        
        return self.process_code_line(line)
    
    def process_code_line(self, line):
        """Procesa una línea de código - VERSIÓN COMPLETA"""
        # Fin de bloque (funciones, clases, if, while, etc.)
        if line in ['fin', 'fin funcion', 'fin función', 'fin clase', 'fin si', 'fin mientras']:
            if self.indent_level > 1:
                self.indent_level -= 1
                return '    ' * (self.indent_level - 1) + '}'
            return None
        
        current_indent = self.indent()
        
        # Conversiones de tipos y valores
        line = line.replace('verdadero', 'true')
        line = line.replace('falso', 'false')
        line = line.replace('nulo', 'null')
        
        # Funciones de conversión avanzadas
        line = re.sub(r'texto\(([^)]+)\)', r'String.valueOf(\1)', line)
        line = re.sub(r'numero\(([^)]+)\)', r'Integer.parseInt(\1)', line)
        line = re.sub(r'decimal\(([^)]+)\)', r'Double.parseDouble(\1)', line)
        line = re.sub(r'longitud\(([^)]+)\)', r'\1.length()', line)
        
        # Operadores matemáticos avanzados
        line = re.sub(r'raiz\(([^)]+)\)', r'Math.sqrt(\1)', line)
        line = re.sub(r'potencia\(([^,]+),\s*([^)]+)\)', r'Math.pow(\1, \2)', line)
        line = re.sub(r'absoluto\(([^)]+)\)', r'Math.abs(\1)', line)
        line = re.sub(r'redondear\(([^)]+)\)', r'Math.round(\1)', line)
        
        # Estructuras de datos avanzadas
        # Arrays y listas
        if line.startswith('crear lista '):
            var_name = line.replace('crear lista ', '').strip()
            if var_name not in self.declared_vars:
                self.declared_vars.add(var_name)
                return current_indent + f'List<String> {var_name} = new ArrayList<>();'
        
        if line.startswith('crear array '):
            parts = line.replace('crear array ', '').split(' de tamaño ')
            var_name = parts[0].strip()
            size = parts[1].strip() if len(parts) > 1 else '10'
            if var_name not in self.declared_vars:
                self.declared_vars.add(var_name)
                return current_indent + f'String[] {var_name} = new String[{size}];'
        
        if line.startswith('crear mapa '):
            var_name = line.replace('crear mapa ', '').strip()
            if var_name not in self.declared_vars:
                self.declared_vars.add(var_name)
                return current_indent + f'Map<String, String> {var_name} = new HashMap<>();'
        
        # Operaciones con listas
        if ' agregar ' in line and ' a ' in line:
            parts = line.split(' agregar ')
            if len(parts) == 2 and ' a ' in parts[1]:
                item_and_list = parts[1].split(' a ')
                item = item_and_list[0].strip()
                list_name = item_and_list[1].strip()
                return current_indent + f'{list_name}.add({item});'
        
        if ' obtener elemento ' in line and ' de ' in line:
            parts = line.split(' obtener elemento ')
            if len(parts) == 2 and ' de ' in parts[1]:
                index_and_list = parts[1].split(' de ')
                index = index_and_list[0].strip()
                list_name = index_and_list[1].strip()
                var_name = parts[0].strip() if parts[0].strip() else 'elemento'
                if var_name not in self.declared_vars:
                    self.declared_vars.add(var_name)
                    return current_indent + f'String {var_name} = {list_name}.get({index});'
                else:
                    return current_indent + f'{var_name} = {list_name}.get({index});'
        
        # Print statements
        if line.startswith('mostrar ') or line.startswith('decir '):
            content = line.split(' ', 1)[1]
            # Manejo de concatenación avanzada
            if ' + ' in content:
                return current_indent + f'System.out.println({content});'
            else:
                return current_indent + f'System.out.println({content});'
        
        # Input statements
        if 'preguntar ' in line and 'guardar' in line:
            if 'guardar la respuesta en' in line:
                parts = line.split('guardar la respuesta en')
                question = parts[0].replace('preguntar ', '').strip()
                var_name = parts[1].strip()
            elif 'guárdalo en' in line:
                parts = line.split('guárdalo en')
                question = parts[0].replace('preguntar ', '').strip()
                var_name = parts[1].strip()
            else:
                return current_indent + line + ';'
            
            if var_name not in self.declared_vars:
                self.declared_vars.add(var_name)
                return current_indent + f'System.out.print({question}); String {var_name} = scanner.nextLine();'
            else:
                return current_indent + f'System.out.print({question}); {var_name} = scanner.nextLine();'
        
        # Condicionales
        if line.startswith('si ') and ('entonces' in line or line.endswith(':')):
            condition = line.replace('si ', '').replace(' entonces', '').replace(':', '').strip()
            # Convertir operadores
            condition = condition.replace(' es igual a ', ' == ')
            condition = condition.replace(' es mayor que ', ' > ')
            condition = condition.replace(' es menor que ', ' < ')
            condition = condition.replace(' mayor que ', ' > ')
            condition = condition.replace(' menor que ', ' < ')
            condition = condition.replace(' igual a ', ' == ')
            
            self.indent_level += 1
            return current_indent + f'if ({condition}) {{'
        
        # Else
        if line == 'sino' or line == 'si no':
            if self.indent_level > 2:
                self.indent_level -= 1
            else_indent = self.indent()
            self.indent_level += 1
            return else_indent + '} else {'
        
        # Bucles for
        if line.startswith('repetir ') and ' veces' in line:
            times = line.replace('repetir ', '').replace(' veces', '').strip()
            self.indent_level += 1
            return current_indent + f'for (int i = 0; i < {times}; i++) {{'
        
        # Bucles while
        if line.startswith('mientras '):
            condition = line.replace('mientras ', '').replace(':', '').strip()
            condition = condition.replace(' es igual a ', ' == ')
            condition = condition.replace(' es mayor que ', ' > ')
            condition = condition.replace(' es menor que ', ' < ')
            condition = condition.replace(' mayor que ', ' > ')
            condition = condition.replace(' menor que ', ' < ')
            condition = condition.replace(' igual a ', ' == ')
            self.indent_level += 1
            return current_indent + f'while ({condition}) {{'
        
        # Definición de funciones avanzadas con tipos
        if line.startswith('funcion ') or line.startswith('función '):
            func_def = line.replace('funcion ', '').replace('función ', '')
            
            # Detectar tipo de retorno
            return_type = 'void'
            if ' que devuelve ' in func_def:
                parts = func_def.split(' que devuelve ')
                func_def = parts[0]
                return_type_str = parts[1].replace(':', '').strip()
                if return_type_str in ['numero', 'entero']:
                    return_type = 'int'
                elif return_type_str in ['decimal', 'flotante']:
                    return_type = 'double'
                elif return_type_str in ['texto', 'cadena']:
                    return_type = 'String'
                elif return_type_str in ['booleano', 'logico']:
                    return_type = 'boolean'
            
            if ' con ' in func_def:
                name, params = func_def.split(' con ', 1)
                name = name.strip()
                params_str = params.replace(':', '').strip()
                
                # Procesar parámetros con tipos
                typed_params = []
                if params_str:
                    param_list = [p.strip() for p in params_str.replace(' y ', ', ').split(',')]
                    for param in param_list:
                        if ' tipo ' in param:
                            param_parts = param.split(' tipo ')
                            param_name = param_parts[0].strip()
                            param_type = param_parts[1].strip()
                            if param_type in ['numero', 'entero']:
                                typed_params.append(f'int {param_name}')
                            elif param_type in ['decimal', 'flotante']:
                                typed_params.append(f'double {param_name}')
                            elif param_type in ['texto', 'cadena']:
                                typed_params.append(f'String {param_name}')
                            elif param_type in ['booleano', 'logico']:
                                typed_params.append(f'boolean {param_name}')
                            else:
                                typed_params.append(f'String {param_name}')
                        else:
                            typed_params.append(f'String {param}')
                
                params_final = ', '.join(typed_params)
                self.indent_level += 1
                return current_indent + f'public static {return_type} {name}({params_final}) {{'
            else:
                name = func_def.replace(':', '').strip()
                self.indent_level += 1
                return current_indent + f'public static {return_type} {name}() {{'
        
        # Definición de clases avanzadas
        if line.startswith('clase '):
            class_def = line.replace('clase ', '').replace(':', '').strip()
            
            # Manejo de herencia
            if ' hereda de ' in class_def:
                parts = class_def.split(' hereda de ')
                class_name = parts[0].strip()
                parent_class = parts[1].strip()
                self.in_class = True
                self.current_class = class_name
                self.indent_level += 1
                return current_indent + f'public static class {class_name} extends {parent_class} {{'
            else:
                class_name = class_def
                self.in_class = True
                self.current_class = class_name
                self.indent_level += 1
                return current_indent + f'public static class {class_name} {{'
        
        # Atributos de clase
        if line.startswith('atributo ') and self.in_class:
            attr_def = line.replace('atributo ', '').strip()
            if ' tipo ' in attr_def:
                parts = attr_def.split(' tipo ')
                attr_name = parts[0].strip()
                attr_type = parts[1].strip()
                if attr_type in ['numero', 'entero']:
                    java_type = 'int'
                elif attr_type in ['decimal', 'flotante']:
                    java_type = 'double'
                elif attr_type in ['texto', 'cadena']:
                    java_type = 'String'
                elif attr_type in ['booleano', 'logico']:
                    java_type = 'boolean'
                else:
                    java_type = 'String'
                return current_indent + f'private {java_type} {attr_name};'
            else:
                return current_indent + f'private String {attr_def};'
        
        # Constructor de clase
        if line.startswith('constructor con '):
            params = line.replace('constructor con ', '').replace(':', '').strip()
            if params:
                # Procesar parámetros con tipos explícitos
                typed_params = []
                param_list = [p.strip() for p in params.replace(' y ', ', ').split(',')]
                for param in param_list:
                    if ' tipo ' in param:
                        param_parts = param.split(' tipo ')
                        param_name = param_parts[0].strip()
                        param_type = param_parts[1].strip()
                        if param_type in ['numero', 'entero']:
                            typed_params.append(f'int {param_name}')
                        elif param_type in ['decimal', 'flotante']:
                            typed_params.append(f'double {param_name}')
                        elif param_type in ['texto', 'cadena']:
                            typed_params.append(f'String {param_name}')
                        elif param_type in ['booleano', 'logico']:
                            typed_params.append(f'boolean {param_name}')
                        else:
                            typed_params.append(f'String {param_name}')
                    else:
                        # Inferir tipo basado en el nombre del parámetro
                        if param in ['edad', 'numero', 'cantidad', 'id']:
                            typed_params.append(f'int {param}')
                        elif param in ['precio', 'salario', 'peso', 'altura']:
                            typed_params.append(f'double {param}')
                        elif param in ['activo', 'visible', 'habilitado']:
                            typed_params.append(f'boolean {param}')
                        else:
                            typed_params.append(f'String {param}')
                
                params_final = ', '.join(typed_params)
                self.indent_level += 1
                return current_indent + f'public {self.current_class}({params_final}) {{'
            else:
                self.indent_level += 1
                return current_indent + f'public {self.current_class}() {{'
        
        # Retorno de funciones
        if line.startswith('retornar ') or line.startswith('devolver '):
            value = line.replace('retornar ', '').replace('devolver ', '').strip()
            # Si el valor contiene comillas, mantenerlas; si no, asumimos que es una expresión
            if '"' in value or "'" in value:
                return current_indent + f'return {value};'
            else:
                # Para expresiones o variables, mantener como está
                return current_indent + f'return {value};'
        
        # Manejo de errores y excepciones
        if line.startswith('intentar'):
            self.indent_level += 1
            return current_indent + 'try {'
        
        if line.startswith('capturar '):
            exception_type = line.replace('capturar ', '').strip()
            if self.indent_level > 1:
                self.indent_level -= 1
            catch_indent = self.indent()
            self.indent_level += 1
            if exception_type in ['error', 'excepcion', 'excepción']:
                return catch_indent + '} catch (Exception e) {'
            else:
                return catch_indent + f'}} catch ({exception_type} e) {{'
        
        if line.startswith('finalmente'):
            if self.indent_level > 1:
                self.indent_level -= 1
            finally_indent = self.indent()
            self.indent_level += 1
            return finally_indent + '} finally {'
        
        if line.startswith('lanzar '):
            exception = line.replace('lanzar ', '').strip()
            return current_indent + f'throw new Exception({exception});'
        
        # Asignación de variables con detección avanzada de tipos
        if ' = ' in line and not any(line.startswith(kw) for kw in ['if', 'while', 'for', 'public', 'try', 'catch']):
            # Convertir operadores en la asignación
            line_converted = line
            line_converted = line_converted.replace(' mayor que ', ' > ')
            line_converted = line_converted.replace(' menor que ', ' < ')
            line_converted = line_converted.replace(' igual a ', ' == ')
            line_converted = line_converted.replace(' es mayor que ', ' > ')
            line_converted = line_converted.replace(' es menor que ', ' < ')
            line_converted = line_converted.replace(' es igual a ', ' == ')
            
            var_name = line_converted.split(' = ')[0].strip()
            right_side = line_converted.split(' = ', 1)[1].strip()
            
            if var_name not in self.declared_vars:
                self.declared_vars.add(var_name)
                # Inferencia de tipos avanzada
                var_type = self.infer_java_type(right_side)
                return current_indent + f'{var_type} {line_converted};'
            else:
                return current_indent + line_converted + ';'
        
        # Creación explícita de variables con tipo
        if line.startswith('crear variable '):
            var_def = line.replace('crear variable ', '').strip()
            if ' tipo ' in var_def:
                parts = var_def.split(' tipo ')
                var_name = parts[0].strip()
                var_type_str = parts[1].strip()
                
                # Mapear tipos de Vader a Java
                if var_type_str in ['numero', 'entero']:
                    java_type = 'int'
                elif var_type_str in ['decimal', 'flotante']:
                    java_type = 'double'
                elif var_type_str in ['texto', 'cadena']:
                    java_type = 'String'
                elif var_type_str in ['booleano', 'logico']:
                    java_type = 'boolean'
                elif var_type_str == 'lista':
                    java_type = 'List<String>'
                elif var_type_str == 'mapa':
                    java_type = 'Map<String, String>'
                else:
                    java_type = 'String'
                
                if var_name not in self.declared_vars:
                    self.declared_vars.add(var_name)
                    if java_type == 'List<String>':
                        return current_indent + f'{java_type} {var_name} = new ArrayList<>();'
                    elif java_type == 'Map<String, String>':
                        return current_indent + f'{java_type} {var_name} = new HashMap<>();'
                    else:
                        return current_indent + f'{java_type} {var_name};'
            else:
                # Variable sin tipo explícito
                if var_def not in self.declared_vars:
                    self.declared_vars.add(var_def)
                    return current_indent + f'String {var_def};'
        
        # Llamadas a funciones o expresiones
        if not line.endswith(';'):
            return current_indent + line + ';'
        else:
            return current_indent + line
    
    def infer_java_type(self, value):
        """Infiere el tipo de Java basado en el valor"""
        value = value.strip()
        
        # Booleanos
        if value in ['true', 'false', 'verdadero', 'falso']:
            return 'boolean'
        
        # Strings
        if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
            return 'String'
        
        # Números enteros
        if value.isdigit() or (value.startswith('-') and value[1:].isdigit()):
            return 'int'
        
        # Números decimales
        if '.' in value and value.replace('.', '').replace('-', '').isdigit():
            return 'double'
        
        # Arrays o listas
        if value.startswith('[') and value.endswith(']'):
            return 'String[]'
        
        # Llamadas a métodos que devuelven tipos específicos
        if 'new ArrayList' in value:
            return 'List<String>'
        elif 'new HashMap' in value:
            return 'Map<String, String>'
        elif '.length()' in value or '.size()' in value:
            return 'int'
        elif 'Math.' in value:
            return 'double'
        
        # Por defecto, String
        return 'String'
    
    def indent(self):
        return '    ' * self.indent_level

def transpile_to_java(vader_code):
    transpiler = JavaTranspiler()
    return transpiler.transpile(vader_code)

def transpilar(vader_code):
    """Alias for CLI compatibility"""
    return transpile_to_java(vader_code)
