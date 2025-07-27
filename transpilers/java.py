# Java Transpiler for Vader - VERSIÓN CORREGIDA
# Converts Vader syntax to Java code

import re

class JavaTranspiler:
    def __init__(self):
        self.indent_level = 0
        self.class_name = "VaderProgram"
        self.declared_vars = set()
    
    def transpile(self, vader_code):
        """Transpile Vader code to Java"""
        lines = vader_code.split('\n')
        java_lines = [
            'import java.util.Scanner;',
            'import java.util.ArrayList;',
            'import java.util.List;',
            '',
            f'public class {self.class_name} {{',
            '    public static void main(String[] args) {',
            '        Scanner scanner = new Scanner(System.in);'
        ]
        
        self.indent_level = 2
        self.declared_vars = set()
        
        for line in lines:
            original_line = line
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
                java_lines.append(java_line)
        
        java_lines.extend([
            '        scanner.close();',
            '    }',
            '}'
        ])
        
        return '\n'.join(java_lines)
    
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
        """Procesa una línea de código"""
        # Manejo de indentación para estructuras de control
        if line in ['fin si', 'fin', 'fin funcion', 'fin función', 'fin clase', 'fin mientras', 'fin repetir']:
            if self.indent_level > 2:
                self.indent_level -= 1
            return self.indent() + '}'
        
        current_indent = self.indent()
        
        # Variables booleanas
        line = line.replace('verdadero', 'true')
        line = line.replace('falso', 'false')
        line = line.replace('nulo', 'null')
        
        # Función texto() para conversión a string
        line = re.sub(r'texto\(([^)]+)\)', r'String.valueOf(\1)', line)
        
        # Print statements
        if line.startswith('mostrar ') or line.startswith('decir '):
            content = line.split(' ', 1)[1]
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
        
        # Definición de funciones (métodos estáticos)
        if line.startswith('funcion ') or line.startswith('función '):
            func_def = line.replace('funcion ', '').replace('función ', '')
            if ' con ' in func_def:
                name, params = func_def.split(' con ', 1)
                name = name.strip()
                params = params.replace(':', '').replace(' y ', ', ').strip()
                self.indent_level += 1
                return current_indent + f'public static void {name}({params}) {{'
            else:
                name = func_def.replace(':', '').strip()
                self.indent_level += 1
                return current_indent + f'public static void {name}() {{'
        
        # Return statements
        if line.startswith('devolver ') or line.startswith('retornar '):
            value = line.split(' ', 1)[1]
            return current_indent + f'return {value};'
        
        # Asignación de variables
        if ' = ' in line and not any(line.startswith(kw) for kw in ['if', 'while', 'for', 'public']):
            # Convertir operadores en la asignación
            line_converted = line
            line_converted = line_converted.replace(' mayor que ', ' > ')
            line_converted = line_converted.replace(' menor que ', ' < ')
            line_converted = line_converted.replace(' igual a ', ' == ')
            line_converted = line_converted.replace(' es mayor que ', ' > ')
            line_converted = line_converted.replace(' es menor que ', ' < ')
            line_converted = line_converted.replace(' es igual a ', ' == ')
            
            var_name = line_converted.split(' = ')[0].strip()
            
            # Detectar tipo de variable
            right_side = line_converted.split(' = ', 1)[1]
            
            if var_name not in self.declared_vars:
                self.declared_vars.add(var_name)
                # Inferir tipo
                if right_side.strip().isdigit() or (right_side.strip().startswith('-') and right_side.strip()[1:].isdigit()):
                    var_type = 'int'
                elif 'true' in right_side or 'false' in right_side:
                    var_type = 'boolean'
                elif right_side.strip().replace('.', '').isdigit():
                    var_type = 'double'
                else:
                    var_type = 'String'
                
                return current_indent + f'{var_type} {line_converted};'
            else:
                return current_indent + line_converted + ';'
        
        # Llamadas a funciones o expresiones
        if not line.endswith(';'):
            return current_indent + line + ';'
        else:
            return current_indent + line
    
    def indent(self):
        return '    ' * self.indent_level

def transpile_to_java(vader_code):
    transpiler = JavaTranspiler()
    return transpiler.transpile(vader_code)

def transpilar(vader_code):
    """Alias for CLI compatibility"""
    return transpile_to_java(vader_code)
