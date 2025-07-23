#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VADER 7.0 UNIVERSAL CLI ENHANCED

CLI unificado para ejecutar archivos .vdr en cualquier plataforma/contexto
con detección automática del runtime apropiado y ejecución nativa.

Uso:
    vader <archivo.vdr> [plataforma] [opciones]

Ejemplos:
    vader mi_app.vdr                    # Detección automática
    vader mi_api.vdr aws_lambda         # AWS Lambda específico
    vader mi_iot.vdr arduino            # Arduino específico
    vader mi_web.vdr react              # React específico

Autor: Vader Universal Runtime Team
Versión: 7.0.0 Universal CLI Enhanced
Fecha: Julio 2025
"""

import sys
import os
import json
import time
import subprocess
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime

# Configuración del CLI Universal
VADER_VERSION = "7.0.0"
VADER_CLI_VERSION = "1.0.0"
VADER_SLOGAN = "LA PROGRAMACIÓN UNIVERSAL: Libre, Descentralizada, Accesible"

class VaderUniversalCLI:
    """CLI Universal para todos los runtimes de Vader 7.0"""
    
    def __init__(self):
        self.version = VADER_VERSION
        self.cli_version = VADER_CLI_VERSION
        self.slogan = VADER_SLOGAN
        
        # Mapeo de runtimes disponibles
        self.runtimes = {
            # Runtimes Enhanced (auditados y mejorados)
            'python': {
                'file': 'vader-7.0-universal-python-enhanced.py',
                'platforms': ['python', 'django', 'flask', 'fastapi', 'jupyter', 'pandas', 'tensorflow'],
                'description': 'Runtime Python Enhanced con soporte para frameworks web y ML',
                'enhanced': True
            },
            'javascript': {
                'file': 'vader-7.0-universal-js-enhanced.js',
                'platforms': ['web', 'react', 'vue', 'angular', 'node', 'express', 'electron'],
                'description': 'Runtime JavaScript Enhanced para web y aplicaciones',
                'enhanced': True
            },
            'iot': {
                'file': 'vader-7.0-universal-iot-enhanced.py',
                'platforms': ['arduino', 'esp32', 'esp8266', 'raspberry_pi', 'microbit'],
                'description': 'Runtime IoT Enhanced para dispositivos inteligentes',
                'enhanced': True
            },
            'cloud': {
                'file': 'vader-7.0-universal-cloud-enhanced.py',
                'platforms': ['aws_lambda', 'vercel', 'netlify', 'azure_functions', 'google_cloud'],
                'description': 'Runtime Cloud Enhanced para plataformas serverless',
                'enhanced': True
            },
            
            # Runtimes Originales (funcionales, pendientes de migración Enhanced)
            'ai': {
                'file': 'vader-7.0-universal-ai.py',
                'platforms': ['openai', 'anthropic', 'huggingface', 'ollama', 'local'],
                'description': 'Runtime AI para modelos de inteligencia artificial',
                'enhanced': False
            },
            'mobile': {
                'file': 'vader-7.0-universal-mobile.py',
                'platforms': ['react_native', 'flutter', 'ionic', 'xamarin'],
                'description': 'Runtime móvil para iOS y Android',
                'enhanced': False
            },
            'gaming': {
                'file': 'vader-7.0-universal-gaming.py',
                'platforms': ['unity', 'godot', 'pygame', 'phaser'],
                'description': 'Runtime gaming para desarrollo de videojuegos',
                'enhanced': False
            },
            'blockchain': {
                'file': 'vader-7.0-universal-blockchain.py',
                'platforms': ['ethereum', 'solana', 'polygon', 'web3'],
                'description': 'Runtime blockchain para contratos inteligentes',
                'enhanced': False
            },
            'desktop': {
                'file': 'vader-7.0-universal-desktop.py',
                'platforms': ['electron', 'tauri', 'flutter_desktop', 'qt'],
                'description': 'Runtime desktop para aplicaciones de escritorio',
                'enhanced': False
            },
            'database': {
                'file': 'vader-7.0-universal-database.py',
                'platforms': ['mysql', 'mongodb', 'postgresql', 'graphql'],
                'description': 'Runtime database para bases de datos',
                'enhanced': False
            },
            'creative': {
                'file': 'vader-7.0-universal-creative.py',
                'platforms': ['blender', 'gimp', 'audacity', 'ffmpeg'],
                'description': 'Runtime creative para herramientas multimedia',
                'enhanced': False
            },
            'robotics': {
                'file': 'vader-7.0-universal-robotics.py',
                'platforms': ['ros', 'arduino_ide', 'raspberry_pi'],
                'description': 'Runtime robotics para sistemas robóticos',
                'enhanced': False
            },
            'datascience': {
                'file': 'vader-7.0-universal-datascience.py',
                'platforms': ['jupyter', 'r', 'matlab', 'pandas'],
                'description': 'Runtime data science para análisis de datos',
                'enhanced': False
            },
            'edge': {
                'file': 'vader-7.0-universal-edge.py',
                'platforms': ['webassembly', 'cloudflare_workers', 'vercel_edge', 'netlify_edge'],
                'description': 'Runtime edge computing para computación distribuida',
                'enhanced': False
            }
        }
        
        # Contextos automáticos para detección inteligente
        self.context_detection = {
            'web': ['html', 'css', 'javascript', 'react', 'vue', 'angular'],
            'mobile': ['react native', 'flutter', 'ionic', 'app', 'móvil'],
            'iot': ['arduino', 'esp32', 'raspberry', 'sensor', 'actuador'],
            'cloud': ['aws', 'lambda', 'vercel', 'netlify', 'serverless'],
            'ai': ['ai', 'ia', 'modelo', 'prompt', 'openai', 'gpt'],
            'gaming': ['unity', 'godot', 'juego', 'game', 'pygame'],
            'blockchain': ['ethereum', 'solana', 'web3', 'smart contract'],
            'desktop': ['electron', 'tauri', 'desktop', 'gui'],
            'database': ['database', 'sql', 'mongodb', 'mysql'],
            'creative': ['blender', 'gimp', 'audio', 'video', 'imagen'],
            'robotics': ['robot', 'ros', 'robótica', 'automation'],
            'datascience': ['data', 'análisis', 'jupyter', 'pandas', 'ml'],
            'edge': ['edge', 'webassembly', 'cdn', 'workers']
        }
        
        print(f"🚀 VADER {self.version} - CLI Universal Enhanced v{self.cli_version}")
        print(f"⚡ {self.slogan}")
        print()
    
    def detect_runtime_from_code(self, code: str) -> str:
        """Detecta automáticamente el runtime apropiado basado en el contenido"""
        code_lower = code.lower()
        
        # Puntuación por contexto
        context_scores = {}
        
        for context, keywords in self.context_detection.items():
            score = 0
            for keyword in keywords:
                if keyword in code_lower:
                    score += code_lower.count(keyword)
            context_scores[context] = score
        
        # Encontrar el contexto con mayor puntuación
        if context_scores:
            best_context = max(context_scores.items(), key=lambda x: x[1])
            if best_context[1] > 0:
                return best_context[0]
        
        # Default: Python si no se detecta nada específico
        return 'python'
    
    def get_available_platforms(self) -> List[str]:
        """Obtiene todas las plataformas disponibles"""
        platforms = []
        for runtime_info in self.runtimes.values():
            platforms.extend(runtime_info['platforms'])
        return sorted(list(set(platforms)))
    
    def find_runtime_for_platform(self, platform: str) -> Optional[str]:
        """Encuentra el runtime apropiado para una plataforma específica"""
        for runtime_name, runtime_info in self.runtimes.items():
            if platform in runtime_info['platforms']:
                return runtime_name
        return None
    
    def validate_vdr_file(self, file_path: str) -> Tuple[bool, str]:
        """Valida un archivo .vdr"""
        if not os.path.exists(file_path):
            return False, f"Archivo no encontrado: {file_path}"
        
        if not file_path.endswith('.vdr'):
            return False, f"El archivo debe tener extensión .vdr: {file_path}"
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if not content.strip():
                return False, f"El archivo está vacío: {file_path}"
            
            return True, "Archivo válido"
            
        except Exception as e:
            return False, f"Error leyendo archivo: {str(e)}"
    
    def execute_runtime(self, runtime_name: str, vdr_file: str, platform: str, options: Dict) -> Tuple[bool, str]:
        """Ejecuta un runtime específico"""
        runtime_info = self.runtimes.get(runtime_name)
        if not runtime_info:
            return False, f"Runtime no encontrado: {runtime_name}"
        
        runtime_file = runtime_info['file']
        runtime_path = os.path.join(os.getcwd(), runtime_file)
        
        if not os.path.exists(runtime_path):
            return False, f"Archivo de runtime no encontrado: {runtime_path}"
        
        try:
            print(f"🎯 Ejecutando runtime: {runtime_name}")
            print(f"📁 Archivo: {vdr_file}")
            print(f"🚀 Plataforma: {platform}")
            print(f"{'🌟 Enhanced' if runtime_info['enhanced'] else '📦 Original'}")
            print("=" * 60)
            
            # Construir comando
            if runtime_file.endswith('.py'):
                cmd = ['python3', runtime_path, vdr_file, platform]
            elif runtime_file.endswith('.js'):
                cmd = ['node', runtime_path, vdr_file, platform]
            else:
                return False, f"Tipo de runtime no soportado: {runtime_file}"
            
            # Agregar opciones adicionales
            if options.get('verbose'):
                cmd.append('--verbose')
            
            # Ejecutar comando
            start_time = time.time()
            result = subprocess.run(cmd, capture_output=True, text=True)
            execution_time = time.time() - start_time
            
            # Mostrar salida
            if result.stdout:
                print(result.stdout)
            
            if result.stderr:
                print("⚠️ Advertencias/Errores:")
                print(result.stderr)
            
            print("=" * 60)
            print(f"⏱️ Tiempo total de ejecución: {execution_time:.3f}s")
            print(f"🎯 Código de salida: {result.returncode}")
            
            if result.returncode == 0:
                print("✅ Ejecución completada exitosamente")
                return True, "Éxito"
            else:
                print("❌ Ejecución falló")
                return False, f"Error de ejecución (código {result.returncode})"
                
        except Exception as e:
            return False, f"Error ejecutando runtime: {str(e)}"
    
    def show_help(self):
        """Muestra ayuda del CLI"""
        print(f"🚀 VADER {self.version} - CLI Universal Enhanced")
        print(f"⚡ {self.slogan}")
        print()
        print("USO:")
        print("  vader <archivo.vdr> [plataforma] [opciones]")
        print()
        print("EJEMPLOS:")
        print("  vader mi_app.vdr                    # Detección automática")
        print("  vader mi_api.vdr aws_lambda         # AWS Lambda específico")
        print("  vader mi_iot.vdr arduino            # Arduino específico")
        print("  vader mi_web.vdr react              # React específico")
        print("  vader mi_ai.vdr openai --verbose    # OpenAI con verbose")
        print()
        print("RUNTIMES DISPONIBLES:")
        
        # Mostrar runtimes Enhanced primero
        print("\n🌟 RUNTIMES ENHANCED (Auditados y Mejorados):")
        for name, info in self.runtimes.items():
            if info['enhanced']:
                platforms = ', '.join(info['platforms'][:3])
                if len(info['platforms']) > 3:
                    platforms += f" (+{len(info['platforms'])-3} más)"
                print(f"  {name:12} - {info['description']}")
                print(f"               Plataformas: {platforms}")
        
        # Mostrar runtimes originales
        print("\n📦 RUNTIMES ORIGINALES (Funcionales, migración pendiente):")
        for name, info in self.runtimes.items():
            if not info['enhanced']:
                platforms = ', '.join(info['platforms'][:3])
                if len(info['platforms']) > 3:
                    platforms += f" (+{len(info['platforms'])-3} más)"
                print(f"  {name:12} - {info['description']}")
                print(f"               Plataformas: {platforms}")
        
        print()
        print("OPCIONES:")
        print("  --help, -h          Mostrar esta ayuda")
        print("  --version, -v       Mostrar versión")
        print("  --list, -l          Listar todas las plataformas")
        print("  --verbose           Modo verbose")
        print("  --auto              Detección automática (default)")
        print()
        print("PLATAFORMAS SOPORTADAS:")
        platforms = self.get_available_platforms()
        for i in range(0, len(platforms), 4):
            row = platforms[i:i+4]
            print("  " + "  ".join(f"{p:15}" for p in row))
        print()
        print("🎯 Para más información: https://github.com/LangVader/core")
    
    def show_version(self):
        """Muestra información de versión"""
        print(f"🚀 VADER Universal Runtime: {self.version}")
        print(f"🛠️ CLI Enhanced: {self.cli_version}")
        print(f"⚡ {self.slogan}")
        print()
        print("📊 ESTADÍSTICAS:")
        enhanced_count = sum(1 for info in self.runtimes.values() if info['enhanced'])
        original_count = len(self.runtimes) - enhanced_count
        total_platforms = len(self.get_available_platforms())
        
        print(f"  Runtimes Enhanced: {enhanced_count}")
        print(f"  Runtimes Originales: {original_count}")
        print(f"  Total Runtimes: {len(self.runtimes)}")
        print(f"  Plataformas soportadas: {total_platforms}")
        print()
        print("🌟 Estado: Universalidad Total Absoluta Completada")
    
    def run(self, args: List[str]):
        """Función principal del CLI"""
        if not args:
            self.show_help()
            return 1
        
        # Parsear argumentos
        if args[0] in ['--help', '-h', 'help']:
            self.show_help()
            return 0
        
        if args[0] in ['--version', '-v', 'version']:
            self.show_version()
            return 0
        
        if args[0] in ['--list', '-l', 'list']:
            print("🌐 PLATAFORMAS DISPONIBLES:")
            for platform in self.get_available_platforms():
                runtime_name = self.find_runtime_for_platform(platform)
                runtime_info = self.runtimes.get(runtime_name, {})
                enhanced = "🌟" if runtime_info.get('enhanced') else "📦"
                print(f"  {enhanced} {platform:20} ({runtime_name})")
            return 0
        
        # Validar archivo .vdr
        vdr_file = args[0]
        is_valid, message = self.validate_vdr_file(vdr_file)
        if not is_valid:
            print(f"❌ Error: {message}")
            return 1
        
        # Determinar plataforma
        platform = None
        options = {'verbose': '--verbose' in args}
        
        if len(args) > 1 and not args[1].startswith('--'):
            platform = args[1]
        
        # Detección automática si no se especifica plataforma
        if not platform:
            try:
                with open(vdr_file, 'r', encoding='utf-8') as f:
                    code = f.read()
                
                detected_runtime = self.detect_runtime_from_code(code)
                # Usar la primera plataforma del runtime detectado
                platform = self.runtimes[detected_runtime]['platforms'][0]
                
                print(f"🔍 Detección automática:")
                print(f"  Runtime detectado: {detected_runtime}")
                print(f"  Plataforma seleccionada: {platform}")
                print()
                
            except Exception as e:
                print(f"❌ Error en detección automática: {str(e)}")
                return 1
        
        # Encontrar runtime apropiado
        runtime_name = self.find_runtime_for_platform(platform)
        if not runtime_name:
            print(f"❌ Error: Plataforma no soportada: {platform}")
            print("💡 Usa 'vader --list' para ver plataformas disponibles")
            return 1
        
        # Ejecutar runtime
        success, message = self.execute_runtime(runtime_name, vdr_file, platform, options)
        
        if success:
            print(f"\n🎉 ¡Archivo .vdr ejecutado exitosamente para {platform}!")
            print("⚡ VADER: La programación universal enhanced")
            return 0
        else:
            print(f"\n💥 Error: {message}")
            return 1

def main():
    """Función principal"""
    try:
        cli = VaderUniversalCLI()
        return cli.run(sys.argv[1:])
    except KeyboardInterrupt:
        print("\n🛑 Ejecución interrumpida por el usuario")
        return 130
    except Exception as e:
        print(f"💥 Error fatal: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
