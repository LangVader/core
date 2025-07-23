# HTML Transpiler for Vader
# Converts Vader syntax to HTML code

class HTMLTranspiler:
    def __init__(self):
        self.indent_level = 0
    
    def transpile(self, vader_code):
        """Transpile Vader code to HTML"""
        lines = vader_code.split('\n')
        html_lines = [
            '<!DOCTYPE html>',
            '<html lang="es">',
            '<head>',
            '    <meta charset="UTF-8">',
            '    <meta name="viewport" content="width=device-width, initial-scale=1.0">',
            '    <title>Vader App</title>',
            '</head>',
            '<body>'
        ]
        
        self.indent_level = 1
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('//'):
                continue
                
            html_line = self.transpile_line(line)
            if html_line:
                html_lines.append(html_line)
        
        html_lines.extend([
            '</body>',
            '</html>'
        ])
        
        return '\n'.join(html_lines)
    
    def transpile_line(self, line):
        """Transpile a single line"""
        # Page structure
        if line.startswith('pagina '):
            title = line.replace('pagina ', '').replace(':', '')
            return self.indent() + f'<h1>{title}</h1>'
        
        # Headers
        if line.startswith('titulo1 '):
            content = line.replace('titulo1 ', '')
            return self.indent() + f'<h1>{content}</h1>'
        
        if line.startswith('titulo2 '):
            content = line.replace('titulo2 ', '')
            return self.indent() + f'<h2>{content}</h2>'
        
        if line.startswith('titulo3 '):
            content = line.replace('titulo3 ', '')
            return self.indent() + f'<h3>{content}</h3>'
        
        # Paragraphs
        if line.startswith('parrafo '):
            content = line.replace('parrafo ', '')
            return self.indent() + f'<p>{content}</p>'
        
        # Links
        if line.startswith('enlace '):
            parts = line.replace('enlace ', '').split(' a ')
            if len(parts) == 2:
                text, url = parts
                return self.indent() + f'<a href="{url}">{text}</a>'
        
        # Buttons
        if line.startswith('boton '):
            content = line.replace('boton ', '')
            return self.indent() + f'<button>{content}</button>'
        
        # Images
        if line.startswith('imagen '):
            src = line.replace('imagen ', '')
            return self.indent() + f'<img src="{src}" alt="Imagen">'
        
        # Lists
        if line.startswith('lista:'):
            return self.indent() + '<ul>'
        
        if line.startswith('- '):
            content = line.replace('- ', '')
            return self.indent() + f'    <li>{content}</li>'
        
        # Forms
        if line.startswith('formulario:'):
            return self.indent() + '<form>'
        
        if line.startswith('campo '):
            name = line.replace('campo ', '')
            return self.indent() + f'    <input type="text" name="{name}" placeholder="{name}">'
        
        # Default: wrap in paragraph
        return self.indent() + f'<p>{line}</p>'
    
    def indent(self):
        return '    ' * self.indent_level

def transpile_to_html(vader_code):
    transpiler = HTMLTranspiler()
    return transpiler.transpile(vader_code)

def transpilar(vader_code):
    """Alias for CLI compatibility"""
    return transpile_to_html(vader_code)
