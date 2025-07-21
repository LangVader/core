#!/usr/bin/env python3
"""
🌐 VADER IoT RUNTIME - PRIMERA IMPLEMENTACIÓN MUNDIAL
Runtime de Vader para Internet de las Cosas (IoT)
Soporta sensores, actuadores, comunicación MQTT, dispositivos inteligentes
"""

import asyncio
import json
import time
import logging
from typing import Dict, Any, Optional, List
import paho.mqtt.client as mqtt
import serial
import requests
from datetime import datetime
import threading

# Simulación de librerías IoT (instalar según dispositivo)
try:
    import RPi.GPIO as GPIO  # Raspberry Pi
    RASPBERRY_PI = True
except ImportError:
    RASPBERRY_PI = False

try:
    import board
    import digitalio
    import analogio  # CircuitPython/MicroPython
    CIRCUITPYTHON = True
except ImportError:
    CIRCUITPYTHON = False

class VaderIoTRuntime:
    """Runtime de Vader optimizado para dispositivos IoT"""
    
    def __init__(self, device_id="vader-iot-001"):
        self.device_id = device_id
        self.variables = {}
        self.functions = {}
        self.sensors = {}
        self.actuators = {}
        self.mqtt_client = None
        self.serial_connections = {}
        self.debug_mode = True
        
        # Configuración IoT
        self.iot_config = {
            'mqtt_broker': 'localhost',
            'mqtt_port': 1883,
            'mqtt_topic_prefix': f'vader/{device_id}',
            'sensor_read_interval': 1.0,
            'device_type': self.detect_device_type()
        }
        
        # Inicializar componentes
        self.setup_logging()
        self.init_gpio()
        self.init_mqtt()
        
        print(f"🌐 Vader IoT Runtime inicializado para {self.iot_config['device_type']}")
    
    def setup_logging(self):
        """Configurar logging para IoT"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - VaderIoT - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(f'/tmp/vader_iot_{self.device_id}.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def detect_device_type(self):
        """Detectar tipo de dispositivo IoT"""
        if RASPBERRY_PI:
            return "Raspberry Pi"
        elif CIRCUITPYTHON:
            return "CircuitPython"
        else:
            return "Generic Linux"
    
    def init_gpio(self):
        """Inicializar GPIO según la plataforma"""
        if RASPBERRY_PI:
            GPIO.setmode(GPIO.BCM)
            GPIO.setwarnings(False)
            self.logger.info("🔌 GPIO Raspberry Pi inicializado")
        elif CIRCUITPYTHON:
            self.logger.info("🔌 CircuitPython GPIO inicializado")
        else:
            self.logger.info("🔌 GPIO simulado inicializado")
    
    def init_mqtt(self):
        """Inicializar cliente MQTT"""
        try:
            self.mqtt_client = mqtt.Client(self.device_id)
            self.mqtt_client.on_connect = self.on_mqtt_connect
            self.mqtt_client.on_message = self.on_mqtt_message
            self.mqtt_client.connect(self.iot_config['mqtt_broker'], self.iot_config['mqtt_port'], 60)
            self.mqtt_client.loop_start()
            self.logger.info("📡 Cliente MQTT inicializado")
        except Exception as e:
            self.logger.warning(f"⚠️ MQTT no disponible: {e}")
    
    def on_mqtt_connect(self, client, userdata, flags, rc):
        """Callback de conexión MQTT"""
        if rc == 0:
            topic = f"{self.iot_config['mqtt_topic_prefix']}/commands"
            client.subscribe(topic)
            self.logger.info(f"📡 Conectado a MQTT, suscrito a {topic}")
        else:
            self.logger.error(f"❌ Error conectando MQTT: {rc}")
    
    def on_mqtt_message(self, client, userdata, msg):
        """Callback de mensaje MQTT"""
        try:
            payload = msg.payload.decode('utf-8')
            self.logger.info(f"📨 Mensaje MQTT recibido: {payload}")
            
            # Ejecutar comando Vader recibido por MQTT
            asyncio.create_task(self.execute_code(payload))
        except Exception as e:
            self.logger.error(f"❌ Error procesando mensaje MQTT: {e}")
    
    async def execute_code(self, code: str) -> Dict[str, Any]:
        """Ejecutar código Vader IoT"""
        output = []
        lines = code.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            if line and not line.startswith('#'):
                try:
                    result = await self.execute_line(line)
                    if result:
                        output.append(result)
                except Exception as e:
                    error_msg = f"❌ Error línea {line_num}: {str(e)}"
                    output.append(error_msg)
                    self.logger.error(error_msg)
        
        return {
            'output': output,
            'variables': self.variables,
            'device_id': self.device_id,
            'timestamp': datetime.now().isoformat()
        }
    
    async def execute_line(self, line: str) -> Optional[str]:
        """Ejecutar línea individual con comandos IoT"""
        
        # Comandos de sensores
        if line.startswith('leer sensor'):
            return await self.read_sensor(line)
        elif line.startswith('configurar sensor'):
            return self.configure_sensor(line)
        
        # Comandos de actuadores
        elif line.startswith('activar actuador'):
            return self.activate_actuator(line)
        elif line.startswith('desactivar actuador'):
            return self.deactivate_actuator(line)
        elif line.startswith('configurar actuador'):
            return self.configure_actuator(line)
        
        # Comandos de comunicación
        elif line.startswith('enviar mqtt'):
            return self.send_mqtt_message(line)
        elif line.startswith('enviar http'):
            return await self.send_http_request(line)
        elif line.startswith('leer serial'):
            return self.read_serial(line)
        elif line.startswith('escribir serial'):
            return self.write_serial(line)
        
        # Comandos de control
        elif line.startswith('esperar'):
            return await self.wait_command(line)
        elif line.startswith('repetir cada'):
            return self.schedule_repeat(line)
        elif line.startswith('si sensor'):
            return await self.sensor_conditional(line)
        
        # Comandos básicos
        elif line.startswith('mostrar'):
            message = self.extract_string(line, 'mostrar')
            self.logger.info(f"📤 {message}")
            return message
        elif ' = ' in line:
            return self.handle_assignment(line)
        
        return None
    
    async def read_sensor(self, line: str) -> str:
        """Leer valor de sensor"""
        # leer sensor "temperatura" pin=18 tipo="DHT22"
        import re
        match = re.match(r'leer sensor "([^"]+)" pin=(\d+) tipo="([^"]+)"', line)
        
        if not match:
            return "❌ Sintaxis: leer sensor \"nombre\" pin=X tipo=\"tipo\""
        
        sensor_name, pin, sensor_type = match.groups()
        pin = int(pin)
        
        try:
            if sensor_type.upper() == "DHT22":
                value = await self.read_dht22(pin)
            elif sensor_type.upper() == "ANALOG":
                value = await self.read_analog(pin)
            elif sensor_type.upper() == "DIGITAL":
                value = await self.read_digital(pin)
            elif sensor_type.upper() == "ULTRASONIC":
                value = await self.read_ultrasonic(pin)
            else:
                # Sensor simulado
                value = self.simulate_sensor_reading(sensor_type)
            
            self.variables[f'sensor_{sensor_name}'] = value
            self.sensors[sensor_name] = {'pin': pin, 'type': sensor_type, 'last_value': value}
            
            # Publicar por MQTT
            if self.mqtt_client:
                topic = f"{self.iot_config['mqtt_topic_prefix']}/sensors/{sensor_name}"
                self.mqtt_client.publish(topic, json.dumps({'value': value, 'timestamp': time.time()}))
            
            return f"📊 Sensor {sensor_name}: {value}"
            
        except Exception as e:
            return f"❌ Error leyendo sensor {sensor_name}: {e}"
    
    async def read_dht22(self, pin: int) -> Dict[str, float]:
        """Leer sensor DHT22 (temperatura y humedad)"""
        if RASPBERRY_PI:
            try:
                import Adafruit_DHT
                humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, pin)
                return {'temperatura': temperature, 'humedad': humidity}
            except ImportError:
                pass
        
        # Simulación
        import random
        return {
            'temperatura': round(random.uniform(18.0, 35.0), 1),
            'humedad': round(random.uniform(30.0, 80.0), 1)
        }
    
    async def read_analog(self, pin: int) -> float:
        """Leer pin analógico"""
        if CIRCUITPYTHON:
            try:
                analog_pin = analogio.AnalogIn(getattr(board, f'A{pin}'))
                return (analog_pin.value * 3.3) / 65536
            except:
                pass
        
        # Simulación
        import random
        return round(random.uniform(0.0, 3.3), 2)
    
    async def read_digital(self, pin: int) -> bool:
        """Leer pin digital"""
        if RASPBERRY_PI:
            GPIO.setup(pin, GPIO.IN)
            return bool(GPIO.input(pin))
        elif CIRCUITPYTHON:
            try:
                digital_pin = digitalio.DigitalInOut(getattr(board, f'D{pin}'))
                digital_pin.direction = digitalio.Direction.INPUT
                return digital_pin.value
            except:
                pass
        
        # Simulación
        import random
        return random.choice([True, False])
    
    async def read_ultrasonic(self, pin: int) -> float:
        """Leer sensor ultrasónico HC-SR04"""
        if RASPBERRY_PI:
            try:
                trigger_pin = pin
                echo_pin = pin + 1
                
                GPIO.setup(trigger_pin, GPIO.OUT)
                GPIO.setup(echo_pin, GPIO.IN)
                
                # Enviar pulso
                GPIO.output(trigger_pin, True)
                time.sleep(0.00001)
                GPIO.output(trigger_pin, False)
                
                # Medir tiempo
                start_time = time.time()
                while GPIO.input(echo_pin) == 0:
                    start_time = time.time()
                
                while GPIO.input(echo_pin) == 1:
                    end_time = time.time()
                
                # Calcular distancia
                duration = end_time - start_time
                distance = (duration * 34300) / 2  # cm
                
                return round(distance, 1)
            except:
                pass
        
        # Simulación
        import random
        return round(random.uniform(5.0, 200.0), 1)
    
    def simulate_sensor_reading(self, sensor_type: str) -> Any:
        """Simular lectura de sensor"""
        import random
        
        simulations = {
            'temperatura': round(random.uniform(15.0, 40.0), 1),
            'humedad': round(random.uniform(20.0, 90.0), 1),
            'presion': round(random.uniform(990.0, 1030.0), 1),
            'luz': random.randint(0, 1023),
            'movimiento': random.choice([True, False]),
            'sonido': random.randint(0, 100),
            'gas': random.randint(0, 500),
            'ph': round(random.uniform(6.0, 8.0), 1)
        }
        
        return simulations.get(sensor_type.lower(), random.randint(0, 100))
    
    def activate_actuator(self, line: str) -> str:
        """Activar actuador"""
        # activar actuador "led" pin=18 valor=True
        import re
        match = re.match(r'activar actuador "([^"]+)" pin=(\d+) valor=(\w+)', line)
        
        if not match:
            return "❌ Sintaxis: activar actuador \"nombre\" pin=X valor=True/False/número"
        
        actuator_name, pin, value = match.groups()
        pin = int(pin)
        
        try:
            # Convertir valor
            if value.lower() == 'true':
                value = True
            elif value.lower() == 'false':
                value = False
            else:
                value = float(value)
            
            if RASPBERRY_PI:
                GPIO.setup(pin, GPIO.OUT)
                if isinstance(value, bool):
                    GPIO.output(pin, value)
                else:
                    # PWM para valores analógicos
                    pwm = GPIO.PWM(pin, 1000)
                    pwm.start(value)
            
            self.actuators[actuator_name] = {'pin': pin, 'value': value, 'active': True}
            
            # Publicar estado por MQTT
            if self.mqtt_client:
                topic = f"{self.iot_config['mqtt_topic_prefix']}/actuators/{actuator_name}"
                self.mqtt_client.publish(topic, json.dumps({'value': value, 'active': True}))
            
            return f"🔧 Actuador {actuator_name} activado: {value}"
            
        except Exception as e:
            return f"❌ Error activando actuador {actuator_name}: {e}"
    
    def send_mqtt_message(self, line: str) -> str:
        """Enviar mensaje MQTT"""
        # enviar mqtt "topic/subtopic" mensaje "Hola desde Vader IoT"
        import re
        match = re.match(r'enviar mqtt "([^"]+)" mensaje "([^"]+)"', line)
        
        if not match:
            return "❌ Sintaxis: enviar mqtt \"topic\" mensaje \"mensaje\""
        
        topic, message = match.groups()
        
        if self.mqtt_client:
            try:
                full_topic = f"{self.iot_config['mqtt_topic_prefix']}/{topic}"
                self.mqtt_client.publish(full_topic, message)
                return f"📡 Mensaje MQTT enviado a {full_topic}: {message}"
            except Exception as e:
                return f"❌ Error enviando MQTT: {e}"
        else:
            return "❌ Cliente MQTT no disponible"
    
    async def send_http_request(self, line: str) -> str:
        """Enviar petición HTTP"""
        # enviar http "POST" a "http://api.ejemplo.com/data" datos "{'sensor': 'temp', 'value': 25}"
        import re
        match = re.match(r'enviar http "([^"]+)" a "([^"]+)" datos "([^"]+)"', line)
        
        if not match:
            return "❌ Sintaxis: enviar http \"método\" a \"url\" datos \"json\""
        
        method, url, data = match.groups()
        
        try:
            if method.upper() == 'POST':
                response = requests.post(url, json=json.loads(data), timeout=10)
            elif method.upper() == 'GET':
                response = requests.get(url, timeout=10)
            else:
                return f"❌ Método HTTP no soportado: {method}"
            
            self.variables['ultima_respuesta_http'] = response.status_code
            return f"🌐 HTTP {method} {url}: {response.status_code}"
            
        except Exception as e:
            return f"❌ Error en petición HTTP: {e}"
    
    async def sensor_conditional(self, line: str) -> str:
        """Condicional basada en sensor"""
        # si sensor "temperatura" mayor que 30 entonces activar actuador "ventilador" pin=20 valor=True
        import re
        match = re.match(r'si sensor "([^"]+)" (mayor|menor|igual) que ([\d.]+) entonces (.+)', line)
        
        if not match:
            return "❌ Sintaxis: si sensor \"nombre\" mayor/menor/igual que valor entonces acción"
        
        sensor_name, operator, threshold, action = match.groups()
        threshold = float(threshold)
        
        # Obtener valor actual del sensor
        sensor_value = self.variables.get(f'sensor_{sensor_name}')
        
        if sensor_value is None:
            return f"❌ Sensor {sensor_name} no encontrado"
        
        # Evaluar condición
        condition_met = False
        if isinstance(sensor_value, dict):
            # Para sensores como DHT22 que devuelven múltiples valores
            sensor_value = sensor_value.get('temperatura', 0)
        
        if operator == 'mayor' and sensor_value > threshold:
            condition_met = True
        elif operator == 'menor' and sensor_value < threshold:
            condition_met = True
        elif operator == 'igual' and abs(sensor_value - threshold) < 0.1:
            condition_met = True
        
        if condition_met:
            result = await self.execute_line(action)
            return f"✅ Condición cumplida: {sensor_name}={sensor_value} {operator} {threshold} → {result}"
        else:
            return f"❌ Condición no cumplida: {sensor_name}={sensor_value} {operator} {threshold}"
    
    async def wait_command(self, line: str) -> str:
        """Comando de espera"""
        import re
        match = re.match(r'esperar (\d+) segundos', line)
        
        if match:
            seconds = int(match.group(1))
            await asyncio.sleep(seconds)
            return f"⏱️ Esperado {seconds} segundos"
        
        return "❌ Sintaxis: esperar X segundos"
    
    def schedule_repeat(self, line: str) -> str:
        """Programar repetición"""
        # repetir cada 30 segundos leer sensor "temperatura" pin=18 tipo="DHT22"
        import re
        match = re.match(r'repetir cada (\d+) segundos (.+)', line)
        
        if not match:
            return "❌ Sintaxis: repetir cada X segundos comando"
        
        interval, command = match.groups()
        interval = int(interval)
        
        def repeat_task():
            while True:
                try:
                    asyncio.create_task(self.execute_line(command))
                    time.sleep(interval)
                except Exception as e:
                    self.logger.error(f"❌ Error en tarea repetitiva: {e}")
        
        # Ejecutar en hilo separado
        thread = threading.Thread(target=repeat_task, daemon=True)
        thread.start()
        
        return f"🔄 Tarea programada cada {interval} segundos: {command}"
    
    # Funciones auxiliares
    def extract_string(self, line: str, command: str) -> str:
        import re
        pattern = f'{command}\\s+"([^"]+)"'
        match = re.search(pattern, line)
        return match.group(1) if match else line.replace(command, '').strip()
    
    def handle_assignment(self, line: str) -> str:
        variable, value = line.split(' = ', 1)
        variable = variable.strip()
        evaluated_value = self.evaluate_expression(value.strip())
        self.variables[variable] = evaluated_value
        
        return f"📝 {variable} = {evaluated_value}"
    
    def evaluate_expression(self, expr: str):
        # Reemplazar variables
        for var, val in self.variables.items():
            expr = expr.replace(var, str(val))
        
        try:
            return eval(expr)
        except:
            return expr.strip('"\'')
    
    def cleanup(self):
        """Limpiar recursos"""
        if RASPBERRY_PI:
            GPIO.cleanup()
        
        if self.mqtt_client:
            self.mqtt_client.loop_stop()
            self.mqtt_client.disconnect()
        
        self.logger.info("🧹 Recursos IoT limpiados")

# Función principal para dispositivos IoT
async def main():
    """Función principal para ejecutar en dispositivos IoT"""
    runtime = VaderIoTRuntime()
    
    # Código de ejemplo
    test_code = '''
    # Configurar sensores
    configurar sensor "temperatura" pin=18 tipo="DHT22"
    configurar actuador "led" pin=20
    
    # Leer sensores
    leer sensor "temperatura" pin=18 tipo="DHT22"
    mostrar "Temperatura leída"
    
    # Condicional IoT
    si sensor "temperatura" mayor que 25 entonces activar actuador "led" pin=20 valor=True
    
    # Comunicación
    enviar mqtt "status" mensaje "Vader IoT funcionando"
    
    # Programar tarea repetitiva
    repetir cada 60 segundos leer sensor "temperatura" pin=18 tipo="DHT22"
    '''
    
    try:
        result = await runtime.execute_code(test_code)
        print("\n📊 Resultado IoT:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
        # Mantener el programa corriendo
        while True:
            await asyncio.sleep(1)
            
    except KeyboardInterrupt:
        print("\n🛑 Deteniendo Vader IoT...")
    finally:
        runtime.cleanup()

if __name__ == "__main__":
    asyncio.run(main())
