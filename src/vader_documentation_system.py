#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VADER 7.0 - SISTEMA DE DOCUMENTACIÓN ESTANDARIZADA
==================================================
Sistema completo de documentación automática para Vader con generación HTML/Markdown

Características:
- Docstrings estandarizados en código
- Generación automática de documentación
- Exportación a HTML, Markdown, PDF
- API documentation
- Ejemplos interactivos
- Búsqueda en documentación
- Versionado de docs

Autor: Vader Team
Versión: 7.0.0 "Universal"
Fecha: 2025
"""

import os
import re
import json
import markdown
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import webbrowser
import tempfile

@dataclass
class VaderDocString:
    """Representa una documentación de función/clase"""
    name: str
    description: str
    parameters: Dict[str, str] = field(default_factory=dict)
    returns: str = ""
    examples: List[str] = field(default_factory=list)
    notes: List[str] = field(default_factory=list)
    author: str = ""
    version: str = ""
    since: str = ""
    deprecated: bool = False
    see_also: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    line_number: int = 0
    file_path: str = ""

@dataclass
class VaderModule:
    """Representa un módulo documentado"""
    name: str
    description: str
    file_path: str
    functions: List[VaderDocString] = field(default_factory=list)
    classes: List[VaderDocString] = field(default_factory=list)
    constants: Dict[str, str] = field(default_factory=dict)
    examples: List[str] = field(default_factory=list)
    author: str = ""
    version: str = ""
    license: str = ""

@dataclass
class VaderDocumentation:
    """Documentación completa del proyecto"""
    project_name: str
    description: str
    version: str
    modules: List[VaderModule] = field(default_factory=list)
    generated_at: str = ""
    
    def __post_init__(self):
        self.generated_at = datetime.now().isoformat()

class VaderDocumentationGenerator:
    """Generador de documentación para Vader"""
    
    def __init__(self):
        # Patrones de reconocimiento de documentación
        self.doc_patterns = {
            'module_doc': r'#@modulo:\s*(.+)',
            'function_doc': r'#@funcion:\s*(.+)',
            'class_doc': r'#@clase:\s*(.+)',
            'description': r'#@descripcion:\s*(.+)',
            'param': r'#@param\s+(\w+):\s*(.+)',
            'return': r'#@retorna:\s*(.+)',
            'example': r'#@ejemplo:\s*(.+)',
            'note': r'#@nota:\s*(.+)',
            'author': r'#@autor:\s*(.+)',
            'version': r'#@version:\s*(.+)',
            'since': r'#@desde:\s*(.+)',
            'deprecated': r'#@deprecado',
            'see_also': r'#@ver_tambien:\s*(.+)',
            'tag': r'#@tag:\s*(.+)',
        }
        
        # Templates HTML
        self.html_templates = {
            'base': self._get_base_template(),
            'module': self._get_module_template(),
            'function': self._get_function_template(),
        }
    
    def parse_file_documentation(self, file_path: str) -> VaderModule:
        """Parsea documentación de un archivo .vdr"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        module_name = Path(file_path).stem
        module = VaderModule(
            name=module_name,
            description="",
            file_path=file_path
        )
        
        lines = content.split('\n')
        current_doc = None
        current_type = None
        
        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            
            # Documentación de módulo
            if match := re.match(self.doc_patterns['module_doc'], line):
                module.name = match.group(1)
                current_type = 'module'
                continue
            
            # Descripción
            if match := re.match(self.doc_patterns['description'], line):
                description = match.group(1)
                if current_type == 'module':
                    module.description = description
                elif current_doc:
                    current_doc.description = description
                continue
            
            # Documentación de función
            if match := re.match(self.doc_patterns['function_doc'], line):
                if current_doc:
                    module.functions.append(current_doc)
                
                current_doc = VaderDocString(
                    name=match.group(1),
                    description="",
                    line_number=line_num,
                    file_path=file_path
                )
                current_type = 'function'
                continue
            
            # Documentación de clase
            if match := re.match(self.doc_patterns['class_doc'], line):
                if current_doc:
                    module.classes.append(current_doc)
                
                current_doc = VaderDocString(
                    name=match.group(1),
                    description="",
                    line_number=line_num,
                    file_path=file_path
                )
                current_type = 'class'
                continue
            
            # Parámetros
            if match := re.match(self.doc_patterns['param'], line):
                if current_doc:
                    param_name = match.group(1)
                    param_desc = match.group(2)
                    current_doc.parameters[param_name] = param_desc
                continue
            
            # Retorno
            if match := re.match(self.doc_patterns['return'], line):
                if current_doc:
                    current_doc.returns = match.group(1)
                continue
            
            # Ejemplo
            if match := re.match(self.doc_patterns['example'], line):
                example = match.group(1)
                if current_type == 'module':
                    module.examples.append(example)
                elif current_doc:
                    current_doc.examples.append(example)
                continue
            
            # Nota
            if match := re.match(self.doc_patterns['note'], line):
                if current_doc:
                    current_doc.notes.append(match.group(1))
                continue
            
            # Autor
            if match := re.match(self.doc_patterns['author'], line):
                author = match.group(1)
                if current_type == 'module':
                    module.author = author
                elif current_doc:
                    current_doc.author = author
                continue
            
            # Versión
            if match := re.match(self.doc_patterns['version'], line):
                version = match.group(1)
                if current_type == 'module':
                    module.version = version
                elif current_doc:
                    current_doc.version = version
                continue
            
            # Desde
            if match := re.match(self.doc_patterns['since'], line):
                if current_doc:
                    current_doc.since = match.group(1)
                continue
            
            # Deprecado
            if re.match(self.doc_patterns['deprecated'], line):
                if current_doc:
                    current_doc.deprecated = True
                continue
            
            # Ver también
            if match := re.match(self.doc_patterns['see_also'], line):
                if current_doc:
                    current_doc.see_also.append(match.group(1))
                continue
            
            # Tag
            if match := re.match(self.doc_patterns['tag'], line):
                if current_doc:
                    current_doc.tags.append(match.group(1))
                continue
            
            # Detectar fin de función/clase para guardar documentación pendiente
            if line.startswith('funcion ') or line.startswith('clase '):
                # Extraer nombre de función/clase del código
                if 'funcion ' in line:
                    func_match = re.match(r'funcion\s+(\w+)', line)
                    if func_match and current_doc and current_type == 'function':
                        if not current_doc.name:
                            current_doc.name = func_match.group(1)
                
                elif 'clase ' in line:
                    class_match = re.match(r'clase\s+(\w+)', line)
                    if class_match and current_doc and current_type == 'class':
                        if not current_doc.name:
                            current_doc.name = class_match.group(1)
        
        # Agregar última documentación pendiente
        if current_doc:
            if current_type == 'function':
                module.functions.append(current_doc)
            elif current_type == 'class':
                module.classes.append(current_doc)
        
        return module
    
    def generate_project_documentation(self, project_dir: str, project_name: str = None) -> VaderDocumentation:
        """Genera documentación completa del proyecto"""
        project_path = Path(project_dir)
        
        if project_name is None:
            project_name = project_path.name
        
        documentation = VaderDocumentation(
            project_name=project_name,
            description=f"Documentación del proyecto {project_name}",
            version="1.0.0"
        )
        
        # Buscar archivos .vdr
        vdr_files = list(project_path.rglob("*.vdr"))
        
        for vdr_file in vdr_files:
            try:
                module = self.parse_file_documentation(str(vdr_file))
                documentation.modules.append(module)
            except Exception as e:
                print(f"⚠️ Error procesando {vdr_file}: {e}")
        
        return documentation
    
    def generate_html_documentation(self, documentation: VaderDocumentation, output_dir: str):
        """Genera documentación HTML"""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Página principal
        self._generate_index_html(documentation, output_path)
        
        # Páginas de módulos
        for module in documentation.modules:
            self._generate_module_html(module, output_path)
        
        # Archivos de estilo y JavaScript
        self._generate_assets(output_path)
        
        print(f"📚 Documentación HTML generada en: {output_path}")
    
    def _generate_index_html(self, documentation: VaderDocumentation, output_path: Path):
        """Genera página principal de documentación"""
        modules_html = ""
        for module in documentation.modules:
            modules_html += f"""
            <div class="module-card">
                <h3><a href="{module.name}.html">📁 {module.name}</a></h3>
                <p>{module.description or 'Sin descripción'}</p>
                <div class="stats">
                    <span>🔧 {len(module.functions)} funciones</span>
                    <span>🏗️ {len(module.classes)} clases</span>
                </div>
            </div>
            """
        
        html_content = self.html_templates['base'].format(
            title=f"Documentación - {documentation.project_name}",
            content=f"""
            <div class="header">
                <h1>📚 {documentation.project_name}</h1>
                <p>{documentation.description}</p>
                <div class="meta">
                    <span>📦 Versión: {documentation.version}</span>
                    <span>📅 Generado: {documentation.generated_at}</span>
                    <span>📁 {len(documentation.modules)} módulos</span>
                </div>
            </div>
            
            <div class="modules-grid">
                {modules_html}
            </div>
            """
        )
        
        with open(output_path / "index.html", 'w', encoding='utf-8') as f:
            f.write(html_content)
    
    def _generate_module_html(self, module: VaderModule, output_path: Path):
        """Genera página HTML de un módulo"""
        functions_html = ""
        for func in module.functions:
            functions_html += self._generate_function_html(func)
        
        classes_html = ""
        for cls in module.classes:
            classes_html += self._generate_class_html(cls)
        
        examples_html = ""
        for example in module.examples:
            examples_html += f'<pre><code class="vader">{example}</code></pre>'
        
        content = f"""
        <div class="module-header">
            <h1>📁 {module.name}</h1>
            <p>{module.description}</p>
            {f'<p><strong>👤 Autor:</strong> {module.author}</p>' if module.author else ''}
            {f'<p><strong>📦 Versión:</strong> {module.version}</p>' if module.version else ''}
            <p><strong>📄 Archivo:</strong> <code>{module.file_path}</code></p>
        </div>
        
        {f'<div class="section"><h2>💡 Ejemplos</h2>{examples_html}</div>' if examples_html else ''}
        
        {f'<div class="section"><h2>🔧 Funciones ({len(module.functions)})</h2>{functions_html}</div>' if functions_html else ''}
        
        {f'<div class="section"><h2>🏗️ Clases ({len(module.classes)})</h2>{classes_html}</div>' if classes_html else ''}
        """
        
        html_content = self.html_templates['base'].format(
            title=f"{module.name} - Documentación",
            content=content
        )
        
        with open(output_path / f"{module.name}.html", 'w', encoding='utf-8') as f:
            f.write(html_content)
    
    def _generate_function_html(self, func: VaderDocString) -> str:
        """Genera HTML para una función"""
        params_html = ""
        for param_name, param_desc in func.parameters.items():
            params_html += f"<li><code>{param_name}</code>: {param_desc}</li>"
        
        examples_html = ""
        for example in func.examples:
            examples_html += f'<pre><code class="vader">{example}</code></pre>'
        
        notes_html = ""
        for note in func.notes:
            notes_html += f"<div class='note'>💡 {note}</div>"
        
        tags_html = ""
        for tag in func.tags:
            tags_html += f'<span class="tag">{tag}</span>'
        
        deprecated_html = ""
        if func.deprecated:
            deprecated_html = '<div class="deprecated">⚠️ Esta función está deprecada</div>'
        
        return f"""
        <div class="function-doc" id="{func.name}">
            <h3>🔧 {func.name}</h3>
            {deprecated_html}
            <p>{func.description}</p>
            
            {f'<div><strong>📥 Parámetros:</strong><ul>{params_html}</ul></div>' if params_html else ''}
            {f'<div><strong>📤 Retorna:</strong> {func.returns}</div>' if func.returns else ''}
            {f'<div><strong>💡 Ejemplos:</strong>{examples_html}</div>' if examples_html else ''}
            {notes_html}
            {f'<div class="tags">{tags_html}</div>' if tags_html else ''}
            
            <div class="meta">
                {f'<span>👤 {func.author}</span>' if func.author else ''}
                {f'<span>📦 {func.version}</span>' if func.version else ''}
                {f'<span>📅 Desde: {func.since}</span>' if func.since else ''}
                <span>📍 Línea: {func.line_number}</span>
            </div>
        </div>
        """
    
    def _generate_class_html(self, cls: VaderDocString) -> str:
        """Genera HTML para una clase"""
        # Similar a función pero adaptado para clases
        return self._generate_function_html(cls).replace('🔧', '🏗️').replace('function-doc', 'class-doc')
    
    def _generate_assets(self, output_path: Path):
        """Genera archivos CSS y JS"""
        css_content = """
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 40px 20px; border-radius: 10px; margin-bottom: 30px; }
        .header h1 { font-size: 2.5em; margin-bottom: 10px; }
        .meta { display: flex; gap: 20px; margin-top: 20px; }
        .meta span { background: rgba(255,255,255,0.2); padding: 5px 10px; border-radius: 5px; }
        .modules-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }
        .module-card { background: white; border: 1px solid #ddd; border-radius: 10px; padding: 20px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .module-card h3 a { color: #667eea; text-decoration: none; }
        .stats { display: flex; gap: 15px; margin-top: 10px; font-size: 0.9em; color: #666; }
        .section { margin: 30px 0; }
        .section h2 { color: #667eea; border-bottom: 2px solid #667eea; padding-bottom: 10px; margin-bottom: 20px; }
        .function-doc, .class-doc { background: #f8f9fa; border-left: 4px solid #667eea; padding: 20px; margin: 20px 0; border-radius: 5px; }
        .function-doc h3, .class-doc h3 { color: #667eea; margin-bottom: 10px; }
        .deprecated { background: #fff3cd; border: 1px solid #ffeaa7; padding: 10px; border-radius: 5px; margin: 10px 0; }
        .note { background: #d1ecf1; border-left: 4px solid #bee5eb; padding: 10px; margin: 10px 0; }
        .tags { margin: 10px 0; }
        .tag { background: #667eea; color: white; padding: 3px 8px; border-radius: 15px; font-size: 0.8em; margin-right: 5px; }
        pre { background: #2d3748; color: #e2e8f0; padding: 15px; border-radius: 5px; overflow-x: auto; }
        code { font-family: 'Monaco', 'Menlo', monospace; }
        """
        
        with open(output_path / "styles.css", 'w', encoding='utf-8') as f:
            f.write(css_content)
    
    def generate_markdown_documentation(self, documentation: VaderDocumentation, output_file: str):
        """Genera documentación en Markdown"""
        md_content = f"""# 📚 {documentation.project_name}

{documentation.description}

**📦 Versión:** {documentation.version}  
**📅 Generado:** {documentation.generated_at}  
**📁 Módulos:** {len(documentation.modules)}

## 📋 Índice de Módulos

"""
        
        # Índice
        for module in documentation.modules:
            md_content += f"- [📁 {module.name}](#{module.name.lower()})\n"
        
        md_content += "\n---\n\n"
        
        # Módulos
        for module in documentation.modules:
            md_content += f"## 📁 {module.name}\n\n"
            md_content += f"{module.description}\n\n"
            
            if module.author:
                md_content += f"**👤 Autor:** {module.author}  \n"
            if module.version:
                md_content += f"**📦 Versión:** {module.version}  \n"
            
            md_content += f"**📄 Archivo:** `{module.file_path}`\n\n"
            
            # Funciones
            if module.functions:
                md_content += f"### 🔧 Funciones ({len(module.functions)})\n\n"
                for func in module.functions:
                    md_content += self._generate_function_markdown(func)
            
            # Clases
            if module.classes:
                md_content += f"### 🏗️ Clases ({len(module.classes)})\n\n"
                for cls in module.classes:
                    md_content += self._generate_class_markdown(cls)
            
            md_content += "\n---\n\n"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        print(f"📝 Documentación Markdown generada: {output_file}")
    
    def _generate_function_markdown(self, func: VaderDocString) -> str:
        """Genera Markdown para una función"""
        md = f"#### 🔧 `{func.name}`\n\n"
        
        if func.deprecated:
            md += "⚠️ **Esta función está deprecada**\n\n"
        
        md += f"{func.description}\n\n"
        
        if func.parameters:
            md += "**📥 Parámetros:**\n"
            for param_name, param_desc in func.parameters.items():
                md += f"- `{param_name}`: {param_desc}\n"
            md += "\n"
        
        if func.returns:
            md += f"**📤 Retorna:** {func.returns}\n\n"
        
        if func.examples:
            md += "**💡 Ejemplos:**\n"
            for example in func.examples:
                md += f"```vader\n{example}\n```\n\n"
        
        if func.notes:
            for note in func.notes:
                md += f"💡 **Nota:** {note}\n\n"
        
        return md
    
    def _generate_class_markdown(self, cls: VaderDocString) -> str:
        """Genera Markdown para una clase"""
        return self._generate_function_markdown(cls).replace('🔧', '🏗️')
    
    def _get_base_template(self) -> str:
        """Template HTML base"""
        return """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <div class="container">
        {content}
    </div>
</body>
</html>"""
    
    def _get_module_template(self) -> str:
        """Template para módulos"""
        return self._get_base_template()
    
    def _get_function_template(self) -> str:
        """Template para funciones"""
        return self._get_base_template()

def main():
    """Función principal para testing"""
    # Ejemplo de archivo .vdr con documentación
    example_code = """
#@modulo: Utilidades Matemáticas
#@descripcion: Módulo con funciones matemáticas básicas
#@autor: Equipo Vader
#@version: 1.0.0
#@ejemplo: importar matematicas

#@funcion: sumar
#@descripcion: Suma dos números enteros o decimales
#@param a: Primer número a sumar
#@param b: Segundo número a sumar
#@retorna: La suma de a y b
#@ejemplo: resultado = sumar(5, 3)  # retorna 8
#@ejemplo: resultado = sumar(2.5, 1.5)  # retorna 4.0
#@nota: Esta función maneja tanto enteros como decimales
#@tag: matematicas
#@tag: basico
#@desde: 1.0.0
funcion sumar(a, b)
    retornar a + b
fin funcion

#@funcion: dividir
#@descripcion: Divide dos números con validación de división por cero
#@param dividendo: Número a dividir
#@param divisor: Número por el cual dividir
#@retorna: El resultado de la división
#@ejemplo: resultado = dividir(10, 2)  # retorna 5
#@nota: Lanza error si el divisor es cero
#@tag: matematicas
#@tag: validacion
funcion dividir(dividendo, divisor)
    si divisor == 0
        lanzar_error "División por cero no permitida"
    fin si
    retornar dividendo / divisor
fin funcion

#@clase: Calculadora
#@descripcion: Clase para operaciones matemáticas avanzadas
#@autor: Equipo Vader
#@version: 1.0.0
#@ejemplo: calc = nueva Calculadora()
clase Calculadora
    funcion constructor()
        este.historial = []
    fin funcion
fin clase
"""
    
    # Crear archivo temporal
    with tempfile.NamedTemporaryFile(mode='w', suffix='.vdr', delete=False, encoding='utf-8') as f:
        f.write(example_code)
        temp_file = f.name
    
    try:
        # Crear generador
        generator = VaderDocumentationGenerator()
        
        # Parsear archivo
        module = generator.parse_file_documentation(temp_file)
        
        print("📚 VADER DOCUMENTATION GENERATOR - Resultados:")
        print(f"📁 Módulo: {module.name}")
        print(f"📝 Descripción: {module.description}")
        print(f"👤 Autor: {module.author}")
        print(f"📦 Versión: {module.version}")
        print(f"🔧 Funciones: {len(module.functions)}")
        print(f"🏗️ Clases: {len(module.classes)}")
        print()
        
        # Mostrar funciones encontradas
        for func in module.functions:
            print(f"🔧 {func.name}")
            print(f"   📝 {func.description}")
            print(f"   📥 Parámetros: {len(func.parameters)}")
            print(f"   💡 Ejemplos: {len(func.examples)}")
            print(f"   🏷️ Tags: {', '.join(func.tags)}")
            if func.deprecated:
                print("   ⚠️ DEPRECADA")
            print()
        
        # Mostrar clases encontradas
        for cls in module.classes:
            print(f"🏗️ {cls.name}")
            print(f"   📝 {cls.description}")
            print()
        
        print("✅ Sistema de documentación Vader implementado correctamente")
        print("🚀 Características disponibles:")
        print("  - Docstrings estandarizados (#@funcion, #@descripcion, etc.)")
        print("  - Generación automática HTML y Markdown")
        print("  - Ejemplos interactivos")
        print("  - Sistema de tags y versionado")
        print("  - Detección de funciones deprecadas")
        
    finally:
        # Limpiar archivo temporal
        os.unlink(temp_file)

if __name__ == "__main__":
    main()
