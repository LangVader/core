#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VADER 7.0 - FRAMEWORK DE TESTING NATIVO
=======================================
Sistema completo de testing para Vader con pruebas unitarias, integración y E2E

Características:
- Pruebas unitarias con asserts
- Mocking y stubbing
- Coverage reporting
- Test runners paralelos
- Fixtures y setup/teardown
- Pruebas de integración
- Benchmarking
- Continuous testing

Autor: Vader Team
Versión: 7.0.0 "Universal"
Fecha: 2025
"""

import os
import re
import sys
import time
import json
import traceback
import subprocess
from pathlib import Path
from typing import Dict, List, Any, Optional, Callable, Tuple
from dataclasses import dataclass, field
from enum import Enum
import unittest
import threading
from concurrent.futures import ThreadPoolExecutor
import coverage

class TestStatus(Enum):
    """Estados de las pruebas"""
    PENDING = "pending"
    RUNNING = "running"
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"
    ERROR = "error"

@dataclass
class TestResult:
    """Resultado de una prueba individual"""
    name: str
    status: TestStatus
    duration: float
    message: str = ""
    stack_trace: str = ""
    assertions: int = 0
    file_path: str = ""
    line_number: int = 0

@dataclass
class TestSuite:
    """Suite de pruebas"""
    name: str
    file_path: str
    tests: List[TestResult] = field(default_factory=list)
    setup_code: str = ""
    teardown_code: str = ""
    fixtures: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def total_tests(self) -> int:
        return len(self.tests)
    
    @property
    def passed_tests(self) -> int:
        return len([t for t in self.tests if t.status == TestStatus.PASSED])
    
    @property
    def failed_tests(self) -> int:
        return len([t for t in self.tests if t.status == TestStatus.FAILED])
    
    @property
    def success_rate(self) -> float:
        if self.total_tests == 0:
            return 0.0
        return (self.passed_tests / self.total_tests) * 100

@dataclass
class TestReport:
    """Reporte completo de testing"""
    suites: List[TestSuite] = field(default_factory=list)
    total_duration: float = 0.0
    coverage_data: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = ""
    
    @property
    def total_tests(self) -> int:
        return sum(suite.total_tests for suite in self.suites)
    
    @property
    def passed_tests(self) -> int:
        return sum(suite.passed_tests for suite in self.suites)
    
    @property
    def failed_tests(self) -> int:
        return sum(suite.failed_tests for suite in self.suites)
    
    @property
    def success_rate(self) -> float:
        if self.total_tests == 0:
            return 0.0
        return (self.passed_tests / self.total_tests) * 100

class VaderAssert:
    """Sistema de assertions para Vader"""
    
    def __init__(self):
        self.assertion_count = 0
    
    def afirmar(self, condition: bool, message: str = "Assertion failed"):
        """Assertion básica"""
        self.assertion_count += 1
        if not condition:
            raise AssertionError(f"❌ {message}")
    
    def afirmar_igual(self, actual: Any, expected: Any, message: str = None):
        """Assertion de igualdad"""
        self.assertion_count += 1
        if actual != expected:
            msg = message or f"Se esperaba {expected}, pero se obtuvo {actual}"
            raise AssertionError(f"❌ {msg}")
    
    def afirmar_no_igual(self, actual: Any, expected: Any, message: str = None):
        """Assertion de desigualdad"""
        self.assertion_count += 1
        if actual == expected:
            msg = message or f"No se esperaba {expected}"
            raise AssertionError(f"❌ {msg}")
    
    def afirmar_verdadero(self, condition: bool, message: str = None):
        """Assertion de verdadero"""
        self.assertion_count += 1
        if not condition:
            msg = message or "Se esperaba verdadero"
            raise AssertionError(f"❌ {msg}")
    
    def afirmar_falso(self, condition: bool, message: str = None):
        """Assertion de falso"""
        self.assertion_count += 1
        if condition:
            msg = message or "Se esperaba falso"
            raise AssertionError(f"❌ {msg}")
    
    def afirmar_nulo(self, value: Any, message: str = None):
        """Assertion de nulo"""
        self.assertion_count += 1
        if value is not None:
            msg = message or f"Se esperaba nulo, pero se obtuvo {value}"
            raise AssertionError(f"❌ {msg}")
    
    def afirmar_no_nulo(self, value: Any, message: str = None):
        """Assertion de no nulo"""
        self.assertion_count += 1
        if value is None:
            msg = message or "Se esperaba un valor no nulo"
            raise AssertionError(f"❌ {msg}")
    
    def afirmar_contiene(self, container: Any, item: Any, message: str = None):
        """Assertion de contención"""
        self.assertion_count += 1
        if item not in container:
            msg = message or f"Se esperaba que {container} contuviera {item}"
            raise AssertionError(f"❌ {msg}")
    
    def afirmar_tipo(self, value: Any, expected_type: type, message: str = None):
        """Assertion de tipo"""
        self.assertion_count += 1
        if not isinstance(value, expected_type):
            msg = message or f"Se esperaba tipo {expected_type.__name__}, pero se obtuvo {type(value).__name__}"
            raise AssertionError(f"❌ {msg}")
    
    def afirmar_excepcion(self, func: Callable, exception_type: type = Exception, message: str = None):
        """Assertion de excepción"""
        self.assertion_count += 1
        try:
            func()
            msg = message or f"Se esperaba excepción {exception_type.__name__}"
            raise AssertionError(f"❌ {msg}")
        except exception_type:
            pass  # Excepción esperada
        except Exception as e:
            msg = message or f"Se esperaba {exception_type.__name__}, pero se obtuvo {type(e).__name__}"
            raise AssertionError(f"❌ {msg}")

class VaderTestRunner:
    """Ejecutor de pruebas Vader"""
    
    def __init__(self, coverage_enabled: bool = True):
        self.coverage_enabled = coverage_enabled
        self.coverage = None
        if coverage_enabled:
            self.coverage = coverage.Coverage()
        
        # Patrones de reconocimiento
        self.test_patterns = {
            'test_function': r'prueba\s+(\w+)\s*\(',
            'test_suite': r'suite\s+(\w+)\s*\{',
            'setup': r'antes_de_cada\s*\(',
            'teardown': r'despues_de_cada\s*\(',
            'fixture': r'fixture\s+(\w+)\s*\(',
            'mock': r'mock\s+(\w+)\s*=',
            'benchmark': r'benchmark\s+(\w+)\s*\(',
        }
    
    def discover_tests(self, directory: str, pattern: str = "*.test.vdr") -> List[str]:
        """Descubre archivos de prueba"""
        test_files = []
        path = Path(directory)
        
        for file_path in path.rglob(pattern):
            if file_path.is_file():
                test_files.append(str(file_path))
        
        return test_files
    
    def parse_test_file(self, file_path: str) -> TestSuite:
        """Parsea un archivo de pruebas Vader"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        suite_name = Path(file_path).stem
        suite = TestSuite(name=suite_name, file_path=file_path)
        
        lines = content.split('\n')
        current_test = None
        current_function = []
        in_test = False
        
        for line_num, line in enumerate(lines, 1):
            line_stripped = line.strip()
            
            # Función de prueba
            test_match = re.match(self.test_patterns['test_function'], line_stripped)
            if test_match:
                test_name = test_match.group(1)
                current_test = TestResult(
                    name=test_name,
                    status=TestStatus.PENDING,
                    duration=0.0,
                    file_path=file_path,
                    line_number=line_num
                )
                in_test = True
                current_function = []
                continue
            
            # Fin de función
            if in_test and line_stripped.startswith('fin prueba'):
                if current_test:
                    # Guardar código de la prueba
                    current_test.message = '\n'.join(current_function)
                    suite.tests.append(current_test)
                in_test = False
                current_test = None
                current_function = []
                continue
            
            # Código dentro de la prueba
            if in_test and current_test:
                current_function.append(line)
            
            # Setup
            if re.match(self.test_patterns['setup'], line_stripped):
                # Extraer código de setup
                setup_lines = []
                for i in range(line_num, len(lines)):
                    if lines[i].strip().startswith('fin antes_de_cada'):
                        break
                    setup_lines.append(lines[i])
                suite.setup_code = '\n'.join(setup_lines)
            
            # Teardown
            if re.match(self.test_patterns['teardown'], line_stripped):
                # Extraer código de teardown
                teardown_lines = []
                for i in range(line_num, len(lines)):
                    if lines[i].strip().startswith('fin despues_de_cada'):
                        break
                    teardown_lines.append(lines[i])
                suite.teardown_code = '\n'.join(teardown_lines)
        
        return suite
    
    def execute_test(self, test: TestResult, suite: TestSuite, assert_instance: VaderAssert) -> TestResult:
        """Ejecuta una prueba individual"""
        start_time = time.time()
        
        try:
            # Ejecutar setup si existe
            if suite.setup_code:
                exec(suite.setup_code)
            
            # Ejecutar código de la prueba
            test_code = test.message
            
            # Reemplazar sintaxis Vader con Python equivalente
            test_code = self._translate_vader_to_python(test_code, assert_instance)
            
            # Ejecutar prueba
            exec(test_code)
            
            # Ejecutar teardown si existe
            if suite.teardown_code:
                exec(suite.teardown_code)
            
            test.status = TestStatus.PASSED
            test.assertions = assert_instance.assertion_count
            
        except AssertionError as e:
            test.status = TestStatus.FAILED
            test.message = str(e)
            test.stack_trace = traceback.format_exc()
            
        except Exception as e:
            test.status = TestStatus.ERROR
            test.message = f"Error inesperado: {str(e)}"
            test.stack_trace = traceback.format_exc()
        
        finally:
            test.duration = time.time() - start_time
        
        return test
    
    def _translate_vader_to_python(self, vader_code: str, assert_instance: VaderAssert) -> str:
        """Traduce código Vader a Python para ejecución"""
        python_code = vader_code
        
        # Reemplazar assertions
        python_code = re.sub(r'afirmar\s+(.+)', r'assert_instance.afirmar(\1)', python_code)
        python_code = re.sub(r'afirmar_igual\s*\(([^,]+),\s*([^)]+)\)', r'assert_instance.afirmar_igual(\1, \2)', python_code)
        python_code = re.sub(r'afirmar_verdadero\s*\(([^)]+)\)', r'assert_instance.afirmar_verdadero(\1)', python_code)
        python_code = re.sub(r'afirmar_falso\s*\(([^)]+)\)', r'assert_instance.afirmar_falso(\1)', python_code)
        
        # Reemplazar sintaxis básica
        python_code = re.sub(r'\bsi\b', 'if', python_code)
        python_code = re.sub(r'\bsino\b', 'else', python_code)
        python_code = re.sub(r'\bpara\b', 'for', python_code)
        python_code = re.sub(r'\bmientras\b', 'while', python_code)
        python_code = re.sub(r'\bverdadero\b', 'True', python_code)
        python_code = re.sub(r'\bfalso\b', 'False', python_code)
        python_code = re.sub(r'\bnulo\b', 'None', python_code)
        
        return python_code
    
    def run_suite(self, suite: TestSuite, parallel: bool = False) -> TestSuite:
        """Ejecuta una suite de pruebas"""
        print(f"🧪 Ejecutando suite: {suite.name}")
        
        if parallel and len(suite.tests) > 1:
            # Ejecución paralela
            with ThreadPoolExecutor(max_workers=4) as executor:
                futures = []
                
                for test in suite.tests:
                    assert_instance = VaderAssert()
                    future = executor.submit(self.execute_test, test, suite, assert_instance)
                    futures.append((future, test))
                
                for future, test in futures:
                    result = future.result()
                    # Actualizar test con resultado
                    test.status = result.status
                    test.duration = result.duration
                    test.message = result.message
                    test.stack_trace = result.stack_trace
                    test.assertions = result.assertions
        else:
            # Ejecución secuencial
            for test in suite.tests:
                assert_instance = VaderAssert()
                self.execute_test(test, suite, assert_instance)
        
        return suite
    
    def run_tests(self, test_files: List[str], parallel: bool = False) -> TestReport:
        """Ejecuta todas las pruebas"""
        start_time = time.time()
        
        if self.coverage_enabled and self.coverage:
            self.coverage.start()
        
        report = TestReport()
        report.timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        
        for test_file in test_files:
            print(f"📁 Procesando: {test_file}")
            
            try:
                suite = self.parse_test_file(test_file)
                suite = self.run_suite(suite, parallel)
                report.suites.append(suite)
                
                # Mostrar resultados de la suite
                print(f"  ✅ Pasaron: {suite.passed_tests}")
                print(f"  ❌ Fallaron: {suite.failed_tests}")
                print(f"  📊 Tasa de éxito: {suite.success_rate:.1f}%")
                print()
                
            except Exception as e:
                print(f"❌ Error procesando {test_file}: {e}")
        
        if self.coverage_enabled and self.coverage:
            self.coverage.stop()
            self.coverage.save()
            
            # Generar reporte de coverage
            report.coverage_data = self._generate_coverage_report()
        
        report.total_duration = time.time() - start_time
        return report
    
    def _generate_coverage_report(self) -> Dict[str, Any]:
        """Genera reporte de cobertura de código"""
        if not self.coverage:
            return {}
        
        coverage_data = {}
        
        try:
            # Obtener datos de cobertura
            self.coverage.load()
            
            # Generar reporte
            with open('coverage_report.txt', 'w') as f:
                self.coverage.report(file=f)
            
            # Leer reporte generado
            with open('coverage_report.txt', 'r') as f:
                coverage_text = f.read()
            
            # Parsear datos básicos
            lines = coverage_text.split('\n')
            for line in lines:
                if 'TOTAL' in line:
                    parts = line.split()
                    if len(parts) >= 4:
                        coverage_data = {
                            'statements': int(parts[1]) if parts[1].isdigit() else 0,
                            'missing': int(parts[2]) if parts[2].isdigit() else 0,
                            'coverage': parts[3] if '%' in parts[3] else '0%'
                        }
                    break
            
            # Limpiar archivo temporal
            os.remove('coverage_report.txt')
            
        except Exception as e:
            coverage_data = {'error': str(e)}
        
        return coverage_data
    
    def generate_html_report(self, report: TestReport, output_file: str = "test_report.html"):
        """Genera reporte HTML"""
        html_content = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reporte de Pruebas Vader</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .header {{ background: #2c3e50; color: white; padding: 20px; border-radius: 5px; }}
        .summary {{ display: flex; gap: 20px; margin: 20px 0; }}
        .metric {{ background: #ecf0f1; padding: 15px; border-radius: 5px; text-align: center; }}
        .suite {{ margin: 20px 0; border: 1px solid #ddd; border-radius: 5px; }}
        .suite-header {{ background: #34495e; color: white; padding: 10px; }}
        .test {{ padding: 10px; border-bottom: 1px solid #eee; }}
        .passed {{ background: #d5f4e6; }}
        .failed {{ background: #ffeaa7; }}
        .error {{ background: #fab1a0; }}
        .stack-trace {{ background: #2d3436; color: white; padding: 10px; font-family: monospace; font-size: 12px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🧪 Reporte de Pruebas Vader</h1>
        <p>Generado: {report.timestamp}</p>
    </div>
    
    <div class="summary">
        <div class="metric">
            <h3>{report.total_tests}</h3>
            <p>Total de Pruebas</p>
        </div>
        <div class="metric">
            <h3>{report.passed_tests}</h3>
            <p>Pasaron</p>
        </div>
        <div class="metric">
            <h3>{report.failed_tests}</h3>
            <p>Fallaron</p>
        </div>
        <div class="metric">
            <h3>{report.success_rate:.1f}%</h3>
            <p>Tasa de Éxito</p>
        </div>
        <div class="metric">
            <h3>{report.total_duration:.2f}s</h3>
            <p>Duración Total</p>
        </div>
    </div>
"""
        
        # Agregar suites
        for suite in report.suites:
            html_content += f"""
    <div class="suite">
        <div class="suite-header">
            <h3>📁 {suite.name}</h3>
            <p>{suite.file_path}</p>
        </div>
"""
            
            # Agregar pruebas
            for test in suite.tests:
                status_class = test.status.value
                status_icon = {
                    'passed': '✅',
                    'failed': '❌',
                    'error': '💥',
                    'skipped': '⏭️'
                }.get(test.status.value, '❓')
                
                html_content += f"""
        <div class="test {status_class}">
            <h4>{status_icon} {test.name}</h4>
            <p>Duración: {test.duration:.3f}s | Assertions: {test.assertions}</p>
"""
                
                if test.message and test.status != TestStatus.PASSED:
                    html_content += f"<p><strong>Mensaje:</strong> {test.message}</p>"
                
                if test.stack_trace:
                    html_content += f'<div class="stack-trace">{test.stack_trace}</div>'
                
                html_content += "</div>"
            
            html_content += "</div>"
        
        # Agregar cobertura si está disponible
        if report.coverage_data:
            html_content += f"""
    <div class="suite">
        <div class="suite-header">
            <h3>📊 Cobertura de Código</h3>
        </div>
        <div class="test">
            <p><strong>Cobertura:</strong> {report.coverage_data.get('coverage', 'N/A')}</p>
            <p><strong>Declaraciones:</strong> {report.coverage_data.get('statements', 'N/A')}</p>
            <p><strong>Faltantes:</strong> {report.coverage_data.get('missing', 'N/A')}</p>
        </div>
    </div>
"""
        
        html_content += """
</body>
</html>
"""
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"📄 Reporte HTML generado: {output_file}")

def main():
    """Función principal del CLI de testing"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Vader Testing Framework")
    parser.add_argument('directory', nargs='?', default='.', help='Directorio de pruebas')
    parser.add_argument('--pattern', default='*.test.vdr', help='Patrón de archivos de prueba')
    parser.add_argument('--parallel', action='store_true', help='Ejecución paralela')
    parser.add_argument('--no-coverage', action='store_true', help='Deshabilitar cobertura')
    parser.add_argument('--html-report', help='Generar reporte HTML')
    
    args = parser.parse_args()
    
    # Crear runner
    runner = VaderTestRunner(coverage_enabled=not args.no_coverage)
    
    # Descubrir pruebas
    test_files = runner.discover_tests(args.directory, args.pattern)
    
    if not test_files:
        print(f"❌ No se encontraron archivos de prueba con patrón '{args.pattern}' en '{args.directory}'")
        return
    
    print(f"🔍 Encontrados {len(test_files)} archivos de prueba")
    print()
    
    # Ejecutar pruebas
    report = runner.run_tests(test_files, args.parallel)
    
    # Mostrar resumen
    print("=" * 60)
    print("📊 RESUMEN FINAL")
    print("=" * 60)
    print(f"🧪 Total de pruebas: {report.total_tests}")
    print(f"✅ Pasaron: {report.passed_tests}")
    print(f"❌ Fallaron: {report.failed_tests}")
    print(f"📈 Tasa de éxito: {report.success_rate:.1f}%")
    print(f"⏱️ Duración total: {report.total_duration:.2f}s")
    
    if report.coverage_data:
        print(f"📊 Cobertura: {report.coverage_data.get('coverage', 'N/A')}")
    
    # Generar reporte HTML si se solicita
    if args.html_report:
        runner.generate_html_report(report, args.html_report)
    
    # Código de salida
    sys.exit(0 if report.failed_tests == 0 else 1)

if __name__ == "__main__":
    main()
