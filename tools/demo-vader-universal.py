#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VADER 7.0 UNIVERSAL DEMO INTERACTIVO

Demo interactivo que muestra todos los runtimes de Vader 7.0 en acción,
permitiendo al usuario probar diferentes plataformas y ver la ejecución
nativa de archivos .vdr en tiempo real.

Características:
- Interfaz interactiva en terminal
- Ejemplos predefinidos para cada runtime
- Ejecución en tiempo real
- Métricas de rendimiento
- Comparación entre runtimes

Autor: Vader Universal Runtime Team
Versión: 7.0.0 Universal Demo Enhanced
Fecha: Julio 2025
"""

import sys
import os
import time
import subprocess
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import tempfile

# Configuración del demo
VADER_VERSION = "7.0.0"
DEMO_VERSION = "1.0.0"
VADER_SLOGAN = "LA PROGRAMACIÓN UNIVERSAL: Libre, Descentralizada, Accesible"

class VaderUniversalDemo:
    """Demo Interactivo Universal para Vader 7.0"""
    
    def __init__(self):
        self.version = VADER_VERSION
        self.demo_version = DEMO_VERSION
        self.slogan = VADER_SLOGAN
        
        # Ejemplos de código .vdr para cada runtime
        self.examples = {
            'python': {
                'name': '🐍 Python Enhanced',
                'description': 'Aplicación web con Flask y análisis de datos',
                'code': '''// Vader 7.0 - Aplicación Python Enhanced
configurar servidor web flask
crear api rest "/datos"
mostrar dashboard con pandas
procesar datos csv
generar gráficos matplotlib
ejecutar análisis estadístico
'''
            },
            'javascript': {
                'name': '🟨 JavaScript Enhanced',
                'description': 'Aplicación React con componentes interactivos',
                'code': '''// Vader 7.0 - Aplicación React Enhanced
crear componente react "Dashboard"
mostrar header navegación
configurar estado con hooks
fetch datos api externa
renderizar tabla interactiva
manejar eventos click
'''
            },
            'iot': {
                'name': '🤖 IoT Enhanced',
                'description': 'Sistema Arduino con sensores y actuadores',
                'code': '''// Vader 7.0 - Sistema IoT Enhanced
configurar arduino uno
leer sensor temperatura dht22 pin 2
leer sensor humedad dht22 pin 2
controlar led rgb pin 9
activar buzzer pin 8
mostrar datos serial monitor
'''
            },
            'cloud': {
                'name': '☁️ Cloud Enhanced',
                'description': 'API serverless en AWS Lambda',
                'code': '''// Vader 7.0 - API Cloud Enhanced
crear función lambda handler
configurar api gateway
conectar database dynamodb
implementar autenticación jwt
procesar requests http
responder json formato
'''
            },
            'ai': {
                'name': '🧠 AI Universal',
                'description': 'Integración con modelos de IA',
                'code': '''// Vader 7.0 - Sistema AI Universal
configurar modelo openai gpt-4
crear prompt análisis texto
procesar respuesta ia
generar resumen automático
traducir múltiples idiomas
mostrar resultados json
'''
            },
            'mobile': {
                'name': '📱 Mobile Universal',
                'description': 'App móvil multiplataforma',
                'code': '''// Vader 7.0 - App Mobile Universal
crear app react native
configurar navegación stack
mostrar pantalla login
implementar formulario
conectar api backend
guardar datos locales
'''
            },
            'gaming': {
                'name': '🎮 Gaming Universal',
                'description': 'Juego 2D con Unity',
                'code': '''// Vader 7.0 - Juego Gaming Universal
crear escena unity 2d
configurar personaje player
implementar movimiento wasd
detectar colisiones
mostrar puntuación ui
reproducir efectos sonido
'''
            },
            'blockchain': {
                'name': '⛓️ Blockchain Universal',
                'description': 'Smart contract en Ethereum',
                'code': '''// Vader 7.0 - Blockchain Universal
crear contrato ethereum
definir token erc20
implementar función transfer
configurar eventos logs
desplegar red testnet
interactuar web3 js
'''
            }
        }
        
        # Métricas de rendimiento
        self.metrics = {}
        
        print(f"🚀 VADER {self.version} - Demo Universal Enhanced v{self.demo_version}")
        print(f"⚡ {self.slogan}")
        print()
    
    def show_welcome(self):
        """Muestra la pantalla de bienvenida"""
        print("="*70)
        print("🌟 BIENVENIDO AL DEMO INTERACTIVO DE VADER 7.0 UNIVERSAL RUNTIME")
        print("="*70)
        print()
        print("Este demo te permite explorar todos los runtimes de Vader 7.0 y ver")
        print("cómo los archivos .vdr se ejecutan nativamente en diferentes contextos:")
        print()
        print("🌟 RUNTIMES ENHANCED (Auditados y Mejorados):")
        print("   • Python Enhanced - Aplicaciones web y análisis de datos")
        print("   • JavaScript Enhanced - Aplicaciones React y Node.js")
        print("   • IoT Enhanced - Dispositivos Arduino y Raspberry Pi")
        print("   • Cloud Enhanced - Funciones serverless AWS/Vercel/Netlify")
        print()
        print("📦 RUNTIMES UNIVERSALES (Funcionales):")
        print("   • AI Universal - Integración con modelos de IA")
        print("   • Mobile Universal - Apps iOS/Android multiplataforma")
        print("   • Gaming Universal - Videojuegos Unity/Godot")
        print("   • Blockchain Universal - Smart contracts y Web3")
        print("   • Y muchos más...")
        print()
        print("🎯 Cada ejemplo muestra:")
        print("   ✅ Ejecución nativa sin transpilación")
        print("   ✅ Preservación de identidad .vdr")
        print("   ✅ Detección automática de contexto")
        print("   ✅ Generación de código específico")
        print("   ✅ Métricas de rendimiento")
        print()
        print("="*70)
        input("Presiona ENTER para continuar...")
        print()
    
    def show_menu(self) -> str:
        """Muestra el menú principal y retorna la opción seleccionada"""
        print("🎯 MENÚ PRINCIPAL - DEMO VADER 7.0 UNIVERSAL")
        print("="*50)
        print()
        
        options = list(self.examples.keys())
        
        for i, (key, example) in enumerate(self.examples.items(), 1):
            status = "🌟" if key in ['python', 'javascript', 'iot', 'cloud'] else "📦"
            print(f"{i:2}. {status} {example['name']}")
            print(f"     {example['description']}")
            print()
        
        print(f"{len(options)+1:2}. 📊 Ver métricas de rendimiento")
        print(f"{len(options)+2:2}. 🔄 Ejecutar benchmark completo")
        print(f"{len(options)+3:2}. ❓ Ayuda y documentación")
        print(f"{len(options)+4:2}. 🚪 Salir")
        print()
        
        while True:
            try:
                choice = input("Selecciona una opción (1-{}): ".format(len(options)+4))
                
                if choice.isdigit():
                    choice_num = int(choice)
                    if 1 <= choice_num <= len(options):
                        return options[choice_num - 1]
                    elif choice_num == len(options) + 1:
                        return 'metrics'
                    elif choice_num == len(options) + 2:
                        return 'benchmark'
                    elif choice_num == len(options) + 3:
                        return 'help'
                    elif choice_num == len(options) + 4:
                        return 'exit'
                
                print("❌ Opción inválida. Intenta de nuevo.")
                
            except (ValueError, KeyboardInterrupt):
                print("❌ Entrada inválida. Intenta de nuevo.")
    
    def create_temp_vdr_file(self, code: str) -> str:
        """Crea un archivo .vdr temporal con el código"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.vdr', delete=False, encoding='utf-8') as f:
            f.write(code)
            return f.name
    
    def execute_runtime_demo(self, runtime_key: str):
        """Ejecuta un demo específico de runtime"""
        example = self.examples[runtime_key]
        
        print(f"\n🚀 EJECUTANDO DEMO: {example['name']}")
        print("="*60)
        print(f"📝 Descripción: {example['description']}")
        print()
        print("📄 Código .vdr:")
        print("-"*40)
        print(example['code'])
        print("-"*40)
        print()
        
        # Crear archivo temporal
        temp_file = self.create_temp_vdr_file(example['code'])
        
        try:
            print("⏳ Ejecutando con CLI Universal...")
            print()
            
            # Usar el CLI universal para ejecutar
            cli_path = Path("vader-cli-universal.py")
            if not cli_path.exists():
                print("❌ CLI Universal no encontrado. Asegúrate de estar en el directorio correcto.")
                return
            
            # Determinar plataforma por defecto para cada runtime
            platform_map = {
                'python': 'python',
                'javascript': 'react',
                'iot': 'arduino',
                'cloud': 'aws_lambda',
                'ai': 'openai',
                'mobile': 'react_native',
                'gaming': 'unity',
                'blockchain': 'ethereum'
            }
            
            platform = platform_map.get(runtime_key, 'python')
            
            # Ejecutar comando
            start_time = time.time()
            
            cmd = ['python3', str(cli_path), temp_file, platform]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            execution_time = time.time() - start_time
            
            # Mostrar resultados
            if result.stdout:
                print(result.stdout)
            
            if result.stderr:
                print("⚠️ Advertencias:")
                print(result.stderr)
            
            # Guardar métricas
            self.metrics[runtime_key] = {
                'execution_time': execution_time,
                'success': result.returncode == 0,
                'timestamp': datetime.now().isoformat(),
                'platform': platform
            }
            
            print("="*60)
            print(f"⏱️ Tiempo de ejecución: {execution_time:.3f}s")
            print(f"🎯 Estado: {'✅ ÉXITO' if result.returncode == 0 else '❌ ERROR'}")
            print(f"🚀 Plataforma: {platform}")
            
            if result.returncode == 0:
                print("🎉 ¡Demo ejecutado exitosamente!")
                print("⚡ Archivo .vdr ejecutado nativamente sin transpilación")
            else:
                print("💥 Error en la ejecución del demo")
            
        except Exception as e:
            print(f"❌ Error ejecutando demo: {str(e)}")
            
        finally:
            # Limpiar archivo temporal
            try:
                os.unlink(temp_file)
            except:
                pass
        
        print()
        input("Presiona ENTER para continuar...")
    
    def show_metrics(self):
        """Muestra métricas de rendimiento"""
        print("\n📊 MÉTRICAS DE RENDIMIENTO")
        print("="*50)
        
        if not self.metrics:
            print("❌ No hay métricas disponibles. Ejecuta algunos demos primero.")
            print()
            input("Presiona ENTER para continuar...")
            return
        
        print()
        print(f"{'Runtime':<15} {'Plataforma':<15} {'Tiempo (s)':<12} {'Estado':<8}")
        print("-"*50)
        
        total_time = 0
        success_count = 0
        
        for runtime, metrics in self.metrics.items():
            status = "✅ OK" if metrics['success'] else "❌ ERROR"
            print(f"{runtime:<15} {metrics['platform']:<15} {metrics['execution_time']:<12.3f} {status}")
            
            total_time += metrics['execution_time']
            if metrics['success']:
                success_count += 1
        
        print("-"*50)
        print(f"📊 RESUMEN:")
        print(f"   Demos ejecutados: {len(self.metrics)}")
        print(f"   Exitosos: {success_count}")
        print(f"   Tiempo total: {total_time:.3f}s")
        print(f"   Tiempo promedio: {total_time/len(self.metrics):.3f}s")
        print(f"   Tasa de éxito: {success_count/len(self.metrics)*100:.1f}%")
        
        print()
        input("Presiona ENTER para continuar...")
    
    def run_benchmark(self):
        """Ejecuta un benchmark completo de todos los runtimes"""
        print("\n🔄 EJECUTANDO BENCHMARK COMPLETO")
        print("="*50)
        print("⏳ Esto ejecutará todos los runtimes disponibles...")
        print()
        
        confirm = input("¿Continuar? (s/N): ").lower().strip()
        if confirm != 's':
            return
        
        print("\n🚀 Iniciando benchmark...")
        
        # Limpiar métricas anteriores
        self.metrics.clear()
        
        # Ejecutar cada runtime
        for i, runtime_key in enumerate(self.examples.keys(), 1):
            print(f"\n[{i}/{len(self.examples)}] Ejecutando {self.examples[runtime_key]['name']}...")
            
            # Versión silenciosa del execute_runtime_demo
            example = self.examples[runtime_key]
            temp_file = self.create_temp_vdr_file(example['code'])
            
            try:
                cli_path = Path("vader-cli-universal.py")
                platform_map = {
                    'python': 'python',
                    'javascript': 'react',
                    'iot': 'arduino',
                    'cloud': 'aws_lambda',
                    'ai': 'openai',
                    'mobile': 'react_native',
                    'gaming': 'unity',
                    'blockchain': 'ethereum'
                }
                
                platform = platform_map.get(runtime_key, 'python')
                
                start_time = time.time()
                cmd = ['python3', str(cli_path), temp_file, platform]
                result = subprocess.run(cmd, capture_output=True, text=True)
                execution_time = time.time() - start_time
                
                self.metrics[runtime_key] = {
                    'execution_time': execution_time,
                    'success': result.returncode == 0,
                    'timestamp': datetime.now().isoformat(),
                    'platform': platform
                }
                
                status = "✅" if result.returncode == 0 else "❌"
                print(f"   {status} {execution_time:.3f}s")
                
            except Exception as e:
                print(f"   ❌ Error: {str(e)}")
                self.metrics[runtime_key] = {
                    'execution_time': 0,
                    'success': False,
                    'timestamp': datetime.now().isoformat(),
                    'platform': platform
                }
            
            finally:
                try:
                    os.unlink(temp_file)
                except:
                    pass
        
        print("\n🎉 Benchmark completado!")
        self.show_metrics()
    
    def show_help(self):
        """Muestra ayuda y documentación"""
        print("\n❓ AYUDA Y DOCUMENTACIÓN")
        print("="*50)
        print()
        print("🎯 SOBRE ESTE DEMO:")
        print("   Este demo interactivo muestra las capacidades de Vader 7.0")
        print("   Universal Runtime, permitiendo ejecutar archivos .vdr nativamente")
        print("   en múltiples contextos tecnológicos sin transpilación.")
        print()
        print("🌟 RUNTIMES ENHANCED:")
        print("   Los runtimes marcados con 🌟 han sido auditados y mejorados")
        print("   con arquitectura robusta, validación automática y métricas.")
        print()
        print("📦 RUNTIMES UNIVERSALES:")
        print("   Los runtimes marcados con 📦 son funcionales y están")
        print("   pendientes de migración al patrón Enhanced.")
        print()
        print("🔧 CARACTERÍSTICAS:")
        print("   • Detección automática de contexto y idioma")
        print("   • Validación robusta de archivos .vdr")
        print("   • Generación de código específico por plataforma")
        print("   • Preservación total de identidad .vdr")
        print("   • Métricas de rendimiento en tiempo real")
        print()
        print("📚 DOCUMENTACIÓN:")
        print("   • README.md - Guía de inicio")
        print("   • AUDITORIA_RUNTIMES_ENHANCED.md - Detalles técnicos")
        print("   • https://github.com/LangVader/core - Repositorio oficial")
        print()
        print("🛠️ COMANDOS CLI:")
        print("   vader --help                    # Ayuda del CLI")
        print("   vader archivo.vdr               # Detección automática")
        print("   vader archivo.vdr plataforma    # Plataforma específica")
        print("   vader --list                    # Listar plataformas")
        print()
        input("Presiona ENTER para continuar...")
    
    def run(self):
        """Ejecuta el demo interactivo"""
        try:
            self.show_welcome()
            
            while True:
                choice = self.show_menu()
                
                if choice == 'exit':
                    print("\n👋 ¡Gracias por probar Vader 7.0 Universal Runtime!")
                    print("⚡ LA PROGRAMACIÓN UNIVERSAL: Libre, Descentralizada, Accesible")
                    print("🎯 Para más información: https://github.com/LangVader/core")
                    break
                elif choice == 'metrics':
                    self.show_metrics()
                elif choice == 'benchmark':
                    self.run_benchmark()
                elif choice == 'help':
                    self.show_help()
                elif choice in self.examples:
                    self.execute_runtime_demo(choice)
                else:
                    print("❌ Opción no válida")
                
                print()
                
        except KeyboardInterrupt:
            print("\n\n🛑 Demo interrumpido por el usuario")
            print("👋 ¡Gracias por probar Vader 7.0!")
        except Exception as e:
            print(f"\n💥 Error en el demo: {str(e)}")

def main():
    """Función principal"""
    try:
        demo = VaderUniversalDemo()
        demo.run()
        return 0
    except Exception as e:
        print(f"💥 Error fatal: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
