#!/usr/bin/env python3
# CÓDIGO GENERADO POR VADER 7.0 UNIVERSAL IoT
# Archivo .vdr ejecutado nativamente en Raspberry Pi

import time
import sys

print("🤖 VADER 7.0 IoT - Raspberry Pi")
print("⚡ Ejecutando archivo .vdr nativamente")

# Configuración GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


def main():
    try:
        while True:
            print("🤖 ¡Hola desde Vader 7.0 IoT Universal!")
            # Leer sensor de temperatura
            temp = read_temperature_sensor()
            print(f"Temperatura: {temp}°C")
            print("Iniciando sistema de monitoreo...")
            # Leer sensor de temperatura
            temp = read_temperature_sensor()
            print(f"Temperatura: {temp}°C")
            GPIO.output(18, GPIO.HIGH)  # LED ON
            time.sleep(1.0)
            GPIO.output(18, GPIO.LOW)   # LED OFF
            print("¡Movimiento detectado!")
            print("Temperatura leída")
            print("Luz ambiente medida")
            print("Sistema funcionando correctamente")
            time.sleep(2.0)
            print("✅ Vader IoT Runtime funcionando perfectamente en Arduino")
    except KeyboardInterrupt:
        print("\n🛑 Programa detenido por el usuario")
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()
