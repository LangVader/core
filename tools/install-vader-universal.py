#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VADER 7.0 UNIVERSAL INSTALLER ENHANCED

Instalador universal multiplataforma para Vader 7.0 que configura:
- Todos los runtimes Enhanced y originales
- CLI Universal
- Dependencias y herramientas necesarias
- Configuración de entorno
- Validación de instalación

Soporta: Windows, macOS, Linux
Autor: Vader Universal Runtime Team
Versión: 7.0.0 Universal Installer Enhanced
Fecha: Julio 2025
"""

import sys
import os
import platform
import subprocess
import json
import shutil
import urllib.request
import zipfile
import tarfile
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import tempfile

# Configuración del instalador
VADER_VERSION = "7.0.0"
INSTALLER_VERSION = "1.0.0"
VADER_REPO_URL = "https://github.com/LangVader/core"
VADER_SLOGAN = "LA PROGRAMACIÓN UNIVERSAL: Libre, Descentralizada, Accesible"

class VaderUniversalInstaller:
    """Instalador Universal para Vader 7.0 Enhanced"""
    
    def __init__(self):
        self.version = VADER_VERSION
        self.installer_version = INSTALLER_VERSION
        self.slogan = VADER_SLOGAN
        self.system = platform.system().lower()
        self.architecture = platform.machine().lower()
        
        # Directorios de instalación
        if self.system == "windows":
            self.install_dir = Path.home() / "AppData" / "Local" / "Vader"
            self.bin_dir = self.install_dir / "bin"
            self.config_dir = Path.home() / "AppData" / "Roaming" / "Vader"
        elif self.system == "darwin":  # macOS
            self.install_dir = Path.home() / ".vader"
            self.bin_dir = Path("/usr/local/bin")
            self.config_dir = Path.home() / ".config" / "vader"
        else:  # Linux
            self.install_dir = Path.home() / ".vader"
            self.bin_dir = Path.home() / ".local" / "bin"
            self.config_dir = Path.home() / ".config" / "vader"
        
        # Componentes a instalar
        self.components = {
            'core': {
                'name': 'Vader Core Runtime',
                'files': ['src/vader.py'],
                'required': True
            },
            'cli': {
                'name': 'CLI Universal Enhanced',
                'files': ['vader-cli-universal.py'],
                'required': True
            },
            'runtimes_enhanced': {
                'name': 'Runtimes Enhanced (Auditados)',
                'files': [
                    'vader-7.0-universal-python-enhanced.py',
                    'vader-7.0-universal-js-enhanced.js',
                    'vader-7.0-universal-iot-enhanced.py',
                    'vader-7.0-universal-cloud-enhanced.py'
                ],
                'required': True
            },
            'runtimes_original': {
                'name': 'Runtimes Originales',
                'files': [
                    'vader-7.0-universal-ai.py',
                    'vader-7.0-universal-mobile.py',
                    'vader-7.0-universal-gaming.py',
                    'vader-7.0-universal-blockchain.py',
                    'vader-7.0-universal-desktop.py',
                    'vader-7.0-universal-database.py',
                    'vader-7.0-universal-creative.py',
                    'vader-7.0-universal-robotics.py',
                    'vader-7.0-universal-datascience.py',
                    'vader-7.0-universal-edge.py'
                ],
                'required': False
            },
            'examples': {
                'name': 'Ejemplos y Demos',
                'files': [
                    'test_simple.vdr',
                    'demo_vader_7.0.vdr',
                    'test_ai_nativo.vdr',
                    'test_iot_nativo.vdr',
                    'test_cloud_nativo.vdr'
                ],
                'required': False
            },
            'documentation': {
                'name': 'Documentación',
                'files': [
                    'README.md',
                    'INSTALACION.md',
                    'AUDITORIA_RUNTIMES_ENHANCED.md'
                ],
                'required': False
            }
        }
        
        # Dependencias por sistema
        self.dependencies = {
            'python': {
                'command': 'python3',
                'version_check': ['--version'],
                'min_version': '3.8',
                'install_instructions': {
                    'windows': 'Descargar desde https://python.org',
                    'darwin': 'brew install python3',
                    'linux': 'sudo apt-get install python3 python3-pip'
                }
            },
            'node': {
                'command': 'node',
                'version_check': ['--version'],
                'min_version': '14.0',
                'install_instructions': {
                    'windows': 'Descargar desde https://nodejs.org',
                    'darwin': 'brew install node',
                    'linux': 'sudo apt-get install nodejs npm'
                }
            },
            'git': {
                'command': 'git',
                'version_check': ['--version'],
                'min_version': '2.0',
                'install_instructions': {
                    'windows': 'Descargar desde https://git-scm.com',
                    'darwin': 'brew install git',
                    'linux': 'sudo apt-get install git'
                }
            }
        }
        
        print(f"🚀 VADER {self.version} - Instalador Universal Enhanced v{self.installer_version}")
        print(f"⚡ {self.slogan}")
        print(f"💻 Sistema: {platform.system()} {platform.release()} ({self.architecture})")
        print()
    
    def check_system_requirements(self) -> Tuple[bool, List[str]]:
        """Verifica los requisitos del sistema"""
        print("🔍 Verificando requisitos del sistema...")
        
        issues = []
        
        # Verificar Python
        if not self.check_dependency('python'):
            issues.append("Python 3.8+ no encontrado")
        
        # Verificar Node.js (opcional pero recomendado)
        if not self.check_dependency('node'):
            print("⚠️ Node.js no encontrado (opcional para runtimes JS)")
        
        # Verificar Git (opcional)
        if not self.check_dependency('git'):
            print("⚠️ Git no encontrado (opcional para actualizaciones)")
        
        # Verificar permisos de escritura
        if not self.check_write_permissions():
            issues.append("Sin permisos de escritura en directorio de instalación")
        
        # Verificar espacio en disco
        if not self.check_disk_space():
            issues.append("Espacio insuficiente en disco (mínimo 100MB)")
        
        success = len(issues) == 0
        
        if success:
            print("✅ Todos los requisitos cumplidos")
        else:
            print("❌ Algunos requisitos no se cumplen:")
            for issue in issues:
                print(f"   • {issue}")
        
        return success, issues
    
    def check_dependency(self, dep_name: str) -> bool:
        """Verifica si una dependencia está instalada"""
        dep_info = self.dependencies.get(dep_name)
        if not dep_info:
            return False
        
        try:
            result = subprocess.run(
                [dep_info['command']] + dep_info['version_check'],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                print(f"✅ {dep_name}: {result.stdout.strip()}")
                return True
            else:
                print(f"❌ {dep_name}: No encontrado")
                return False
                
        except (subprocess.TimeoutExpired, FileNotFoundError):
            print(f"❌ {dep_name}: No encontrado")
            return False
    
    def check_write_permissions(self) -> bool:
        """Verifica permisos de escritura"""
        try:
            self.install_dir.mkdir(parents=True, exist_ok=True)
            test_file = self.install_dir / "test_write.tmp"
            test_file.write_text("test")
            test_file.unlink()
            return True
        except (PermissionError, OSError):
            return False
    
    def check_disk_space(self) -> bool:
        """Verifica espacio disponible en disco"""
        try:
            if self.system == "windows":
                import ctypes
                free_bytes = ctypes.c_ulonglong(0)
                ctypes.windll.kernel32.GetDiskFreeSpaceExW(
                    ctypes.c_wchar_p(str(self.install_dir.parent)),
                    ctypes.pointer(free_bytes),
                    None,
                    None
                )
                free_space = free_bytes.value
            else:
                stat = os.statvfs(self.install_dir.parent)
                free_space = stat.f_bavail * stat.f_frsize
            
            # Requerir al menos 100MB
            return free_space > 100 * 1024 * 1024
            
        except Exception:
            return True  # Asumir que hay espacio si no se puede verificar
    
    def create_directories(self):
        """Crea los directorios necesarios"""
        print("📁 Creando directorios de instalación...")
        
        directories = [
            self.install_dir,
            self.install_dir / "runtimes",
            self.install_dir / "examples",
            self.install_dir / "docs",
            self.config_dir,
            self.bin_dir
        ]
        
        for directory in directories:
            try:
                directory.mkdir(parents=True, exist_ok=True)
                print(f"✅ {directory}")
            except PermissionError:
                print(f"❌ Sin permisos para crear: {directory}")
                if directory == self.bin_dir and self.system != "windows":
                    print("💡 Intenta ejecutar con sudo o usa un directorio local")
                raise
    
    def install_component(self, component_name: str, component_info: Dict) -> bool:
        """Instala un componente específico"""
        print(f"📦 Instalando {component_info['name']}...")
        
        success = True
        for file_name in component_info['files']:
            source_path = Path(file_name)
            
            if not source_path.exists():
                print(f"⚠️ Archivo no encontrado: {file_name}")
                if component_info['required']:
                    success = False
                continue
            
            # Determinar directorio de destino
            if component_name == 'runtimes_enhanced' or component_name == 'runtimes_original':
                dest_dir = self.install_dir / "runtimes"
            elif component_name == 'examples':
                dest_dir = self.install_dir / "examples"
            elif component_name == 'documentation':
                dest_dir = self.install_dir / "docs"
            else:
                dest_dir = self.install_dir
            
            dest_path = dest_dir / source_path.name
            
            try:
                shutil.copy2(source_path, dest_path)
                
                # Hacer ejecutables los scripts
                if dest_path.suffix in ['.py', '.js', '.sh']:
                    dest_path.chmod(0o755)
                
                print(f"✅ {source_path.name} → {dest_path}")
                
            except Exception as e:
                print(f"❌ Error copiando {file_name}: {str(e)}")
                success = False
        
        return success
    
    def create_cli_wrapper(self):
        """Crea el wrapper del CLI para acceso global"""
        print("🔧 Configurando CLI global...")
        
        cli_source = self.install_dir / "vader-cli-universal.py"
        
        if self.system == "windows":
            # Crear archivo .bat para Windows
            wrapper_path = self.bin_dir / "vader.bat"
            wrapper_content = f'''@echo off
python "{cli_source}" %*
'''
        else:
            # Crear script shell para Unix
            wrapper_path = self.bin_dir / "vader"
            wrapper_content = f'''#!/bin/bash
python3 "{cli_source}" "$@"
'''
        
        try:
            wrapper_path.write_text(wrapper_content)
            wrapper_path.chmod(0o755)
            print(f"✅ CLI wrapper creado: {wrapper_path}")
            
            # Verificar que el directorio bin esté en PATH
            self.check_path_configuration()
            
        except Exception as e:
            print(f"❌ Error creando CLI wrapper: {str(e)}")
    
    def check_path_configuration(self):
        """Verifica y sugiere configuración de PATH"""
        path_env = os.environ.get('PATH', '')
        bin_dir_str = str(self.bin_dir)
        
        if bin_dir_str not in path_env:
            print("⚠️ El directorio bin no está en PATH")
            print("💡 Para usar 'vader' globalmente, agrega esto a tu shell:")
            
            if self.system == "windows":
                print(f"   set PATH=%PATH%;{bin_dir_str}")
                print("   O configúralo permanentemente en Variables de Entorno")
            else:
                shell_config = "~/.bashrc" if Path.home().joinpath(".bashrc").exists() else "~/.zshrc"
                print(f"   echo 'export PATH=\"{bin_dir_str}:$PATH\"' >> {shell_config}")
                print(f"   source {shell_config}")
    
    def install_python_dependencies(self):
        """Instala dependencias de Python"""
        print("🐍 Instalando dependencias de Python...")
        
        # Crear requirements.txt con todas las dependencias
        requirements = [
            "requests>=2.28.0",
            "aiohttp>=3.8.0",
            "websockets>=10.0",
            "pyyaml>=6.0",
            "click>=8.0.0",
            "rich>=12.0.0",
            "psutil>=5.9.0"
        ]
        
        requirements_path = self.install_dir / "requirements.txt"
        requirements_path.write_text('\n'.join(requirements))
        
        try:
            subprocess.run([
                "python3", "-m", "pip", "install", "-r", str(requirements_path)
            ], check=True, capture_output=True)
            print("✅ Dependencias de Python instaladas")
        except subprocess.CalledProcessError as e:
            print("⚠️ Algunas dependencias de Python no se pudieron instalar")
            print("💡 Puedes instalarlas manualmente con:")
            print(f"   pip install -r {requirements_path}")
    
    def create_config_file(self):
        """Crea archivo de configuración"""
        print("⚙️ Creando configuración...")
        
        config = {
            "version": self.version,
            "install_date": str(Path().cwd()),
            "install_dir": str(self.install_dir),
            "system": self.system,
            "architecture": self.architecture,
            "components_installed": list(self.components.keys()),
            "default_runtime": "python",
            "auto_detect": True,
            "verbose": False
        }
        
        config_file = self.config_dir / "config.json"
        config_file.write_text(json.dumps(config, indent=2))
        print(f"✅ Configuración guardada: {config_file}")
    
    def validate_installation(self) -> bool:
        """Valida que la instalación sea correcta"""
        print("🔍 Validando instalación...")
        
        # Verificar archivos principales
        essential_files = [
            self.install_dir / "vader-cli-universal.py",
            self.install_dir / "runtimes" / "vader-7.0-universal-python-enhanced.py"
        ]
        
        for file_path in essential_files:
            if not file_path.exists():
                print(f"❌ Archivo esencial faltante: {file_path}")
                return False
        
        # Probar CLI
        try:
            cli_path = self.install_dir / "vader-cli-universal.py"
            result = subprocess.run([
                "python3", str(cli_path), "--version"
            ], capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                print("✅ CLI funcional")
            else:
                print("❌ CLI no funciona correctamente")
                return False
                
        except Exception as e:
            print(f"❌ Error probando CLI: {str(e)}")
            return False
        
        print("✅ Instalación validada correctamente")
        return True
    
    def show_installation_summary(self):
        """Muestra resumen de la instalación"""
        print("\n" + "="*60)
        print("🎉 ¡INSTALACIÓN COMPLETADA EXITOSAMENTE!")
        print("="*60)
        print(f"🚀 VADER {self.version} - Universal Runtime Enhanced")
        print(f"⚡ {self.slogan}")
        print()
        print("📍 UBICACIONES:")
        print(f"   Instalación: {self.install_dir}")
        print(f"   Configuración: {self.config_dir}")
        print(f"   CLI: {self.bin_dir / 'vader'}")
        print()
        print("🛠️ COMPONENTES INSTALADOS:")
        for comp_name, comp_info in self.components.items():
            print(f"   ✅ {comp_info['name']}")
        print()
        print("🚀 PRIMEROS PASOS:")
        print("   1. Reinicia tu terminal")
        print("   2. Ejecuta: vader --help")
        print("   3. Prueba: vader test_simple.vdr")
        print()
        print("📚 DOCUMENTACIÓN:")
        print(f"   {self.install_dir / 'docs' / 'README.md'}")
        print(f"   {VADER_REPO_URL}")
        print()
        print("🎯 ¡Vader está listo para la programación universal!")
        print("="*60)
    
    def install(self, components_to_install: Optional[List[str]] = None) -> bool:
        """Ejecuta la instalación completa"""
        try:
            print("🚀 Iniciando instalación de Vader 7.0 Universal Runtime...")
            print()
            
            # 1. Verificar requisitos
            requirements_ok, issues = self.check_system_requirements()
            if not requirements_ok:
                print("❌ No se pueden cumplir los requisitos mínimos")
                return False
            
            # 2. Crear directorios
            self.create_directories()
            
            # 3. Instalar componentes
            components_to_install = components_to_install or list(self.components.keys())
            
            for comp_name in components_to_install:
                if comp_name in self.components:
                    success = self.install_component(comp_name, self.components[comp_name])
                    if not success and self.components[comp_name]['required']:
                        print(f"❌ Error instalando componente requerido: {comp_name}")
                        return False
            
            # 4. Configurar CLI
            self.create_cli_wrapper()
            
            # 5. Instalar dependencias
            self.install_python_dependencies()
            
            # 6. Crear configuración
            self.create_config_file()
            
            # 7. Validar instalación
            if not self.validate_installation():
                print("❌ La validación de instalación falló")
                return False
            
            # 8. Mostrar resumen
            self.show_installation_summary()
            
            return True
            
        except KeyboardInterrupt:
            print("\n🛑 Instalación interrumpida por el usuario")
            return False
        except Exception as e:
            print(f"\n💥 Error durante la instalación: {str(e)}")
            return False

def main():
    """Función principal del instalador"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Instalador Universal para Vader 7.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  python install-vader-universal.py                    # Instalación completa
  python install-vader-universal.py --components core cli  # Solo componentes específicos
  python install-vader-universal.py --help            # Mostrar ayuda
        """
    )
    
    parser.add_argument(
        '--components',
        nargs='+',
        choices=['core', 'cli', 'runtimes_enhanced', 'runtimes_original', 'examples', 'documentation'],
        help='Componentes específicos a instalar'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version=f'Vader Universal Installer {INSTALLER_VERSION}'
    )
    
    args = parser.parse_args()
    
    try:
        installer = VaderUniversalInstaller()
        success = installer.install(args.components)
        return 0 if success else 1
        
    except KeyboardInterrupt:
        print("\n🛑 Instalación cancelada")
        return 130
    except Exception as e:
        print(f"💥 Error fatal: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
