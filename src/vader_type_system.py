#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VADER 7.0 - SISTEMA DE TIPADO FUERTE/OPCIONAL
=============================================
Sistema de tipos avanzado para Vader con validación estática y runtime

Características:
- Tipado estático opcional
- Inferencia de tipos
- Tipos personalizados
- Validación en tiempo de compilación
- Soporte para tipos union y opcionales

Autor: Vader Team
Versión: 7.0.0 "Universal"
Fecha: 2025
"""

import re
import ast
from typing import Dict, List, Any, Optional, Union, Set, Tuple
from dataclasses import dataclass
from enum import Enum

class VaderType(Enum):
    """Tipos básicos de Vader"""
    ENTERO = "entero"
    DECIMAL = "decimal"
    TEXTO = "texto"
    BOOLEANO = "booleano"
    LISTA = "lista"
    DICCIONARIO = "diccionario"
    FUNCION = "funcion"
    NODO = "nodo"
    NODOS = "nodos"
    NUMERO = "numero"
    CUALQUIERA = "cualquiera"
    VACIO = "vacio"

@dataclass
class TypeAnnotation:
    """Anotación de tipo para variables y funciones"""
    base_type: VaderType
    is_optional: bool = False
    is_array: bool = False
    union_types: List[VaderType] = None
    custom_type: str = None
    constraints: Dict[str, Any] = None

@dataclass
class FunctionSignature:
    """Firma de función con tipos"""
    name: str
    parameters: Dict[str, TypeAnnotation]
    return_type: TypeAnnotation
    is_async: bool = False

@dataclass
class CustomType:
    """Tipo personalizado definido por el usuario"""
    name: str
    fields: Dict[str, TypeAnnotation]
    methods: Dict[str, FunctionSignature]
    parent_type: str = None

class VaderTypeChecker:
    """Verificador de tipos para Vader"""
    
    def __init__(self):
        self.variables: Dict[str, TypeAnnotation] = {}
        self.functions: Dict[str, FunctionSignature] = {}
        self.custom_types: Dict[str, CustomType] = {}
        self.errors: List[str] = []
        self.warnings: List[str] = []
        
        # Patrones de reconocimiento de tipos
        self.type_patterns = {
            'typed_variable': r'(\w+)\s*:\s*([^=]+?)(?:\s*=|$)',
            'union_type': r'([^|]+(?:\s*\|\s*[^|]+)+)',
            'optional_type': r'(\w+)\?',
            'array_type': r'lista\[(\w+)\]',
            'function_type': r'funcion\s*\(([^)]*)\)\s*->\s*(\w+)',
            'custom_type_def': r'tipo\s+(\w+)\s*\{([^}]+)\}',
        }
    
    def parse_type_annotation(self, type_str: str) -> TypeAnnotation:
        """Parsea una anotación de tipo desde string"""
        type_str = type_str.strip()
        
        # Tipo opcional (nombre?)
        if type_str.endswith('?'):
            base_type_str = type_str[:-1].strip()
            return TypeAnnotation(
                base_type=self._parse_base_type(base_type_str),
                is_optional=True
            )
        
        # Tipo union (tipo1 | tipo2 | tipo3)
        if '|' in type_str:
            union_parts = [part.strip() for part in type_str.split('|')]
            union_types = [self._parse_base_type(part) for part in union_parts]
            return TypeAnnotation(
                base_type=union_types[0],
                union_types=union_types
            )
        
        # Tipo array (lista[tipo])
        array_match = re.match(r'lista\[(\w+)\]', type_str)
        if array_match:
            element_type = self._parse_base_type(array_match.group(1))
            return TypeAnnotation(
                base_type=VaderType.LISTA,
                is_array=True,
                constraints={'element_type': element_type}
            )
        
        # Tipo función
        func_match = re.match(r'funcion\s*\(([^)]*)\)\s*->\s*(\w+)', type_str)
        if func_match:
            params_str = func_match.group(1)
            return_type_str = func_match.group(2)
            return TypeAnnotation(
                base_type=VaderType.FUNCION,
                constraints={
                    'parameters': params_str,
                    'return_type': self._parse_base_type(return_type_str)
                }
            )
        
        # Tipo personalizado
        if type_str not in [t.value for t in VaderType]:
            return TypeAnnotation(
                base_type=VaderType.CUALQUIERA,
                custom_type=type_str
            )
        
        # Tipo básico
        return TypeAnnotation(base_type=self._parse_base_type(type_str))
    
    def _parse_base_type(self, type_str: str) -> VaderType:
        """Parsea un tipo básico"""
        type_mapping = {
            'entero': VaderType.ENTERO,
            'int': VaderType.ENTERO,
            'decimal': VaderType.DECIMAL,
            'float': VaderType.DECIMAL,
            'texto': VaderType.TEXTO,
            'string': VaderType.TEXTO,
            'str': VaderType.TEXTO,
            'booleano': VaderType.BOOLEANO,
            'bool': VaderType.BOOLEANO,
            'lista': VaderType.LISTA,
            'array': VaderType.LISTA,
            'diccionario': VaderType.DICCIONARIO,
            'dict': VaderType.DICCIONARIO,
            'funcion': VaderType.FUNCION,
            'function': VaderType.FUNCION,
            'nodo': VaderType.NODO,
            'nodos': VaderType.NODOS,
            'numero': VaderType.NUMERO,
            'number': VaderType.NUMERO,
            'cualquiera': VaderType.CUALQUIERA,
            'any': VaderType.CUALQUIERA,
            'vacio': VaderType.VACIO,
            'void': VaderType.VACIO,
        }
        
        return type_mapping.get(type_str.lower(), VaderType.CUALQUIERA)
    
    def check_code(self, code: str) -> Dict[str, Any]:
        """Verifica tipos en código Vader"""
        self.errors = []
        self.warnings = []
        
        lines = code.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            # Verificar declaraciones de variables tipadas
            self._check_typed_variables(line, line_num)
            
            # Verificar definiciones de tipos personalizados
            self._check_custom_types(line, line_num)
            
            # Verificar firmas de funciones
            self._check_function_signatures(line, line_num)
            
            # Verificar asignaciones de tipos
            self._check_type_assignments(line, line_num)
        
        return {
            'success': len(self.errors) == 0,
            'errors': self.errors,
            'warnings': self.warnings,
            'variables': self.variables,
            'functions': self.functions,
            'custom_types': self.custom_types
        }
    
    def _check_typed_variables(self, line: str, line_num: int):
        """Verifica declaraciones de variables tipadas"""
        # Patrón: variable: tipo = valor
        match = re.match(r'(\w+)\s*:\s*([^=]+?)(?:\s*=\s*(.+))?$', line)
        if match:
            var_name = match.group(1)
            type_str = match.group(2).strip()
            value = match.group(3)
            
            try:
                type_annotation = self.parse_type_annotation(type_str)
                self.variables[var_name] = type_annotation
                
                # Verificar compatibilidad de valor inicial si existe
                if value:
                    inferred_type = self._infer_type_from_value(value)
                    if not self._types_compatible(type_annotation, inferred_type):
                        self.errors.append(
                            f"Línea {line_num}: Tipo incompatible para '{var_name}'. "
                            f"Esperado: {type_str}, Inferido: {inferred_type.base_type.value}"
                        )
                
            except Exception as e:
                self.errors.append(f"Línea {line_num}: Error parseando tipo '{type_str}': {e}")
    
    def _check_custom_types(self, line: str, line_num: int):
        """Verifica definiciones de tipos personalizados"""
        # Patrón: tipo NombreTipo { campo1: tipo1, campo2: tipo2 }
        match = re.match(r'tipo\s+(\w+)\s*\{([^}]+)\}', line)
        if match:
            type_name = match.group(1)
            fields_str = match.group(2)
            
            fields = {}
            for field_def in fields_str.split(','):
                field_def = field_def.strip()
                if ':' in field_def:
                    field_name, field_type = field_def.split(':', 1)
                    field_name = field_name.strip()
                    field_type = field_type.strip()
                    
                    try:
                        fields[field_name] = self.parse_type_annotation(field_type)
                    except Exception as e:
                        self.errors.append(
                            f"Línea {line_num}: Error en campo '{field_name}' del tipo '{type_name}': {e}"
                        )
            
            self.custom_types[type_name] = CustomType(
                name=type_name,
                fields=fields,
                methods={}
            )
    
    def _check_function_signatures(self, line: str, line_num: int):
        """Verifica firmas de funciones tipadas"""
        # Patrón: funcion nombre(param1: tipo1, param2: tipo2) -> tipo_retorno
        match = re.match(r'funcion\s+(\w+)\s*\(([^)]*)\)(?:\s*->\s*(\w+))?', line)
        if match:
            func_name = match.group(1)
            params_str = match.group(2)
            return_type_str = match.group(3) or 'vacio'
            
            parameters = {}
            if params_str.strip():
                for param in params_str.split(','):
                    param = param.strip()
                    if ':' in param:
                        param_name, param_type = param.split(':', 1)
                        param_name = param_name.strip()
                        param_type = param_type.strip()
                        
                        try:
                            parameters[param_name] = self.parse_type_annotation(param_type)
                        except Exception as e:
                            self.errors.append(
                                f"Línea {line_num}: Error en parámetro '{param_name}': {e}"
                            )
                    else:
                        # Parámetro sin tipo (inferir como cualquiera)
                        parameters[param] = TypeAnnotation(base_type=VaderType.CUALQUIERA)
            
            try:
                return_type = self.parse_type_annotation(return_type_str)
                self.functions[func_name] = FunctionSignature(
                    name=func_name,
                    parameters=parameters,
                    return_type=return_type
                )
            except Exception as e:
                self.errors.append(
                    f"Línea {line_num}: Error en tipo de retorno de '{func_name}': {e}"
                )
    
    def _check_type_assignments(self, line: str, line_num: int):
        """Verifica asignaciones de tipos"""
        # Patrón: variable = valor
        match = re.match(r'(\w+)\s*=\s*(.+)$', line)
        if match:
            var_name = match.group(1)
            value = match.group(2)
            
            if var_name in self.variables:
                expected_type = self.variables[var_name]
                inferred_type = self._infer_type_from_value(value)
                
                if not self._types_compatible(expected_type, inferred_type):
                    self.errors.append(
                        f"Línea {line_num}: Asignación incompatible para '{var_name}'. "
                        f"Esperado: {expected_type.base_type.value}, "
                        f"Asignado: {inferred_type.base_type.value}"
                    )
    
    def _infer_type_from_value(self, value: str) -> TypeAnnotation:
        """Infiere el tipo de un valor"""
        value = value.strip()
        
        # Número entero
        if re.match(r'^-?\d+$', value):
            return TypeAnnotation(base_type=VaderType.ENTERO)
        
        # Número decimal
        if re.match(r'^-?\d*\.\d+$', value):
            return TypeAnnotation(base_type=VaderType.DECIMAL)
        
        # Texto (string)
        if (value.startswith('"') and value.endswith('"')) or \
           (value.startswith("'") and value.endswith("'")):
            return TypeAnnotation(base_type=VaderType.TEXTO)
        
        # Booleano
        if value.lower() in ['verdadero', 'falso', 'true', 'false']:
            return TypeAnnotation(base_type=VaderType.BOOLEANO)
        
        # Lista
        if value.startswith('[') and value.endswith(']'):
            return TypeAnnotation(base_type=VaderType.LISTA)
        
        # Diccionario
        if value.startswith('{') and value.endswith('}'):
            return TypeAnnotation(base_type=VaderType.DICCIONARIO)
        
        # Por defecto, cualquiera
        return TypeAnnotation(base_type=VaderType.CUALQUIERA)
    
    def _types_compatible(self, expected: TypeAnnotation, actual: TypeAnnotation) -> bool:
        """Verifica si dos tipos son compatibles"""
        # Cualquiera es compatible con todo
        if expected.base_type == VaderType.CUALQUIERA or \
           actual.base_type == VaderType.CUALQUIERA:
            return True
        
        # Tipos exactos
        if expected.base_type == actual.base_type:
            return True
        
        # Compatibilidad numérica
        numeric_types = {VaderType.ENTERO, VaderType.DECIMAL, VaderType.NUMERO}
        if expected.base_type in numeric_types and actual.base_type in numeric_types:
            return True
        
        # Tipos union
        if expected.union_types:
            return actual.base_type in expected.union_types
        
        # Tipos opcionales
        if expected.is_optional and actual.base_type == VaderType.VACIO:
            return True
        
        return False
    
    def generate_type_definitions(self) -> str:
        """Genera definiciones de tipos para transpilación"""
        definitions = []
        
        # Tipos personalizados
        for custom_type in self.custom_types.values():
            fields_def = []
            for field_name, field_type in custom_type.fields.items():
                type_str = self._type_annotation_to_string(field_type)
                fields_def.append(f"  {field_name}: {type_str}")
            
            definitions.append(f"""
// Tipo personalizado: {custom_type.name}
interface {custom_type.name} {{
{chr(10).join(fields_def)}
}}
""")
        
        # Firmas de funciones
        for func in self.functions.values():
            params = []
            for param_name, param_type in func.parameters.items():
                type_str = self._type_annotation_to_string(param_type)
                params.append(f"{param_name}: {type_str}")
            
            return_type_str = self._type_annotation_to_string(func.return_type)
            
            definitions.append(f"""
// Función: {func.name}
function {func.name}({', '.join(params)}): {return_type_str};
""")
        
        return '\n'.join(definitions)
    
    def _type_annotation_to_string(self, annotation: TypeAnnotation) -> str:
        """Convierte una anotación de tipo a string"""
        if annotation.custom_type:
            type_str = annotation.custom_type
        else:
            type_str = annotation.base_type.value
        
        if annotation.union_types:
            union_strs = [t.value for t in annotation.union_types]
            type_str = ' | '.join(union_strs)
        
        if annotation.is_array:
            type_str = f"{type_str}[]"
        
        if annotation.is_optional:
            type_str = f"{type_str} | null"
        
        return type_str

def main():
    """Función principal para testing"""
    code_example = """
# Ejemplos de tipado fuerte en Vader
edad: entero = 25
nombre: texto = "Juan"
activo: booleano? = verdadero
puntuaciones: lista[entero] = [10, 20, 30]
configuracion: diccionario = {"tema": "oscuro"}

# Tipo personalizado
tipo Usuario {
    nombre: texto,
    edad: entero,
    email: texto?
}

# Función tipada
funcion saludar(nombre: texto, edad: entero?) -> texto
    si edad
        retornar "Hola " + nombre + ", tienes " + edad + " años"
    sino
        retornar "Hola " + nombre
    fin si
fin funcion

# Función con tipos union
funcion procesar_dato(valor: entero | texto) -> texto
    retornar "Procesado: " + valor
fin funcion
"""
    
    checker = VaderTypeChecker()
    result = checker.check_code(code_example)
    
    print("🔍 VADER TYPE CHECKER - Resultados:")
    print(f"✅ Éxito: {result['success']}")
    print(f"❌ Errores: {len(result['errors'])}")
    print(f"⚠️ Advertencias: {len(result['warnings'])}")
    print()
    
    if result['errors']:
        print("❌ ERRORES:")
        for error in result['errors']:
            print(f"  - {error}")
        print()
    
    if result['warnings']:
        print("⚠️ ADVERTENCIAS:")
        for warning in result['warnings']:
            print(f"  - {warning}")
        print()
    
    print(f"📝 Variables encontradas: {len(result['variables'])}")
    for var_name, var_type in result['variables'].items():
        print(f"  - {var_name}: {var_type.base_type.value}")
    
    print(f"🔧 Funciones encontradas: {len(result['functions'])}")
    for func_name, func_sig in result['functions'].items():
        params = [f"{p}:{t.base_type.value}" for p, t in func_sig.parameters.items()]
        print(f"  - {func_name}({', '.join(params)}) -> {func_sig.return_type.base_type.value}")
    
    print(f"🏗️ Tipos personalizados: {len(result['custom_types'])}")
    for type_name, custom_type in result['custom_types'].items():
        fields = [f"{f}:{t.base_type.value}" for f, t in custom_type.fields.items()]
        print(f"  - {type_name} {{ {', '.join(fields)} }}")

if __name__ == "__main__":
    main()
