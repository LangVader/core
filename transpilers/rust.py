#!/usr/bin/env python3
"""
Transpilador de Vader a Rust
Convierte código Vader en español natural a Rust válido y funcional
"""

import re

class RustTranspiler:
    def __init__(self):
        self.indent_level = 0
        self.in_function = False
        self.in_impl = False
        self.declared_vars = set()
        self.current_struct = None
        
    def indent(self):
        return '    ' * self.indent_level
    
    def infer_rust_type(self, value):
        """Infiere el tipo de Rust basado en el valor"""
        if value.strip() in ['true', 'false', 'verdadero', 'falso']:
            return 'bool'
        elif value.strip().startswith('"') and value.strip().endswith('"'):
            return 'String'
        elif '.' in value and value.replace('.', '').replace('-', '').isdigit():
            return 'f64'
        elif value.replace('-', '').isdigit():
            return 'i32'
        else:
            return ''
    
    def transpile(self, vader_code):
        """Transpila código Vader completo a Rust"""
        lines = vader_code.split('\n')
        rust_lines = [
            'use std::io;',
            'use std::collections::HashMap;',
            'use std::collections::VecDeque;',
            ''
        ]
        
        # Separar funciones, structs y código main
        functions_code, structs_code, main_code = self.separate_code_sections(lines)
        
        # Generar funciones primero
        if functions_code:
            for line in functions_code:
                if line.strip():  # Solo procesar líneas no vacías
                    rust_line = self.transpile_line(line.strip())
                    if rust_line is not None:
                        if isinstance(rust_line, list):
                            rust_lines.extend(rust_line)
                        else:
                            rust_lines.append(rust_line)
            rust_lines.append('')
        
        # Generar structs
        if structs_code:
            for line in structs_code:
                if line.strip():  # Solo procesar líneas no vacías
                    rust_line = self.transpile_line(line.strip())
                    if rust_line is not None:
                        if isinstance(rust_line, list):
                            rust_lines.extend(rust_line)
                        else:
                            rust_lines.append(rust_line)
            rust_lines.append('')
        
        # Generar main
        rust_lines.append('fn main() {')
        self.indent_level = 1
        self.declared_vars = set()
        
        for line in main_code:
            line = line.strip()
            
            if not line:
                rust_lines.append('')
                continue
                
            if line.startswith('#'):
                rust_lines.append(self.indent() + '//' + line[1:])
                continue
                
            rust_line = self.transpile_line(line)
            if rust_line is not None:
                if isinstance(rust_line, list):
                    rust_lines.extend(rust_line)
                else:
                    rust_lines.append(rust_line)
        
        rust_lines.append('}')
        return '\n'.join(rust_lines)
    
    def separate_code_sections(self, lines):
        """Separa el código en funciones, structs y main basado en sintaxis Vader original"""
        functions = []
        structs = []
        main_code = []
        
        in_function = False
        in_struct = False
        current_block = []
        
        for line in lines:
            stripped = line.strip()
            
            # Detectar inicio de función en sintaxis Vader
            if stripped.startswith('funcion ') or stripped.startswith('función '):
                if current_block:
                    main_code.extend(current_block)
                    current_block = []
                in_function = True
                in_struct = False
                current_block = [line]
                continue
            
            # Detectar inicio de struct en sintaxis Vader
            elif stripped.startswith('struct ') or stripped.startswith('clase '):
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
                    functions.extend(current_block)
                    functions.append('')
                    in_function = False
                    current_block = []
                    continue
            
            elif stripped in ['fin struct', 'fin clase']:
                if in_struct:
                    current_block.append(line)
                    structs.extend(current_block)
                    structs.append('')
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
        
        return functions, structs, main_code
    
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
        # Fin de bloque (funciones, structs, if, while, etc.)
        if line in ['fin', 'fin funcion', 'fin función', 'fin struct', 'fin clase', 'fin si', 'fin mientras']:
            if self.indent_level > 1:
                self.indent_level -= 1
                return '    ' * (self.indent_level - 1) + '}'
            return None
        
        current_indent = self.indent()
        
        # Variables booleanas
        line = line.replace('verdadero', 'true')
        line = line.replace('falso', 'false')
        line = line.replace('nulo', 'None')
        
        # Operaciones matemáticas - mapeo correcto a funciones Rust
        line = re.sub(r'raiz\(([^)]+)\)', r'(\1 as f64).sqrt()', line)
        line = re.sub(r'potencia\(([^,]+),\s*([^)]+)\)', r'(\1 as f64).powf(\2 as f64)', line)
        line = re.sub(r'absoluto\(([^)]+)\)', r'(\1).abs()', line)
        line = re.sub(r'redondear\(([^)]+)\)', r'(\1 as f64).round()', line)
        line = re.sub(r'numero\(([^)]+)\)', r'\1.parse::<i32>().unwrap_or(0)', line)
        
        # Función texto() para conversión a string
        line = re.sub(r'texto\(([^)]+)\)', r'\1.to_string()', line)
        
        # Print statements
        if line.startswith('mostrar ') or line.startswith('decir '):
            content = line.split(' ', 1)[1]
            # Convertir concatenación con + a format! macro
            if ' + ' in content:
                # Convertir concatenación a format!
                parts = [p.strip() for p in content.split(' + ')]
                format_str = ''
                args = []
                for part in parts:
                    if part.startswith('"') and part.endswith('"'):
                        format_str += part[1:-1]
                    else:
                        format_str += '{}'
                        args.append(part)
                
                if args:
                    args_str = ', '.join(args)
                    return current_indent + f'println!("{format_str}", {args_str});'
                else:
                    return current_indent + f'println!("{format_str}");'
            else:
                if content.startswith('"') and content.endswith('"'):
                    return current_indent + f'println!({content});'
                else:
                    return current_indent + f'println!("{{}}", {content});'
        
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
            
            result = current_indent + f'println!({question});\n'
            result += current_indent + f'let mut {var_name} = String::new();\n'
            result += current_indent + f'io::stdin().read_line(&mut {var_name}).expect("Failed to read line");\n'
            result += current_indent + f'{var_name} = {var_name}.trim().to_string();'
            self.declared_vars.add(var_name)
            return result
        
        # Asignación de variables
        if '=' in line and not any(op in line for op in ['==', '!=', '<=', '>=']):
            parts = line.split('=', 1)
            var_name = parts[0].strip()
            value = parts[1].strip()
            
            if var_name not in self.declared_vars:
                rust_type = self.infer_rust_type(value)
                self.declared_vars.add(var_name)
                if rust_type:
                    return current_indent + f'let mut {var_name}: {rust_type} = {value};'
                else:
                    return current_indent + f'let mut {var_name} = {value};'
            else:
                return current_indent + f'{var_name} = {value};'
        
        # Condicionales
        if line.startswith('si ') and ('entonces' in line or line.endswith(':')):
            condition = line.replace('si ', '').replace(' entonces', '').replace(':', '').strip()
            condition = self.convert_operators(condition)
            self.indent_level += 1
            return current_indent + f'if {condition} {{'
        
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
            return current_indent + f'for _ in 0..{times} {{'
        
        if 'repetir con cada' in line or 'para cada' in line:
            line_clean = line.replace('repetir con cada ', '').replace('para cada ', '')
            if ' en ' in line_clean:
                parts = line_clean.split(' en ')
                var_name = parts[0].strip()
                iterable = parts[1].strip()
                self.indent_level += 1
                return current_indent + f'for {var_name} in {iterable} {{'
        
        # Bucles while
        if line.startswith('mientras '):
            condition = line.replace('mientras ', '').replace(':', '').strip()
            condition = self.convert_operators(condition)
            self.indent_level += 1
            return current_indent + f'while {condition} {{'
        
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
                    return_type = ' -> i32'
                elif return_type_str in ['decimal', 'flotante']:
                    return_type = ' -> f64'
                elif return_type_str in ['texto', 'cadena']:
                    return_type = ' -> String'
                elif return_type_str in ['booleano', 'logico']:
                    return_type = ' -> bool'
            
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
                                typed_params.append(f'{param_name}: i32')
                            elif param_type in ['decimal', 'flotante']:
                                typed_params.append(f'{param_name}: f64')
                            elif param_type in ['texto', 'cadena']:
                                typed_params.append(f'{param_name}: String')
                            elif param_type in ['booleano', 'logico']:
                                typed_params.append(f'{param_name}: bool')
                            else:
                                typed_params.append(f'{param_name}: String')
                        else:
                            typed_params.append(f'{param}: String')
                
                params_final = ', '.join(typed_params)
                self.indent_level += 1
                return current_indent + f'fn {name}({params_final}){return_type} {{'
            else:
                name = func_def.replace(':', '').strip()
                self.indent_level += 1
                return current_indent + f'fn {name}(){return_type} {{'
        
        # Retorno de funciones
        if line.startswith('retornar ') or line.startswith('devolver '):
            value = line.replace('retornar ', '').replace('devolver ', '').strip()
            # Si el valor contiene comillas, mantenerlas; si no, asumimos que es una expresión
            if '"' in value or "'" in value:
                return current_indent + f'{value}'
            else:
                # Para expresiones o variables, mantener como está
                return current_indent + f'{value}'
        
        # Definición de structs avanzados
        if line.startswith('struct ') or line.startswith('clase '):
            struct_name = line.replace('struct ', '').replace('clase ', '').replace(':', '').strip()
            self.current_struct = struct_name
            self.in_impl = True
            self.indent_level += 1
            return current_indent + f'struct {struct_name} {{'
        
        # Atributos de struct
        if line.startswith('atributo ') and self.in_impl:
            attr_def = line.replace('atributo ', '').strip()
            if ' tipo ' in attr_def:
                attr_parts = attr_def.split(' tipo ')
                attr_name = attr_parts[0].strip()
                attr_type = attr_parts[1].strip()
                if attr_type in ['numero', 'entero']:
                    return current_indent + f'{attr_name}: i32,'
                elif attr_type in ['decimal', 'flotante']:
                    return current_indent + f'{attr_name}: f64,'
                elif attr_type in ['texto', 'cadena']:
                    return current_indent + f'{attr_name}: String,'
                elif attr_type in ['booleano', 'logico']:
                    return current_indent + f'{attr_name}: bool,'
                else:
                    return current_indent + f'{attr_name}: String,'
            else:
                return current_indent + f'{attr_def}: String,'
        
        # Constructor de struct (impl block)
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
                            typed_params.append(f'{param_name}: i32')
                        elif param_type in ['decimal', 'flotante']:
                            typed_params.append(f'{param_name}: f64')
                        elif param_type in ['texto', 'cadena']:
                            typed_params.append(f'{param_name}: String')
                        elif param_type in ['booleano', 'logico']:
                            typed_params.append(f'{param_name}: bool')
                        else:
                            typed_params.append(f'{param_name}: String')
                    else:
                        # Inferir tipo basado en el nombre del parámetro
                        if param in ['edad', 'numero', 'cantidad', 'id']:
                            typed_params.append(f'{param}: i32')
                        elif param in ['precio', 'salario', 'peso', 'altura']:
                            typed_params.append(f'{param}: f64')
                        elif param in ['activo', 'visible', 'habilitado']:
                            typed_params.append(f'{param}: bool')
                        else:
                            typed_params.append(f'{param}: String')
                
                params_final = ', '.join(typed_params)
                # Generar impl block
                impl_lines = [
                    '}',
                    '',
                    f'impl {self.current_struct} {{',
                    f'    pub fn new({params_final}) -> Self {{'
                ]
                self.indent_level += 2
                return impl_lines
            else:
                # Constructor sin parámetros
                impl_lines = [
                    '}',
                    '',
                    f'impl {self.current_struct} {{',
                    f'    pub fn new() -> Self {{'
                ]
                self.indent_level += 2
                return impl_lines
        
        # Manejo de errores y excepciones
        if line.startswith('intentar'):
            self.indent_level += 1
            return current_indent + 'match (|| -> Result<(), Box<dyn std::error::Error>> {'
        
        if line.startswith('capturar '):
            exception_type = line.replace('capturar ', '').strip()
            if self.indent_level > 1:
                self.indent_level -= 1
            catch_indent = self.indent()
            self.indent_level += 1
            return catch_indent + '    Ok(())\n})() {\n    Err(e) => {'
        
        if line.startswith('finalmente'):
            if self.indent_level > 1:
                self.indent_level -= 1
            finally_indent = self.indent()
            self.indent_level += 1
            return finally_indent + '},\n    Ok(_) => {'
        
        if line.startswith('lanzar '):
            exception = line.replace('lanzar ', '').strip()
            return current_indent + f'return Err(Box::new(std::io::Error::new(std::io::ErrorKind::Other, {exception})));'
        
        # Crear listas/vectores
        if line.startswith('crear lista '):
            list_name = line.replace('crear lista ', '').strip()
            return current_indent + f'let mut {list_name}: Vec<String> = Vec::new();'
        
        # Agregar elementos a listas
        if line.startswith('agregar ') and ' a ' in line:
            parts = line.replace('agregar ', '').split(' a ')
            element = parts[0].strip()
            list_name = parts[1].strip()
            return current_indent + f'{list_name}.push({element}.to_string());'
        
        # Crear mapas
        if line.startswith('crear mapa '):
            map_name = line.replace('crear mapa ', '').strip()
            return current_indent + f'let mut {map_name}: HashMap<String, String> = HashMap::new();'
        
        # Línea de código general
        if line.strip():
            return current_indent + line + ';'
        
        return None
    
    def convert_operators(self, condition):
        """Convierte operadores de Vader a Rust"""
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

def transpile_to_rust(vader_code):
    transpiler = RustTranspiler()
    return transpiler.transpile(vader_code)

def transpilar(vader_code):
    """Alias for CLI compatibility"""
    return transpile_to_rust(vader_code)
