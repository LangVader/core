#!/usr/bin/env python3
"""
🌍 VADER MULTILENGUAJE COMPLETO - SISTEMA AVANZADO
================================================

Sistema multilenguaje completo que traduce:
- Keywords y sintaxis
- Strings y cadenas de texto
- Variables y nombres
- Comentarios y documentación
- Mensajes de error y salida

Soporta 20+ idiomas con traducción completa.

Autor: Adriano & Cascade AI
Versión: 8.0 Multilanguage Complete
"""

import json
import re
import time
import logging
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass
from googletrans import Translator
import requests

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class TranslationResult:
    """Resultado de traducción completa"""
    success: bool
    original_code: str
    translated_code: str
    source_language: str
    target_language: str
    translation_time: float
    elements_translated: int

class VaderMultilanguageComplete:
    """Sistema multilenguaje completo de Vader"""
    
    def __init__(self):
        logger.info("🌍 Iniciando Sistema Multilenguaje Completo...")
        
        # Inicializar traductor
        try:
            self.translator = Translator()
            self.translation_available = True
        except:
            self.translation_available = False
            logger.warning("⚠️ Google Translate no disponible, usando traducciones locales")
        
        # Cache de traducciones
        self.translation_cache = {}
        
        # Idiomas soportados con códigos ISO
        self.supported_languages = {
            'es': 'Español',
            'en': 'English', 
            'fr': 'Français',
            'de': 'Deutsch',
            'it': 'Italiano',
            'pt': 'Português',
            'ru': 'Русский',
            'ar': 'العربية',
            'zh': '中文',
            'ja': '日本語',
            'ko': '한국어',
            'hi': 'हिन्दी',
            'th': 'ไทย',
            'vi': 'Tiếng Việt',
            'tr': 'Türkçe',
            'nl': 'Nederlands',
            'sv': 'Svenska',
            'id': 'Bahasa Indonesia',
            'sw': 'Kiswahili',
            'pl': 'Polski',
            'cs': 'Čeština',
            'hu': 'Magyar',
            'ro': 'Română',
            'bg': 'Български',
            'hr': 'Hrvatski'
        }
        
        # Keywords base en español
        self.base_keywords = {
            'decir': ['say', 'dire', 'sagen', 'dire', 'dizer', 'сказать', 'قول', '说', '言う', '말하다', 'कहना'],
            'si': ['if', 'si', 'wenn', 'se', 'se', 'если', 'إذا', '如果', 'もし', '만약', 'अगर'],
            'sino': ['else', 'sinon', 'sonst', 'altrimenti', 'senão', 'иначе', 'وإلا', '否则', 'そうでなければ', '그렇지않으면', 'अन्यथा'],
            'mientras': ['while', 'pendant', 'während', 'mentre', 'enquanto', 'пока', 'بينما', '当', 'の間', '동안', 'जबकि'],
            'para': ['for', 'pour', 'für', 'per', 'para', 'для', 'لـ', '为了', 'のために', '위해', 'के लिए'],
            'funcion': ['function', 'fonction', 'funktion', 'funzione', 'função', 'функция', 'وظيفة', '函数', '関数', '함수', 'फ़ंक्शन'],
            'clase': ['class', 'classe', 'klasse', 'classe', 'classe', 'класс', 'فئة', '类', 'クラス', '클래스', 'वर्ग'],
            'importar': ['import', 'importer', 'importieren', 'importare', 'importar', 'импорт', 'استيراد', '导入', 'インポート', '가져오기', 'आयात'],
            'retornar': ['return', 'retourner', 'zurückgeben', 'ritornare', 'retornar', 'вернуть', 'إرجاع', '返回', '戻る', '반환', 'वापसी'],
            'verdadero': ['true', 'vrai', 'wahr', 'vero', 'verdadeiro', 'истина', 'صحيح', '真', '真', '참', 'सच'],
            'falso': ['false', 'faux', 'falsch', 'falso', 'falso', 'ложь', 'خطأ', '假', '偽', '거짓', 'झूठा']
        }
        
        # Patrones de strings y variables
        self.string_patterns = [
            r'"([^"]*)"',  # Strings con comillas dobles
            r"'([^']*)'",  # Strings con comillas simples
            r'`([^`]*)`',  # Template strings
            r'f"([^"]*)"', # F-strings
            r"f'([^']*)'"  # F-strings con comillas simples
        ]
        
        # Patrones de variables y nombres
        self.variable_patterns = [
            r'\b([a-zA-Z_][a-zA-Z0-9_]*)\s*=',  # Asignaciones
            r'def\s+([a-zA-Z_][a-zA-Z0-9_]*)',   # Definiciones de función
            r'class\s+([a-zA-Z_][a-zA-Z0-9_]*)', # Definiciones de clase
            r'([a-zA-Z_][a-zA-Z0-9_]*)\s*\(',    # Llamadas a función
        ]
        
        # Diccionarios de traducción locales
        self._load_local_translations()
        
        logger.info("✅ Sistema Multilenguaje Completo iniciado")
    
    def _load_local_translations(self):
        """Cargar traducciones locales para casos sin internet"""
        self.local_translations = {
            'common_strings': {
                'es': {
                    'Hola mundo': {'en': 'Hello world', 'fr': 'Bonjour monde', 'de': 'Hallo Welt'},
                    'Bienvenido': {'en': 'Welcome', 'fr': 'Bienvenue', 'de': 'Willkommen'},
                    'Error': {'en': 'Error', 'fr': 'Erreur', 'de': 'Fehler'},
                    'Éxito': {'en': 'Success', 'fr': 'Succès', 'de': 'Erfolg'},
                    'Procesando': {'en': 'Processing', 'fr': 'Traitement', 'de': 'Verarbeitung'},
                    'Completado': {'en': 'Completed', 'fr': 'Terminé', 'de': 'Abgeschlossen'},
                    'Iniciando': {'en': 'Starting', 'fr': 'Démarrage', 'de': 'Starten'},
                    'Conectando': {'en': 'Connecting', 'fr': 'Connexion', 'de': 'Verbinden'},
                    'Datos': {'en': 'Data', 'fr': 'Données', 'de': 'Daten'},
                    'Resultado': {'en': 'Result', 'fr': 'Résultat', 'de': 'Ergebnis'}
                }
            },
            'common_variables': {
                'es': {
                    'nombre': {'en': 'name', 'fr': 'nom', 'de': 'name'},
                    'edad': {'en': 'age', 'fr': 'age', 'de': 'alter'},
                    'email': {'en': 'email', 'fr': 'email', 'de': 'email'},
                    'usuario': {'en': 'user', 'fr': 'utilisateur', 'de': 'benutzer'},
                    'contraseña': {'en': 'password', 'fr': 'mot_de_passe', 'de': 'passwort'},
                    'datos': {'en': 'data', 'fr': 'donnees', 'de': 'daten'},
                    'resultado': {'en': 'result', 'fr': 'resultat', 'de': 'ergebnis'},
                    'archivo': {'en': 'file', 'fr': 'fichier', 'de': 'datei'},
                    'servidor': {'en': 'server', 'fr': 'serveur', 'de': 'server'},
                    'cliente': {'en': 'client', 'fr': 'client', 'de': 'kunde'}
                }
            }
        }
    
    def detect_language(self, code: str) -> str:
        """Detectar idioma del código"""
        # Contar keywords en diferentes idiomas
        language_scores = {}
        
        for lang_code in self.supported_languages:
            score = 0
            
            # Verificar keywords
            for spanish_keyword, translations in self.base_keywords.items():
                if lang_code == 'es':
                    if spanish_keyword in code.lower():
                        score += 1
                else:
                    lang_index = ['en', 'fr', 'de', 'it', 'pt', 'ru', 'ar', 'zh', 'ja', 'ko', 'hi'].index(lang_code) if lang_code in ['en', 'fr', 'de', 'it', 'pt', 'ru', 'ar', 'zh', 'ja', 'ko', 'hi'] else 0
                    if lang_index < len(translations) and translations[lang_index] in code.lower():
                        score += 1
            
            language_scores[lang_code] = score
        
        # Retornar idioma con mayor puntuación
        detected_lang = max(language_scores, key=language_scores.get)
        return detected_lang if language_scores[detected_lang] > 0 else 'es'
    
    def translate_string(self, text: str, source_lang: str, target_lang: str) -> str:
        """Traducir string individual"""
        if source_lang == target_lang:
            return text
        
        # Verificar cache
        cache_key = f"{text}:{source_lang}:{target_lang}"
        if cache_key in self.translation_cache:
            return self.translation_cache[cache_key]
        
        # Intentar traducción local primero
        if source_lang in self.local_translations['common_strings']:
            local_dict = self.local_translations['common_strings'][source_lang]
            if text in local_dict and target_lang in local_dict[text]:
                translated = local_dict[text][target_lang]
                self.translation_cache[cache_key] = translated
                return translated
        
        # Usar Google Translate si está disponible
        if self.translation_available:
            try:
                result = self.translator.translate(text, src=source_lang, dest=target_lang)
                translated = result.text
                self.translation_cache[cache_key] = translated
                return translated
            except Exception as e:
                logger.warning(f"Error en Google Translate: {e}")
        
        # Fallback: retornar texto original
        return text
    
    def translate_variable_name(self, var_name: str, source_lang: str, target_lang: str) -> str:
        """Traducir nombre de variable"""
        if source_lang == target_lang:
            return var_name
        
        # Verificar traducciones locales de variables
        if source_lang in self.local_translations['common_variables']:
            local_dict = self.local_translations['common_variables'][source_lang]
            if var_name.lower() in local_dict and target_lang in local_dict[var_name.lower()]:
                return local_dict[var_name.lower()]
        
        # Para nombres compuestos, traducir cada parte
        if '_' in var_name:
            parts = var_name.split('_')
            translated_parts = []
            for part in parts:
                translated_part = self.translate_string(part, source_lang, target_lang)
                translated_parts.append(translated_part.lower().replace(' ', '_'))
            return '_'.join(translated_parts)
        
        # Traducir nombre simple
        translated = self.translate_string(var_name, source_lang, target_lang)
        return translated.lower().replace(' ', '_')
    
    def translate_keywords(self, code: str, source_lang: str, target_lang: str) -> str:
        """Traducir keywords del código"""
        if source_lang == target_lang:
            return code
        
        translated_code = code
        
        # Traducir cada keyword
        for spanish_keyword, translations in self.base_keywords.items():
            if source_lang == 'es':
                source_keyword = spanish_keyword
            else:
                # Encontrar keyword en idioma fuente
                lang_codes = ['en', 'fr', 'de', 'it', 'pt', 'ru', 'ar', 'zh', 'ja', 'ko', 'hi']
                if source_lang in lang_codes:
                    lang_index = lang_codes.index(source_lang)
                    source_keyword = translations[lang_index] if lang_index < len(translations) else spanish_keyword
                else:
                    source_keyword = spanish_keyword
            
            # Encontrar keyword en idioma destino
            if target_lang == 'es':
                target_keyword = spanish_keyword
            else:
                if target_lang in lang_codes:
                    lang_index = lang_codes.index(target_lang)
                    target_keyword = translations[lang_index] if lang_index < len(translations) else spanish_keyword
                else:
                    target_keyword = spanish_keyword
            
            # Reemplazar keyword (palabra completa)
            pattern = r'\b' + re.escape(source_keyword) + r'\b'
            translated_code = re.sub(pattern, target_keyword, translated_code, flags=re.IGNORECASE)
        
        return translated_code
    
    def translate_strings_in_code(self, code: str, source_lang: str, target_lang: str) -> Tuple[str, int]:
        """Traducir todos los strings en el código"""
        if source_lang == target_lang:
            return code, 0
        
        translated_code = code
        strings_translated = 0
        
        # Traducir strings con diferentes patrones
        for pattern in self.string_patterns:
            matches = re.finditer(pattern, code)
            for match in matches:
                original_string = match.group(1)
                if original_string.strip():  # Solo traducir strings no vacíos
                    translated_string = self.translate_string(original_string, source_lang, target_lang)
                    
                    # Reemplazar en el código
                    old_full = match.group(0)
                    new_full = old_full.replace(original_string, translated_string)
                    translated_code = translated_code.replace(old_full, new_full, 1)
                    strings_translated += 1
        
        return translated_code, strings_translated
    
    def translate_variables_in_code(self, code: str, source_lang: str, target_lang: str) -> Tuple[str, int]:
        """Traducir nombres de variables en el código"""
        if source_lang == target_lang:
            return code, 0
        
        translated_code = code
        variables_translated = 0
        
        # Traducir variables con diferentes patrones
        for pattern in self.variable_patterns:
            matches = re.finditer(pattern, code)
            for match in matches:
                original_var = match.group(1)
                if original_var and not original_var.isupper():  # No traducir constantes
                    translated_var = self.translate_variable_name(original_var, source_lang, target_lang)
                    
                    if translated_var != original_var:
                        # Reemplazar todas las ocurrencias de la variable
                        var_pattern = r'\b' + re.escape(original_var) + r'\b'
                        translated_code = re.sub(var_pattern, translated_var, translated_code)
                        variables_translated += 1
        
        return translated_code, variables_translated
    
    def translate_comments(self, code: str, source_lang: str, target_lang: str) -> Tuple[str, int]:
        """Traducir comentarios en el código"""
        if source_lang == target_lang:
            return code, 0
        
        translated_code = code
        comments_translated = 0
        
        # Patrones de comentarios
        comment_patterns = [
            r'#\s*(.+)',      # Comentarios Python
            r'//\s*(.+)',     # Comentarios JavaScript/C++
            r'/\*\s*(.+?)\s*\*/', # Comentarios multi-línea
        ]
        
        for pattern in comment_patterns:
            matches = re.finditer(pattern, code, re.DOTALL)
            for match in matches:
                original_comment = match.group(1).strip()
                if original_comment:
                    translated_comment = self.translate_string(original_comment, source_lang, target_lang)
                    
                    # Reemplazar comentario
                    old_full = match.group(0)
                    new_full = old_full.replace(original_comment, translated_comment)
                    translated_code = translated_code.replace(old_full, new_full, 1)
                    comments_translated += 1
        
        return translated_code, comments_translated
    
    def translate_code_complete(self, code: str, source_lang: str, target_lang: str) -> TranslationResult:
        """Traducción completa del código"""
        start_time = time.time()
        
        if source_lang not in self.supported_languages or target_lang not in self.supported_languages:
            return TranslationResult(
                success=False,
                original_code=code,
                translated_code=code,
                source_language=source_lang,
                target_language=target_lang,
                translation_time=time.time() - start_time,
                elements_translated=0
            )
        
        try:
            translated_code = code
            total_elements = 0
            
            # 1. Traducir keywords
            translated_code = self.translate_keywords(translated_code, source_lang, target_lang)
            
            # 2. Traducir strings
            translated_code, strings_count = self.translate_strings_in_code(translated_code, source_lang, target_lang)
            total_elements += strings_count
            
            # 3. Traducir variables
            translated_code, vars_count = self.translate_variables_in_code(translated_code, source_lang, target_lang)
            total_elements += vars_count
            
            # 4. Traducir comentarios
            translated_code, comments_count = self.translate_comments(translated_code, source_lang, target_lang)
            total_elements += comments_count
            
            return TranslationResult(
                success=True,
                original_code=code,
                translated_code=translated_code,
                source_language=source_lang,
                target_language=target_lang,
                translation_time=time.time() - start_time,
                elements_translated=total_elements
            )
            
        except Exception as e:
            logger.error(f"Error en traducción completa: {e}")
            return TranslationResult(
                success=False,
                original_code=code,
                translated_code=code,
                source_language=source_lang,
                target_language=target_lang,
                translation_time=time.time() - start_time,
                elements_translated=0
            )
    
    def get_supported_languages(self) -> Dict[str, str]:
        """Obtener idiomas soportados"""
        return self.supported_languages.copy()
    
    def get_translation_stats(self) -> Dict[str, Any]:
        """Obtener estadísticas de traducción"""
        return {
            'cache_size': len(self.translation_cache),
            'supported_languages': len(self.supported_languages),
            'translation_service': 'Google Translate' if self.translation_available else 'Local',
            'local_strings': len(self.local_translations['common_strings'].get('es', {})),
            'local_variables': len(self.local_translations['common_variables'].get('es', {}))
        }

def demo_multilanguage_complete():
    """Demo completo del sistema multilenguaje"""
    print("🌍 VADER MULTILENGUAJE COMPLETO - DEMO")
    print("=" * 45)
    
    # Inicializar sistema
    multilang = VaderMultilanguageComplete()
    
    # Código de ejemplo en español
    spanish_code = '''
# Aplicación web simple
decir "Hola mundo desde Vader"

funcion saludar(nombre):
    mensaje = "Bienvenido " + nombre
    decir mensaje
    retornar verdadero

clase Usuario:
    def __init__(self, nombre, edad):
        self.nombre = nombre  # Nombre del usuario
        self.edad = edad      # Edad en años
    
    def presentarse(self):
        decir f"Hola, soy {self.nombre} y tengo {self.edad} años"

# Crear usuario
usuario = Usuario("Adriano", 25)
usuario.presentarse()

si usuario.edad >= 18:
    decir "Es mayor de edad"
sino:
    decir "Es menor de edad"
'''
    
    # Idiomas de prueba
    target_languages = ['en', 'fr', 'de', 'it', 'pt']
    
    print(f"📝 Código original (español):")
    print(spanish_code[:200] + "...")
    
    print(f"\n🔄 Traduciendo a {len(target_languages)} idiomas...")
    
    for target_lang in target_languages:
        lang_name = multilang.supported_languages[target_lang]
        print(f"\n🌐 Traduciendo a {lang_name} ({target_lang})...")
        
        result = multilang.translate_code_complete(spanish_code, 'es', target_lang)
        
        if result.success:
            print(f"✅ Traducción exitosa en {result.translation_time*1000:.2f}ms")
            print(f"📊 Elementos traducidos: {result.elements_translated}")
            print(f"📝 Muestra del código traducido:")
            print(result.translated_code[:150] + "...")
        else:
            print(f"❌ Error en traducción a {lang_name}")
    
    # Mostrar estadísticas
    stats = multilang.get_translation_stats()
    print(f"\n📊 ESTADÍSTICAS DEL SISTEMA:")
    for key, value in stats.items():
        print(f"   • {key}: {value}")
    
    print(f"\n🎉 ¡Sistema Multilenguaje Completo funcionando!")
    return True

if __name__ == "__main__":
    demo_multilanguage_complete()
