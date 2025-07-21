#!/usr/bin/env python3
"""
VADER NATIVE INTERPRETER
El primer intérprete nativo para el Lenguaje Supremo Universal

Este módulo permite ejecutar archivos .vdr directamente sin transpilación,
convirtiendo a Vader en un lenguaje de primera clase.

Autor: Vader Team
Versión: 1.0.0 - Native Runtime
"""

import sys
import os
import re
import json
from typing import Dict, Any, List, Optional
from pathlib import Path

class VaderNativeRuntime:
    """Runtime nativo de Vader - Ejecuta .vdr directamente"""
    
    def __init__(self):
        self.variables = {}
        self.functions = {}
        self.output_buffer = []
        self.debug_mode = False
        
    def execute_file(self, file_path: str) -> bool:
        """Ejecuta un archivo .vdr directamente"""
        try:
            if not os.path.exists(file_path):
                self.error(f"Archivo no encontrado: {file_path}")
                return False
                
            with open(file_path, 'r', encoding='utf-8') as f:
                code = f.read()
                
            return self.execute_code(code, file_path)
            
        except Exception as e:
            self.error(f"Error ejecutando {file_path}: {str(e)}")
            return False
    
    def execute_code(self, code: str, filename: str = "<string>") -> bool:
        """Ejecuta código Vader directamente"""
        try:
            lines = code.split('\n')
            return self.execute_lines(lines, filename)
            
        except Exception as e:
            self.error(f"Error en {filename}: {str(e)}")
            return False
    
    def execute_lines(self, lines: List[str], filename: str) -> bool:
        """Ejecuta líneas de código Vader"""
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            # Saltar líneas vacías y comentarios
            if not line or line.startswith('#'):
                i += 1
                continue
                
            # Ejecutar línea
            try:
                next_i = self.execute_line(line, lines, i, filename)
                i = next_i if next_i is not None else i + 1
                
            except Exception as e:
                self.error(f"Error en línea {i+1} de {filename}: {str(e)}")
                self.error(f"Línea: {line}")
                return False
                
        return True
    
    def execute_line(self, line: str, lines: List[str], current_line: int, filename: str) -> Optional[int]:
        """Ejecuta una línea individual de código Vader"""
        
        # MOSTRAR - Imprimir en pantalla
        if line.startswith('mostrar '):
            content = line[8:].strip()
            value = self.evaluate_expression(content)
            print(value)
            self.output_buffer.append(str(value))
            return None
            
        # VARIABLE ASSIGNMENT - Asignación de variables
        if '=' in line and not any(op in line for op in ['==', '!=', '>=', '<=']):
            parts = line.split('=', 1)
            var_name = parts[0].strip()
            var_value = parts[1].strip()
            
            # Evaluar el valor
            self.variables[var_name] = self.evaluate_expression(var_value)
            return None
            
        # PREGUNTAR - Input del usuario
        if line.startswith('preguntar '):
            prompt_match = re.match(r'preguntar "([^"]*)"(?:\s+guardar\s+(?:la\s+)?respuesta\s+en\s+(\w+))?', line)
            if prompt_match:
                prompt = prompt_match.group(1)
                var_name = prompt_match.group(2)
                
                user_input = input(prompt + " ")
                if var_name:
                    self.variables[var_name] = user_input
                return None
                
        # LEER - Input simple
        if line.startswith('leer '):
            var_name = line[5:].strip()
            user_input = input()
            self.variables[var_name] = user_input
            return None
            
        # CONVERTIR - Conversiones de tipo
        if line.startswith('convertir '):
            convert_match = re.match(r'convertir\s+(\w+)\s+a\s+(numero|texto)', line)
            if convert_match:
                var_name = convert_match.group(1)
                target_type = convert_match.group(2)
                
                if var_name in self.variables:
                    if target_type == 'numero':
                        try:
                            self.variables[var_name] = float(self.variables[var_name])
                            if self.variables[var_name].is_integer():
                                self.variables[var_name] = int(self.variables[var_name])
                        except ValueError:
                            self.error(f"No se puede convertir '{self.variables[var_name]}' a número")
                    elif target_type == 'texto':
                        self.variables[var_name] = str(self.variables[var_name])
                return None
                
        # SI - Condicionales
        if line.startswith('si '):
            return self.execute_conditional(line, lines, current_line, filename)
            
        # FUNCION - Definición de funciones
        if line.startswith('funcion '):
            return self.execute_function_definition(line, lines, current_line, filename)
            
        # REPETIR - Bucles
        if line.startswith('repetir '):
            return self.execute_loop(line, lines, current_line, filename)
            
        # Llamada a función
        if line in self.functions:
            return self.call_function(line)
            
        # Línea no reconocida
        if self.debug_mode:
            print(f"[DEBUG] Línea no reconocida: {line}")
            
        return None
    
    def execute_conditional(self, line: str, lines: List[str], current_line: int, filename: str) -> int:
        """Ejecuta condicionales (si/sino/fin si)"""
        condition = line[3:].strip()
        condition_result = self.evaluate_condition(condition)
        
        i = current_line + 1
        executed_block = False
        
        while i < len(lines):
            current = lines[i].strip()
            
            if current == 'fin si':
                return i + 1
                
            elif current == 'sino' or current.startswith('sino si '):
                if executed_block:
                    # Saltar este bloque
                    i = self.skip_to_next_else_or_end(lines, i)
                    continue
                elif current == 'sino':
                    # Ejecutar bloque else
                    i += 1
                    while i < len(lines) and lines[i].strip() != 'fin si':
                        next_i = self.execute_line(lines[i].strip(), lines, i, filename)
                        i = next_i if next_i is not None else i + 1
                    executed_block = True
                else:
                    # sino si - evaluar nueva condición
                    new_condition = current[8:].strip()
                    if self.evaluate_condition(new_condition):
                        condition_result = True
                    else:
                        i = self.skip_to_next_else_or_end(lines, i)
                        continue
                        
            elif condition_result and not executed_block:
                # Ejecutar bloque si
                next_i = self.execute_line(current, lines, i, filename)
                i = next_i if next_i is not None else i + 1
                executed_block = True
            else:
                i += 1
                
        return i
    
    def execute_function_definition(self, line: str, lines: List[str], current_line: int, filename: str) -> int:
        """Define una función"""
        func_name = line[8:].strip()
        func_lines = []
        
        i = current_line + 1
        while i < len(lines):
            current = lines[i].strip()
            if current == 'fin funcion':
                break
            func_lines.append(lines[i])
            i += 1
            
        self.functions[func_name] = func_lines
        return i + 1
    
    def execute_loop(self, line: str, lines: List[str], current_line: int, filename: str) -> int:
        """Ejecuta bucles"""
        # repetir X veces
        times_match = re.match(r'repetir\s+(\d+)\s+veces', line)
        if times_match:
            times = int(times_match.group(1))
            loop_lines = []
            
            i = current_line + 1
            while i < len(lines):
                current = lines[i].strip()
                if current == 'fin repetir':
                    break
                loop_lines.append(lines[i])
                i += 1
                
            # Ejecutar el bucle
            for _ in range(times):
                self.execute_lines(loop_lines, filename)
                
            return i + 1
            
        return current_line + 1
    
    def call_function(self, func_name: str) -> None:
        """Llama a una función definida"""
        if func_name in self.functions:
            self.execute_lines(self.functions[func_name], f"<function:{func_name}>")
    
    def evaluate_expression(self, expr: str) -> Any:
        """Evalúa una expresión Vader"""
        expr = expr.strip()
        
        # String literal
        if expr.startswith('"') and expr.endswith('"'):
            return expr[1:-1]
            
        # Número
        try:
            if '.' in expr:
                return float(expr)
            return int(expr)
        except ValueError:
            pass
            
        # Variable
        if expr in self.variables:
            return self.variables[expr]
            
        # Operaciones matemáticas simples
        if '+' in expr:
            parts = expr.split('+')
            if len(parts) == 2:
                left = self.evaluate_expression(parts[0].strip())
                right = self.evaluate_expression(parts[1].strip())
                # Concatenación de strings o suma matemática
                if isinstance(left, str) or isinstance(right, str):
                    return str(left) + str(right)
                return left + right
                
        if '-' in expr and not expr.startswith('-'):
            parts = expr.split('-')
            if len(parts) == 2:
                left = self.evaluate_expression(parts[0].strip())
                right = self.evaluate_expression(parts[1].strip())
                return left - right
                
        if '*' in expr:
            parts = expr.split('*')
            if len(parts) == 2:
                left = self.evaluate_expression(parts[0].strip())
                right = self.evaluate_expression(parts[1].strip())
                return left * right
                
        if '/' in expr:
            parts = expr.split('/')
            if len(parts) == 2:
                left = self.evaluate_expression(parts[0].strip())
                right = self.evaluate_expression(parts[1].strip())
                return left / right
                
        return expr
    
    def evaluate_condition(self, condition: str) -> bool:
        """Evalúa una condición booleana"""
        condition = condition.strip()
        
        # Operadores de comparación
        if ' es igual a ' in condition:
            parts = condition.split(' es igual a ')
            left = self.evaluate_expression(parts[0].strip())
            right = self.evaluate_expression(parts[1].strip())
            return left == right
            
        if ' es mayor que ' in condition:
            parts = condition.split(' es mayor que ')
            left = self.evaluate_expression(parts[0].strip())
            right = self.evaluate_expression(parts[1].strip())
            return left > right
            
        if ' es menor que ' in condition:
            parts = condition.split(' es menor que ')
            left = self.evaluate_expression(parts[0].strip())
            right = self.evaluate_expression(parts[1].strip())
            return left < right
            
        # Condición simple (variable existe y es verdadera)
        value = self.evaluate_expression(condition)
        return bool(value)
    
    def skip_to_next_else_or_end(self, lines: List[str], start: int) -> int:
        """Salta hasta el próximo 'sino' o 'fin si'"""
        i = start + 1
        while i < len(lines):
            current = lines[i].strip()
            if current in ['sino', 'fin si'] or current.startswith('sino si '):
                return i
            i += 1
        return i
    
    def error(self, message: str):
        """Muestra un error"""
        print(f"❌ Error Vader: {message}", file=sys.stderr)
    
    def info(self, message: str):
        """Muestra información"""
        if self.debug_mode:
            print(f"ℹ️  {message}")

def main():
    """Función principal del intérprete nativo"""
    if len(sys.argv) < 2:
        print("❌ Uso: python3 vader_interpreter.py archivo.vdr [--debug]")
        sys.exit(1)
        
    file_path = sys.argv[1]
    debug_mode = '--debug' in sys.argv
    
    # Crear runtime
    runtime = VaderNativeRuntime()
    runtime.debug_mode = debug_mode
    
    if debug_mode:
        print(f"🚀 Iniciando Vader Native Runtime")
        print(f"📁 Ejecutando: {file_path}")
        print("=" * 50)
    
    # Ejecutar archivo
    success = runtime.execute_file(file_path)
    
    if debug_mode:
        print("=" * 50)
        if success:
            print("✅ Ejecución completada exitosamente")
        else:
            print("❌ Ejecución terminada con errores")
            
        print(f"📊 Variables definidas: {len(runtime.variables)}")
        print(f"🔧 Funciones definidas: {len(runtime.functions)}")
        
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
