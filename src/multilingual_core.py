#!/usr/bin/env python3
"""
VADER MULTILINGUAL CORE SYSTEM
Sistema central multiidioma para Vader - El primer lenguaje de programación universal
que permite programar en español, inglés, francés, portugués, italiano, chino, japonés, ruso y más.

Arquitectura revolucionaria que democratiza la programación a nivel mundial.
"""

import json
import os
import re
from typing import Dict, List, Optional, Tuple
from pathlib import Path

class VaderMultilingualCore:
    """Sistema central multiidioma de Vader"""
    
    def __init__(self):
        self.languages_dir = Path(__file__).parent / "languages"
        self.supported_languages = {}
        self.current_language = "es"  # Español por defecto
        self.load_all_languages()
    
    def load_all_languages(self):
        """Carga todos los idiomas soportados"""
        if not self.languages_dir.exists():
            self.languages_dir.mkdir(exist_ok=True)
        
        # Cargar idiomas desde archivos JSON
        for lang_file in self.languages_dir.glob("*.json"):
            lang_code = lang_file.stem
            try:
                with open(lang_file, 'r', encoding='utf-8') as f:
                    self.supported_languages[lang_code] = json.load(f)
            except Exception as e:
                print(f"Error cargando idioma {lang_code}: {e}")
    
    def detect_language(self, code: str) -> str:
        """Detecta automáticamente el idioma del código"""
        # Contar palabras clave de cada idioma
        language_scores = {}
        
        for lang_code, lang_data in self.supported_languages.items():
            score = 0
            keywords = lang_data.get('keywords', {})
            
            # Contar coincidencias de palabras clave
            for category, words in keywords.items():
                for word in words:
                    # Usar regex para buscar palabras completas
                    pattern = r'\b' + re.escape(word) + r'\b'
                    matches = len(re.findall(pattern, code, re.IGNORECASE))
                    score += matches
            
            language_scores[lang_code] = score
        
        # Retornar el idioma con mayor puntuación
        if language_scores:
            detected_lang = max(language_scores, key=language_scores.get)
            if language_scores[detected_lang] > 0:
                return detected_lang
        
        return "es"  # Español por defecto
    
    def translate_code(self, code: str, source_lang: str, target_lang: str) -> str:
        """Traduce código de un idioma a otro"""
        if source_lang == target_lang:
            return code
        
        if source_lang not in self.supported_languages:
            raise ValueError(f"Idioma fuente no soportado: {source_lang}")
        
        if target_lang not in self.supported_languages:
            raise ValueError(f"Idioma objetivo no soportado: {target_lang}")
        
        source_keywords = self.supported_languages[source_lang]['keywords']
        target_keywords = self.supported_languages[target_lang]['keywords']
        
        translated_code = code
        
        # Traducir por categorías de palabras clave
        for category in source_keywords:
            if category in target_keywords:
                source_words = source_keywords[category]
                target_words = target_keywords[category]
                
                # Mapear palabras fuente a objetivo
                for i, source_word in enumerate(source_words):
                    if i < len(target_words):
                        target_word = target_words[i]
                        # Reemplazar palabra completa
                        pattern = r'\b' + re.escape(source_word) + r'\b'
                        translated_code = re.sub(
                            pattern, target_word, translated_code, flags=re.IGNORECASE
                        )
        
        return translated_code
    
    def normalize_to_spanish(self, code: str, source_lang: str = None) -> str:
        """Normaliza código de cualquier idioma a español (idioma base)"""
        if source_lang is None:
            source_lang = self.detect_language(code)
        
        return self.translate_code(code, source_lang, "es")
    
    def get_supported_languages(self) -> Dict:
        """Retorna todos los idiomas soportados con metadatos"""
        result = {}
        for lang_code, lang_data in self.supported_languages.items():
            result[lang_code] = {
                'name': lang_data.get('name', lang_code),
                'native_name': lang_data.get('native_name', lang_code),
                'direction': lang_data.get('direction', 'ltr'),
                'encoding': lang_data.get('encoding', 'utf-8'),
                'keywords_count': sum(len(words) for words in lang_data.get('keywords', {}).values())
            }
        return result
    
    def validate_multilingual_syntax(self, code: str, lang: str = None) -> Tuple[List[str], List[str]]:
        """Valida sintaxis multiidioma"""
        if lang is None:
            lang = self.detect_language(code)
        
        errors = []
        warnings = []
        
        if lang not in self.supported_languages:
            errors.append(f"Idioma no soportado: {lang}")
            return errors, warnings
        
        # Validaciones básicas
        lang_data = self.supported_languages[lang]
        keywords = lang_data.get('keywords', {})
        
        # Verificar estructura básica
        if 'control_flow' in keywords:
            if_words = keywords['control_flow'][:3]  # si, sino, fin si
            for if_word in if_words[:1]:  # solo 'si'
                if_pattern = r'\b' + re.escape(if_word) + r'\b'
                if_matches = re.findall(if_pattern, code, re.IGNORECASE)
                
                # Verificar que cada 'si' tenga su 'fin si' correspondiente
                end_word = if_words[-1] if len(if_words) > 2 else "fin " + if_word
                end_pattern = r'\b' + re.escape(end_word) + r'\b'
                end_matches = re.findall(end_pattern, code, re.IGNORECASE)
                
                if len(if_matches) != len(end_matches):
                    warnings.append(f"Posible desbalance en estructuras condicionales ({if_word})")
        
        return errors, warnings
    
    def get_language_info(self, lang_code: str) -> Optional[Dict]:
        """Obtiene información detallada de un idioma"""
        return self.supported_languages.get(lang_code)
    
    def create_language_template(self, lang_code: str, lang_name: str, native_name: str) -> Dict:
        """Crea plantilla para nuevo idioma"""
        return {
            "name": lang_name,
            "native_name": native_name,
            "code": lang_code,
            "direction": "ltr",
            "encoding": "utf-8",
            "keywords": {
                "basic": ["mostrar", "decir", "preguntar", "guardar"],
                "data_types": ["numero", "texto", "booleano", "lista"],
                "control_flow": ["si", "sino", "fin si", "repetir", "fin repetir"],
                "functions": ["funcion", "devolver", "fin funcion"],
                "classes": ["clase", "fin clase", "atributo", "metodo"],
                "operators": ["y", "o", "no", "es igual a", "es mayor que", "es menor que"],
                "loops": ["repetir", "fin repetir", "para cada", "mientras"],
                "file_operations": ["leer archivo", "escribir archivo", "abrir", "cerrar"],
                "advanced": ["intentar", "capturar", "finalmente", "lanzar"]
            },
            "examples": {
                "hello_world": f'decir "¡Hola mundo en {native_name}!"',
                "variable": "guardar nombre = \"Usuario\"",
                "function": "funcion saludar:\n    decir \"¡Hola!\"\nfin funcion",
                "conditional": "si edad >= 18:\n    decir \"Eres mayor de edad\"\nfin si"
            }
        }

# Instancia global del sistema multiidioma
multilingual_system = VaderMultilingualCore()
