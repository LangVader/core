# Kotlin Transpiler for Vader
# Converts Vader syntax to Kotlin code

class KotlinTranspiler:
    def __init__(self):
        self.indent_level = 0
    
    def transpile(self, vader_code):
        """Transpile Vader code to Kotlin"""
        lines = vader_code.split('\n')
        kotlin_lines = ['fun main() {']
        
        self.indent_level = 1
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('//'):
                continue
                
            kotlin_line = self.transpile_line(line)
            if kotlin_line:
                kotlin_lines.append(kotlin_line)
        
        kotlin_lines.append('}')
        return '\n'.join(kotlin_lines)
    
    def transpile_line(self, line):
        """Transpile a single line"""
        # Print statements
        if line.startswith('decir ') or line.startswith('mostrar '):
            content = line.split(' ', 1)[1]
            return self.indent() + f'println({content})'
        
        # Input statements
        if 'preguntar ' in line and 'guardar la respuesta en' in line:
            parts = line.split('guardar la respuesta en')
            question = parts[0].replace('preguntar ', '').strip()
            var_name = parts[1].strip()
            return self.indent() + f'print({question})\nval {var_name} = readLine() ?: ""'
        
        # Variable declarations
        if ' = ' in line and not line.startswith('if'):
            return self.indent() + 'val ' + line
        
        return self.indent() + line
    
    def indent(self):
        return '    ' * self.indent_level

def transpile_to_kotlin(vader_code):
    transpiler = KotlinTranspiler()
    return transpiler.transpile(vader_code)

def transpilar(vader_code):
    """Alias for CLI compatibility"""
    return transpile_to_kotlin(vader_code)
