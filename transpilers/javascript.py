# JavaScript Transpiler for Vader - VERSIÓN CORREGIDA
# Converts Vader syntax to JavaScript code

import re

class JavaScriptTranspiler:
    def __init__(self):
        self.indent_level = 0
        self.in_class = False
        self.in_function = False
    
    def transpile(self, vader_code):
        """Transpile Vader code to JavaScript"""
        lines = vader_code.split('\n')
        js_lines = []
        
        for line in lines:
            original_line = line
            line = line.strip()
            
            # Preservar líneas vacías y comentarios
            if not line:
                js_lines.append('')
                continue
            if line.startswith('#'):
                js_lines.append('//' + line[1:])  # Convertir # a //
                continue
                
            js_line = self.transpile_line(line)
            if js_line is not None:
                js_lines.append(js_line)
        
        return '\n'.join(js_lines)
    
    def transpile_line(self, line):
        """Transpile a single line"""
        # Remover comentarios inline
        if '#' in line:
            code_part = line.split('#')[0].strip()
            comment_part = '//' + '#'.join(line.split('#')[1:])
            if code_part:
                return self.process_code_line(code_part) + '  ' + comment_part
            else:
                return '//' + line[1:]  # Solo comentario
        
        return self.process_code_line(line)
    
    def process_code_line(self, line):
        """Procesa una línea de código"""
        # Manejo de indentación para estructuras de control
        if line in ['fin si', 'fin', 'fin funcion', 'fin función', 'fin clase', 'fin mientras', 'fin repetir']:
            if self.indent_level > 0:
                self.indent_level -= 1
            return self.indent() + '}'
        
        current_indent = self.indent()
        
        # Variables booleanas
        line = line.replace('verdadero', 'true')
        line = line.replace('falso', 'false')
        line = line.replace('nulo', 'null')
        
        # Función texto() para conversión a string
        line = re.sub(r'texto\(([^)]+)\)', r'String(\1)', line)
        
        # Print statements
        if line.startswith('mostrar ') or line.startswith('decir '):
            content = line.split(' ', 1)[1]
            return current_indent + f'console.log({content});'
        
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
                return current_indent + line + ';'  # No reconocido
            return current_indent + f'let {var_name} = prompt({question});'
        
        # Condicionales
        if line.startswith('si ') and ('entonces' in line or line.endswith(':')):
            condition = line.replace('si ', '').replace(' entonces', '').replace(':', '').strip()
            # Convertir operadores
            condition = condition.replace(' es igual a ', ' === ')
            condition = condition.replace(' es mayor que ', ' > ')
            condition = condition.replace(' es menor que ', ' < ')
            condition = condition.replace(' mayor que ', ' > ')
            condition = condition.replace(' menor que ', ' < ')
            condition = condition.replace(' igual a ', ' === ')
            
            self.indent_level += 1
            return current_indent + f'if ({condition}) {{'
        
        # Else
        if line == 'sino' or line == 'si no':
            # Reducir indentación temporalmente para el else
            if self.indent_level > 0:
                self.indent_level -= 1
            else_indent = self.indent()
            self.indent_level += 1  # Restaurar para el contenido del else
            return else_indent + '} else {'
        
        # Bucles for
        if line.startswith('repetir ') and ' veces' in line:
            times = line.replace('repetir ', '').replace(' veces', '').strip()
            self.indent_level += 1
            return current_indent + f'for (let i = 0; i < {times}; i++) {{'
        
        if 'repetir con cada' in line or 'para cada' in line:
            # Formato: "repetir con cada X en Y" o "para cada X en Y"
            line_clean = line.replace('repetir con cada ', '').replace('para cada ', '')
            if ' en ' in line_clean:
                parts = line_clean.split(' en ')
                var_name = parts[0].strip()
                iterable = parts[1].strip()
                self.indent_level += 1
                return current_indent + f'for (let {var_name} of {iterable}) {{'
        
        # Bucles while
        if line.startswith('mientras '):
            condition = line.replace('mientras ', '').replace(':', '').strip()
            # Convertir operadores de comparación
            condition = condition.replace(' es igual a ', ' === ')
            condition = condition.replace(' es mayor que ', ' > ')
            condition = condition.replace(' es menor que ', ' < ')
            condition = condition.replace(' mayor que ', ' > ')
            condition = condition.replace(' menor que ', ' < ')
            condition = condition.replace(' igual a ', ' === ')
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
                return current_indent + f'function {name}({params}) {{'
            else:
                name = func_def.replace(':', '').strip()
                self.indent_level += 1
                self.in_function = True
                return current_indent + f'function {name}() {{'
        
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
        
        # Asignación de variables
        if ' = ' in line and not any(line.startswith(kw) for kw in ['if', 'while', 'for', 'function', 'class']):
            # Convertir operadores en la asignación también
            line_converted = line
            line_converted = line_converted.replace(' mayor que ', ' > ')
            line_converted = line_converted.replace(' menor que ', ' < ')
            line_converted = line_converted.replace(' igual a ', ' === ')
            line_converted = line_converted.replace(' es mayor que ', ' > ')
            line_converted = line_converted.replace(' es menor que ', ' < ')
            line_converted = line_converted.replace(' es igual a ', ' === ')
            
            # Detectar si es primera declaración o reasignación
            var_name = line_converted.split(' = ')[0].strip()
            
            # Si la variable ya existe en el lado derecho, es una reasignación
            right_side = line_converted.split(' = ', 1)[1]
            if var_name in right_side:
                # Es una reasignación, no usar 'let'
                return current_indent + line_converted + ';'
            else:
                # Es una nueva declaración
                return current_indent + 'let ' + line_converted + ';'
        
        # Llamadas a funciones o expresiones
        if not line.endswith(';'):
            return current_indent + line + ';'
        else:
            return current_indent + line
    
    def indent(self):
        """Return current indentation"""
        return '    ' * self.indent_level

def transpile_to_javascript(vader_code):
    """Main function to transpile Vader to JavaScript"""
    transpiler = JavaScriptTranspiler()
    return transpiler.transpile(vader_code)

def transpilar(vader_code):
    """Alias for CLI compatibility"""
    return transpile_to_javascript(vader_code)
