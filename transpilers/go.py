# Go Transpiler for Vader
# Converts Vader syntax to Go code

class GoTranspiler:
    def __init__(self):
        self.indent_level = 0
    
    def transpile(self, vader_code):
        """Transpile Vader code to Go"""
        lines = vader_code.split('\n')
        go_lines = [
            'package main',
            '',
            'import (',
            '    "fmt"',
            '    "bufio"',
            '    "os"',
            '    "strings"',
            ')',
            '',
            'func main() {'
        ]
        
        self.indent_level = 1
        go_lines.append(self.indent() + 'reader := bufio.NewReader(os.Stdin)')
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('//'):
                continue
                
            go_line = self.transpile_line(line)
            if go_line:
                go_lines.append(go_line)
        
        go_lines.append('}')
        return '\n'.join(go_lines)
    
    def transpile_line(self, line):
        """Transpile a single line"""
        # Print statements
        if line.startswith('decir ') or line.startswith('mostrar '):
            content = line.split(' ', 1)[1]
            return self.indent() + f'fmt.Println({content})'
        
        # Input statements
        if 'preguntar ' in line and 'guardar la respuesta en' in line:
            parts = line.split('guardar la respuesta en')
            question = parts[0].replace('preguntar ', '').strip()
            var_name = parts[1].strip()
            return self.indent() + f'fmt.Print({question})\n' + self.indent() + f'{var_name}, _ := reader.ReadString(\'\\n\')\n' + self.indent() + f'{var_name} = strings.TrimSpace({var_name})'
        
        # Variable declarations
        if ' = ' in line and not line.startswith('if'):
            return self.indent() + line
        
        return self.indent() + line
    
    def indent(self):
        return '    ' * self.indent_level

def transpile_to_go(vader_code):
    transpiler = GoTranspiler()
    return transpiler.transpile(vader_code)

def transpilar(vader_code):
    """Alias for CLI compatibility"""
    return transpile_to_go(vader_code)
