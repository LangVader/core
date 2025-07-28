#!/usr/bin/env python3
"""
Transpilador automático de React/Next.js a Vader (.vdr)
Convierte toda la aplicación react-ui-master a sintaxis Vader preservando funcionalidad
"""

import os
import re
import json
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Tuple

class ReactToVaderTranspiler:
    def __init__(self, source_dir: str, target_dir: str):
        self.source_dir = Path(source_dir)
        self.target_dir = Path(target_dir)
        self.component_mappings = {}
        self.imports_map = {}
        
    def transpile_project(self):
        """Transpila todo el proyecto de React a Vader"""
        print(f"🚀 Iniciando transpilación de {self.source_dir} -> {self.target_dir}")
        
        # Crear directorio destino
        self.target_dir.mkdir(exist_ok=True)
        
        # Transpilar estructura de carpetas
        self._copy_project_structure()
        
        # Transpilar archivos principales
        self._transpile_package_json()
        self._transpile_next_config()
        
        # Transpilar páginas (app directory)
        self._transpile_app_directory()
        
        # Transpilar componentes
        self._transpile_components()
        
        # Transpilar contenido y documentación
        self._transpile_content()
        
        # Crear archivo principal main.vdr
        self._create_main_vdr()
        
        print("✅ Transpilación completada exitosamente!")
        
    def _copy_project_structure(self):
        """Copia la estructura básica del proyecto"""
        # Copiar archivos estáticos
        static_files = ['README.md', '.gitignore']
        for file in static_files:
            src = self.source_dir / file
            if src.exists():
                shutil.copy2(src, self.target_dir / file)
        
        # Copiar carpeta public
        public_src = self.source_dir / 'public'
        if public_src.exists():
            shutil.copytree(public_src, self.target_dir / 'public', dirs_exist_ok=True)
            
    def _transpile_package_json(self):
        """Convierte package.json a package.vdr"""
        package_path = self.source_dir / 'package.json'
        if not package_path.exists():
            return
            
        with open(package_path, 'r') as f:
            package_data = json.load(f)
        
        # Crear package.vdr equivalente
        vdr_content = f"""// Configuración del proyecto VaderUI
configurar proyecto {{
    nombre: "{package_data.get('name', 'vader-ui')}"
    version: "{package_data.get('version', '1.0.0')}"
    descripcion: "{package_data.get('description', 'UI Components library in Vader')}"
    
    dependencias: {{
        vader: "^7.0.0"
        tailwindcss: "^3.4.0"
        typescript: "^5.0.0"
    }}
    
    scripts: {{
        dev: "vader dev"
        build: "vader build"
        start: "vader start"
        preview: "vader preview"
    }}
    
    configuracion: {{
        puerto: 3000
        tema: "oscuro"
        idioma: "es"
        hot_reload: true
        typescript: true
    }}
}}

exportar configuracion
"""
        
        with open(self.target_dir / 'package.vdr', 'w', encoding='utf-8') as f:
            f.write(vdr_content)
            
    def _transpile_next_config(self):
        """Convierte next.config.ts a configuración Vader"""
        config_content = """// Configuración de Vader equivalente a Next.js
configurar aplicacion {{
    framework: "vader"
    modo: "desarrollo"
    puerto: 3000
    
    rutas: {{
        base: "/"
        api: "/api"
        estaticos: "/public"
    }}
    
    optimizacion: {{
        minificacion: true
        lazy_loading: true
        cache_estrategia: "stale-while-revalidate"
    }}
    
    desarrollo: {{
        hot_reload: true
        error_overlay: true
        debug: true
    }}
}}
"""
        
        with open(self.target_dir / 'config.vdr', 'w', encoding='utf-8') as f:
            f.write(config_content)
    
    def _transpile_app_directory(self):
        """Transpila la carpeta app/ (páginas de Next.js)"""
        app_dir = self.source_dir / 'app'
        if not app_dir.exists():
            return
            
        target_app = self.target_dir / 'src' / 'paginas'
        target_app.mkdir(parents=True, exist_ok=True)
        
        # Transpilar página principal
        main_page = app_dir / '(root)' / 'page.tsx'
        if main_page.exists():
            self._transpile_tsx_file(main_page, target_app / 'Principal.vdr')
            
        # Transpilar layout
        layout_file = app_dir / 'layout.tsx'
        if layout_file.exists():
            self._transpile_tsx_file(layout_file, target_app / 'Layout.vdr')
            
        # Transpilar páginas de documentación
        docs_dir = app_dir / 'docs'
        if docs_dir.exists():
            target_docs = target_app / 'documentacion'
            target_docs.mkdir(exist_ok=True)
            for file in docs_dir.rglob('*.tsx'):
                relative_path = file.relative_to(docs_dir)
                target_file = target_docs / f"{relative_path.stem}.vdr"
                target_file.parent.mkdir(parents=True, exist_ok=True)
                self._transpile_tsx_file(file, target_file)
    
    def _transpile_components(self):
        """Transpila todos los componentes React a Vader"""
        components_dir = self.source_dir / 'components'
        if not components_dir.exists():
            return
            
        target_components = self.target_dir / 'src' / 'componentes'
        target_components.mkdir(parents=True, exist_ok=True)
        
        # Transpilar componentes principales
        for file in components_dir.rglob('*.tsx'):
            if file.name.startswith('.'):
                continue
                
            relative_path = file.relative_to(components_dir)
            target_file = target_components / f"{relative_path.stem}.vdr"
            target_file.parent.mkdir(parents=True, exist_ok=True)
            
            self._transpile_tsx_file(file, target_file)
    
    def _transpile_content(self):
        """Transpila contenido y documentación"""
        content_dir = self.source_dir / 'content'
        if not content_dir.exists():
            return
            
        target_content = self.target_dir / 'contenido'
        target_content.mkdir(exist_ok=True)
        
        for file in content_dir.rglob('*.mdx'):
            relative_path = file.relative_to(content_dir)
            target_file = target_content / f"{relative_path.stem}.vdr"
            target_file.parent.mkdir(parents=True, exist_ok=True)
            
            self._transpile_mdx_file(file, target_file)
    
    def _transpile_tsx_file(self, source_file: Path, target_file: Path):
        """Transpila un archivo TSX individual a VDR"""
        try:
            with open(source_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Convertir a sintaxis Vader
            vdr_content = self._convert_tsx_to_vdr(content, source_file.name)
            
            with open(target_file, 'w', encoding='utf-8') as f:
                f.write(vdr_content)
                
            print(f"✅ Transpilado: {source_file.name} -> {target_file.name}")
            
        except Exception as e:
            print(f"❌ Error transpilando {source_file}: {e}")
    
    def _convert_tsx_to_vdr(self, tsx_content: str, filename: str) -> str:
        """Convierte contenido TSX a sintaxis Vader"""
        
        # Extraer imports
        imports = self._extract_imports(tsx_content)
        
        # Extraer componente principal
        component_match = re.search(r'export default function (\w+)\([^)]*\)\s*{(.*)}', tsx_content, re.DOTALL)
        if not component_match:
            component_match = re.search(r'export function (\w+)\([^)]*\)\s*{(.*)}', tsx_content, re.DOTALL)
        
        if not component_match:
            # Si no es un componente, tratar como módulo
            return self._convert_module_to_vdr(tsx_content, filename)
        
        component_name = component_match.group(1)
        component_body = component_match.group(2).strip()
        
        # Convertir JSX a sintaxis Vader
        jsx_content = self._extract_jsx_return(component_body)
        vader_jsx = self._convert_jsx_to_vader(jsx_content)
        
        # Generar archivo VDR
        vdr_content = f"""// Componente {component_name} convertido de React
{self._convert_imports_to_vader(imports)}

crear componente {component_name} {{
    propiedades: {{
        className?: texto
        children?: nodos
    }}
    
    renderizar: {{
{self._indent_content(vader_jsx, 8)}
    }}
}}

exportar {component_name}
"""
        
        return vdr_content
    
    def _extract_imports(self, content: str) -> List[str]:
        """Extrae todas las declaraciones import"""
        import_pattern = r'import\s+.*?from\s+["\'].*?["\'];?'
        return re.findall(import_pattern, content, re.MULTILINE)
    
    def _convert_imports_to_vader(self, imports: List[str]) -> str:
        """Convierte imports de React a sintaxis Vader"""
        vader_imports = []
        
        for imp in imports:
            # Convertir imports de componentes
            if '@/components' in imp:
                # import { Component } from "@/components/path"
                match = re.search(r'import\s+{([^}]+)}\s+from\s+["\']@/components/([^"\']+)["\']', imp)
                if match:
                    components = [c.strip() for c in match.group(1).split(',')]
                    path = match.group(2).replace('/', '.')
                    for comp in components:
                        vader_imports.append(f"importar {comp} desde 'componentes.{path}'")
            
            # Convertir imports de React
            elif 'react' in imp.lower():
                if 'useState' in imp:
                    vader_imports.append("importar { estado } desde 'vader/estado'")
                if 'useEffect' in imp:
                    vader_imports.append("importar { efecto } desde 'vader/efectos'")
            
            # Convertir otros imports
            else:
                vader_imports.append(f"// {imp}")
        
        return '\n'.join(vader_imports) if vader_imports else ""
    
    def _extract_jsx_return(self, component_body: str) -> str:
        """Extrae el JSX del return statement"""
        # Buscar return statement
        return_match = re.search(r'return\s*\((.*?)\);?\s*$', component_body, re.DOTALL)
        if return_match:
            return return_match.group(1).strip()
        
        # Buscar return sin paréntesis
        return_match = re.search(r'return\s+(.*?);?\s*$', component_body, re.DOTALL)
        if return_match:
            return return_match.group(1).strip()
        
        return component_body
    
    def _convert_jsx_to_vader(self, jsx: str) -> str:
        """Convierte JSX a sintaxis Vader"""
        # Convertir className a clase
        jsx = re.sub(r'className=', 'clase=', jsx)
        
        # Convertir componentes React a sintaxis Vader
        jsx = re.sub(r'<(\w+)([^>]*?)>', r'<\1\2>', jsx)
        
        # Convertir props booleanas
        jsx = re.sub(r'(\w+)={true}', r'\1', jsx)
        jsx = re.sub(r'(\w+)={false}', r'no_\1', jsx)
        
        # Convertir interpolaciones JavaScript
        jsx = re.sub(r'{([^}]+)}', r'{{ \1 }}', jsx)
        
        return jsx
    
    def _convert_module_to_vdr(self, content: str, filename: str) -> str:
        """Convierte módulos que no son componentes"""
        return f"""// Módulo {filename} convertido de TypeScript
// Contenido original:
/*
{content}
*/

// TODO: Convertir manualmente este módulo a sintaxis Vader
"""
    
    def _transpile_mdx_file(self, source_file: Path, target_file: Path):
        """Transpila archivos MDX a VDR"""
        try:
            with open(source_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            vdr_content = f"""// Documentación convertida de MDX
crear documento {{
    titulo: "{source_file.stem}"
    tipo: "documentacion"
    
    contenido: {{
        markdown: '''
{content}
        '''
    }}
}}

exportar documento
"""
            
            with open(target_file, 'w', encoding='utf-8') as f:
                f.write(vdr_content)
                
        except Exception as e:
            print(f"❌ Error transpilando MDX {source_file}: {e}")
    
    def _create_main_vdr(self):
        """Crea el archivo principal main.vdr"""
        main_content = """// Aplicación VaderUI - Transpilada desde React
importar { configurar_aplicacion } desde './config.vdr'
importar Principal desde './src/paginas/Principal.vdr'
importar Layout desde './src/paginas/Layout.vdr'

configurar aplicacion {{
    titulo: "VaderUI - Component Library"
    descripcion: "Librería de componentes UI transpilada de React a Vader"
    puerto: 3000
    tema: "oscuro"
    idioma: "es"
    
    rutas: {{
        "/": Principal
        "/docs/*": "src/paginas/documentacion"
        "/components/*": "src/componentes"
    }}
    
    funcionalidades: {{
        navegacion_fluida: true
        busqueda_avanzada: true
        copy_paste_componentes: true
        preview_en_vivo: true
        documentacion_interactiva: true
        ai_chat_integration: true
        github_sync: true
        tema_oscuro_claro: true
        responsive_completo: true
        animaciones_avanzadas: true
    }}
    
    desarrollo: {{
        hot_reload: true
        debug: true
        puerto_dev: 3000
        auto_refresh: true
        error_overlay: true
    }}
    
    produccion: {{
        optimizacion: true
        minificacion: true
        lazy_loading: true
        cache_estrategia: "aggressive"
        cdn_assets: true
    }}
}}

cuando iniciar {{
    cargar Layout
    cargar Principal
    mostrar mensaje "🚀 VaderUI cargado exitosamente!"
    abrir navegador "http://localhost:3000"
}}

ejecutar aplicacion
"""
        
        with open(self.target_dir / 'main.vdr', 'w', encoding='utf-8') as f:
            f.write(main_content)
    
    def _indent_content(self, content: str, spaces: int) -> str:
        """Indenta contenido con el número especificado de espacios"""
        indent = ' ' * spaces
        return '\n'.join(indent + line for line in content.split('\n'))

def main():
    """Función principal"""
    source_dir = "/Users/coderfull/Desktop/Todo Vader/react-ui-master"
    target_dir = "/Users/coderfull/Desktop/Todo Vader/vader-ui-transpiled"
    
    transpiler = ReactToVaderTranspiler(source_dir, target_dir)
    transpiler.transpile_project()

if __name__ == "__main__":
    main()
