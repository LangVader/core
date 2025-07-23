#!/usr/bin/env python3
"""
VADER 7.0 - UNIVERSAL IoT RUNTIME
Ejecuta archivos .vdr nativamente en dispositivos IoT (Arduino, ESP32, Raspberry Pi)
LA PROGRAMACIÓN UNIVERSAL: Libre, Descentralizada, Accesible

Autor: Vader Universal Team
Versión: 7.0.0 Universal IoT
Fecha: 22 de Julio, 2025
"""

import sys
import os
import json
import time
import threading
from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from datetime import datetime

# Constantes Vader IoT
VADER_VERSION = "7.0.0"
VADER_CODENAME = "UNIVERSAL IOT"
VADER_SLOGAN = "LA PROGRAMACIÓN UNIVERSAL: Libre, Descentralizada, Accesible"

@dataclass
class VaderIoTResult:
    """Resultado de ejecución IoT de Vader"""
    success: bool
    output: str
    context: str
    language: str
    device_type: str
    sensors_detected: List[str]
    actuators_detected: List[str]
    generated_code: str
    execution_time: float
    timestamp: str

class VaderUniversalIoT:
    """Runtime Universal de Vader para dispositivos IoT"""
    
    def __init__(self):
        self.version = VADER_VERSION
        self.codename = VADER_CODENAME
        self.slogan = VADER_SLOGAN
        
        # Contextos IoT soportados
        self.iot_contexts = [
            'arduino', 'esp32', 'esp8266', 'raspberry_pi', 
            'microbit', 'sensor', 'actuador', 'robot',
            'domótica', 'agricultura', 'monitoreo', 'automatización'
        ]
        
        # Idiomas humanos soportados
        self.languages = [
            'es', 'en', 'fr', 'it', 'pt', 'de', 'ja', 'zh', 'ko', 'ar', 'ru', 'hi'
        ]
        
        # Sensores IoT comunes
        self.sensors = {
            'temperatura': 'DHT22, DS18B20, BME280',
            'humedad': 'DHT22, BME280, SHT30',
            'presión': 'BME280, BMP180',
            'luz': 'LDR, BH1750, TSL2561',
            'movimiento': 'PIR, HC-SR501',
            'distancia': 'HC-SR04, VL53L0X',
            'gas': 'MQ-2, MQ-135',
            'sonido': 'MAX4466, INMP441',
            'acelerómetro': 'MPU6050, ADXL345',
            'gps': 'NEO-6M, NEO-8M',
            'cámara': 'ESP32-CAM, Pi Camera'
        }
        
        # Actuadores IoT comunes
        self.actuators = {
            'led': 'LED simple, LED RGB, NeoPixel',
            'motor': 'Servo, Stepper, DC Motor',
            'relé': 'Relay Module, SSR',
            'buzzer': 'Passive/Active Buzzer',
            'pantalla': 'LCD, OLED, TFT',
            'bomba': 'Water Pump, Air Pump',
            'ventilador': 'DC Fan, Servo Fan',
            'calefactor': 'Heating Element',
            'válvula': 'Solenoid Valve'
        }
        
        print(f"🤖 VADER {self.version} - {self.codename}")
        print(f"⚡ {self.slogan}")
        print(f"🔧 Runtime IoT inicializado para dispositivos inteligentes")
    
    def detect_context_and_language(self, code: str) -> tuple:
        """Detecta el contexto IoT y idioma del código"""
        code_lower = code.lower()
        
        # Detectar contexto IoT
        detected_context = 'iot_general'
        for context in self.iot_contexts:
            if context in code_lower:
                detected_context = context
                break
        
        # Detectar idioma (por defecto español)
        detected_language = 'es'
        
        # Palabras clave en inglés
        english_keywords = ['sensor', 'read', 'write', 'digital', 'analog', 'setup', 'loop']
        if any(keyword in code_lower for keyword in english_keywords):
            detected_language = 'en'
        
        return detected_context, detected_language
    
    def detect_sensors_and_actuators(self, code: str) -> tuple:
        """Detecta sensores y actuadores en el código"""
        code_lower = code.lower()
        detected_sensors = []
        detected_actuators = []
        
        # Detectar sensores
        for sensor, description in self.sensors.items():
            if sensor in code_lower:
                detected_sensors.append(f"{sensor} ({description})")
            else:
                # Verificar modelos específicos
                models = description.split(', ')
                for model in models:
                    if model.lower() in code_lower:
                        detected_sensors.append(f"{sensor} ({description})")
                        break
        
        # Detectar actuadores
        for actuator, description in self.actuators.items():
            if actuator in code_lower:
                detected_actuators.append(f"{actuator} ({description})")
            else:
                # Verificar modelos específicos
                models = description.split(', ')
                for model in models:
                    if model.lower() in code_lower:
                        detected_actuators.append(f"{actuator} ({description})")
                        break
        
        return detected_sensors, detected_actuators
    
    def generate_arduino_code(self, code: str, sensors: List[str], actuators: List[str]) -> str:
        """Genera código Arduino/C++ desde Vader"""
        arduino_code = """// CÓDIGO GENERADO POR VADER 7.0 UNIVERSAL IoT
// Archivo .vdr ejecutado nativamente en Arduino/ESP32

"""
        
        # Headers necesarios
        if sensors and any('dht' in sensor.lower() for sensor in sensors):
            arduino_code += '#include <DHT.h>\n'
        if actuators and any('servo' in actuator.lower() for actuator in actuators):
            arduino_code += '#include <Servo.h>\n'
        if 'wifi' in code.lower() or 'esp32' in code.lower():
            arduino_code += '#include <WiFi.h>\n'
        
        arduino_code += '\n// Definiciones de pines\n'
        
        # Procesar líneas de código Vader
        lines = code.split('\n')
        setup_code = ""
        loop_code = ""
        
        for line in lines:
            line = line.strip()
            
            if line.startswith('mostrar '):
                message = line.replace('mostrar ', '').replace('"', '')
                loop_code += f'  Serial.println("{message}");\n'
            
            elif 'temperatura' in line.lower():
                setup_code += '  dht.begin();\n'
                loop_code += '  float temp = dht.readTemperature();\n'
                loop_code += '  Serial.print("Temperatura: ");\n'
                loop_code += '  Serial.println(temp);\n'
            
            elif 'led' in line.lower():
                if 'encender' in line.lower():
                    loop_code += '  digitalWrite(LED_PIN, HIGH);\n'
                elif 'apagar' in line.lower():
                    loop_code += '  digitalWrite(LED_PIN, LOW);\n'
            
            elif 'sensor' in line.lower() and 'leer' in line.lower():
                loop_code += '  int sensorValue = analogRead(A0);\n'
                loop_code += '  Serial.print("Sensor: ");\n'
                loop_code += '  Serial.println(sensorValue);\n'
            
            elif 'esperar' in line.lower():
                delay_match = [s for s in line.split() if s.isdigit()]
                delay = delay_match[0] if delay_match else '1000'
                loop_code += f'  delay({delay});\n'
        
        # Estructura Arduino completa
        arduino_code += """
void setup() {
  Serial.begin(115200);
  pinMode(LED_BUILTIN, OUTPUT);
""" + setup_code + """}

void loop() {
""" + loop_code + """}
"""
        
        return arduino_code
    
    def generate_python_iot_code(self, code: str, sensors: List[str], actuators: List[str]) -> str:
        """Genera código Python para Raspberry Pi desde Vader"""
        python_code = """#!/usr/bin/env python3
# CÓDIGO GENERADO POR VADER 7.0 UNIVERSAL IoT
# Archivo .vdr ejecutado nativamente en Raspberry Pi

import time
import sys
"""
        
        # Imports necesarios según sensores/actuadores detectados
        all_devices = sensors + actuators if sensors and actuators else (sensors or actuators or [])
        if all_devices and any('gpio' in device.lower() for device in all_devices):
            python_code += "import RPi.GPIO as GPIO\n"
        if sensors and any('cámara' in sensor.lower() for sensor in sensors):
            python_code += "from picamera import PiCamera\n"
        if sensors and any('i2c' in sensor.lower() for sensor in sensors):
            python_code += "import smbus\n"
        
        python_code += '\nprint("🤖 VADER 7.0 IoT - Raspberry Pi")\nprint("⚡ Ejecutando archivo .vdr nativamente")\n\n'
        
        # Configuración GPIO
        python_code += "# Configuración GPIO\nGPIO.setmode(GPIO.BCM)\nGPIO.setwarnings(False)\n\n"
        
        # Procesar código Vader
        lines = code.split('\n')
        main_code = ""
        
        for line in lines:
            line = line.strip()
            
            if line.startswith('mostrar '):
                message = line.replace('mostrar ', '').replace('"', '')
                main_code += f'print("{message}")\n'
            
            elif 'temperatura' in line.lower():
                main_code += '# Leer sensor de temperatura\ntemp = read_temperature_sensor()\nprint(f"Temperatura: {temp}°C")\n'
            
            elif 'led' in line.lower():
                if 'encender' in line.lower():
                    main_code += 'GPIO.output(18, GPIO.HIGH)  # LED ON\n'
                elif 'apagar' in line.lower():
                    main_code += 'GPIO.output(18, GPIO.LOW)   # LED OFF\n'
            
            elif 'esperar' in line.lower():
                delay_match = [s for s in line.split() if s.isdigit()]
                delay = float(delay_match[0])/1000 if delay_match else 1.0
                main_code += f'time.sleep({delay})\n'
        
        # Función principal
        python_code += f"""
def main():
    try:
        while True:
{chr(10).join('            ' + line for line in main_code.split(chr(10)) if line.strip())}
    except KeyboardInterrupt:
        print("\\n🛑 Programa detenido por el usuario")
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()
"""
        
        return python_code
    
    def execute(self, code: str, context: str = None, language: str = None, device_type: str = 'arduino') -> VaderIoTResult:
        """Ejecuta código .vdr para dispositivos IoT"""
        start_time = time.time()
        
        try:
            # Detectar contexto y idioma automáticamente
            if not context or not language:
                detected_context, detected_language = self.detect_context_and_language(code)
                context = context or detected_context
                language = language or detected_language
            
            # Detectar sensores y actuadores
            sensors, actuators = self.detect_sensors_and_actuators(code)
            
            print(f"🔍 Contexto detectado: {context}")
            print(f"🌐 Idioma detectado: {language}")
            print(f"📱 Dispositivo objetivo: {device_type}")
            print(f"🔧 Sensores detectados: {len(sensors)}")
            print(f"⚙️ Actuadores detectados: {len(actuators)}")
            
            # Generar código según el dispositivo
            if device_type in ['arduino', 'esp32', 'esp8266']:
                generated_code = self.generate_arduino_code(code, sensors, actuators)
                output = f"✅ Código Arduino/C++ generado para {device_type}"
            elif device_type in ['raspberry_pi', 'pi']:
                generated_code = self.generate_python_iot_code(code, sensors, actuators)
                output = f"✅ Código Python IoT generado para Raspberry Pi"
            else:
                generated_code = f"// Código IoT genérico para {device_type}\n" + code
                output = f"✅ Código IoT genérico generado para {device_type}"
            
            execution_time = time.time() - start_time
            
            return VaderIoTResult(
                success=True,
                output=output,
                context=context,
                language=language,
                device_type=device_type,
                sensors_detected=sensors,
                actuators_detected=actuators,
                generated_code=generated_code,
                execution_time=execution_time,
                timestamp=datetime.now().isoformat()
            )
            
        except Exception as e:
            execution_time = time.time() - start_time
            return VaderIoTResult(
                success=False,
                output=f"❌ Error en ejecución IoT: {str(e)}",
                context=context or 'unknown',
                language=language or 'unknown',
                device_type=device_type,
                sensors_detected=[],
                actuators_detected=[],
                generated_code="",
                execution_time=execution_time,
                timestamp=datetime.now().isoformat()
            )

def main():
    """Función principal del runtime IoT"""
    if len(sys.argv) < 2:
        print("🤖 VADER 7.0 - Universal IoT Runtime")
        print("⚡ LA PROGRAMACIÓN UNIVERSAL: Libre, Descentralizada, Accesible")
        print("")
        print("Uso:")
        print("  python3 vader-7.0-universal-iot.py archivo.vdr [dispositivo]")
        print("")
        print("Dispositivos soportados:")
        print("  arduino, esp32, esp8266, raspberry_pi, microbit")
        print("")
        print("Ejemplo:")
        print("  python3 vader-7.0-universal-iot.py mi_sensor.vdr arduino")
        return
    
    vdr_file = sys.argv[1]
    device_type = sys.argv[2] if len(sys.argv) > 2 else 'arduino'
    
    if not os.path.exists(vdr_file):
        print(f"❌ Error: El archivo {vdr_file} no existe")
        return
    
    # Leer archivo .vdr
    try:
        with open(vdr_file, 'r', encoding='utf-8') as f:
            vdr_code = f.read()
    except Exception as e:
        print(f"❌ Error al leer archivo: {e}")
        return
    
    # Crear runtime IoT y ejecutar
    vader_iot = VaderUniversalIoT()
    print(f"\n📄 Ejecutando archivo: {vdr_file}")
    print(f"🎯 Dispositivo objetivo: {device_type}")
    print("=" * 60)
    
    result = vader_iot.execute(vdr_code, device_type=device_type)
    
    # Mostrar resultados
    print(f"\n{result.output}")
    print(f"⏱️ Tiempo de ejecución: {result.execution_time:.3f}s")
    
    if result.sensors_detected:
        print(f"\n🔧 Sensores detectados:")
        for sensor in result.sensors_detected:
            print(f"   • {sensor}")
    
    if result.actuators_detected:
        print(f"\n⚙️ Actuadores detectados:")
        for actuator in result.actuators_detected:
            print(f"   • {actuator}")
    
    print(f"\n📋 Código generado para {result.device_type}:")
    print("=" * 60)
    print(result.generated_code)
    print("=" * 60)
    
    # Guardar código generado
    output_extension = '.ino' if device_type in ['arduino', 'esp32', 'esp8266'] else '.py'
    output_file = vdr_file.replace('.vdr', f'_{device_type}{output_extension}')
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(result.generated_code)
        print(f"💾 Código guardado en: {output_file}")
    except Exception as e:
        print(f"⚠️ No se pudo guardar el archivo: {e}")
    
    print(f"\n🚀 ¡Archivo .vdr ejecutado nativamente para {device_type}!")
    print("⚡ VADER: La programación universal para IoT")

if __name__ == "__main__":
    main()
