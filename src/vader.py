#!/usr/bin/env python3

import sys
import os
import argparse
import json
from pathlib import Path

# Agregar el directorio raíz al path para que encuentre el módulo transpilers
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from transpilers import python, javascript, java, csharp, go, rust, swift, kotlin

# Versión de Vader
VADER_VERSION = "1.0.0"

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
    
    return parser

def list_supported_targets():
    """Lista todos los lenguajes objetivo soportados"""
    print("Lenguajes objetivo soportados:")
    print("=" * 40)
    for key, info in SUPPORTED_LANGUAGES.items():
        print(f"  {key:<12} - {info['description']} (extensión: {info['extension']})")
    print()

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

def transpile_code(codigo, target_lang, verbose=False):
    """Transpila el código Vader al lenguaje objetivo"""
    if verbose:
        print(f"Transpilando a {SUPPORTED_LANGUAGES[target_lang]['description']}...")
    
    try:
        transpiler = SUPPORTED_LANGUAGES[target_lang]['transpiler']
        if target_lang == "go" or target_lang == "golang":
            resultado = go.transpilar(codigo)
        elif target_lang == "rust" or target_lang == "rs":
            resultado = rust.transpilar(codigo)
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

def main():
    """Función principal del transpilador Vader"""
    parser = create_argument_parser()
    args = parser.parse_args()
    
    # Listar lenguajes objetivo si se solicita
    if args.list_targets:
        list_supported_targets()
        return 0
    
    # Validar que se proporcionaron los argumentos necesarios
    if not args.archivo:
        print("Error: Se requiere especificar un archivo .vdr")
        parser.print_help()
        return 1
        
    # Solo requerir target si no es verificación de sintaxis
    if not args.check_syntax and not args.target:
        print("Error: Se requiere especificar un lenguaje objetivo con --target")
        parser.print_help()
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
    
    if args.verbose:
        print(f"Archivo leído: {args.archivo}")
        print(f"Líneas de código: {len(codigo.splitlines())}")
    
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
    resultado = transpile_code(codigo, args.target, args.verbose)
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
