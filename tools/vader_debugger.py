#!/usr/bin/env python3
"""
Vader Debugger - Herramientas avanzadas de debugging para código Vader
Incluye depuración paso a paso, profiling, análisis de logs y detección de errores
"""

import os
import sys
import json
import time
import traceback
import logging
import cProfile
import pstats
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime

class VaderDebugger:
    """Debugger avanzado para código Vader"""
    
    def __init__(self):
        self.debug_session = None
        self.breakpoints = []
        self.call_stack = []
        self.variables = {}
        self.execution_log = []
        self.profiler = None
        self.is_debugging = False
        
        # Configurar logging
        self.setup_logging()
        
        print("🐛 Vader Debugger inicializado")
    
    def setup_logging(self):
        """Configurar sistema de logging"""
        log_dir = Path('./logs')
        log_dir.mkdir(exist_ok=True)
        
        # Configurar logger principal
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / 'vader_debug.log'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        
        self.logger = logging.getLogger('VaderDebugger')
        self.logger.info("Sistema de logging configurado")
    
    def start_debug_session(self, vader_code: str, target_language: str = 'python'):
        """Iniciar sesión de debugging"""
        self.debug_session = {
            'id': f"debug_{int(time.time())}",
            'vader_code': vader_code,
            'target_language': target_language,
            'start_time': datetime.now(),
            'status': 'active'
        }
        
        self.is_debugging = True
        self.execution_log = []
        self.call_stack = []
        self.variables = {}
        
        self.logger.info(f"Sesión de debugging iniciada: {self.debug_session['id']}")
        print(f"🚀 Sesión de debugging iniciada: {self.debug_session['id']}")
        
        return self.debug_session['id']
    
    def add_breakpoint(self, line_number: int, condition: str = None):
        """Agregar breakpoint en línea específica"""
        breakpoint = {
            'line': line_number,
            'condition': condition,
            'hit_count': 0,
            'enabled': True,
            'id': len(self.breakpoints) + 1
        }
        
        self.breakpoints.append(breakpoint)
        self.logger.info(f"Breakpoint agregado en línea {line_number}")
        print(f"🔴 Breakpoint agregado en línea {line_number}")
        
        return breakpoint['id']
    
    def remove_breakpoint(self, breakpoint_id: int):
        """Remover breakpoint por ID"""
        self.breakpoints = [bp for bp in self.breakpoints if bp['id'] != breakpoint_id]
        self.logger.info(f"Breakpoint {breakpoint_id} removido")
        print(f"⚪ Breakpoint {breakpoint_id} removido")
    
    def step_through_code(self, vader_code: str) -> List[Dict]:
        """Ejecutar código paso a paso con debugging"""
        if not self.is_debugging:
            print("⚠️ Iniciar sesión de debugging primero")
            return []
        
        lines = vader_code.split('\n')
        execution_steps = []
        
        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            # Verificar breakpoints
            if self.should_break(line_num, line):
                self.handle_breakpoint(line_num, line)
            
            # Ejecutar paso
            step_info = self.execute_step(line_num, line)
            execution_steps.append(step_info)
            
            # Log del paso
            self.log_execution_step(step_info)
        
        return execution_steps
    
    def should_break(self, line_number: int, line: str) -> bool:
        """Verificar si debe parar en breakpoint"""
        for bp in self.breakpoints:
            if bp['enabled'] and bp['line'] == line_number:
                # Verificar condición si existe
                if bp['condition']:
                    try:
                        # Evaluar condición en contexto actual
                        if eval(bp['condition'], {}, self.variables):
                            bp['hit_count'] += 1
                            return True
                    except:
                        self.logger.warning(f"Error evaluando condición de breakpoint: {bp['condition']}")
                        return True
                else:
                    bp['hit_count'] += 1
                    return True
        
        return False
    
    def handle_breakpoint(self, line_number: int, line: str):
        """Manejar parada en breakpoint"""
        print(f"\n🔴 BREAKPOINT en línea {line_number}: {line}")
        print(f"📊 Variables actuales: {self.variables}")
        print(f"📚 Call stack: {self.call_stack}")
        
        # Interfaz interactiva simple
        while True:
            command = input("Debug> ").strip().lower()
            
            if command in ['c', 'continue']:
                break
            elif command in ['s', 'step']:
                break
            elif command in ['n', 'next']:
                break
            elif command.startswith('p '):
                # Print variable
                var_name = command[2:]
                if var_name in self.variables:
                    print(f"{var_name} = {self.variables[var_name]}")
                else:
                    print(f"Variable '{var_name}' no encontrada")
            elif command in ['vars', 'variables']:
                print("Variables:", self.variables)
            elif command in ['stack']:
                print("Call stack:", self.call_stack)
            elif command in ['h', 'help']:
                self.show_debug_help()
            elif command in ['q', 'quit']:
                self.stop_debug_session()
                return
            else:
                print("Comando no reconocido. Usa 'h' para ayuda.")
    
    def execute_step(self, line_number: int, line: str) -> Dict:
        """Ejecutar un paso individual del código"""
        step_start = time.time()
        
        step_info = {
            'line_number': line_number,
            'line_content': line,
            'timestamp': datetime.now(),
            'variables_before': self.variables.copy(),
            'call_stack_before': self.call_stack.copy()
        }
        
        try:
            # Simular ejecución y actualizar variables
            self.simulate_vader_execution(line)
            
            step_info['status'] = 'success'
            step_info['execution_time'] = time.time() - step_start
            step_info['variables_after'] = self.variables.copy()
            step_info['call_stack_after'] = self.call_stack.copy()
            
        except Exception as e:
            step_info['status'] = 'error'
            step_info['error'] = str(e)
            step_info['traceback'] = traceback.format_exc()
            
            self.logger.error(f"Error en línea {line_number}: {e}")
        
        return step_info
    
    def simulate_vader_execution(self, line: str):
        """Simular ejecución de línea Vader y actualizar estado"""
        line = line.strip().lower()
        
        # Detectar asignaciones de variables
        if '=' in line and not any(op in line for op in ['==', '!=', '>=', '<=']):
            parts = line.split('=', 1)
            var_name = parts[0].strip()
            var_value = parts[1].strip().replace('"', '').replace("'", '')
            
            # Intentar convertir a número si es posible
            try:
                if '.' in var_value:
                    var_value = float(var_value)
                else:
                    var_value = int(var_value)
            except ValueError:
                pass  # Mantener como string
            
            self.variables[var_name] = var_value
        
        # Detectar llamadas a funciones
        if 'funcion' in line or 'def' in line:
            func_name = line.split()[1] if len(line.split()) > 1 else 'unknown'
            self.call_stack.append(func_name)
        
        # Detectar fin de función
        if line == 'fin' or line == 'return':
            if self.call_stack:
                self.call_stack.pop()
    
    def log_execution_step(self, step_info: Dict):
        """Registrar paso de ejecución en log"""
        self.execution_log.append(step_info)
        
        if step_info['status'] == 'success':
            self.logger.debug(f"Línea {step_info['line_number']}: {step_info['line_content']}")
        else:
            self.logger.error(f"Error en línea {step_info['line_number']}: {step_info.get('error', 'Unknown error')}")
    
    def show_debug_help(self):
        """Mostrar ayuda de comandos de debugging"""
        help_text = """
🐛 COMANDOS DE DEBUGGING:

c, continue  - Continuar ejecución
s, step      - Ejecutar siguiente línea
n, next      - Ejecutar siguiente línea (sin entrar en funciones)
p <var>      - Mostrar valor de variable
vars         - Mostrar todas las variables
stack        - Mostrar call stack
h, help      - Mostrar esta ayuda
q, quit      - Salir del debugger

Ejemplo: p mi_variable
"""
        print(help_text)
    
    def start_profiling(self):
        """Iniciar profiling de rendimiento"""
        self.profiler = cProfile.Profile()
        self.profiler.enable()
        self.logger.info("Profiling iniciado")
        print("📊 Profiling de rendimiento iniciado")
    
    def stop_profiling(self, output_file: str = None):
        """Detener profiling y generar reporte"""
        if not self.profiler:
            print("⚠️ Profiling no está activo")
            return
        
        self.profiler.disable()
        
        # Generar reporte
        if output_file is None:
            output_file = f"./logs/profile_{int(time.time())}.txt"
        
        with open(output_file, 'w') as f:
            stats = pstats.Stats(self.profiler, stream=f)
            stats.sort_stats('cumulative')
            stats.print_stats()
        
        self.logger.info(f"Reporte de profiling guardado en {output_file}")
        print(f"📊 Reporte de profiling guardado en {output_file}")
        
        # Mostrar resumen en consola
        stats = pstats.Stats(self.profiler)
        stats.sort_stats('cumulative')
        print("\n📈 TOP 10 FUNCIONES MÁS COSTOSAS:")
        stats.print_stats(10)
    
    def analyze_performance(self, execution_steps: List[Dict]) -> Dict:
        """Analizar rendimiento de ejecución"""
        if not execution_steps:
            return {}
        
        total_time = sum(step.get('execution_time', 0) for step in execution_steps)
        successful_steps = [step for step in execution_steps if step['status'] == 'success']
        error_steps = [step for step in execution_steps if step['status'] == 'error']
        
        # Encontrar líneas más lentas
        slowest_lines = sorted(
            [step for step in execution_steps if 'execution_time' in step],
            key=lambda x: x['execution_time'],
            reverse=True
        )[:5]
        
        analysis = {
            'total_execution_time': total_time,
            'total_steps': len(execution_steps),
            'successful_steps': len(successful_steps),
            'error_steps': len(error_steps),
            'average_step_time': total_time / len(execution_steps) if execution_steps else 0,
            'slowest_lines': [
                {
                    'line_number': step['line_number'],
                    'line_content': step['line_content'],
                    'execution_time': step['execution_time']
                }
                for step in slowest_lines
            ],
            'error_summary': [
                {
                    'line_number': step['line_number'],
                    'error': step['error']
                }
                for step in error_steps
            ]
        }
        
        return analysis
    
    def generate_debug_report(self, output_file: str = None) -> str:
        """Generar reporte completo de debugging"""
        if not self.debug_session:
            print("⚠️ No hay sesión de debugging activa")
            return ""
        
        if output_file is None:
            output_file = f"./logs/debug_report_{self.debug_session['id']}.json"
        
        # Analizar rendimiento
        performance_analysis = self.analyze_performance(self.execution_log)
        
        report = {
            'session_info': self.debug_session,
            'breakpoints': self.breakpoints,
            'execution_log': self.execution_log,
            'final_variables': self.variables,
            'final_call_stack': self.call_stack,
            'performance_analysis': performance_analysis,
            'generated_at': datetime.now().isoformat()
        }
        
        # Guardar reporte
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, default=str)
        
        self.logger.info(f"Reporte de debugging guardado en {output_file}")
        print(f"📄 Reporte de debugging guardado en {output_file}")
        
        return output_file
    
    def detect_common_errors(self, vader_code: str) -> List[Dict]:
        """Detectar errores comunes en código Vader"""
        errors = []
        lines = vader_code.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            # Detectar variables no definidas
            if '=' not in line and any(word.isalpha() for word in line.split()):
                words = [w for w in line.split() if w.isalpha() and w not in ['si', 'entonces', 'sino', 'fin', 'mientras', 'para']]
                for word in words:
                    if word not in self.variables and word not in ['mostrar', 'decir', 'leer']:
                        errors.append({
                            'type': 'undefined_variable',
                            'line_number': line_num,
                            'line_content': line,
                            'variable': word,
                            'message': f"Variable '{word}' posiblemente no definida"
                        })
            
            # Detectar sintaxis incorrecta
            if line.startswith('si ') and not line.endswith(' entonces'):
                errors.append({
                    'type': 'syntax_error',
                    'line_number': line_num,
                    'line_content': line,
                    'message': "Falta 'entonces' después de condición 'si'"
                })
            
            # Detectar bucles infinitos potenciales
            if line.startswith('mientras ') and 'verdadero' in line.lower():
                errors.append({
                    'type': 'infinite_loop',
                    'line_number': line_num,
                    'line_content': line,
                    'message': "Posible bucle infinito detectado"
                })
        
        return errors
    
    def stop_debug_session(self):
        """Detener sesión de debugging"""
        if self.debug_session:
            self.debug_session['status'] = 'completed'
            self.debug_session['end_time'] = datetime.now()
            
            # Generar reporte final
            report_file = self.generate_debug_report()
            
            self.logger.info(f"Sesión de debugging completada: {self.debug_session['id']}")
            print(f"🏁 Sesión de debugging completada: {self.debug_session['id']}")
            print(f"📄 Reporte guardado en: {report_file}")
            
            self.is_debugging = False
        else:
            print("⚠️ No hay sesión de debugging activa")

def main():
    """Función principal para testing del debugger"""
    debugger = VaderDebugger()
    
    # Código Vader de ejemplo para debugging
    vader_code = """# Ejemplo de código Vader para debugging
nombre = "Juan"
edad = 25
contador = 0

mientras contador menor que 5 entonces
    mostrar "Contador: " + contador
    contador = contador + 1
fin mientras

si edad mayor que 18 entonces
    mostrar nombre + " es mayor de edad"
sino
    mostrar nombre + " es menor de edad"
fin si

resultado = edad * 2
mostrar "Resultado final: " + resultado
"""
    
    print("🧪 PROBANDO VADER DEBUGGER")
    print("=" * 50)
    
    # Iniciar sesión de debugging
    session_id = debugger.start_debug_session(vader_code, 'python')
    
    # Agregar algunos breakpoints
    debugger.add_breakpoint(6)  # En el bucle mientras
    debugger.add_breakpoint(11, "edad > 20")  # Breakpoint condicional
    
    # Detectar errores comunes
    errors = debugger.detect_common_errors(vader_code)
    if errors:
        print(f"\n⚠️ ERRORES DETECTADOS: {len(errors)}")
        for error in errors:
            print(f"  Línea {error['line_number']}: {error['message']}")
    
    # Iniciar profiling
    debugger.start_profiling()
    
    # Ejecutar código paso a paso
    print(f"\n🚀 Ejecutando código paso a paso...")
    execution_steps = debugger.step_through_code(vader_code)
    
    # Detener profiling
    debugger.stop_profiling()
    
    # Analizar rendimiento
    performance = debugger.analyze_performance(execution_steps)
    print(f"\n📊 ANÁLISIS DE RENDIMIENTO:")
    print(f"  Tiempo total: {performance.get('total_execution_time', 0):.4f}s")
    print(f"  Pasos totales: {performance.get('total_steps', 0)}")
    print(f"  Pasos exitosos: {performance.get('successful_steps', 0)}")
    print(f"  Errores: {performance.get('error_steps', 0)}")
    
    # Detener sesión
    debugger.stop_debug_session()
    
    print("\n🎉 VADER DEBUGGER FUNCIONAL")
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
