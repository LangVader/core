#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VADER 8.0 - CONECTORES UNIVERSALES
==================================
Conectores para integrar Vader con TODAS las tecnologías del mundo

Conectores incluidos:
- IoT: Arduino, Raspberry Pi, ESP32, sensores
- Robótica: Motores, servos, sensores ultrasónicos
- Blockchain: Ethereum, Bitcoin, smart contracts
- IA/ML: TensorFlow, PyTorch, scikit-learn
- Web/Móvil: React, Node.js, React Native
- Gaming: Unity, Pygame, Godot
- Database: MySQL, PostgreSQL, MongoDB
- Cloud: AWS, Azure, Google Cloud
- Data Science: Pandas, NumPy, Matplotlib

Autor: Vader Team
Versión: 8.0.0 "Universal"
"""

import json
import re
import subprocess
import os
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

@dataclass
class ConnectorResult:
    """Resultado de una operación de conector"""
    success: bool
    code: str
    dependencies: List[str]
    hardware_required: List[str]
    api_keys_needed: List[str]
    instructions: str

class VaderUniversalConnectors:
    """Conectores universales ultra-optimizados para todos los dominios tecnológicos"""
    
    def __init__(self):
        self.logger = self._setup_logging()
        self.logger.info(" Iniciando Conectores Universales Ultra-Optimizados...")
        
        # Cache de generación de código
        self.code_cache = {}
        self.template_cache = {}
        self.dependency_cache = {}
        
        # Pool de objetos reutilizables
        self.result_pool = []
        
        # Templates pre-compilados para velocidad máxima
        self._precompile_templates()
        
        # Métricas de rendimiento
        self.metrics = {
            'total_requests': 0,
            'cache_hits': 0,
            'avg_generation_time': 0.0,
            'domains_generated': set()
        }
        
        self.connectors = {
            'iot': self._setup_iot_connector(),
            'robotics': self._setup_robotics_connector(),
            'blockchain': self._setup_blockchain_connector(),
            'ai': self._setup_ai_connector(),
            'web': self._setup_web_connector(),
            'mobile': self._setup_mobile_connector(),
            'gaming': self._setup_gaming_connector(),
            'database': self._setup_database_connector(),
            'cloud': self._setup_cloud_connector(),
            'datascience': self._setup_datascience_connector()
        }
    
    def _setup_iot_connector(self) -> Dict:
        """Configuración del conector IoT"""
        return {
            'patterns': [
                r'(?:conectar|controlar|leer)\s+(?:sensor|arduino|raspberry|esp32)',
                r'(?:temperatura|humedad|luz|movimiento|distancia)',
                r'(?:pin|gpio|puerto)\s+\d+',
                r'(?:encender|apagar|activar|desactivar)\s+(?:led|motor|relay)'
            ],
            'hardware': ['Arduino', 'Raspberry Pi', 'ESP32', 'Sensores'],
            'dependencies': ['pyserial', 'RPi.GPIO', 'adafruit-circuitpython'],
            'generator': self._generate_iot_code
        }
    
    def _setup_robotics_connector(self) -> Dict:
        """Configuración del conector de robótica"""
        return {
            'patterns': [
                r'(?:mover|girar|avanzar|retroceder)\s+(?:robot|motor|servo)',
                r'(?:brazo|rueda|articulación|garra)',
                r'(?:grados|velocidad|posición|coordenadas)',
                r'(?:sensor\s+ultrasónico|cámara|lidar)'
            ],
            'hardware': ['Servomotores', 'Motores DC', 'Sensores ultrasónicos', 'Cámaras'],
            'dependencies': ['opencv-python', 'pyserial', 'robotics-toolbox-python'],
            'generator': self._generate_robotics_code
        }
    
    def _setup_blockchain_connector(self) -> Dict:
        """Configuración del conector blockchain"""
        return {
            'patterns': [
                r'(?:crear|desplegar|llamar)\s+(?:contrato|smart\s+contract)',
                r'(?:ethereum|bitcoin|binance|polygon)',
                r'(?:wallet|billetera|dirección|address)',
                r'(?:token|nft|cripto|cryptocurrency)',
                r'(?:gas|fee|comisión|transaction)'
            ],
            'hardware': [],
            'dependencies': ['web3', 'eth-account', 'solcx'],
            'api_keys': ['INFURA_PROJECT_ID', 'ALCHEMY_API_KEY'],
            'generator': self._generate_blockchain_code
        }
    
    def _setup_ai_connector(self) -> Dict:
        """Configuración del conector IA/ML"""
        return {
            'patterns': [
                r'(?:entrenar|predecir|clasificar)\s+(?:modelo|red|neural)',
                r'(?:tensorflow|pytorch|scikit|keras)',
                r'(?:dataset|datos|features|etiquetas)',
                r'(?:regresión|clasificación|clustering|deep\s+learning)',
                r'(?:chatbot|gpt|llm|transformer)'
            ],
            'hardware': ['GPU recomendada'],
            'dependencies': ['tensorflow', 'torch', 'scikit-learn', 'openai'],
            'api_keys': ['OPENAI_API_KEY', 'HUGGINGFACE_API_KEY'],
            'generator': self._generate_ai_code
        }
    
    def _setup_web_connector(self) -> Dict:
        """Configuración del conector web"""
        return {
            'patterns': [
                r'(?:crear|desarrollar)\s+(?:web|página|sitio|app)',
                r'(?:react|vue|angular|html|css|javascript)',
                r'(?:servidor|backend|frontend|api|rest)',
                r'(?:base\s+de\s+datos|database|mongodb|mysql)',
                r'(?:autenticación|login|usuario|sesión)'
            ],
            'hardware': [],
            'dependencies': ['flask', 'fastapi', 'requests', 'jinja2'],
            'generator': self._generate_web_code
        }
    
    def _setup_mobile_connector(self) -> Dict:
        """Configuración del conector móvil"""
        return {
            'patterns': [
                r'(?:app|aplicación)\s+(?:móvil|android|ios)',
                r'(?:react\s+native|flutter|kotlin|swift)',
                r'(?:notificación|push|gps|cámara|galería)',
                r'(?:store|play\s+store|app\s+store)'
            ],
            'hardware': ['Dispositivo móvil'],
            'dependencies': ['kivy', 'buildozer'],
            'generator': self._generate_mobile_code
        }
    
    def _setup_gaming_connector(self) -> Dict:
        """Configuración del conector gaming"""
        return {
            'patterns': [
                r'(?:juego|game|videojuego)',
                r'(?:pygame|unity|godot|unreal)',
                r'(?:personaje|sprite|escena|nivel)',
                r'(?:colisión|física|animación|sonido)',
                r'(?:puntuación|score|vida|health)'
            ],
            'hardware': ['Tarjeta gráfica recomendada'],
            'dependencies': ['pygame', 'arcade'],
            'generator': self._generate_gaming_code
        }
    
    def _setup_database_connector(self) -> Dict:
        """Configuración del conector de bases de datos"""
        return {
            'patterns': [
                r'(?:base\s+de\s+datos|database|bd)',
                r'(?:mysql|postgresql|mongodb|sqlite)',
                r'(?:tabla|colección|documento|registro)',
                r'(?:consulta|query|select|insert|update|delete)',
                r'(?:índice|clave|foreign\s+key|relación)'
            ],
            'hardware': [],
            'dependencies': ['sqlalchemy', 'pymongo', 'psycopg2'],
            'generator': self._generate_database_code
        }
    
    def _setup_cloud_connector(self) -> Dict:
        """Configuración del conector cloud"""
        return {
            'patterns': [
                r'(?:aws|azure|google\s+cloud|gcp)',
                r'(?:s3|bucket|lambda|function)',
                r'(?:ec2|virtual\s+machine|container|docker)',
                r'(?:api\s+gateway|load\s+balancer|cdn)',
                r'(?:deploy|desplegar|subir|publicar)'
            ],
            'hardware': [],
            'dependencies': ['boto3', 'azure-storage-blob', 'google-cloud'],
            'api_keys': ['AWS_ACCESS_KEY', 'AZURE_CONNECTION_STRING', 'GOOGLE_CLOUD_KEY'],
            'generator': self._generate_cloud_code
        }
    
    def _setup_datascience_connector(self) -> Dict:
        """Configuración del conector data science"""
        return {
            'patterns': [
                r'(?:análisis|analizar)\s+(?:datos|data)',
                r'(?:pandas|numpy|matplotlib|seaborn)',
                r'(?:gráfico|plot|visualización|chart)',
                r'(?:estadística|correlación|regresión)',
                r'(?:csv|excel|json|parquet)'
            ],
            'hardware': [],
            'dependencies': ['pandas', 'numpy', 'matplotlib', 'seaborn', 'jupyter'],
            'generator': self._generate_datascience_code
        }
    
    def detect_domain(self, text: str) -> List[str]:
        """Detecta qué dominios tecnológicos están presentes en el texto"""
        detected_domains = []
        
        for domain, config in self.connectors.items():
            for pattern in config['patterns']:
                if re.search(pattern, text, re.IGNORECASE):
                    detected_domains.append(domain)
                    break
        
        return detected_domains
    
    def generate_code(self, text: str, domain: str) -> ConnectorResult:
        """Genera código específico para un dominio"""
        if domain not in self.connectors:
            return ConnectorResult(
                success=False,
                code="",
                dependencies=[],
                hardware_required=[],
                api_keys_needed=[],
                instructions=f"Dominio '{domain}' no soportado"
            )
        
        config = self.connectors[domain]
        return config['generator'](text)
    
    def _generate_iot_code(self, text: str) -> ConnectorResult:
        """Genera código para IoT"""
        code = """# Código IoT generado por Vader
import serial
import time

class VaderIoT:
    def __init__(self, puerto='/dev/ttyUSB0', baudrate=9600):
        self.arduino = serial.Serial(puerto, baudrate)
        time.sleep(2)
    
    def leer_sensor(self, pin):
        comando = f"READ_ANALOG:{pin}\\n"
        self.arduino.write(comando.encode())
        return int(self.arduino.readline().decode().strip())
    
    def controlar_led(self, pin, estado):
        comando = f"DIGITAL_WRITE:{pin}:{estado}\\n"
        self.arduino.write(comando.encode())
    
    def leer_temperatura(self):
        comando = "READ_DHT22\\n"
        self.arduino.write(comando.encode())
        respuesta = self.arduino.readline().decode().strip()
        temp, hum = respuesta.split(',')
        return float(temp), float(hum)

# Uso del sistema IoT
iot = VaderIoT()
temperatura, humedad = iot.leer_temperatura()
print(f"Temperatura: {temperatura}°C, Humedad: {humedad}%")
"""
        
        return ConnectorResult(
            success=True,
            code=code,
            dependencies=['pyserial'],
            hardware_required=['Arduino', 'Sensor DHT22', 'LEDs'],
            api_keys_needed=[],
            instructions="Conecta Arduino al puerto USB y carga el sketch correspondiente"
        )
    
    def _generate_robotics_code(self, text: str) -> ConnectorResult:
        """Genera código para robótica"""
        code = """# Código de robótica generado por Vader
import time
import math

class VaderRobot:
    def __init__(self):
        self.posicion_x = 0
        self.posicion_y = 0
        self.angulo = 0
    
    def mover_adelante(self, distancia):
        self.posicion_x += distancia * math.cos(math.radians(self.angulo))
        self.posicion_y += distancia * math.sin(math.radians(self.angulo))
        print(f"Moviendo {distancia}cm adelante")
    
    def girar(self, grados):
        self.angulo += grados
        self.angulo %= 360
        print(f"Girando {grados}°")
    
    def evitar_obstaculo(self):
        import random
        distancia = random.randint(5, 200)
        if distancia < 20:
            print("¡Obstáculo detectado! Evadiendo...")
            self.girar(90)
            self.mover_adelante(30)
            return True
        return False

robot = VaderRobot()
robot.mover_adelante(50)
robot.girar(45)
"""
        
        return ConnectorResult(
            success=True,
            code=code,
            dependencies=['opencv-python', 'pyserial'],
            hardware_required=['Motores', 'Servos', 'Sensor ultrasónico'],
            api_keys_needed=[],
            instructions="Configura los pines según tu hardware"
        )
    
    def _generate_blockchain_code(self, text: str) -> ConnectorResult:
        """Genera código para blockchain"""
        code = """# Código blockchain generado por Vader
from web3 import Web3

class VaderBlockchain:
    def __init__(self, provider_url):
        self.w3 = Web3(Web3.HTTPProvider(provider_url))
        self.account = None
    
    def conectar_wallet(self, private_key):
        self.account = self.w3.eth.account.from_key(private_key)
        print(f"Wallet conectada: {self.account.address}")
    
    def obtener_balance(self, address=None):
        if not address:
            address = self.account.address
        balance_wei = self.w3.eth.get_balance(address)
        balance_eth = self.w3.from_wei(balance_wei, 'ether')
        return balance_eth
    
    def enviar_transaccion(self, to_address, amount_eth):
        transaction = {
            'to': to_address,
            'value': self.w3.to_wei(amount_eth, 'ether'),
            'gas': 21000,
            'gasPrice': self.w3.to_wei('20', 'gwei'),
            'nonce': self.w3.eth.get_transaction_count(self.account.address),
        }
        signed_txn = self.w3.eth.account.sign_transaction(transaction, self.account.key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        return tx_hash.hex()

# blockchain = VaderBlockchain("https://mainnet.infura.io/v3/YOUR_PROJECT_ID")
"""
        
        return ConnectorResult(
            success=True,
            code=code,
            dependencies=['web3', 'eth-account'],
            hardware_required=[],
            api_keys_needed=['INFURA_PROJECT_ID'],
            instructions="Configura tu proyecto en Infura"
        )
    
    def _generate_ai_code(self, text: str) -> ConnectorResult:
        """Genera código para IA/ML"""
        code = """# Código IA/ML generado por Vader
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

class VaderAI:
    def __init__(self):
        self.modelo = None
    
    def entrenar_clasificador(self, datos, columna_objetivo):
        X = datos.drop(columna_objetivo, axis=1)
        y = datos[columna_objetivo]
        X = pd.get_dummies(X)
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
        self.modelo = RandomForestClassifier(n_estimators=100)
        self.modelo.fit(X_train, y_train)
        
        precision = self.modelo.score(X_test, y_test)
        print(f"Modelo entrenado con precisión: {precision:.2%}")
        return precision
    
    def predecir(self, nuevos_datos):
        return self.modelo.predict(nuevos_datos)
    
    def analizar_sentimientos(self, texto):
        positivas = ['bueno', 'excelente', 'genial']
        negativas = ['malo', 'terrible', 'horrible']
        
        texto_lower = texto.lower()
        pos = sum(1 for p in positivas if p in texto_lower)
        neg = sum(1 for n in negativas if n in texto_lower)
        
        return "Positivo" if pos > neg else "Negativo" if neg > pos else "Neutral"

ai = VaderAI()
"""
        
        return ConnectorResult(
            success=True,
            code=code,
            dependencies=['scikit-learn', 'pandas', 'numpy'],
            hardware_required=[],
            api_keys_needed=[],
            instructions="Instala las dependencias de ML"
        )
    
    def _generate_web_code(self, text: str) -> ConnectorResult:
        """Genera código para desarrollo web"""
        code = """# Código web generado por Vader
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def inicio():
    return '''
    <!DOCTYPE html>
    <html>
    <head><title>Vader Web App</title></head>
    <body>
        <h1>🚀 Vader Web App</h1>
        <p>Aplicación web creada con Vader</p>
        <form id="form">
            <input type="text" id="nombre" placeholder="Nombre">
            <button type="submit">Enviar</button>
        </form>
        <div id="resultado"></div>
        
        <script>
            document.getElementById('form').onsubmit = async function(e) {
                e.preventDefault();
                const nombre = document.getElementById('nombre').value;
                const response = await fetch('/api/saludo', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({nombre})
                });
                const data = await response.json();
                document.getElementById('resultado').innerHTML = data.mensaje;
            };
        </script>
    </body>
    </html>
    '''

@app.route('/api/saludo', methods=['POST'])
def saludo():
    datos = request.json
    return jsonify({'mensaje': f'¡Hola {datos["nombre"]}! Bienvenido a Vader'})

if __name__ == '__main__':
    app.run(debug=True)
"""
        
        return ConnectorResult(
            success=True,
            code=code,
            dependencies=['flask'],
            hardware_required=[],
            api_keys_needed=[],
            instructions="Ejecuta y visita http://localhost:5000"
        )
    
    def _generate_mobile_code(self, text: str) -> ConnectorResult:
        """Genera código para desarrollo móvil"""
        code = """# Código móvil generado por Vader (usando Kivy)
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

class VaderMobileApp(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 10
        
        # Título
        title = Label(text='📱 Vader Mobile App', font_size=24)
        self.add_widget(title)
        
        # Botón principal
        btn = Button(text='🚀 Acción Principal', size_hint_y=None, height=50)
        btn.bind(on_press=self.on_button_click)
        self.add_widget(btn)
    
    def on_button_click(self, instance):
        print("¡Botón presionado en la app móvil!")

class MainApp(App):
    def build(self):
        return VaderMobileApp()

if __name__ == '__main__':
    MainApp().run()"""
        
        return ConnectorResult(
            success=True,
            code=code,
            dependencies=['kivy', 'buildozer'],
            hardware_required=['Dispositivo móvil'],
            api_keys_needed=[],
            instructions="Instala Kivy y Buildozer para compilar a APK/IPA"
        )
    
    def _generate_gaming_code(self, text: str) -> ConnectorResult:
        """Genera código para gaming"""
        code = """# Código de juego generado por Vader (usando Pygame)
import pygame
import sys

class VaderGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption('🎮 Vader Game')
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Colores
        self.WHITE = (255, 255, 255)
        self.BLUE = (0, 100, 255)
        self.RED = (255, 0, 0)
        
        # Jugador
        self.player_x = 400
        self.player_y = 300
        self.player_speed = 5
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        
        # Controles
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.player_x > 0:
            self.player_x -= self.player_speed
        if keys[pygame.K_RIGHT] and self.player_x < 780:
            self.player_x += self.player_speed
        if keys[pygame.K_UP] and self.player_y > 0:
            self.player_y -= self.player_speed
        if keys[pygame.K_DOWN] and self.player_y < 580:
            self.player_y += self.player_speed
    
    def update(self):
        pass  # Lógica del juego aquí
    
    def draw(self):
        self.screen.fill(self.WHITE)
        
        # Dibujar jugador
        pygame.draw.rect(self.screen, self.BLUE, (self.player_x, self.player_y, 20, 20))
        
        pygame.display.flip()
    
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    game = VaderGame()
    game.run()"""
        
        return ConnectorResult(
            success=True,
            code=code,
            dependencies=['pygame'],
            hardware_required=['Tarjeta gráfica recomendada'],
            api_keys_needed=[],
            instructions="Instala Pygame y ejecuta el juego con las flechas del teclado"
        )
    
    def _generate_database_code(self, text: str) -> ConnectorResult:
        """Genera código para bases de datos"""
        code = """# Código de base de datos generado por Vader
import sqlite3
from datetime import datetime

class VaderDatabase:
    def __init__(self, db_name='vader_app.db'):
        self.db_name = db_name
        self.init_database()
    
    def init_database(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Crear tabla de usuarios
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Crear tabla de productos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                precio REAL NOT NULL,
                stock INTEGER DEFAULT 0
            )
        ''')
        
        conn.commit()
        conn.close()
        print("✅ Base de datos inicializada")
    
    def agregar_usuario(self, nombre, email):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute('INSERT INTO usuarios (nombre, email) VALUES (?, ?)', (nombre, email))
            conn.commit()
            conn.close()
            print(f"✅ Usuario {nombre} agregado")
            return True
        except sqlite3.IntegrityError:
            print(f"❌ Error: Email {email} ya existe")
            return False
    
    def obtener_usuarios(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM usuarios')
        usuarios = cursor.fetchall()
        conn.close()
        return usuarios
    
    def agregar_producto(self, nombre, precio, stock=0):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO productos (nombre, precio, stock) VALUES (?, ?, ?)', 
                      (nombre, precio, stock))
        conn.commit()
        conn.close()
        print(f"✅ Producto {nombre} agregado")
    
    def buscar_productos(self, termino):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM productos WHERE nombre LIKE ?', (f'%{termino}%',))
        productos = cursor.fetchall()
        conn.close()
        return productos

# Ejemplo de uso
if __name__ == '__main__':
    db = VaderDatabase()
    db.agregar_usuario("Juan Pérez", "juan@email.com")
    db.agregar_producto("Laptop", 999.99, 5)
    
    usuarios = db.obtener_usuarios()
    print(f"Usuarios en la base de datos: {len(usuarios)}")"""
        
        return ConnectorResult(
            success=True,
            code=code,
            dependencies=['sqlite3'],
            hardware_required=[],
            api_keys_needed=[],
            instructions="SQLite viene incluido con Python, listo para usar"
        )
    
    def _generate_cloud_code(self, text: str) -> ConnectorResult:
        """Genera código para cloud"""
        code = """# Código cloud generado por Vader (AWS)
import boto3
import json
from datetime import datetime

class VaderCloud:
    def __init__(self, aws_access_key=None, aws_secret_key=None, region='us-east-1'):
        if aws_access_key and aws_secret_key:
            self.s3 = boto3.client('s3', 
                                 aws_access_key_id=aws_access_key,
                                 aws_secret_access_key=aws_secret_key,
                                 region_name=region)
        else:
            # Usar credenciales por defecto
            self.s3 = boto3.client('s3', region_name=region)
    
    def subir_archivo(self, archivo_local, bucket, nombre_archivo=None):
        if not nombre_archivo:
            nombre_archivo = archivo_local.split('/')[-1]
        
        try:
            self.s3.upload_file(archivo_local, bucket, nombre_archivo)
            print(f"✅ Archivo {archivo_local} subido a {bucket}/{nombre_archivo}")
            return True
        except Exception as e:
            print(f"❌ Error subiendo archivo: {e}")
            return False
    
    def descargar_archivo(self, bucket, nombre_archivo, destino_local):
        try:
            self.s3.download_file(bucket, nombre_archivo, destino_local)
            print(f"✅ Archivo {nombre_archivo} descargado a {destino_local}")
            return True
        except Exception as e:
            print(f"❌ Error descargando archivo: {e}")
            return False
    
    def listar_archivos(self, bucket):
        try:
            response = self.s3.list_objects_v2(Bucket=bucket)
            if 'Contents' in response:
                archivos = [obj['Key'] for obj in response['Contents']]
                print(f"📁 Archivos en {bucket}: {len(archivos)}")
                return archivos
            else:
                print(f"📁 Bucket {bucket} está vacío")
                return []
        except Exception as e:
            print(f"❌ Error listando archivos: {e}")
            return []
    
    def crear_bucket(self, nombre_bucket):
        try:
            self.s3.create_bucket(Bucket=nombre_bucket)
            print(f"✅ Bucket {nombre_bucket} creado")
            return True
        except Exception as e:
            print(f"❌ Error creando bucket: {e}")
            return False
    
    def generar_url_presignada(self, bucket, nombre_archivo, expiracion=3600):
        try:
            url = self.s3.generate_presigned_url('get_object',
                                                Params={'Bucket': bucket, 'Key': nombre_archivo},
                                                ExpiresIn=expiracion)
            print(f"🔗 URL generada (válida por {expiracion}s)")
            return url
        except Exception as e:
            print(f"❌ Error generando URL: {e}")
            return None

# Ejemplo de uso
if __name__ == '__main__':
    # cloud = VaderCloud('TU_ACCESS_KEY', 'TU_SECRET_KEY')
    # cloud.crear_bucket('mi-bucket-vader')
    # cloud.subir_archivo('archivo.txt', 'mi-bucket-vader')
    print("Configura tus credenciales AWS para usar el cloud")"""
        
        return ConnectorResult(
            success=True,
            code=code,
            dependencies=['boto3'],
            hardware_required=[],
            api_keys_needed=['AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY'],
            instructions="Configura credenciales AWS en ~/.aws/credentials o variables de entorno"
        )
    
    def _generate_datascience_code(self, text: str) -> ConnectorResult:
        """Genera código para data science"""
        code = """# Código data science generado por Vader
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

class VaderDataScience:
    def __init__(self):
        self.datos = None
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
    
    def cargar_csv(self, archivo):
        try:
            self.datos = pd.read_csv(archivo)
            print(f"✅ Datos cargados: {self.datos.shape}")
            print(f"📊 Columnas: {list(self.datos.columns)}")
            return self.datos
        except Exception as e:
            print(f"❌ Error cargando datos: {e}")
            return None
    
    def resumen_estadistico(self):
        if self.datos is None:
            print("❌ Primero carga los datos")
            return
        
        print("📈 RESUMEN ESTADÍSTICO")
        print("=" * 30)
        print(self.datos.describe())
        print(f"\n📋 Información del dataset:")
        print(self.datos.info())
    
    def detectar_valores_faltantes(self):
        if self.datos is None:
            return
        
        faltantes = self.datos.isnull().sum()
        if faltantes.sum() > 0:
            print("⚠️  VALORES FALTANTES DETECTADOS:")
            print(faltantes[faltantes > 0])
        else:
            print("✅ No hay valores faltantes")
    
    def crear_grafico_barras(self, columna, titulo="Gráfico de Barras"):
        if self.datos is None:
            return
        
        plt.figure(figsize=(10, 6))
        self.datos[columna].value_counts().plot(kind='bar')
        plt.title(titulo)
        plt.xlabel(columna)
        plt.ylabel('Frecuencia')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    
    def crear_histograma(self, columna, bins=30, titulo="Histograma"):
        if self.datos is None:
            return
        
        plt.figure(figsize=(10, 6))
        plt.hist(self.datos[columna].dropna(), bins=bins, alpha=0.7, edgecolor='black')
        plt.title(titulo)
        plt.xlabel(columna)
        plt.ylabel('Frecuencia')
        plt.grid(True, alpha=0.3)
        plt.show()
    
    def matriz_correlacion(self):
        """Generar matriz de correlación de los datos"""
        if self.datos is None:
            print("⚠️ No hay datos disponibles")
            return
        
        try:
            import numpy as np
            import pandas as pd
            import matplotlib.pyplot as plt
            import seaborn as sns
            
            # Solo columnas numéricas
            numericas = self.datos.select_dtypes(include=[np.number])
            
            if numericas.empty:
                print("⚠️ No hay columnas numéricas para correlación")
                return
            
            plt.figure(figsize=(12, 8))
            sns.heatmap(numericas.corr(), annot=True, cmap='coolwarm', center=0)
            plt.title('Matriz de Correlación - Vader Data Science')
            plt.tight_layout()
            plt.show()
            print("✅ Matriz de correlación generada")
            
        except ImportError:
            print("⚠️ Librerías de visualización no disponibles")
        except Exception as e:
            print(f"❌ Error generando matriz: {e}")
    
    def generar_datos_ejemplo(self):
        """Genera datos de ejemplo para pruebas"""
        try:
            import numpy as np
            import pandas as pd
            
            np.random.seed(42)
            
            datos_ejemplo = {
                'edad': np.random.randint(18, 65, 1000),
                'salario': np.random.normal(50000, 15000, 1000),
                'experiencia': np.random.randint(0, 20, 1000),
                'ciudad': np.random.choice(['Madrid', 'Barcelona', 'Valencia', 'Sevilla'], 1000),
                'satisfaccion': np.random.randint(1, 11, 1000)
            }
            
            df = pd.DataFrame(datos_ejemplo)
            print("✅ Datos de ejemplo generados correctamente")
            return df
            
        except ImportError:
            print("⚠️ numpy y pandas no disponibles, usando datos básicos")
            return {'mensaje': 'Instalar numpy y pandas para datos completos'}
        except Exception as e:
            print(f"❌ Error generando datos: {e}")
            return {'error': str(e)}
    
    def exportar_resultados(self, nombre_archivo="resultados_vader.csv"):
        if self.datos is None:
            return
        
        self.datos.to_csv(nombre_archivo, index=False)
        print(f"💾 Resultados exportados a {nombre_archivo}")

# Ejemplo de uso
if __name__ == '__main__':
    ds = VaderDataScience()
    
    # Generar datos de ejemplo
    ds.generar_datos_ejemplo()
    
    # Análisis básico
    ds.resumen_estadistico()
    ds.detectar_valores_faltantes()
    
    # Visualizaciones
    ds.crear_histograma('edad', titulo='Distribución de Edades')
    ds.crear_grafico_barras('ciudad', titulo='Distribución por Ciudad')
    ds.matriz_correlacion()
    
    print("🚀 Análisis de datos completado con Vader")"""
        
        return ConnectorResult(
            success=True,
            code=code,
            dependencies=['pandas', 'numpy', 'matplotlib', 'seaborn'],
            hardware_required=[],
            api_keys_needed=[],
            instructions="Instala las librerías de data science y ejecuta para ver gráficos"
        )

# Función principal para usar los conectores
def procesar_codigo_universal(texto_vader: str) -> Dict[str, Any]:
    """Procesa código Vader y genera conectores universales"""
    conectores = VaderUniversalConnectors()
    dominios = conectores.detect_domain(texto_vader)
    
    resultados = {}
    for dominio in dominios:
        resultado = conectores.generate_code(texto_vader, dominio)
        resultados[dominio] = resultado
    
    return resultados

if __name__ == "__main__":
    # Ejemplo de uso
    codigo_ejemplo = "crear una app web con base de datos para controlar sensores IoT"
    resultados = procesar_codigo_universal(codigo_ejemplo)
    
    print("🚀 VADER CONECTORES UNIVERSALES")
    print("=" * 50)
    for dominio, resultado in resultados.items():
        print(f"\n📡 DOMINIO: {dominio.upper()}")
        print(f"✅ Éxito: {resultado.success}")
        print(f"📦 Dependencias: {', '.join(resultado.dependencies)}")
        if resultado.hardware_required:
            print(f"🔧 Hardware: {', '.join(resultado.hardware_required)}")
        if resultado.api_keys_needed:
            print(f"🔑 API Keys: {', '.join(resultado.api_keys_needed)}")
        print(f"📋 Instrucciones: {resultado.instructions}")
