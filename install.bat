@echo off
REM ===============================================
REM 🚀 INSTALADOR VADER PARA WINDOWS 🚀
REM Lenguaje de Programación Universal Multiidioma
REM ===============================================

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    🚀 INSTALADOR VADER 🚀                   ║
echo ║                                                              ║
echo ║           Lenguaje Universal de Programación                 ║
echo ║              Funciona en 11 idiomas                          ║
echo ║             25+ Frameworks soportados                        ║
echo ║                                                              ║
echo ║                    WINDOWS VERSION                           ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    py --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo ❌ ERROR: Python no encontrado
        echo    Por favor instala Python 3.6+ desde: https://python.org
        echo    Asegúrate de marcar "Add Python to PATH" durante la instalación
        pause
        exit /b 1
    ) else (
        set PYTHON_CMD=py
    )
) else (
    set PYTHON_CMD=python
)

echo ✅ Python encontrado, ejecutando instalador...
echo.

REM Ejecutar el instalador Python
%PYTHON_CMD% install.py

if %errorlevel% neq 0 (
    echo.
    echo ❌ Error durante la instalación
    pause
    exit /b 1
)

echo.
echo 🎉 ¡Instalación completada!
echo    Puedes cerrar esta ventana o presionar cualquier tecla
pause >nul
