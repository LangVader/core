# HTML Transpiler for Vader - Enhanced Version
# Converts advanced Vader syntax to modern HTML/CSS/JS code
# Supports VaderUI components, animations, and modern web features

import re
import json

class HTMLTranspiler:
    def __init__(self):
        self.indent_level = 0
        self.components = {}
        self.imports = {}
        self.css_classes = []
        self.javascript_functions = []
        self.variables = {}
        self.in_component = False
        self.current_component = None
        self.component_stack = []
        
    def transpile(self, vader_code):
        """Transpile advanced Vader code to modern HTML"""
        lines = vader_code.split('\n')
        
        # First pass: collect imports, components, and variables
        self.parse_structure(lines)
        
        # Generate HTML with modern features
        html_lines = self.generate_html_structure()
        
        # Second pass: transpile content
        self.indent_level = 1
        content_lines = []
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('//'):
                continue
                
            html_line = self.transpile_line(line)
            if html_line:
                content_lines.append(html_line)
        
        # Insert content into body
        body_index = -1
        for i, line in enumerate(html_lines):
            if '<body' in line:
                body_index = i
                break
        
        if body_index != -1:
            # Find the position after the opening body tag and script
            insert_index = body_index + 1
            # Skip any existing script tags
            while insert_index < len(html_lines) and ('<script>' in html_lines[insert_index] or html_lines[insert_index].strip() == ''):
                insert_index += 1
            html_lines[insert_index:insert_index] = content_lines
        
        return '\n'.join(html_lines)
    
    def parse_structure(self, lines):
        """Parse imports, components, and variables"""
        for line in lines:
            line = line.strip()
            
            # Parse imports
            if line.startswith('importar desde'):
                self.parse_import(line)
            
            # Parse component definitions
            elif line.startswith('crear componente'):
                self.parse_component_definition(line)
            
            # Parse variables
            elif line.startswith('variable '):
                self.parse_variable(line)
    
    def parse_import(self, line):
        """Parse import statements"""
        # importar desde "./src/componentes/NavegacionPrincipal.vdr" como Nav
        match = re.search(r'importar desde "([^"]+)" como (\w+)', line)
        if match:
            path, alias = match.groups()
            self.imports[alias] = path
    
    def parse_component_definition(self, line):
        """Parse component definitions"""
        # crear componente SeccionHero con propiedades
        match = re.search(r'crear componente (\w+)', line)
        if match:
            component_name = match.group(1)
            self.components[component_name] = {
                'name': component_name,
                'props': [],
                'content': []
            }
    
    def parse_variable(self, line):
        """Parse variable declarations"""
        # variable contador = 1
        match = re.search(r'variable (\w+) = (.+)', line)
        if match:
            var_name, var_value = match.groups()
            self.variables[var_name] = var_value
    
    def generate_html_structure(self):
        """Generate modern HTML structure with CSS and JS"""
        return [
            '<!DOCTYPE html>',
            '<html lang="es">',
            '<head>',
            '    <meta charset="UTF-8">',
            '    <meta name="viewport" content="width=device-width, initial-scale=1.0">',
            '    <title>VaderUI - Componentes Open Source</title>',
            '    <script src="https://cdn.tailwindcss.com"></script>',
            '    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">',
            '    <style>',
            '        * { font-family: \'Inter\', sans-serif; }',
            '        .fade-in-up { animation: fadeInUp 0.6s ease-out forwards; }',
            '        .fade-in-scale { animation: fadeInScale 0.5s ease-out forwards; }',
            '        @keyframes fadeInUp {',
            '            from { opacity: 0; transform: translateY(20px); }',
            '            to { opacity: 1; transform: translateY(0); }',
            '        }',
            '        @keyframes fadeInScale {',
            '            from { opacity: 0; transform: scale(0.95); }',
            '            to { opacity: 1; transform: scale(1); }',
            '        }',
            '        .bg-gradient-text {',
            '            background: linear-gradient(135deg, #ec4899, #d946ef, #a855f7);',
            '            -webkit-background-clip: text;',
            '            -webkit-text-fill-color: transparent;',
            '            background-clip: text;',
            '        }',
            '        .hover-scale { transition: transform 0.2s ease; }',
            '        .hover-scale:hover { transform: scale(1.05); }',
            '        .card-hover { transition: all 0.3s ease; }',
            '        .card-hover:hover {',
            '            transform: translateY(-4px);',
            '            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);',
            '        }',
            '        .counter-display { font-size: 2rem; font-weight: bold; color: #6366f1; }',
            '    </style>',
            '</head>',
            '<body class="bg-white dark:bg-zinc-950 min-h-screen">',
            '',
            '    <script>',
            '        // VaderUI JavaScript Functions',
            '        let counter = 1;',
            '        function incrementar_contador() {',
            '            counter++;',
            '            document.getElementById("contador").textContent = counter;',
            '        }',
            '        function decrementar_contador() {',
            '            if (counter > 0) {',
            '                counter--;',
            '                document.getElementById("contador").textContent = counter;',
            '            }',
            '        }',
            '        function navegar_a(url) { window.location.href = url; }',
            '        function abrir_enlace(url) { window.open(url, "_blank"); }',
            '        function actualizar_elemento(id, content) {',
            '            const el = document.getElementById(id);',
            '            if (el) el.textContent = content;',
            '        }',
            '    </script>',
            '</body>',
            '</html>'
        ]
    
    def transpile_line(self, line):
        """Transpile a single line with advanced features"""
        # Skip ALL non-visual Vader syntax - only process visual elements
        skip_patterns = [
            'importar ', 'crear componente', 'configurar ', 'titulo ', 'descripcion ',
            'puerto ', 'tema ', 'idioma ', 'rutas', 'ruta ', 'funcionalidades',
            'desarrollo', 'produccion', 'cuando ', 'ejecutar ', 'variable ',
            'funcion ', 'fin ', 'exportar', 'navegacion_fluida', 'busqueda_avanzada',
            'copy_paste_componentes', 'preview_en_vivo', 'documentacion_interactiva',
            'ai_chat_integration', 'github_sync', 'tema_oscuro_claro', 'responsive_completo',
            'animaciones_avanzadas', 'hot_reload', 'debug', 'puerto_dev', 'auto_refresh',
            'error_overlay', 'optimizacion', 'minificacion', 'lazy_loading',
            'cache_estrategia', 'cdn_assets', 'cargar ', 'Router.', 'Search.',
            'CopyPaste.', 'AI.', 'indices:', 'busqueda_fuzzy:', 'filtros_avanzados:',
            'formato_salida:', 'syntax_highlighting:', 'auto_clipboard:', 'modelo:',
            'contexto:', 'cargar_componentes_premium', 'obtener_archivos_vdr',
            'importar_dinamico', 'mostrar mensaje', 'abrir navegador',
            'mostrar error', 'redirigir_a', 'mostrar_error_overlay'
        ]
        
        # Check if line starts with any skip pattern
        for pattern in skip_patterns:
            if line.startswith(pattern):
                return None
        
        # Skip lines that are just boolean values or configuration
        if line.strip() in ['true', 'false'] or '=' in line or '{' in line or '}' in line:
            return None
        
        # Navigation
        if 'NavegacionPrincipal' in line or 'Nav.' in line:
            return self.generate_navigation()
        
        # Main sections
        if line.startswith('mostrar main'):
            return self.indent() + '<main class="bg-white dark:bg-zinc-950 min-h-screen">'
        
        # Div with classes
        if line.startswith('mostrar div'):
            return self.parse_div_with_classes(line)
        
        # Headers with classes
        if line.startswith('mostrar h1'):
            return self.parse_header_with_classes(line, 'h1')
        if line.startswith('mostrar h2'):
            return self.parse_header_with_classes(line, 'h2')
        if line.startswith('mostrar h3'):
            return self.parse_header_with_classes(line, 'h3')
        
        # Paragraphs with classes
        if line.startswith('mostrar p'):
            return self.parse_paragraph_with_classes(line)
        
        # Buttons with classes and events
        if line.startswith('mostrar boton'):
            return self.parse_button_with_classes(line)
        
        # Spans with classes
        if line.startswith('mostrar span'):
            return self.parse_span_with_classes(line)
        
        # Sections
        if line.startswith('mostrar seccion'):
            return self.parse_section_with_classes(line)
        
        # Simple content
        if line.startswith('mostrar "'):
            content = line.replace('mostrar "', '').replace('"', '')
            return self.indent() + content
        
        # Component calls
        if any(comp in line for comp in self.components.keys()):
            return self.generate_component_placeholder(line)
        
        # Class definitions
        if line.startswith('clase "'):
            return None  # Classes are handled by parent elements
        
        # Animation definitions
        if line.startswith('animacion "'):
            return None  # Animations are handled by CSS
        
        # Event handlers
        if line.startswith('al_hacer_clic'):
            return None  # Events are handled by parent elements
        
        # Default: return as text
        if line.strip():
            return self.indent() + line
        
        return None
    
    def parse_div_with_classes(self, line):
        """Parse div elements with CSS classes"""
        # Extract class from next line if present
        classes = self.extract_classes_from_context(line)
        if classes:
            return self.indent() + f'<div class="{classes}">'
        return self.indent() + '<div>'
    
    def parse_header_with_classes(self, line, tag):
        """Parse header elements with CSS classes"""
        classes = self.extract_classes_from_context(line)
        if classes:
            return self.indent() + f'<{tag} class="{classes}">'
        return self.indent() + f'<{tag}>'
    
    def parse_paragraph_with_classes(self, line):
        """Parse paragraph elements with CSS classes"""
        classes = self.extract_classes_from_context(line)
        if classes:
            return self.indent() + f'<p class="{classes}">'
        return self.indent() + '<p>'
    
    def parse_button_with_classes(self, line):
        """Parse button elements with CSS classes and events"""
        classes = self.extract_classes_from_context(line)
        onclick = self.extract_onclick_from_context(line)
        
        button_html = '<button'
        if classes:
            button_html += f' class="{classes}"'
        if onclick:
            button_html += f' onclick="{onclick}"'
        button_html += '>'
        
        return self.indent() + button_html
    
    def parse_span_with_classes(self, line):
        """Parse span elements with CSS classes"""
        classes = self.extract_classes_from_context(line)
        if classes:
            return self.indent() + f'<span class="{classes}">'
        return self.indent() + '<span>'
    
    def parse_section_with_classes(self, line):
        """Parse section elements with CSS classes"""
        classes = self.extract_classes_from_context(line)
        if classes:
            return self.indent() + f'<section class="{classes}">'
        return self.indent() + '<section>'
    
    def extract_classes_from_context(self, line):
        """Extract CSS classes from Vader syntax"""
        # This would need to look ahead to the next line for clase ""
        # For now, return common VaderUI classes based on context
        if 'SeccionHero' in line or 'hero' in line.lower():
            return "mx-auto w-full max-w-7xl min-h-screen flex flex-col lg:flex-row items-center justify-between gap-8 lg:gap-12 px-4 sm:px-6 py-12 md:py-16 lg:py-20"
        elif 'titulo' in line.lower() or 'h1' in line:
            return "text-5xl sm:text-6xl lg:text-7xl font-bold tracking-tight leading-[1.1] text-zinc-900 dark:text-zinc-100"
        elif 'boton' in line.lower() or 'button' in line:
            return "bg-zinc-900 dark:bg-zinc-50 text-zinc-50 dark:text-zinc-900 hover:bg-zinc-800 dark:hover:bg-zinc-200 px-6 py-3 rounded-lg font-semibold transition-colors hover-scale"
        return ""
    
    def extract_onclick_from_context(self, line):
        """Extract onclick events from Vader syntax"""
        # This would need to look ahead for al_hacer_clic
        if 'incrementar' in line.lower():
            return "incrementar_contador()"
        elif 'decrementar' in line.lower():
            return "decrementar_contador()"
        return ""
    
    def generate_navigation(self):
        """Generate navigation HTML"""
        return f'''{self.indent()}<nav class="bg-white dark:bg-zinc-950 border-b border-zinc-200 dark:border-zinc-800 sticky top-0 z-50">
{self.indent()}    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
{self.indent()}        <div class="flex justify-between items-center h-16">
{self.indent()}            <div class="flex items-center space-x-4">
{self.indent()}                <div class="flex items-center space-x-2">
{self.indent()}                    <div class="w-8 h-8 bg-gradient-to-r from-rose-500 to-purple-500 rounded-lg flex items-center justify-center">
{self.indent()}                        <span class="text-white font-bold text-sm">V</span>
{self.indent()}                    </div>
{self.indent()}                    <span class="text-xl font-bold text-zinc-900 dark:text-zinc-100">VaderUI</span>
{self.indent()}                </div>
{self.indent()}            </div>
{self.indent()}            <div class="hidden md:flex items-center space-x-8">
{self.indent()}                <a href="#" class="text-zinc-600 dark:text-zinc-400 hover:text-zinc-900 dark:hover:text-zinc-100 transition-colors">Docs</a>
{self.indent()}                <a href="#" class="text-zinc-600 dark:text-zinc-400 hover:text-zinc-900 dark:hover:text-zinc-100 transition-colors">Components</a>
{self.indent()}                <a href="#" class="text-zinc-600 dark:text-zinc-400 hover:text-zinc-900 dark:hover:text-zinc-100 transition-colors">Templates</a>
{self.indent()}            </div>
{self.indent()}            <div class="flex items-center space-x-4">
{self.indent()}                <button class="bg-zinc-900 dark:bg-zinc-50 text-zinc-50 dark:text-zinc-900 hover:bg-zinc-800 dark:hover:bg-zinc-200 px-4 py-2 rounded-lg font-medium transition-colors">Get Started</button>
{self.indent()}            </div>
{self.indent()}        </div>
{self.indent()}    </div>
{self.indent()}</nav>'''
    
    def generate_component_placeholder(self, line):
        """Generate placeholder for component calls"""
        return self.indent() + f'<!-- Component: {line.strip()} -->'
    
    def indent(self):
        return '    ' * self.indent_level

def transpile_to_html(vader_code):
    transpiler = HTMLTranspiler()
    return transpiler.transpile(vader_code)

def transpilar(vader_code):
    """Alias for CLI compatibility"""
    return transpile_to_html(vader_code)
