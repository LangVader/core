# CSS Transpiler for Vader
# Converts Vader syntax to CSS code

class CSSTranspiler:
    def __init__(self):
        self.indent_level = 0
    
    def transpile(self, vader_code):
        """Transpile Vader code to CSS"""
        lines = vader_code.split('\n')
        css_lines = []
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('//'):
                continue
                
            css_line = self.transpile_line(line)
            if css_line:
                css_lines.append(css_line)
        
        return '\n'.join(css_lines)
    
    def transpile_line(self, line):
        """Transpile a single line"""
        # Selectors
        if line.endswith(':') and not any(prop in line for prop in ['color', 'fondo', 'tamaño']):
            selector = line.replace(':', '').strip()
            return f'{selector} {{'
        
        # Colors
        color_map = {
            'rojo': 'red',
            'azul': 'blue',
            'verde': 'green',
            'amarillo': 'yellow',
            'negro': 'black',
            'blanco': 'white',
            'gris': 'gray',
            'rosa': 'pink',
            'morado': 'purple',
            'naranja': 'orange'
        }
        
        # Properties
        if 'color:' in line:
            color = line.split('color:')[1].strip()
            css_color = color_map.get(color, color)
            return f'    color: {css_color};'
        
        if 'fondo_color:' in line:
            color = line.split('fondo_color:')[1].strip()
            css_color = color_map.get(color, color)
            return f'    background-color: {css_color};'
        
        if 'tamaño_fuente:' in line:
            size = line.split('tamaño_fuente:')[1].strip()
            return f'    font-size: {size};'
        
        if 'margen:' in line:
            margin = line.split('margen:')[1].strip()
            return f'    margin: {margin};'
        
        if 'relleno:' in line:
            padding = line.split('relleno:')[1].strip()
            return f'    padding: {padding};'
        
        if 'ancho:' in line:
            width = line.split('ancho:')[1].strip()
            return f'    width: {width};'
        
        if 'alto:' in line:
            height = line.split('alto:')[1].strip()
            return f'    height: {height};'
        
        # End of rule
        if line == 'fin' or line == '}':
            return '}'
        
        # Default: return as is
        return line
    
    def indent(self):
        return '    ' * self.indent_level

def transpile_to_css(vader_code):
    transpiler = CSSTranspiler()
    return transpiler.transpile(vader_code)

def transpilar(vader_code):
    """Alias for CLI compatibility"""
    return transpile_to_css(vader_code)
