#!/usr/bin/env python3
"""
Vader IoT Runtime - Ejecución nativa de código Vader en dispositivos IoT
Soporta Arduino, Raspberry Pi, ESP32, MicroPython y dispositivos embebidos
"""

import os
import sys
import json
import subprocess
import tempfile
from pathlib import Path
from typing import Dict, List, Optional, Any

class VaderIoTRuntime:
    """Runtime para ejecutar código Vader en dispositivos IoT"""
    
    def __init__(self):
        self.supported_platforms = {
            'arduino': {
                'extension': '.ino',
                'language': 'C++',
                'description': 'Arduino IDE compatible (Uno, Nano, ESP32, etc.)'
            },
            'raspberry-pi': {
                'extension': '.py',
                'language': 'Python',
                'description': 'Raspberry Pi con Python'
            },
            'esp32': {
                'extension': '.ino',
                'language': 'C++',
                'description': 'ESP32 con Arduino Framework'
            },
            'micropython': {
                'extension': '.py',
                'language': 'MicroPython',
                'description': 'MicroPython para microcontroladores'
            },
            'platformio': {
                'extension': '.cpp',
                'language': 'C++',
                'description': 'PlatformIO para desarrollo embebido'
            }
        }
        
        self.iot_components = [
            'led', 'boton', 'sensor', 'motor', 'servo', 'display', 'buzzer',
            'relay', 'potenciometro', 'fotoresistor', 'termistor', 'ultrasonico',
            'acelerometro', 'giroscopio', 'magnetometro', 'presion', 'humedad',
            'temperatura', 'luz', 'sonido', 'movimiento', 'proximidad'
        ]
        
        self.iot_protocols = [
            'wifi', 'bluetooth', 'zigbee', 'lora', 'mqtt', 'http', 'websocket',
            'i2c', 'spi', 'uart', 'can', 'modbus', 'tcp', 'udp'
        ]
        
        self.iot_actions = [
            'encender', 'apagar', 'leer', 'escribir', 'enviar', 'recibir',
            'medir', 'controlar', 'monitorear', 'alertar', 'dormir', 'despertar'
        ]
    
    def detect_iot_components(self, vader_code: str) -> Dict[str, List[str]]:
        """Detectar componentes IoT en el código Vader"""
        detected = {
            'components': [],
            'protocols': [],
            'actions': [],
            'pins': [],
            'sensors': []
        }
        
        lines = vader_code.lower().split('\n')
        
        for line in lines:
            # Detectar componentes
            for component in self.iot_components:
                if component in line:
                    if component not in detected['components']:
                        detected['components'].append(component)
            
            # Detectar protocolos
            for protocol in self.iot_protocols:
                if protocol in line:
                    if protocol not in detected['protocols']:
                        detected['protocols'].append(protocol)
            
            # Detectar acciones
            for action in self.iot_actions:
                if action in line:
                    if action not in detected['actions']:
                        detected['actions'].append(action)
            
            # Detectar pines
            if 'pin' in line:
                pin_num = self.extract_pin_number(line)
                if pin_num and pin_num not in detected['pins']:
                    detected['pins'].append(pin_num)
            
            # Detectar sensores específicos
            if 'sensor' in line:
                sensor_type = self.extract_sensor_type(line)
                if sensor_type and sensor_type not in detected['sensors']:
                    detected['sensors'].append(sensor_type)
        
        return detected
    
    def extract_pin_number(self, line: str) -> Optional[str]:
        """Extraer número de pin de una línea"""
        import re
        match = re.search(r'pin\s*(\d+)', line)
        return match.group(1) if match else None
    
    def extract_sensor_type(self, line: str) -> Optional[str]:
        """Extraer tipo de sensor de una línea"""
        for component in self.iot_components:
            if component in line and 'sensor' in line:
                return component
        return None
    
    def generate_arduino_code(self, vader_code: str, components: Dict) -> str:
        """Generar código Arduino desde Vader"""
        includes = [
            "#include <Arduino.h>"
        ]
        
        # Agregar includes específicos según componentes
        if 'wifi' in components['protocols']:
            includes.append("#include <WiFi.h>")
        if 'bluetooth' in components['protocols']:
            includes.append("#include <BluetoothSerial.h>")
        if 'mqtt' in components['protocols']:
            includes.append("#include <PubSubClient.h>")
        if 'display' in components['components']:
            includes.append("#include <LiquidCrystal.h>")
        if 'servo' in components['components']:
            includes.append("#include <Servo.h>")
        if 'ultrasonico' in components['components']:
            includes.append("#include <NewPing.h>")
        
        code_lines = includes + [""]
        
        # Definir constantes y variables
        code_lines.extend([
            "// Definiciones de pines y constantes",
            "// Generado automáticamente desde código Vader",
            ""
        ])
        
        # Definir pines según componentes detectados
        pin_counter = 2  # Empezar desde pin 2
        pin_definitions = {}
        
        for component in components['components']:
            if component in ['led', 'relay', 'buzzer']:
                pin_definitions[component] = pin_counter
                code_lines.append(f"#define {component.upper()}_PIN {pin_counter}")
                pin_counter += 1
            elif component in ['boton', 'sensor']:
                pin_definitions[component] = pin_counter
                code_lines.append(f"#define {component.upper()}_PIN {pin_counter}")
                pin_counter += 1
        
        code_lines.append("")
        
        # Variables globales
        code_lines.extend([
            "// Variables globales",
            "bool systemRunning = true;",
            "unsigned long lastUpdate = 0;",
            "const unsigned long UPDATE_INTERVAL = 1000; // 1 segundo",
            ""
        ])
        
        # Función setup
        code_lines.extend([
            "void setup() {",
            "  // Inicialización del sistema",
            "  Serial.begin(115200);",
            "  Serial.println(\"Iniciando dispositivo Vader IoT...\");",
            ""
        ])
        
        # Configurar pines según componentes
        for component, pin in pin_definitions.items():
            if component in ['led', 'relay', 'buzzer']:
                code_lines.append(f"  pinMode({component.upper()}_PIN, OUTPUT);")
            elif component in ['boton', 'sensor']:
                code_lines.append(f"  pinMode({component.upper()}_PIN, INPUT);")
        
        # Inicialización específica
        if 'wifi' in components['protocols']:
            code_lines.extend([
                "",
                "  // Configuración WiFi",
                "  WiFi.begin(\"SSID\", \"PASSWORD\");",
                "  while (WiFi.status() != WL_CONNECTED) {",
                "    delay(1000);",
                "    Serial.println(\"Conectando a WiFi...\");",
                "  }",
                "  Serial.println(\"WiFi conectado!\");"
            ])
        
        code_lines.extend([
            "",
            "  Serial.println(\"Sistema inicializado correctamente\");",
            "}",
            ""
        ])
        
        # Función loop principal
        code_lines.extend([
            "void loop() {",
            "  unsigned long currentTime = millis();",
            "  ",
            "  if (currentTime - lastUpdate >= UPDATE_INTERVAL) {",
            "    lastUpdate = currentTime;",
            "    ",
            "    // Lógica principal generada desde Vader"
        ])
        
        # Procesar código Vader
        vader_lines = vader_code.split('\n')
        for line in vader_lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            arduino_line = self.convert_vader_to_arduino(line, components, pin_definitions)
            if arduino_line:
                code_lines.append(f"    {arduino_line}")
        
        code_lines.extend([
            "  }",
            "  ",
            "  // Pequeña pausa para no saturar el procesador",
            "  delay(10);",
            "}"
        ])
        
        # Funciones auxiliares
        code_lines.extend([
            "",
            "// Funciones auxiliares generadas automáticamente",
            "",
            "void encenderLed(int pin) {",
            "  digitalWrite(pin, HIGH);",
            "  Serial.println(\"LED encendido en pin \" + String(pin));",
            "}",
            "",
            "void apagarLed(int pin) {",
            "  digitalWrite(pin, LOW);",
            "  Serial.println(\"LED apagado en pin \" + String(pin));",
            "}",
            "",
            "int leerSensor(int pin) {",
            "  int valor = analogRead(pin);",
            "  Serial.println(\"Sensor pin \" + String(pin) + \": \" + String(valor));",
            "  return valor;",
            "}",
            "",
            "void enviarDatos(String datos) {",
            "  Serial.println(\"Enviando: \" + datos);",
            "  // Implementar envío según protocolo configurado",
            "}"
        ])
        
        return '\n'.join(code_lines)
    
    def generate_raspberry_pi_code(self, vader_code: str, components: Dict) -> str:
        """Generar código Python para Raspberry Pi desde Vader"""
        imports = [
            "#!/usr/bin/env python3",
            "# Código Raspberry Pi generado automáticamente desde Vader",
            "",
            "import time",
            "import sys",
            "import json",
            "from datetime import datetime"
        ]
        
        # Agregar imports específicos
        if any(comp in components['components'] for comp in ['led', 'boton', 'sensor']):
            imports.append("import RPi.GPIO as GPIO")
        if 'wifi' in components['protocols'] or 'http' in components['protocols']:
            imports.append("import requests")
        if 'mqtt' in components['protocols']:
            imports.append("import paho.mqtt.client as mqtt")
        if 'bluetooth' in components['protocols']:
            imports.append("import bluetooth")
        if any(sensor in components['components'] for sensor in ['temperatura', 'humedad']):
            imports.append("import Adafruit_DHT")
        
        code_lines = imports + [
            "",
            "class VaderIoTDevice:",
            "    \"\"\"Dispositivo IoT controlado por Vader\"\"\"",
            "    ",
            "    def __init__(self):",
            "        self.running = True",
            "        self.setup_gpio()",
            "        self.setup_protocols()",
            "        print('Dispositivo Vader IoT inicializado')",
            "    ",
            "    def setup_gpio(self):",
            "        \"\"\"Configurar pines GPIO\"\"\"",
            "        GPIO.setmode(GPIO.BCM)",
            "        GPIO.setwarnings(False)",
            "        "
        ]
        
        # Configurar pines según componentes
        pin_counter = 18  # Empezar desde GPIO 18
        pin_definitions = {}
        
        for component in components['components']:
            if component in ['led', 'relay', 'buzzer']:
                pin_definitions[component] = pin_counter
                code_lines.append(f"        self.{component}_pin = {pin_counter}")
                code_lines.append(f"        GPIO.setup(self.{component}_pin, GPIO.OUT)")
                pin_counter += 1
            elif component in ['boton', 'sensor']:
                pin_definitions[component] = pin_counter
                code_lines.append(f"        self.{component}_pin = {pin_counter}")
                code_lines.append(f"        GPIO.setup(self.{component}_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)")
                pin_counter += 1
        
        code_lines.extend([
            "    ",
            "    def setup_protocols(self):",
            "        \"\"\"Configurar protocolos de comunicación\"\"\"",
        ])
        
        # Configurar protocolos
        if 'mqtt' in components['protocols']:
            code_lines.extend([
                "        self.mqtt_client = mqtt.Client()",
                "        self.mqtt_client.on_connect = self.on_mqtt_connect",
                "        self.mqtt_client.on_message = self.on_mqtt_message",
                "        # self.mqtt_client.connect('broker.hivemq.com', 1883, 60)",
            ])
        
        code_lines.extend([
            "        pass",
            "    ",
            "    def run(self):",
            "        \"\"\"Ejecutar lógica principal\"\"\"",
            "        try:",
            "            while self.running:",
            "                self.update()",
            "                time.sleep(1)",
            "        except KeyboardInterrupt:",
            "            print('\\nDeteniendo dispositivo...')",
            "        finally:",
            "            self.cleanup()",
            "    ",
            "    def update(self):",
            "        \"\"\"Actualización principal - lógica desde Vader\"\"\"",
        ])
        
        # Procesar código Vader
        vader_lines = vader_code.split('\n')
        for line in vader_lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            pi_line = self.convert_vader_to_raspberry_pi(line, components, pin_definitions)
            if pi_line:
                code_lines.append(f"        {pi_line}")
        
        # Métodos auxiliares
        code_lines.extend([
            "    ",
            "    def encender_led(self, pin=None):",
            "        \"\"\"Encender LED\"\"\"",
            "        pin = pin or self.led_pin if hasattr(self, 'led_pin') else 18",
            "        GPIO.output(pin, GPIO.HIGH)",
            "        print(f'LED encendido en pin {pin}')",
            "    ",
            "    def apagar_led(self, pin=None):",
            "        \"\"\"Apagar LED\"\"\"",
            "        pin = pin or self.led_pin if hasattr(self, 'led_pin') else 18",
            "        GPIO.output(pin, GPIO.LOW)",
            "        print(f'LED apagado en pin {pin}')",
            "    ",
            "    def leer_sensor(self, pin=None):",
            "        \"\"\"Leer valor de sensor\"\"\"",
            "        pin = pin or self.sensor_pin if hasattr(self, 'sensor_pin') else 19",
            "        # Para sensores analógicos necesitarías un ADC como MCP3008",
            "        valor = GPIO.input(pin)",
            "        print(f'Sensor pin {pin}: {valor}')",
            "        return valor",
            "    ",
            "    def enviar_datos(self, datos):",
            "        \"\"\"Enviar datos por protocolo configurado\"\"\"",
            "        print(f'Enviando datos: {datos}')",
            "        # Implementar según protocolo (MQTT, HTTP, etc.)",
            "    ",
            "    def cleanup(self):",
            "        \"\"\"Limpiar recursos\"\"\"",
            "        GPIO.cleanup()",
            "        print('Recursos liberados')",
            "",
            "def main():",
            "    \"\"\"Función principal\"\"\"",
            "    device = VaderIoTDevice()",
            "    device.run()",
            "",
            "if __name__ == '__main__':",
            "    main()"
        ])
        
        return '\n'.join(code_lines)
    
    def convert_vader_to_arduino(self, line: str, components: Dict, pins: Dict) -> Optional[str]:
        """Convertir línea de Vader a código Arduino"""
        line = line.strip().lower()
        
        if 'encender led' in line:
            return "encenderLed(LED_PIN);"
        elif 'apagar led' in line:
            return "apagarLed(LED_PIN);"
        elif 'leer sensor' in line:
            return "int sensorValue = leerSensor(SENSOR_PIN);"
        elif line.startswith('mostrar '):
            content = line.replace('mostrar ', '', 1)
            return f'Serial.println("{content}");'
        elif 'dormir' in line:
            return "delay(1000);"
        elif 'enviar' in line:
            return 'enviarDatos("datos");'
        
        return None
    
    def convert_vader_to_raspberry_pi(self, line: str, components: Dict, pins: Dict) -> Optional[str]:
        """Convertir línea de Vader a código Raspberry Pi"""
        line = line.strip().lower()
        
        if 'encender led' in line:
            return "self.encender_led()"
        elif 'apagar led' in line:
            return "self.apagar_led()"
        elif 'leer sensor' in line:
            return "sensor_value = self.leer_sensor()"
        elif line.startswith('mostrar '):
            content = line.replace('mostrar ', '', 1)
            return f'print("{content}")'
        elif 'dormir' in line:
            return "time.sleep(1)"
        elif 'enviar' in line:
            return 'self.enviar_datos("datos")'
        
        return None
    
    def generate_project_structure(self, platform: str, project_name: str) -> Dict[str, str]:
        """Generar estructura de proyecto IoT"""
        structure = {}
        
        if platform == 'arduino':
            structure = {
                f'{project_name}.ino': '',  # Código principal
                'README.md': self.generate_iot_readme(platform, project_name),
                'platformio.ini': self.generate_platformio_config(),
                'lib/README.md': 'Librerías adicionales para el proyecto'
            }
        elif platform == 'raspberry-pi':
            structure = {
                'main.py': '',  # Código principal
                'requirements.txt': self.generate_pi_requirements(),
                'README.md': self.generate_iot_readme(platform, project_name),
                'config.json': self.generate_pi_config(),
                'systemd/vader-iot.service': self.generate_systemd_service(project_name)
            }
        elif platform == 'esp32':
            structure = {
                f'{project_name}.ino': '',  # Código principal
                'README.md': self.generate_iot_readme(platform, project_name),
                'platformio.ini': self.generate_esp32_platformio_config(),
                'data/config.json': '{"wifi_ssid": "", "wifi_password": ""}'
            }
        
        return structure
    
    def generate_platformio_config(self) -> str:
        """Generar configuración PlatformIO"""
        return """[env:uno]
platform = atmelavr
board = uno
framework = arduino

[env:esp32]
platform = espressif32
board = esp32dev
framework = arduino
monitor_speed = 115200

lib_deps = 
    WiFi
    PubSubClient
    ArduinoJson"""
    
    def generate_esp32_platformio_config(self) -> str:
        """Generar configuración PlatformIO para ESP32"""
        return """[env:esp32dev]
platform = espressif32
board = esp32dev
framework = arduino
monitor_speed = 115200

lib_deps = 
    WiFi
    PubSubClient
    ArduinoJson
    WebServer
    SPIFFS"""
    
    def generate_pi_requirements(self) -> str:
        """Generar requirements.txt para Raspberry Pi"""
        return """RPi.GPIO>=0.7.1
paho-mqtt>=1.6.0
requests>=2.28.0
Adafruit-DHT>=1.4.0
adafruit-circuitpython-dht>=3.7.0
board>=1.0
digitalio>=3.3.0"""
    
    def generate_pi_config(self) -> str:
        """Generar configuración JSON para Raspberry Pi"""
        return json.dumps({
            "device_name": "vader_iot_device",
            "update_interval": 1000,
            "mqtt": {
                "broker": "broker.hivemq.com",
                "port": 1883,
                "topic": "vader/iot/data"
            },
            "gpio": {
                "led_pin": 18,
                "button_pin": 19,
                "sensor_pin": 20
            }
        }, indent=2)
    
    def generate_systemd_service(self, project_name: str) -> str:
        """Generar servicio systemd para Raspberry Pi"""
        return f"""[Unit]
Description=Vader IoT Device - {project_name}
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/{project_name}
ExecStart=/usr/bin/python3 /home/pi/{project_name}/main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target"""
    
    def generate_iot_readme(self, platform: str, project_name: str) -> str:
        """Generar README para proyecto IoT"""
        return f"""# {project_name} - Vader IoT

Proyecto IoT generado automáticamente con Vader Runtime.

## Plataforma: {platform.title()}

### Hardware Requerido

{"- Arduino Uno/Nano/ESP32" if platform == "arduino" else "- Raspberry Pi 3/4"}
- LEDs, resistencias, sensores según el código
- Cables jumper y protoboard
- Fuente de alimentación

### Instalación

```bash
{"# Abrir en Arduino IDE o PlatformIO" if platform == "arduino" else "# Instalar dependencias"}
{"# Conectar dispositivo y subir código" if platform == "arduino" else "pip install -r requirements.txt"}
{"" if platform == "arduino" else "# Ejecutar"}
{"" if platform == "arduino" else "python3 main.py"}
```

### Configuración

{"Configurar WiFi y otros parámetros en el código principal." if platform == "arduino" else "Editar config.json con tus parámetros específicos."}

### Características

- ✅ Generado automáticamente desde código Vader
- ✅ Soporte para componentes IoT estándar
- ✅ Protocolos de comunicación integrados
- ✅ Configuración lista para producción

### Uso

```bash
# Regenerar desde Vader
vader generate iot mi_codigo.vdr --platform {platform}

# Monitorear dispositivo
{"# Usar monitor serie de Arduino IDE" if platform == "arduino" else "journalctl -u vader-iot -f"}
```

### Componentes Detectados

El sistema detectó automáticamente los siguientes componentes en tu código Vader:
- LEDs, sensores, botones, etc.
- Protocolos de comunicación (WiFi, MQTT, etc.)
- Acciones específicas del dispositivo

### Troubleshooting

{"- Verificar conexiones de hardware" if platform == "arduino" else "- Verificar permisos GPIO: sudo usermod -a -G gpio $USER"}
{"- Revisar configuración de pines" if platform == "arduino" else "- Verificar configuración de red"}
{"- Comprobar librerías instaladas" if platform == "arduino" else "- Revisar logs: journalctl -u vader-iot"}
"""
    
    def run_vader_iot(self, vader_code: str, platform: str, output_dir: str = './iot_device') -> bool:
        """Ejecutar código Vader en runtime IoT"""
        try:
            print(f"🔌 Ejecutando Vader IoT Runtime para {platform}...")
            
            # Detectar componentes IoT
            components = self.detect_iot_components(vader_code)
            
            print(f"🔍 Componentes IoT detectados:")
            print(f"  🔧 Componentes: {len(components['components'])} ({', '.join(components['components'])})")
            print(f"  📡 Protocolos: {len(components['protocols'])} ({', '.join(components['protocols'])})")
            print(f"  ⚡ Acciones: {len(components['actions'])} ({', '.join(components['actions'])})")
            print(f"  📌 Pines: {len(components['pins'])} ({', '.join(components['pins'])})")
            
            # Crear directorio de salida
            Path(output_dir).mkdir(parents=True, exist_ok=True)
            
            # Generar código específico de la plataforma
            if platform == 'arduino':
                iot_code = self.generate_arduino_code(vader_code, components)
                main_file = f'{Path(output_dir).name}.ino'
            elif platform == 'raspberry-pi':
                iot_code = self.generate_raspberry_pi_code(vader_code, components)
                main_file = 'main.py'
            elif platform == 'esp32':
                iot_code = self.generate_arduino_code(vader_code, components)  # ESP32 usa Arduino framework
                main_file = f'{Path(output_dir).name}.ino'
            else:
                print(f"❌ Plataforma {platform} no soportada")
                return False
            
            # Generar estructura de proyecto
            project_name = Path(output_dir).name
            structure = self.generate_project_structure(platform, project_name)
            
            # Escribir archivos
            for file_path, content in structure.items():
                full_path = Path(output_dir) / file_path
                full_path.parent.mkdir(parents=True, exist_ok=True)
                
                if file_path.endswith(main_file.split('/')[-1]) or file_path == main_file:
                    content = iot_code
                
                with open(full_path, 'w', encoding='utf-8') as f:
                    f.write(content)
            
            print(f"✅ Dispositivo IoT generado en {output_dir}")
            print(f"📁 Archivos principales:")
            for file_path in structure.keys():
                print(f"  - {file_path}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error en IoT Runtime: {e}")
            return False

def main():
    """Función principal para testing"""
    runtime = VaderIoTRuntime()
    
    # Código Vader de ejemplo
    vader_code = """# Dispositivo IoT de ejemplo
nombre_dispositivo = "Sensor Inteligente"

# Componentes
led_estado = "pin 13"
boton_control = "pin 2"
sensor_temperatura = "pin A0"
sensor_humedad = "pin A1"

# Protocolos
usar wifi
usar mqtt

# Lógica principal
encender led
leer sensor temperatura
leer sensor humedad

si temperatura mayor que 25 entonces
    encender led
    enviar alerta "Temperatura alta"
sino
    apagar led
fin si

dormir 5 segundos
"""
    
    print("🧪 PROBANDO VADER IOT RUNTIME")
    print("=" * 50)
    
    # Probar Arduino
    success_arduino = runtime.run_vader_iot(vader_code, 'arduino', './test_arduino_device')
    
    # Probar Raspberry Pi
    success_pi = runtime.run_vader_iot(vader_code, 'raspberry-pi', './test_pi_device')
    
    # Probar ESP32
    success_esp32 = runtime.run_vader_iot(vader_code, 'esp32', './test_esp32_device')
    
    if success_arduino and success_pi and success_esp32:
        print("\n🎉 IOT RUNTIME FUNCIONAL - Todas las plataformas generadas exitosamente")
        return True
    else:
        print("\n❌ Algunos runtimes fallaron")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
