#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VADER 7.0 - SISTEMA DE LINTING Y VALIDACIÓN DE ESTILO
=====================================================
Sistema completo de linting para Vader con validación de código

Características:
- Análisis estático de código
- Validación de estilo y convenciones
- Detección de errores potenciales
- Métricas de calidad de código
- Reglas personalizables
- Autofix de problemas comunes
- Reportes detallados

Autor: Vader Team
Versión: 7.0.0 "Universal"
Fecha: 2025
"""

import re
import os
import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime

class LintSeverity(Enum):
    """Severidad de problemas de linting"""
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"
    HINT = "hint"

class LintCategory(Enum):
    """Categorías de reglas de linting"""
    SYNTAX = "syntax"
    STYLE = "style"
    LOGIC = "logic"
    PERFORMANCE = "performance"
    SECURITY = "security"
    MAINTAINABILITY = "maintainability"
    COMPLEXITY = "complexity"
    NAMING = "naming"

@dataclass
class LintIssue:
    """Problema encontrado por el linter"""
    rule_id: str
    severity: LintSeverity
    category: LintCategory
    message: str
    file_path: str
    line_number: int
    column: int
    suggestion: Optional[str] = None
    auto_fixable: bool = False
    context: Optional[str] = None

@dataclass
class LintRule:
    """Regla de linting"""
    rule_id: str
    name: str
    description: str
    category: LintCategory
    severity: LintSeverity
    enabled: bool = True
    auto_fix: bool = False
    checker_function: Optional[callable] = None

@dataclass
class LintReport:
    """Reporte de linting"""
    file_path: str
    issues: List[LintIssue] = field(default_factory=list)
    metrics: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)

class VaderLinter:
    """Linter principal de Vader"""
    
    def __init__(self, config_path: str = None):
        self.rules: Dict[str, LintRule] = {}
        self.config = self._load_config(config_path)
        self.reports: List[LintReport] = []
        
        # Registrar reglas predefinidas
        self._register_builtin_rules()
        
        # Patrones comunes de Vader
        self.vader_patterns = {
            'function_def': r'funcion\s+(\w+)\s*\([^)]*\)\s*\{',
            'class_def': r'clase\s+(\w+)(?:\s+hereda\s+\w+)?\s*\{',
            'variable_assignment': r'(\w+)\s*=\s*(.+)',
            'import_statement': r'importar\s+(.+)',
            'comment': r'#.*$',
        }
    
    def _load_config(self, config_path: str = None) -> Dict[str, Any]:
        """Carga configuración del linter"""
        return {
            'max_line_length': 100,
            'max_function_length': 50,
            'max_complexity': 10,
            'naming_conventions': {
                'function': 'snake_case',
                'class': 'PascalCase',
                'variable': 'snake_case'
            },
            'required_docstrings': True,
            'allow_unused_variables': False
        }
    
    def _register_builtin_rules(self):
        """Registra reglas predefinidas"""
        
        # Regla de longitud de línea
        self.add_rule(LintRule(
            rule_id="V001",
            name="line_too_long",
            description="Línea demasiado larga",
            category=LintCategory.STYLE,
            severity=LintSeverity.WARNING,
            checker_function=self._check_line_length
        ))
        
        # Regla de nombres de funciones
        self.add_rule(LintRule(
            rule_id="V002",
            name="function_naming",
            description="Convención de nombres de funciones",
            category=LintCategory.NAMING,
            severity=LintSeverity.WARNING,
            checker_function=self._check_function_naming
        ))
        
        # Regla de variables no utilizadas
        self.add_rule(LintRule(
            rule_id="V003",
            name="unused_variable",
            description="Variable no utilizada",
            category=LintCategory.LOGIC,
            severity=LintSeverity.INFO,
            checker_function=self._check_unused_variables
        ))
        
        # Regla de complejidad
        self.add_rule(LintRule(
            rule_id="V004",
            name="cyclomatic_complexity",
            description="Complejidad ciclomática alta",
            category=LintCategory.COMPLEXITY,
            severity=LintSeverity.WARNING,
            checker_function=self._check_complexity
        ))
        
        # Regla de documentación
        self.add_rule(LintRule(
            rule_id="V005",
            name="missing_docstring",
            description="Documentación faltante",
            category=LintCategory.MAINTAINABILITY,
            severity=LintSeverity.INFO,
            checker_function=self._check_docstrings
        ))
        
        # Regla de espacios en blanco
        self.add_rule(LintRule(
            rule_id="V006",
            name="trailing_whitespace",
            description="Espacios en blanco al final",
            category=LintCategory.STYLE,
            severity=LintSeverity.INFO,
            auto_fix=True,
            checker_function=self._check_trailing_whitespace
        ))
        
        # Regla de seguridad
        self.add_rule(LintRule(
            rule_id="V007",
            name="dangerous_eval",
            description="Uso peligroso de eval/exec",
            category=LintCategory.SECURITY,
            severity=LintSeverity.ERROR,
            checker_function=self._check_dangerous_eval
        ))
    
    def add_rule(self, rule: LintRule):
        """Añade una regla de linting"""
        self.rules[rule.rule_id] = rule
    
    def lint_content(self, content: str, file_path: str = "<string>") -> LintReport:
        """Analiza contenido de código"""
        report = LintReport(file_path=file_path)
        lines = content.split('\n')
        
        # Ejecutar reglas habilitadas
        for rule in self.rules.values():
            if not rule.enabled or not rule.checker_function:
                continue
            
            issues = rule.checker_function(content, lines, file_path)
            report.issues.extend(issues)
        
        # Calcular métricas
        report.metrics = self._calculate_metrics(content, lines)
        
        # Ordenar issues por línea
        report.issues.sort(key=lambda x: (x.line_number, x.column))
        
        self.reports.append(report)
        return report
    
    def _check_line_length(self, content: str, lines: List[str], file_path: str) -> List[LintIssue]:
        """Verifica longitud de líneas"""
        issues = []
        max_length = self.config.get('max_line_length', 100)
        
        for i, line in enumerate(lines, 1):
            if len(line) > max_length:
                issues.append(LintIssue(
                    rule_id="V001",
                    severity=LintSeverity.WARNING,
                    category=LintCategory.STYLE,
                    message=f"Línea demasiado larga ({len(line)} > {max_length} caracteres)",
                    file_path=file_path,
                    line_number=i,
                    column=max_length + 1,
                    context=line[:50] + "..." if len(line) > 50 else line
                ))
        
        return issues
    
    def _check_function_naming(self, content: str, lines: List[str], file_path: str) -> List[LintIssue]:
        """Verifica convención de nombres de funciones"""
        issues = []
        
        for i, line in enumerate(lines, 1):
            match = re.search(self.vader_patterns['function_def'], line)
            if match:
                func_name = match.group(1)
                
                if not self._is_snake_case(func_name):
                    issues.append(LintIssue(
                        rule_id="V002",
                        severity=LintSeverity.WARNING,
                        category=LintCategory.NAMING,
                        message=f"Función '{func_name}' debe usar snake_case",
                        file_path=file_path,
                        line_number=i,
                        column=1,
                        suggestion=self._to_snake_case(func_name),
                        context=line.strip()
                    ))
        
        return issues
    
    def _check_unused_variables(self, content: str, lines: List[str], file_path: str) -> List[LintIssue]:
        """Verifica variables no utilizadas"""
        issues = []
        
        if self.config.get('allow_unused_variables', False):
            return issues
        
        # Encontrar asignaciones y usos
        assignments = set()
        usages = set()
        
        for i, line in enumerate(lines, 1):
            assign_match = re.search(self.vader_patterns['variable_assignment'], line)
            if assign_match:
                var_name = assign_match.group(1)
                if not var_name.startswith('_'):
                    assignments.add((var_name, i))
            
            # Buscar usos
            for var_name, _ in assignments:
                if re.search(rf'\b{re.escape(var_name)}\b', line) and '=' not in line.split(var_name)[0]:
                    usages.add(var_name)
        
        # Reportar no utilizadas
        for var_name, line_num in assignments:
            if var_name not in usages:
                issues.append(LintIssue(
                    rule_id="V003",
                    severity=LintSeverity.INFO,
                    category=LintCategory.LOGIC,
                    message=f"Variable '{var_name}' definida pero no utilizada",
                    file_path=file_path,
                    line_number=line_num,
                    column=1,
                    suggestion=f"Considerar eliminar '{var_name}'"
                ))
        
        return issues
    
    def _check_complexity(self, content: str, lines: List[str], file_path: str) -> List[LintIssue]:
        """Verifica complejidad ciclomática"""
        issues = []
        max_complexity = self.config.get('max_complexity', 10)
        
        current_function = None
        function_start = 0
        complexity = 1
        brace_count = 0
        
        for i, line in enumerate(lines, 1):
            func_match = re.search(self.vader_patterns['function_def'], line)
            if func_match:
                if current_function and complexity > max_complexity:
                    issues.append(LintIssue(
                        rule_id="V004",
                        severity=LintSeverity.WARNING,
                        category=LintCategory.COMPLEXITY,
                        message=f"Función '{current_function}' tiene complejidad alta ({complexity})",
                        file_path=file_path,
                        line_number=function_start,
                        column=1,
                        suggestion="Dividir en funciones más pequeñas"
                    ))
                
                current_function = func_match.group(1)
                function_start = i
                complexity = 1
                brace_count = 0
            
            brace_count += line.count('{') - line.count('}')
            
            if current_function and brace_count > 0:
                if re.search(r'\b(si|mientras|para|caso)\b', line):
                    complexity += 1
        
        return issues
    
    def _check_docstrings(self, content: str, lines: List[str], file_path: str) -> List[LintIssue]:
        """Verifica documentación faltante"""
        issues = []
        
        if not self.config.get('required_docstrings', True):
            return issues
        
        for i, line in enumerate(lines, 1):
            func_match = re.search(self.vader_patterns['function_def'], line)
            if func_match:
                func_name = func_match.group(1)
                next_line_idx = i
                while next_line_idx < len(lines) and not lines[next_line_idx].strip():
                    next_line_idx += 1
                
                if (next_line_idx >= len(lines) or 
                    not lines[next_line_idx].strip().startswith(('"""', "'''", '#'))):
                    issues.append(LintIssue(
                        rule_id="V005",
                        severity=LintSeverity.INFO,
                        category=LintCategory.MAINTAINABILITY,
                        message=f"Función '{func_name}' sin documentación",
                        file_path=file_path,
                        line_number=i,
                        column=1,
                        suggestion=f"Añadir docstring a '{func_name}'"
                    ))
        
        return issues
    
    def _check_trailing_whitespace(self, content: str, lines: List[str], file_path: str) -> List[LintIssue]:
        """Verifica espacios en blanco al final"""
        issues = []
        
        for i, line in enumerate(lines, 1):
            if line.rstrip() != line and line.strip():
                issues.append(LintIssue(
                    rule_id="V006",
                    severity=LintSeverity.INFO,
                    category=LintCategory.STYLE,
                    message="Espacios en blanco al final",
                    file_path=file_path,
                    line_number=i,
                    column=len(line.rstrip()) + 1,
                    auto_fixable=True,
                    suggestion="Eliminar espacios al final"
                ))
        
        return issues
    
    def _check_dangerous_eval(self, content: str, lines: List[str], file_path: str) -> List[LintIssue]:
        """Verifica uso peligroso de eval/exec"""
        issues = []
        
        for i, line in enumerate(lines, 1):
            if re.search(r'\b(eval|exec)\s*\(', line):
                issues.append(LintIssue(
                    rule_id="V007",
                    severity=LintSeverity.ERROR,
                    category=LintCategory.SECURITY,
                    message="Uso peligroso de eval/exec",
                    file_path=file_path,
                    line_number=i,
                    column=1,
                    suggestion="Usar alternativas más seguras",
                    context=line.strip()
                ))
        
        return issues
    
    def _calculate_metrics(self, content: str, lines: List[str]) -> Dict[str, Any]:
        """Calcula métricas del código"""
        return {
            'lines_of_code': len(lines),
            'blank_lines': sum(1 for line in lines if not line.strip()),
            'comment_lines': sum(1 for line in lines if line.strip().startswith('#')),
            'function_count': len(re.findall(self.vader_patterns['function_def'], content)),
            'class_count': len(re.findall(self.vader_patterns['class_def'], content)),
            'avg_line_length': sum(len(line) for line in lines) / len(lines) if lines else 0,
        }
    
    def _is_snake_case(self, name: str) -> bool:
        """Verifica si un nombre está en snake_case"""
        return re.match(r'^[a-z][a-z0-9_]*$', name) is not None
    
    def _to_snake_case(self, name: str) -> str:
        """Convierte a snake_case"""
        return re.sub(r'([A-Z])', r'_\1', name).lower().lstrip('_')
    
    def generate_report(self) -> str:
        """Genera reporte de linting"""
        if not self.reports:
            return "No hay reportes disponibles"
        
        report_lines = []
        total_issues = 0
        severity_counts = {severity: 0 for severity in LintSeverity}
        
        for report in self.reports:
            if not report.issues:
                continue
            
            report_lines.append(f"\n📁 {report.file_path}")
            report_lines.append("=" * 60)
            
            for issue in report.issues:
                severity_icon = {
                    LintSeverity.ERROR: "❌",
                    LintSeverity.WARNING: "⚠️",
                    LintSeverity.INFO: "ℹ️",
                    LintSeverity.HINT: "💡"
                }
                
                icon = severity_icon.get(issue.severity, "•")
                report_lines.append(
                    f"{icon} {issue.line_number}:{issue.column} "
                    f"{issue.severity.value.upper()} [{issue.rule_id}] {issue.message}"
                )
                
                if issue.suggestion:
                    report_lines.append(f"   💡 Sugerencia: {issue.suggestion}")
                
                total_issues += 1
                severity_counts[issue.severity] += 1
            
            # Métricas
            metrics = report.metrics
            report_lines.append(f"\n📊 Métricas:")
            report_lines.append(f"   Líneas: {metrics['lines_of_code']}")
            report_lines.append(f"   Funciones: {metrics['function_count']}")
            report_lines.append(f"   Clases: {metrics['class_count']}")
        
        # Resumen
        report_lines.append(f"\n📈 RESUMEN TOTAL:")
        report_lines.append(f"   Total de issues: {total_issues}")
        for severity, count in severity_counts.items():
            if count > 0:
                report_lines.append(f"   {severity.value.capitalize()}: {count}")
        
        return '\n'.join(report_lines)

def main():
    """Función principal para testing"""
    print("🔍 VADER LINTING SYSTEM - Análisis de código:")
    print("=" * 70)
    
    # Crear linter
    linter = VaderLinter()
    
    # Código de prueba con varios problemas
    test_code = """
# Código de prueba para linting
importar os
importar sys  

funcion miFunction(x, y) {    
    # Esta línea es demasiado larga para el límite establecido por defecto que son 100 caracteres de longitud máxima
    variableNoUsada = 42
    resultado = x + y
    
    si (x > 0) {
        si (y > 0) {
            si (resultado > 10) {
                si (resultado > 20) {
                    # Complejidad muy alta
                    eval("print('peligroso')")
                }
            }
        }
    }
    
    retornar resultado
}

clase miClase {
    funcion metodo_sin_docs(self) {
        pasar
    }
}

funcion funcionSinUsar() {
    pasar
}
"""
    
    print("📝 Analizando código de prueba...")
    report = linter.lint_content(test_code, "test.vdr")
    
    print(f"✅ Análisis completado")
    print(f"   Issues encontrados: {len(report.issues)}")
    print(f"   Métricas calculadas: {len(report.metrics)}")
    
    # Mostrar issues por categoría
    categories = {}
    for issue in report.issues:
        if issue.category not in categories:
            categories[issue.category] = []
        categories[issue.category].append(issue)
    
    print(f"\n📊 Issues por categoría:")
    for category, issues in categories.items():
        print(f"   {category.value}: {len(issues)}")
    
    # Generar reporte completo
    print("\n" + linter.generate_report())
    
    print("\n" + "=" * 70)
    print("✅ Sistema de linting Vader implementado")
    print("🚀 Características disponibles:")
    print("  - Análisis estático de código")
    print("  - Validación de estilo y convenciones")
    print("  - Detección de errores potenciales")
    print("  - Métricas de calidad")
    print("  - Reglas personalizables")
    print("  - Categorización de problemas")
    print("  - Sugerencias de mejora")
    print("  - Reportes detallados")

if __name__ == "__main__":
    main()
