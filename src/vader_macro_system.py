#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VADER 7.0 - SISTEMA DE MACROS Y META-PROGRAMACIÓN
=================================================
Sistema completo de macros para Vader con meta-programación y DSLs internos

Características:
- Macros de expansión de código
- Meta-programación con reflexión
- DSLs internos personalizados
- Generación de código dinámico
- Transformaciones AST
- Macros condicionales y recursivas
- Sistema de plantillas avanzado

Autor: Vader Team
Versión: 7.0.0 "Universal"
Fecha: 2025
"""

import re
import ast
import inspect
from typing import Dict, List, Any, Optional, Callable, Union, Tuple
from dataclasses import dataclass, field
from enum import Enum
import textwrap
import importlib
import types

class MacroType(Enum):
    """Tipos de macros"""
    SIMPLE = "simple"           # Reemplazo simple de texto
    PARAMETRIC = "parametric"   # Macro con parámetros
    CONDITIONAL = "conditional" # Macro condicional
    RECURSIVE = "recursive"     # Macro recursiva
    AST_TRANSFORM = "ast_transform"  # Transformación AST
    CODE_GEN = "code_gen"       # Generación de código

@dataclass
class VaderMacro:
    """Representa una macro Vader"""
    name: str
    macro_type: MacroType
    parameters: List[str] = field(default_factory=list)
    body: str = ""
    conditions: Dict[str, str] = field(default_factory=dict)
    transforms: List[Callable] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def expand(self, args: Dict[str, Any] = None) -> str:
        """Expande la macro con los argumentos dados"""
        if not args:
            args = {}
        
        expanded = self.body
        
        # Reemplazar parámetros
        for param in self.parameters:
            if param in args:
                pattern = rf'\b{re.escape(param)}\b'
                replacement = str(args[param])
                expanded = re.sub(pattern, replacement, expanded)
        
        return expanded

@dataclass
class DSLRule:
    """Regla de un DSL interno"""
    pattern: str
    replacement: str
    conditions: List[str] = field(default_factory=list)
    priority: int = 0

class VaderMacroSystem:
    """Sistema de macros para Vader"""
    
    def __init__(self):
        self.macros: Dict[str, VaderMacro] = {}
        self.dsls: Dict[str, List[DSLRule]] = {}
        self.expansion_cache: Dict[str, str] = {}
        self.max_recursion_depth = 100
        
        # Patrones de reconocimiento de macros
        self.macro_patterns = {
            'macro_def': r'macro\s+(\w+)\s*(?:\(([^)]*)\))?\s*\{([^}]+)\}',
            'macro_call': r'@(\w+)(?:\(([^)]*)\))?',
            'conditional_macro': r'macro\s+(\w+)\s*si\s+([^{]+)\s*\{([^}]+)\}',
            'dsl_def': r'dsl\s+(\w+)\s*\{([^}]+)\}',
            'dsl_rule': r'regla\s+([^->]+)->\s*(.+)',
            'code_gen': r'generar\s+(\w+)\s*\(([^)]*)\)',
            'meta_call': r'meta\.(\w+)\s*\(([^)]*)\)',
            'template': r'plantilla\s+(\w+)\s*\{([^}]+)\}',
        }
        
        # Macros predefinidas
        self._register_builtin_macros()
    
    def _register_builtin_macros(self):
        """Registra macros predefinidas del sistema"""
        
        # Macro para logging
        self.register_macro(VaderMacro(
            name="log",
            macro_type=MacroType.PARAMETRIC,
            parameters=["nivel", "mensaje"],
            body="print(f'[{nivel}] {mensaje}')"
        ))
        
        # Macro para validación
        self.register_macro(VaderMacro(
            name="validar",
            macro_type=MacroType.PARAMETRIC,
            parameters=["condicion", "error"],
            body="if not ({condicion}): raise ValueError('{error}')"
        ))
        
        # Macro para timing
        self.register_macro(VaderMacro(
            name="cronometrar",
            macro_type=MacroType.PARAMETRIC,
            parameters=["codigo"],
            body="""
import time
_start = time.time()
{codigo}
_end = time.time()
print(f'Tiempo: {{_end - _start:.4f}}s')
"""
        ))
        
        # Macro para singleton
        self.register_macro(VaderMacro(
            name="singleton",
            macro_type=MacroType.PARAMETRIC,
            parameters=["clase"],
            body="""
_instances = {{}}
def get_instance():
    if '{clase}' not in _instances:
        _instances['{clase}'] = {clase}()
    return _instances['{clase}']
{clase}.get_instance = staticmethod(get_instance)
"""
        ))
        
        # Macro para propiedades
        self.register_macro(VaderMacro(
            name="propiedad",
            macro_type=MacroType.PARAMETRIC,
            parameters=["nombre", "tipo"],
            body="""
@property
def {nombre}(self):
    return self._{nombre}

@{nombre}.setter
def {nombre}(self, value: {tipo}):
    self._{nombre} = value
"""
        ))
    
    def register_macro(self, macro: VaderMacro):
        """Registra una nueva macro"""
        self.macros[macro.name] = macro
    
    def parse_macro_definition(self, code: str) -> List[VaderMacro]:
        """Parsea definiciones de macros en código"""
        macros = []
        
        # Macro simple
        for match in re.finditer(self.macro_patterns['macro_def'], code, re.MULTILINE | re.DOTALL):
            name = match.group(1)
            params_str = match.group(2) or ""
            body = match.group(3).strip()
            
            parameters = []
            if params_str:
                parameters = [p.strip() for p in params_str.split(',')]
            
            macro = VaderMacro(
                name=name,
                macro_type=MacroType.PARAMETRIC if parameters else MacroType.SIMPLE,
                parameters=parameters,
                body=body
            )
            macros.append(macro)
        
        # Macro condicional
        for match in re.finditer(self.macro_patterns['conditional_macro'], code, re.MULTILINE | re.DOTALL):
            name = match.group(1)
            condition = match.group(2).strip()
            body = match.group(3).strip()
            
            macro = VaderMacro(
                name=name,
                macro_type=MacroType.CONDITIONAL,
                body=body,
                conditions={'if': condition}
            )
            macros.append(macro)
        
        return macros
    
    def expand_macros(self, code: str, context: Dict[str, Any] = None) -> str:
        """Expande todas las macros en el código"""
        if context is None:
            context = {}
        
        expanded_code = code
        recursion_count = 0
        
        while recursion_count < self.max_recursion_depth:
            original_code = expanded_code
            
            # Buscar llamadas a macros
            for match in re.finditer(self.macro_patterns['macro_call'], expanded_code):
                macro_name = match.group(1)
                args_str = match.group(2) or ""
                
                if macro_name in self.macros:
                    # Parsear argumentos
                    args = {}
                    if args_str:
                        arg_pairs = [arg.strip() for arg in args_str.split(',')]
                        for i, arg in enumerate(arg_pairs):
                            if '=' in arg:
                                key, value = arg.split('=', 1)
                                args[key.strip()] = value.strip()
                            else:
                                # Argumento posicional
                                if i < len(self.macros[macro_name].parameters):
                                    param_name = self.macros[macro_name].parameters[i]
                                    args[param_name] = arg
                    
                    # Expandir macro
                    macro = self.macros[macro_name]
                    
                    # Verificar condiciones si es macro condicional
                    if macro.macro_type == MacroType.CONDITIONAL:
                        condition = macro.conditions.get('if', 'True')
                        try:
                            if not eval(condition, context):
                                continue
                        except:
                            continue
                    
                    expansion = macro.expand(args)
                    expanded_code = expanded_code.replace(match.group(0), expansion)
            
            # Si no hubo cambios, terminar
            if expanded_code == original_code:
                break
            
            recursion_count += 1
        
        return expanded_code
    
    def create_dsl(self, name: str, rules: List[DSLRule]):
        """Crea un DSL interno"""
        # Ordenar reglas por prioridad
        sorted_rules = sorted(rules, key=lambda r: r.priority, reverse=True)
        self.dsls[name] = sorted_rules
    
    def parse_dsl_definition(self, code: str) -> Dict[str, List[DSLRule]]:
        """Parsea definiciones de DSL"""
        dsls = {}
        
        for match in re.finditer(self.macro_patterns['dsl_def'], code, re.MULTILINE | re.DOTALL):
            dsl_name = match.group(1)
            dsl_body = match.group(2)
            
            rules = []
            for rule_match in re.finditer(self.macro_patterns['dsl_rule'], dsl_body):
                pattern = rule_match.group(1).strip()
                replacement = rule_match.group(2).strip()
                
                rule = DSLRule(pattern=pattern, replacement=replacement)
                rules.append(rule)
            
            dsls[dsl_name] = rules
        
        return dsls
    
    def apply_dsl(self, dsl_name: str, code: str) -> str:
        """Aplica un DSL al código"""
        if dsl_name not in self.dsls:
            return code
        
        transformed_code = code
        
        for rule in self.dsls[dsl_name]:
            # Verificar condiciones
            if rule.conditions:
                # Implementar lógica de condiciones
                pass
            
            # Aplicar transformación
            try:
                transformed_code = re.sub(rule.pattern, rule.replacement, transformed_code)
            except re.error:
                # Si el patrón regex es inválido, intentar reemplazo literal
                transformed_code = transformed_code.replace(rule.pattern, rule.replacement)
        
        return transformed_code
    
    def generate_code(self, template_name: str, **kwargs) -> str:
        """Genera código usando plantillas"""
        if template_name not in self.macros:
            raise ValueError(f"Plantilla '{template_name}' no encontrada")
        
        template_macro = self.macros[template_name]
        return template_macro.expand(kwargs)
    
    def meta_program(self, code: str, meta_context: Dict[str, Any] = None) -> str:
        """Ejecuta meta-programación en el código"""
        if meta_context is None:
            meta_context = {}
        
        processed_code = code
        
        # Procesar llamadas meta
        for match in re.finditer(self.macro_patterns['meta_call'], processed_code):
            meta_func = match.group(1)
            args_str = match.group(2)
            
            if meta_func == 'get_functions':
                # Obtener lista de funciones definidas
                functions = self._extract_functions(processed_code)
                replacement = str(functions)
                processed_code = processed_code.replace(match.group(0), replacement)
            
            elif meta_func == 'get_classes':
                # Obtener lista de clases definidas
                classes = self._extract_classes(processed_code)
                replacement = str(classes)
                processed_code = processed_code.replace(match.group(0), replacement)
            
            elif meta_func == 'generate_getters_setters':
                # Generar getters y setters automáticamente
                class_name = args_str.strip('"\'')
                getters_setters = self._generate_getters_setters(processed_code, class_name)
                processed_code += '\n' + getters_setters
        
        return processed_code
    
    def _extract_functions(self, code: str) -> List[str]:
        """Extrae nombres de funciones del código"""
        functions = []
        for match in re.finditer(r'def\s+(\w+)\s*\(', code):
            functions.append(match.group(1))
        return functions
    
    def _extract_classes(self, code: str) -> List[str]:
        """Extrae nombres de clases del código"""
        classes = []
        for match in re.finditer(r'class\s+(\w+)\s*[:(]', code):
            classes.append(match.group(1))
        return classes
    
    def _generate_getters_setters(self, code: str, class_name: str) -> str:
        """Genera getters y setters para una clase"""
        # Buscar atributos de la clase
        class_pattern = rf'class\s+{re.escape(class_name)}\s*[:(].*?(?=class|\Z)'
        class_match = re.search(class_pattern, code, re.DOTALL)
        
        if not class_match:
            return ""
        
        class_body = class_match.group(0)
        
        # Extraer atributos (self.attribute = ...)
        attributes = set()
        for match in re.finditer(r'self\.(\w+)\s*=', class_body):
            attributes.add(match.group(1))
        
        # Generar getters y setters
        getters_setters = []
        for attr in attributes:
            getter_setter = f"""
    @property
    def {attr}(self):
        return self._{attr}
    
    @{attr}.setter
    def {attr}(self, value):
        self._{attr} = value
"""
            getters_setters.append(getter_setter)
        
        return '\n'.join(getters_setters)
    
    def create_ast_transformer(self, transformer_func: Callable) -> Callable:
        """Crea un transformador AST personalizado"""
        def transform_code(code: str) -> str:
            try:
                tree = ast.parse(code)
                transformed_tree = transformer_func(tree)
                return ast.unparse(transformed_tree)
            except Exception as e:
                print(f"Error en transformación AST: {e}")
                return code
        
        return transform_code
    
    def register_code_generator(self, name: str, generator_func: Callable):
        """Registra un generador de código"""
        macro = VaderMacro(
            name=name,
            macro_type=MacroType.CODE_GEN,
            metadata={'generator': generator_func}
        )
        self.register_macro(macro)
    
    def process_code_generation(self, code: str) -> str:
        """Procesa generación de código"""
        processed_code = code
        
        for match in re.finditer(self.macro_patterns['code_gen'], processed_code):
            gen_name = match.group(1)
            args_str = match.group(2)
            
            if gen_name in self.macros:
                macro = self.macros[gen_name]
                if macro.macro_type == MacroType.CODE_GEN:
                    generator = macro.metadata.get('generator')
                    if generator:
                        # Parsear argumentos
                        args = []
                        if args_str:
                            args = [arg.strip().strip('"\'') for arg in args_str.split(',')]
                        
                        # Generar código
                        generated = generator(*args)
                        processed_code = processed_code.replace(match.group(0), generated)
        
        return processed_code
    
    def create_macro_library(self) -> str:
        """Crea una librería de macros comunes"""
        library = """
# Librería de Macros Vader
# ========================

# Macro para crear enums
macro enum(nombre, valores) {
    from enum import Enum
    class {nombre}(Enum):
        {valores}
}

# Macro para crear dataclasses
macro dataclass(nombre, campos) {
    from dataclasses import dataclass
    
    @dataclass
    class {nombre}:
        {campos}
}

# Macro para crear propiedades automáticas
macro auto_property(nombre, tipo) {
    @property
    def {nombre}(self):
        return getattr(self, f'_{nombre}', None)
    
    @{nombre}.setter
    def {nombre}(self, value: {tipo}):
        setattr(self, f'_{nombre}', value)
}

# Macro para lazy loading
macro lazy(nombre, inicializador) {
    @property
    def {nombre}(self):
        if not hasattr(self, f'_{nombre}_cached'):
            setattr(self, f'_{nombre}_cached', {inicializador})
        return getattr(self, f'_{nombre}_cached')
}

# Macro para retry automático
macro retry(intentos, funcion) {
    for _intento in range({intentos}):
        try:
            result = {funcion}
            break
        except Exception as e:
            if _intento == {intentos} - 1:
                raise e
            continue
}

# Macro para cache de métodos
macro cache_method(metodo) {
    import functools
    {metodo} = functools.lru_cache(maxsize=128)({metodo})
}
"""
        return library

def main():
    """Función principal para testing"""
    # Ejemplos de macros en Vader
    macro_examples = """
# Definición de macros
macro log(nivel, mensaje) {
    print(f'[{nivel}] {mensaje}')
}

macro validar(condicion, error) {
    if not ({condicion}):
        raise ValueError('{error}')
}

# Macro condicional
macro debug_info si DEBUG_MODE {
    print(f'Debug: {info}')
}

# DSL para validaciones
dsl validaciones {
    regla requerido -> if not value: raise ValueError('Campo requerido')
    regla email -> if '@' not in value: raise ValueError('Email inválido')
    regla longitud_min(n) -> if len(value) < n: raise ValueError(f'Mínimo {n} caracteres')
}

# Plantilla para CRUD
plantilla crud_class {
    class {nombre}CRUD:
        def crear(self, datos):
            return self.db.insert('{tabla}', datos)
        
        def leer(self, id):
            return self.db.select('{tabla}', id)
        
        def actualizar(self, id, datos):
            return self.db.update('{tabla}', id, datos)
        
        def eliminar(self, id):
            return self.db.delete('{tabla}', id)
}

# Uso de macros
@log("INFO", "Iniciando aplicación")
@validar(usuario.edad >= 18, "Debe ser mayor de edad")

# Generación de código
generar crud_class("Usuario", "usuarios")

# Meta-programación
funciones_disponibles = meta.get_functions()
clases_disponibles = meta.get_classes()
meta.generate_getters_setters("MiClase")
"""
    
    macro_system = VaderMacroSystem()
    
    print("🧰 VADER MACRO SYSTEM - Análisis y expansión:")
    print("=" * 70)
    
    # Parsear definiciones de macros
    macros = macro_system.parse_macro_definition(macro_examples)
    print(f"📝 Macros definidas: {len(macros)}")
    for macro in macros:
        print(f"  - {macro.name} ({macro.macro_type.value})")
        if macro.parameters:
            print(f"    Parámetros: {', '.join(macro.parameters)}")
    
    print()
    
    # Parsear DSLs
    dsls = macro_system.parse_dsl_definition(macro_examples)
    print(f"🎯 DSLs definidos: {len(dsls)}")
    for dsl_name, rules in dsls.items():
        print(f"  - {dsl_name}: {len(rules)} reglas")
    
    print()
    
    # Ejemplo de expansión de macro
    test_code = """
@log("DEBUG", "Procesando usuario")
@validar(edad > 0, "Edad debe ser positiva")
resultado = procesar_usuario(edad)
"""
    
    print("🔧 Ejemplo de expansión:")
    print("Código original:")
    print(textwrap.indent(test_code, "  "))
    
    # Registrar macros parseadas
    for macro in macros:
        macro_system.register_macro(macro)
    
    expanded = macro_system.expand_macros(test_code)
    print("Código expandido:")
    print(textwrap.indent(expanded, "  "))
    
    print()
    print("=" * 70)
    print("✅ Sistema de macros Vader implementado")
    print("🚀 Características disponibles:")
    print("  - Macros simples y paramétricas")
    print("  - Macros condicionales y recursivas")
    print("  - DSLs internos personalizados")
    print("  - Meta-programación con reflexión")
    print("  - Generación de código dinámico")
    print("  - Transformaciones AST")
    print("  - Plantillas de código")
    print("  - Librería de macros comunes")
    
    # Generar librería de macros
    library = macro_system.create_macro_library()
    print(f"\n📚 Librería de macros generada ({len(library)} caracteres)")
    print("   Incluye: enum, dataclass, auto_property, lazy, retry, cache_method")

if __name__ == "__main__":
    main()
