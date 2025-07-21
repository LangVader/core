import json
import os as sistema_operativo

import json
import os as sistema_operativo
# desde math importar sqrt
@property
@staticmethod
class Animal:
    def __init__(self):
        self.nombre = None
        self.edad = None
    def hacer_sonido(self):
        print("El animal hace un sonido")


class Perro(Animal):
    def __init__(self):
        self.raza = None
    def hacer_sonido(self):
        print("¡Guau! Soy " + self.nombre)

    def info_especie(self):
        print("Los perros son mamíferos")


@staticmethod
async def obtener_datos(url):
    try:
        resultado = esperar fetch(url)
        datos = esperar resultado.json()
        return datos
    except NetworkError as error:
        print("Error de red: " + str(error))
        return None
    finally:
        print("Operación completada")

def saludar(nombre="Invitado", idioma="es"):
    if idioma == "es":
        print("¡Hola, " + nombre + "!")
    else:
        print("Hello, " + nombre + "!")

configuracion = {"debug": True, "version": "1.0"}
coordenadas = (10, 20, 30)
numeros_unicos = {1, 2, 3, 4, 5}
nombres = ["Ana", "Carlos", "María"]
configuracion["puerto"] = 8080
configuracion["host"] = "localhost"
numeros_unicos.add(6)
numeros_unicos.add(7)
cuadrados = [x*x for x en range(1, 6) if x % 2 == 0]
with open("datos.txt", "w") as archivo:
    # archivo.write("Datos de prueba")
for i in range(0, 5):
    print("Número: " + str(i))
for nombre in nombres:
    if nombre.startswith("A"):
        print("Nombre que empieza con A: " + nombre)
while contador < 3:
    print("Contador: " + str(contador))
def numeros_fibonacci():
    a, b = 0, 1
    yield a
    a, b = b, a + b

cuadrado = lambda x: x * x
suma = lambda a, b: a + b
try:
    resultado = 10 / 0
except ZeroDivisionError as error:
    print("No se puede dividir por cero")
except Exception as error:
    print("Error inesperado: " + str(error))
finally:
    print("Limpieza completada")
assert len(nombres) > 0, "La lista no puede estar vacía"
global contador_global
def main():
mi_perro = Perro()
    mi_perro.nombre = "Rex"
    mi_perro.edad = 3
    mi_perro.raza = "Labrador"
    mi_perro.hacer_sonido()
    Perro.info_especie()
    saludar("María", "es")
    saludar()
    print("Configuración: " + str(configuracion))
    print("Coordenadas: " + str(coordenadas))
    print("Números únicos: " + str(numeros_unicos))
    print("Cuadrados pares: " + str(cuadrados))
    print("Cuadrado de 5: " + str(cuadrado(5)))
    print("Suma de 3 y 7: " + str(suma(3, 7)))
    print("Demo completado exitosamente")

main()