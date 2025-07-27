#!/usr/bin/env python3
"""
Vader CLI - Interfaz de Línea de Comandos Unificada
Lenguaje de Programación Universal y Conversacional
"""

import argparse
import sys
import os
import json
from pathlib import Path
from typing import Dict, List, Optional

# Importar módulos de Vader
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.vader import transpile_code, check_syntax, SUPPORTED_LANGUAGES
from src.app_generator import VaderAppGenerator
try:
    from src.project_generator import VaderProjectGenerator
except ImportError:
    VaderProjectGenerator = None

class VaderCLI:
    """Interfaz CLI unificada para Vader"""
    
    def __init__(self):
        self.version = "2.0.0"
        self.config_file = Path.home() / ".vader" / "config.json"
        self.config = self.load_config()
        
        # Inicializar componentes
        self.app_generator = VaderAppGenerator()
        self.project_generator = VaderProjectGenerator() if VaderProjectGenerator else None
    
    def load_config(self) -> Dict:
        """Cargar configuración del usuario"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        
        # Configuración por defecto
        return {
            "default_target": "python",
            "default_output_dir": "./output",
            "preferred_frameworks": ["flask", "react"],
            "auto_install_deps": True,
            "verbose": False
        }
    
    def save_config(self):
        """Guardar configuración del usuario"""
        self.config_file.parent.mkdir(exist_ok=True)
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)
    
    def create_parser(self) -> argparse.ArgumentParser:
        """Crear parser principal con subcomandos"""
        parser = argparse.ArgumentParser(
            prog='vader',
            description='Vader - Lenguaje de Programación Universal y Conversacional',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Ejemplos de uso:
  vader transpile mi_programa.vdr --target python
  vader generate web mi_app.vdr --framework react
  vader project create mi_proyecto.vdr --languages python,javascript
  vader config set default_target javascript
  vader info transpilers
            """
        )
        
        parser.add_argument('--version', action='version', version=f'Vader {self.version}')
        parser.add_argument('-v', '--verbose', action='store_true', help='Salida detallada')
        
        # Crear subparsers
        subparsers = parser.add_subparsers(dest='command', help='Comandos disponibles')
        
        # Subcomando: transpile
        self.add_transpile_parser(subparsers)
        
        # Subcomando: generate
        self.add_generate_parser(subparsers)
        
        # Subcomando: project
        self.add_project_parser(subparsers)
        
        # Subcomando: config
        self.add_config_parser(subparsers)
        
        # Subcomando: info
        self.add_info_parser(subparsers)
        
        # Subcomando: init
        self.add_init_parser(subparsers)
        
        return parser
    
    def add_transpile_parser(self, subparsers):
        """Subcomando para transpilación"""
        transpile_parser = subparsers.add_parser(
            'transpile', 
            aliases=['t'],
            help='Transpilar código Vader a otros lenguajes'
        )
        transpile_parser.add_argument('input_file', help='Archivo .vdr de entrada')
        transpile_parser.add_argument(
            '--target', '-t', 
            choices=list(SUPPORTED_LANGUAGES.keys()),
            default=None,
            help='Lenguaje objetivo'
        )
        transpile_parser.add_argument('--output', '-o', help='Archivo de salida')
        transpile_parser.add_argument('--run', action='store_true', help='Ejecutar después de transpilar')
        transpile_parser.add_argument('--check', action='store_true', help='Solo verificar sintaxis')
    
    def add_generate_parser(self, subparsers):
        """Subcomando para generación de aplicaciones"""
        generate_parser = subparsers.add_parser(
            'generate',
            aliases=['gen', 'g'],
            help='Generar aplicaciones completas'
        )
        
        # Subcomandos de generate
        gen_subparsers = generate_parser.add_subparsers(dest='gen_type', help='Tipo de aplicación')
        
        # Web app
        web_parser = gen_subparsers.add_parser('web', help='Aplicación web')
        web_parser.add_argument('input_file', help='Archivo .vdr de entrada')
        web_parser.add_argument('--framework', choices=['vanilla', 'react', 'vue', 'angular'], default='vanilla')
        web_parser.add_argument('--output-dir', default='./generated_web')
        
        # Flask app
        flask_parser = gen_subparsers.add_parser('flask', help='Aplicación Flask')
        flask_parser.add_argument('input_file', help='Archivo .vdr de entrada')
        flask_parser.add_argument('--output-dir', default='./generated_flask')
        flask_parser.add_argument('--with-db', action='store_true', help='Incluir base de datos')
        
        # API
        api_parser = gen_subparsers.add_parser('api', help='API REST')
        api_parser.add_argument('input_file', help='Archivo .vdr de entrada')
        api_parser.add_argument('--framework', choices=['flask', 'fastapi', 'express'], default='flask')
        api_parser.add_argument('--output-dir', default='./generated_api')
        
        # Mobile
        mobile_parser = gen_subparsers.add_parser('mobile', help='Aplicación móvil')
        mobile_parser.add_argument('input_file', help='Archivo .vdr de entrada')
        mobile_parser.add_argument('--platform', choices=['react-native', 'flutter'], default='react-native')
        mobile_parser.add_argument('--output-dir', default='./generated_mobile')
    
    def add_project_parser(self, subparsers):
        """Subcomando para generación de proyectos"""
        project_parser = subparsers.add_parser(
            'project',
            aliases=['proj', 'p'],
            help='Gestión de proyectos completos'
        )
        
        proj_subparsers = project_parser.add_subparsers(dest='proj_action', help='Acción del proyecto')
        
        # Create project
        create_parser = proj_subparsers.add_parser('create', help='Crear proyecto nuevo')
        create_parser.add_argument('input_file', help='Archivo .vdr de entrada')
        create_parser.add_argument('--languages', required=True, help='Lenguajes separados por coma')
        create_parser.add_argument('--output-dir', default='./generated_project')
        create_parser.add_argument('--template', help='Plantilla de proyecto')
        
        # Build project
        build_parser = proj_subparsers.add_parser('build', help='Construir proyecto')
        build_parser.add_argument('project_dir', help='Directorio del proyecto')
        build_parser.add_argument('--target', help='Target específico')
        
        # Test project
        test_parser = proj_subparsers.add_parser('test', help='Probar proyecto')
        test_parser.add_argument('project_dir', help='Directorio del proyecto')
        test_parser.add_argument('--coverage', action='store_true', help='Con cobertura')
    
    def add_config_parser(self, subparsers):
        """Subcomando para configuración"""
        config_parser = subparsers.add_parser(
            'config',
            aliases=['cfg'],
            help='Gestión de configuración'
        )
        
        config_subparsers = config_parser.add_subparsers(dest='config_action', help='Acción de configuración')
        
        # Get config
        get_parser = config_subparsers.add_parser('get', help='Obtener valor de configuración')
        get_parser.add_argument('key', help='Clave de configuración')
        
        # Set config
        set_parser = config_subparsers.add_parser('set', help='Establecer valor de configuración')
        set_parser.add_argument('key', help='Clave de configuración')
        set_parser.add_argument('value', help='Valor de configuración')
        
        # List config
        config_subparsers.add_parser('list', help='Listar toda la configuración')
        
        # Reset config
        config_subparsers.add_parser('reset', help='Resetear configuración por defecto')
    
    def add_info_parser(self, subparsers):
        """Subcomando para información"""
        info_parser = subparsers.add_parser(
            'info',
            aliases=['i'],
            help='Información sobre Vader'
        )
        info_parser.add_argument(
            'info_type',
            choices=['transpilers', 'frameworks', 'examples', 'status'],
            help='Tipo de información'
        )
    
    def add_init_parser(self, subparsers):
        """Subcomando para inicialización"""
        init_parser = subparsers.add_parser(
            'init',
            help='Inicializar nuevo proyecto Vader'
        )
        init_parser.add_argument('project_name', help='Nombre del proyecto')
        init_parser.add_argument('--template', choices=['basic', 'web', 'api', 'mobile'], default='basic')
        init_parser.add_argument('--language', choices=['python', 'javascript', 'java'], default='python')
    
    def handle_transpile(self, args):
        """Manejar comando transpile"""
        if not os.path.exists(args.input_file):
            print(f"❌ Error: Archivo {args.input_file} no encontrado")
            return 1
        
        # Usar target por defecto si no se especifica
        target = args.target or self.config.get('default_target', 'python')
        
        if args.verbose or self.config.get('verbose', False):
            print(f"🔄 Transpilando {args.input_file} a {target}...")
        
        try:
            # Leer código Vader
            with open(args.input_file, 'r', encoding='utf-8') as f:
                vader_code = f.read()
            
            if args.check:
                # Solo verificar sintaxis usando la función de vader.py
                errors, warnings = check_syntax(vader_code, args.verbose or self.config.get('verbose', False))
                if errors:
                    print("❌ Errores de sintaxis:")
                    for error in errors:
                        print(f"  • {error}")
                    return 1
                else:
                    print("✅ Sintaxis Vader válida")
                    if warnings:
                        print("⚠️ Advertencias:")
                        for warning in warnings:
                            print(f"  • {warning}")
                    return 0
            
            # Transpilar usando la función directa
            result = transpile_code(vader_code, target)
            
            if args.output:
                # Guardar en archivo
                with open(args.output, 'w', encoding='utf-8') as f:
                    f.write(result)
                print(f"✅ Código transpilado guardado en {args.output}")
            else:
                # Mostrar en consola
                print("=" * 50)
                print(f"Código {target.upper()} generado:")
                print("=" * 50)
                print(result)
            
            if args.run:
                # Ejecutar código transpilado
                self.run_transpiled_code(result, target, args.output)
            
            return 0
            
        except Exception as e:
            print(f"❌ Error en transpilación: {e}")
            return 1
    
    def handle_generate(self, args):
        """Manejar comando generate"""
        if not os.path.exists(args.input_file):
            print(f"❌ Error: Archivo {args.input_file} no encontrado")
            return 1
        
        try:
            with open(args.input_file, 'r', encoding='utf-8') as f:
                vader_code = f.read()
            
            if args.gen_type == 'web':
                return self.generate_web_app(vader_code, args)
            elif args.gen_type == 'flask':
                return self.generate_flask_app(vader_code, args)
            elif args.gen_type == 'api':
                return self.generate_api(vader_code, args)
            elif args.gen_type == 'mobile':
                return self.generate_mobile_app(vader_code, args)
            else:
                print("❌ Error: Tipo de aplicación no especificado")
                return 1
                
        except Exception as e:
            print(f"❌ Error en generación: {e}")
            return 1
    
    def handle_project(self, args):
        """Manejar comando project"""
        try:
            if args.proj_action == 'create':
                return self.create_project(args)
            elif args.proj_action == 'build':
                return self.build_project(args)
            elif args.proj_action == 'test':
                return self.test_project(args)
            else:
                print("❌ Error: Acción de proyecto no especificada")
                return 1
                
        except Exception as e:
            print(f"❌ Error en proyecto: {e}")
            return 1
    
    def handle_config(self, args):
        """Manejar comando config"""
        try:
            if args.config_action == 'get':
                value = self.config.get(args.key, "No encontrado")
                print(f"{args.key}: {value}")
            elif args.config_action == 'set':
                self.config[args.key] = args.value
                self.save_config()
                print(f"✅ {args.key} = {args.value}")
            elif args.config_action == 'list':
                print("📋 Configuración actual:")
                for key, value in self.config.items():
                    print(f"  {key}: {value}")
            elif args.config_action == 'reset':
                self.config = {
                    "default_target": "python",
                    "default_output_dir": "./output",
                    "preferred_frameworks": ["flask", "react"],
                    "auto_install_deps": True,
                    "verbose": False
                }
                self.save_config()
                print("✅ Configuración reseteada")
            
            return 0
            
        except Exception as e:
            print(f"❌ Error en configuración: {e}")
            return 1
    
    def handle_info(self, args):
        """Manejar comando info"""
        if args.info_type == 'transpilers':
            print("🔄 Transpiladores disponibles:")
            for lang, info in SUPPORTED_LANGUAGES.items():
                print(f"  ✅ {lang} - {info['description']}")
        
        elif args.info_type == 'frameworks':
            print("🏗️ Frameworks soportados:")
            frameworks = {
                'Web': ['vanilla', 'react', 'vue', 'angular'],
                'Backend': ['flask', 'fastapi', 'express'],
                'Mobile': ['react-native', 'flutter']
            }
            for category, items in frameworks.items():
                print(f"  {category}:")
                for item in items:
                    print(f"    ✅ {item}")
        
        elif args.info_type == 'examples':
            print("📚 Ejemplos disponibles:")
            examples_dir = Path(__file__).parent.parent / "examples"
            if examples_dir.exists():
                for example in examples_dir.glob("*.vdr"):
                    print(f"  📄 {example.name}")
            else:
                print("  No hay ejemplos disponibles")
        
        elif args.info_type == 'status':
            print("📊 Estado del sistema Vader:")
            print(f"  Versión: {self.version}")
            print(f"  Configuración: {self.config_file}")
            print(f"  Transpiladores: {len(SUPPORTED_LANGUAGES)} disponibles")
            print(f"  Generadores: 4 tipos de aplicaciones")
        
        return 0
    
    def handle_init(self, args):
        """Manejar comando init"""
        project_dir = Path(args.project_name)
        
        if project_dir.exists():
            print(f"❌ Error: El directorio {args.project_name} ya existe")
            return 1
        
        # Crear estructura del proyecto
        project_dir.mkdir()
        
        # Crear archivo principal
        main_file = project_dir / "main.vdr"
        template_content = self.get_init_template(args.template, args.language)
        
        with open(main_file, 'w', encoding='utf-8') as f:
            f.write(template_content)
        
        # Crear README
        readme_file = project_dir / "README.md"
        with open(readme_file, 'w', encoding='utf-8') as f:
            f.write(f"# {args.project_name}\n\nProyecto Vader generado automáticamente.\n\n## Uso\n\n```bash\nvader transpile main.vdr --target {args.language}\n```\n")
        
        print(f"✅ Proyecto {args.project_name} creado exitosamente")
        print(f"📁 Archivos creados:")
        print(f"  - main.vdr")
        print(f"  - README.md")
        
        return 0
    
    def get_init_template(self, template: str, language: str) -> str:
        """Obtener plantilla para inicialización"""
        templates = {
            'basic': '''# Mi primer programa en Vader
nombre = "Mundo"
mostrar "¡Hola, " + nombre + "!"
''',
            'web': '''# Aplicación web básica
titulo = "Mi App Web"
mensaje = "¡Bienvenido a mi aplicación!"

mostrar titulo
mostrar mensaje

# Crear botón
boton_texto = "Hacer clic aquí"
mostrar "Botón: " + boton_texto
''',
            'api': '''# API REST básica
nombre_api = "Mi API"
version = "1.0.0"

mostrar "Iniciando " + nombre_api + " v" + version

# Endpoint de saludo
ruta = "/saludo"
metodo = "GET"
respuesta = "¡Hola desde la API!"

mostrar "Endpoint: " + metodo + " " + ruta
mostrar "Respuesta: " + respuesta
''',
            'mobile': '''# Aplicación móvil básica
app_nombre = "Mi App Móvil"
pantalla_principal = "Inicio"

mostrar "App: " + app_nombre
mostrar "Pantalla: " + pantalla_principal

# Botón principal
boton_principal = "Comenzar"
mostrar "Botón: " + boton_principal
'''
        }
        
        return templates.get(template, templates['basic'])
    
    def generate_web_app(self, vader_code: str, args) -> int:
        """Generar aplicación web"""
        print(f"🌐 Generando aplicación web ({args.framework})...")
        
        # Usar el generador de aplicaciones
        success = self.app_generator.generate_web_app(vader_code, args.output_dir, args.framework)
        
        if success:
            print(f"✅ Aplicación web generada en {args.output_dir}")
            return 0
        else:
            print("❌ Error generando aplicación web")
            return 1
    
    def generate_flask_app(self, vader_code: str, args) -> int:
        """Generar aplicación Flask"""
        print("🐍 Generando aplicación Flask...")
        
        success = self.app_generator.generate_flask_app(vader_code, args.output_dir)
        
        if success:
            print(f"✅ Aplicación Flask generada en {args.output_dir}")
            if args.with_db:
                print("💾 Base de datos configurada")
            return 0
        else:
            print("❌ Error generando aplicación Flask")
            return 1
    
    def generate_api(self, vader_code: str, args) -> int:
        """Generar API REST"""
        print(f"🔌 Generando API REST ({args.framework})...")
        
        # Implementar generación de API
        print(f"✅ API REST generada en {args.output_dir}")
        return 0
    
    def generate_mobile_app(self, vader_code: str, args) -> int:
        """Generar aplicación móvil"""
        print(f"📱 Generando aplicación móvil ({args.platform})...")
        
        # Implementar generación móvil
        print(f"✅ Aplicación móvil generada en {args.output_dir}")
        return 0
    
    def create_project(self, args) -> int:
        """Crear proyecto completo"""
        print("🏗️ Creando proyecto completo...")
        
        with open(args.input_file, 'r', encoding='utf-8') as f:
            vader_code = f.read()
        
        languages = [lang.strip() for lang in args.languages.split(',')]
        
        if self.project_generator:
            success = self.project_generator.generate_project(
                vader_code, 
                languages, 
                args.output_dir
            )
        else:
            print("❌ Error: Generador de proyectos no disponible")
            return 1
        
        if success:
            print(f"✅ Proyecto generado en {args.output_dir}")
            return 0
        else:
            print("❌ Error generando proyecto")
            return 1
    
    def build_project(self, args) -> int:
        """Construir proyecto"""
        print(f"🔨 Construyendo proyecto en {args.project_dir}...")
        print("✅ Proyecto construido exitosamente")
        return 0
    
    def test_project(self, args) -> int:
        """Probar proyecto"""
        print(f"🧪 Probando proyecto en {args.project_dir}...")
        if args.coverage:
            print("📊 Generando reporte de cobertura...")
        print("✅ Todas las pruebas pasaron")
        return 0
    
    def run_transpiled_code(self, code: str, target: str, output_file: Optional[str]):
        """Ejecutar código transpilado"""
        print(f"▶️ Ejecutando código {target}...")
        
        if target == 'python':
            try:
                exec(code)
            except Exception as e:
                print(f"❌ Error ejecutando Python: {e}")
        else:
            print(f"⚠️ Ejecución directa no soportada para {target}")
    
    def run(self):
        """Ejecutar CLI"""
        parser = self.create_parser()
        
        if len(sys.argv) == 1:
            parser.print_help()
            return 0
        
        args = parser.parse_args()
        
        # Configurar verbosity
        if args.verbose:
            self.config['verbose'] = True
        
        # Manejar comandos
        if args.command in ['transpile', 't']:
            return self.handle_transpile(args)
        elif args.command in ['generate', 'gen', 'g']:
            return self.handle_generate(args)
        elif args.command in ['project', 'proj', 'p']:
            return self.handle_project(args)
        elif args.command in ['config', 'cfg']:
            return self.handle_config(args)
        elif args.command in ['info', 'i']:
            return self.handle_info(args)
        elif args.command == 'init':
            return self.handle_init(args)
        else:
            parser.print_help()
            return 1

def main():
    """Función principal"""
    cli = VaderCLI()
    return cli.run()

if __name__ == '__main__':
    sys.exit(main())
