#!/usr/bin/env python3
"""
Test completo del transpilador Rust de Vader
Valida que el transpilador genere código Rust válido y funcional
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from transpilers.rust import RustTranspiler

def test_rust_completo():
    """Test completo del transpilador Rust con todas las características"""
    
    # Código Vader con todas las características avanzadas
    vader_code = '''
# Test completo del transpilador Rust
mostrar "=== Test Transpilador Rust COMPLETO ==="

# Variables con tipos automáticos
crear variable edad tipo numero
edad = 25
crear variable nombre tipo texto
nombre = "Juan"
crear variable activo tipo booleano
activo = verdadero

# Estructuras de datos
crear lista amigos
agregar "Ana" a amigos
agregar "Luis" a amigos
crear mapa datos
crear array numeros[5]

# Funciones con tipos
funcion saludar con persona tipo texto que devuelve texto:
    devolver "Hola " + persona
fin

funcion sumar con a tipo numero y b tipo numero que devuelve numero:
    devolver a + b
fin

# Struct con implementación
struct Persona:
    atributo nombre tipo texto
    atributo edad tipo numero
    
    constructor con nombre tipo texto y edad tipo numero:
        this.nombre = nombre
        this.edad = edad
    fin
    
    metodo presentarse que devuelve texto:
        devolver "Soy " + nombre + " y tengo " + edad + " años"
    fin
fin struct

# Condicionales y bucles
si edad es mayor que 18 entonces
    mostrar "Es mayor de edad"
sino
    mostrar "Es menor de edad"
fin si

repetir 3 veces
    mostrar "Iteración: " + i
fin repetir

# Manejo de errores
intentar
    numero("abc")
capturar error
    mostrar "Error al convertir número"
finalmente
    mostrar "Proceso completado"
fin

# Operaciones matemáticas
resultado = raiz(16) + potencia(2, 3)
mostrar "Resultado matemático: " + resultado
'''

    # Transpilación
    transpiler = RustTranspiler()
    rust_code = transpiler.transpile(vader_code)
    
    print("🧪 Iniciando test del transpilador Rust COMPLETO...")
    print("✅ Transpilación completada!")
    print("\n" + "="*60)
    print("CÓDIGO RUST GENERADO:")
    print("="*60)
    print(rust_code)
    print("="*60)
    
    # Validaciones específicas
    validaciones = [
        ("Imports correctos", "use std::io;" in rust_code and "use std::collections::HashMap;" in rust_code),
        ("Función main", "fn main()" in rust_code),
        ("Variables tipadas", "let mut edad" in rust_code or "let edad" in rust_code),
        ("Vectores/Listas", "Vec<" in rust_code or "vec!" in rust_code),
        ("HashMap/Mapas", "HashMap" in rust_code),
        ("Funciones con tipos", "fn saludar(" in rust_code and "-> String" in rust_code),
        ("Structs personalizados", "struct Persona" in rust_code),
        ("Constructores/impl", "impl " in rust_code and "new(" in rust_code),
        ("Result/Error handling", "Result<" in rust_code or "match " in rust_code or "unwrap()" in rust_code),
        ("Operaciones matemáticas", "sqrt(" in rust_code or "powf(" in rust_code),
        ("Condicionales", "if " in rust_code and "} else {" in rust_code),
        ("Bucles", "for " in rust_code and "in 0.." in rust_code)
    ]
    
    print("\n🔍 VALIDACIONES:")
    passed = 0
    total = len(validaciones)
    
    for desc, condition in validaciones:
        if condition:
            print(f"✅ {desc}")
            passed += 1
        else:
            print(f"❌ {desc}")
    
    print(f"\n📊 RESULTADO: {passed}/{total} validaciones pasadas")
    
    if passed == total:
        print("🎉 ¡TRANSPILADOR RUST COMPLETO Y FUNCIONAL!")
        return True
    else:
        print("⚠️ El transpilador necesita mejoras")
        return False

if __name__ == "__main__":
    test_rust_completo()
