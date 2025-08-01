#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VADER 8.0 - SINTAXIS ULTRA-NATURAL
==================================
Sistema que permite múltiples formas naturales de expresar operaciones en Vader

Características:
- Múltiples formas de declarar variables
- Expresiones condicionales ultra-flexibles
- Bucles en lenguaje natural
- Funciones conversacionales
- Operaciones matemáticas intuitivas
- Estructuras de datos naturales
- Manejo de errores humano

Autor: Vader Team
Versión: 8.0.0 "Ultra-Natural"
"""

import re
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass

@dataclass
class NaturalPattern:
    """Patrón de sintaxis natural"""
    patterns: List[str]
    template: str
    category: str
    examples: List[str]

class VaderUltraNaturalSyntax:
    """Parser de sintaxis ultra-natural para Vader"""
    
    def __init__(self):
        self.natural_patterns = self._initialize_patterns()
        self.context_stack = []
        self.variables = {}
    
    def _initialize_patterns(self) -> Dict[str, List[NaturalPattern]]:
        """Inicializa todos los patrones de sintaxis natural"""
        return {
            'variables': self._get_variable_patterns(),
            'conditionals': self._get_conditional_patterns(),
            'loops': self._get_loop_patterns(),
            'functions': self._get_function_patterns(),
            'math': self._get_math_patterns(),
            'data_structures': self._get_data_structure_patterns(),
            'error_handling': self._get_error_handling_patterns(),
            'io_operations': self._get_io_patterns(),
            'comparisons': self._get_comparison_patterns(),
            'assignments': self._get_assignment_patterns()
        }
    
    def _get_variable_patterns(self) -> List[NaturalPattern]:
        """Patrones para declaración de variables"""
        return [
            NaturalPattern(
                patterns=[
                    r'(?:que|sea|define|crear|hacer)\s+(\w+)\s+(?:sea|igual\s+a|=|como)\s+(.+)',
                    r'(\w+)\s+(?:es|será|va\s+a\s+ser)\s+(.+)',
                    r'(?:poner|asignar|guardar)\s+(.+)\s+(?:en|a)\s+(\w+)',
                    r'(?:la|el)\s+(?:variable|valor)\s+(\w+)\s+(?:es|será)\s+(.+)',
                    r'(\w+)\s*[:=]\s*(.+)',
                    r'(?:llamemos|digamos\s+que)\s+(\w+)\s+(?:es|será)\s+(.+)',
                    r'(?:tengo|tenemos)\s+(?:un|una)\s+(\w+)\s+(?:que\s+es|con\s+valor)\s+(.+)'
                ],
                template='{var} = {value}',
                category='variable_declaration',
                examples=[
                    'que nombre sea "Juan"',
                    'edad es 25',
                    'poner "Hola" en saludo',
                    'la variable contador es 0',
                    'precio: 100',
                    'llamemos total 500',
                    'tengo un numero que es 42'
                ]
            )
        ]
    
    def _get_conditional_patterns(self) -> List[NaturalPattern]:
        """Patrones para condicionales"""
        return [
            NaturalPattern(
                patterns=[
                    r'si\s+(.+?)\s+(?:entonces|:|,)?\s*(.*?)(?:\s+(?:sino|otherwise|de\s+lo\s+contrario)(.*))?',
                    r'(?:cuando|if)\s+(.+?)\s+(?:hacer|do|ejecutar)\s+(.*)',
                    r'(?:en\s+caso\s+de\s+que|if)\s+(.+?)\s*[:,]?\s*(.*)',
                    r'(?:verificar\s+si|check\s+if)\s+(.+?)\s+(?:y\s+)?(?:entonces|then)?\s*(.*)',
                    r'(.+?)\s*\?\s*(.*?)\s*:\s*(.*)',  # Operador ternario
                    r'(?:solo\s+si|only\s+if)\s+(.+?)\s+(?:hacer|do)\s+(.*)',
                    r'(?:mientras\s+que|while)\s+(.+?)\s+(?:sea|is)\s+(?:verdad|true|cierto)\s+(.*)'
                ],
                template='if {condition}:\n    {action}\n{else_action}',
                category='conditional',
                examples=[
                    'si edad > 18 entonces decir "Mayor de edad"',
                    'cuando llueva hacer llevar paraguas',
                    'en caso de que precio < 100, aplicar descuento',
                    'verificar si usuario existe y entonces mostrar perfil',
                    'edad >= 18 ? "Adulto" : "Menor"',
                    'solo si tengo dinero hacer comprar',
                    'mientras que contador sea verdad incrementar'
                ]
            )
        ]
    
    def _get_loop_patterns(self) -> List[NaturalPattern]:
        """Patrones para bucles"""
        return [
            NaturalPattern(
                patterns=[
                    r'(?:repetir|repeat)\s+(\d+)\s+(?:veces|times)\s+(.*)',
                    r'(?:para\s+cada|for\s+each)\s+(\w+)\s+(?:en|in)\s+(.+?)\s+(?:hacer|do)\s+(.*)',
                    r'(?:mientras|while)\s+(.+?)\s+(?:hacer|do|ejecutar)\s+(.*)',
                    r'(?:recorrer|iterar)\s+(.+?)\s+(?:y\s+)?(?:hacer|ejecutar)\s+(.*)',
                    r'(?:desde|from)\s+(\w+)\s*=\s*(\d+)\s+(?:hasta|to)\s+(\d+)\s+(?:hacer|do)\s+(.*)',
                    r'(?:por\s+cada|for)\s+(\w+)\s+(?:de|from)\s+(\d+)\s+(?:a|to)\s+(\d+)\s+(.*)',
                    r'(?:hacer|do)\s+(.*?)\s+(?:mientras|while)\s+(.+)',
                    r'(?:continuar|seguir)\s+(?:hasta\s+que|until)\s+(.+?)\s+(?:haciendo|doing)\s+(.*)'
                ],
                template='for {var} in range({start}, {end}):\n    {action}',
                category='loop',
                examples=[
                    'repetir 5 veces decir "Hola"',
                    'para cada item en lista hacer procesar',
                    'mientras contador < 10 hacer incrementar',
                    'recorrer numeros y sumar',
                    'desde i = 0 hasta 10 hacer imprimir i',
                    'por cada numero de 1 a 100 verificar si es par',
                    'hacer calcular mientras hay datos',
                    'continuar hasta que usuario diga "stop" haciendo preguntar'
                ]
            )
        ]
    
    def _get_function_patterns(self) -> List[NaturalPattern]:
        """Patrones para funciones"""
        return [
            NaturalPattern(
                patterns=[
                    r'(?:crear|define|hacer)\s+(?:una\s+)?(?:función|funcion|metodo)\s+(?:llamada\s+)?(\w+)\s+(?:que|para)\s+(.*)',
                    r'(?:función|funcion)\s+(\w+)\s*\((.*?)\)\s*(?::|que)\s+(.*)',
                    r'(?:cuando\s+llamen\s+a|al\s+ejecutar)\s+(\w+)\s+(?:hacer|ejecutar)\s+(.*)',
                    r'(\w+)\s+(?:recibe|toma)\s+(.*?)\s+(?:y\s+)?(?:devuelve|retorna)\s+(.*)',
                    r'(?:definir|def)\s+(\w+)\s+(?:como|as)\s+(.*)',
                    r'(?:el\s+proceso|la\s+operación)\s+(\w+)\s+(?:consiste\s+en|es)\s+(.*)',
                    r'(?:para|to)\s+(\w+)\s*[:,]\s*(.*)'
                ],
                template='def {name}({params}):\n    {body}',
                category='function',
                examples=[
                    'crear una función llamada saludar que diga hola',
                    'función calcular(a, b): sumar a y b',
                    'cuando llamen a procesar hacer validar datos',
                    'multiplicar recibe dos números y devuelve su producto',
                    'definir factorial como calcular n!',
                    'el proceso validar consiste en verificar formato',
                    'para sumar: retornar a + b'
                ]
            )
        ]
    
    def _get_math_patterns(self) -> List[NaturalPattern]:
        """Patrones para operaciones matemáticas"""
        return [
            NaturalPattern(
                patterns=[
                    r'(?:sumar|suma|añadir|agregar)\s+(.+?)\s+(?:y|con|más|\+)\s+(.+)',
                    r'(?:restar|resta|quitar)\s+(.+?)\s+(?:de|menos|-)\s+(.+)',
                    r'(?:multiplicar|multiplica)\s+(.+?)\s+(?:por|x|\*)\s+(.+)',
                    r'(?:dividir|divide)\s+(.+?)\s+(?:entre|por|/)\s+(.+)',
                    r'(?:elevar|potencia)\s+(.+?)\s+(?:a\s+la|al)\s+(?:potencia\s+)?(.+)',
                    r'(?:raíz\s+cuadrada|sqrt)\s+(?:de\s+)?(.+)',
                    r'(?:el\s+)?(?:porcentaje|%)\s+(.+?)\s+(?:de\s+)?(.+)',
                    r'(?:incrementar|aumentar)\s+(.+?)\s+(?:en\s+)?(.+)',
                    r'(?:decrementar|disminuir)\s+(.+?)\s+(?:en\s+)?(.+)'
                ],
                template='{operation}',
                category='math',
                examples=[
                    'sumar 5 y 3',
                    'restar 10 de 20',
                    'multiplicar precio por 1.21',
                    'dividir total entre 4',
                    'elevar 2 a la potencia 8',
                    'raíz cuadrada de 16',
                    'el 15% de 200',
                    'incrementar contador en 1',
                    'decrementar vida en 10'
                ]
            )
        ]
    
    def _get_data_structure_patterns(self) -> List[NaturalPattern]:
        """Patrones para estructuras de datos"""
        return [
            NaturalPattern(
                patterns=[
                    r'(?:crear|hacer)\s+(?:una\s+)?(?:lista|array)\s+(?:llamada\s+)?(\w+)\s+(?:con|que\s+contenga)\s+(.*)',
                    r'(?:agregar|añadir|meter)\s+(.+?)\s+(?:a\s+la\s+lista|al\s+array)\s+(\w+)',
                    r'(?:quitar|eliminar|sacar)\s+(.+?)\s+(?:de\s+la\s+lista|del\s+array)\s+(\w+)',
                    r'(?:el\s+)?(?:elemento|item)\s+(\d+)\s+(?:de|en)\s+(\w+)',
                    r'(?:crear|hacer)\s+(?:un\s+)?(?:diccionario|objeto)\s+(\w+)\s+(?:con|que\s+tenga)\s+(.*)',
                    r'(?:la\s+)?(?:clave|key)\s+(.+?)\s+(?:del\s+diccionario|en)\s+(\w+)',
                    r'(?:ordenar|sort)\s+(?:la\s+lista\s+)?(\w+)',
                    r'(?:buscar|encontrar)\s+(.+?)\s+(?:en\s+)?(\w+)'
                ],
                template='{operation}',
                category='data_structure',
                examples=[
                    'crear una lista llamada numeros con 1, 2, 3',
                    'agregar "nuevo" a la lista items',
                    'quitar "viejo" de la lista items',
                    'el elemento 0 de numeros',
                    'crear un diccionario persona con nombre: "Juan"',
                    'la clave "edad" del diccionario persona',
                    'ordenar la lista numeros',
                    'buscar "Juan" en usuarios'
                ]
            )
        ]
    
    def _get_error_handling_patterns(self) -> List[NaturalPattern]:
        """Patrones para manejo de errores"""
        return [
            NaturalPattern(
                patterns=[
                    r'(?:intentar|try|probar)\s+(.*?)\s+(?:y\s+)?(?:si\s+falla|catch|en\s+caso\s+de\s+error)\s+(.*)',
                    r'(?:manejar|handle)\s+(?:el\s+)?(?:error|exception)\s+(.*?)\s+(?:haciendo|doing)\s+(.*)',
                    r'(?:si\s+hay\s+un\s+error|if\s+error)\s+(?:en\s+)?(.+?)\s+(?:entonces|then)\s+(.*)',
                    r'(?:proteger|protect)\s+(.+?)\s+(?:contra|from)\s+(.+)',
                    r'(?:validar|validate)\s+(?:que\s+)?(.+?)\s+(?:o\s+)?(?:sino|otherwise)\s+(.*)',
                    r'(?:asegurar|ensure)\s+(?:que\s+)?(.+?)\s+(?:o\s+fallar|or\s+fail)\s+(.*)'
                ],
                template='try:\n    {action}\nexcept {error}:\n    {handler}',
                category='error_handling',
                examples=[
                    'intentar abrir archivo y si falla mostrar error',
                    'manejar el error de conexión haciendo reintentar',
                    'si hay un error en la división entonces usar 0',
                    'proteger la operación contra división por cero',
                    'validar que edad sea número o sino pedir de nuevo',
                    'asegurar que archivo existe o fallar con mensaje'
                ]
            )
        ]
    
    def _get_io_patterns(self) -> List[NaturalPattern]:
        """Patrones para entrada/salida"""
        return [
            NaturalPattern(
                patterns=[
                    r'(?:mostrar|imprimir|decir|print)\s+(.*)',
                    r'(?:preguntar|pedir|ask)\s+(?:al\s+usuario\s+)?(?:por\s+)?(.+?)(?:\s+y\s+guardar\s+en\s+(\w+))?',
                    r'(?:leer|read)\s+(?:el\s+)?(?:archivo|file)\s+(.+?)(?:\s+y\s+guardar\s+en\s+(\w+))?',
                    r'(?:escribir|write|guardar)\s+(.+?)\s+(?:en\s+el\s+archivo|to\s+file)\s+(.+)',
                    r'(?:abrir|open)\s+(?:el\s+)?(?:archivo|file)\s+(.+)',
                    r'(?:cerrar|close)\s+(?:el\s+)?(?:archivo|file)\s+(.+)',
                    r'(?:crear|create)\s+(?:el\s+)?(?:archivo|file)\s+(.+)',
                    r'(?:eliminar|delete|borrar)\s+(?:el\s+)?(?:archivo|file)\s+(.+)'
                ],
                template='{operation}',
                category='io',
                examples=[
                    'mostrar "Hola mundo"',
                    'preguntar al usuario por su nombre y guardar en nombre',
                    'leer el archivo datos.txt y guardar en contenido',
                    'escribir resultado en el archivo salida.txt',
                    'abrir el archivo config.json',
                    'cerrar el archivo log.txt',
                    'crear el archivo nuevo.txt',
                    'eliminar el archivo temporal.tmp'
                ]
            )
        ]
    
    def _get_comparison_patterns(self) -> List[NaturalPattern]:
        """Patrones para comparaciones"""
        return [
            NaturalPattern(
                patterns=[
                    r'(.+?)\s+(?:es\s+)?(?:mayor\s+que|>)\s+(.+)',
                    r'(.+?)\s+(?:es\s+)?(?:menor\s+que|<)\s+(.+)',
                    r'(.+?)\s+(?:es\s+)?(?:igual\s+a|==)\s+(.+)',
                    r'(.+?)\s+(?:es\s+)?(?:diferente\s+(?:de|a)|!=)\s+(.+)',
                    r'(.+?)\s+(?:es\s+)?(?:mayor\s+o\s+igual\s+(?:que|a)|>=)\s+(.+)',
                    r'(.+?)\s+(?:es\s+)?(?:menor\s+o\s+igual\s+(?:que|a)|<=)\s+(.+)',
                    r'(.+?)\s+(?:contiene|includes)\s+(.+)',
                    r'(.+?)\s+(?:está\s+en|in)\s+(.+)',
                    r'(.+?)\s+(?:empieza\s+con|starts\s+with)\s+(.+)',
                    r'(.+?)\s+(?:termina\s+con|ends\s+with)\s+(.+)'
                ],
                template='{left} {operator} {right}',
                category='comparison',
                examples=[
                    'edad es mayor que 18',
                    'precio es menor que 100',
                    'nombre es igual a "Juan"',
                    'estado es diferente de "activo"',
                    'puntuación es mayor o igual que 80',
                    'descuento es menor o igual a 50',
                    'texto contiene "error"',
                    'usuario está en lista_admin',
                    'archivo empieza con "temp"',
                    'extensión termina con ".txt"'
                ]
            )
        ]
    
    def _get_assignment_patterns(self) -> List[NaturalPattern]:
        """Patrones para asignaciones"""
        return [
            NaturalPattern(
                patterns=[
                    r'(?:cambiar|modificar|actualizar)\s+(\w+)\s+(?:a|por)\s+(.+)',
                    r'(?:incrementar|aumentar)\s+(\w+)(?:\s+en\s+(.+))?',
                    r'(?:decrementar|disminuir|reducir)\s+(\w+)(?:\s+en\s+(.+))?',
                    r'(?:duplicar|doblar)\s+(\w+)',
                    r'(?:resetear|reiniciar)\s+(\w+)(?:\s+a\s+(.+))?',
                    r'(?:intercambiar|swap)\s+(\w+)\s+(?:y|con)\s+(\w+)',
                    r'(?:copiar|copy)\s+(\w+)\s+(?:a|en)\s+(\w+)',
                    r'(?:limpiar|clear|vaciar)\s+(\w+)'
                ],
                template='{operation}',
                category='assignment',
                examples=[
                    'cambiar contador a 0',
                    'incrementar edad en 1',
                    'decrementar vida en 10',
                    'duplicar salario',
                    'resetear puntuación a 0',
                    'intercambiar a y b',
                    'copiar original a copia',
                    'limpiar lista'
                ]
            )
        ]
    
    def parse_natural_text(self, text: str) -> List[Dict[str, Any]]:
        """Parsea texto natural y lo convierte a código Vader"""
        results = []
        lines = text.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            parsed = self._parse_single_line(line)
            if parsed:
                results.append(parsed)
        
        return results
    
    def _parse_single_line(self, line: str) -> Optional[Dict[str, Any]]:
        """Parsea una sola línea de texto natural"""
        for category, patterns in self.natural_patterns.items():
            for pattern_obj in patterns:
                for pattern in pattern_obj.patterns:
                    match = re.search(pattern, line, re.IGNORECASE)
                    if match:
                        return {
                            'category': category,
                            'original': line,
                            'pattern': pattern,
                            'groups': match.groups(),
                            'template': pattern_obj.template,
                            'examples': pattern_obj.examples
                        }
        
        return None
    
    def generate_code(self, natural_text: str) -> str:
        """Genera código Vader a partir de texto natural"""
        parsed_lines = self.parse_natural_text(natural_text)
        code_lines = []
        
        for parsed in parsed_lines:
            code_line = self._generate_code_line(parsed)
            if code_line:
                code_lines.append(code_line)
        
        return '\n'.join(code_lines)
    
    def _generate_code_line(self, parsed: Dict[str, Any]) -> str:
        """Genera una línea de código a partir de un parsing"""
        category = parsed['category']
        groups = parsed['groups']
        
        if category == 'variables':
            if len(groups) >= 2:
                var_name = groups[0] if groups[0] else groups[1]
                value = groups[1] if groups[0] else groups[0]
                return f'{var_name} = {value}'
        
        elif category == 'conditionals':
            condition = groups[0]
            action = groups[1] if len(groups) > 1 else ""
            else_action = groups[2] if len(groups) > 2 else ""
            
            code = f'si {condition}:\n    {action}'
            if else_action:
                code += f'\nsino:\n    {else_action}'
            return code
        
        elif category == 'loops':
            if 'repetir' in parsed['original']:
                times = groups[0]
                action = groups[1]
                return f'repetir {times} veces:\n    {action}'
            elif 'para cada' in parsed['original']:
                var = groups[0]
                iterable = groups[1]
                action = groups[2]
                return f'para cada {var} en {iterable}:\n    {action}'
        
        elif category == 'functions':
            name = groups[0]
            body = groups[1] if len(groups) > 1 else groups[-1]
            return f'función {name}():\n    {body}'
        
        elif category == 'math':
            if 'sumar' in parsed['original']:
                return f'{groups[0]} + {groups[1]}'
            elif 'restar' in parsed['original']:
                return f'{groups[1]} - {groups[0]}'
            elif 'multiplicar' in parsed['original']:
                return f'{groups[0]} * {groups[1]}'
            elif 'dividir' in parsed['original']:
                return f'{groups[0]} / {groups[1]}'
        
        elif category == 'io':
            if 'mostrar' in parsed['original'] or 'decir' in parsed['original']:
                return f'decir {groups[0]}'
            elif 'preguntar' in parsed['original']:
                if len(groups) > 1 and groups[1]:
                    return f'{groups[1]} = preguntar("{groups[0]}")'
                else:
                    return f'preguntar("{groups[0]}")'
        
        return f'# {parsed["original"]}'  # Comentario si no se puede parsear

def test_ultra_natural_syntax():
    """Función de prueba para la sintaxis ultra-natural"""
    parser = VaderUltraNaturalSyntax()
    
    test_cases = [
        "que nombre sea 'Juan'",
        "edad es 25",
        "si edad > 18 entonces decir 'Mayor de edad'",
        "repetir 5 veces decir 'Hola'",
        "sumar 10 y 5",
        "crear función saludar que diga hola",
        "mostrar 'Bienvenido'",
        "preguntar por el nombre y guardar en usuario"
    ]
    
    print("🚀 VADER SINTAXIS ULTRA-NATURAL - PRUEBAS")
    print("=" * 60)
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n📝 Prueba {i}: {test}")
        parsed = parser._parse_single_line(test)
        if parsed:
            print(f"✅ Categoría: {parsed['category']}")
            print(f"🔍 Grupos: {parsed['groups']}")
            code = parser._generate_code_line(parsed)
            print(f"💻 Código: {code}")
        else:
            print("❌ No se pudo parsear")

if __name__ == "__main__":
    test_ultra_natural_syntax()
