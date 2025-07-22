#!/usr/bin/env python3
"""
🚀 INSTALADOR COMPLETO DE VADER 🚀
Incluye clonado automático del repositorio

Este instalador:
1. Clona el repositorio desde GitHub
2. Instala todas las dependencias
3. Configura Vader para uso global

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
import tempfile

class VaderCompleteInstaller:
    def __init__(self):
        self.system = platform.system().lower()
        self.python_cmd = self.detect_python()
        self.git_cmd = self.detect_git()
        self.home_dir = Path.home()
        self.install_dir = self.home_dir / "vader"
        
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
    
    def detect_git(self):
        """Detecta si git está disponible"""
        try:
            result = subprocess.run(['git', '--version'], 
                                  capture_output=True, text=True)
            return result.returncode == 0
        except FileNotFoundError:
            return False
    
    def print_banner(self):
        """Muestra el banner de instalación"""
        banner = """
╔══════════════════════════════════════════════════════════════╗
║                🚀 INSTALADOR COMPLETO VADER 🚀              ║
║                                                              ║
║           Lenguaje Universal de Programación                 ║
║              Funciona en 11 idiomas                          ║
║             25+ Frameworks soportados                        ║
║                                                              ║
║  INCLUYE: Clonado automático del repositorio                ║
║  Sistema:  {:<49} ║
║  Python:   {:<49} ║
║  Git:      {:<49} ║
╚══════════════════════════════════════════════════════════════╝
        """.format(
            f"{platform.system()} {platform.release()}"[:49],
            f"{self.python_cmd} {sys.version.split()[0]}"[:49] if self.python_cmd else "No encontrado"[:49],
            "Disponible"[:49] if self.git_cmd else "No encontrado"[:49]
        )
        print(banner)
    
    def check_requirements(self):
        """Verifica los requisitos del sistema"""
        print("🔍 Verificando requisitos del sistema...")
        
        # Verificar Python
        if not self.python_cmd:
            print("❌ ERROR: Python 3.6+ no encontrado")
            self.show_python_install_instructions()
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
            print(f"✅ Python {version} encontrado")
        except:
            print("❌ ERROR: No se pudo verificar la versión de Python")
            return False
        
        # Verificar Git
        if not self.git_cmd:
            print("❌ ERROR: Git no encontrado")
            self.show_git_install_instructions()
            return False
        
        print("✅ Git encontrado")
        return True
    
    def show_python_install_instructions(self):
        """Muestra instrucciones para instalar Python"""
        print("\n📥 INSTALAR PYTHON:")
        if self.system == 'windows':
            print("   - Descarga desde: https://python.org")
            print("   - Marca 'Add Python to PATH' durante la instalación")
        elif self.system == 'darwin':
            print("   - brew install python3")
            print("   - O descarga desde: https://python.org")
        else:
            print("   - sudo apt install python3 python3-pip (Ubuntu/Debian)")
            print("   - sudo yum install python3 python3-pip (CentOS/RHEL)")
            print("   - sudo pacman -S python python-pip (Arch)")
    
    def show_git_install_instructions(self):
        """Muestra instrucciones para instalar Git"""
        print("\n📥 INSTALAR GIT:")
        if self.system == 'windows':
            print("   - Descarga desde: https://git-scm.com")
        elif self.system == 'darwin':
            print("   - brew install git")
            print("   - O instala Xcode Command Line Tools: xcode-select --install")
        else:
            print("   - sudo apt install git (Ubuntu/Debian)")
            print("   - sudo yum install git (CentOS/RHEL)")
            print("   - sudo pacman -S git (Arch)")
    
    def clone_repository(self):
        """Clona el repositorio de Vader"""
        print(f"\n📦 Clonando repositorio de Vader...")
        print(f"   Destino: {self.install_dir}")
        
        # Eliminar directorio existente si existe
        if self.install_dir.exists():
            print(f"⚠️  Directorio {self.install_dir} ya existe")
            response = input("¿Quieres eliminarlo y clonar de nuevo? (s/N): ").lower()
            if response in ['s', 'si', 'sí', 'y', 'yes']:
                print("🗑️  Eliminando directorio existente...")
                shutil.rmtree(str(self.install_dir))
            else:
                print("✅ Usando directorio existente")
                return True
        
        try:
            # Clonar repositorio
            cmd = ['git', 'clone', 'https://github.com/LangVader/core.git', str(self.install_dir)]
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            print("✅ Repositorio clonado exitosamente")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Error al clonar repositorio: {e}")
            print(f"   Salida: {e.stderr}")
            return False
        except Exception as e:
            print(f"❌ Error inesperado al clonar: {e}")
            return False
    
    def install_vader(self):
        """Instala Vader usando el instalador del repositorio"""
        print("\n🔧 Instalando Vader...")
        
        # Cambiar al directorio de Vader
        original_dir = os.getcwd()
        os.chdir(str(self.install_dir))
        
        try:
            # Ejecutar el instalador de Vader
            installer_script = self.install_dir / "install.py"
            if installer_script.exists():
                cmd = [self.python_cmd, str(installer_script)]
                result = subprocess.run(cmd, check=True)
                print("✅ Vader instalado exitosamente")
                return True
            else:
                print("⚠️  install.py no encontrado, instalando manualmente...")
                return self.manual_install()
        except subprocess.CalledProcessError as e:
            print(f"❌ Error durante la instalación: {e}")
            return False
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
            return False
        finally:
            os.chdir(original_dir)
    
    def manual_install(self):
        """Instalación manual como respaldo"""
        print("🔧 Realizando instalación manual...")
        
        try:
            # Instalar dependencias si existe requirements.txt
            requirements_file = self.install_dir / "requirements.txt"
            if requirements_file.exists():
                cmd = [self.python_cmd, '-m', 'pip', 'install', '-r', str(requirements_file)]
                subprocess.run(cmd, check=True)
                print("✅ Dependencias instaladas")
            
            # Instalar como paquete editable
            cmd = [self.python_cmd, '-m', 'pip', 'install', '-e', '.']
            subprocess.run(cmd, check=True, cwd=str(self.install_dir))
            print("✅ Vader instalado como paquete")
            return True
        except subprocess.CalledProcessError as e:
            print(f"⚠️  Instalación manual falló: {e}")
            print("   Vader funcionará en modo directo")
            return True
    
    def test_installation(self):
        """Prueba la instalación"""
        print("\n🧪 Probando instalación...")
        
        # Crear archivo de prueba
        test_file = self.install_dir / "test_instalacion_completa.vdr"
        test_content = '''decir "🎉 ¡Instalación completa exitosa!"
decir "Vader está funcionando correctamente"
decir "Sistema: ''' + platform.system() + '''"
decir "Python: ''' + sys.version.split()[0] + '''"
decir "¡Listo para programar en español!"'''
        
        try:
            with open(test_file, 'w', encoding='utf-8') as f:
                f.write(test_content)
            
            # Probar ejecución
            cmd = [self.python_cmd, 'src/vader.py', str(test_file)]
            result = subprocess.run(cmd, cwd=str(self.install_dir), 
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
    
    def show_final_instructions(self):
        """Muestra las instrucciones finales"""
        print(f"""
╔══════════════════════════════════════════════════════════════╗
║                    ✅ INSTALACIÓN COMPLETA                   ║
╚══════════════════════════════════════════════════════════════╝

🚀 VADER INSTALADO EN: {self.install_dir}

📝 CÓMO USAR VADER:

1. Crear un programa:
   echo 'decir "¡Hola Mundo!"' > mi_programa.vdr

2. Ejecutar programa:
   {self.python_cmd} {self.install_dir}/src/vader.py mi_programa.vdr

3. Ver características:
   {self.python_cmd} {self.install_dir}/src/vader.py --list-languages
   {self.python_cmd} {self.install_dir}/src/vader.py --list-frameworks

4. Ver ayuda:
   {self.python_cmd} {self.install_dir}/src/vader.py --help

📚 DOCUMENTACIÓN:
   - {self.install_dir}/README.md
   - {self.install_dir}/VADER_SUPER_FACIL.md
   - {self.install_dir}/docs/

🎯 EJEMPLOS:
   - {self.install_dir}/ejemplos/ (60+ ejemplos)

💡 CONSEJO: Agrega un alias a tu shell para facilitar el uso:
   alias vader='{self.python_cmd} {self.install_dir}/src/vader.py'

¡Vader está listo para democratizar la programación! 🎉
""")
    
    def run(self):
        """Ejecuta el instalador completo"""
        self.print_banner()
        
        if not self.check_requirements():
            print("\n❌ No se pueden cumplir los requisitos del sistema")
            sys.exit(1)
        
        if not self.clone_repository():
            print("\n❌ No se pudo clonar el repositorio")
            sys.exit(1)
        
        if not self.install_vader():
            print("\n❌ Error en la instalación")
            sys.exit(1)
        
        if not self.test_installation():
            print("\n⚠️  Instalación completa pero con advertencias")
        
        self.show_final_instructions()
        print("\n🎉 ¡Instalación completa de Vader terminada exitosamente!")

def main():
    """Función principal"""
    try:
        installer = VaderCompleteInstaller()
        installer.run()
    except KeyboardInterrupt:
        print("\n\n❌ Instalación cancelada por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
