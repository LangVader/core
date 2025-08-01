# Python Transpiler for Vader - VERSIÓN CORREGIDA
# Converts Vader syntax to Python code

import re

class PythonTranspiler:
    def __init__(self):
        self.indent_level = 0
        self.in_class = False
        self.in_function = False
    
    def transpile(self, vader_code):
        """Transpile Vader code to Python"""
        lines = vader_code.split('\n')
        python_lines = []
        
        for line in lines:
            original_line = line
            line = line.strip()
            
            # Preservar líneas vacías y comentarios
            if not line:
                python_lines.append('')
                continue
            if line.startswith('#'):
                python_lines.append(original_line)
                continue
                
            python_line = self.transpile_line(line)
            if python_line is not None:
                python_lines.append(python_line)
        
        return '\n'.join(python_lines)
    
    def transpile_line(self, line):
        """Transpile a single line"""
        # Remover comentarios inline
        if '#' in line:
            code_part = line.split('#')[0].strip()
            comment_part = '#' + '#'.join(line.split('#')[1:])
            if code_part:
                return self.process_code_line(code_part) + '  ' + comment_part
            else:
                return line  # Solo comentario
        
        return self.process_code_line(line)
    
    def process_code_line(self, line):
        """Procesa una línea de código"""
        # Manejo de indentación para estructuras de control
        if line in ['fin si', 'fin', 'fin funcion', 'fin función', 'fin clase', 'fin mientras', 'fin repetir']:
            if self.indent_level > 0:
                self.indent_level -= 1
            return None  # No generar línea para 'fin'
        
        current_indent = self.indent()
        
        # Variables booleanas
        line = line.replace('verdadero', 'True')
        line = line.replace('falso', 'False')
        line = line.replace('nulo', 'None')
        
        # Función texto() para conversión a string
        line = re.sub(r'texto\(([^)]+)\)', r'str(\1)', line)
        
        # Print statements
        if line.startswith('mostrar ') or line.startswith('decir '):
            content = line.split(' ', 1)[1]
            # Asegurar que las strings estén bien formateadas
            if not (content.startswith('"') or content.startswith("'")):
                # Si no es una string literal, podría ser una variable o expresión
                pass
            return current_indent + f'print({content})'
        
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
                return current_indent + line  # No reconocido
            return current_indent + f'{var_name} = input({question})'
        
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
            condition = condition.replace('>=', '>=')
            condition = condition.replace('<=', '<=')
            
            self.indent_level += 1
            return current_indent + f'if {condition}:'
        
        # Else
        if line == 'sino' or line == 'si no':
            # Reducir indentación temporalmente para el else
            if self.indent_level > 0:
                self.indent_level -= 1
            else_indent = self.indent()
            self.indent_level += 1  # Restaurar para el contenido del else
            return else_indent + 'else:'
        
        # Bucles for
        if line.startswith('repetir ') and ' veces' in line:
            times = line.replace('repetir ', '').replace(' veces', '').strip()
            self.indent_level += 1
            return current_indent + f'for _ in range({times}):'
        
        if 'repetir con cada' in line or 'para cada' in line:
            # Formato: "repetir con cada X en Y" o "para cada X en Y"
            line_clean = line.replace('repetir con cada ', '').replace('para cada ', '')
            if ' en ' in line_clean:
                parts = line_clean.split(' en ')
                var_name = parts[0].strip()
                iterable = parts[1].strip()
                self.indent_level += 1
                return current_indent + f'for {var_name} in {iterable}:'
        
        # Bucles while
        if line.startswith('mientras '):
            condition = line.replace('mientras ', '').replace(':', '').strip()
            condition = condition.replace(' es igual a ', ' == ')
            condition = condition.replace(' es mayor que ', ' > ')
            condition = condition.replace(' es menor que ', ' < ')
            condition = condition.replace(' mayor que ', ' > ')
            condition = condition.replace(' menor que ', ' < ')
            condition = condition.replace(' igual a ', ' == ')
            condition = condition.replace('>=', '>=')
            condition = condition.replace('<=', '<=')
            self.indent_level += 1
            return current_indent + f'while {condition}:'
        
        # Definición de funciones
        if line.startswith('funcion ') or line.startswith('función '):
            func_def = line.replace('funcion ', '').replace('función ', '')
            if ' con ' in func_def:
                name, params = func_def.split(' con ', 1)
                name = name.strip()
                params = params.replace(':', '').replace(' y ', ', ').strip()
                self.indent_level += 1
                self.in_function = True
                return current_indent + f'def {name}({params}):'
            else:
                name = func_def.replace(':', '').strip()
                self.indent_level += 1
                self.in_function = True
                return current_indent + f'def {name}():'
        
        # Return statements
        if line.startswith('devolver ') or line.startswith('retornar '):
            value = line.split(' ', 1)[1]
            return current_indent + f'return {value}'
        
        # Definición de clases
        if line.startswith('clase '):
            class_name = line.replace('clase ', '').replace(':', '').strip()
            self.in_class = True
            self.indent_level += 1
            return current_indent + f'class {class_name}:'
        
        # Llamadas a funciones con 'con'
        if ' con ' in line and not line.startswith('funcion ') and not line.startswith('función '):
            # Formato: "nombre_funcion con parametro1, parametro2"
            parts = line.split(' con ', 1)
            func_name = parts[0].strip()
            params = parts[1].strip()
            # Si los parámetros están entre comillas, mantenerlos
            return current_indent + f'{func_name}({params})'
        
        # Asignación de variables
        if ' = ' in line and not any(line.startswith(kw) for kw in ['if', 'while', 'for', 'def', 'class']):
            return current_indent + line
        
        # Llamadas a funciones o expresiones
        return current_indent + line
    
    def indent(self):
        """Return current indentation"""
        return '    ' * self.indent_level

def transpile_to_python(vader_code):
    """Main function to transpile Vader to Python"""
    transpiler = PythonTranspiler()
    return transpiler.transpile(vader_code)

def transpilar(vader_code):
    """Alias for CLI compatibility"""
    return transpile_to_python(vader_code)

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) != 2:
        print("Uso: python3 transpilers/python.py archivo.vdr")
        sys.exit(1)
    
    vader_file = sys.argv[1]
    
    try:
        with open(vader_file, 'r', encoding='utf-8') as f:
            vader_code = f.read()
        
        python_code = transpile_to_python(vader_code)
        
        # Ejecutar el código Python transpilado
        exec(python_code)
        
    except FileNotFoundError:
        print(f"Error: No se pudo encontrar el archivo '{vader_file}'")
        sys.exit(1)
    except Exception as e:
        print(f"Error al transpilar/ejecutar: {e}")
        sys.exit(1)
