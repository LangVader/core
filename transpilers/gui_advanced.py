# Advanced GUI Transpiler for Vader
# Extends Vader with modern GUI capabilities for complex applications

import re
import json

class AdvancedGUITranspiler:
    def __init__(self):
        self.indent_level = 0
        self.components = {}
        self.styles = {}
        self.events = {}
        self.variables = {}
        self.current_component = None
        self.layout_stack = []
        
    def transpile(self, vader_code):
        """Transpile Vader GUI code to complete web application"""
        lines = vader_code.split('\n')
        
        # Parse all components, styles, and events first
        self.parse_definitions(lines)
        
        # Generate HTML structure
        html = self.generate_html()
        
        # Generate CSS styles
        css = self.generate_css()
        
        # Generate JavaScript functionality
        js = self.generate_javascript()
        
        return {
            'html': html,
            'css': css,
            'js': js,
            'package_json': self.generate_package_json()
        }
    
    def parse_definitions(self, lines):
        """Parse component definitions, styles, and events"""
        current_section = None
        current_component = None
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('//'):
                continue
            
            # Application configuration
            if line.startswith('configurar aplicacion'):
                current_section = 'app_config'
                continue
            
            # Component definitions
            if line.startswith('crear componente '):
                component_name = line.replace('crear componente ', '')
                current_component = component_name
                self.components[component_name] = {
                    'type': 'container',
                    'properties': {},
                    'children': [],
                    'events': {}
                }
                current_section = 'component'
                continue
            
            # Layout containers
            if line.startswith('crear contenedor '):
                container_name = line.replace('crear contenedor ', '')
                self.components[container_name] = {
                    'type': 'container',
                    'properties': {'display': 'flex'},
                    'children': [],
                    'events': {}
                }
                current_component = container_name
                continue
            
            # UI Elements
            if line.startswith('crear '):
                self.parse_ui_element(line, current_component)
                continue
            
            # Styles
            if line.startswith('definir tema ') or line.startswith('aplicar_a '):
                current_section = 'styles'
                self.parse_style_definition(line)
                continue
            
            # Events
            if line.startswith('cuando '):
                current_section = 'events'
                self.parse_event_definition(line, current_component)
                continue
            
            # Properties for current component
            if current_component and current_section in ['component', 'ui_element']:
                self.parse_property(line, current_component)
    
    def parse_ui_element(self, line, parent_component):
        """Parse UI element creation"""
        parts = line.replace('crear ', '').split(' ', 1)
        element_type = parts[0]
        element_name = parts[1] if len(parts) > 1 else f"{element_type}_{len(self.components)}"
        
        element_config = {
            'type': element_type,
            'properties': {},
            'children': [],
            'events': {}
        }
        
        # Map Vader element types to HTML/CSS
        type_mapping = {
            'boton': {'tag': 'button', 'class': 'vader-button'},
            'texto': {'tag': 'span', 'class': 'vader-text'},
            'entrada': {'tag': 'input', 'class': 'vader-input'},
            'imagen': {'tag': 'img', 'class': 'vader-image'},
            'panel': {'tag': 'div', 'class': 'vader-panel'},
            'lista': {'tag': 'ul', 'class': 'vader-list'},
            'pestana': {'tag': 'div', 'class': 'vader-tab'},
            'pestañas': {'tag': 'div', 'class': 'vader-tabs'},
            'menu': {'tag': 'nav', 'class': 'vader-menu'},
            'barra_herramientas': {'tag': 'div', 'class': 'vader-toolbar'},
            'barra_estado': {'tag': 'div', 'class': 'vader-status-bar'},
            'editor_codigo': {'tag': 'textarea', 'class': 'vader-code-editor'},
            'arbol': {'tag': 'div', 'class': 'vader-tree'},
            'terminal': {'tag': 'div', 'class': 'vader-terminal'}
        }
        
        if element_type in type_mapping:
            element_config.update(type_mapping[element_type])
        
        self.components[element_name] = element_config
        
        # Add to parent if exists
        if parent_component and parent_component in self.components:
            self.components[parent_component]['children'].append(element_name)
        
        return element_name
    
    def parse_property(self, line, component_name):
        """Parse component properties"""
        if component_name not in self.components:
            return
        
        component = self.components[component_name]
        
        # Layout properties
        if line.startswith('orientacion '):
            direction = line.replace('orientacion ', '')
            if direction == 'horizontal':
                component['properties']['flex-direction'] = 'row'
            elif direction == 'vertical':
                component['properties']['flex-direction'] = 'column'
        
        elif line.startswith('ancho '):
            width = line.replace('ancho ', '').replace(' pixeles', 'px').replace('%', '%')
            component['properties']['width'] = width
        
        elif line.startswith('alto '):
            height = line.replace('alto ', '').replace(' pixeles', 'px').replace('%', '%')
            component['properties']['height'] = height
        
        elif line.startswith('color fondo '):
            color = line.replace('color fondo ', '').replace('"', '')
            component['properties']['background-color'] = color
        
        elif line.startswith('color texto '):
            color = line.replace('color texto ', '').replace('"', '')
            component['properties']['color'] = color
        
        elif line.startswith('fuente '):
            font = line.replace('fuente ', '').replace('"', '')
            component['properties']['font-family'] = font
        
        elif line.startswith('borde '):
            border = line.replace('borde ', '')
            component['properties']['border'] = border
        
        elif line.startswith('margen '):
            margin = line.replace('margen ', '').replace(' pixeles', 'px')
            component['properties']['margin'] = margin
        
        elif line.startswith('padding '):
            padding = line.replace('padding ', '').replace(' pixeles', 'px')
            component['properties']['padding'] = padding
        
        elif line.startswith('flex '):
            flex = line.replace('flex ', '')
            component['properties']['flex'] = flex
        
        elif line.startswith('posicion '):
            position = line.replace('posicion ', '')
            if position == 'absoluta':
                component['properties']['position'] = 'absolute'
            elif position == 'relativa':
                component['properties']['position'] = 'relative'
            elif position == 'fija':
                component['properties']['position'] = 'fixed'
        
        elif line.startswith('contenido '):
            content = line.replace('contenido ', '').replace('"', '')
            component['properties']['content'] = content
        
        elif line.startswith('placeholder '):
            placeholder = line.replace('placeholder ', '').replace('"', '')
            component['properties']['placeholder'] = placeholder
    
    def parse_event_definition(self, line, component_name):
        """Parse event definitions"""
        if not component_name or component_name not in self.components:
            return
        
        # Extract event type and action
        if line.startswith('cuando '):
            event_def = line.replace('cuando ', '')
            
            # Common event patterns
            if 'click' in event_def:
                event_type = 'click'
                action = event_def.replace('click', '').strip()
            elif 'hover' in event_def:
                event_type = 'mouseenter'
                action = event_def.replace('hover', '').strip()
            elif 'cambiar' in event_def or 'change' in event_def:
                event_type = 'change'
                action = event_def.replace('cambiar', '').replace('change', '').strip()
            elif 'enter' in event_def:
                event_type = 'keypress'
                action = event_def.replace('enter', '').strip()
            else:
                event_type = 'click'  # default
                action = event_def
            
            self.components[component_name]['events'][event_type] = action
    
    def parse_style_definition(self, line):
        """Parse style and theme definitions"""
        # This would handle theme definitions
        pass
    
    def generate_html(self):
        """Generate complete HTML structure"""
        html = '''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Vader GUI Application</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
'''
        
        # Generate component tree
        for name, component in self.components.items():
            if not any(name in comp['children'] for comp in self.components.values()):
                # This is a root component
                html += self.generate_component_html(name, component, 1)
        
        html += '''
    <script src="script.js"></script>
</body>
</html>'''
        
        return html
    
    def generate_component_html(self, name, component, indent_level):
        """Generate HTML for a single component"""
        indent = '    ' * indent_level
        tag = component.get('tag', 'div')
        css_class = component.get('class', 'vader-component')
        
        # Start tag
        html = f'{indent}<{tag} id="{name}" class="{css_class}"'
        
        # Add properties as attributes
        if 'placeholder' in component['properties']:
            html += f' placeholder="{component["properties"]["placeholder"]}"'
        
        html += '>\n'
        
        # Add content
        if 'content' in component['properties']:
            html += f'{indent}    {component["properties"]["content"]}\n'
        
        # Add children
        for child_name in component['children']:
            if child_name in self.components:
                child_component = self.components[child_name]
                html += self.generate_component_html(child_name, child_component, indent_level + 1)
        
        # End tag
        html += f'{indent}</{tag}>\n'
        
        return html
    
    def generate_css(self):
        """Generate CSS styles"""
        css = '''/* Vader GUI Application Styles */

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background-color: #1e1e1e;
    color: #cccccc;
    height: 100vh;
    overflow: hidden;
}

/* Component-specific styles */
'''
        
        # Generate styles for each component
        for name, component in self.components.items():
            css += f'#{name} {{\n'
            
            for prop, value in component['properties'].items():
                if prop not in ['content', 'placeholder']:  # Skip non-CSS properties
                    css += f'    {prop}: {value};\n'
            
            css += '}\n\n'
        
        # Add default component styles
        css += '''
.vader-button {
    background-color: #0e639c;
    border: 1px solid #0e639c;
    color: white;
    padding: 6px 12px;
    border-radius: 3px;
    cursor: pointer;
    font-size: 12px;
    transition: all 0.1s ease;
}

.vader-button:hover {
    background-color: #1177bb;
    border-color: #1177bb;
}

.vader-input {
    background-color: #3c3c3c;
    border: 1px solid #3c3c3c;
    color: #cccccc;
    padding: 4px 8px;
    border-radius: 2px;
    font-size: 13px;
    outline: none;
}

.vader-input:focus {
    border-color: #007acc;
    background-color: #2d2d30;
}

.vader-panel {
    background-color: #252526;
    border: 1px solid #3c3c3c;
}

.vader-code-editor {
    background-color: #1e1e1e;
    color: #cccccc;
    border: none;
    outline: none;
    font-family: 'Cascadia Code', 'Monaco', monospace;
    font-size: 14px;
    padding: 10px;
    resize: none;
}

.vader-toolbar {
    background-color: #2d2d30;
    border-bottom: 1px solid #3c3c3c;
    display: flex;
    align-items: center;
    padding: 0 10px;
    gap: 10px;
    height: 35px;
}

.vader-status-bar {
    background-color: #007acc;
    color: white;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 10px;
    font-size: 12px;
    height: 25px;
}

.vader-tabs {
    display: flex;
    background-color: #2d2d30;
    border-bottom: 1px solid #3c3c3c;
}

.vader-tab {
    padding: 8px 16px;
    background-color: #2d2d30;
    border-right: 1px solid #3c3c3c;
    cursor: pointer;
    transition: background-color 0.2s ease;
}

.vader-tab:hover {
    background-color: #37373d;
}

.vader-tab.active {
    background-color: #1e1e1e;
    border-bottom: 2px solid #007acc;
}
'''
        
        return css
    
    def generate_javascript(self):
        """Generate JavaScript functionality"""
        js = '''// Vader GUI Application JavaScript

// Component event handlers
const VaderApp = {
    components: {},
    
    init() {
        this.bindEvents();
        this.initializeComponents();
    },
    
    bindEvents() {
'''
        
        # Generate event handlers
        for name, component in self.components.items():
            for event_type, action in component['events'].items():
                js += f'''        document.getElementById('{name}').addEventListener('{event_type}', function(e) {{
            {self.generate_action_code(action)}
        }});
'''
        
        js += '''    },
    
    initializeComponents() {
        // Initialize component-specific functionality
'''
        
        # Add component initialization
        for name, component in self.components.items():
            if component['type'] == 'editor_codigo':
                js += f'''        this.initCodeEditor('{name}');
'''
            elif component['type'] == 'terminal':
                js += f'''        this.initTerminal('{name}');
'''
        
        js += '''    },
    
    initCodeEditor(elementId) {
        const editor = document.getElementById(elementId);
        // Add syntax highlighting, line numbers, etc.
        editor.addEventListener('input', function() {
            // Update line numbers, syntax highlighting
        });
    },
    
    initTerminal(elementId) {
        const terminal = document.getElementById(elementId);
        // Initialize terminal functionality
    }
};

// Initialize application when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    VaderApp.init();
});
'''
        
        return js
    
    def generate_action_code(self, action):
        """Generate JavaScript code for actions"""
        if action.startswith('mostrar '):
            target = action.replace('mostrar ', '')
            return f"document.getElementById('{target}').style.display = 'block';"
        elif action.startswith('ocultar '):
            target = action.replace('ocultar ', '')
            return f"document.getElementById('{target}').style.display = 'none';"
        elif action.startswith('ejecutar '):
            command = action.replace('ejecutar ', '')
            return f"console.log('Ejecutando: {command}');"
        else:
            return f"console.log('Acción: {action}');"
    
    def generate_package_json(self):
        """Generate package.json for Electron app"""
        return {
            "name": "vader-gui-app",
            "version": "1.0.0",
            "description": "GUI Application generated by Vader",
            "main": "main.js",
            "scripts": {
                "start": "electron .",
                "dev": "electron . --dev"
            },
            "devDependencies": {
                "electron": "^22.0.0"
            }
        }

def transpile_to_gui(vader_code):
    """Main function to transpile Vader to GUI application"""
    transpiler = AdvancedGUITranspiler()
    return transpiler.transpile(vader_code)

def transpilar(vader_code):
    """Alias for CLI compatibility"""
    return transpile_to_gui(vader_code)
