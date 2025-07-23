#!/usr/bin/env python3
"""
🌟 VADER - EL PRIMER LENGUAJE UNIVERSAL Y CONVERSACIONAL DE LA HISTORIA
Creado por: El hombre que enseñó al mundo a programar

Vader no es un lenguaje de programación, Vader es LA PROGRAMACIÓN:
libre, descentralizada y accesible a todos
"""

import argparse
import sys
import os
from pathlib import Path
from conversational_integration import integrate_conversational_with_vader, detect_conversational_file

# Agregar el directorio raíz al path para que encuentre el módulo transpilers
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from transpilers import python, javascript, java, csharp, go, rust, swift, kotlin, typescript, dart, php, ruby, solidity, html, css
from vader_interpreter import VaderNativeRuntime
from multilingual_core import multilingual_system

# Versión de Vader
VADER_VERSION = "7.0.0"
VADER_CODENAME = "UNIVERSAL"

# Lenguajes soportados
SUPPORTED_LANGUAGES = {
    'python': {
        'transpiler': python,
        'extension': '.py',
        'description': 'Python 3.x'
    },
    'js': {
        'transpiler': javascript,
        'extension': '.js', 
        'description': 'JavaScript ES6+'
    },
    'javascript': {
        'transpiler': javascript,
        'extension': '.js',
        'description': 'JavaScript ES6+'
    },
    'java': {
        'transpiler': java,
        'extension': '.java',
        'description': 'Java 8+'
    },
    'csharp': {
        'transpiler': csharp,
        'extension': '.cs',
        'description': 'C# .NET'
    },
    'cs': {
        'transpiler': csharp,
        'extension': '.cs',
        'description': 'C# .NET'
    },
    'go': {
        'transpiler': go,
        'extension': '.go',
        'description': 'Go'
    },
    'rust': {
        'transpiler': rust,
        'extension': '.rs',
        'description': 'Rust'
    },
    'rs': {
        'transpiler': rust,
        'extension': '.rs',
        'description': 'Rust'
    },
    'swift': {
        'transpiler': swift,
        'extension': '.swift',
        'description': 'Swift'
    },
    'kotlin': {
        'transpiler': kotlin,
        'extension': '.kt',
        'description': 'Kotlin'
    },
    'typescript': {
        'transpiler': typescript,
        'extension': '.ts',
        'description': 'TypeScript'
    },
    'ts': {
        'transpiler': typescript,
        'extension': '.ts',
        'description': 'TypeScript'
    },
    'dart': {
        'transpiler': dart,
        'extension': '.dart',
        'description': 'Dart'
    },
    'php': {
        'transpiler': php,
        'extension': '.php',
        'description': 'PHP'
    },
    'ruby': {
        'transpiler': ruby,
        'extension': '.rb',
        'description': 'Ruby'
    },
    'rb': {
        'transpiler': ruby,
        'extension': '.rb',
        'description': 'Ruby'
    },
    'solidity': {
        'transpiler': solidity,
        'extension': '.sol',
        'description': 'Solidity (Smart Contracts)'
    },
    'sol': {
        'transpiler': solidity,
        'extension': '.sol',
        'description': 'Solidity (Smart Contracts)'
    },
    'html': {
        'transpiler': html,
        'extension': '.html',
        'description': 'HTML5'
    },
    'css': {
        'transpiler': css,
        'extension': '.css',
        'description': 'CSS3'
    }
}

def create_argument_parser():
    """Crea y configura el parser de argumentos de línea de comandos"""
    parser = argparse.ArgumentParser(
        prog='vader',
        description='Transpilador del lenguaje Vader - Programa en español, ejecuta en cualquier lugar',
        epilog=f'Vader v{VADER_VERSION} - Lenguaje de programación en español'
    )
    
    parser.add_argument(
        'archivo',
        nargs='?',
        help='Archivo fuente .vdr a transpilar'
    )
    
    parser.add_argument(
        '--target', '-t',
        choices=list(SUPPORTED_LANGUAGES.keys()),
        help='Lenguaje objetivo para la transpilación'
    )
    
    parser.add_argument(
        '--output', '-o',
        help='Archivo de salida (opcional, por defecto imprime a stdout)'
    )
    
    parser.add_argument(
        '--version', '-v',
        action='version',
        version=f'Vader v{VADER_VERSION}'
    )
    
    parser.add_argument(
        '--run', '-r',
        action='store_true',
        help='Ejecutar el archivo .vdr directamente (sin transpilar)'
    )
    
    parser.add_argument(
        '--interpret', '-i',
        action='store_true',
        help='Interpretar el archivo .vdr nativamente'
    )
    
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Activar modo debug para el intérprete nativo'
    )
    
    parser.add_argument(
        '--list-targets', '-l',
        action='store_true',
        help='Lista todos los lenguajes objetivo soportados'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Modo verboso - muestra información adicional'
    )
    
    parser.add_argument(
        '--check-syntax',
        action='store_true',
        help='Solo verifica la sintaxis sin transpilar'
    )
    
    parser.add_argument(
        '--framework', '-f',
        help='Framework específico para JavaScript/TypeScript (react, vue, angular, nextjs, etc.)'
    )
    
    parser.add_argument(
        '--list-frameworks',
        action='store_true',
        help='Lista todos los frameworks disponibles para JavaScript/TypeScript'
    )
    
    # Argumentos de Inteligencia Artificial
    parser.add_argument(
        '--ai-generate',
        help='Genera código automáticamente desde una descripción en español natural'
    )
    
    parser.add_argument(
        '--ai-analyze',
        action='store_true',
        help='Analiza el código y proporciona métricas de calidad y sugerencias'
    )
    
    parser.add_argument(
        '--ai-optimize',
        action='store_true',
        help='Optimiza el código automáticamente usando IA'
    )
    
    parser.add_argument(
        '--ai-suggest',
        action='store_true',
        help='Proporciona sugerencias de mejora para el código'
    )
    
    parser.add_argument(
        '--ai-check-errors',
        action='store_true',
        help='Detecta errores en el código usando IA'
    )
    
    parser.add_argument(
        '--ai-detailed',
        action='store_true',
        help='Análisis detallado cuando se usa con opciones de IA'
    )
    
    # Argumentos Multiidioma
    parser.add_argument(
        '--language', '--lang',
        help='Especificar el idioma del código fuente (es, en, fr, pt, it, zh, ja, ru, de, ar, ko, etc.)'
    )
    
    parser.add_argument(
        '--detect-language',
        action='store_true',
        help='Detectar automáticamente el idioma del código fuente'
    )
    
    parser.add_argument(
        '--list-languages',
        action='store_true',
        help='Lista todos los idiomas soportados para programar'
    )
    
    parser.add_argument(
        '--translate-to',
        help='Traducir el código de un idioma a otro (especificar idioma objetivo)'
    )
    
    parser.add_argument(
        '--multilingual-info',
        help='Mostrar información detallada de un idioma específico'
    )
    
    return parser

def list_supported_targets():
    """Lista todos los lenguajes objetivo soportados"""
    print("Lenguajes objetivo soportados:")
    print("=" * 40)
    for key, info in SUPPORTED_LANGUAGES.items():
        print(f"  {key:<12} - {info['description']} (extensión: {info['extension']})")
    print()

def list_supported_frameworks():
    """Lista todos los frameworks disponibles para JavaScript/TypeScript"""
    try:
        from transpilers.frameworks import list_frameworks, get_framework_info
        
        print("🚀 Frameworks soportados por Vader:")
        print("=" * 40)
        
        frameworks = list_frameworks()
        framework_info = get_framework_info()
        
        for framework in frameworks:
            info = framework_info.get(framework, {})
            name = info.get('name', framework.capitalize())
            description = info.get('description', 'Framework disponible')
            target = info.get('target_language', 'javascript')
            
            print(f"📦 {name} ({framework})")
            print(f"   Descripción: {description}")
            print(f"   Lenguaje: {target}")
            print()
        
        print(f"Total: {len(frameworks)} frameworks disponibles")
        print("\n💡 Uso: python3 src/vader.py archivo.vdr --target javascript --framework <nombre>")
        
    except ImportError:
        print("Error: Sistema de frameworks no disponible")
        print("Asegúrate de que el módulo transpilers.frameworks esté instalado")
    except Exception as e:
        print(f"Error al listar frameworks: {e}")

def validate_framework(framework_name):
    """Valida que el framework especificado sea soportado"""
    try:
        from transpilers.frameworks import get_available_frameworks
        available = get_available_frameworks()
        if framework_name.lower() not in available:
            print(f"Error: Framework '{framework_name}' no soportado")
            print(f"Frameworks disponibles: {', '.join(available)}")
            return False
        return True
    except ImportError:
        print("Error: Sistema de frameworks no disponible")
        return False

def validate_vader_file(filepath):
    """Valida que el archivo sea un archivo Vader válido"""
    if not filepath.endswith('.vdr'):
        print(f"Advertencia: El archivo '{filepath}' no tiene extensión .vdr")
    
    if not os.path.exists(filepath):
        print(f"Error: Archivo no encontrado: {filepath}")
        return False
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            if not content.strip():
                print("Uso: python3 src/vader.py archivo.vdr --target python|js|java|csharp|go|rust")
        return True
    except UnicodeDecodeError:
        print(f"Error: No se puede leer el archivo '{filepath}' - problemas de codificación")
        return False
    except Exception as e:
        print(f"Error al leer el archivo '{filepath}': {e}")
        return False

def check_syntax(codigo, verbose=False):
    """Verifica la sintaxis básica del código Vader"""
    lines = codigo.strip().split('\n')
    errors = []
    warnings = []
    
    # Contadores para verificar estructura
    open_blocks = {
        'clase': 0,
        'funcion': 0,
        'si': 0,
        'repetir': 0,
        'intentar': 0,
        'con': 0
    }
    
    for i, line in enumerate(lines, 1):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
            
        # Verificar bloques de apertura
        if line.startswith('clase'):
            open_blocks['clase'] += 1
        elif line.startswith('funcion') or line.startswith('asincrona funcion'):
            open_blocks['funcion'] += 1
        elif line.startswith('si '):
            open_blocks['si'] += 1
        elif line.startswith('repetir'):
            open_blocks['repetir'] += 1
        elif line.startswith('intentar'):
            open_blocks['intentar'] += 1
        elif line.startswith('con '):
            open_blocks['con'] += 1
            
        # Verificar bloques de cierre
        elif line == 'fin clase':
            if open_blocks['clase'] > 0:
                open_blocks['clase'] -= 1
            else:
                errors.append(f"Línea {i}: 'fin clase' sin 'clase' correspondiente")
        elif line == 'fin funcion':
            if open_blocks['funcion'] > 0:
                open_blocks['funcion'] -= 1
            else:
                errors.append(f"Línea {i}: 'fin funcion' sin 'funcion' correspondiente")
        elif line == 'fin si':
            if open_blocks['si'] > 0:
                open_blocks['si'] -= 1
            else:
                errors.append(f"Línea {i}: 'fin si' sin 'si' correspondiente")
        elif line in ['fin repetir', 'fin mientras']:
            if open_blocks['repetir'] > 0:
                open_blocks['repetir'] -= 1
            else:
                errors.append(f"Línea {i}: '{line}' sin bloque correspondiente")
        elif line == 'fin intentar':
            if open_blocks['intentar'] > 0:
                open_blocks['intentar'] -= 1
            else:
                errors.append(f"Línea {i}: 'fin intentar' sin 'intentar' correspondiente")
        elif line == 'fin con':
            if open_blocks['con'] > 0:
                open_blocks['con'] -= 1
            else:
                errors.append(f"Línea {i}: 'fin con' sin 'con' correspondiente")
    
    # Verificar bloques sin cerrar
    for block_type, count in open_blocks.items():
        if count > 0:
            errors.append(f"Bloque '{block_type}' sin cerrar ({count} instancia(s))")
    
    return errors, warnings

def detect_database_operations(codigo):
    """Detecta operaciones de base de datos en el código Vader"""
    db_keywords = {
        'conectar base_datos': 'connection',
        'crear tabla': 'create_table',
        'insertar en': 'insert',
        'buscar en': 'select',
        'buscar todos en': 'select',
        'buscar desde': 'select',
        'actualizar': 'update',
        'eliminar de': 'delete'
    }
    
    detected_operations = []
    db_type = 'mysql'  # default
    
    lines = codigo.lower().split('\n')
    for line in lines:
        line = line.strip()
        for keyword, operation in db_keywords.items():
            if line.startswith(keyword):
                detected_operations.append(operation)
                # Detectar tipo de base de datos
                if 'mysql' in line:
                    db_type = 'mysql'
                elif 'postgresql' in line or 'postgres' in line:
                    db_type = 'postgresql'
                elif 'mongodb' in line:
                    db_type = 'mongodb'
                elif 'sqlite' in line:
                    db_type = 'sqlite'
                break
    
    if detected_operations:
        return {
            'types': list(set(detected_operations)),
            'db_type': db_type,
            'has_db_operations': True
        }
    
    return None

def detect_html_content(codigo):
    """Detecta contenido HTML en el código Vader"""
    html_keywords = [
        'pagina', 'encabezado', 'navegacion', 'seccion', 'articulo', 'pie_pagina',
        'titulo1', 'titulo2', 'titulo3', 'parrafo', 'enlace', 'boton', 'imagen',
        'lista', 'elemento', 'formulario', 'campo', 'tabla', 'fila', 'celda'
    ]
    
    lines = codigo.lower().split('\n')
    for line in lines:
        line = line.strip()
        for keyword in html_keywords:
            if line.startswith(keyword) and not '=' in line:
                return True
    
    return False

def detect_css_content(codigo):
    """Detecta contenido CSS en el código Vader"""
    css_keywords = [
        'estilos', 'color', 'fondo', 'fuente', 'tamaño_fuente', 'margen', 'relleno',
        'borde', 'sombra', 'mostrar', 'posicion', 'ancho', 'alto', 'responsive',
        'animacion', 'hover', 'active'
    ]
    
    lines = codigo.lower().split('\n')
    for line in lines:
        line = line.strip()
        if line.startswith('estilos'):
            return True
        for keyword in css_keywords:
            if ('=' in line or ':' in line) and keyword in line:
                return True
    
    return False

def transpile_code(codigo, target_lang, framework=None, verbose=False):
    """Transpila el código Vader al lenguaje objetivo"""
    if verbose:
        print(f"Transpilando a {SUPPORTED_LANGUAGES[target_lang]['description']}...")
        if framework:
            print(f"Usando framework: {framework}")
    
    # Detectar si el código contiene operaciones de base de datos
    db_operations = detect_database_operations(codigo)
    if db_operations:
        if verbose:
            print(f"Detectadas operaciones de base de datos: {', '.join(db_operations['types'])}")
            print(f"Tipo de base de datos: {db_operations['db_type']}")
    
    # Detectar si el código contiene HTML o CSS
    has_html = detect_html_content(codigo)
    has_css = detect_css_content(codigo)
    
    if has_html and verbose:
        print("Detectado contenido HTML en el código")
    if has_css and verbose:
        print("Detectado contenido CSS en el código")
    
    try:
        transpiler = SUPPORTED_LANGUAGES[target_lang]['transpiler']
        
        # Si el código contiene HTML, usar el transpilador HTML
        if has_html and target_lang == 'html':
            try:
                from transpilers.html import transpilar_html
                if verbose:
                    print("Procesando contenido HTML...")
                resultado = transpilar_html(codigo)
            except ImportError as e:
                if verbose:
                    print(f"Advertencia: No se pudo cargar el módulo HTML: {e}")
                    print("Usando transpilación estándar...")
                resultado = transpiler.transpilar(codigo)
        # Si el código contiene CSS, usar el transpilador CSS
        elif has_css and target_lang == 'css':
            try:
                from transpilers.css import transpilar_css
                if verbose:
                    print("Procesando contenido CSS...")
                resultado = transpilar_css(codigo)
            except ImportError as e:
                if verbose:
                    print(f"Advertencia: No se pudo cargar el módulo CSS: {e}")
                    print("Usando transpilación estándar...")
                resultado = transpiler.transpilar(codigo)
        # Si el código contiene operaciones de base de datos, usar el transpilador de BD
        elif db_operations and db_operations['has_db_operations']:
            try:
                from transpilers.database import transpilar_base_datos
                if verbose:
                    print(f"Procesando operaciones de base de datos con {db_operations['db_type']}...")
                resultado = transpilar_base_datos(codigo, target_lang, db_operations['db_type'])
            except ImportError as e:
                if verbose:
                    print(f"Advertencia: No se pudo cargar el módulo de base de datos: {e}")
                    print("Usando transpilación estándar...")
                resultado = transpiler.transpilar(codigo)
        # Si se especifica un framework, intentar usarlo para cualquier lenguaje
        elif framework:
            try:
                from transpilers.frameworks import transpile_with_framework, get_framework_info
                framework_info = get_framework_info(framework)
                if framework_info:
                    # Verificar si el framework es compatible con el lenguaje objetivo
                    framework_ext = framework_info['extension']
                    target_extensions = {
                        'python': '.py', 'js': '.js', 'javascript': '.js', 'ts': '.ts', 'typescript': '.ts',
                        'php': '.php', 'dart': '.dart', 'java': '.java', 'csharp': '.cs', 'cs': '.cs'
                    }
                    
                    if target_lang in target_extensions and (framework_ext == target_extensions[target_lang] or 
                        (target_lang in ['js', 'javascript', 'ts', 'typescript'] and framework_ext in ['.js', '.jsx', '.ts', '.tsx'])):
                        resultado = transpile_with_framework(codigo, framework)
                    else:
                        print(f"Advertencia: Framework {framework} ({framework_ext}) no es compatible con {target_lang}")
                        print("Usando transpilación estándar...")
                        resultado = transpiler.transpilar(codigo)
                else:
                    print(f"Advertencia: Framework {framework} no encontrado")
                    resultado = transpiler.transpilar(codigo)
            except (ImportError, ValueError) as e:
                print(f"Advertencia: No se pudo usar el framework {framework}: {e}")
                print("Usando transpilación estándar...")
                resultado = transpiler.transpilar(codigo)
        elif target_lang == "go" or target_lang == "golang":
            resultado = go.transpilar(codigo)
        elif target_lang == "rust" or target_lang == "rs":
            resultado = rust.transpilar(codigo)
        elif target_lang == "elixir" or target_lang == "ex":
            import transpilers.elixir as elixir
            resultado = elixir.transpilar(codigo)
        elif target_lang == "julia" or target_lang == "jl":
            import transpilers.julia as julia
            resultado = julia.transpilar(codigo)
        else:
            # Para JavaScript, pasar el framework como parámetro si está disponible
            if target_lang in ['js', 'javascript'] and hasattr(transpiler, 'transpile_to_javascript'):
                resultado = transpiler.transpile_to_javascript(codigo, framework=framework)
            else:
                resultado = transpiler.transpilar(codigo)
        
        if verbose:
            print(f"Transpilación completada exitosamente.")
            print(f"Líneas generadas: {len(resultado.split())}")
        
        return resultado
    except Exception as e:
        print(f"Error durante la transpilación: {e}")
        return None

def save_output(content, output_path, target_lang):
    """Guarda el contenido transpilado en un archivo"""
    try:
        # Si no se especifica extensión, usar la del lenguaje objetivo
        if not output_path.endswith(SUPPORTED_LANGUAGES[target_lang]['extension']):
            output_path += SUPPORTED_LANGUAGES[target_lang]['extension']
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Archivo guardado: {output_path}")
        return True
    except Exception as e:
        print(f"Error al guardar el archivo: {e}")
        return False

def list_supported_languages():
    """Lista todos los idiomas soportados para programar"""
    languages = multilingual_system.get_supported_languages()
    if not languages:
        print("❌ No se encontraron idiomas configurados")
        return
    
    print("🌍 IDIOMAS SOPORTADOS PARA PROGRAMAR EN VADER:")
    print("=" * 60)
    for code, info in languages.items():
        print(f"  {code:<4} - {info['native_name']:<15} ({info['name']:<10}) - {info['keywords_count']} palabras clave")
    print(f"\n✨ Total: {len(languages)} idiomas disponibles")
    print("\n💡 Usa --language <código> para especificar el idioma")
    print("💡 Usa --detect-language para detección automática")

def detect_code_language(code):
    """Detecta automáticamente el idioma del código"""
    detected = multilingual_system.detect_language(code)
    languages = multilingual_system.get_supported_languages()
    
    if detected in languages:
        lang_info = languages[detected]
        print(f"🔍 IDIOMA DETECTADO: {lang_info['native_name']} ({lang_info['name']})")
        print(f"📝 Código de idioma: {detected}")
        return detected
    else:
        print(f"⚠️  Idioma detectado: {detected} (puede no estar completamente soportado)")
        return detected

def show_language_info(lang_code):
    """Muestra información detallada de un idioma específico"""
    lang_info = multilingual_system.get_language_info(lang_code)
    
    if not lang_info:
        print(f"❌ Idioma '{lang_code}' no encontrado")
        print("💡 Usa --list-languages para ver idiomas disponibles")
        return False
    
    print(f"🌍 INFORMACIÓN DEL IDIOMA: {lang_info['native_name']}")
    print("=" * 50)
    print(f"📝 Nombre: {lang_info['name']}")
    print(f"🏷️  Código: {lang_info['code']}")
    print(f"📖 Dirección: {'Derecha a Izquierda' if lang_info.get('direction') == 'rtl' else 'Izquierda a Derecha'}")
    print(f"🔤 Codificación: {lang_info.get('encoding', 'utf-8')}")
    
    keywords = lang_info.get('keywords', {})
    print(f"\n🔑 PALABRAS CLAVE ({sum(len(words) for words in keywords.values())} total):")
    
    for category, words in keywords.items():
        print(f"  📂 {category.replace('_', ' ').title()}: {', '.join(words[:5])}{'...' if len(words) > 5 else ''}")
    
    examples = lang_info.get('examples', {})
    if examples:
        print(f"\n📚 EJEMPLOS DE CÓDIGO:")
        for example_name, code in examples.items():
            print(f"  💻 {example_name.replace('_', ' ').title()}:")
            print(f"     {code}")
    
    return True

def translate_code_language(code, source_lang, target_lang):
    """Traduce código de un idioma a otro"""
    try:
        if source_lang == target_lang:
            print(f"ℹ️  El código ya está en {target_lang}")
            return code
        
        languages = multilingual_system.get_supported_languages()
        
        if source_lang not in languages:
            print(f"❌ Idioma fuente '{source_lang}' no soportado")
            return None
        
        if target_lang not in languages:
            print(f"❌ Idioma objetivo '{target_lang}' no soportado")
            return None
        
        source_name = languages[source_lang]['native_name']
        target_name = languages[target_lang]['native_name']
        
        print(f"🔄 Traduciendo código de {source_name} → {target_name}...")
        
        translated = multilingual_system.translate_code(code, source_lang, target_lang)
        
        print(f"✅ Traducción completada exitosamente")
        return translated
        
    except Exception as e:
        print(f"❌ Error durante la traducción: {e}")
        return None

def validate_vader_file(filepath):
    """Valida si un archivo es un archivo Vader válido"""
    if not filepath.endswith('.vdr'):
        print(f"Advertencia: El archivo '{filepath}' no tiene extensión .vdr")
    
    if not os.path.exists(filepath):
        print(f"Error: Archivo no encontrado: {filepath}")
        return False
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            if not content.strip():
                print("Error: El archivo está vacío")
                return False
        return True
    except UnicodeDecodeError:
        print(f"Error: No se puede leer el archivo '{filepath}' - problemas de codificación")
        return False
    except Exception as e:
        print(f"Error al leer el archivo '{filepath}': {e}")
        return False

def handle_ai_generate(args):
    """Maneja la generación automática de código con IA"""
    try:
        from transpilers.ai_assistant import VaderAIAssistant
        
        print("🤖 Iniciando generación automática de código con IA...")
        print(f"📝 Descripción: {args.ai_generate}")
        
        ai = VaderAIAssistant()
        codigo_generado = ai.generate_code_from_description(args.ai_generate)
        
        if codigo_generado:
            print("\n✅ Código generado exitosamente:")
            print("=" * 50)
            print(codigo_generado)
            print("=" * 50)
            
            # Guardar el código generado si se especifica output
            if args.output:
                output_file = args.output if args.output.endswith('.vdr') else args.output + '.vdr'
                try:
                    with open(output_file, 'w', encoding='utf-8') as f:
                        f.write(codigo_generado)
                    print(f"\n💾 Código guardado en: {output_file}")
                except Exception as e:
                    print(f"❌ Error al guardar: {e}")
                    return 1
            
            # Si se especifica target, transpilar automáticamente
            if args.target:
                print(f"\n🔄 Transpilando automáticamente a {args.target}...")
                resultado = transpile_code(codigo_generado, args.target, 
                                         framework=args.framework, verbose=args.verbose)
                if resultado:
                    print("\n🎯 Código transpilado:")
                    print("-" * 40)
                    print(resultado)
                    print("-" * 40)
                    
                    # Guardar código transpilado
                    if args.output:
                        transpiled_output = args.output.replace('.vdr', '') + SUPPORTED_LANGUAGES[args.target]['extension']
                        if save_output(resultado, transpiled_output, args.target):
                            print(f"💾 Código transpilado guardado en: {transpiled_output}")
            
            return 0
        else:
            print("❌ No se pudo generar código. Intenta con una descripción más específica.")
            return 1
            
    except ImportError:
        print("❌ Error: Sistema de IA no disponible")
        print("Asegúrate de que el módulo transpilers.ai_assistant esté instalado")
        return 1
    except Exception as e:
        print(f"❌ Error durante la generación: {e}")
        return 1

def handle_ai_analyze(codigo, detailed=False):
    """Maneja el análisis de código con IA"""
    try:
        from transpilers.ai_assistant import VaderAIAssistant
        
        print("🔍 Analizando código con IA...")
        
        ai = VaderAIAssistant()
        analisis = ai.analyze_code(codigo, detailed=detailed)
        
        print("\n📊 ANÁLISIS DE CÓDIGO:")
        print("=" * 50)
        
        # Mostrar errores
        if analisis['errors']:
            print("❌ ERRORES DETECTADOS:")
            for error in analisis['errors']:
                print(f"  • {error}")
            print()
        
        # Mostrar advertencias
        if analisis['warnings']:
            print("⚠️  ADVERTENCIAS:")
            for warning in analisis['warnings']:
                print(f"  • {warning}")
            print()
        
        # Mostrar sugerencias
        if analisis['suggestions']:
            print("💡 SUGERENCIAS DE MEJORA:")
            for suggestion in analisis['suggestions']:
                print(f"  • {suggestion}")
            print()
        
        # Mostrar métricas
        if 'metrics' in analisis:
            metrics = analisis['metrics']
            print("📈 MÉTRICAS DE CALIDAD:")
            print(f"  • Líneas totales: {metrics.get('total_lines', 0)}")
            print(f"  • Líneas de código: {metrics.get('code_lines', 0)}")
            print(f"  • Funciones: {metrics.get('functions', 0)}")
            print(f"  • Clases: {metrics.get('classes', 0)}")
            print(f"  • Complejidad: {metrics.get('complexity_score', 0)}")
            print(f"  • Puntuación general: {analisis.get('score', 0)}/100")
            print()
        
        if not analisis['errors'] and not analisis['warnings']:
            print("✅ ¡Código excelente! No se encontraron problemas.")
        
        print("=" * 50)
        return True
        
    except ImportError:
        print("❌ Error: Sistema de IA no disponible")
        return False
    except Exception as e:
        print(f"❌ Error durante el análisis: {e}")
        return False

def handle_ai_optimize(codigo):
    """Maneja la optimización de código con IA"""
    try:
        from transpilers.ai_assistant import VaderAIAssistant
        
        print("⚡ Optimizando código con IA...")
        
        ai = VaderAIAssistant()
        codigo_optimizado = ai.optimize_code(codigo)
        
        if codigo_optimizado and codigo_optimizado != codigo:
            print("\n✅ Código optimizado exitosamente:")
            print("=" * 50)
            print(codigo_optimizado)
            print("=" * 50)
            return codigo_optimizado
        else:
            print("ℹ️  El código ya está optimizado o no se encontraron mejoras.")
            return codigo
            
    except ImportError:
        print("❌ Error: Sistema de IA no disponible")
        return codigo
    except Exception as e:
        print(f"❌ Error durante la optimización: {e}")
        return codigo

def main():
    """Función principal del transpilador Vader"""
    parser = create_argument_parser()
    args = parser.parse_args()
    
    # Listar lenguajes objetivo si se solicita
    if args.list_targets:
        list_supported_targets()
        return 0
    
    # Listar frameworks si se solicita
    if args.list_frameworks:
        list_supported_frameworks()
        return 0
    
    # Manejar comandos multiidioma
    if args.list_languages:
        list_supported_languages()
        return 0
    
    if args.multilingual_info:
        if show_language_info(args.multilingual_info):
            return 0
        else:
            return 1
    
    # Manejar comandos de IA
    if args.ai_generate:
        return handle_ai_generate(args)
    
    # NUEVO: Manejar intérprete nativo
    if args.run or args.interpret:
        if not args.archivo:
            print("❌ Error: Se requiere especificar un archivo .vdr para ejecutar")
            parser.print_help()
            return 1
            
        print(f"🚀 Ejecutando {args.archivo} con Vader Native Runtime...")
        
        # Crear runtime nativo
        runtime = VaderNativeRuntime()
        runtime.debug_mode = args.debug
        
        if args.debug:
            print(f"📁 Archivo: {args.archivo}")
            print(f"🔧 Modo debug: Activado")
            print("=" * 50)
        
        # Ejecutar archivo directamente
        success = runtime.execute_file(args.archivo)
        
        if args.debug:
            print("=" * 50)
            if success:
                print("✅ Ejecución completada exitosamente")
            else:
                print("❌ Ejecución terminada con errores")
                
            print(f"📊 Variables: {len(runtime.variables)}")
            print(f"🔧 Funciones: {len(runtime.functions)}")
        
        return 0 if success else 1
    
    # Validar que se proporcionaron los argumentos necesarios
    if not args.archivo and not args.ai_generate:
        print("Error: Se requiere especificar un archivo .vdr o usar --ai-generate")
        parser.print_help()
        return 1
        
    # Solo requerir target si no es verificación de sintaxis
    if not args.check_syntax and not args.target:
        print("Error: Se requiere especificar un lenguaje objetivo con --target")
        parser.print_help()
        return 1
    
    # Validar framework si se especifica
    if args.framework:
        if not args.target:
            print("Error: Se requiere especificar un lenguaje objetivo (--target) para usar frameworks")
            return 1
        elif not validate_framework(args.framework):
            return 1
    
    # Validar archivo de entrada
    if not validate_vader_file(args.archivo):
        return 1
    
    # Leer el código fuente
    try:
        with open(args.archivo, 'r', encoding='utf-8') as archivo:
            codigo = archivo.read()
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        return 1
    
    # 🌟 PROCESAMIENTO CONVERSACIONAL - HITO HISTÓRICO
    # Detectar y procesar sintaxis conversacional automáticamente
    is_conversational_file = detect_conversational_file(args.archivo)
    
    if is_conversational_file or args.archivo.endswith('.vdr-conv'):
        if args.verbose:
            print("🌟 VADER CONVERSACIONAL DETECTADO")
            print("Procesando sintaxis conversacional...")
        
        # Procesar con el parser conversacional
        codigo = integrate_conversational_with_vader(codigo, verbose=args.verbose)
        
        if args.verbose:
            print("✅ Conversión conversacional completada")
    
    if args.verbose:
        print(f"Archivo leído: {args.archivo}")
        print(f"Líneas de código: {len(codigo.splitlines())}")
    
    # Procesamiento multiidioma
    source_language = None
    
    # Detectar idioma automáticamente si se solicita
    if args.detect_language:
        source_language = detect_code_language(codigo)
    
    # Usar idioma especificado por el usuario
    if args.language:
        source_language = args.language
        if args.verbose:
            languages = multilingual_system.get_supported_languages()
            if source_language in languages:
                lang_info = languages[source_language]
                print(f"🌍 Idioma especificado: {lang_info['native_name']} ({lang_info['name']})")
    
    # Traducir código si se especifica idioma objetivo diferente
    if args.translate_to:
        if not source_language:
            source_language = multilingual_system.detect_language(codigo)
            print(f"🔍 Idioma detectado automáticamente: {source_language}")
        
        translated_code = translate_code_language(codigo, source_language, args.translate_to)
        if translated_code:
            codigo = translated_code
            # Actualizar idioma fuente para el resto del procesamiento
            source_language = args.translate_to
            
            # Guardar código traducido si se especifica output
            if args.output:
                translated_file = args.output.replace('.vdr', f'_{args.translate_to}.vdr') if args.output.endswith('.vdr') else args.output + f'_{args.translate_to}.vdr'
                try:
                    with open(translated_file, 'w', encoding='utf-8') as f:
                        f.write(codigo)
                    print(f"💾 Código traducido guardado en: {translated_file}")
                except Exception as e:
                    print(f"❌ Error al guardar código traducido: {e}")
        else:
            return 1
    
    # Normalizar código a español (idioma base) para transpilación
    if source_language and source_language != 'es':
        if args.verbose:
            print(f"🔄 Normalizando código de {source_language} a español para transpilación...")
        codigo = multilingual_system.normalize_to_spanish(codigo, source_language)
    
    # Manejar comandos de IA con archivo existente
    if args.ai_analyze:
        if handle_ai_analyze(codigo, detailed=args.ai_detailed):
            if not args.target:  # Solo análisis, no transpilación
                return 0
    
    if args.ai_check_errors:
        try:
            from transpilers.ai_assistant import VaderAIAssistant
            ai = VaderAIAssistant()
            errors = ai.check_errors(codigo)
            if errors:
                print("❌ ERRORES DETECTADOS POR IA:")
                for error in errors:
                    print(f"  • {error}")
                return 1
            else:
                print("✅ No se detectaron errores con IA")
                if not args.target:  # Solo verificación, no transpilación
                    return 0
        except ImportError:
            print("❌ Error: Sistema de IA no disponible")
            return 1
    
    if args.ai_suggest:
        try:
            from transpilers.ai_assistant import VaderAIAssistant
            ai = VaderAIAssistant()
            sugerencias = ai.suggest_improvements(codigo)
            if sugerencias:
                print("💡 SUGERENCIAS DE MEJORA:")
                for sugerencia in sugerencias:
                    print(f"  • {sugerencia}")
            else:
                print("ℹ️  No se encontraron sugerencias de mejora")
            if not args.target:  # Solo sugerencias, no transpilación
                return 0
        except ImportError:
            print("❌ Error: Sistema de IA no disponible")
            return 1
    
    if args.ai_optimize:
        codigo_original = codigo
        codigo = handle_ai_optimize(codigo)
        if codigo != codigo_original and args.output:
            # Guardar código optimizado
            optimized_file = args.output.replace('.vdr', '_optimizado.vdr') if args.output.endswith('.vdr') else args.output + '_optimizado.vdr'
            try:
                with open(optimized_file, 'w', encoding='utf-8') as f:
                    f.write(codigo)
                print(f"💾 Código optimizado guardado en: {optimized_file}")
            except Exception as e:
                print(f"❌ Error al guardar código optimizado: {e}")
    
    # Verificar sintaxis si se solicita
    if args.check_syntax:
        errors, warnings = check_syntax(codigo, args.verbose)
        
        if warnings:
            print("Advertencias:")
            for warning in warnings:
                print(f"  ⚠️  {warning}")
        
        if errors:
            print("Errores de sintaxis:")
            for error in errors:
                print(f"  ❌ {error}")
            return 1
        else:
            print("✅ Sintaxis correcta")
            return 0
    
    # Transpilar el código
    resultado = transpile_code(codigo, args.target, framework=args.framework, verbose=args.verbose)
    if resultado is None:
        return 1
    
    # Guardar o imprimir el resultado
    if args.output:
        if save_output(resultado, args.output, args.target):
            return 0
        else:
            return 1
    else:
        print(resultado)
        return 0

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code if exit_code is not None else 0)
    except KeyboardInterrupt:
        print("\n⚠️  Operación cancelada por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        sys.exit(1)
