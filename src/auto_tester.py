#!/usr/bin/env python3
"""
Sistema de Testing Automático para Vader
Valida que el código transpilado funcione correctamente
"""

import os
import sys
import subprocess
import tempfile
import json
from pathlib import Path
from datetime import datetime

class VaderAutoTester:
    def __init__(self):
        self.results = {
            'total_tests': 0,
            'passed': 0,
            'failed': 0,
            'errors': [],
            'timestamp': datetime.now().isoformat()
        }
    
    def test_python_transpilation(self, vader_code, expected_output=None):
        """Prueba la transpilación a Python y su ejecución"""
        try:
            # Importar transpilador
            sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            from transpilers.python import transpile_to_python
            
            # Transpilar código
            python_code = transpile_to_python(vader_code)
            
            # Validar sintaxis
            try:
                compile(python_code, '<string>', 'exec')
                syntax_valid = True
            except SyntaxError as e:
                syntax_valid = False
                error_msg = f"Error de sintaxis: {e}"
                self.results['errors'].append({
                    'type': 'syntax_error',
                    'message': error_msg,
                    'code': vader_code[:100] + '...' if len(vader_code) > 100 else vader_code
                })
                return False
            
            # Ejecutar código y capturar salida
            if syntax_valid:
                try:
                    # Crear archivo temporal
                    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                        f.write(python_code)
                        temp_file = f.name
                    
                    # Ejecutar y capturar salida
                    result = subprocess.run([sys.executable, temp_file], 
                                          capture_output=True, text=True, timeout=10)
                    
                    # Limpiar archivo temporal
                    os.unlink(temp_file)
                    
                    if result.returncode == 0:
                        execution_success = True
                        output = result.stdout
                    else:
                        execution_success = False
                        error_msg = f"Error de ejecución: {result.stderr}"
                        self.results['errors'].append({
                            'type': 'execution_error',
                            'message': error_msg,
                            'code': vader_code[:100] + '...' if len(vader_code) > 100 else vader_code
                        })
                        return False
                    
                except subprocess.TimeoutExpired:
                    execution_success = False
                    error_msg = "Timeout: El código tardó más de 10 segundos en ejecutar"
                    self.results['errors'].append({
                        'type': 'timeout_error',
                        'message': error_msg,
                        'code': vader_code[:100] + '...' if len(vader_code) > 100 else vader_code
                    })
                    return False
                except Exception as e:
                    execution_success = False
                    error_msg = f"Error inesperado: {str(e)}"
                    self.results['errors'].append({
                        'type': 'unexpected_error',
                        'message': error_msg,
                        'code': vader_code[:100] + '...' if len(vader_code) > 100 else vader_code
                    })
                    return False
            
            # Verificar salida esperada si se proporciona
            if expected_output and execution_success:
                if expected_output.strip() in output.strip():
                    return True
                else:
                    error_msg = f"Salida esperada: '{expected_output}', Salida obtenida: '{output}'"
                    self.results['errors'].append({
                        'type': 'output_mismatch',
                        'message': error_msg,
                        'code': vader_code[:100] + '...' if len(vader_code) > 100 else vader_code
                    })
                    return False
            
            return execution_success
            
        except Exception as e:
            error_msg = f"Error en test de transpilación: {str(e)}"
            self.results['errors'].append({
                'type': 'transpilation_error',
                'message': error_msg,
                'code': vader_code[:100] + '...' if len(vader_code) > 100 else vader_code
            })
            return False
    
    def test_javascript_transpilation(self, vader_code):
        """Prueba la transpilación a JavaScript"""
        try:
            from transpilers.javascript import transpile_to_javascript
            js_code = transpile_to_javascript(vader_code)
            
            # Validación básica de JavaScript (verificar que no esté vacío)
            if js_code and len(js_code.strip()) > 0:
                return True
            else:
                self.results['errors'].append({
                    'type': 'empty_js_output',
                    'message': 'Transpilación JavaScript produjo código vacío',
                    'code': vader_code[:100] + '...' if len(vader_code) > 100 else vader_code
                })
                return False
                
        except Exception as e:
            error_msg = f"Error en transpilación JavaScript: {str(e)}"
            self.results['errors'].append({
                'type': 'js_transpilation_error',
                'message': error_msg,
                'code': vader_code[:100] + '...' if len(vader_code) > 100 else vader_code
            })
            return False
    
    def run_comprehensive_tests(self):
        """Ejecuta una suite completa de tests"""
        print("🧪 Iniciando tests automáticos de Vader...")
        
        # Tests básicos
        basic_tests = [
            {
                'name': 'Variables básicas',
                'code': '''nombre = "Juan"
edad = 25
activo = verdadero
mostrar nombre''',
                'expected': 'Juan'
            },
            {
                'name': 'Condicionales',
                'code': '''edad = 20
si edad >= 18 entonces
    mostrar "Mayor de edad"
sino
    mostrar "Menor de edad"
fin si''',
                'expected': 'Mayor de edad'
            },
            {
                'name': 'Bucles',
                'code': '''para cada numero en [1, 2, 3]
    mostrar numero
fin''',
                'expected': '1\n2\n3'
            },
            {
                'name': 'Funciones',
                'code': '''funcion saludar con nombre
    mostrar "Hola " + nombre
fin

saludar con "Mundo"''',
                'expected': 'Hola Mundo'
            },
            {
                'name': 'Matemáticas',
                'code': '''resultado = 10 + 5
mostrar resultado''',
                'expected': '15'
            }
        ]
        
        print(f"\n📋 Ejecutando {len(basic_tests)} tests básicos...")
        
        for i, test in enumerate(basic_tests, 1):
            print(f"  {i}. {test['name']}... ", end='')
            self.results['total_tests'] += 1
            
            if self.test_python_transpilation(test['code'], test.get('expected')):
                print("✅ PASÓ")
                self.results['passed'] += 1
            else:
                print("❌ FALLÓ")
                self.results['failed'] += 1
        
        # Tests de transpiladores
        print(f"\n🔄 Probando transpiladores...")
        transpiler_tests = [
            {
                'name': 'Python',
                'code': 'mostrar "Hola Python"',
                'test_func': self.test_python_transpilation
            },
            {
                'name': 'JavaScript',
                'code': 'mostrar "Hola JavaScript"',
                'test_func': self.test_javascript_transpilation
            }
        ]
        
        for test in transpiler_tests:
            print(f"  Transpilador {test['name']}... ", end='')
            self.results['total_tests'] += 1
            
            if test['test_func'](test['code']):
                print("✅ PASÓ")
                self.results['passed'] += 1
            else:
                print("❌ FALLÓ")
                self.results['failed'] += 1
        
        # Resumen
        print(f"\n📊 RESUMEN DE TESTS:")
        print(f"  Total: {self.results['total_tests']}")
        print(f"  ✅ Pasaron: {self.results['passed']}")
        print(f"  ❌ Fallaron: {self.results['failed']}")
        
        if self.results['failed'] > 0:
            print(f"\n🚨 ERRORES ENCONTRADOS:")
            for i, error in enumerate(self.results['errors'], 1):
                print(f"  {i}. {error['type']}: {error['message']}")
        
        success_rate = (self.results['passed'] / self.results['total_tests']) * 100
        print(f"\n🎯 Tasa de éxito: {success_rate:.1f}%")
        
        return self.results
    
    def save_results(self, filename="test_results.json"):
        """Guarda los resultados en un archivo JSON"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        print(f"📄 Resultados guardados en: {filename}")

def run_auto_tests():
    """Función principal para ejecutar tests automáticos"""
    tester = VaderAutoTester()
    results = tester.run_comprehensive_tests()
    tester.save_results()
    return results

if __name__ == "__main__":
    run_auto_tests()
