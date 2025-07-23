# C# Transpiler for Vader
# Converts Vader syntax to C# code

class CSharpTranspiler:
    def __init__(self):
        self.indent_level = 0
        self.class_name = "VaderProgram"
    
    def transpile(self, vader_code):
        """Transpile Vader code to C#"""
        lines = vader_code.split('\n')
        csharp_lines = [
            'using System;',
            '',
            f'public class {self.class_name}',
            '{',
            '    public static void Main(string[] args)',
            '    {'
        ]
        
        self.indent_level = 2
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('//'):
                continue
                
            csharp_line = self.transpile_line(line)
            if csharp_line:
                csharp_lines.append(csharp_line)
        
        csharp_lines.extend([
            '    }',
            '}'
        ])
        
        return '\n'.join(csharp_lines)
    
    def transpile_line(self, line):
        """Transpile a single line"""
        # Print statements
        if line.startswith('decir ') or line.startswith('mostrar '):
            content = line.split(' ', 1)[1]
            return self.indent() + f'Console.WriteLine({content});'
        
        # Input statements
        if 'preguntar ' in line and 'guardar la respuesta en' in line:
            parts = line.split('guardar la respuesta en')
            question = parts[0].replace('preguntar ', '').strip()
            var_name = parts[1].strip()
            return self.indent() + f'Console.Write({question}); string {var_name} = Console.ReadLine();'
        
        # Variable declarations
        if ' = ' in line and not line.startswith('if'):
            return self.indent() + 'string ' + line + ';'
        
        return self.indent() + line + ';'
    
    def indent(self):
        return '    ' * self.indent_level

def transpile_to_csharp(vader_code):
    transpiler = CSharpTranspiler()
    return transpiler.transpile(vader_code)

def transpilar(vader_code):
    """Alias for CLI compatibility"""
    return transpile_to_csharp(vader_code)
