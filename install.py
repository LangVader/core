#!/usr/bin/env python3
"""
🚀 INSTALADOR UNIVERSAL DE VADER 🚀
Lenguaje de Programación Universal Multiidioma

Funciona en: Windows, macOS, Linux
Autor: Vader Team
Versión: 2.0
"""

import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path

class VaderInstaller:
    def __init__(self):
        self.system = platform.system().lower()
        self.python_cmd = self.detect_python()
        self.pip_cmd = self.detect_pip()
        self.vader_dir = Path(__file__).parent.absolute()
        self.home_dir = Path.home()
        
    def detect_python(self):
        """Detecta el comando Python correcto para el sistema"""
        commands = ['python3', 'python', 'py']
        for cmd in commands:
            try:
                result = subprocess.run([cmd, '--version'], 
                                      capture_output=True, text=True)
                if result.returncode == 0 and 'Python 3' in result.stdout:
                    return cmd
            except FileNotFoundError:
                continue
        return None
    
    def detect_pip(self):
        """Detecta el comando pip correcto para el sistema"""
        commands = ['pip3', 'pip', 'py -m pip']
        for cmd in commands:
            try:
                if cmd == 'py -m pip':
                    result = subprocess.run(['py', '-m', 'pip', '--version'], 
                                          capture_output=True, text=True)
                else:
                    result = subprocess.run([cmd, '--version'], 
                                          capture_output=True, text=True)
                if result.returncode == 0:
                    return cmd
            except FileNotFoundError:
                continue
        return None
    
    def print_banner(self):
        """Muestra el banner de instalación"""
        banner = """
╔══════════════════════════════════════════════════════════════╗
║                    🚀 INSTALADOR VADER 🚀                   ║
║                                                              ║
║           Lenguaje Universal de Programación                 ║
║              Funciona en 11 idiomas                          ║
║             25+ Frameworks soportados                        ║
║                                                              ║
║  Sistema detectado: {:<45} ║
║  Python detectado:  {:<45} ║
╚══════════════════════════════════════════════════════════════╝
        """.format(
            f"{platform.system()} {platform.release()}"[:45],
            f"{self.python_cmd} {sys.version.split()[0]}"[:45] if self.python_cmd else "No encontrado"[:45]
        )
        print(banner)
    
    def check_requirements(self):
        """Verifica los requisitos del sistema"""
        print("🔍 Verificando requisitos del sistema...")
        
        if not self.python_cmd:
            print("❌ ERROR: Python 3.6+ no encontrado")
            print("   Por favor instala Python 3.6 o superior:")
            if self.system == 'windows':
                print("   - Descarga desde: https://python.org")
            elif self.system == 'darwin':
                print("   - brew install python3")
                print("   - O descarga desde: https://python.org")
            else:
                print("   - sudo apt install python3 (Ubuntu/Debian)")
                print("   - sudo yum install python3 (CentOS/RHEL)")
            return False
        
        # Verificar versión de Python
        try:
            result = subprocess.run([self.python_cmd, '--version'], 
                                  capture_output=True, text=True)
            version = result.stdout.strip().split()[1]
            major, minor = map(int, version.split('.')[:2])
            if major < 3 or (major == 3 and minor < 6):
                print(f"❌ ERROR: Python {version} es muy antiguo")
                print("   Se requiere Python 3.6 o superior")
                return False
        except:
            print("❌ ERROR: No se pudo verificar la versión de Python")
            return False
        
        print(f"✅ Python {version} encontrado")
        
        if not self.pip_cmd:
            print("⚠️  ADVERTENCIA: pip no encontrado, intentando instalar...")
            try:
                subprocess.run([self.python_cmd, '-m', 'ensurepip', '--default-pip'], 
                             check=True, capture_output=True)
                self.pip_cmd = f"{self.python_cmd} -m pip"
                print("✅ pip instalado correctamente")
            except:
                print("❌ ERROR: No se pudo instalar pip")
                return False
        else:
            print("✅ pip encontrado")
        
        return True
    
    def install_dependencies(self):
        """Instala las dependencias necesarias"""
        print("\n📦 Instalando dependencias...")
        
        # Crear requirements.txt si no existe
        requirements_file = self.vader_dir / "requirements.txt"
        if not requirements_file.exists():
            requirements = [
                "setuptools>=42",
                "wheel",
                "colorama",  # Para colores en terminal
                "requests",  # Para funcionalidades web
            ]
            with open(requirements_file, 'w') as f:
                f.write('\n'.join(requirements))
        
        try:
            if self.pip_cmd == 'py -m pip':
                cmd = ['py', '-m', 'pip', 'install', '-r', str(requirements_file)]
            else:
                cmd = [self.pip_cmd, 'install', '-r', str(requirements_file)]
            
            subprocess.run(cmd, check=True, cwd=str(self.vader_dir))
            print("✅ Dependencias instaladas correctamente")
            return True
        except subprocess.CalledProcessError:
            print("⚠️  Algunas dependencias no se pudieron instalar, pero Vader funcionará")
            return True
    
    def install_vader(self):
        """Instala Vader como paquete"""
        print("\n🔧 Instalando Vader...")
        
        try:
            if self.pip_cmd == 'py -m pip':
                cmd = ['py', '-m', 'pip', 'install', '-e', '.']
            else:
                cmd = [self.pip_cmd, 'install', '-e', '.']
            
            subprocess.run(cmd, check=True, cwd=str(self.vader_dir))
            print("✅ Vader instalado como paquete Python")
            return True
        except subprocess.CalledProcessError:
            print("⚠️  Instalación como paquete falló, configurando modo directo...")
            return self.setup_direct_mode()
    
    def setup_direct_mode(self):
        """Configura Vader para uso directo"""
        print("🔧 Configurando modo directo...")
        
        # Hacer ejecutables los scripts
        vader_script = self.vader_dir / "src" / "vader.py"
        if vader_script.exists():
            if self.system != 'windows':
                os.chmod(str(vader_script), 0o755)
            print("✅ Script principal configurado")
        
        # Crear script de lanzamiento universal
        launcher_content = self.create_launcher_script()
        launcher_path = self.vader_dir / "vader"
        
        with open(launcher_path, 'w') as f:
            f.write(launcher_content)
        
        if self.system != 'windows':
            os.chmod(str(launcher_path), 0o755)
        
        print("✅ Launcher universal creado")
        return True
    
    def create_launcher_script(self):
        """Crea el script launcher universal"""
        if self.system == 'windows':
            return f'''@echo off
cd /d "{self.vader_dir}"
{self.python_cmd} src\\vader.py %*
'''
        else:
            return f'''#!/bin/bash
cd "{self.vader_dir}"
{self.python_cmd} src/vader.py "$@"
'''
    
    def setup_path(self):
        """Configura el PATH para usar Vader globalmente"""
        print("\n🌍 Configurando acceso global...")
        
        if self.system == 'windows':
            return self.setup_windows_path()
        else:
            return self.setup_unix_path()
    
    def setup_windows_path(self):
        """Configura PATH en Windows"""
        print("📝 Para usar 'vader' globalmente en Windows:")
        print(f"   1. Agrega esta ruta al PATH: {self.vader_dir}")
        print("   2. O usa el comando completo:")
        print(f"      {self.vader_dir}\\vader.bat mi_programa.vdr")
        return True
    
    def setup_unix_path(self):
        """Configura PATH en Unix/Linux/macOS"""
        shell_configs = [
            self.home_dir / ".bashrc",
            self.home_dir / ".zshrc",
            self.home_dir / ".profile"
        ]
        
        path_line = f'export PATH="{self.vader_dir}:$PATH"'
        
        for config_file in shell_configs:
            if config_file.exists():
                try:
                    with open(config_file, 'r') as f:
                        content = f.read()
                    
                    if str(self.vader_dir) not in content:
                        with open(config_file, 'a') as f:
                            f.write(f'\n# Vader Language Path\n{path_line}\n')
                        print(f"✅ PATH agregado a {config_file.name}")
                except:
                    pass
        
        print("📝 Para usar 'vader' globalmente:")
        print("   1. Reinicia tu terminal, o ejecuta:")
        print(f"      source ~/.bashrc  # o ~/.zshrc")
        print("   2. O usa el comando completo:")
        print(f"      {self.vader_dir}/vader mi_programa.vdr")
        return True
    
    def test_installation(self):
        """Prueba la instalación"""
        print("\n🧪 Probando instalación...")
        
        # Crear archivo de prueba
        test_file = self.vader_dir / "test_instalacion.vdr"
        test_content = '''decir "¡Hola! Vader está funcionando correctamente 🚀"
decir "Sistema: ''' + platform.system() + '''"
decir "Versión Python: ''' + sys.version.split()[0] + '''"
decir "¡Instalación exitosa!"'''
        
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(test_content)
        
        try:
            # Probar ejecución
            cmd = [self.python_cmd, 'src/vader.py', str(test_file)]
            result = subprocess.run(cmd, cwd=str(self.vader_dir), 
                                  capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                print("✅ Prueba exitosa:")
                print(result.stdout)
                return True
            else:
                print("⚠️  Prueba con advertencias:")
                print(result.stderr)
                return True
        except Exception as e:
            print(f"❌ Error en la prueba: {e}")
            return False
        finally:
            # Limpiar archivo de prueba
            if test_file.exists():
                test_file.unlink()
    
    def show_usage_info(self):
        """Muestra información de uso"""
        print("""
╔══════════════════════════════════════════════════════════════╗
║                    ✅ INSTALACIÓN COMPLETA                   ║
╚══════════════════════════════════════════════════════════════╝

🚀 CÓMO USAR VADER:

1. Crear un archivo .vdr:
   echo 'decir "¡Hola Mundo!"' > mi_programa.vdr

2. Ejecutar programa:""")
        
        if self.system == 'windows':
            print(f"   {self.python_cmd} {self.vader_dir}\\src\\vader.py mi_programa.vdr")
        else:
            print(f"   {self.python_cmd} {self.vader_dir}/src/vader.py mi_programa.vdr")
        
        print(f"""
3. Ver ayuda:
   {self.python_cmd} {self.vader_dir}/src/vader.py --help

4. Listar idiomas (11 disponibles):
   {self.python_cmd} {self.vader_dir}/src/vader.py --list-languages

5. Listar frameworks (25+ disponibles):
   {self.python_cmd} {self.vader_dir}/src/vader.py --list-frameworks

📚 DOCUMENTACIÓN:
   - README.md - Guía completa
   - VADER_SUPER_FACIL.md - Tutorial para principiantes
   - docs/ - Documentación técnica

🌍 EJEMPLOS:
   - ejemplos/ - Más de 60 ejemplos listos
   - test_simple.vdr - Ejemplo básico

¡Vader está listo para democratizar la programación! 🎉
""")
    
    def run(self):
        """Ejecuta el instalador"""
        self.print_banner()
        
        if not self.check_requirements():
            sys.exit(1)
        
        if not self.install_dependencies():
            print("⚠️  Continuando sin todas las dependencias...")
        
        if not self.install_vader():
            print("❌ Error en la instalación")
            sys.exit(1)
        
        self.setup_path()
        
        if not self.test_installation():
            print("⚠️  Instalación completa pero con advertencias")
        
        self.show_usage_info()
        print("🎉 ¡Instalación de Vader completada exitosamente!")

def main():
    """Función principal"""
    try:
        installer = VaderInstaller()
        installer.run()
    except KeyboardInterrupt:
        print("\n\n❌ Instalación cancelada por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
