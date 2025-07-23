# Rust Transpiler for Vader
# Converts Vader syntax to Rust code

class RustTranspiler:
    def __init__(self):
        self.indent_level = 0
    
    def transpile(self, vader_code):
        """Transpile Vader code to Rust"""
        lines = vader_code.split('\n')
        rust_lines = [
            'use std::io;',
            '',
            'fn main() {'
        ]
        
        self.indent_level = 1
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('//'):
                continue
                
            rust_line = self.transpile_line(line)
            if rust_line:
                rust_lines.append(rust_line)
        
        rust_lines.append('}')
        return '\n'.join(rust_lines)
    
    def transpile_line(self, line):
        """Transpile a single line"""
        # Print statements
        if line.startswith('decir ') or line.startswith('mostrar '):
            content = line.split(' ', 1)[1]
            return self.indent() + f'println!("{content}");'
        
        # Input statements
        if 'preguntar ' in line and 'guardar la respuesta en' in line:
            parts = line.split('guardar la respuesta en')
            question = parts[0].replace('preguntar ', '').strip()
            var_name = parts[1].strip()
            return self.indent() + f'println!("{question}");\n' + self.indent() + f'let mut {var_name} = String::new();\n' + self.indent() + f'io::stdin().read_line(&mut {var_name}).expect("Failed to read line");'
        
        # Variable declarations
        if ' = ' in line and not line.startswith('if'):
            return self.indent() + 'let ' + line + ';'
        
        return self.indent() + line + ';'
    
    def indent(self):
        return '    ' * self.indent_level

def transpile_to_rust(vader_code):
    transpiler = RustTranspiler()
    return transpiler.transpile(vader_code)

def transpilar(vader_code):
    """Alias for CLI compatibility"""
    return transpile_to_rust(vader_code)
