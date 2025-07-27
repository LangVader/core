#!/usr/bin/env python3
"""
Transpilador de Vader a C++
Convierte código Vader en español natural a C++ válido y funcional
"""

import re

class CppTranspiler:
    def __init__(self):
        self.indent_level = 0
        self.in_function = False
        self.in_class = False
        self.declared_vars = set()
        self.includes = set(['<iostream>', '<string>', '<vector>', '<map>'])
        
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
        cpp_lines.append('int main() {')
        
        self.indent_level = 1
        self.declared_vars = set()
        
        for line in lines:
            original_line = line
            line = line.strip()
            
            if not line:
                cpp_lines.append('')
                continue
                
            if line.startswith('#'):
                cpp_lines.append(self.indent() + '//' + line[1:])
                continue
                
            cpp_line = self.transpile_line(line)
            if cpp_line is not None:
                cpp_lines.append(cpp_line)
        
        cpp_lines.extend([
            '    return 0;',
            '}'
        ])
        
        return '\n'.join(cpp_lines)
    
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
        line = line.replace('nulo', 'nullptr')
        
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
        
        # Definición de funciones
        if line.startswith('funcion ') or line.startswith('función '):
            func_def = line.replace('funcion ', '').replace('función ', '')
            if ' con ' in func_def:
                name, params = func_def.split(' con ', 1)
                name = name.strip()
                params = params.replace(':', '').replace(' y ', ', ').strip()
                self.indent_level += 1
                self.in_function = True
                return current_indent + f'void {name}({params}) {{'
            else:
                name = func_def.replace(':', '').strip()
                self.indent_level += 1
                self.in_function = True
                return current_indent + f'void {name}() {{'
        
        # Return statements
        if line.startswith('devolver ') or line.startswith('retornar '):
            value = line.split(' ', 1)[1]
            return current_indent + f'return {value};'
        
        # Definición de clases
        if line.startswith('clase '):
            class_name = line.replace('clase ', '').replace(':', '').strip()
            self.in_class = True
            self.indent_level += 1
            return current_indent + f'class {class_name} {{'
        
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
