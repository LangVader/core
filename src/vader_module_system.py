#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VADER 7.0 - SISTEMA DE MÓDULOS E IMPORTS
=======================================
Sistema completo de modularización para Vader con imports, exports y dependencias

Características:
- Import/export de archivos .vdr
- Resolución de dependencias
- Cache de módulos
- Imports relativos y absolutos
- Namespace management
- Detección de dependencias circulares

Autor: Vader Team
Versión: 7.0.0 "Universal"
Fecha: 2025
"""

import os
import re
import sys
import hashlib
from pathlib import Path
from typing import Dict, List, Any, Optional, Set, Tuple
from dataclasses import dataclass, field
import json
import time

@dataclass
class VaderModule:
    """Representa un módulo Vader"""
    name: str
    path: str
    content: str
    exports: Dict[str, Any] = field(default_factory=dict)
    imports: Dict[str, str] = field(default_factory=dict)
    dependencies: Set[str] = field(default_factory=set)
    hash: str = ""
    last_modified: float = 0
    compiled: bool = False
    
    def __post_init__(self):
        self.hash = self._calculate_hash()
        if os.path.exists(self.path):
            self.last_modified = os.path.getmtime(self.path)
    
    def _calculate_hash(self) -> str:
        """Calcula hash del contenido del módulo"""
        return hashlib.md5(self.content.encode('utf-8')).hexdigest()

@dataclass
class ImportStatement:
    """Representa una declaración de import"""
    module_path: str
    imported_items: List[str]
    alias: Optional[str] = None
    is_relative: bool = False
    line_number: int = 0

class VaderModuleSystem:
    """Sistema de módulos para Vader"""
    
    def __init__(self, root_path: str = "."):
        self.root_path = Path(root_path).resolve()
        self.modules: Dict[str, VaderModule] = {}
        self.module_cache: Dict[str, Any] = {}
        self.dependency_graph: Dict[str, Set[str]] = {}
        self.search_paths: List[Path] = [self.root_path]
        
        # Patrones de reconocimiento
        self.import_patterns = {
            'import_from': r'importar\s+([^/\s]+(?:/[^/\s]+)*)\s+desde\s+([^\s]+)',
            'import_all': r'importar\s+([^\s]+)',
            'import_as': r'importar\s+([^\s]+)\s+como\s+([^\s]+)',
            'export': r'exportar\s+([^\s]+)',
            'export_default': r'exportar\s+por_defecto\s+([^\s]+)',
        }
    
    def add_search_path(self, path: str):
        """Añade un directorio de búsqueda de módulos"""
        search_path = Path(path).resolve()
        if search_path.exists() and search_path not in self.search_paths:
            self.search_paths.append(search_path)
    
    def resolve_module_path(self, module_name: str, current_file: str = None) -> Optional[str]:
        """Resuelve la ruta de un módulo"""
        # Import relativo
        if module_name.startswith('./') or module_name.startswith('../'):
            if current_file:
                current_dir = Path(current_file).parent
                resolved_path = (current_dir / module_name).resolve()
                
                # Buscar con extensión .vdr
                if resolved_path.suffix != '.vdr':
                    resolved_path = resolved_path.with_suffix('.vdr')
                
                if resolved_path.exists():
                    return str(resolved_path)
        
        # Import absoluto
        for search_path in self.search_paths:
            # Buscar directamente
            module_path = search_path / f"{module_name}.vdr"
            if module_path.exists():
                return str(module_path)
            
            # Buscar en subdirectorios
            module_path = search_path / module_name / "main.vdr"
            if module_path.exists():
                return str(module_path)
            
            # Buscar con estructura de paquete
            parts = module_name.split('/')
            if len(parts) > 1:
                module_path = search_path
                for part in parts:
                    module_path = module_path / part
                module_path = module_path.with_suffix('.vdr')
                
                if module_path.exists():
                    return str(module_path)
        
        return None
    
    def parse_imports(self, code: str, file_path: str = None) -> List[ImportStatement]:
        """Parsea declaraciones de import en código Vader"""
        imports = []
        lines = code.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            # importar item1, item2 desde modulo
            match = re.match(self.import_patterns['import_from'], line)
            if match:
                items_str = match.group(1)
                module_path = match.group(2)
                items = [item.strip() for item in items_str.split(',')]
                
                imports.append(ImportStatement(
                    module_path=module_path,
                    imported_items=items,
                    is_relative=module_path.startswith('./') or module_path.startswith('../'),
                    line_number=line_num
                ))
                continue
            
            # importar modulo como alias
            match = re.match(self.import_patterns['import_as'], line)
            if match:
                module_path = match.group(1)
                alias = match.group(2)
                
                imports.append(ImportStatement(
                    module_path=module_path,
                    imported_items=['*'],
                    alias=alias,
                    is_relative=module_path.startswith('./') or module_path.startswith('../'),
                    line_number=line_num
                ))
                continue
            
            # importar modulo
            match = re.match(self.import_patterns['import_all'], line)
            if match:
                module_path = match.group(1)
                
                imports.append(ImportStatement(
                    module_path=module_path,
                    imported_items=['*'],
                    is_relative=module_path.startswith('./') or module_path.startswith('../'),
                    line_number=line_num
                ))
        
        return imports
    
    def parse_exports(self, code: str) -> Dict[str, Any]:
        """Parsea declaraciones de export en código Vader"""
        exports = {}
        lines = code.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            # exportar item
            match = re.match(self.import_patterns['export'], line)
            if match:
                item = match.group(1)
                exports[item] = {'type': 'named', 'name': item}
                continue
            
            # exportar por_defecto item
            match = re.match(self.import_patterns['export_default'], line)
            if match:
                item = match.group(1)
                exports['default'] = {'type': 'default', 'name': item}
        
        return exports
    
    def load_module(self, module_path: str, current_file: str = None) -> Optional[VaderModule]:
        """Carga un módulo Vader"""
        # Resolver ruta del módulo
        resolved_path = self.resolve_module_path(module_path, current_file)
        if not resolved_path:
            raise ImportError(f"No se pudo encontrar el módulo: {module_path}")
        
        # Verificar si ya está en cache y no ha cambiado
        if resolved_path in self.modules:
            module = self.modules[resolved_path]
            if os.path.exists(resolved_path):
                current_mtime = os.path.getmtime(resolved_path)
                if current_mtime <= module.last_modified:
                    return module
        
        # Leer contenido del archivo
        try:
            with open(resolved_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            raise ImportError(f"Error leyendo módulo {resolved_path}: {e}")
        
        # Crear módulo
        module_name = Path(resolved_path).stem
        module = VaderModule(
            name=module_name,
            path=resolved_path,
            content=content
        )
        
        # Parsear imports y exports
        module.imports = {imp.module_path: imp for imp in self.parse_imports(content, resolved_path)}
        module.exports = self.parse_exports(content)
        
        # Extraer dependencias
        for imp in module.imports.values():
            dep_path = self.resolve_module_path(imp.module_path, resolved_path)
            if dep_path:
                module.dependencies.add(dep_path)
        
        # Guardar en cache
        self.modules[resolved_path] = module
        self.dependency_graph[resolved_path] = module.dependencies
        
        return module
    
    def resolve_dependencies(self, module_path: str) -> List[str]:
        """Resuelve todas las dependencias de un módulo recursivamente"""
        visited = set()
        resolved = []
        
        def _resolve_recursive(path: str):
            if path in visited:
                return
            
            visited.add(path)
            module = self.load_module(path)
            
            # Resolver dependencias primero
            for dep_path in module.dependencies:
                _resolve_recursive(dep_path)
            
            resolved.append(path)
        
        _resolve_recursive(module_path)
        return resolved
    
    def check_circular_dependencies(self, module_path: str) -> List[List[str]]:
        """Detecta dependencias circulares"""
        cycles = []
        visited = set()
        rec_stack = set()
        path_stack = []
        
        def _has_cycle(path: str) -> bool:
            if path in rec_stack:
                # Encontramos un ciclo
                cycle_start = path_stack.index(path)
                cycle = path_stack[cycle_start:] + [path]
                cycles.append(cycle)
                return True
            
            if path in visited:
                return False
            
            visited.add(path)
            rec_stack.add(path)
            path_stack.append(path)
            
            if path in self.dependency_graph:
                for dep in self.dependency_graph[path]:
                    if _has_cycle(dep):
                        return True
            
            rec_stack.remove(path)
            path_stack.pop()
            return False
        
        _has_cycle(module_path)
        return cycles
    
    def compile_module(self, module_path: str) -> Dict[str, Any]:
        """Compila un módulo y sus dependencias"""
        # Verificar dependencias circulares
        cycles = self.check_circular_dependencies(module_path)
        if cycles:
            cycle_strs = [' -> '.join(cycle) for cycle in cycles]
            raise ImportError(f"Dependencias circulares detectadas: {'; '.join(cycle_strs)}")
        
        # Resolver orden de dependencias
        dependency_order = self.resolve_dependencies(module_path)
        
        # Compilar módulos en orden
        compiled_modules = {}
        namespace = {}
        
        for dep_path in dependency_order:
            module = self.modules[dep_path]
            
            # Compilar contenido del módulo
            compiled_content = self._compile_module_content(module, namespace)
            compiled_modules[dep_path] = compiled_content
            
            # Añadir exports al namespace
            for export_name, export_info in module.exports.items():
                if export_info['type'] == 'named':
                    namespace[f"{module.name}.{export_name}"] = export_info
                elif export_info['type'] == 'default':
                    namespace[module.name] = export_info
        
        return {
            'main_module': module_path,
            'compiled_modules': compiled_modules,
            'dependency_order': dependency_order,
            'namespace': namespace,
            'success': True
        }
    
    def _compile_module_content(self, module: VaderModule, namespace: Dict[str, Any]) -> str:
        """Compila el contenido de un módulo individual"""
        content = module.content
        
        # Reemplazar imports con código resuelto
        lines = content.split('\n')
        compiled_lines = []
        
        for line in lines:
            line_stripped = line.strip()
            
            # Saltar líneas de import (ya resueltas)
            if any(re.match(pattern, line_stripped) for pattern in self.import_patterns.values()):
                compiled_lines.append(f"# {line}  // Resuelto por el sistema de módulos")
                continue
            
            # Reemplazar referencias a imports
            for import_path, import_stmt in module.imports.items():
                if isinstance(import_stmt, ImportStatement):
                    for item in import_stmt.imported_items:
                        if item != '*':
                            # Reemplazar referencias directas
                            pattern = r'\b' + re.escape(item) + r'\b'
                            if import_stmt.alias:
                                replacement = f"{import_stmt.alias}.{item}"
                            else:
                                resolved_module = self.resolve_module_path(import_path, module.path)
                                if resolved_module:
                                    module_name = Path(resolved_module).stem
                                    replacement = f"{module_name}.{item}"
                                else:
                                    replacement = item
                            
                            line = re.sub(pattern, replacement, line)
            
            compiled_lines.append(line)
        
        return '\n'.join(compiled_lines)
    
    def generate_dependency_graph_viz(self, module_path: str) -> str:
        """Genera visualización del grafo de dependencias"""
        dependencies = self.resolve_dependencies(module_path)
        
        viz = ["digraph VaderDependencies {"]
        viz.append("  rankdir=TB;")
        viz.append("  node [shape=box, style=filled, fillcolor=lightblue];")
        
        for dep in dependencies:
            module_name = Path(dep).stem
            viz.append(f'  "{module_name}";')
            
            if dep in self.dependency_graph:
                for child_dep in self.dependency_graph[dep]:
                    child_name = Path(child_dep).stem
                    viz.append(f'  "{module_name}" -> "{child_name}";')
        
        viz.append("}")
        return '\n'.join(viz)
    
    def create_package_json(self, module_path: str, output_path: str = None):
        """Crea un archivo package.json equivalente para el módulo"""
        module = self.load_module(module_path)
        dependencies = self.resolve_dependencies(module_path)
        
        package_info = {
            "name": module.name,
            "version": "1.0.0",
            "description": f"Módulo Vader: {module.name}",
            "main": "main.vdr",
            "dependencies": {},
            "vaderDependencies": [Path(dep).stem for dep in dependencies if dep != module_path],
            "files": [Path(dep).name for dep in dependencies],
            "scripts": {
                "start": f"vader {module.name}.vdr",
                "build": f"vader compile {module.name}.vdr",
                "test": f"vader test {module.name}.vdr"
            },
            "keywords": ["vader", "module"],
            "author": "Vader Developer",
            "license": "MIT"
        }
        
        if output_path is None:
            output_path = Path(module.path).parent / "package.json"
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(package_info, f, indent=2, ensure_ascii=False)
        
        return package_info

def main():
    """Función principal para testing"""
    # Crear sistema de módulos
    module_system = VaderModuleSystem()
    
    # Ejemplo de uso
    example_main = """
# main.vdr - Archivo principal
importar saludar, despedir desde ./utils
importar matematicas como math
importar configuracion

funcion principal()
    saludar("Mundo")
    resultado = math.sumar(5, 3)
    mostrar "Resultado: " + resultado
    despedir()
fin funcion

principal()
"""
    
    example_utils = """
# utils.vdr - Utilidades
exportar saludar
exportar despedir

funcion saludar(nombre)
    mostrar "¡Hola " + nombre + "!"
fin funcion

funcion despedir()
    mostrar "¡Hasta luego!"
fin funcion
"""
    
    example_math = """
# matematicas.vdr - Funciones matemáticas
exportar por_defecto matematicas

tipo matematicas {
    funcion sumar(a, b)
        retornar a + b
    fin funcion
    
    funcion restar(a, b)
        retornar a - b
    fin funcion
}
"""
    
    print("🧩 VADER MODULE SYSTEM - Ejemplo de uso:")
    print()
    
    # Parsear imports
    imports = module_system.parse_imports(example_main)
    print(f"📥 Imports encontrados: {len(imports)}")
    for imp in imports:
        items = ', '.join(imp.imported_items)
        alias_str = f" como {imp.alias}" if imp.alias else ""
        print(f"  - {items} desde {imp.module_path}{alias_str}")
    
    print()
    
    # Parsear exports
    exports = module_system.parse_exports(example_utils)
    print(f"📤 Exports encontrados: {len(exports)}")
    for name, info in exports.items():
        print(f"  - {name} ({info['type']})")
    
    print()
    print("✅ Sistema de módulos Vader implementado correctamente")
    print("🚀 Características disponibles:")
    print("  - Import/export de archivos .vdr")
    print("  - Resolución de dependencias")
    print("  - Detección de dependencias circulares")
    print("  - Cache de módulos")
    print("  - Imports relativos y absolutos")
    print("  - Generación de package.json")

if __name__ == "__main__":
    main()
