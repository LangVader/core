# TypeScript Transpiler for Vader
# Converts Vader syntax to TypeScript code

class TypeScriptTranspiler:
    def __init__(self):
        self.indent_level = 0
    
    def transpile(self, vader_code):
        """Transpile Vader code to TypeScript"""
        lines = vader_code.split('\n')
        ts_lines = []
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('//'):
                continue
                
            ts_line = self.transpile_line(line)
            if ts_line:
                ts_lines.append(ts_line)
        
        return '\n'.join(ts_lines)
    
    def transpile_line(self, line):
        """Transpile a single line"""
        # Print statements
        if line.startswith('decir ') or line.startswith('mostrar '):
            content = line.split(' ', 1)[1]
            return self.indent() + f'console.log({content});'
        
        # Input statements (using prompt for browser)
        if 'preguntar ' in line and 'guardar la respuesta en' in line:
            parts = line.split('guardar la respuesta en')
            question = parts[0].replace('preguntar ', '').strip()
            var_name = parts[1].strip()
            return self.indent() + f'const {var_name}: string = prompt({question}) || "";'
        
        # Variable declarations
        if ' = ' in line and not line.startswith('if'):
            return self.indent() + 'const ' + line + ';'
        
        return self.indent() + line + ';'
    
    def indent(self):
        return '    ' * self.indent_level

def transpile_to_typescript(vader_code):
    transpiler = TypeScriptTranspiler()
    return transpiler.transpile(vader_code)
