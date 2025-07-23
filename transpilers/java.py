# Java Transpiler for Vader
# Converts Vader syntax to Java code

class JavaTranspiler:
    def __init__(self):
        self.indent_level = 0
        self.class_name = "VaderProgram"
    
    def transpile(self, vader_code):
        """Transpile Vader code to Java"""
        lines = vader_code.split('\n')
        java_lines = [
            'import java.util.Scanner;',
            '',
            f'public class {self.class_name} {{',
            '    public static void main(String[] args) {',
            '        Scanner scanner = new Scanner(System.in);'
        ]
        
        self.indent_level = 2
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('//'):
                continue
                
            java_line = self.transpile_line(line)
            if java_line:
                java_lines.append(java_line)
        
        java_lines.extend([
            '        scanner.close();',
            '    }',
            '}'
        ])
        
        return '\n'.join(java_lines)
    
    def transpile_line(self, line):
        """Transpile a single line"""
        # Print statements
        if line.startswith('decir ') or line.startswith('mostrar '):
            content = line.split(' ', 1)[1]
            return self.indent() + f'System.out.println({content});'
        
        # Input statements
        if 'preguntar ' in line and 'guardar la respuesta en' in line:
            parts = line.split('guardar la respuesta en')
            question = parts[0].replace('preguntar ', '').strip()
            var_name = parts[1].strip()
            return self.indent() + f'System.out.print({question}); String {var_name} = scanner.nextLine();'
        
        # Variable declarations
        if ' = ' in line and not line.startswith('if'):
            return self.indent() + 'String ' + line + ';'
        
        return self.indent() + line + ';'
    
    def indent(self):
        return '    ' * self.indent_level

def transpile_to_java(vader_code):
    transpiler = JavaTranspiler()
    return transpiler.transpile(vader_code)

def transpilar(vader_code):
    """Alias for CLI compatibility"""
    return transpile_to_java(vader_code)
