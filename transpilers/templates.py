# Sistema de Plantillas y Componentes Reutilizables para Vader
# Permite crear aplicaciones complejas usando componentes predefinidos

import os
import json
from pathlib import Path

class VaderTemplateSystem:
    """Sistema de plantillas para Vader"""
    
    def __init__(self):
        self.templates_dir = Path(__file__).parent.parent / "plantillas"
        self.components_dir = Path(__file__).parent.parent / "componentes"
        self.ensure_directories()
    
    def ensure_directories(self):
        """Crear directorios de plantillas y componentes si no existen"""
        self.templates_dir.mkdir(exist_ok=True)
        self.components_dir.mkdir(exist_ok=True)
    
    def get_available_templates(self):
        """Obtener todas las plantillas disponibles"""
        templates = {}
        if self.templates_dir.exists():
            for template_file in self.templates_dir.glob("*.json"):
                with open(template_file, 'r', encoding='utf-8') as f:
                    template_data = json.load(f)
                    templates[template_file.stem] = template_data
        return templates
    
    def get_available_components(self):
        """Obtener todos los componentes disponibles"""
        components = {}
        if self.components_dir.exists():
            for component_file in self.components_dir.glob("*.vdr"):
                with open(component_file, 'r', encoding='utf-8') as f:
                    component_code = f.read()
                    components[component_file.stem] = component_code
        return components
    
    def apply_template(self, template_name, variables=None):
        """Aplicar una plantilla con variables específicas"""
        templates = self.get_available_templates()
        if template_name not in templates:
            raise ValueError(f"Plantilla '{template_name}' no encontrada")
        
        template = templates[template_name]
        code = template.get('code', '')
        
        # Reemplazar variables en el código
        if variables:
            for var_name, var_value in variables.items():
                code = code.replace(f"{{{var_name}}}", str(var_value))
        
        return code
    
    def use_component(self, component_name, props=None):
        """Usar un componente con propiedades específicas"""
        components = self.get_available_components()
        if component_name not in components:
            raise ValueError(f"Componente '{component_name}' no encontrado")
        
        component_code = components[component_name]
        
        # Reemplazar propiedades en el componente
        if props:
            for prop_name, prop_value in props.items():
                component_code = component_code.replace(f"{{{prop_name}}}", str(prop_value))
        
        return component_code

def transpile_with_templates(code):
    """Transpila código que incluye plantillas y componentes"""
    template_system = VaderTemplateSystem()
    lines = code.split('\n')
    result = []
    
    for line in lines:
        line = line.strip()
        
        if line.startswith('usar plantilla'):
            # Usar plantilla: usar plantilla "web_basica" con titulo="Mi App"
            parts = line.replace('usar plantilla', '').strip()
            if 'con' in parts:
                template_name, variables_part = parts.split('con', 1)
                template_name = template_name.strip().strip('"')
                
                # Parsear variables
                variables = {}
                for var_pair in variables_part.split(','):
                    if '=' in var_pair:
                        var_name, var_value = var_pair.split('=', 1)
                        variables[var_name.strip()] = var_value.strip().strip('"')
                
                template_code = template_system.apply_template(template_name, variables)
                result.append(template_code)
            else:
                template_name = parts.strip().strip('"')
                template_code = template_system.apply_template(template_name)
                result.append(template_code)
        
        elif line.startswith('usar componente'):
            # Usar componente: usar componente "boton_moderno" con texto="Enviar", color="azul"
            parts = line.replace('usar componente', '').strip()
            if 'con' in parts:
                component_name, props_part = parts.split('con', 1)
                component_name = component_name.strip().strip('"')
                
                # Parsear propiedades
                props = {}
                for prop_pair in props_part.split(','):
                    if '=' in prop_pair:
                        prop_name, prop_value = prop_pair.split('=', 1)
                        props[prop_name.strip()] = prop_value.strip().strip('"')
                
                component_code = template_system.use_component(component_name, props)
                result.append(component_code)
            else:
                component_name = parts.strip().strip('"')
                component_code = template_system.use_component(component_name)
                result.append(component_code)
        
        elif line.startswith('listar plantillas'):
            # Mostrar plantillas disponibles
            templates = template_system.get_available_templates()
            result.append(f"# Plantillas disponibles: {list(templates.keys())}")
        
        elif line.startswith('listar componentes'):
            # Mostrar componentes disponibles
            components = template_system.get_available_components()
            result.append(f"# Componentes disponibles: {list(components.keys())}")
        
        else:
            result.append(line)
    
    return '\n'.join(result)

# Palabras clave para detección de plantillas
TEMPLATE_KEYWORDS = [
    'usar plantilla', 'usar componente', 'listar plantillas', 'listar componentes'
]

def detect_templates(code):
    """Detecta si el código usa plantillas o componentes"""
    code_lower = code.lower()
    return any(keyword in code_lower for keyword in TEMPLATE_KEYWORDS)
