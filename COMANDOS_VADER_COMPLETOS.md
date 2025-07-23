# 🚀 COMANDOS COMPLETOS DE VADER 7.0 UNIVERSAL
## LA PROGRAMACIÓN: Libre, Descentralizada, Accesible

---

## 📋 TABLA DE CONTENIDOS
1. [Comandos Básicos CLI](#comandos-básicos-cli)
2. [CLI Universal Enhanced](#cli-universal-enhanced)
3. [Runtimes Específicos](#runtimes-específicos)
4. [Frameworks y Lenguajes](#frameworks-y-lenguajes)
5. [Herramientas Adicionales](#herramientas-adicionales)
6. [GUI y Demos](#gui-y-demos)
7. [Ejemplos Prácticos](#ejemplos-prácticos)

---

## 🎯 COMANDOS BÁSICOS CLI

### Ejecución Directa (Runtime Nativo)
```bash
# Ejecutar archivo .vdr nativamente
python3 src/vader.py mi_programa.vdr --run

# Ejecutar con verbose
python3 src/vader.py mi_programa.vdr --run --verbose

# Ejecutar y guardar salida
python3 src/vader.py mi_programa.vdr --run --output resultado.txt
```

### Transpilación
```bash
# Transpilar a Python
python3 src/vader.py mi_programa.vdr --target python

# Transpilar a JavaScript
python3 src/vader.py mi_programa.vdr --target javascript

# Transpilar y guardar archivo
python3 src/vader.py mi_programa.vdr --target python --output programa.py

# Transpilar a HTML
python3 src/vader.py mi_pagina.vdr --target html --output index.html

# Transpilar a CSS
python3 src/vader.py mis_estilos.vdr --target css --output styles.css
```

### Información del Sistema
```bash
# Listar todos los frameworks (25+)
python3 src/vader.py --list-frameworks

# Listar todos los idiomas (11 idiomas)
python3 src/vader.py --list-languages

# Ver versión de Vader
python3 src/vader.py --version

# Ayuda completa
python3 src/vader.py --help

# Verificar sintaxis sin ejecutar
python3 src/vader.py mi_programa.vdr --check-syntax
```

### Multiidioma
```bash
# Detectar idioma automáticamente
python3 src/vader.py mi_codigo.vdr --detect-language

# Especificar idioma del código
python3 src/vader.py mi_codigo.vdr --language es --run

# Traducir código entre idiomas
python3 src/vader.py mi_codigo.vdr --translate-to english

# Información detallada de un idioma
python3 src/vader.py --multilingual-info es
```

---

## 🌟 CLI UNIVERSAL ENHANCED

### Comando Principal
```bash
# Sintaxis básica
python3 tools/vader-cli-universal.py <archivo.vdr> [plataforma] [opciones]

# Detección automática
python3 tools/vader-cli-universal.py mi_app.vdr

# Con plataforma específica
python3 tools/vader-cli-universal.py mi_app.vdr python --verbose
```

### Información del CLI Universal
```bash
# Ayuda completa
python3 tools/vader-cli-universal.py --help

# Ver versión
python3 tools/vader-cli-universal.py --version

# Listar todas las plataformas
python3 tools/vader-cli-universal.py --list

# Modo verbose
python3 tools/vader-cli-universal.py mi_app.vdr python --verbose

# Detección automática (default)
python3 tools/vader-cli-universal.py mi_app.vdr --auto
```

---

## 🔧 RUNTIMES ESPECÍFICOS

### Runtimes Enhanced (Auditados)
```bash
# Python Enhanced
python3 runtimes/enhanced/vader-7.0-universal-python-enhanced.py mi_app.vdr python
python3 runtimes/enhanced/vader-7.0-universal-python-enhanced.py mi_app.vdr django
python3 runtimes/enhanced/vader-7.0-universal-python-enhanced.py mi_app.vdr flask
python3 runtimes/enhanced/vader-7.0-universal-python-enhanced.py mi_app.vdr fastapi
python3 runtimes/enhanced/vader-7.0-universal-python-enhanced.py mi_app.vdr jupyter

# JavaScript Enhanced
node runtimes/enhanced/vader-7.0-universal-js-enhanced.js mi_app.vdr web
node runtimes/enhanced/vader-7.0-universal-js-enhanced.js mi_app.vdr react
node runtimes/enhanced/vader-7.0-universal-js-enhanced.js mi_app.vdr vue
node runtimes/enhanced/vader-7.0-universal-js-enhanced.js mi_app.vdr node
node runtimes/enhanced/vader-7.0-universal-js-enhanced.js mi_app.vdr express

# IoT Enhanced
python3 runtimes/enhanced/vader-7.0-universal-iot-enhanced.py mi_iot.vdr arduino
python3 runtimes/enhanced/vader-7.0-universal-iot-enhanced.py mi_iot.vdr esp32
python3 runtimes/enhanced/vader-7.0-universal-iot-enhanced.py mi_iot.vdr esp8266
python3 runtimes/enhanced/vader-7.0-universal-iot-enhanced.py mi_iot.vdr raspberry_pi
python3 runtimes/enhanced/vader-7.0-universal-iot-enhanced.py mi_iot.vdr microbit

# Cloud Enhanced
python3 runtimes/enhanced/vader-7.0-universal-cloud-enhanced.py mi_cloud.vdr aws_lambda
python3 runtimes/enhanced/vader-7.0-universal-cloud-enhanced.py mi_cloud.vdr vercel
python3 runtimes/enhanced/vader-7.0-universal-cloud-enhanced.py mi_cloud.vdr netlify
python3 runtimes/enhanced/vader-7.0-universal-cloud-enhanced.py mi_cloud.vdr azure_functions
python3 runtimes/enhanced/vader-7.0-universal-cloud-enhanced.py mi_cloud.vdr google_cloud
```

### Runtimes Universales (Funcionales)
```bash
# AI Universal
python3 runtimes/universal/vader-7.0-universal-ai.py mi_ia.vdr openai
python3 runtimes/universal/vader-7.0-universal-ai.py mi_ia.vdr anthropic
python3 runtimes/universal/vader-7.0-universal-ai.py mi_ia.vdr huggingface
python3 runtimes/universal/vader-7.0-universal-ai.py mi_ia.vdr local
python3 runtimes/universal/vader-7.0-universal-ai.py mi_ia.vdr ollama

# Gaming Universal
python3 runtimes/universal/vader-7.0-universal-gaming.py mi_juego.vdr unity
python3 runtimes/universal/vader-7.0-universal-gaming.py mi_juego.vdr godot
python3 runtimes/universal/vader-7.0-universal-gaming.py mi_juego.vdr pygame
python3 runtimes/universal/vader-7.0-universal-gaming.py mi_juego.vdr phaser

# Blockchain Universal
python3 runtimes/universal/vader-7.0-universal-blockchain.py mi_token.vdr ethereum
python3 runtimes/universal/vader-7.0-universal-blockchain.py mi_token.vdr polygon
python3 runtimes/universal/vader-7.0-universal-blockchain.py mi_token.vdr solana
python3 runtimes/universal/vader-7.0-universal-blockchain.py mi_token.vdr web3

# Desktop Universal
python3 runtimes/universal/vader-7.0-universal-desktop.py mi_app.vdr electron
python3 runtimes/universal/vader-7.0-universal-desktop.py mi_app.vdr tauri
python3 runtimes/universal/vader-7.0-universal-desktop.py mi_app.vdr flutter_desktop
python3 runtimes/universal/vader-7.0-universal-desktop.py mi_app.vdr qt

# Database Universal
python3 runtimes/universal/vader-7.0-universal-database.py mi_bd.vdr mysql
python3 runtimes/universal/vader-7.0-universal-database.py mi_bd.vdr mongodb
python3 runtimes/universal/vader-7.0-universal-database.py mi_bd.vdr postgresql
python3 runtimes/universal/vader-7.0-universal-database.py mi_bd.vdr graphql

# Creative Universal
python3 runtimes/universal/vader-7.0-universal-creative.py mi_proyecto.vdr blender
python3 runtimes/universal/vader-7.0-universal-creative.py mi_proyecto.vdr gimp
python3 runtimes/universal/vader-7.0-universal-creative.py mi_proyecto.vdr audacity
python3 runtimes/universal/vader-7.0-universal-creative.py mi_proyecto.vdr ffmpeg

# Robotics Universal
python3 runtimes/universal/vader-7.0-universal-robotics.py mi_robot.vdr ros
python3 runtimes/universal/vader-7.0-universal-robotics.py mi_robot.vdr arduino_ide
python3 runtimes/universal/vader-7.0-universal-robotics.py mi_robot.vdr raspberry_pi

# Data Science Universal
python3 runtimes/universal/vader-7.0-universal-datascience.py mi_analisis.vdr jupyter
python3 runtimes/universal/vader-7.0-universal-datascience.py mi_analisis.vdr r
python3 runtimes/universal/vader-7.0-universal-datascience.py mi_analisis.vdr matlab
python3 runtimes/universal/vader-7.0-universal-datascience.py mi_analisis.vdr pandas

# Edge Computing Universal
python3 runtimes/universal/vader-7.0-universal-edge.py mi_edge.vdr webassembly
python3 runtimes/universal/vader-7.0-universal-edge.py mi_edge.vdr cloudflare_workers
python3 runtimes/universal/vader-7.0-universal-edge.py mi_edge.vdr vercel_edge
python3 runtimes/universal/vader-7.0-universal-edge.py mi_edge.vdr netlify_edge
```

---

## 🎨 FRAMEWORKS Y LENGUAJES

### Frameworks Web
```bash
# React
python3 src/vader.py mi_app.vdr --framework react --target javascript

# Vue.js
python3 src/vader.py mi_app.vdr --framework vue --target javascript

# Angular
python3 src/vader.py mi_app.vdr --framework angular --target typescript

# Next.js
python3 src/vader.py mi_app.vdr --framework nextjs --target javascript

# Express.js
python3 src/vader.py mi_api.vdr --framework express --target javascript

# Svelte
python3 src/vader.py mi_app.vdr --framework svelte --target javascript

# SvelteKit
python3 src/vader.py mi_app.vdr --framework sveltekit --target javascript

# Nuxt.js
python3 src/vader.py mi_app.vdr --framework nuxtjs --target javascript
```

### Lenguajes de Programación
```bash
# Python
python3 src/vader.py mi_codigo.vdr --target python

# JavaScript
python3 src/vader.py mi_codigo.vdr --target javascript

# TypeScript
python3 src/vader.py mi_codigo.vdr --target typescript

# Java
python3 src/vader.py mi_codigo.vdr --target java

# C#
python3 src/vader.py mi_codigo.vdr --target csharp

# Go
python3 src/vader.py mi_codigo.vdr --target go

# Rust
python3 src/vader.py mi_codigo.vdr --target rust

# PHP
python3 src/vader.py mi_codigo.vdr --target php

# Ruby
python3 src/vader.py mi_codigo.vdr --target ruby

# Dart
python3 src/vader.py mi_codigo.vdr --target dart

# Solidity
python3 src/vader.py mi_contrato.vdr --target solidity
```

---

## 🛠️ HERRAMIENTAS ADICIONALES

### Instalador Universal
```bash
# Instalar Vader completo
python3 install-vader-universal.py

# Instalador con verificación
python3 install.py

# Script de instalación Unix/Linux/macOS
./install.sh

# Script de instalación Windows
install.bat
```

### Demo Interactivo
```bash
# Demo completo con todos los runtimes
python3 tools/demo-vader-universal.py

# Demo específico (seleccionar opción en menú)
# 1. Python Enhanced
# 2. JavaScript Enhanced
# 3. IoT Enhanced
# 4. Cloud Enhanced
# 5. AI Universal
# 6. Mobile Universal
# 7. Gaming Universal
# 8. Blockchain Universal
# 9. Ver métricas
# 10. Benchmark completo
```

---

## 🖥️ GUI Y DEMOS

### GUI Moderna
```bash
# GUI principal (oscura y moderna)
python3 gui_simple.py

# Launcher de GUI
python3 launch_gui.py

# Pruebas automatizadas de GUI
python3 test_gui.py
```

### Demos Web
```bash
# Servidor local para demos web
python3 -m http.server 8000

# Luego abrir en navegador:
# http://localhost:8000/demo_web.html
# http://localhost:8000/test_gaming.html
# http://localhost:8000/demo_completo.html
```

---

## 📝 EJEMPLOS PRÁCTICOS

### Crear y Ejecutar Programas
```bash
# Crear programa simple
echo 'mostrar "¡Hola Vader!"' > mi_programa.vdr
python3 src/vader.py mi_programa.vdr --run

# Crear calculadora
echo 'numero1 = 10
numero2 = 5
resultado = numero1 + numero2
mostrar "El resultado es: " + texto(resultado)' > calculadora.vdr
python3 src/vader.py calculadora.vdr --run

# Crear página web
echo 'pagina "Mi Sitio Web"
titulo1 "Bienvenido a mi sitio"
parrafo "Este sitio está hecho con Vader"' > mi_sitio.vdr
python3 src/vader.py mi_sitio.vdr --target html --output index.html
```

### Trabajar con Archivos Existentes
```bash
# Ejecutar ejemplos incluidos
python3 src/vader.py ejemplos/hola_mundo.vdr --run
python3 src/vader.py ejemplos/calculadora.vdr --run
python3 src/vader.py ejemplos/lista_tareas.vdr --run

# Probar archivos creados anteriormente
python3 src/vader.py test_ai.vdr --run
python3 src/vader.py test_iot.vdr --run
python3 src/vader.py mi_archivo.vdr --run
```

### Comandos de Desarrollo
```bash
# Verificar instalación
python3 src/vader.py --version

# Verificar sintaxis
python3 src/vader.py mi_programa.vdr --check-syntax

# Modo debug
python3 src/vader.py mi_programa.vdr --run --verbose --debug

# Generar documentación
python3 src/vader.py --generate-docs
```

---

## 🚀 COMANDOS AVANZADOS

### Integración con IA
```bash
# Generar código con IA
python3 src/vader.py --ai-generate "crear calculadora" --output calc.vdr

# Analizar código con IA
python3 src/vader.py mi_codigo.vdr --ai-analyze --ai-detailed

# Optimizar código con IA
python3 src/vader.py mi_codigo.vdr --ai-optimize --output optimizado.vdr

# Sugerencias de IA
python3 src/vader.py mi_codigo.vdr --ai-suggest

# Verificar errores con IA
python3 src/vader.py mi_codigo.vdr --ai-check-errors
```

### Plantillas y Componentes
```bash
# Usar plantilla predefinida
echo 'usar plantilla "web_basica" con titulo="Mi Sitio", autor="Mi Nombre"' > desde_plantilla.vdr
python3 src/vader.py desde_plantilla.vdr --run

# Usar componente reutilizable
echo 'usar componente "boton_moderno" con texto="Enviar", color="azul"' > con_componente.vdr
python3 src/vader.py con_componente.vdr --run

# Listar plantillas disponibles
echo 'listar plantillas' > listar.vdr
python3 src/vader.py listar.vdr --run

# Listar componentes disponibles
echo 'listar componentes' > componentes.vdr
python3 src/vader.py componentes.vdr --run
```

---

## 🌍 COMANDOS MULTIIDIOMA

### Programar en Diferentes Idiomas
```bash
# Inglés
echo 'show "Hello World"' > hello.vdr
python3 src/vader.py hello.vdr --language en --run

# Francés
echo 'afficher "Bonjour le monde"' > bonjour.vdr
python3 src/vader.py bonjour.vdr --language fr --run

# Chino
echo '显示 "你好世界"' > nihao.vdr
python3 src/vader.py nihao.vdr --language zh --run

# Japonés
echo '表示 "こんにちは世界"' > konnichiwa.vdr
python3 src/vader.py konnichiwa.vdr --language ja --run
```

---

## 📊 COMANDOS DE MÉTRICAS Y BENCHMARKS

### Análisis de Rendimiento
```bash
# Benchmark de transpilación
python3 tools/vader-cli-universal.py mi_app.vdr python --benchmark

# Métricas de ejecución
python3 src/vader.py mi_programa.vdr --run --metrics

# Análisis de complejidad
python3 src/vader.py mi_programa.vdr --analyze-complexity

# Reporte de rendimiento
python3 tools/demo-vader-universal.py --performance-report
```

---

## 🔍 COMANDOS DE DEBUGGING

### Depuración y Diagnóstico
```bash
# Modo debug completo
python3 src/vader.py mi_programa.vdr --run --debug --verbose

# Trace de ejecución
python3 src/vader.py mi_programa.vdr --run --trace

# Verificar dependencias
python3 src/vader.py --check-dependencies

# Diagnóstico del sistema
python3 tools/vader-cli-universal.py --system-info

# Log detallado
python3 src/vader.py mi_programa.vdr --run --log-level debug
```

---

## 📚 COMANDOS DE DOCUMENTACIÓN

### Generar y Ver Documentación
```bash
# Ver documentación completa
cat docs/VADER_7.0_UNIVERSAL_COMPLETE.md

# Ver guías específicas
cat docs/guides/AUDITORIA_RUNTIMES_ENHANCED.md
cat VADER_SUPER_FACIL.md
cat PROGRAMAR_COMO_HABLAR.md

# Generar documentación automática
python3 src/vader.py --generate-docs --output docs/

# Ver ejemplos
ls ejemplos/
ls examples/
```

---

## 🎯 COMANDOS ESENCIALES PARA EMPEZAR

### Los 10 Comandos Más Importantes
```bash
# 1. Ejecutar programa básico
python3 src/vader.py ejemplos/hola_mundo.vdr --run

# 2. Ver frameworks disponibles
python3 src/vader.py --list-frameworks

# 3. Ver idiomas soportados
python3 src/vader.py --list-languages

# 4. Usar CLI Universal
python3 tools/vader-cli-universal.py mi_archivo.vdr python

# 5. Abrir GUI moderna
python3 gui_simple.py

# 6. Demo interactivo
python3 tools/demo-vader-universal.py

# 7. Transpilar a Python
python3 src/vader.py mi_programa.vdr --target python

# 8. Crear página web
python3 src/vader.py mi_sitio.vdr --target html

# 9. Probar con React
python3 tools/vader-cli-universal.py mi_app.vdr react

# 10. Ver ayuda completa
python3 src/vader.py --help
```

---

## 🌟 NOTAS IMPORTANTES

### Recordatorios
- Los archivos `.vdr` se ejecutan **nativamente** sin transpilación
- Vader preserva la **identidad .vdr** en todos los contextos
- Soporta **11 idiomas** humanos para programar
- Incluye **25+ frameworks** modernos
- **15+ runtimes** universales disponibles
- **GUI moderna** con IA integrada
- **CLI unificado** para todas las funciones

### Estructura de Archivos
```
Vader/
├── src/vader.py              # CLI principal
├── tools/                    # Herramientas universales
├── runtimes/                 # Runtimes específicos
├── ejemplos/                 # Ejemplos en español
├── examples/                 # Ejemplos adicionales
├── docs/                     # Documentación completa
├── gui_simple.py            # GUI moderna
└── COMANDOS_VADER_COMPLETOS.md # Este archivo
```

---

## 🚀 ¡VADER ES LA PROGRAMACIÓN UNIVERSAL!

**"Vader no es un lenguaje de programación, Vader es LA PROGRAMACIÓN: libre, descentralizada y accesible a todos"**

¡Disfruta programando en español natural con el primer lenguaje universal de la historia! 🌍✨
