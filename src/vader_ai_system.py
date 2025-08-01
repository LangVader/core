#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VADER 7.0 - SISTEMA DE IA INTEGRADA
===================================
Sistema completo de IA para Vader con autocompletado y optimización

Características:
- Autocompletado inteligente basado en contexto
- Optimización automática de código
- Sugerencias de refactoring
- Detección de patrones y antipatrones
- Generación de código asistida
- Análisis semántico avanzado
- Predicción de errores

Autor: Vader Team
Versión: 7.0.0 "Universal"
Fecha: 2025
"""

import re
import json
import hashlib
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import difflib
from datetime import datetime
import pickle
import os

class SuggestionType(Enum):
    """Tipos de sugerencias de IA"""
    AUTOCOMPLETE = "autocomplete"
    OPTIMIZATION = "optimization"
    REFACTOR = "refactor"
    BUG_FIX = "bug_fix"
    DOCUMENTATION = "documentation"

class ConfidenceLevel(Enum):
    """Niveles de confianza"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"

@dataclass
class AISuggestion:
    """Sugerencia generada por IA"""
    suggestion_id: str
    suggestion_type: SuggestionType
    confidence: ConfidenceLevel
    title: str
    description: str
    code_before: str
    code_after: str
    file_path: str
    line_number: int
    reasoning: str
    benefits: List[str] = field(default_factory=list)
    auto_applicable: bool = False

@dataclass
class CodeContext:
    """Contexto de código para análisis"""
    file_path: str
    content: str
    cursor_position: int
    current_line: str
    surrounding_lines: List[str]
    function_context: Optional[str] = None
    variables_in_scope: Dict[str, str] = field(default_factory=dict)

class VaderAIEngine:
    """Motor de IA para Vader"""
    
    def __init__(self, model_path: str = None):
        self.patterns: Dict[str, Any] = {}
        self.user_preferences: Dict[str, Any] = {}
        self.suggestion_history: List[AISuggestion] = []
        self.model_path = model_path or "vader_ai_model.pkl"
        
        # Vocabulario de Vader
        self.vader_vocabulary = {
            'keywords': [
                'funcion', 'clase', 'si', 'sino', 'mientras', 'para', 'en',
                'retornar', 'importar', 'de', 'como', 'intentar', 'capturar',
                'finalmente', 'con', 'pasar', 'romper', 'continuar', 'y', 'o',
                'no', 'es', 'lambda', 'global', 'assert', 'del', 'yield', 'raise'
            ],
            'built_in_functions': [
                'print', 'len', 'range', 'enumerate', 'zip', 'map', 'filter',
                'sorted', 'reversed', 'sum', 'max', 'min', 'abs', 'round',
                'type', 'isinstance', 'hasattr', 'getattr', 'setattr'
            ],
            'data_types': [
                'int', 'float', 'str', 'bool', 'list', 'dict', 'tuple', 'set'
            ],
            'common_patterns': [
                'si (__name__ == "__main__"):',
                'para (item en lista):',
                'mientras (condicion):',
                'intentar:',
                'capturar Exception como e:',
                'con open(archivo) como f:',
                'clase MiClase:',
                'funcion mi_funcion():',
                'retornar resultado'
            ]
        }
        
        # Patrones de Vader
        self.vader_syntax = {
            'function_def': r'funcion\s+(\w+)\s*\([^)]*\)\s*\{',
            'class_def': r'clase\s+(\w+)(?:\s+hereda\s+\w+)?\s*\{',
            'variable_assignment': r'(\w+)\s*=\s*(.+)',
            'import_statement': r'importar\s+(.+)',
        }
        
        # Reglas de optimización
        self.optimization_rules = {
            'loop_optimizations': [
                {
                    'name': 'list_comprehension',
                    'pattern': r'(\w+)\s*=\s*\[\]\s*\n\s*para\s*\((\w+)\s+en\s+(\w+)\)\s*\{\s*\1\.append\(([^)]+)\)\s*\}',
                    'replacement': r'\1 = [\4 para \2 en \3]',
                    'benefit': 'List comprehension es más eficiente'
                },
                {
                    'name': 'enumerate_usage',
                    'pattern': r'para\s*\((\w+)\s+en\s+range\(len\((\w+)\)\)\)',
                    'replacement': r'para (\1, valor en enumerate(\2))',
                    'benefit': 'enumerate es más legible'
                }
            ],
            'conditional_optimizations': [
                {
                    'name': 'simplify_boolean',
                    'pattern': r'si\s*\((\w+)\s*==\s*True\)',
                    'replacement': r'si (\1)',
                    'benefit': 'Simplificar comparación booleana'
                }
            ]
        }
        
        # Cargar modelo si existe
        self._load_model()
    
    def _load_model(self):
        """Carga modelo de IA entrenado"""
        if os.path.exists(self.model_path):
            try:
                with open(self.model_path, 'rb') as f:
                    data = pickle.load(f)
                    self.patterns = data.get('patterns', {})
                    self.user_preferences = data.get('preferences', {})
                    print(f"✅ Modelo de IA cargado: {len(self.patterns)} patrones")
            except Exception as e:
                print(f"⚠️ Error cargando modelo: {e}")
    
    def _save_model(self):
        """Guarda modelo de IA"""
        try:
            data = {
                'patterns': self.patterns,
                'preferences': self.user_preferences,
                'timestamp': datetime.now().isoformat()
            }
            with open(self.model_path, 'wb') as f:
                pickle.dump(data, f)
        except Exception as e:
            print(f"⚠️ Error guardando modelo: {e}")
    
    def analyze_code_context(self, file_path: str, content: str, cursor_position: int) -> CodeContext:
        """Analiza el contexto del código"""
        lines = content.split('\n')
        
        # Encontrar línea actual
        current_pos = 0
        current_line_num = 0
        for i, line in enumerate(lines):
            if current_pos + len(line) >= cursor_position:
                current_line_num = i
                break
            current_pos += len(line) + 1
        
        current_line = lines[current_line_num] if current_line_num < len(lines) else ""
        
        # Obtener líneas circundantes
        start_line = max(0, current_line_num - 5)
        end_line = min(len(lines), current_line_num + 6)
        surrounding_lines = lines[start_line:end_line]
        
        # Detectar contexto de función
        function_context = self._find_function_context(lines, current_line_num)
        
        # Detectar variables en scope
        variables_in_scope = self._find_variables_in_scope(lines, current_line_num)
        
        return CodeContext(
            file_path=file_path,
            content=content,
            cursor_position=cursor_position,
            current_line=current_line,
            surrounding_lines=surrounding_lines,
            function_context=function_context,
            variables_in_scope=variables_in_scope
        )
    
    def generate_autocomplete_suggestions(self, context: CodeContext) -> List[AISuggestion]:
        """Genera sugerencias de autocompletado"""
        suggestions = []
        
        # Obtener texto parcial
        cursor_line = context.current_line
        words = cursor_line.split()
        partial_word = words[-1] if words else ""
        
        # Sugerencias del vocabulario
        vocab_suggestions = self._get_vocabulary_suggestions(partial_word)
        
        # Sugerencias de contexto
        context_suggestions = self._get_context_suggestions(context, partial_word)
        
        # Crear objetos AISuggestion
        all_suggestions = vocab_suggestions + context_suggestions
        
        for i, (suggestion_text, confidence, reasoning) in enumerate(all_suggestions[:10]):
            suggestions.append(AISuggestion(
                suggestion_id=f"ac_{i}",
                suggestion_type=SuggestionType.AUTOCOMPLETE,
                confidence=confidence,
                title=f"Autocompletar: {suggestion_text}",
                description=f"Completar con '{suggestion_text}'",
                code_before=cursor_line,
                code_after=cursor_line.replace(partial_word, suggestion_text),
                file_path=context.file_path,
                line_number=context.cursor_position,
                reasoning=reasoning,
                auto_applicable=True
            ))
        
        return suggestions
    
    def generate_optimization_suggestions(self, context: CodeContext) -> List[AISuggestion]:
        """Genera sugerencias de optimización"""
        suggestions = []
        content = context.content
        
        # Aplicar reglas de optimización
        for category, rules in self.optimization_rules.items():
            for rule in rules:
                matches = re.finditer(rule['pattern'], content, re.MULTILINE)
                
                for match in matches:
                    line_num = content[:match.start()].count('\n') + 1
                    optimized_code = re.sub(rule['pattern'], rule['replacement'], match.group(0))
                    
                    suggestions.append(AISuggestion(
                        suggestion_id=f"opt_{rule['name']}_{line_num}",
                        suggestion_type=SuggestionType.OPTIMIZATION,
                        confidence=ConfidenceLevel.HIGH,
                        title=f"Optimización: {rule['name']}",
                        description=rule['benefit'],
                        code_before=match.group(0),
                        code_after=optimized_code,
                        file_path=context.file_path,
                        line_number=line_num,
                        reasoning=f"Aplicar optimización {rule['name']}",
                        benefits=[rule['benefit']],
                        auto_applicable=True
                    ))
        
        return suggestions
    
    def generate_refactor_suggestions(self, context: CodeContext) -> List[AISuggestion]:
        """Genera sugerencias de refactoring"""
        suggestions = []
        
        # Detectar funciones largas
        long_functions = self._detect_long_functions(context.content)
        for func_name, line_count, start_line in long_functions:
            suggestions.append(AISuggestion(
                suggestion_id=f"ref_long_func_{func_name}",
                suggestion_type=SuggestionType.REFACTOR,
                confidence=ConfidenceLevel.MEDIUM,
                title=f"Refactorizar función larga: {func_name}",
                description=f"La función {func_name} tiene {line_count} líneas",
                code_before=f"funcion {func_name}(...)",
                code_after=f"# Dividir {func_name} en funciones más pequeñas",
                file_path=context.file_path,
                line_number=start_line,
                reasoning="Funciones largas son difíciles de mantener",
                benefits=["Mejor legibilidad", "Más fácil de testear"],
                auto_applicable=False
            ))
        
        return suggestions
    
    def generate_bug_fix_suggestions(self, context: CodeContext) -> List[AISuggestion]:
        """Genera sugerencias de corrección de bugs"""
        suggestions = []
        
        # Detectar posibles bugs
        bug_patterns = [
            {
                'pattern': r'si\s*\((\w+)\s*=\s*([^)]+)\)',
                'issue': 'Asignación en condicional (posible error)',
                'fix': 'Usar == para comparación'
            },
            {
                'pattern': r'(\w+)\[(\d+)\]',
                'issue': 'Acceso directo a índice puede causar IndexError',
                'fix': 'Verificar longitud antes del acceso'
            }
        ]
        
        for pattern_info in bug_patterns:
            matches = re.finditer(pattern_info['pattern'], context.content)
            
            for match in matches:
                line_num = context.content[:match.start()].count('\n') + 1
                
                suggestions.append(AISuggestion(
                    suggestion_id=f"bug_{hashlib.md5(match.group(0).encode()).hexdigest()[:8]}",
                    suggestion_type=SuggestionType.BUG_FIX,
                    confidence=ConfidenceLevel.MEDIUM,
                    title="Posible bug detectado",
                    description=pattern_info['issue'],
                    code_before=match.group(0),
                    code_after=f"# {pattern_info['fix']}",
                    file_path=context.file_path,
                    line_number=line_num,
                    reasoning=pattern_info['issue'],
                    benefits=["Prevenir errores en runtime"],
                    auto_applicable=False
                ))
        
        return suggestions
    
    def _get_vocabulary_suggestions(self, partial_word: str) -> List[Tuple[str, ConfidenceLevel, str]]:
        """Obtiene sugerencias del vocabulario"""
        suggestions = []
        
        if not partial_word:
            return suggestions
        
        for category, words in self.vader_vocabulary.items():
            for word in words:
                if word.startswith(partial_word.lower()):
                    confidence = ConfidenceLevel.HIGH if len(partial_word) > 2 else ConfidenceLevel.MEDIUM
                    suggestions.append((word, confidence, f"Palabra clave de {category}"))
        
        return suggestions
    
    def _get_context_suggestions(self, context: CodeContext, partial_word: str) -> List[Tuple[str, ConfidenceLevel, str]]:
        """Obtiene sugerencias basadas en contexto"""
        suggestions = []
        
        # Sugerir variables en scope
        for var_name, var_type in context.variables_in_scope.items():
            if var_name.startswith(partial_word):
                suggestions.append((var_name, ConfidenceLevel.HIGH, f"Variable en scope ({var_type})"))
        
        return suggestions
    
    def _find_function_context(self, lines: List[str], current_line: int) -> Optional[str]:
        """Encuentra el contexto de función actual"""
        for i in range(current_line, -1, -1):
            match = re.match(self.vader_syntax['function_def'], lines[i])
            if match:
                return match.group(1)
        return None
    
    def _find_variables_in_scope(self, lines: List[str], current_line: int) -> Dict[str, str]:
        """Encuentra variables en el scope actual"""
        variables = {}
        
        for i in range(current_line, -1, -1):
            line = lines[i]
            assign_match = re.match(self.vader_syntax['variable_assignment'], line)
            if assign_match:
                var_name = assign_match.group(1)
                var_value = assign_match.group(2)
                
                # Inferir tipo básico
                var_type = "unknown"
                if var_value.startswith('"') or var_value.startswith("'"):
                    var_type = "str"
                elif var_value.isdigit():
                    var_type = "int"
                elif var_value in ['True', 'False']:
                    var_type = "bool"
                elif var_value.startswith('['):
                    var_type = "list"
                
                variables[var_name] = var_type
        
        return variables
    
    def _detect_long_functions(self, content: str) -> List[Tuple[str, int, int]]:
        """Detecta funciones largas"""
        long_functions = []
        lines = content.split('\n')
        
        current_function = None
        function_start = 0
        brace_count = 0
        
        for i, line in enumerate(lines):
            func_match = re.match(self.vader_syntax['function_def'], line)
            if func_match:
                if current_function and (i - function_start) > 30:
                    long_functions.append((current_function, i - function_start, function_start + 1))
                
                current_function = func_match.group(1)
                function_start = i
                brace_count = 0
            
            if current_function:
                brace_count += line.count('{') - line.count('}')
                if brace_count <= 0 and i > function_start:
                    if (i - function_start) > 30:
                        long_functions.append((current_function, i - function_start, function_start + 1))
                    current_function = None
        
        return long_functions
    
    def learn_from_user_action(self, suggestion: AISuggestion, accepted: bool):
        """Aprende de las acciones del usuario"""
        pattern_id = f"learned_{suggestion.suggestion_type.value}_{len(self.patterns)}"
        
        if accepted:
            self.patterns[pattern_id] = {
                'type': suggestion.suggestion_type.value,
                'before': suggestion.code_before,
                'after': suggestion.code_after,
                'success_rate': 1.0,
                'usage_count': 1
            }
        
        self._save_model()
    
    def get_ai_insights(self, context: CodeContext) -> Dict[str, Any]:
        """Obtiene insights de IA sobre el código"""
        insights = {
            'complexity_score': self._calculate_complexity_score(context.content),
            'maintainability_score': self._calculate_maintainability_score(context.content),
            'recommendations': []
        }
        
        if insights['complexity_score'] > 7:
            insights['recommendations'].append("Considerar dividir funciones complejas")
        
        if insights['maintainability_score'] < 6:
            insights['recommendations'].append("Añadir más documentación")
        
        return insights
    
    def _calculate_complexity_score(self, content: str) -> float:
        """Calcula puntuación de complejidad"""
        lines = content.split('\n')
        complexity = 1
        
        for line in lines:
            if re.search(r'\b(si|mientras|para|caso)\b', line):
                complexity += 1
        
        return min(10, complexity / len(lines) * 100) if lines else 1
    
    def _calculate_maintainability_score(self, content: str) -> float:
        """Calcula puntuación de mantenibilidad"""
        lines = content.split('\n')
        comment_lines = sum(1 for line in lines if line.strip().startswith('#'))
        code_lines = len([line for line in lines if line.strip() and not line.strip().startswith('#')])
        
        if code_lines == 0:
            return 10
        
        comment_ratio = comment_lines / code_lines
        return min(10, comment_ratio * 20 + 5)

def main():
    """Función principal para testing"""
    print("🤖 VADER AI SYSTEM - Sistema de IA integrada:")
    print("=" * 70)
    
    # Crear motor de IA
    ai_engine = VaderAIEngine()
    
    # Código de prueba
    test_code = """
# Código de prueba para IA
importar os
importar sys

funcion procesarDatos(lista) {
    resultado = []
    para (i en range(len(lista))) {
        si (lista[i] == True) {
            resultado.append(lista[i])
        }
    }
    retornar resultado
}

funcion funcionMuyLarga() {
    # Esta función es muy larga
    linea1 = 1
    linea2 = 2
    # ... muchas líneas más
    para (i en range(100)) {
        si (i > 50) {
            print(i)
        }
    }
    retornar "resultado"
}

nombre = "test"
edad = 25
activo = True
"""
    
    print("📝 Analizando código de prueba...")
    
    # Crear contexto
    context = ai_engine.analyze_code_context("test.vdr", test_code, 100)
    print(f"✅ Contexto analizado:")
    print(f"   Función actual: {context.function_context}")
    print(f"   Variables en scope: {len(context.variables_in_scope)}")
    
    # Generar sugerencias de autocompletado
    print(f"\n🔤 Sugerencias de autocompletado:")
    autocomplete = ai_engine.generate_autocomplete_suggestions(context)
    for suggestion in autocomplete[:3]:
        print(f"   - {suggestion.title}: {suggestion.description}")
    
    # Generar sugerencias de optimización
    print(f"\n⚡ Sugerencias de optimización:")
    optimizations = ai_engine.generate_optimization_suggestions(context)
    for suggestion in optimizations:
        print(f"   - {suggestion.title}: {suggestion.description}")
        print(f"     Antes: {suggestion.code_before.strip()}")
        print(f"     Después: {suggestion.code_after.strip()}")
    
    # Generar sugerencias de refactoring
    print(f"\n🔧 Sugerencias de refactoring:")
    refactors = ai_engine.generate_refactor_suggestions(context)
    for suggestion in refactors:
        print(f"   - {suggestion.title}: {suggestion.description}")
    
    # Generar insights
    print(f"\n📊 Insights de IA:")
    insights = ai_engine.get_ai_insights(context)
    print(f"   Complejidad: {insights['complexity_score']:.1f}/10")
    print(f"   Mantenibilidad: {insights['maintainability_score']:.1f}/10")
    print(f"   Recomendaciones:")
    for rec in insights['recommendations']:
        print(f"     - {rec}")
    
    print("\n" + "=" * 70)
    print("✅ Sistema de IA Vader implementado")
    print("🚀 Características disponibles:")
    print("  - Autocompletado inteligente")
    print("  - Optimización automática de código")
    print("  - Sugerencias de refactoring")
    print("  - Detección de bugs potenciales")
    print("  - Análisis de complejidad")
    print("  - Insights de mantenibilidad")
    print("  - Aprendizaje de patrones")
    print("  - Contexto semántico")

if __name__ == "__main__":
    main()
