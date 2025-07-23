# Swift Transpiler for Vader
# Converts Vader syntax to Swift code

class SwiftTranspiler:
    def __init__(self):
        self.indent_level = 0
    
    def transpile(self, vader_code):
        """Transpile Vader code to Swift"""
        lines = vader_code.split('\n')
        swift_lines = ['import Foundation', '']
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('//'):
                continue
                
            swift_line = self.transpile_line(line)
            if swift_line:
                swift_lines.append(swift_line)
        
        return '\n'.join(swift_lines)
    
    def transpile_line(self, line):
        """Transpile a single line"""
        # Print statements
        if line.startswith('decir ') or line.startswith('mostrar '):
            content = line.split(' ', 1)[1]
            return self.indent() + f'print({content})'
        
        # Input statements
        if 'preguntar ' in line and 'guardar la respuesta en' in line:
            parts = line.split('guardar la respuesta en')
            question = parts[0].replace('preguntar ', '').strip()
            var_name = parts[1].strip()
            return self.indent() + f'print({question}, terminator: "")\nlet {var_name} = readLine() ?? ""'
        
        # Variable declarations
        if ' = ' in line and not line.startswith('if'):
            return self.indent() + 'let ' + line
        
        return self.indent() + line
    
    def indent(self):
        return '    ' * self.indent_level

def transpile_to_swift(vader_code):
    transpiler = SwiftTranspiler()
    return transpiler.transpile(vader_code)

def transpilar(vader_code):
    """Alias for CLI compatibility"""
    return transpile_to_swift(vader_code)
