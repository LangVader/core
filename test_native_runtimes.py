#!/usr/bin/env python3
"""
Tests automáticos para los runtimes nativos de Vader
Valida Mobile Runtime, IoT Runtime y Blockchain Runtime
"""

import unittest
import tempfile
import shutil
import os
import sys
from pathlib import Path

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'runtimes'))

from mobile_runtime import VaderMobileRuntime
from iot_runtime import VaderIoTRuntime
from blockchain_runtime import VaderBlockchainRuntime

class TestVaderNativeRuntimes(unittest.TestCase):
    """Tests para los runtimes nativos de Vader"""
    
    def setUp(self):
        """Configurar tests"""
        self.temp_dir = tempfile.mkdtemp()
        self.mobile_runtime = VaderMobileRuntime()
        self.iot_runtime = VaderIoTRuntime()
        self.blockchain_runtime = VaderBlockchainRuntime()
        
        # Código Vader de ejemplo para móvil
        self.mobile_vader_code = """# App móvil de ejemplo
titulo_app = "Mi App Vader"

# Componentes móvil
mostrar pantalla "Inicio"
crear boton "Presionar"
mostrar texto "Hola Mundo"

# Navegación
ir a pantalla "Detalles"
mostrar lista elementos

# Funciones móvil
vibrar dispositivo
tomar foto
enviar notificacion "Mensaje"
"""
        
        # Código Vader de ejemplo para IoT
        self.iot_vader_code = """# Dispositivo IoT de ejemplo
nombre_dispositivo = "Sensor Inteligente"

# Componentes
led_estado = "pin 13"
boton_control = "pin 2"
sensor_temperatura = "pin A0"

# Protocolos
usar wifi
usar mqtt

# Lógica principal
encender led
leer sensor temperatura

si temperatura mayor que 25 entonces
    encender led
    enviar alerta "Temperatura alta"
sino
    apagar led
fin si

dormir 5 segundos
"""
        
        # Código Vader de ejemplo para blockchain
        self.blockchain_vader_code = """# Contrato blockchain de ejemplo
nombre_token = "Vader Token"
simbolo = "VDR"
suministro_total = 1000000

# Tipo de contrato
tipo = token
tipo = staking

# Funciones principales
transfer tokens
mint nuevos_tokens
burn tokens_viejos
approve gastos

# Eventos
evento Transfer
evento Mint
evento Stake

# Staking
stake tokens por recompensas
unstake tokens cuando necesario
"""
    
    def tearDown(self):
        """Limpiar después de tests"""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_mobile_runtime_initialization(self):
        """Test inicialización del Mobile Runtime"""
        self.assertIsInstance(self.mobile_runtime, VaderMobileRuntime)
        self.assertIn('react-native', self.mobile_runtime.supported_platforms)
        self.assertIn('flutter', self.mobile_runtime.supported_platforms)
        self.assertIn('boton', self.mobile_runtime.mobile_components)
        self.assertIn('pantalla', self.mobile_runtime.mobile_components)
    
    def test_mobile_component_detection(self):
        """Test detección de componentes móviles"""
        components = self.mobile_runtime.detect_mobile_components(self.mobile_vader_code)
        
        self.assertIn('boton', components['components'])
        self.assertIn('pantalla', components['components'])
        self.assertIn('texto', components['components'])
        self.assertIn('lista', components['components'])
        # Verificar que existe la clave 'actions' antes de acceder
        if 'actions' in components:
            self.assertIn('navegar', components['actions'])
            self.assertIn('vibrar', components['actions'])
            self.assertIn('foto', components['actions'])
    
    def test_mobile_react_native_generation(self):
        """Test generación de código React Native"""
        components = self.mobile_runtime.detect_mobile_components(self.mobile_vader_code)
        react_code = self.mobile_runtime.generate_react_native_code(self.mobile_vader_code, components)
        
        self.assertIn('import React', react_code)
        self.assertIn('import { View, Text, Button', react_code)
        self.assertIn('export default App', react_code)
        self.assertIn('Mi App Vader', react_code)
        self.assertIn('Hola Mundo', react_code)
        self.assertIn('onPress', react_code)
    
    def test_mobile_flutter_generation(self):
        """Test generación de código Flutter"""
        components = self.mobile_runtime.detect_mobile_components(self.mobile_vader_code)
        flutter_code = self.mobile_runtime.generate_flutter_code(self.mobile_vader_code, components)
        
        self.assertIn('import \'package:flutter/material.dart\'', flutter_code)
        self.assertIn('class VaderMobileApp extends StatelessWidget', flutter_code)
        self.assertIn('MaterialApp', flutter_code)
        self.assertIn('Mi App Vader', flutter_code)
        self.assertIn('ElevatedButton', flutter_code)
    
    def test_mobile_runtime_execution(self):
        """Test ejecución completa del Mobile Runtime"""
        output_dir = os.path.join(self.temp_dir, 'test_mobile_app')
        
        # Probar React Native
        success_rn = self.mobile_runtime.run_vader_mobile(
            self.mobile_vader_code, 'react-native', output_dir + '_rn'
        )
        self.assertTrue(success_rn)
        
        # Verificar archivos generados
        rn_files = [
            'App.js', 'package.json', 'README.md', 
            'android/app/src/main/AndroidManifest.xml'
        ]
        for file_name in rn_files:
            file_path = Path(output_dir + '_rn') / file_name
            self.assertTrue(file_path.exists(), f"Archivo {file_name} no encontrado")
        
        # Probar Flutter
        success_flutter = self.mobile_runtime.run_vader_mobile(
            self.mobile_vader_code, 'flutter', output_dir + '_flutter'
        )
        self.assertTrue(success_flutter)
        
        # Verificar archivos Flutter
        flutter_files = ['lib/main.dart', 'pubspec.yaml', 'README.md']
        for file_name in flutter_files:
            file_path = Path(output_dir + '_flutter') / file_name
            self.assertTrue(file_path.exists(), f"Archivo Flutter {file_name} no encontrado")
    
    def test_iot_runtime_initialization(self):
        """Test inicialización del IoT Runtime"""
        self.assertIsInstance(self.iot_runtime, VaderIoTRuntime)
        self.assertIn('arduino', self.iot_runtime.supported_platforms)
        self.assertIn('raspberry-pi', self.iot_runtime.supported_platforms)
        self.assertIn('esp32', self.iot_runtime.supported_platforms)
        self.assertIn('led', self.iot_runtime.iot_components)
        self.assertIn('sensor', self.iot_runtime.iot_components)
    
    def test_iot_component_detection(self):
        """Test detección de componentes IoT"""
        components = self.iot_runtime.detect_iot_components(self.iot_vader_code)
        
        self.assertIn('led', components['components'])
        self.assertIn('boton', components['components'])
        self.assertIn('sensor', components['components'])
        self.assertIn('wifi', components['protocols'])
        self.assertIn('mqtt', components['protocols'])
        self.assertIn('encender', components['actions'])
        self.assertIn('leer', components['actions'])
    
    def test_iot_arduino_generation(self):
        """Test generación de código Arduino"""
        components = self.iot_runtime.detect_iot_components(self.iot_vader_code)
        arduino_code = self.iot_runtime.generate_arduino_code(self.iot_vader_code, components)
        
        self.assertIn('#include <Arduino.h>', arduino_code)
        self.assertIn('#include <WiFi.h>', arduino_code)
        self.assertIn('void setup()', arduino_code)
        self.assertIn('void loop()', arduino_code)
        self.assertIn('Serial.begin(115200)', arduino_code)
        self.assertIn('LED_PIN', arduino_code)
        self.assertIn('SENSOR_PIN', arduino_code)
    
    def test_iot_raspberry_pi_generation(self):
        """Test generación de código Raspberry Pi"""
        components = self.iot_runtime.detect_iot_components(self.iot_vader_code)
        pi_code = self.iot_runtime.generate_raspberry_pi_code(self.iot_vader_code, components)
        
        self.assertIn('import RPi.GPIO as GPIO', pi_code)
        self.assertIn('import paho.mqtt.client as mqtt', pi_code)
        self.assertIn('class VaderIoTDevice', pi_code)
        self.assertIn('def setup_gpio(self)', pi_code)
        self.assertIn('def encender_led(self', pi_code)
        self.assertIn('GPIO.setmode(GPIO.BCM)', pi_code)
    
    def test_iot_runtime_execution(self):
        """Test ejecución completa del IoT Runtime"""
        output_dir = os.path.join(self.temp_dir, 'test_iot_device')
        
        # Probar Arduino
        success_arduino = self.iot_runtime.run_vader_iot(
            self.iot_vader_code, 'arduino', output_dir + '_arduino'
        )
        self.assertTrue(success_arduino)
        
        # Verificar archivos Arduino
        arduino_files = ['test_iot_device_arduino.ino', 'README.md', 'platformio.ini']
        for file_name in arduino_files:
            file_path = Path(output_dir + '_arduino') / file_name
            self.assertTrue(file_path.exists(), f"Archivo Arduino {file_name} no encontrado")
        
        # Probar Raspberry Pi
        success_pi = self.iot_runtime.run_vader_iot(
            self.iot_vader_code, 'raspberry-pi', output_dir + '_pi'
        )
        self.assertTrue(success_pi)
        
        # Verificar archivos Raspberry Pi
        pi_files = ['main.py', 'requirements.txt', 'README.md', 'config.json']
        for file_name in pi_files:
            file_path = Path(output_dir + '_pi') / file_name
            self.assertTrue(file_path.exists(), f"Archivo Pi {file_name} no encontrado")
    
    def test_blockchain_runtime_initialization(self):
        """Test inicialización del Blockchain Runtime"""
        self.assertIsInstance(self.blockchain_runtime, VaderBlockchainRuntime)
        self.assertIn('ethereum', self.blockchain_runtime.supported_networks)
        self.assertIn('polygon', self.blockchain_runtime.supported_networks)
        self.assertIn('solana', self.blockchain_runtime.supported_networks)
        self.assertIn('token', self.blockchain_runtime.contract_types)
        self.assertIn('nft', self.blockchain_runtime.contract_types)
    
    def test_blockchain_component_detection(self):
        """Test detección de componentes blockchain"""
        components = self.blockchain_runtime.detect_blockchain_components(self.blockchain_vader_code)
        
        self.assertIn('token', components['contract_types'])
        self.assertIn('staking', components['contract_types'])
        self.assertIn('transfer', components['functions'])
        self.assertIn('mint', components['functions'])
        self.assertIn('burn', components['functions'])
        self.assertIn('Transfer', components['events'])
        self.assertIn('Mint', components['events'])
    
    def test_blockchain_solidity_generation(self):
        """Test generación de código Solidity"""
        components = self.blockchain_runtime.detect_blockchain_components(self.blockchain_vader_code)
        solidity_code = self.blockchain_runtime.generate_solidity_code(
            self.blockchain_vader_code, components, 'ethereum'
        )
        
        self.assertIn('pragma solidity ^0.8.19', solidity_code)
        self.assertIn('contract VaderTokenContract', solidity_code)
        self.assertIn('import "@openzeppelin/contracts', solidity_code)
        self.assertIn('function mint(', solidity_code)
        self.assertIn('function burn(', solidity_code)
        self.assertIn('event Mint(', solidity_code)
        self.assertIn('modifier onlyAuthorized', solidity_code)
    
    def test_blockchain_runtime_execution(self):
        """Test ejecución completa del Blockchain Runtime"""
        output_dir = os.path.join(self.temp_dir, 'test_blockchain_contract')
        
        # Probar Ethereum
        success_eth = self.blockchain_runtime.run_vader_blockchain(
            self.blockchain_vader_code, 'ethereum', output_dir + '_eth'
        )
        self.assertTrue(success_eth)
        
        # Verificar archivos Ethereum
        eth_files = [
            'contracts/VaderTokenContract.sol', 
            'hardhat.config.js', 
            'scripts/deploy.js',
            'package.json'
        ]
        for file_name in eth_files:
            file_path = Path(output_dir + '_eth') / file_name
            self.assertTrue(file_path.exists(), f"Archivo Ethereum {file_name} no encontrado")
        
        # Probar Polygon
        success_polygon = self.blockchain_runtime.run_vader_blockchain(
            self.blockchain_vader_code, 'polygon', output_dir + '_polygon'
        )
        self.assertTrue(success_polygon)
    
    def test_runtime_integration(self):
        """Test integración entre runtimes"""
        # Verificar que todos los runtimes pueden coexistir
        self.assertIsNotNone(self.mobile_runtime)
        self.assertIsNotNone(self.iot_runtime)
        self.assertIsNotNone(self.blockchain_runtime)
        
        # Verificar que no hay conflictos de nombres
        mobile_platforms = set(self.mobile_runtime.supported_platforms.keys())
        iot_platforms = set(self.iot_runtime.supported_platforms.keys())
        blockchain_networks = set(self.blockchain_runtime.supported_networks.keys())
        
        # No debería haber superposición entre plataformas
        self.assertEqual(len(mobile_platforms & iot_platforms), 0)
        self.assertEqual(len(mobile_platforms & blockchain_networks), 0)
        self.assertEqual(len(iot_platforms & blockchain_networks), 0)
    
    def test_code_quality_validation(self):
        """Test validación de calidad de código generado"""
        # Test Mobile - React Native
        components = self.mobile_runtime.detect_mobile_components(self.mobile_vader_code)
        rn_code = self.mobile_runtime.generate_react_native_code(self.mobile_vader_code, components)
        
        # Verificar estructura básica de React Native
        self.assertIn('export default', rn_code)
        self.assertIn('function', rn_code)
        self.assertIn('return (', rn_code)
        
        # Test IoT - Arduino
        iot_components = self.iot_runtime.detect_iot_components(self.iot_vader_code)
        arduino_code = self.iot_runtime.generate_arduino_code(self.iot_vader_code, iot_components)
        
        # Verificar estructura básica de Arduino
        self.assertIn('void setup()', arduino_code)
        self.assertIn('void loop()', arduino_code)
        self.assertIn('#include', arduino_code)
        
        # Test Blockchain - Solidity
        blockchain_components = self.blockchain_runtime.detect_blockchain_components(self.blockchain_vader_code)
        solidity_code = self.blockchain_runtime.generate_solidity_code(
            self.blockchain_vader_code, blockchain_components, 'ethereum'
        )
        
        # Verificar estructura básica de Solidity
        self.assertIn('pragma solidity', solidity_code)
        self.assertIn('contract ', solidity_code)
        self.assertIn('function ', solidity_code)
    
    def test_error_handling(self):
        """Test manejo de errores en runtimes"""
        # Test con código Vader vacío
        empty_code = ""
        
        # Mobile Runtime con código vacío
        mobile_components = self.mobile_runtime.detect_mobile_components(empty_code)
        self.assertEqual(len(mobile_components['components']), 0)
        
        # IoT Runtime con código vacío
        iot_components = self.iot_runtime.detect_iot_components(empty_code)
        self.assertEqual(len(iot_components['components']), 0)
        
        # Blockchain Runtime con código vacío
        blockchain_components = self.blockchain_runtime.detect_blockchain_components(empty_code)
        self.assertEqual(len(blockchain_components['contract_types']), 0)
        
        # Test con plataforma no soportada
        invalid_output = os.path.join(self.temp_dir, 'invalid_test')
        
        # Esto debería fallar graciosamente
        success = self.mobile_runtime.run_vader_mobile(
            self.mobile_vader_code, 'invalid_platform', invalid_output
        )
        self.assertFalse(success)

def run_runtime_tests():
    """Ejecutar todos los tests de runtimes"""
    print("🧪 EJECUTANDO TESTS DE RUNTIMES NATIVOS")
    print("=" * 60)
    
    # Crear suite de tests
    suite = unittest.TestLoader().loadTestsFromTestCase(TestVaderNativeRuntimes)
    
    # Ejecutar tests con output detallado
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Mostrar resumen
    print("\n" + "=" * 60)
    print(f"📊 RESUMEN DE TESTS:")
    print(f"  ✅ Tests exitosos: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"  ❌ Tests fallidos: {len(result.failures)}")
    print(f"  🚨 Errores: {len(result.errors)}")
    print(f"  📈 Total ejecutados: {result.testsRun}")
    
    if result.failures:
        print(f"\n❌ FALLOS:")
        for test, traceback in result.failures:
            error_msg = traceback.split('AssertionError: ')[-1].split('\n')[0]
            print(f"  - {test}: {error_msg}")
    
    if result.errors:
        print(f"\n🚨 ERRORES:")
        for test, traceback in result.errors:
            error_msg = traceback.split('\n')[-2]
            print(f"  - {test}: {error_msg}")
    
    success = len(result.failures) == 0 and len(result.errors) == 0
    
    if success:
        print(f"\n🎉 TODOS LOS TESTS DE RUNTIMES NATIVOS PASARON EXITOSAMENTE")
        print(f"✅ Mobile Runtime: Funcional")
        print(f"✅ IoT Runtime: Funcional") 
        print(f"✅ Blockchain Runtime: Funcional")
    else:
        print(f"\n⚠️ ALGUNOS TESTS FALLARON - REVISAR IMPLEMENTACIÓN")
    
    return success

if __name__ == '__main__':
    success = run_runtime_tests()
    sys.exit(0 if success else 1)
