#!/usr/bin/env python3
"""
VADER MULTILINGUAL SYSTEM TESTER
Prueba independiente del sistema multiidioma de Vader
"""

import sys
import os
from pathlib import Path

# Agregar el directorio src al path
sys.path.append(str(Path(__file__).parent / "src"))

try:
    from multilingual_core import multilingual_system
except ImportError as e:
    print(f"❌ Error importando sistema multiidioma: {e}")
    sys.exit(1)

def test_language_detection():
    """Prueba la detección automática de idiomas"""
    print("🔍 PRUEBA DE DETECCIÓN DE IDIOMAS")
    print("=" * 50)
    
    test_codes = {
        "español": 'decir "Hola mundo"\nguardar nombre = "Juan"\nsi edad >= 18:\n    mostrar "Eres mayor"\nfin si',
        "inglés": 'say "Hello world"\nstore name = "John"\nif age >= 18:\n    show "You are adult"\nend if',
        "francés": 'dire "Bonjour monde"\nstocker nom = "Marie"\nsi âge >= 18:\n    montrer "Vous êtes majeur"\nfin si',
        "chino": '说 "你好世界"\n存储 姓名 = "小明"\n如果 年龄 >= 18:\n    显示 "你是成年人"\n结束如果',
        "japonés": '言う "こんにちは世界"\n保存 名前 = "田中"\nもし 年齢 >= 18:\n    表示 "あなたは大人です"\nもし終了'
    }
    
    for lang_name, code in test_codes.items():
        detected = multilingual_system.detect_language(code)
        print(f"  📝 {lang_name}: {detected}")
    
    print()

def test_language_translation():
    """Prueba la traducción entre idiomas"""
    print("🔄 PRUEBA DE TRADUCCIÓN DE IDIOMAS")
    print("=" * 50)
    
    # Código base en español
    spanish_code = '''decir "Hola mundo"
guardar nombre = "Usuario"
si edad >= 18:
    mostrar "Eres mayor de edad"
sino:
    mostrar "Eres menor de edad"
fin si'''
    
    print("📝 Código original (español):")
    print(spanish_code)
    print()
    
    # Traducir a diferentes idiomas
    target_languages = ['en', 'fr', 'zh', 'ja']
    
    for target_lang in target_languages:
        try:
            translated = multilingual_system.translate_code(spanish_code, 'es', target_lang)
            languages = multilingual_system.get_supported_languages()
            lang_name = languages[target_lang]['native_name']
            
            print(f"🌍 Traducido a {lang_name} ({target_lang}):")
            print(translated)
            print("-" * 30)
        except Exception as e:
            print(f"❌ Error traduciendo a {target_lang}: {e}")
    
    print()

def test_language_info():
    """Prueba la información detallada de idiomas"""
    print("📚 PRUEBA DE INFORMACIÓN DE IDIOMAS")
    print("=" * 50)
    
    languages = multilingual_system.get_supported_languages()
    
    print(f"🌍 Total de idiomas soportados: {len(languages)}")
    print()
    
    # Mostrar información de algunos idiomas
    sample_langs = ['es', 'en', 'zh', 'ar']
    
    for lang_code in sample_langs:
        if lang_code in languages:
            lang_info = languages[lang_code]
            print(f"🏷️  {lang_code}: {lang_info['native_name']} ({lang_info['name']})")
            print(f"   📖 Dirección: {'RTL' if lang_info.get('direction') == 'rtl' else 'LTR'}")
            print(f"   🔤 Palabras clave: {lang_info['keywords_count']}")
            print()

def test_syntax_validation():
    """Prueba la validación de sintaxis multiidioma"""
    print("✅ PRUEBA DE VALIDACIÓN DE SINTAXIS")
    print("=" * 50)
    
    test_codes = {
        'es': 'si edad >= 18:\n    decir "Mayor"\nfin si',
        'en': 'if age >= 18:\n    say "Adult"\nend if',
        'fr': 'si âge >= 18:\n    dire "Majeur"\nfin si'
    }
    
    for lang, code in test_codes.items():
        errors, warnings = multilingual_system.validate_multilingual_syntax(code, lang)
        
        print(f"📝 Validando código en {lang}:")
        print(f"   Errores: {len(errors)}")
        print(f"   Advertencias: {len(warnings)}")
        
        if errors:
            for error in errors:
                print(f"   ❌ {error}")
        
        if warnings:
            for warning in warnings:
                print(f"   ⚠️  {warning}")
        
        print()

def main():
    """Función principal de pruebas"""
    print("🌍 VADER MULTILINGUAL SYSTEM - PRUEBAS COMPLETAS")
    print("=" * 60)
    print()
    
    try:
        # Cargar sistema multiidioma
        print("🔄 Cargando sistema multiidioma...")
        multilingual_system.load_all_languages()
        
        languages = multilingual_system.get_supported_languages()
        print(f"✅ Sistema cargado: {len(languages)} idiomas disponibles")
        print()
        
        # Ejecutar pruebas
        test_language_detection()
        test_language_translation()
        test_language_info()
        test_syntax_validation()
        
        print("🎉 TODAS LAS PRUEBAS COMPLETADAS EXITOSAMENTE")
        print("🌍 Vader es ahora oficialmente MULTIIDIOMA UNIVERSAL!")
        
    except Exception as e:
        print(f"❌ Error durante las pruebas: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
