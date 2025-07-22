# 🚀 Vader Language Support - VS Code Extension

**¡Programa en español natural con Vader!**

La extensión oficial de Visual Studio Code para el lenguaje de programación **Vader** - el primer lenguaje universal multiidioma del mundo.

## ✨ Características

- 🎨 **Syntax Highlighting** - Colores optimizados para código Vader
- 📝 **Snippets Inteligentes** - Autocompletado para todas las palabras clave
- 🌙 **Temas Incluidos** - Dark y Light themes diseñados para Vader
- ⚙️ **Configuración Completa** - Soporte nativo para archivos `.vdr`
- 🔧 **IntelliSense** - Sugerencias inteligentes mientras programas
- 📋 **Formateo** - Indentación y formateo automático

## 🎯 Palabras Clave Soportadas

### Básicas
- `decir` - Mostrar texto en pantalla
- `preguntar` - Solicitar entrada del usuario
- `guardar la respuesta en` - Almacenar input en variable

### Condicionales
- `si` / `sino` / `fin si` - Estructuras condicionales
- `es igual a` / `es mayor que` / `es menor que` - Comparaciones

### Bucles
- `repetir` / `fin repetir` - Bucles
- `repetir X veces` - Bucles con contador
- `repetir mientras` - Bucles condicionales

### Funciones
- `funcion` / `fin funcion` - Definir funciones
- `devolver` - Retornar valores

### Clases
- `clase` / `fin clase` - Definir clases
- `hacer` - Definir métodos

## 🚀 Uso Rápido

### 1. Crear archivo Vader
```bash
# Crear nuevo archivo con extensión .vdr
touch mi_programa.vdr
```

### 2. Escribir código en español natural
```vader
decir "¡Hola mundo desde Vader!"
preguntar "¿Cómo te llamas?" y guardar la respuesta en nombre
decir "¡Hola " + nombre + "! Bienvenido a la programación"

si nombre es igual a "Vader"
    decir "¡Excelente nombre! 🚀"
sino
    decir "¡Gracias por usar Vader!"
fin si
```

### 3. Ejecutar desde terminal
```bash
python3 src/vader.py mi_programa.vdr
```

## 📚 Snippets Disponibles

Escribe estas abreviaciones y presiona `Tab`:

- `decir` → `decir "texto"`
- `preguntar` → `preguntar "pregunta" y guardar la respuesta en variable`
- `si` → Estructura completa de condicional
- `repetir` → Estructura completa de bucle
- `funcion` → Estructura completa de función
- `clase` → Estructura completa de clase

## 🎨 Temas Incluidos

- **Vader Dark** - Tema oscuro optimizado para Vader
- **Vader Light** - Tema claro con colores suaves
- **Vader Neon** - Tema oscuro con acentos neón

Para activar: `Ctrl+K Ctrl+T` → Seleccionar tema Vader

## ⚙️ Configuración

La extensión se activa automáticamente para archivos `.vdr`. 

### Configuraciones disponibles:
```json
{
    "vader.enableSnippets": true,
    "vader.enableSyntaxHighlighting": true,
    "vader.theme": "vader-dark"
}
```

## 🌍 Soporte Multiidioma

Vader soporta **11 idiomas**:
- 🇪🇸 Español - `decir "¡Hola!"`
- 🇺🇸 English - `say "Hello!"`
- 🇫🇷 Français - `dire "Bonjour!"`
- 🇵🇹 Português - `dizer "Olá!"`
- 🇮🇹 Italiano - `dire "Ciao!"`
- 🇨🇳 中文 - `说 "你好!"`
- 🇯🇵 日本語 - `言う "こんにちは!"`
- 🇷🇺 Русский - `сказать "Привет!"`
- 🇩🇪 Deutsch - `sagen "Hallo!"`
- 🇸🇦 العربية - `قول "مرحبا!"`
- 🇰🇷 한국어 - `말하다 "안녕하세요!"`

## 🔧 Instalación

### Desde VS Code Marketplace
1. Abre VS Code
2. Ve a Extensions (`Ctrl+Shift+X`)
3. Busca "Vader Language Support"
4. Haz clic en "Install"

### Desde archivo local
```bash
cd vscode_extension
code --install-extension .
```

## 📖 Documentación Completa

- [Guía de Inicio Rápido](../VADER_SUPER_FACIL.md)
- [Sintaxis Completa](../PROGRAMAR_COMO_HABLAR.md)
- [Ejemplos](../ejemplos/)
- [Documentación Técnica](../docs/)

## 🚀 Características de Vader

- **Universal**: Funciona en 11 idiomas
- **25+ Frameworks**: React, Vue, Angular, Django, Laravel, etc.
- **Runtime Nativo**: Ejecuta sin transpilación
- **IA Integrada**: Asistente de programación
- **Multiplataforma**: Windows, macOS, Linux

## 🆘 Soporte

¿Problemas o sugerencias?

- 📧 **Issues**: [GitHub Issues](https://github.com/LangVader/core/issues)
- 📚 **Documentación**: [README Principal](../README.md)
- 🌐 **Sitio Web**: [vader-lang.org](https://vader-lang.org)

## 📄 Licencia

MIT License - Consulta [LICENSE](../LICENSE) para más detalles.

---

**¡Democratizando la programación para toda la humanidad!** 🌍

*Vader - El primer lenguaje universal multiidioma del mundo*
