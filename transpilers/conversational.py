#!/usr/bin/env python3
"""
🌟 VADER CONVERSACIONAL - PARSER UNIVERSAL
El primer lenguaje de programación universal y conversacional de la historia

Creado por: El hombre que enseñó al mundo a programar
Fecha: 23 de Julio, 2025
Propósito: Democratizar la programación para toda la humanidad
"""

import re
import json
from typing import Dict, List, Tuple, Optional

class VaderConversationalParser:
    """
    Parser que convierte lenguaje natural español a sintaxis Vader estándar
    
    Características revolucionarias:
    - Sintaxis 100% conversacional
    - Sin errores de sintaxis posibles
    - Comprensible por cualquier persona
    - Universal para todos los dominios
    """
    
    def __init__(self):
        self.general_patterns = self._load_general_patterns()
        self.domain_patterns = self._load_domain_patterns()
        self.conversation_indicators = [
            "cuando", "entonces", "pregunta", "suma", "para cada",
            "si el", "si la", "muestra", "decir", "guárdalo",
            "calcula", "abre el", "lee el", "cierra el", "envía",
            "enciende", "apaga", "mueve", "gira", "ve hacia"
        ]
    
    def _load_general_patterns(self) -> List[Tuple[str, str]]:
        """Patrones conversacionales generales MEJORADOS"""
        return [
            # Condicionales naturales avanzados
            (r'cuando\s+(.+?)\s+(?:entonces|,)\s+(.+)', r'si \1 entonces\n\2'),
            (r'si\s+(.+?)\s+(?:entonces|,)\s+(.+)', r'si \1 entonces\n\2'),
            (r'mientras\s+(.+?)\s+(?:entonces|,)\s+(.+)', r'mientras \1\n\2'),
            
            # Variables y asignaciones mejoradas
            (r'(.+?)\s+se\s+llama\s+(.+?)\s+y\s+tiene\s+(.+?)\s+años', r'\1 = {"nombre": "\2", "edad": \3}'),
            (r'(.+?)\s+se\s+llama\s+(.+?)\s+y\s+(?:tiene|es)\s+(.+)', r'\1 = {"nombre": "\2", "valor": \3}'),
            (r'la\s+(.+?)\s+de\s+(.+?)\s+es\s+(.+?)\s+grados', r'\1_\2 = \3'),
            (r'la\s+(.+?)\s+(?:de\s+)?(.+?)\s+es\s+(.+)', r'\1_\2 = \3'),
            (r'mi\s+(.+?)\s+(?:incluye|contiene)\s+(.+)', r'\1 = [\2]'),
            (r'el\s+(.+?)\s+tiene\s+(.+?)\s+puntos', r'\1_puntos = \2'),
            
            # Preguntas y entrada de usuario mejoradas
            (r'pregunta\s+al\s+usuario\s+"(.+?)"\s+y\s+guárdalo\s+en\s+(.+)', r'\2 = input("\1")'),
            (r'pregunta\s+"(.+?)"\s+y\s+guárdalo\s+en\s+(.+)', r'\2 = input("\1")'),
            (r'pregunta\s+"(.+?)"\s+y\s+guarda\s+(?:la\s+)?respuesta\s+en\s+(.+)', r'\2 = input("\1")'),
            (r'pregunta\s+"(.+?)"\s+y\s+úsalo\s+como\s+(.+)', r'\2 = input("\1")'),
            
            # Matemáticas conversacionales avanzadas
            (r'suma\s+(.+?)\s+(?:más|\+)\s+(.+?)\s+y\s+guárdalo\s+en\s+(.+)', r'\3 = \1 + \2'),
            (r'resta\s+(.+?)\s+menos\s+(.+?)\s+y\s+guárdalo\s+en\s+(.+)', r'\3 = \1 - \2'),
            (r'multiplica\s+(.+?)\s+por\s+(.+?)\s+y\s+guárdalo\s+en\s+(.+)', r'\3 = \1 * \2'),
            (r'calcula\s+el\s+promedio\s+de\s+(.+?)\s+y\s+llámalo\s+(.+)', r'\2 = promedio(\1)'),
            (r'calcula\s+(.+?)\s+y\s+(?:guárdalo|llámalo)\s+(.+)', r'\2 = \1'),
            
            # Bucles naturales mejorados
            (r'para\s+cada\s+(.+?)\s+en\s+(?:mi\s+)?(?:lista\s+de\s+)?(.+)', r'repetir con cada \1 en \2'),
            (r'hazlo\s+(\d+)\s+veces', r'for _ in range(\1):'),
            (r'repite\s+(\d+)\s+veces', r'for _ in range(\1):'),
            (r'cada\s+(\d+)\s+(?:segundos|minutos)\s+(.+)', r'# Ejecutar cada \1: \2'),
            
            # Salida y mensajes mejorados
            (r'decir\s+"(.+?)"', r'mostrar "\1"'),
            (r'muestra\s+"(.+?)"', r'mostrar "\1"'),
            (r'muestra\s+(?:que\s+)?(.+?)\s+"(.+?)"', r'mostrar \1 + " \2"'),
            (r'muestra\s+(.+)', r'mostrar \1'),
            (r'imprime\s+(.+)', r'mostrar \1'),
            
            # Condicionales conversacionales adicionales
            (r'cuando (.*?) sea mayor a (\d+)', r'si \1 > \2 entonces'),
            (r'cuando (.*?) sea menor a (\d+)', r'si \1 < \2 entonces'),
            (r'cuando (.*?) sea igual a (.+?)', r'si \1 == \2 entonces'),
            
            # Matemáticas conversacionales adicionales
            (r'suma (.*?) más (.+?) y guárdalo en (.+)', r'\3 = \1 + \2'),
            (r'resta (.*?) menos (.+?) y guárdalo en (.+)', r'\3 = \1 - \2'),
            (r'multiplica (.*?) por (.+?) y guárdalo en (.+)', r'\3 = \1 * \2'),
            (r'divide (.*?) entre (.+?) y guárdalo en (.+)', r'\3 = \1 / \2'),
            
            # Mostrar información adicional
            (r'dile al usuario (.+)', r'mostrar \1'),
            (r'explica que (.+)', r'mostrar \1'),
            
            # Bucles conversacionales adicionales
            (r'repite (\d+) veces', r'repetir \1 veces'),
            (r'mientras (.+?)', r'repetir mientras \1'),
            (r'continúa hasta que (.+?)', r'repetir hasta \1'),
            
            # Variables conversacionales adicionales
            (r'mi lista de (.+?) incluye (.+)', r'lista_\1 = [\2]'),
            
            # Archivos conversacionales
            (r'abre el archivo "(.+?)" para leer', r'archivo = abrir("\1", "r")'),
            (r'lee todo el contenido y guárdalo en (.+)', r'\1 = archivo.leer()'),
            (r'cierra el archivo cuando termines', r'archivo.cerrar()'),
            (r'guarda (.+?) en el archivo "(.+?)"', r'escribir_archivo("\2", \1)'),
            
            # Funciones conversacionales
            (r'para (.+?) necesito (.+?)', r'funcion \1(\2):'),
            (r'devuelve (.+?)', r'retornar \1'),
            
            # Manejo de errores conversacional
            (r'si hay un error entonces (.+)', r'try:\n    # código\nexcept:\n    \1'),
            (r'si algo sale mal entonces (.+)', r'try:\n    # código\nexcept:\n    \1')
        ]
    
    def _load_domain_patterns(self) -> Dict[str, Dict[str, str]]:
        """Patrones específicos por dominio"""
        return {
            "iot": {
                r"enciende (.+)": r"encender(\1)",
                r"apaga (.+)": r"apagar(\1)",
                r"lee el sensor (.+)": r"leer_sensor(\1)",
                r"si detectas (.+?) entonces (.+)": r"si detectar(\1) entonces\n    \2",
                r"cuando la temperatura sea mayor a (\d+) grados entonces (.+)": r"si temperatura > \1 entonces\n    \2",
            },
            
            "web": {
                r'crea una página web que diga "(.+?)"': r'pagina "\1"',
                r"cuando el usuario haga click en (.+?) entonces (.+)": r"al_hacer_click(\1, \2)",
                r"muestra una alerta con (.+)": r"alerta(\1)",
                r"crea un botón que diga (.+)": r"boton(\1)",
            },
            
            "robotics": {
                r"mueve el robot hacia (.+?) por (\d+) segundos": r"mover(\1, \2)",
                r"si hay un obstáculo entonces (.+)": r"si detectar_obstaculo() entonces\n    \1",
                r"gira a la (.+)": r"girar(\1)",
                r"cuando veas (.+?) entonces (.+)": r"si detectar(\1) entonces\n    \2",
            },
            
            "mobile": {
                r"crea una app que tenga (.+)": r"app_crear(\1)",
                r"cuando toquen (.+?) entonces (.+)": r"al_tocar(\1, \2)",
                r"vibra el teléfono": r"vibrar()",
                r"guarda (.+?) en el teléfono": r"guardar_local(\1)",
            },
            
            "ai": {
                r'pregunta a la IA "(.+?)"': r'consultar_ia("\1")',
                r"analiza (.+?) y dime (.+)": r"analizar_con_ia(\1, \2)",
                r"genera (.+?) de (.+)": r"generar_con_ia(\1, \2)",
            },
            
            "gaming": {
                r"crea un personaje que (.+)": r"personaje.crear(\1)",
                r"cuando presionen (.+?) entonces (.+)": r"al_presionar(\1, \2)",
                r"si el jugador (.+?) entonces (.+)": r"si jugador.\1 entonces\n    \2",
                r"suma (\d+) puntos": r"puntos += \1",
            }
        }
    
    def detect_conversational_syntax(self, content: str) -> bool:
        """Detecta si el contenido usa sintaxis conversacional"""
        content_lower = content.lower()
        indicator_count = sum(1 for indicator in self.conversation_indicators 
                            if indicator in content_lower)
        
        # Si tiene 2 o más indicadores conversacionales, es conversacional
        return indicator_count >= 2
    
    def detect_domain(self, content: str) -> Optional[str]:
        """Detecta el dominio basado en palabras clave"""
        content_lower = content.lower()
        
        domain_keywords = {
            "iot": ["sensor", "temperatura", "enciende", "apaga", "arduino", "raspberry"],
            "web": ["página", "botón", "click", "formulario", "alerta", "navegador"],
            "robotics": ["robot", "mueve", "gira", "obstáculo", "detectar", "navegar"],
            "mobile": ["app", "teléfono", "tocar", "vibrar", "pantalla", "móvil"],
            "ai": ["ia", "inteligencia", "analiza", "genera", "pregunta a la ia"],
            "gaming": ["juego", "personaje", "jugador", "puntos", "nivel", "presionar"]
        }
        
        for domain, keywords in domain_keywords.items():
            if any(keyword in content_lower for keyword in keywords):
                return domain
        
        return None
    
    def convert_to_vader_standard(self, content: str) -> str:
        """Convierte sintaxis conversacional a Vader estándar"""
        if not self.detect_conversational_syntax(content):
            return content  # Ya es sintaxis estándar
        
        # Aplicar patrones generales
        code = content
        for pattern, replacement in self.general_patterns:
            code = re.sub(pattern, replacement, code, flags=re.IGNORECASE)
        
        # Detectar dominio y aplicar patrones específicos
        domain = self.detect_domain(content)
        if domain and domain in self.domain_patterns:
            for pattern, replacement in self.domain_patterns[domain].items():
                code = re.sub(pattern, replacement, code, flags=re.IGNORECASE)
        
        # Limpiar espacios extra y formatear
        code = self._clean_and_format(code)
        
        return code
    
    def _clean_and_format(self, content: str) -> str:
        """Limpia y formatea el código convertido"""
        lines = content.split('\n')
        cleaned_lines = []
        
        for line in lines:
            line = line.strip()
            if line:
                cleaned_lines.append(line)
        
        return '\n'.join(cleaned_lines)
    
    def get_conversion_info(self, content: str) -> Dict:
        """Obtiene información sobre la conversión"""
        is_conversational = self.detect_conversational_syntax(content)
        domain = self.detect_domain(content)
        
        return {
            "is_conversational": is_conversational,
            "detected_domain": domain,
            "indicators_found": [ind for ind in self.conversation_indicators 
                               if ind in content.lower()],
            "conversion_needed": is_conversational
        }

# Función principal para integración con Vader
def process_conversational_vader(content: str) -> Tuple[str, Dict]:
    """
    Procesa contenido Vader conversacional
    
    Returns:
        Tuple[str, Dict]: (contenido_convertido, info_conversion)
    """
    parser = VaderConversationalParser()
    
    # Obtener información de conversión
    conversion_info = parser.get_conversion_info(content)
    
    # Convertir si es necesario
    if conversion_info["conversion_needed"]:
        converted_content = parser.convert_to_vader_standard(content)
        conversion_info["converted"] = True
    else:
        converted_content = content
        conversion_info["converted"] = False
    
    return converted_content, conversion_info

# Ejemplo de uso
if __name__ == "__main__":
    # Ejemplo conversacional
    conversational_code = """
cuando la edad sea mayor a 18 años
    decir "Eres mayor de edad"

suma 10 más 5 y guárdalo en resultado
pregunta "¿Cómo te llamas?" y guárdalo en nombre

para cada estudiante en lista_estudiantes
    si el estudiante tiene nota mayor a 7
        muestra que el estudiante "aprobó"
    """
    
    parser = VaderConversationalParser()
    converted = parser.convert_to_vader_standard(conversational_code)
    info = parser.get_conversion_info(conversational_code)
    
    print("🌟 VADER CONVERSACIONAL - DEMO")
    print("=" * 50)
    print("CÓDIGO CONVERSACIONAL:")
    print(conversational_code)
    print("\nCÓDIGO VADER ESTÁNDAR:")
    print(converted)
    print(f"\nINFO: {info}")
