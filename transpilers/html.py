# Transpilador de HTML simplificado para Vader
# Convierte sintaxis natural en español a HTML5 básico

def transpilar_html(code):
    """Función principal para transpilar Vader a HTML"""
    transpiler = HTMLTranspiler()
    return transpiler.transpile_to_html(code)

class HTMLTranspiler:
    """Transpilador que convierte sintaxis Vader a HTML5"""
    
    def __init__(self):
        self.page_title = "Página Vader"
        
    def transpile_to_html(self, code):
        """Transpila código Vader a HTML5"""
        lines = code.split('\n')
        result = []
        
        # Estructura HTML básica
        result.extend([
            '<!DOCTYPE html>',
            '<html lang="es">',
            '<head>',
            '    <meta charset="UTF-8">',
            '    <meta name="viewport" content="width=device-width, initial-scale=1.0">',
            f'    <title>{self.page_title}</title>',
            '</head>',
            '<body>'
        ])
        
        # Procesar contenido
        for line in lines:
            line = line.strip()
            
            if line.startswith('pagina'):
                # Extraer título si existe
                if '"' in line:
                    parts = line.split('"')
                    if len(parts) > 1:
                        self.page_title = parts[1]
                        result[5] = f'    <title>{self.page_title}</title>'
                        
            elif line.startswith('titulo1'):
                text = self._extract_text(line, 'titulo1')
                result.append(f'    <h1>{text}</h1>')
                
            elif line.startswith('titulo2'):
                text = self._extract_text(line, 'titulo2')
                result.append(f'    <h2>{text}</h2>')
                
            elif line.startswith('titulo3'):
                text = self._extract_text(line, 'titulo3')
                result.append(f'    <h3>{text}</h3>')
                
            elif line.startswith('parrafo'):
                text = self._extract_text(line, 'parrafo')
                result.append(f'    <p>{text}</p>')
                
            elif line.startswith('enlace'):
                text, href = self._extract_link(line)
                result.append(f'    <a href="{href}">{text}</a>')
                
            elif line.startswith('boton'):
                text = self._extract_text(line, 'boton')
                result.append(f'    <button>{text}</button>')
                
            elif line.startswith('imagen'):
                src, alt = self._extract_image(line)
                result.append(f'    <img src="{src}" alt="{alt}">')
                
            elif line.startswith('encabezado'):
                result.append('    <header>')
                
            elif line.startswith('fin encabezado'):
                result.append('    </header>')
                
            elif line.startswith('navegacion'):
                result.append('    <nav>')
                
            elif line.startswith('fin navegacion'):
                result.append('    </nav>')
                
            elif line.startswith('contenido'):
                result.append('    <main>')
                
            elif line.startswith('fin contenido'):
                result.append('    </main>')
                
            elif line.startswith('seccion'):
                class_attr = self._extract_class(line, 'seccion')
                result.append(f'    <section{class_attr}>')
                
            elif line.startswith('fin seccion'):
                result.append('    </section>')
                
            elif line.startswith('pie_pagina'):
                result.append('    <footer>')
                
            elif line.startswith('fin pie_pagina'):
                result.append('    </footer>')
                
            elif line.startswith('lista'):
                class_attr = self._extract_class(line, 'lista')
                result.append(f'    <ul{class_attr}>')
                
            elif line.startswith('fin lista'):
                result.append('    </ul>')
                
            elif line.startswith('elemento'):
                text = self._extract_text(line, 'elemento')
                if text:
                    result.append(f'        <li>{text}</li>')
                else:
                    result.append('        <li>')
                    
            elif line.startswith('fin elemento'):
                result.append('        </li>')
                
            elif line.startswith('formulario'):
                class_attr = self._extract_class(line, 'formulario')
                result.append(f'    <form{class_attr}>')
                
            elif line.startswith('fin formulario'):
                result.append('    </form>')
                
            elif line.startswith('campo'):
                field_html = self._extract_field(line)
                result.append(f'        {field_html}')
                
            elif line.startswith('tarjeta'):
                class_attr = self._extract_class(line, 'tarjeta')
                if class_attr:
                    clean_class = class_attr.replace(' class="', ' ').replace('"', '')
                    result.append(f'    <div class="card{clean_class}">')
                else:
                    result.append('    <div class="card">')
                
            elif line.startswith('fin tarjeta'):
                result.append('    </div>')
        
        # Cerrar HTML
        result.extend([
            '</body>',
            '</html>'
        ])
        
        return '\n'.join(result)
    
    def _extract_text(self, line, keyword):
        """Extrae texto de una línea"""
        text = line.replace(keyword, '').strip()
        if text.startswith('"') and text.endswith('"'):
            text = text[1:-1]
        return text
    
    def _extract_class(self, line, keyword):
        """Extrae clase de una línea"""
        if '"' in line:
            parts = line.split('"')
            if len(parts) > 1:
                return f' class="{parts[1]}"'
        return ''
    
    def _extract_link(self, line):
        """Extrae texto y href de un enlace"""
        parts = line.replace('enlace', '').strip().split('"')
        if len(parts) >= 3:
            text = parts[1]
            href = parts[3] if len(parts) > 3 else '#'
            return text, href
        return 'Enlace', '#'
    
    def _extract_image(self, line):
        """Extrae src y alt de una imagen"""
        parts = line.replace('imagen', '').strip().split('"')
        if len(parts) >= 3:
            src = parts[1]
            alt = parts[3] if len(parts) > 3 else ''
            return src, alt
        return '', 'Imagen'
    
    def _extract_field(self, line):
        """Extrae campo de formulario"""
        parts = line.replace('campo', '').strip().split('"')
        if len(parts) >= 5:
            name = parts[1]
            field_type = parts[3]
            placeholder = parts[5] if len(parts) > 5 else ''
            
            if field_type == 'textarea':
                return f'<textarea name="{name}" placeholder="{placeholder}"></textarea>'
            else:
                return f'<input type="{field_type}" name="{name}" placeholder="{placeholder}">'
        
        return '<input type="text">'
