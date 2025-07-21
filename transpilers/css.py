# Transpilador de CSS para Vader
# Convierte sintaxis natural en español a CSS3 moderno

import re

def transpilar_css(code):
    """Función principal para transpilar Vader a CSS"""
    transpiler = CSSTranspiler()
    return transpiler.transpile_to_css(code)

class CSSTranspiler:
    """Transpilador que convierte sintaxis Vader a CSS3"""
    
    def __init__(self):
        self.color_map = {
            'rojo': '#e74c3c',
            'azul': '#3498db',
            'verde': '#2ecc71',
            'amarillo': '#f1c40f',
            'morado': '#9b59b6',
            'naranja': '#e67e22',
            'rosa': '#e91e63',
            'gris': '#95a5a6',
            'negro': '#2c3e50',
            'blanco': '#ffffff',
            'transparente': 'transparent'
        }
        
    def transpile_to_css(self, code):
        """Transpila código Vader a CSS3"""
        lines = code.split('\n')
        result = []
        
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            if line.startswith('estilos'):
                css_lines, i = self._process_styles(lines, i)
                result.extend(css_lines)
            else:
                i += 1
                
        return '\n'.join(result)
    
    def _process_styles(self, lines, start_index):
        """Procesa el bloque de estilos"""
        result = ['/* Estilos generados por Vader */']
        
        i = start_index + 1
        while i < len(lines) and not lines[i].strip().startswith('fin estilos'):
            line = lines[i].strip()
            
            if self._is_selector(line):
                selector_lines, i = self._process_selector(lines, i)
                result.extend(selector_lines)
                continue
                
            elif line.startswith('responsive'):
                responsive_lines, i = self._process_responsive(lines, i)
                result.extend(responsive_lines)
                continue
                
            elif line.startswith('animacion'):
                animation_lines, i = self._process_animation(lines, i)
                result.extend(animation_lines)
                continue
                
            i += 1
        
        return result, i + 1
    
    def _is_selector(self, line):
        """Determina si una línea es un selector CSS"""
        selectors = [
            'cuerpo', 'body', 'encabezado', 'header', 'navegacion', 'nav',
            'contenido', 'main', 'seccion', 'section', 'pie_pagina', 'footer',
            'titulo1', 'h1', 'titulo2', 'h2', 'titulo3', 'h3',
            'parrafo', 'p', 'enlace', 'a', 'boton', 'button',
            'imagen', 'img', 'lista', 'ul', 'ol', 'elemento', 'li',
            'formulario', 'form', 'campo', 'input', 'tarjeta', 'card'
        ]
        
        # Verificar si es un selector básico
        for selector in selectors:
            if line.startswith(selector) and not '=' in line:
                return True
        
        # Verificar si es una clase o ID
        if line.startswith('.') or line.startswith('#'):
            return True
            
        return False
    
    def _process_selector(self, lines, start_index):
        """Procesa un selector CSS"""
        line = lines[start_index].strip()
        
        # Convertir selector de español a CSS
        css_selector = self._convert_selector(line)
        
        result = [f'{css_selector} {{']
        
        i = start_index + 1
        while i < len(lines) and not self._is_end_of_selector(lines[i]):
            line = lines[i].strip()
            
            if line and not self._is_selector(line) and not line.startswith('fin'):
                css_property = self._convert_property(line)
                if css_property:
                    result.append(f'    {css_property}')
                    
            elif line.startswith('al_pasar_mouse') or line.startswith('hover'):
                hover_lines, i = self._process_hover(lines, i, css_selector)
                result.extend(hover_lines)
                continue
                
            elif line.startswith('al_hacer_click') or line.startswith('active'):
                active_lines, i = self._process_active(lines, i, css_selector)
                result.extend(active_lines)
                continue
                
            i += 1
        
        result.append('}')
        result.append('')  # Línea vacía para separación
        
        return result, i
    
    def _convert_selector(self, line):
        """Convierte selector de Vader a CSS"""
        selector_map = {
            'cuerpo': 'body',
            'encabezado': 'header',
            'navegacion': 'nav',
            'contenido': 'main',
            'seccion': 'section',
            'pie_pagina': 'footer',
            'titulo1': 'h1',
            'titulo2': 'h2',
            'titulo3': 'h3',
            'titulo4': 'h4',
            'titulo5': 'h5',
            'titulo6': 'h6',
            'parrafo': 'p',
            'enlace': 'a',
            'boton': 'button',
            'imagen': 'img',
            'lista': 'ul',
            'lista_ordenada': 'ol',
            'elemento': 'li',
            'formulario': 'form',
            'campo': 'input',
            'tarjeta': '.card',
            'contenedor': '.container'
        }
        
        # Buscar en el mapeo
        for vader_selector, css_selector in selector_map.items():
            if line.startswith(vader_selector):
                # Manejar clases adicionales
                if '"' in line:
                    class_name = line.split('"')[1]
                    return f'{css_selector}.{class_name}'
                return css_selector
        
        # Si no se encuentra, asumir que es una clase o ID
        if line.startswith('.') or line.startswith('#'):
            return line
            
        # Por defecto, tratar como clase
        return f'.{line}'
    
    def _convert_property(self, line):
        """Convierte propiedad de Vader a CSS"""
        # Mapeo de propiedades
        property_map = {
            'color': 'color',
            'fondo': 'background',
            'fondo_color': 'background-color',
            'fondo_imagen': 'background-image',
            'fondo_gradiente': 'background',
            'fuente': 'font-family',
            'tamaño_fuente': 'font-size',
            'peso_fuente': 'font-weight',
            'estilo_fuente': 'font-style',
            'altura_linea': 'line-height',
            'alineacion_texto': 'text-align',
            'decoracion_texto': 'text-decoration',
            'transformar_texto': 'text-transform',
            'ancho': 'width',
            'alto': 'height',
            'ancho_maximo': 'max-width',
            'alto_maximo': 'max-height',
            'ancho_minimo': 'min-width',
            'alto_minimo': 'min-height',
            'margen': 'margin',
            'margen_arriba': 'margin-top',
            'margen_abajo': 'margin-bottom',
            'margen_izquierda': 'margin-left',
            'margen_derecha': 'margin-right',
            'relleno': 'padding',
            'relleno_arriba': 'padding-top',
            'relleno_abajo': 'padding-bottom',
            'relleno_izquierda': 'padding-left',
            'relleno_derecha': 'padding-right',
            'borde': 'border',
            'borde_radio': 'border-radius',
            'borde_color': 'border-color',
            'borde_ancho': 'border-width',
            'borde_estilo': 'border-style',
            'sombra': 'box-shadow',
            'sombra_texto': 'text-shadow',
            'mostrar': 'display',
            'posicion': 'position',
            'arriba': 'top',
            'abajo': 'bottom',
            'izquierda': 'left',
            'derecha': 'right',
            'z_index': 'z-index',
            'flotante': 'float',
            'limpiar': 'clear',
            'desbordamiento': 'overflow',
            'visibilidad': 'visibility',
            'opacidad': 'opacity',
            'cursor': 'cursor',
            'transicion': 'transition',
            'transformar': 'transform',
            'filtro': 'filter'
        }
        
        # Buscar el signo igual
        if '=' in line:
            parts = line.split('=', 1)
            property_name = parts[0].strip()
            property_value = parts[1].strip().strip('"')
        elif ':' in line:
            parts = line.split(':', 1)
            property_name = parts[0].strip()
            property_value = parts[1].strip().strip('"')
        else:
            # Propiedades especiales sin valor
            return self._handle_special_properties(line)
        
        # Convertir nombre de propiedad
        css_property = property_map.get(property_name, property_name.replace('_', '-'))
        
        # Convertir valor
        css_value = self._convert_value(property_name, property_value)
        
        return f'{css_property}: {css_value};'
    
    def _convert_value(self, property_name, value):
        """Convierte valores de Vader a CSS"""
        # Convertir colores
        if property_name in ['color', 'fondo_color', 'borde_color']:
            return self.color_map.get(value.lower(), value)
        
        # Convertir gradientes
        if property_name == 'fondo_gradiente':
            if ' a ' in value:
                colors = value.split(' a ')
                color1 = self.color_map.get(colors[0].strip().lower(), colors[0].strip())
                color2 = self.color_map.get(colors[1].strip().lower(), colors[1].strip())
                return f'linear-gradient(135deg, {color1}, {color2})'
        
        # Convertir fuentes
        if property_name == 'fuente':
            font_map = {
                'arial': 'Arial, sans-serif',
                'helvetica': 'Helvetica, Arial, sans-serif',
                'times': 'Times, "Times New Roman", serif',
                'courier': 'Courier, "Courier New", monospace',
                'georgia': 'Georgia, serif',
                'verdana': 'Verdana, sans-serif'
            }
            return font_map.get(value.lower(), value)
        
        # Convertir pesos de fuente
        if property_name == 'peso_fuente':
            weight_map = {
                'normal': 'normal',
                'negrita': 'bold',
                'ligero': '300',
                'medio': '500',
                'pesado': '700',
                'extra_pesado': '900'
            }
            return weight_map.get(value.lower(), value)
        
        # Convertir alineación de texto
        if property_name == 'alineacion_texto':
            align_map = {
                'izquierda': 'left',
                'derecha': 'right',
                'centro': 'center',
                'justificado': 'justify'
            }
            return align_map.get(value.lower(), value)
        
        # Convertir display
        if property_name == 'mostrar':
            display_map = {
                'bloque': 'block',
                'linea': 'inline',
                'bloque_linea': 'inline-block',
                'flex': 'flex',
                'grid': 'grid',
                'tabla': 'table',
                'ninguno': 'none',
                'oculto': 'none'
            }
            return display_map.get(value.lower(), value)
        
        # Convertir posición
        if property_name == 'posicion':
            position_map = {
                'estatica': 'static',
                'relativa': 'relative',
                'absoluta': 'absolute',
                'fija': 'fixed',
                'pegajosa': 'sticky'
            }
            return position_map.get(value.lower(), value)
        
        return value
    
    def _handle_special_properties(self, line):
        """Maneja propiedades especiales sin valor"""
        special_map = {
            'centrar_texto': 'text-align: center;',
            'sin_decoracion': 'text-decoration: none;',
            'negrita': 'font-weight: bold;',
            'cursiva': 'font-style: italic;',
            'subrayado': 'text-decoration: underline;',
            'mayusculas': 'text-transform: uppercase;',
            'minusculas': 'text-transform: lowercase;',
            'capitalizar': 'text-transform: capitalize;',
            'centrar': 'margin: 0 auto;',
            'ocultar': 'display: none;',
            'mostrar_bloque': 'display: block;',
            'mostrar_flex': 'display: flex;',
            'sin_margen': 'margin: 0;',
            'sin_relleno': 'padding: 0;',
            'ancho_completo': 'width: 100%;',
            'alto_completo': 'height: 100%;'
        }
        
        return special_map.get(line, None)
    
    def _process_hover(self, lines, start_index, parent_selector):
        """Procesa estado hover"""
        result = [f'{parent_selector}:hover {{']
        
        i = start_index + 1
        while i < len(lines) and not lines[i].strip().startswith('fin hover'):
            line = lines[i].strip()
            
            if line and not line.startswith('fin'):
                css_property = self._convert_property(line)
                if css_property:
                    result.append(f'    {css_property}')
                    
            i += 1
        
        result.append('}')
        return result, i + 1
    
    def _process_active(self, lines, start_index, parent_selector):
        """Procesa estado active"""
        result = [f'{parent_selector}:active {{']
        
        i = start_index + 1
        while i < len(lines) and not lines[i].strip().startswith('fin active'):
            line = lines[i].strip()
            
            if line and not line.startswith('fin'):
                css_property = self._convert_property(line)
                if css_property:
                    result.append(f'    {css_property}')
                    
            i += 1
        
        result.append('}')
        return result, i + 1
    
    def _process_responsive(self, lines, start_index):
        """Procesa media queries responsivas"""
        result = []
        
        i = start_index + 1
        while i < len(lines) and not lines[i].strip().startswith('fin responsive'):
            line = lines[i].strip()
            
            if line.startswith('en_movil'):
                mobile_lines, i = self._process_media_query(lines, i, 'max-width: 768px')
                result.extend(mobile_lines)
                continue
                
            elif line.startswith('en_tablet'):
                tablet_lines, i = self._process_media_query(lines, i, 'max-width: 1024px')
                result.extend(tablet_lines)
                continue
                
            elif line.startswith('en_escritorio'):
                desktop_lines, i = self._process_media_query(lines, i, 'min-width: 1025px')
                result.extend(desktop_lines)
                continue
                
            i += 1
        
        return result, i + 1
    
    def _process_media_query(self, lines, start_index, media_condition):
        """Procesa una media query específica"""
        result = [f'@media ({media_condition}) {{']
        
        i = start_index + 1
        while i < len(lines) and not self._is_end_of_media_query(lines[i]):
            line = lines[i].strip()
            
            if self._is_selector(line):
                selector_lines, i = self._process_selector(lines, i)
                # Indentar las reglas dentro de la media query
                for selector_line in selector_lines:
                    result.append(f'    {selector_line}')
                continue
                
            i += 1
        
        result.append('}')
        return result, i + 1
    
    def _process_animation(self, lines, start_index):
        """Procesa animaciones CSS"""
        line = lines[start_index].strip()
        
        # Extraer nombre de la animación
        animation_name = "vader-animation"
        if '"' in line:
            animation_name = line.split('"')[1]
        
        result = [f'@keyframes {animation_name} {{']
        
        i = start_index + 1
        while i < len(lines) and not lines[i].strip().startswith('fin animacion'):
            line = lines[i].strip()
            
            if line.startswith('desde') or line.startswith('0%'):
                result.append('    0% {')
            elif line.startswith('hasta') or line.startswith('100%'):
                result.append('    100% {')
            elif line.endswith('%'):
                result.append(f'    {line} {{')
            elif line and not line.startswith('fin'):
                css_property = self._convert_property(line)
                if css_property:
                    result.append(f'        {css_property}')
            elif line == '}' or line.startswith('fin paso'):
                result.append('    }')
                
            i += 1
        
        result.append('}')
        return result, i + 1
    
    def _is_end_of_selector(self, line):
        """Determina si es el final de un selector"""
        line = line.strip()
        return (self._is_selector(line) or 
                line.startswith('fin estilos') or 
                line.startswith('responsive') or
                line.startswith('animacion') or
                line == '')
    
    def _is_end_of_media_query(self, line):
        """Determina si es el final de una media query"""
        line = line.strip()
        return (line.startswith('fin movil') or 
                line.startswith('fin tablet') or
                line.startswith('fin escritorio') or
                line.startswith('fin responsive'))
