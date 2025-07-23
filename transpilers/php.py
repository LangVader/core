# PHP Transpiler for Vader
# Converts Vader syntax to PHP code

class PHPTranspiler:
    def __init__(self):
        self.indent_level = 0
    
    def transpile(self, vader_code):
        """Transpile Vader code to PHP"""
        lines = vader_code.split('\n')
        php_lines = ['<?php']
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('//'):
                continue
                
            php_line = self.transpile_line(line)
            if php_line:
                php_lines.append(php_line)
        
        php_lines.append('?>')
        return '\n'.join(php_lines)
    
    def transpile_line(self, line):
        """Transpile a single line"""
        # Print statements
        if line.startswith('decir ') or line.startswith('mostrar '):
            content = line.split(' ', 1)[1]
            return self.indent() + f'echo {content};'
        
        # Input statements
        if 'preguntar ' in line and 'guardar la respuesta en' in line:
            parts = line.split('guardar la respuesta en')
            question = parts[0].replace('preguntar ', '').strip()
            var_name = parts[1].strip()
            return self.indent() + f'echo {question};\n${var_name} = trim(fgets(STDIN));'
        
        # Variable declarations
        if ' = ' in line and not line.startswith('if'):
            var_name, value = line.split(' = ', 1)
            return self.indent() + f'${var_name} = {value};'
        
        return self.indent() + line + ';'
    
    def indent(self):
        return '    ' * self.indent_level

def transpile_to_php(vader_code):
    transpiler = PHPTranspiler()
    return transpiler.transpile(vader_code)

def transpilar(vader_code):
    """Alias for CLI compatibility"""
    return transpile_to_php(vader_code)
