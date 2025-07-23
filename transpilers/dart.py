# Dart Transpiler for Vader
# Converts Vader syntax to Dart code

class DartTranspiler:
    def __init__(self):
        self.indent_level = 0
    
    def transpile(self, vader_code):
        """Transpile Vader code to Dart"""
        lines = vader_code.split('\n')
        dart_lines = [
            'import "dart:io";',
            '',
            'void main() {'
        ]
        
        self.indent_level = 1
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('//'):
                continue
                
            dart_line = self.transpile_line(line)
            if dart_line:
                dart_lines.append(dart_line)
        
        dart_lines.append('}')
        return '\n'.join(dart_lines)
    
    def transpile_line(self, line):
        """Transpile a single line"""
        # Print statements
        if line.startswith('decir ') or line.startswith('mostrar '):
            content = line.split(' ', 1)[1]
            return self.indent() + f'print({content});'
        
        # Input statements
        if 'preguntar ' in line and 'guardar la respuesta en' in line:
            parts = line.split('guardar la respuesta en')
            question = parts[0].replace('preguntar ', '').strip()
            var_name = parts[1].strip()
            return self.indent() + f'stdout.write({question});\nString {var_name} = stdin.readLineSync() ?? "";'
        
        # Variable declarations
        if ' = ' in line and not line.startswith('if'):
            return self.indent() + 'var ' + line + ';'
        
        return self.indent() + line + ';'
    
    def indent(self):
        return '    ' * self.indent_level

def transpile_to_dart(vader_code):
    transpiler = DartTranspiler()
    return transpiler.transpile(vader_code)

def transpilar(vader_code):
    """Alias for CLI compatibility"""
    return transpile_to_dart(vader_code)
