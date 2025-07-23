# JavaScript Transpiler for Vader
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
            line = line.strip()
            if not line or line.startswith('//'):
                continue
                
            js_line = self.transpile_line(line)
            if js_line:
                js_lines.append(js_line)
        
        return '\n'.join(js_lines)
    
    def transpile_line(self, line):
        """Transpile a single line"""
        # Remove comments
        if '//' in line:
            line = line.split('//')[0].strip()
        
        # Variable declarations
        if ' = ' in line and not line.startswith('if') and not line.startswith('while'):
            return self.indent() + 'let ' + line + ';'
        
        # Print statements
        if line.startswith('decir ') or line.startswith('mostrar '):
            content = line.split(' ', 1)[1]
            return self.indent() + f'console.log({content});'
        
        # Input statements (using prompt for browser)
        if 'preguntar ' in line and 'guardar la respuesta en' in line:
            parts = line.split('guardar la respuesta en')
            question = parts[0].replace('preguntar ', '').strip()
            var_name = parts[1].strip()
            return self.indent() + f'let {var_name} = prompt({question});'
        
        # Function definitions
        if line.startswith('funcion ') or line.startswith('función '):
            func_def = line.replace('funcion ', '').replace('función ', '')
            if ' con ' in func_def:
                name, params = func_def.split(' con ', 1)
                params = params.replace(':', '').replace(' y ', ', ')
                return self.indent() + f'function {name}({params}) {{'
            else:
                name = func_def.replace(':', '')
                return self.indent() + f'function {name}() {{'
        
        # Function calls
        if ' con ' in line and not line.startswith('funcion') and not line.startswith('función'):
            parts = line.split(' con ')
            func_name = parts[0]
            args = parts[1].replace(' y ', ', ')
            return self.indent() + f'{func_name}({args});'
        
        # Class definitions
        if line.startswith('clase '):
            class_name = line.replace('clase ', '').replace(':', '')
            self.in_class = True
            return self.indent() + f'class {class_name} {{'
        
        # If statements
        if line.startswith('si '):
            condition = line.replace('si ', '').replace(':', '')
            condition = condition.replace(' es igual a ', ' === ')
            condition = condition.replace(' es mayor que ', ' > ')
            condition = condition.replace(' es menor que ', ' < ')
            return self.indent() + f'if ({condition}) {{'
        
        # Else statements
        if line == 'sino:' or line == 'si no:':
            return self.indent() + '} else {'
        
        # While loops
        if line.startswith('mientras '):
            condition = line.replace('mientras ', '').replace(':', '')
            condition = condition.replace(' es igual a ', ' === ')
            condition = condition.replace(' es mayor que ', ' > ')
            condition = condition.replace(' es menor que ', ' < ')
            return self.indent() + f'while ({condition}) {{'
        
        # For loops
        if line.startswith('repetir ') and ' veces' in line:
            times = line.replace('repetir ', '').replace(' veces:', '').replace(' veces', '')
            return self.indent() + f'for (let i = 0; i < {times}; i++) {{'
        
        if 'repetir con cada ' in line and ' en ' in line:
            parts = line.replace('repetir con cada ', '').replace(':', '').split(' en ')
            var_name = parts[0]
            iterable = parts[1]
            return self.indent() + f'for (let {var_name} of {iterable}) {{'
        
        # End statements
        if line in ['fin', 'fin si', 'fin funcion', 'fin función', 'fin clase', 'fin mientras', 'fin repetir']:
            return self.indent() + '}'
        
        # Return statements
        if line.startswith('devolver ') or line.startswith('retornar '):
            value = line.split(' ', 1)[1]
            return self.indent() + f'return {value};'
        
        # Default: return as is with semicolon
        return self.indent() + line + ';'
    
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
