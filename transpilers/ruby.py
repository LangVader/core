# Ruby Transpiler for Vader
# Converts Vader syntax to Ruby code

class RubyTranspiler:
    def __init__(self):
        self.indent_level = 0
    
    def transpile(self, vader_code):
        """Transpile Vader code to Ruby"""
        lines = vader_code.split('\n')
        ruby_lines = []
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('//'):
                continue
                
            ruby_line = self.transpile_line(line)
            if ruby_line:
                ruby_lines.append(ruby_line)
        
        return '\n'.join(ruby_lines)
    
    def transpile_line(self, line):
        """Transpile a single line"""
        # Print statements
        if line.startswith('decir ') or line.startswith('mostrar '):
            content = line.split(' ', 1)[1]
            return self.indent() + f'puts {content}'
        
        # Input statements
        if 'preguntar ' in line and 'guardar la respuesta en' in line:
            parts = line.split('guardar la respuesta en')
            question = parts[0].replace('preguntar ', '').strip()
            var_name = parts[1].strip()
            return self.indent() + f'print {question}\n{var_name} = gets.chomp'
        
        # Variable declarations
        if ' = ' in line and not line.startswith('if'):
            return self.indent() + line
        
        return self.indent() + line
    
    def indent(self):
        return '    ' * self.indent_level

def transpile_to_ruby(vader_code):
    transpiler = RubyTranspiler()
    return transpiler.transpile(vader_code)

def transpilar(vader_code):
    """Alias for CLI compatibility"""
    return transpile_to_ruby(vader_code)
