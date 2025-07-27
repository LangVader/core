#!/usr/bin/env python3
"""
Transpilador de Vader a Go
Convierte código Vader en español natural a Go válido y funcional
"""

import re

class GoTranspiler:
    def __init__(self):
        self.indent_level = 0
        self.in_function = False
        self.declared_vars = set()
        self.current_struct = None
        
    def indent(self):
        return '    ' * self.indent_level
    
    def infer_go_type(self, value):
        """Infiere el tipo de Go basado en el valor"""
        if value.strip() in ['true', 'false', 'verdadero', 'falso']:
            return 'bool'
        elif value.strip().startswith('"') and value.strip().endswith('"'):
            return 'string'
        elif '.' in value and value.replace('.', '').replace('-', '').isdigit():
            return 'float64'
        elif value.replace('-', '').isdigit():
            return 'int'
        else:
            return ''
    
    def separate_code_sections(self, lines):
        """Separa el código en secciones de funciones, structs y main"""
        functions_code = []
        structs_code = []
        main_code = []
        
        in_function = False
        in_struct = False
        current_block = []
        
        for line in lines:
            stripped = line.strip()
            
            # Detectar inicio de función
            if stripped.startswith('funcion ') or stripped.startswith('función '):
                if current_block:
                    main_code.extend(current_block)
                    current_block = []
                in_function = True
                in_struct = False
                current_block = [line]
                continue
            
            # Detectar inicio de struct
            elif stripped.startswith('clase '):
                if current_block:
                    main_code.extend(current_block)
                    current_block = []
                in_struct = True
                in_function = False
                current_block = [line]
                continue
            
            # Detectar fin de bloques
            elif stripped in ['fin', 'fin funcion', 'fin función']:
                if in_function:
                    current_block.append(line)
                    functions_code.extend(current_block)
                    functions_code.append('')
                    in_function = False
                    current_block = []
                    continue
            
            elif stripped in ['fin clase']:
                if in_struct:
                    current_block.append(line)
                    structs_code.extend(current_block)
                    structs_code.append('')
                    in_struct = False
                    current_block = []
                    continue
            
            # Agregar líneas al bloque actual
            if in_function or in_struct:
                current_block.append(line)
            else:
                current_block.append(line)
        
        # Agregar código restante a main
        if current_block:
            main_code.extend(current_block)
        
        return functions_code, structs_code, main_code
    
    def transpile(self, vader_code):
        """Transpila código Vader completo a Go - VERSIÓN COMPLETA"""
        lines = [line.strip() for line in vader_code.split('\n') if line.strip()]
        
        # Separar código en secciones
        functions_code, structs_code, main_code = self.separate_code_sections(lines)
        
        go_lines = [
            'package main',
            '',
            'import (',
            '    "fmt"',
            '    "math"',
            '    "strconv"',
            '    "errors"',
            ')',
            ''
        ]
        
        # Procesar structs primero
        if structs_code:
            for line in structs_code:
                if line.strip():
                    go_line = self.process_code_line(line)
                    if go_line:
                        if isinstance(go_line, list):
                            go_lines.extend(go_line)
                        else:
                            go_lines.append(go_line)
            go_lines.append('')
        
        # Procesar funciones
        if functions_code:
            for line in functions_code:
                if line.strip():
                    go_line = self.process_code_line(line)
                    if go_line:
                        if isinstance(go_line, list):
                            go_lines.extend(go_line)
                        else:
                            go_lines.append(go_line)
            go_lines.append('')
        
        # Procesar main
        go_lines.append('func main() {')
        self.indent_level = 1
        
        for line in main_code:
            if line.strip():
                if line.startswith('#'):
                    go_lines.append(self.indent() + '//' + line[1:])
                else:
                    go_line = self.process_code_line(line)
                    if go_line:
                        if isinstance(go_line, list):
                            go_lines.extend(go_line)
                        else:
                            go_lines.append(go_line)
        
        go_lines.append('}')
        return '\n'.join(go_lines)
    
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
        # Fin de bloque
        if line in ['fin', 'fin funcion', 'fin función', 'fin clase', 'fin si', 'fin mientras', 'fin repetir']:
            if self.indent_level > 0:
                self.indent_level -= 1
                return '    ' * self.indent_level + '}'
            return None
        
        current_indent = '    ' * self.indent_level
        
        # Variables booleanas
        line = line.replace('verdadero', 'true')
        line = line.replace('falso', 'false')
        line = line.replace('nulo', 'nil')
        
        # Operaciones matemáticas
        line = re.sub(r'raiz\(([^)]+)\)', r'math.Sqrt(float64(\1))', line)
        line = re.sub(r'potencia\(([^,]+),\s*([^)]+)\)', r'math.Pow(float64(\1), float64(\2))', line)
        line = re.sub(r'absoluto\(([^)]+)\)', r'math.Abs(float64(\1))', line)
        line = re.sub(r'redondear\(([^)]+)\)', r'math.Round(float64(\1))', line)
        line = re.sub(r'numero\(([^)]+)\)', r'strconv.Atoi(\1)', line)
        
        # Función texto() para conversión a string
        line = re.sub(r'texto\(([^)]+)\)', r'strconv.Itoa(\1)', line)
        
        # Definición de funciones avanzadas con tipos
        if line.startswith('funcion ') or line.startswith('función '):
            func_def = line.replace('funcion ', '').replace('función ', '')
            
            # Detectar tipo de retorno
            return_type = ''
            if ' que devuelve ' in func_def:
                parts = func_def.split(' que devuelve ')
                func_def = parts[0]
                return_type_str = parts[1].replace(':', '').strip()
                if return_type_str in ['numero', 'entero']:
                    return_type = ' int'
                elif return_type_str in ['decimal', 'flotante']:
                    return_type = ' float64'
                elif return_type_str in ['texto', 'cadena']:
                    return_type = ' string'
                elif return_type_str in ['booleano', 'logico']:
                    return_type = ' bool'
            
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
                                typed_params.append(f'{param_name} int')
                            elif param_type in ['decimal', 'flotante']:
                                typed_params.append(f'{param_name} float64')
                            elif param_type in ['texto', 'cadena']:
                                typed_params.append(f'{param_name} string')
                            elif param_type in ['booleano', 'logico']:
                                typed_params.append(f'{param_name} bool')
                            else:
                                typed_params.append(f'{param_name} string')
                        else:
                            typed_params.append(f'{param} string')
                
                params_final = ', '.join(typed_params)
                self.indent_level += 1
                return current_indent + f'func {name}({params_final}){return_type} {{'
            else:
                name = func_def.replace(':', '').strip()
                self.indent_level += 1
                return current_indent + f'func {name}(){return_type} {{'
        
        # Retorno de funciones
        if line.startswith('retornar ') or line.startswith('devolver '):
            value = line.replace('retornar ', '').replace('devolver ', '').strip()
            return current_indent + f'return {value}'
        
        # Definición de structs avanzados
        if line.startswith('clase '):
            struct_name = line.replace('clase ', '').replace(':', '').strip()
            self.current_struct = struct_name
            self.indent_level += 1
            return current_indent + f'type {struct_name} struct {{'
        
        # Atributos de struct
        if line.startswith('atributo '):
            attr_def = line.replace('atributo ', '').strip()
            if ' tipo ' in attr_def:
                attr_parts = attr_def.split(' tipo ')
                attr_name = attr_parts[0].strip().title()
                attr_type = attr_parts[1].strip()
                if attr_type in ['numero', 'entero']:
                    return current_indent + f'{attr_name} int'
                elif attr_type in ['decimal', 'flotante']:
                    return current_indent + f'{attr_name} float64'
                elif attr_type in ['texto', 'cadena']:
                    return current_indent + f'{attr_name} string'
                elif attr_type in ['booleano', 'logico']:
                    return current_indent + f'{attr_name} bool'
                else:
                    return current_indent + f'{attr_name} string'
            else:
                attr_name = attr_def.title()
                return current_indent + f'{attr_name} string'
        
        # Constructor de struct (método New)
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
                            typed_params.append(f'{param_name} int')
                        elif param_type in ['decimal', 'flotante']:
                            typed_params.append(f'{param_name} float64')
                        elif param_type in ['texto', 'cadena']:
                            typed_params.append(f'{param_name} string')
                        elif param_type in ['booleano', 'logico']:
                            typed_params.append(f'{param_name} bool')
                        else:
                            typed_params.append(f'{param_name} string')
                    else:
                        typed_params.append(f'{param} string')
                
                params_final = ', '.join(typed_params)
                constructor_lines = [
                    '}',
                    '',
                    f'func New{self.current_struct}({params_final}) *{self.current_struct} {{',
                    f'    return &{self.current_struct}{{'
                ]
                self.indent_level += 2
                return constructor_lines
            else:
                constructor_lines = [
                    '}',
                    '',
                    f'func New{self.current_struct}() *{self.current_struct} {{',
                    f'    return &{self.current_struct}{{}}'
                ]
                return constructor_lines
        
        # Variables con tipos explícitos
        if line.startswith('crear variable ') and ' tipo ' in line:
            var_def = line.replace('crear variable ', '').strip()
            if ' tipo ' in var_def:
                var_parts = var_def.split(' tipo ')
                var_name = var_parts[0].strip()
                var_type = var_parts[1].strip()
                if var_type in ['numero', 'entero']:
                    return current_indent + f'var {var_name} int'
                elif var_type in ['decimal', 'flotante']:
                    return current_indent + f'var {var_name} float64'
                elif var_type in ['texto', 'cadena']:
                    return current_indent + f'var {var_name} string'
                elif var_type in ['booleano', 'logico']:
                    return current_indent + f'var {var_name} bool'
                else:
                    return current_indent + f'var {var_name} string'
        
        # Crear listas/slices
        if line.startswith('crear lista '):
            list_name = line.replace('crear lista ', '').strip()
            return current_indent + f'{list_name} := make([]string, 0)'
        
        # Agregar elementos a listas
        if line.startswith('agregar ') and ' a ' in line:
            parts = line.replace('agregar ', '').split(' a ')
            element = parts[0].strip()
            list_name = parts[1].strip()
            return current_indent + f'{list_name} = append({list_name}, {element})'
        
        # Crear mapas
        if line.startswith('crear mapa '):
            map_name = line.replace('crear mapa ', '').strip()
            return current_indent + f'{map_name} := make(map[string]string)'
        
        # Crear arrays
        if line.startswith('crear array ') and '[' in line and ']' in line:
            array_def = line.replace('crear array ', '').strip()
            if '[' in array_def and ']' in array_def:
                array_name = array_def.split('[')[0].strip()
                array_size = array_def.split('[')[1].split(']')[0].strip()
                return current_indent + f'var {array_name} [{array_size}]int'
        
        # Manejo de errores
        if line.startswith('intentar'):
            self.indent_level += 1
            return current_indent + 'func() {'
        
        if line.startswith('capturar '):
            exception_type = line.replace('capturar ', '').strip()
            if self.indent_level > 0:
                self.indent_level -= 1
            catch_indent = '    ' * self.indent_level
            self.indent_level += 1
            return catch_indent + '}()\nif err != nil {'
        
        if line.startswith('finalmente'):
            if self.indent_level > 0:
                self.indent_level -= 1
            finally_indent = '    ' * self.indent_level
            self.indent_level += 1
            return finally_indent + '}\ndefer func() {'
        
        if line.startswith('lanzar '):
            exception = line.replace('lanzar ', '').strip()
            return current_indent + f'panic({exception})'
        
        # Print statements
        if line.startswith('mostrar ') or line.startswith('decir '):
            content = line.split(' ', 1)[1]
            # Convertir concatenación con + a fmt.Sprintf
            if ' + ' in content:
                parts = [p.strip() for p in content.split(' + ')]
                format_str = ''
                args = []
                for part in parts:
                    if part.startswith('"') and part.endswith('"'):
                        format_str += part[1:-1]
                    else:
                        format_str += '%v'
                        args.append(part)
                
                if args:
                    args_str = ', '.join(args)
                    return current_indent + f'fmt.Printf("{format_str}\\n", {args_str})'
                else:
                    return current_indent + f'fmt.Println("{format_str}")'
            else:
                if content.startswith('"') and content.endswith('"'):
                    return current_indent + f'fmt.Println({content})'
                else:
                    return current_indent + f'fmt.Println({content})'
        
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
            
            result = current_indent + f'fmt.Print({question})\n'
            result += current_indent + f'{var_name}, _ := reader.ReadString(\'\\n\')\n'
            result += current_indent + f'{var_name} = strings.TrimSpace({var_name})'
            self.declared_vars.add(var_name)
            return result
        
        # Condicionales
        if line.startswith('si ') and ('entonces' in line or line.endswith(':')):
            condition = line.replace('si ', '').replace(' entonces', '').replace(':', '').strip()
            condition = self.convert_operators(condition)
            self.indent_level += 1
            return current_indent + f'if {condition} {{'
        
        # Else
        if line == 'sino' or line == 'si no' or line == 'sino:':
            if self.indent_level > 0:
                self.indent_level -= 1
            else_indent = '    ' * self.indent_level
            self.indent_level += 1
            return else_indent + '} else {'
        
        # Asignación de variables
        if '=' in line and not any(op in line for op in ['==', '!=', '>=', '<=']):
            parts = line.split('=', 1)
            var_name = parts[0].strip()
            value = parts[1].strip()
            
            if var_name not in self.declared_vars:
                self.declared_vars.add(var_name)
                var_type = self.infer_go_type(value)
                if var_type:
                    return current_indent + f'var {var_name} {var_type} = {value}'
                else:
                    return current_indent + f'{var_name} := {value}'
            else:
                return current_indent + f'{var_name} = {value}'
        
        # Bucles for
        if line.startswith('repetir ') and ' veces' in line:
            times = line.replace('repetir ', '').replace(' veces', '').strip()
            self.indent_level += 1
            return current_indent + f'for i := 0; i < {times}; i++ {{'
        
        if 'repetir con cada' in line or 'para cada' in line:
            line_clean = line.replace('repetir con cada ', '').replace('para cada ', '')
            if ' en ' in line_clean:
                parts = line_clean.split(' en ')
                var_name = parts[0].strip()
                iterable = parts[1].strip()
                self.indent_level += 1
                return current_indent + f'for _, {var_name} := range {iterable} {{'
        
        # Bucles while
        if line.startswith('mientras '):
            condition = line.replace('mientras ', '').replace(':', '').strip()
            condition = self.convert_operators(condition)
            self.indent_level += 1
            return current_indent + f'for {condition} {{'
        
        # Definición de funciones
        if line.startswith('funcion ') or line.startswith('función '):
            func_def = line.replace('funcion ', '').replace('función ', '')
            if ' con ' in func_def:
                name, params = func_def.split(' con ', 1)
                name = name.strip()
                params = params.replace(':', '').replace(' y ', ', ').strip()
                self.indent_level += 1
                self.in_function = True
                return current_indent + f'func {name}({params}) {{'
            else:
                name = func_def.replace(':', '').strip()
                self.indent_level += 1
                self.in_function = True
                return current_indent + f'func {name}() {{'
        
        # Return statements
        if line.startswith('devolver ') or line.startswith('retornar '):
            value = line.split(' ', 1)[1]
            return current_indent + f'return {value}'
        
        # Definición de structs
        if line.startswith('clase '):
            struct_name = line.replace('clase ', '').replace(':', '').strip()
            self.indent_level += 1
            return current_indent + f'type {struct_name} struct {{'
        
        # Línea de código general
        if line.strip():
            return current_indent + line
        
        return None
    
    def convert_operators(self, condition):
        """Convierte operadores de Vader a Go"""
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

def transpile_to_go(vader_code):
    transpiler = GoTranspiler()
    return transpiler.transpile(vader_code)

def transpilar(vader_code):
    """Alias for CLI compatibility"""
    return transpile_to_go(vader_code)
