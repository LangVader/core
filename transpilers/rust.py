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
            '',
            'fn main() {'
        ]
        
        self.indent_level = 1
        self.declared_vars = set()
        
        for line in lines:
            original_line = line
            line = line.strip()
            
            if not line:
                rust_lines.append('')
                continue
                
            if line.startswith('#'):
                rust_lines.append(self.indent() + '//' + line[1:])
                continue
                
            rust_line = self.transpile_line(line)
            if rust_line is not None:
                rust_lines.append(rust_line)
        
        rust_lines.append('}')
        return '\n'.join(rust_lines)
    
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
        """Procesa una línea de código"""
        # Manejo de fin de bloques
        if line in ['fin si', 'fin', 'fin funcion', 'fin función', 'fin clase', 'fin mientras', 'fin repetir']:
            if self.indent_level > 1:
                self.indent_level -= 1
            return self.indent() + '}'
        
        current_indent = self.indent()
        
        # Variables booleanas
        line = line.replace('verdadero', 'true')
        line = line.replace('falso', 'false')
        line = line.replace('nulo', 'None')
        
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
        
        # Definición de funciones
        if line.startswith('funcion ') or line.startswith('función '):
            func_def = line.replace('funcion ', '').replace('función ', '')
            if ' con ' in func_def:
                name, params = func_def.split(' con ', 1)
                name = name.strip()
                params = params.replace(':', '').replace(' y ', ', ').strip()
                self.indent_level += 1
                self.in_function = True
                return current_indent + f'fn {name}({params}) {{'
            else:
                name = func_def.replace(':', '').strip()
                self.indent_level += 1
                self.in_function = True
                return current_indent + f'fn {name}() {{'
        
        # Return statements
        if line.startswith('devolver ') or line.startswith('retornar '):
            value = line.split(' ', 1)[1]
            return current_indent + f'return {value};'
        
        # Definición de structs (clases en Rust)
        if line.startswith('clase '):
            struct_name = line.replace('clase ', '').replace(':', '').strip()
            self.in_impl = True
            self.indent_level += 1
            return current_indent + f'struct {struct_name} {{'
        
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
