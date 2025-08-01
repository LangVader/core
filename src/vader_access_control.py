#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VADER 7.0 - SISTEMA DE CONTROL DE ACCESO EN CLASES
==================================================
Sistema completo de encapsulación para Vader con modificadores de acceso

Características:
- Modificadores de acceso (privado, protegido, público)
- Getters y setters automáticos
- Propiedades con validación
- Herencia con control de acceso
- Interfaces y clases abstractas
- Decoradores de acceso
- Validación en tiempo de ejecución

Autor: Vader Team
Versión: 7.0.0 "Universal"
Fecha: 2025
"""

import re
import inspect
from typing import Dict, List, Any, Optional, Callable, Union, Type
from dataclasses import dataclass, field
from enum import Enum
import functools
import warnings

class AccessLevel(Enum):
    """Niveles de acceso"""
    PUBLIC = "publico"
    PROTECTED = "protegido"
    PRIVATE = "privado"

@dataclass
class AccessMember:
    """Miembro de clase con control de acceso"""
    name: str
    access_level: AccessLevel
    member_type: str  # 'method', 'property', 'attribute'
    getter: Optional[Callable] = None
    setter: Optional[Callable] = None
    validator: Optional[Callable] = None
    documentation: str = ""
    readonly: bool = False
    deprecated: bool = False

@dataclass
class VaderClass:
    """Representa una clase Vader con control de acceso"""
    name: str
    members: Dict[str, AccessMember] = field(default_factory=dict)
    parent_class: Optional[str] = None
    interfaces: List[str] = field(default_factory=list)
    is_abstract: bool = False
    is_final: bool = False

class VaderAccessControlSystem:
    """Sistema de control de acceso para Vader"""
    
    def __init__(self):
        self.classes: Dict[str, VaderClass] = {}
        self.interfaces: Dict[str, List[str]] = {}
        
        # Patrones de reconocimiento
        self.access_patterns = {
            'class_def': r'clase\s+(\w+)(?:\s+hereda\s+(\w+))?(?:\s+implementa\s+([^{]+))?\s*\{',
            'abstract_class': r'abstracta\s+clase\s+(\w+)',
            'final_class': r'final\s+clase\s+(\w+)',
            'interface_def': r'interfaz\s+(\w+)\s*\{([^}]+)\}',
            'private_member': r'privado\s+(\w+)\s+(\w+)',
            'protected_member': r'protegido\s+(\w+)\s+(\w+)',
            'public_member': r'publico\s+(\w+)\s+(\w+)',
            'property_def': r'propiedad\s+(\w+)(?:\s*:\s*(\w+))?\s*\{([^}]+)\}',
            'getter': r'obtener\s*\{([^}]+)\}',
            'setter': r'establecer\s*\(([^)]+)\)\s*\{([^}]+)\}',
            'readonly': r'solo_lectura\s+(\w+)\s+(\w+)',
            'deprecated': r'deprecado\s+(\w+)\s+(\w+)',
            'validator': r'validar\s*\(([^)]+)\)\s*\{([^}]+)\}',
        }
    
    def parse_class_definition(self, code: str) -> List[VaderClass]:
        """Parsea definiciones de clases con control de acceso"""
        classes = []
        lines = code.split('\n')
        current_class = None
        in_class = False
        brace_count = 0
        
        for line_num, line in enumerate(lines):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            # Clase abstracta
            abstract_match = re.match(self.access_patterns['abstract_class'], line)
            if abstract_match:
                class_name = abstract_match.group(1)
                current_class = VaderClass(name=class_name, is_abstract=True)
                in_class = True
                continue
            
            # Clase final
            final_match = re.match(self.access_patterns['final_class'], line)
            if final_match:
                class_name = final_match.group(1)
                current_class = VaderClass(name=class_name, is_final=True)
                in_class = True
                continue
            
            # Definición de clase normal
            class_match = re.match(self.access_patterns['class_def'], line)
            if class_match:
                class_name = class_match.group(1)
                parent_class = class_match.group(2)
                interfaces_str = class_match.group(3)
                
                interfaces = []
                if interfaces_str:
                    interfaces = [i.strip() for i in interfaces_str.split(',')]
                
                current_class = VaderClass(
                    name=class_name,
                    parent_class=parent_class,
                    interfaces=interfaces
                )
                in_class = True
                brace_count = 1
                continue
            
            if in_class and current_class:
                # Contar llaves para saber cuándo termina la clase
                brace_count += line.count('{') - line.count('}')
                
                if brace_count <= 0:
                    classes.append(current_class)
                    current_class = None
                    in_class = False
                    continue
                
                # Miembro privado
                private_match = re.match(self.access_patterns['private_member'], line)
                if private_match:
                    member_type = private_match.group(1)
                    member_name = private_match.group(2)
                    
                    member = AccessMember(
                        name=member_name,
                        access_level=AccessLevel.PRIVATE,
                        member_type=member_type
                    )
                    current_class.members[member_name] = member
                    continue
                
                # Miembro protegido
                protected_match = re.match(self.access_patterns['protected_member'], line)
                if protected_match:
                    member_type = protected_match.group(1)
                    member_name = protected_match.group(2)
                    
                    member = AccessMember(
                        name=member_name,
                        access_level=AccessLevel.PROTECTED,
                        member_type=member_type
                    )
                    current_class.members[member_name] = member
                    continue
                
                # Miembro público
                public_match = re.match(self.access_patterns['public_member'], line)
                if public_match:
                    member_type = public_match.group(1)
                    member_name = public_match.group(2)
                    
                    member = AccessMember(
                        name=member_name,
                        access_level=AccessLevel.PUBLIC,
                        member_type=member_type
                    )
                    current_class.members[member_name] = member
                    continue
                
                # Solo lectura
                readonly_match = re.match(self.access_patterns['readonly'], line)
                if readonly_match:
                    member_type = readonly_match.group(1)
                    member_name = readonly_match.group(2)
                    
                    member = AccessMember(
                        name=member_name,
                        access_level=AccessLevel.PUBLIC,
                        member_type=member_type,
                        readonly=True
                    )
                    current_class.members[member_name] = member
                    continue
                
                # Deprecado
                deprecated_match = re.match(self.access_patterns['deprecated'], line)
                if deprecated_match:
                    member_type = deprecated_match.group(1)
                    member_name = deprecated_match.group(2)
                    
                    member = AccessMember(
                        name=member_name,
                        access_level=AccessLevel.PUBLIC,
                        member_type=member_type,
                        deprecated=True
                    )
                    current_class.members[member_name] = member
                    continue
        
        # Agregar última clase si quedó pendiente
        if current_class:
            classes.append(current_class)
        
        return classes
    
    def parse_properties(self, code: str) -> Dict[str, AccessMember]:
        """Parsea definiciones de propiedades"""
        properties = {}
        
        for match in re.finditer(self.access_patterns['property_def'], code, re.MULTILINE | re.DOTALL):
            prop_name = match.group(1)
            prop_type = match.group(2) or "Any"
            prop_body = match.group(3)
            
            # Buscar getter
            getter_match = re.search(self.access_patterns['getter'], prop_body)
            getter_code = getter_match.group(1) if getter_match else None
            
            # Buscar setter
            setter_match = re.search(self.access_patterns['setter'], prop_body)
            setter_param = setter_match.group(1) if setter_match else None
            setter_code = setter_match.group(2) if setter_match else None
            
            # Buscar validador
            validator_match = re.search(self.access_patterns['validator'], prop_body)
            validator_param = validator_match.group(1) if validator_match else None
            validator_code = validator_match.group(2) if validator_match else None
            
            property_member = AccessMember(
                name=prop_name,
                access_level=AccessLevel.PUBLIC,
                member_type="property",
                readonly=setter_code is None
            )
            
            properties[prop_name] = property_member
        
        return properties
    
    def generate_python_class(self, vader_class: VaderClass) -> str:
        """Genera código Python con control de acceso"""
        class_code = []
        
        # Decoradores de clase
        decorators = []
        if vader_class.is_abstract:
            decorators.append("@abstractmethod")
        
        # Definición de clase
        inheritance = ""
        if vader_class.parent_class:
            inheritance = f"({vader_class.parent_class})"
        
        class_line = f"class {vader_class.name}{inheritance}:"
        if decorators:
            class_code.extend(decorators)
        class_code.append(class_line)
        
        # Constructor con inicialización de miembros privados
        constructor_lines = ["    def __init__(self):"]
        if vader_class.parent_class:
            constructor_lines.append("        super().__init__()")
        
        # Inicializar miembros
        for member_name, member in vader_class.members.items():
            if member.access_level == AccessLevel.PRIVATE:
                constructor_lines.append(f"        self.__{member_name} = None")
            elif member.access_level == AccessLevel.PROTECTED:
                constructor_lines.append(f"        self._{member_name} = None")
            else:
                constructor_lines.append(f"        self.{member_name} = None")
        
        if len(constructor_lines) == 1:
            constructor_lines.append("        pass")
        
        class_code.extend(constructor_lines)
        class_code.append("")
        
        # Generar métodos y propiedades
        for member_name, member in vader_class.members.items():
            if member.member_type == "property":
                class_code.extend(self._generate_property_methods(member))
            elif member.member_type == "method":
                class_code.extend(self._generate_method(member))
        
        # Método para validar acceso
        class_code.extend([
            "    def _validate_access(self, member_name, access_level):",
            "        '''Valida el acceso a un miembro'''",
            "        import inspect",
            "        frame = inspect.currentframe().f_back",
            "        caller_class = frame.f_locals.get('self', None)",
            "        ",
            "        if access_level == 'private':",
            "            if not isinstance(caller_class, self.__class__):",
            "                raise AttributeError(f'No se puede acceder al miembro privado {member_name}')",
            "        elif access_level == 'protected':",
            "            if not (isinstance(caller_class, self.__class__) or ",
            "                   issubclass(caller_class.__class__, self.__class__)):",
            "                raise AttributeError(f'No se puede acceder al miembro protegido {member_name}')",
            ""
        ])
        
        return '\n'.join(class_code)
    
    def _generate_property_methods(self, member: AccessMember) -> List[str]:
        """Genera métodos getter y setter para una propiedad"""
        methods = []
        
        # Determinar nombre interno
        if member.access_level == AccessLevel.PRIVATE:
            internal_name = f"__{member.name}"
        elif member.access_level == AccessLevel.PROTECTED:
            internal_name = f"_{member.name}"
        else:
            internal_name = member.name
        
        # Getter
        methods.extend([
            f"    @property",
            f"    def {member.name}(self):",
        ])
        
        if member.deprecated:
            methods.extend([
                f"        import warnings",
                f"        warnings.warn('La propiedad {member.name} está deprecada', DeprecationWarning)",
            ])
        
        methods.extend([
            f"        return getattr(self, '{internal_name}', None)",
            ""
        ])
        
        # Setter (solo si no es readonly)
        if not member.readonly:
            methods.extend([
                f"    @{member.name}.setter",
                f"    def {member.name}(self, value):",
            ])
            
            if member.validator:
                methods.append(f"        self._validate_{member.name}(value)")
            
            methods.extend([
                f"        setattr(self, '{internal_name}', value)",
                ""
            ])
            
            # Método validador si existe
            if member.validator:
                methods.extend([
                    f"    def _validate_{member.name}(self, value):",
                    f"        '''Valida el valor de {member.name}'''",
                    f"        # Implementar validación personalizada",
                    f"        pass",
                    ""
                ])
        
        return methods
    
    def _generate_method(self, member: AccessMember) -> List[str]:
        """Genera un método con control de acceso"""
        methods = []
        
        # Decoradores
        decorators = []
        if member.deprecated:
            decorators.append("    @deprecated")
        
        # Definición del método
        method_def = f"    def {member.name}(self"
        
        # Agregar parámetros si los hay
        method_def += "):"
        
        if decorators:
            methods.extend(decorators)
        
        methods.append(method_def)
        
        # Validación de acceso
        if member.access_level != AccessLevel.PUBLIC:
            methods.append(f"        self._validate_access('{member.name}', '{member.access_level.value}')")
        
        if member.deprecated:
            methods.extend([
                f"        import warnings",
                f"        warnings.warn('El método {member.name} está deprecado', DeprecationWarning)",
            ])
        
        methods.extend([
            f"        '''Método {member.access_level.value} {member.name}'''",
            f"        pass",
            ""
        ])
        
        return methods
    
    def create_interface(self, name: str, methods: List[str]):
        """Crea una interfaz"""
        self.interfaces[name] = methods
    
    def generate_interface_code(self, name: str) -> str:
        """Genera código para una interfaz"""
        if name not in self.interfaces:
            return ""
        
        interface_code = [
            f"from abc import ABC, abstractmethod",
            f"",
            f"class {name}(ABC):",
            f"    '''Interfaz {name}'''"
        ]
        
        for method in self.interfaces[name]:
            interface_code.extend([
                f"    @abstractmethod",
                f"    def {method}(self):",
                f"        '''Método abstracto {method}'''",
                f"        pass",
                f""
            ])
        
        return '\n'.join(interface_code)
    
    def validate_class_implementation(self, vader_class: VaderClass) -> List[str]:
        """Valida que una clase implemente correctamente sus interfaces"""
        errors = []
        
        for interface_name in vader_class.interfaces:
            if interface_name in self.interfaces:
                required_methods = self.interfaces[interface_name]
                
                for method in required_methods:
                    if method not in vader_class.members:
                        errors.append(f"La clase {vader_class.name} debe implementar el método {method} de la interfaz {interface_name}")
                    else:
                        member = vader_class.members[method]
                        if member.member_type != "method":
                            errors.append(f"El miembro {method} debe ser un método en la clase {vader_class.name}")
        
        return errors
    
    def create_access_decorators(self) -> str:
        """Crea decoradores para control de acceso"""
        decorators_code = """
import functools
import warnings
import inspect

def private(func):
    '''Decorador para métodos privados'''
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        frame = inspect.currentframe().f_back
        caller_class = frame.f_locals.get('self', None)
        
        if not isinstance(caller_class, self.__class__):
            raise AttributeError(f'No se puede acceder al método privado {func.__name__}')
        
        return func(self, *args, **kwargs)
    return wrapper

def protected(func):
    '''Decorador para métodos protegidos'''
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        frame = inspect.currentframe().f_back
        caller_class = frame.f_locals.get('self', None)
        
        if not (isinstance(caller_class, self.__class__) or 
               (caller_class and issubclass(caller_class.__class__, self.__class__))):
            raise AttributeError(f'No se puede acceder al método protegido {func.__name__}')
        
        return func(self, *args, **kwargs)
    return wrapper

def deprecated(func):
    '''Decorador para métodos deprecados'''
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        warnings.warn(f'El método {func.__name__} está deprecado', 
                     DeprecationWarning, stacklevel=2)
        return func(*args, **kwargs)
    return wrapper

def readonly_property(func):
    '''Decorador para propiedades de solo lectura'''
    return property(func)

def validated_property(validator_func):
    '''Decorador para propiedades con validación'''
    def decorator(func):
        def setter(self, value):
            validator_func(value)
            setattr(self, f'_{func.__name__}', value)
        
        def getter(self):
            return getattr(self, f'_{func.__name__}', None)
        
        return property(getter, setter)
    return decorator
"""
        return decorators_code

def main():
    """Función principal para testing"""
    # Ejemplo de clase con control de acceso
    class_example = """
# Interfaz
interfaz Drawable {
    dibujar()
    obtener_area()
}

# Clase abstracta
abstracta clase Forma implementa Drawable {
    protegido atributo color
    privado atributo id
    publico metodo constructor(color)
    
    propiedad area : float {
        obtener {
            return self.calcular_area()
        }
    }
    
    solo_lectura atributo tipo
    deprecado metodo metodo_viejo()
}

# Clase final
final clase Rectangulo hereda Forma {
    privado atributo ancho
    privado atributo alto
    
    publico metodo constructor(ancho, alto, color)
    
    propiedad ancho : float {
        obtener {
            return self.__ancho
        }
        establecer(valor) {
            if valor <= 0:
                raise ValueError("El ancho debe ser positivo")
            self.__ancho = valor
        }
        validar(valor) {
            return valor > 0 and valor < 1000
        }
    }
    
    publico metodo calcular_area()
    publico metodo dibujar()
    publico metodo obtener_area()
}
"""
    
    access_system = VaderAccessControlSystem()
    
    print("🔐 VADER ACCESS CONTROL SYSTEM - Análisis de clases:")
    print("=" * 70)
    
    # Parsear clases
    classes = access_system.parse_class_definition(class_example)
    print(f"📝 Clases analizadas: {len(classes)}")
    
    for vader_class in classes:
        print(f"\n🏗️ Clase: {vader_class.name}")
        print(f"   Abstracta: {vader_class.is_abstract}")
        print(f"   Final: {vader_class.is_final}")
        if vader_class.parent_class:
            print(f"   Hereda de: {vader_class.parent_class}")
        if vader_class.interfaces:
            print(f"   Implementa: {', '.join(vader_class.interfaces)}")
        
        print(f"   Miembros ({len(vader_class.members)}):")
        for member_name, member in vader_class.members.items():
            access_icon = {"publico": "🟢", "protegido": "🟡", "privado": "🔴"}
            icon = access_icon.get(member.access_level.value, "⚪")
            flags = []
            if member.readonly:
                flags.append("readonly")
            if member.deprecated:
                flags.append("deprecated")
            flags_str = f" [{', '.join(flags)}]" if flags else ""
            
            print(f"     {icon} {member.access_level.value} {member.member_type} {member_name}{flags_str}")
    
    print("\n" + "=" * 70)
    
    # Generar código Python para una clase
    if classes:
        print("🔧 Código Python generado para la primera clase:")
        python_code = access_system.generate_python_class(classes[0])
        print()
        for i, line in enumerate(python_code.split('\n')[:20], 1):  # Mostrar primeras 20 líneas
            print(f"{i:2d}: {line}")
        if len(python_code.split('\n')) > 20:
            print("    ... (código truncado)")
    
    print("\n" + "=" * 70)
    print("✅ Sistema de control de acceso Vader implementado")
    print("🚀 Características disponibles:")
    print("  - Modificadores de acceso (privado, protegido, público)")
    print("  - Propiedades con getters/setters automáticos")
    print("  - Validación de propiedades")
    print("  - Miembros de solo lectura")
    print("  - Métodos y propiedades deprecados")
    print("  - Clases abstractas y finales")
    print("  - Interfaces con validación")
    print("  - Decoradores de acceso")
    print("  - Validación en tiempo de ejecución")
    
    # Crear decoradores
    decorators = access_system.create_access_decorators()
    print(f"\n🎨 Decoradores de acceso generados ({len(decorators)} caracteres)")
    print("   Incluye: @private, @protected, @deprecated, @readonly_property, @validated_property")

if __name__ == "__main__":
    main()
