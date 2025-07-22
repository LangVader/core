# 🚀 INSTALACIÓN DE VADER

**Vader** es el primer lenguaje de programación universal multiidioma del mundo. Funciona en **11 idiomas** y soporta **25+ frameworks**. ¡Programa en español natural!

## 📋 Requisitos del Sistema

- **Python 3.6 o superior**
- **Sistema Operativo**: Windows, macOS, Linux
- **Arquitectura**: x86, x64, ARM (Apple M1/M2)

## ⚡ Instalación Rápida (Recomendada)

### 1. Clonar el repositorio
```bash
# Clonar Vader desde GitHub
git clone https://github.com/LangVader/core.git vader
cd vader
```

### 2. Ejecutar instalador

#### 🖥️ Windows
```cmd
# Opción 1: Doble clic en install.bat
# Opción 2: Desde terminal
install.bat
```

#### 🍎 macOS / 🐧 Linux
```bash
# Opción 1: Script automático
./install.sh

# Opción 2: Instalador Python
python3 install.py
```

## 🔧 Instalación Manual

Si prefieres instalar manualmente:

### 1. Clonar repositorio
```bash
# Clonar Vader desde GitHub
git clone https://github.com/LangVader/core.git vader
cd vader
```

### 2. Verificar Python
```bash
python3 --version  # Debe ser 3.6+
```

### 3. Instalar dependencias
```bash
pip3 install -r requirements.txt
```

### 4. Instalar Vader
```bash
# Como paquete (recomendado)
pip3 install -e .

# O usar directamente
python3 src/vader.py --help
```

## ✅ Verificar Instalación

### Prueba básica
```bash
# Crear archivo de prueba
echo 'decir "¡Hola Vader!"' > test.vdr

# Ejecutar
python3 src/vader.py test.vdr
```

### Verificar características
```bash
# Ver idiomas soportados (11 idiomas)
python3 src/vader.py --list-languages

# Ver frameworks soportados (25+ frameworks)
python3 src/vader.py --list-frameworks

# Ver ayuda completa
python3 src/vader.py --help
```

## 🌍 Uso Global

Después de la instalación, puedes usar Vader globalmente:

```bash
# Si se instaló correctamente
vader mi_programa.vdr

# O usando el path completo
python3 /ruta/a/vader/src/vader.py mi_programa.vdr
```

## 🚨 Solución de Problemas

### Python no encontrado
**Windows:**
- Descargar desde [python.org](https://python.org)
- Marcar "Add Python to PATH" durante instalación

**macOS:**
```bash
# Con Homebrew
brew install python3

# Con MacPorts
sudo port install python39
```

**Linux:**
```bash
# Ubuntu/Debian
sudo apt update && sudo apt install python3 python3-pip

# CentOS/RHEL
sudo yum install python3 python3-pip

# Arch Linux
sudo pacman -S python python-pip
```

### Problemas de permisos
```bash
# macOS/Linux: Dar permisos de ejecución
chmod +x install.sh
chmod +x src/vader.py

# Windows: Ejecutar como administrador
```

### Problemas con pip
```bash
# Actualizar pip
python3 -m pip install --upgrade pip

# Instalar pip si no existe
python3 -m ensurepip --default-pip
```

## 📚 Primeros Pasos

### 1. Tu primer programa
```vader
decir "¡Hola mundo desde Vader!"
preguntar "¿Cómo te llamas?" y guardar la respuesta en nombre
decir "¡Hola " + nombre + "!"
```

### 2. Guardar como archivo .vdr
```bash
# Crear archivo
nano mi_primer_programa.vdr

# Ejecutar
python3 src/vader.py mi_primer_programa.vdr
```

### 3. Explorar ejemplos
```bash
# Ver ejemplos disponibles
ls ejemplos/

# Ejecutar ejemplo
python3 src/vader.py ejemplos/hola_mundo.vdr
```

## 🎯 Características Principales

- ✅ **11 Idiomas**: Español, Inglés, Francés, Chino, Japonés, etc.
- ✅ **25+ Frameworks**: React, Vue, Angular, Django, Laravel, etc.
- ✅ **Runtime Nativo**: Ejecuta sin transpilación
- ✅ **IA Integrada**: Asistente de programación
- ✅ **GUI Moderna**: Interfaz gráfica incluida
- ✅ **Multiplataforma**: Windows, macOS, Linux
- ✅ **Sintaxis Natural**: Programa como hablas
### 🎨 Extensión VS Code Incluida
```bash
# Instalar extensión de Vader para VS Code
code --install-extension vscode_extension/vader-language-support-1.0.1.vsix
```

**Características de la extensión:**
- ✅ Logo de Vader visible
- ✅ Syntax highlighting completo
- ✅ Snippets inteligentes
- ✅ README con documentación

### 🆘 ¿Problemas? 
Consulta la **[Guía Completa de Instalación](INSTALACION.md)** con soluciones para todos los sistemas.

## 📖 Documentación

- **README.md** - Guía completa del proyecto
- **VADER_SUPER_FACIL.md** - Tutorial para principiantes
- **PROGRAMAR_COMO_HABLAR.md** - Sintaxis natural
- **docs/** - Documentación técnica completa
- **ejemplos/** - Más de 60 ejemplos listos

## 🆘 Soporte

Si tienes problemas:

1. **Revisa los requisitos** - Python 3.6+
2. **Ejecuta el instalador** - `python3 install.py`
3. **Verifica la instalación** - `python3 src/vader.py --help`
4. **Consulta ejemplos** - Carpeta `ejemplos/`
5. **Lee la documentación** - Archivos `.md`

## 🎉 ¡Listo para Programar!

Una vez instalado, Vader está listo para democratizar la programación:

```bash
# Crear aplicación web
python3 src/vader.py mi_web.vdr --framework react --target javascript

# Programar en francés
python3 src/vader.py mon_programme.vdr --language fr

# Usar IA integrada
python3 src/vader.py --ai-generate "crear calculadora" --output calc.vdr

# Abrir GUI moderna
python3 launch_gui.py
```

**¡Bienvenido al futuro de la programación universal!** 🚀
