import json;
import * as sistema_operativo from os;

import json;
import * as sistema_operativo from os;
// desde math importar sqrt
// @property
// @staticmethod
class Animal {
  constructor() {
    this.nombre = null;
    this.edad = null;
}
  hacer_sonido() {
    console.log("El animal hace un sonido");
  }
}
class Perro extends Animal {
  constructor() {
    this.raza = null;
}
  hacer_sonido() {
    console.log("¡Guau! Soy " + this.nombre);
  }
  info_especie() {
    console.log("Los perros son mamíferos");
  }
}
// @staticmethod
async function obtener_datos(url) {
  try {
    resultado = esperar fetch(url);
    datos = esperar resultado.json();
    return datos;
  } catch (error) { // NetworkError
    console.log("Error de red: " + String(error));
    return None;
  } finally {
    console.log("Operación completada");
  }
}
function saludar(nombre = "Invitado", idioma = "es") {
  if (idioma == "es") {
    console.log("¡Hola, " + nombre + "!");
  } else {
    console.log("Hello, " + nombre + "!");
  }
}
let configuracion = {"debug": True, "version": "1.0"};
tupla coordenadas = (10, 20, 30);
let numeros_unicos = {1, 2, 3, 4, 5};
let nombres = ["Ana", "Carlos", "María"];
configuracion["puerto"] = 8080;
configuracion["host"] = "localhost";
numeros_unicos.add(6);
numeros_unicos.add(7);
comprension lista cuadrados = x*x para x en range(1, 6) si x % 2 == 0;
// con open("datos.txt", "w") como archivo
// archivo.write("Datos de prueba")
// fin con
for (let i = 0; i < 5; i++) {
  console.log("Número: " + String(i));
}
for (let nombre of nombres) {
  if (nombre.startswith("A")) {
    console.log("Nombre que empieza con A: " + nombre);
  }
}
contador = 0;
while (contador < 3) {
  console.log("Contador: " + String(contador));
  contador = contador + 1;
}
function numeros_fibonacci() {
  a, b = 0, 1;
  yield a;
  a, b = b, a + b;
}
}
cuadrado = lambda x: x * x;
suma = lambda a, b: a + b;
try {
resultado = 10 / 0;
} catch (error) { // ZeroDivisionError
console.log("No se puede dividir por cero");
} catch (error) {
console.log("Error inesperado: " + String(error));
} finally {
console.log("Limpieza completada");
}
// afirmar len(nombres) > 0 mensaje "La lista no puede estar vacía"
// global contador_global
contador_global = 100;
function main() {
let mi_perro = new Perro();
mi_perro.nombre = "Rex";
mi_perro.edad = 3;
mi_perro.raza = "Labrador";
mi_perro.hacer_sonido();
Perro.info_especie();
saludar("María", "es");
saludar();
console.log("Configuración: " + String(configuracion));
console.log("Coordenadas: " + String(coordenadas));
console.log("Números únicos: " + String(numeros_unicos));
console.log("Cuadrados pares: " + String(cuadrados));
console.log("Cuadrado de 5: " + String(cuadrado(5)));
console.log("Suma de 3 y 7: " + String(suma(3, 7)));
console.log("Demo completado exitosamente");
}
main();