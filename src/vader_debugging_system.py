#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VADER 7.0 - SISTEMA DE DEBUGGING
================================
Sistema completo de depuración para Vader con breakpoints y análisis

Características:
- Breakpoints dinámicos y condicionales
- Modo paso a paso (step into, step over, step out)
- Inspección de variables y stack trace
- Watchpoints para monitoreo de variables
- Profiling de rendimiento
- Logging avanzado con niveles
- Análisis de memoria y recursos
- Debugging remoto
- Interfaz de debugging interactiva

Autor: Vader Team
Versión: 7.0.0 "Universal"
Fecha: 2025
"""

import sys
import traceback
import inspect
import threading
import time
import gc
import psutil
import os
from typing import Dict, List, Any, Optional, Callable, Union
from dataclasses import dataclass, field
from enum import Enum
import json
import logging
from datetime import datetime
import linecache

class DebugLevel(Enum):
    """Niveles de debugging"""
    TRACE = "trace"
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

class BreakpointType(Enum):
    """Tipos de breakpoints"""
    LINE = "line"           # Breakpoint en línea específica
    FUNCTION = "function"   # Breakpoint en función
    EXCEPTION = "exception" # Breakpoint en excepción
    CONDITIONAL = "conditional"  # Breakpoint condicional
    WATCHPOINT = "watchpoint"    # Watchpoint en variable

class StepMode(Enum):
    """Modos de ejecución paso a paso"""
    STEP_INTO = "step_into"     # Entrar en funciones
    STEP_OVER = "step_over"     # Saltar funciones
    STEP_OUT = "step_out"       # Salir de función actual
    CONTINUE = "continue"       # Continuar ejecución

@dataclass
class VaderBreakpoint:
    """Breakpoint de Vader"""
    id: str
    breakpoint_type: BreakpointType
    file_path: str
    line_number: Optional[int] = None
    function_name: Optional[str] = None
    condition: Optional[str] = None
    variable_name: Optional[str] = None
    hit_count: int = 0
    enabled: bool = True
    temporary: bool = False
    
    def should_break(self, frame, event, arg) -> bool:
        """Determina si debe activarse el breakpoint"""
        if not self.enabled:
            return False
        
        # Verificar archivo y línea
        if self.file_path and frame.f_code.co_filename != self.file_path:
            return False
        
        if self.line_number and frame.f_lineno != self.line_number:
            return False
        
        # Verificar función
        if self.function_name and frame.f_code.co_name != self.function_name:
            return False
        
        # Verificar condición
        if self.condition:
            try:
                if not eval(self.condition, frame.f_globals, frame.f_locals):
                    return False
            except:
                return False
        
        self.hit_count += 1
        return True

@dataclass
class DebugFrame:
    """Frame de debugging"""
    frame_id: int
    function_name: str
    file_path: str
    line_number: int
    local_variables: Dict[str, Any]
    arguments: Dict[str, Any]
    source_line: str

@dataclass
class DebugSession:
    """Sesión de debugging"""
    session_id: str
    start_time: datetime
    breakpoints: Dict[str, VaderBreakpoint] = field(default_factory=dict)
    watchpoints: Dict[str, Any] = field(default_factory=dict)
    call_stack: List[DebugFrame] = field(default_factory=list)
    step_mode: StepMode = StepMode.CONTINUE
    current_frame: Optional[DebugFrame] = None
    is_active: bool = True

class VaderDebugger:
    """Debugger principal de Vader"""
    
    def __init__(self):
        self.sessions: Dict[str, DebugSession] = {}
        self.current_session: Optional[DebugSession] = None
        self.original_trace_function = None
        self.is_debugging = False
        self.step_depth = 0
        self.performance_data = {}
        
        # Configurar logging
        self.logger = self._setup_logging()
        
        # Patrones de comandos de debugging
        self.debug_patterns = {
            'breakpoint': r'breakpoint\s+(.+)',
            'step_into': r'paso\s+dentro|step\s+into',
            'step_over': r'paso\s+sobre|step\s+over',
            'step_out': r'paso\s+fuera|step\s+out',
            'continue': r'continuar|continue',
            'inspect': r'inspeccionar\s+(.+)',
            'watch': r'observar\s+(.+)',
            'stack': r'pila|stack',
            'variables': r'variables|vars',
            'memory': r'memoria|memory',
            'performance': r'rendimiento|performance',
        }
    
    def _setup_logging(self) -> logging.Logger:
        """Configura el sistema de logging"""
        logger = logging.getLogger('vader_debugger')
        logger.setLevel(logging.DEBUG)
        
        # Handler para archivo
        file_handler = logging.FileHandler('vader_debug.log')
        file_handler.setLevel(logging.DEBUG)
        
        # Handler para consola
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Formato
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        return logger
    
    def start_debug_session(self, session_id: str = None) -> DebugSession:
        """Inicia una sesión de debugging"""
        if not session_id:
            session_id = f"debug_{int(time.time())}"
        
        session = DebugSession(
            session_id=session_id,
            start_time=datetime.now()
        )
        
        self.sessions[session_id] = session
        self.current_session = session
        
        # Instalar trace function
        self.original_trace_function = sys.gettrace()
        sys.settrace(self._trace_function)
        self.is_debugging = True
        
        self.logger.info(f"Sesión de debugging iniciada: {session_id}")
        return session
    
    def stop_debug_session(self, session_id: str = None):
        """Detiene una sesión de debugging"""
        if session_id:
            session = self.sessions.get(session_id)
        else:
            session = self.current_session
        
        if session:
            session.is_active = False
            
            # Restaurar trace function original
            sys.settrace(self.original_trace_function)
            self.is_debugging = False
            
            self.logger.info(f"Sesión de debugging terminada: {session.session_id}")
    
    def add_breakpoint(self, file_path: str, line_number: int, 
                      condition: str = None, temporary: bool = False) -> str:
        """Añade un breakpoint"""
        if not self.current_session:
            raise RuntimeError("No hay sesión de debugging activa")
        
        breakpoint_id = f"bp_{len(self.current_session.breakpoints)}"
        
        breakpoint = VaderBreakpoint(
            id=breakpoint_id,
            breakpoint_type=BreakpointType.CONDITIONAL if condition else BreakpointType.LINE,
            file_path=file_path,
            line_number=line_number,
            condition=condition,
            temporary=temporary
        )
        
        self.current_session.breakpoints[breakpoint_id] = breakpoint
        self.logger.info(f"Breakpoint añadido: {file_path}:{line_number}")
        
        return breakpoint_id
    
    def add_function_breakpoint(self, function_name: str, condition: str = None) -> str:
        """Añade un breakpoint en función"""
        if not self.current_session:
            raise RuntimeError("No hay sesión de debugging activa")
        
        breakpoint_id = f"fbp_{len(self.current_session.breakpoints)}"
        
        breakpoint = VaderBreakpoint(
            id=breakpoint_id,
            breakpoint_type=BreakpointType.FUNCTION,
            file_path="",
            function_name=function_name,
            condition=condition
        )
        
        self.current_session.breakpoints[breakpoint_id] = breakpoint
        self.logger.info(f"Function breakpoint añadido: {function_name}")
        
        return breakpoint_id
    
    def add_watchpoint(self, variable_name: str, condition: str = None) -> str:
        """Añade un watchpoint para una variable"""
        if not self.current_session:
            raise RuntimeError("No hay sesión de debugging activa")
        
        watchpoint_id = f"wp_{len(self.current_session.watchpoints)}"
        
        self.current_session.watchpoints[watchpoint_id] = {
            'variable': variable_name,
            'condition': condition,
            'last_value': None,
            'hit_count': 0
        }
        
        self.logger.info(f"Watchpoint añadido: {variable_name}")
        return watchpoint_id
    
    def remove_breakpoint(self, breakpoint_id: str):
        """Elimina un breakpoint"""
        if self.current_session and breakpoint_id in self.current_session.breakpoints:
            del self.current_session.breakpoints[breakpoint_id]
            self.logger.info(f"Breakpoint eliminado: {breakpoint_id}")
    
    def set_step_mode(self, mode: StepMode):
        """Establece el modo de ejecución paso a paso"""
        if self.current_session:
            self.current_session.step_mode = mode
            self.logger.debug(f"Modo de paso establecido: {mode.value}")
    
    def _trace_function(self, frame, event, arg):
        """Función de trazado principal"""
        if not self.current_session or not self.current_session.is_active:
            return
        
        # Verificar breakpoints
        for breakpoint in self.current_session.breakpoints.values():
            if breakpoint.should_break(frame, event, arg):
                self._handle_breakpoint(frame, breakpoint)
                break
        
        # Verificar watchpoints
        self._check_watchpoints(frame)
        
        # Manejar modo paso a paso
        if self.current_session.step_mode != StepMode.CONTINUE:
            self._handle_step_mode(frame, event)
        
        return self._trace_function
    
    def _handle_breakpoint(self, frame, breakpoint: VaderBreakpoint):
        """Maneja la activación de un breakpoint"""
        self.logger.info(f"Breakpoint activado: {breakpoint.id}")
        
        # Crear frame de debugging
        debug_frame = self._create_debug_frame(frame)
        self.current_session.current_frame = debug_frame
        
        # Mostrar información del breakpoint
        self._show_breakpoint_info(debug_frame, breakpoint)
        
        # Entrar en modo interactivo
        self._enter_interactive_mode()
        
        # Eliminar breakpoint temporal
        if breakpoint.temporary:
            self.remove_breakpoint(breakpoint.id)
    
    def _check_watchpoints(self, frame):
        """Verifica watchpoints"""
        for wp_id, watchpoint in self.current_session.watchpoints.items():
            var_name = watchpoint['variable']
            
            # Buscar variable en locals o globals
            current_value = None
            if var_name in frame.f_locals:
                current_value = frame.f_locals[var_name]
            elif var_name in frame.f_globals:
                current_value = frame.f_globals[var_name]
            
            # Verificar cambio
            if current_value != watchpoint['last_value']:
                watchpoint['last_value'] = current_value
                watchpoint['hit_count'] += 1
                
                self.logger.info(f"Watchpoint activado: {var_name} = {current_value}")
                
                # Verificar condición si existe
                if watchpoint['condition']:
                    try:
                        if not eval(watchpoint['condition'], frame.f_globals, frame.f_locals):
                            continue
                    except:
                        continue
                
                # Crear frame y mostrar información
                debug_frame = self._create_debug_frame(frame)
                self._show_watchpoint_info(debug_frame, var_name, current_value)
    
    def _handle_step_mode(self, frame, event):
        """Maneja el modo paso a paso"""
        if event == 'call':
            self.step_depth += 1
        elif event == 'return':
            self.step_depth -= 1
        
        should_break = False
        
        if self.current_session.step_mode == StepMode.STEP_INTO:
            should_break = True
        elif self.current_session.step_mode == StepMode.STEP_OVER:
            should_break = self.step_depth <= 0
        elif self.current_session.step_mode == StepMode.STEP_OUT:
            should_break = self.step_depth < 0
        
        if should_break:
            debug_frame = self._create_debug_frame(frame)
            self.current_session.current_frame = debug_frame
            self._show_step_info(debug_frame)
            self._enter_interactive_mode()
    
    def _create_debug_frame(self, frame) -> DebugFrame:
        """Crea un frame de debugging"""
        # Obtener variables locales
        local_vars = {}
        for name, value in frame.f_locals.items():
            try:
                # Serializar valor para mostrar
                if isinstance(value, (str, int, float, bool, type(None))):
                    local_vars[name] = value
                else:
                    local_vars[name] = f"<{type(value).__name__}>"
            except:
                local_vars[name] = "<no serializable>"
        
        # Obtener argumentos de función
        arg_info = inspect.getargvalues(frame)
        arguments = {arg: frame.f_locals.get(arg) for arg in arg_info.args}
        
        # Obtener línea de código
        source_line = linecache.getline(frame.f_code.co_filename, frame.f_lineno).strip()
        
        return DebugFrame(
            frame_id=id(frame),
            function_name=frame.f_code.co_name,
            file_path=frame.f_code.co_filename,
            line_number=frame.f_lineno,
            local_variables=local_vars,
            arguments=arguments,
            source_line=source_line
        )
    
    def _show_breakpoint_info(self, debug_frame: DebugFrame, breakpoint: VaderBreakpoint):
        """Muestra información del breakpoint"""
        print(f"\n🔴 BREAKPOINT ACTIVADO: {breakpoint.id}")
        print(f"📁 Archivo: {debug_frame.file_path}")
        print(f"📍 Línea: {debug_frame.line_number}")
        print(f"🔧 Función: {debug_frame.function_name}")
        print(f"📝 Código: {debug_frame.source_line}")
        print(f"🎯 Hits: {breakpoint.hit_count}")
        
        if breakpoint.condition:
            print(f"❓ Condición: {breakpoint.condition}")
    
    def _show_watchpoint_info(self, debug_frame: DebugFrame, var_name: str, value: Any):
        """Muestra información del watchpoint"""
        print(f"\n👁️ WATCHPOINT ACTIVADO: {var_name}")
        print(f"📁 Archivo: {debug_frame.file_path}")
        print(f"📍 Línea: {debug_frame.line_number}")
        print(f"🔧 Función: {debug_frame.function_name}")
        print(f"💾 Nuevo valor: {value}")
    
    def _show_step_info(self, debug_frame: DebugFrame):
        """Muestra información del paso"""
        print(f"\n👣 PASO: {self.current_session.step_mode.value}")
        print(f"📁 Archivo: {debug_frame.file_path}")
        print(f"📍 Línea: {debug_frame.line_number}")
        print(f"🔧 Función: {debug_frame.function_name}")
        print(f"📝 Código: {debug_frame.source_line}")
    
    def _enter_interactive_mode(self):
        """Entra en modo interactivo de debugging"""
        print("\n🐛 MODO DEBUGGING INTERACTIVO")
        print("Comandos disponibles:")
        print("  c, continuar - Continuar ejecución")
        print("  s, paso - Paso dentro (step into)")
        print("  n, siguiente - Paso sobre (step over)")
        print("  f, fuera - Paso fuera (step out)")
        print("  v, variables - Mostrar variables")
        print("  p, pila - Mostrar call stack")
        print("  m, memoria - Información de memoria")
        print("  q, salir - Salir del debugger")
        
        while True:
            try:
                command = input("(vader-debug) ").strip().lower()
                
                if command in ['c', 'continuar']:
                    self.set_step_mode(StepMode.CONTINUE)
                    break
                elif command in ['s', 'paso']:
                    self.set_step_mode(StepMode.STEP_INTO)
                    break
                elif command in ['n', 'siguiente']:
                    self.set_step_mode(StepMode.STEP_OVER)
                    break
                elif command in ['f', 'fuera']:
                    self.set_step_mode(StepMode.STEP_OUT)
                    break
                elif command in ['v', 'variables']:
                    self._show_variables()
                elif command in ['p', 'pila']:
                    self._show_call_stack()
                elif command in ['m', 'memoria']:
                    self._show_memory_info()
                elif command in ['q', 'salir']:
                    self.stop_debug_session()
                    break
                else:
                    print("Comando no reconocido. Intenta 'c', 's', 'n', 'f', 'v', 'p', 'm', o 'q'")
            
            except (EOFError, KeyboardInterrupt):
                print("\nSaliendo del debugger...")
                self.stop_debug_session()
                break
    
    def _show_variables(self):
        """Muestra variables del frame actual"""
        if not self.current_session.current_frame:
            print("No hay frame actual")
            return
        
        frame = self.current_session.current_frame
        print(f"\n📊 VARIABLES LOCALES en {frame.function_name}:")
        
        for name, value in frame.local_variables.items():
            print(f"  {name} = {value}")
        
        if frame.arguments:
            print(f"\n📥 ARGUMENTOS:")
            for name, value in frame.arguments.items():
                print(f"  {name} = {value}")
    
    def _show_call_stack(self):
        """Muestra el call stack"""
        print(f"\n📚 CALL STACK:")
        
        # Obtener stack actual
        stack = inspect.stack()
        for i, frame_info in enumerate(stack[1:]):  # Saltar frame actual
            print(f"  #{i}: {frame_info.function} en {frame_info.filename}:{frame_info.lineno}")
    
    def _show_memory_info(self):
        """Muestra información de memoria"""
        try:
            process = psutil.Process()
            memory_info = process.memory_info()
            
            print(f"\n💾 INFORMACIÓN DE MEMORIA:")
            print(f"  RSS: {memory_info.rss / 1024 / 1024:.2f} MB")
            print(f"  VMS: {memory_info.vms / 1024 / 1024:.2f} MB")
            print(f"  Objetos Python: {len(gc.get_objects())}")
            print(f"  Colecciones GC: {gc.get_count()}")
            
        except ImportError:
            print("psutil no disponible para información de memoria")
    
    def profile_function(self, func: Callable) -> Callable:
        """Decorador para profiling de funciones"""
        def wrapper(*args, **kwargs):
            start_time = time.time()
            start_memory = self._get_memory_usage()
            
            try:
                result = func(*args, **kwargs)
                success = True
                error = None
            except Exception as e:
                result = None
                success = False
                error = str(e)
            
            end_time = time.time()
            end_memory = self._get_memory_usage()
            
            # Guardar datos de performance
            func_name = func.__name__
            if func_name not in self.performance_data:
                self.performance_data[func_name] = []
            
            self.performance_data[func_name].append({
                'execution_time': end_time - start_time,
                'memory_delta': end_memory - start_memory,
                'success': success,
                'error': error,
                'timestamp': datetime.now().isoformat()
            })
            
            self.logger.debug(f"Profiling {func_name}: {end_time - start_time:.4f}s")
            
            if not success:
                raise Exception(error)
            
            return result
        
        return wrapper
    
    def _get_memory_usage(self) -> float:
        """Obtiene uso de memoria actual"""
        try:
            process = psutil.Process()
            return process.memory_info().rss / 1024 / 1024  # MB
        except:
            return 0.0
    
    def get_performance_report(self) -> Dict[str, Any]:
        """Genera reporte de performance"""
        report = {}
        
        for func_name, data in self.performance_data.items():
            if not data:
                continue
            
            execution_times = [d['execution_time'] for d in data]
            memory_deltas = [d['memory_delta'] for d in data]
            success_rate = sum(1 for d in data if d['success']) / len(data)
            
            report[func_name] = {
                'calls': len(data),
                'avg_time': sum(execution_times) / len(execution_times),
                'max_time': max(execution_times),
                'min_time': min(execution_times),
                'avg_memory': sum(memory_deltas) / len(memory_deltas),
                'success_rate': success_rate,
                'total_time': sum(execution_times)
            }
        
        return report
    
    def export_debug_session(self, session_id: str = None) -> Dict[str, Any]:
        """Exporta sesión de debugging"""
        session = self.sessions.get(session_id) if session_id else self.current_session
        if not session:
            return {}
        
        return {
            'session_id': session.session_id,
            'start_time': session.start_time.isoformat(),
            'breakpoints': {
                bp_id: {
                    'type': bp.breakpoint_type.value,
                    'file': bp.file_path,
                    'line': bp.line_number,
                    'function': bp.function_name,
                    'condition': bp.condition,
                    'hits': bp.hit_count
                }
                for bp_id, bp in session.breakpoints.items()
            },
            'watchpoints': session.watchpoints,
            'performance': self.get_performance_report()
        }

def debug_decorator(debugger: VaderDebugger):
    """Decorador para debugging automático"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            # Añadir breakpoint temporal en la función
            breakpoint_id = debugger.add_function_breakpoint(func.__name__, temporary=True)
            
            try:
                return func(*args, **kwargs)
            finally:
                # Limpiar breakpoint temporal
                if breakpoint_id in debugger.current_session.breakpoints:
                    debugger.remove_breakpoint(breakpoint_id)
        
        return wrapper
    return decorator

def main():
    """Función principal para testing"""
    print("🐛 VADER DEBUGGING SYSTEM - Pruebas de funcionalidad:")
    print("=" * 70)
    
    # Crear debugger
    debugger = VaderDebugger()
    
    # Iniciar sesión de debugging
    session = debugger.start_debug_session("test_session")
    print(f"✅ Sesión de debugging iniciada: {session.session_id}")
    
    # Función de prueba
    def test_function(x, y):
        """Función de prueba para debugging"""
        a = x + y
        b = a * 2
        c = b - 1
        return c
    
    # Función con error para testing
    def error_function():
        """Función que genera error"""
        result = 10 / 0
        return result
    
    # Añadir breakpoints
    # Nota: En un entorno real, estos serían archivos reales
    bp1 = debugger.add_breakpoint(__file__, 50, condition="x > 5")
    bp2 = debugger.add_function_breakpoint("test_function")
    
    print(f"📍 Breakpoints añadidos: {bp1}, {bp2}")
    
    # Añadir watchpoint
    wp1 = debugger.add_watchpoint("a", condition="a > 10")
    print(f"👁️ Watchpoint añadido: {wp1}")
    
    # Decorador de profiling
    @debugger.profile_function
    def profiled_function(n):
        """Función con profiling"""
        total = 0
        for i in range(n):
            total += i * i
        return total
    
    print("\n🔧 Ejecutando función con profiling...")
    result = profiled_function(1000)
    print(f"   Resultado: {result}")
    
    # Ejecutar múltiples veces para estadísticas
    for i in range(5):
        profiled_function(100 * (i + 1))
    
    # Generar reporte de performance
    print("\n📊 Reporte de performance:")
    performance_report = debugger.get_performance_report()
    for func_name, stats in performance_report.items():
        print(f"   {func_name}:")
        print(f"     Llamadas: {stats['calls']}")
        print(f"     Tiempo promedio: {stats['avg_time']:.4f}s")
        print(f"     Tiempo total: {stats['total_time']:.4f}s")
        print(f"     Memoria promedio: {stats['avg_memory']:.2f}MB")
        print(f"     Tasa de éxito: {stats['success_rate']:.2%}")
    
    # Mostrar información de memoria
    debugger._show_memory_info()
    
    # Exportar sesión
    print("\n💾 Exportando sesión de debugging...")
    session_data = debugger.export_debug_session()
    print(f"   Breakpoints: {len(session_data['breakpoints'])}")
    print(f"   Watchpoints: {len(session_data['watchpoints'])}")
    print(f"   Funciones perfiladas: {len(session_data['performance'])}")
    
    # Detener sesión
    debugger.stop_debug_session()
    print("🛑 Sesión de debugging terminada")
    
    print("\n" + "=" * 70)
    print("✅ Sistema de debugging Vader implementado")
    print("🚀 Características disponibles:")
    print("  - Breakpoints dinámicos y condicionales")
    print("  - Modo paso a paso (step into, over, out)")
    print("  - Inspección de variables y call stack")
    print("  - Watchpoints para monitoreo")
    print("  - Profiling de rendimiento")
    print("  - Análisis de memoria")
    print("  - Logging avanzado")
    print("  - Interfaz interactiva")
    print("  - Exportación de sesiones")
    print("  - Decoradores de debugging")

if __name__ == "__main__":
    main()
