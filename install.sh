#!/bin/bash
# ===============================================
# 🚀 INSTALADOR VADER PARA UNIX/LINUX/MACOS 🚀
# Lenguaje de Programación Universal Multiidioma
# ===============================================

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Banner
echo -e "${CYAN}"
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                    🚀 INSTALADOR VADER 🚀                   ║"
echo "║                                                              ║"
echo "║           Lenguaje Universal de Programación                 ║"
echo "║              Funciona en 11 idiomas                          ║"
echo "║             25+ Frameworks soportados                        ║"
echo "║                                                              ║"
echo "║                  UNIX/LINUX/MACOS VERSION                    ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Detectar sistema operativo
OS=$(uname -s)
ARCH=$(uname -m)

echo -e "${BLUE}🔍 Sistema detectado: $OS $ARCH${NC}"
echo

# Función para verificar comando
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Detectar Python
PYTHON_CMD=""
if command_exists python3; then
    PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
    MAJOR=$(echo $PYTHON_VERSION | cut -d'.' -f1)
    MINOR=$(echo $PYTHON_VERSION | cut -d'.' -f2)
    
    if [ "$MAJOR" -eq 3 ] && [ "$MINOR" -ge 6 ]; then
        PYTHON_CMD="python3"
        echo -e "${GREEN}✅ Python $PYTHON_VERSION encontrado${NC}"
    else
        echo -e "${RED}❌ Python $PYTHON_VERSION es muy antiguo (se requiere 3.6+)${NC}"
    fi
elif command_exists python; then
    PYTHON_VERSION=$(python --version 2>&1 | cut -d' ' -f2)
    MAJOR=$(echo $PYTHON_VERSION | cut -d'.' -f1)
    MINOR=$(echo $PYTHON_VERSION | cut -d'.' -f2)
    
    if [ "$MAJOR" -eq 3 ] && [ "$MINOR" -ge 6 ]; then
        PYTHON_CMD="python"
        echo -e "${GREEN}✅ Python $PYTHON_VERSION encontrado${NC}"
    else
        echo -e "${RED}❌ Python $PYTHON_VERSION es muy antiguo (se requiere 3.6+)${NC}"
    fi
fi

if [ -z "$PYTHON_CMD" ]; then
    echo -e "${RED}❌ ERROR: Python 3.6+ no encontrado${NC}"
    echo
    echo -e "${YELLOW}Por favor instala Python 3.6 o superior:${NC}"
    
    case "$OS" in
        "Darwin")
            echo "  - brew install python3"
            echo "  - O descarga desde: https://python.org"
            ;;
        "Linux")
            if command_exists apt; then
                echo "  - sudo apt update && sudo apt install python3 python3-pip"
            elif command_exists yum; then
                echo "  - sudo yum install python3 python3-pip"
            elif command_exists dnf; then
                echo "  - sudo dnf install python3 python3-pip"
            elif command_exists pacman; then
                echo "  - sudo pacman -S python python-pip"
            else
                echo "  - Instala Python 3.6+ usando tu gestor de paquetes"
            fi
            ;;
        *)
            echo "  - Descarga desde: https://python.org"
            ;;
    esac
    
    echo
    exit 1
fi

# Verificar pip
if ! command_exists pip3 && ! command_exists pip; then
    echo -e "${YELLOW}⚠️  pip no encontrado, intentando instalar...${NC}"
    $PYTHON_CMD -m ensurepip --default-pip
    if [ $? -ne 0 ]; then
        echo -e "${RED}❌ No se pudo instalar pip${NC}"
        exit 1
    fi
    echo -e "${GREEN}✅ pip instalado${NC}"
else
    echo -e "${GREEN}✅ pip encontrado${NC}"
fi

echo
echo -e "${BLUE}🚀 Ejecutando instalador Python...${NC}"
echo

# Ejecutar el instalador Python
# Cambiar al directorio del script para asegurar ruta correcta
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"
$PYTHON_CMD install.py

if [ $? -eq 0 ]; then
    echo
    echo -e "${GREEN}🎉 ¡Instalación de Vader completada exitosamente!${NC}"
    echo
    echo -e "${CYAN}💡 CONSEJO: Reinicia tu terminal o ejecuta 'source ~/.bashrc' para usar 'vader' globalmente${NC}"
    echo
else
    echo
    echo -e "${RED}❌ Error durante la instalación${NC}"
    exit 1
fi
