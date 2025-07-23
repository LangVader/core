#!/usr/bin/env python3
"""
🌟 INTEGRACIÓN VADER CONVERSACIONAL
Integra el parser conversacional con el sistema principal de Vader

Creado por: El hombre que enseñó al mundo a programar
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from transpilers.conversational import process_conversational_vader

def integrate_conversational_with_vader(content: str, verbose: bool = False) -> str:
    """
    Integra el procesamiento conversacional con Vader principal
    
    Args:
        content: Contenido del archivo .vdr
        verbose: Si mostrar información detallada
    
    Returns:
        str: Contenido procesado listo para Vader estándar
    """
    
    # Procesar con parser conversacional
    processed_content, conversion_info = process_conversational_vader(content)
    
    if verbose and conversion_info["converted"]:
        print("🌟 VADER CONVERSACIONAL ACTIVADO")
        print("=" * 40)
        print(f"📋 Dominio detectado: {conversion_info.get('detected_domain', 'General')}")
        print(f"🔍 Indicadores encontrados: {len(conversion_info['indicators_found'])}")
        print(f"✅ Conversión realizada: {conversion_info['converted']}")
        print("=" * 40)
        
        if conversion_info['indicators_found']:
            print("🎯 Patrones conversacionales detectados:")
            for indicator in conversion_info['indicators_found'][:5]:  # Mostrar máximo 5
                print(f"   • {indicator}")
        print()
    
    return processed_content

def detect_conversational_file(filepath: str) -> bool:
    """Detecta si un archivo es conversacional basado en extensión o contenido"""
    
    # Detectar por extensión
    if filepath.endswith('.vdr-conv'):
        return True
    
    # Detectar por contenido si es .vdr normal
    if filepath.endswith('.vdr'):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                from transpilers.conversational import VaderConversationalParser
                parser = VaderConversationalParser()
                return parser.detect_conversational_syntax(content)
        except:
            return False
    
    return False
