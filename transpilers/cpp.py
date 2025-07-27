#!/usr/bin/env python3
"""
Transpilador C++ COMPLETO para Vader
Convierte código Vader en español natural a C++ válido y funcional
Versión: COMPLETA con todas las características avanzadas
"""

import re

class CppTranspiler:
    def __init__(self):
        self.indent_level = 0
        self.in_function = False
        self.in_class = False
        self.declared_vars = set()
        self.declared_functions = set()
        self.declared_classes = set()
        self.includes = set([
            '<iostream>',
            '<string>',
            '<vector>',
            '<map>',
            '<algorithm>',
            '<cmath>',
            '<stdexcept>',
            '<memory>'
        ])
        self.current_class = None
        
    def indent(self):
        return '    ' * self.indent_level
    
    def infer_cpp_type(self, value):
        """Infiere el tipo de C++ basado en el valor"""
        if value.strip() in ['true', 'false', 'verdadero', 'falso']:
            return 'bool'
        elif value.strip().startswith('"') and value.strip().endswith('"'):
            return 'std::string'
        elif '.' in value and value.replace('.', '').replace('-', '').isdigit():
            return 'double'
        elif value.replace('-', '').isdigit():
            return 'int'
        else:
            # Podría ser una variable o expresión
            return 'auto'
    
    def transpile(self, vader_code):
        """Transpila código Vader completo a C++"""
        lines = vader_code.split('\n')
        cpp_lines = []
        
        # Headers y namespace
        for include in sorted(self.includes):
            cpp_lines.append(f'#include {include}')
        cpp_lines.append('')
        cpp_lines.append('using namespace std;')
        cpp_lines.append('')
        
        # Separar funciones, clases y código main
        functions_code, classes_code, main_code = self.separate_code_sections(lines)
        
        # Generar funciones primero
        if functions_code:
            for line in functions_code:
                if line.strip():  # Solo procesar líneas no vacías
                    cpp_line = self.transpile_line(line.strip())
                    if cpp_line is not None:
                        if isinstance(cpp_line, list):
                            cpp_lines.extend(cpp_line)
                        else:
                            cpp_lines.append(cpp_line)
            cpp_lines.append('')
        
        # Generar clases
        if classes_code:
            for line in classes_code:
                if line.strip():  # Solo procesar líneas no vacías
                    cpp_line = self.transpile_line(line.strip())
                    if cpp_line is not None:
                        if isinstance(cpp_line, list):
                            cpp_lines.extend(cpp_line)
                        else:
                            cpp_lines.append(cpp_line)
            cpp_lines.append('')
        
        # Generar main
        cpp_lines.append('int main() {')
        self.indent_level = 1
        self.declared_vars = set()
        
        for line in main_code:
            line = line.strip()
            
            if not line:
                cpp_lines.append('')
                continue
                
            if line.startswith('#'):
                cpp_lines.append(self.indent() + '//' + line[1:])
                continue
                
            cpp_line = self.transpile_line(line)
            if cpp_line is not None:
                if isinstance(cpp_line, list):
                    cpp_lines.extend(cpp_line)
                else:
                    cpp_lines.append(cpp_line)
        
        cpp_lines.extend([
            '    return 0;',
            '}'
        ])
        
        return '\n'.join(cpp_lines)
    
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
        """Transpila una línea individual"""
        if '#' in line:
            code_part = line.split('#')[0].strip()
            comment_part = '//' + '#'.join(line.split('#')[1:])
            if code_part:
                return self.process_code_line(code_part) + '  ' + comment_part
            else:
                return '//' + line[1:]
        
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
        
        # Variables booleanas
        line = line.replace('verdadero', 'true')
        line = line.replace('falso', 'false')
        line = line.replace('nulo', 'nullptr')
        
        # Operaciones matemáticas
        line = line.replace('raiz(', 'sqrt(')
        line = line.replace('potencia(', 'pow(')
        line = line.replace('absoluto(', 'abs(')
        line = line.replace('redondear(', 'round(')
        line = line.replace('numero(', 'stoi(')
        
        # Función texto() para conversión a string
        line = re.sub(r'texto\(([^)]+)\)', r'to_string(\1)', line)
        
        # Print statements
        if line.startswith('mostrar ') or line.startswith('decir '):
            content = line.split(' ', 1)[1]
            # Convertir concatenación con + a << para cout
            content = content.replace(' + ', ' << ')
            return current_indent + f'cout << {content} << endl;'
        
        # Input statements
        if 'preguntar ' in line and ('guardar' in line or 'guárdalo' in line):
            if 'guardar la respuesta en' in line:
                parts = line.split('guardar la respuesta en')
                question = parts[0].replace('preguntar ', '').strip()
                var_name = parts[1].strip()
            elif 'guárdalo en' in line:
                parts = line.split('guárdalo en')
                question = parts[0].replace('preguntar ', '').strip()
                var_name = parts[1].strip()
            else:
                return current_indent + '// ' + line
            
            result = current_indent + f'cout << {question} << endl;\n'
            result += current_indent + f'string {var_name};\n'
            result += current_indent + f'getline(cin, {var_name});'
            self.declared_vars.add(var_name)
            return result
        
        # Asignación de variables
        if '=' in line and not any(op in line for op in ['==', '!=', '<=', '>=']):
            parts = line.split('=', 1)
            var_name = parts[0].strip()
            value = parts[1].strip()
            
            if var_name not in self.declared_vars:
                cpp_type = self.infer_cpp_type(value)
                self.declared_vars.add(var_name)
                return current_indent + f'{cpp_type} {var_name} = {value};'
            else:
                return current_indent + f'{var_name} = {value};'
        
        # Condicionales
        if line.startswith('si ') and ('entonces' in line or line.endswith(':')):
            condition = line.replace('si ', '').replace(' entonces', '').replace(':', '').strip()
            condition = self.convert_operators(condition)
            self.indent_level += 1
            return current_indent + f'if ({condition}) {{'
        
        # Else
        if line == 'sino' or line == 'si no':
            if self.indent_level > 1:
                self.indent_level -= 1
            else_indent = self.indent()
            self.indent_level += 1
            return else_indent + '} else {'
        
        # Bucles for
        if line.startswith('repetir ') and ' veces' in line:
            times = line.replace('repetir ', '').replace(' veces', '').strip()
            self.indent_level += 1
            return current_indent + f'for (int i = 0; i < {times}; i++) {{'
        
        if 'repetir con cada' in line or 'para cada' in line:
            line_clean = line.replace('repetir con cada ', '').replace('para cada ', '')
            if ' en ' in line_clean:
                parts = line_clean.split(' en ')
                var_name = parts[0].strip()
                iterable = parts[1].strip()
                self.indent_level += 1
                return current_indent + f'for (auto {var_name} : {iterable}) {{'
        
        # Bucles while
        if line.startswith('mientras '):
            condition = line.replace('mientras ', '').replace(':', '').strip()
            condition = self.convert_operators(condition)
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
                    return_type = 'string'
                elif return_type_str in ['booleano', 'logico']:
                    return_type = 'bool'
            
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
                                typed_params.append(f'string {param_name}')
                            elif param_type in ['booleano', 'logico']:
                                typed_params.append(f'bool {param_name}')
                            else:
                                typed_params.append(f'string {param_name}')
                        else:
                            typed_params.append(f'string {param}')
                
                params_final = ', '.join(typed_params)
                self.indent_level += 1
                return current_indent + f'{return_type} {name}({params_final}) {{'
            else:
                name = func_def.replace(':', '').strip()
                self.indent_level += 1
                return current_indent + f'{return_type} {name}() {{'
        
        # Retorno de funciones
        if line.startswith('retornar ') or line.startswith('devolver '):
            value = line.replace('retornar ', '').replace('devolver ', '').strip()
            # Si el valor contiene comillas, mantenerlas; si no, asumimos que es una expresión
            if '"' in value or "'" in value:
                return current_indent + f'return {value};'
            else:
                # Para expresiones o variables, mantener como está
                return current_indent + f'return {value};'
        
        # Definición de clases avanzadas
        if line.startswith('clase '):
            class_name = line.replace('clase ', '').replace(':', '').strip()
            self.current_class = class_name
            self.in_class = True
            self.indent_level += 1
            return current_indent + f'class {class_name} {{'
        
        # Atributos de clase
        if line.startswith('atributo ') and self.in_class:
            attr_def = line.replace('atributo ', '').strip()
            if ' tipo ' in attr_def:
                attr_parts = attr_def.split(' tipo ')
                attr_name = attr_parts[0].strip()
                attr_type = attr_parts[1].strip()
                if attr_type in ['numero', 'entero']:
                    return current_indent + f'private: int {attr_name};'
                elif attr_type in ['decimal', 'flotante']:
                    return current_indent + f'private: double {attr_name};'
                elif attr_type in ['texto', 'cadena']:
                    return current_indent + f'private: string {attr_name};'
                elif attr_type in ['booleano', 'logico']:
                    return current_indent + f'private: bool {attr_name};'
                else:
                    return current_indent + f'private: string {attr_name};'
            else:
                return current_indent + f'private: string {attr_def};'
        
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
                            typed_params.append(f'string {param_name}')
                        elif param_type in ['booleano', 'logico']:
                            typed_params.append(f'bool {param_name}')
                        else:
                            typed_params.append(f'string {param_name}')
                    else:
                        # Inferir tipo basado en el nombre del parámetro
                        if param in ['edad', 'numero', 'cantidad', 'id']:
                            typed_params.append(f'int {param}')
                        elif param in ['precio', 'salario', 'peso', 'altura']:
                            typed_params.append(f'double {param}')
                        elif param in ['activo', 'visible', 'habilitado']:
                            typed_params.append(f'bool {param}')
                        else:
                            typed_params.append(f'string {param}')
                
                params_final = ', '.join(typed_params)
                self.indent_level += 1
                return current_indent + f'public: {self.current_class}({params_final}) {{'
            else:
                self.indent_level += 1
                return current_indent + f'public: {self.current_class}() {{'
        
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
                return catch_indent + '} catch (const exception& e) {'
            else:
                return catch_indent + f'}} catch (const {exception_type}& e) {{'
        
        if line.startswith('finalmente'):
            if self.indent_level > 1:
                self.indent_level -= 1
            finally_indent = self.indent()
            self.indent_level += 1
            return finally_indent + '} finally {'
        
        if line.startswith('lanzar '):
            exception = line.replace('lanzar ', '').strip()
            return current_indent + f'throw runtime_error({exception});'
        
        # Línea de código general (expresión o asignación)
        if line.strip():
            return current_indent + line + ';'
        
        return None
    
    def convert_operators(self, condition):
        """Convierte operadores de Vader a C++"""
        condition = condition.replace(' es igual a ', ' == ')
        condition = condition.replace(' es mayor que ', ' > ')
        condition = condition.replace(' es menor que ', ' < ')
        condition = condition.replace(' mayor que ', ' > ')
        condition = condition.replace(' menor que ', ' < ')
        condition = condition.replace(' igual a ', ' == ')
        condition = condition.replace(' y ', ' && ')
        condition = condition.replace(' o ', ' || ')
        condition = condition.replace(' no ', ' ! ')
        return condition
