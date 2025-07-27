#!/usr/bin/env python3
"""
Generador de Aplicaciones Completas para Vader
Crea proyectos completos y funcionales desde código Vader
"""

import os
import sys
import json
from pathlib import Path

# Añadir el directorio padre al path para importar transpiladores
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from transpilers.python import PythonTranspiler
from transpilers.javascript import JavaScriptTranspiler

class VaderAppGenerator:
    def __init__(self):
        self.templates = {
            'web_flask': {
                'name': 'Aplicación Web Flask',
                'description': 'Aplicación web completa con Flask',
                'files': ['app.py', 'templates/index.html', 'static/style.css', 'requirements.txt', 'README.md']
            },
            'calculadora': {
                'name': 'Calculadora Web',
                'description': 'Calculadora funcional con interfaz web',
                'files': ['app.py', 'templates/calculadora.html', 'static/calc.css', 'static/calc.js', 'requirements.txt', 'README.md']
            },
            'api_rest': {
                'name': 'API REST',
                'description': 'API REST completa con Flask',
                'files': ['app.py', 'models.py', 'routes.py', 'requirements.txt', 'README.md', 'test_api.py']
            }
        }
    
    def detect_app_type(self, vader_code):
        """Detecta qué tipo de aplicación generar basado en el código Vader"""
        code_lower = vader_code.lower()
        
        if any(word in code_lower for word in ['calculadora', 'sumar', 'restar', 'multiplicar', 'dividir']):
            return 'calculadora'
        elif any(word in code_lower for word in ['api', 'ruta', 'endpoint', 'json']):
            return 'api_rest'
        else:
            return 'web_flask'
    
    def generate_flask_app(self, vader_code, output_dir, app_name="VaderFlaskApp"):
        """Genera una aplicación Flask completa"""
        
        # Transpilar el código Vader a Python
        python_transpiler = PythonTranspiler()
        python_code = python_transpiler.transpile(vader_code)
        
        # Indentar el código Python para que funcione dentro de Flask
        indented_python_code = '\n'.join(['            ' + line if line.strip() else '' for line in python_code.split('\n')])
        
        # Crear estructura de directorios
        app_dir = Path(output_dir) / app_name
        app_dir.mkdir(parents=True, exist_ok=True)
        (app_dir / 'templates').mkdir(exist_ok=True)
        (app_dir / 'static').mkdir(exist_ok=True)
        
        # Generar app.py
        flask_app = f'''#!/usr/bin/env python3
"""
Aplicación Flask generada automáticamente por Vader
"""

import sys
import io
from contextlib import redirect_stdout
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ejecutar', methods=['POST'])
def ejecutar_codigo():
    """Ejecuta el código Vader transpilado"""
    try:
        # Capturar la salida del código
        output_buffer = io.StringIO()
        
        with redirect_stdout(output_buffer):
            # Código Vader transpilado:
{indented_python_code}
        
        output = output_buffer.getvalue()
        return jsonify({{
            "status": "success", 
            "message": "Código ejecutado correctamente",
            "output": output
        }})
    except Exception as e:
        return jsonify({{"status": "error", "message": str(e)}})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
'''
        
        # Generar HTML
        html_template = '''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Aplicación Vader</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
    <div class="container">
        <h1>🌟 Aplicación generada con Vader</h1>
        <p>Esta aplicación fue generada automáticamente desde código Vader.</p>
        
        <div class="card">
            <h2>Código Original Vader:</h2>
            <pre><code>''' + vader_code + '''</code></pre>
        </div>
        
        <button onclick="ejecutarCodigo()" class="btn-primary">Ejecutar Código</button>
        
        <div id="resultado" class="resultado"></div>
    </div>
    
    <script>
        async function ejecutarCodigo() {
            const resultado = document.getElementById('resultado');
            resultado.innerHTML = 'Ejecutando...';
            
            try {
                const response = await fetch('/ejecutar', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'}
                });
                const data = await response.json();
                
                if (data.status === 'success') {
                    let html = '<div class="success">✅ ' + data.message + '</div>';
                    if (data.output && data.output.trim()) {
                        html += '<div class="output"><h3>Salida del programa:</h3><pre>' + data.output + '</pre></div>';
                    }
                    resultado.innerHTML = html;
                } else {
                    resultado.innerHTML = '<div class="error">❌ ' + data.message + '</div>';
                }
            } catch (error) {
                resultado.innerHTML = '<div class="error">❌ Error: ' + error.message + '</div>';
            }
        }
    </script>
</body>
</html>'''
        
        # Generar CSS
        css_styles = '''/* Estilos para aplicación Vader */
body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    margin: 0;
    padding: 0;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
    color: #333;
}

.container {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
}

h1 {
    text-align: center;
    color: white;
    margin-bottom: 30px;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
}

.card {
    background: white;
    border-radius: 10px;
    padding: 20px;
    margin: 20px 0;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

pre {
    background: #f8f9fa;
    border: 1px solid #e9ecef;
    border-radius: 5px;
    padding: 15px;
    overflow-x: auto;
}

.btn-primary {
    background: #007bff;
    color: white;
    border: none;
    padding: 12px 24px;
    border-radius: 5px;
    cursor: pointer;
    font-size: 16px;
    display: block;
    margin: 20px auto;
    transition: background 0.3s;
}

.btn-primary:hover {
    background: #0056b3;
}

.resultado {
    margin-top: 20px;
}

.success {
    background: #d4edda;
    color: #155724;
    padding: 10px;
    border-radius: 5px;
    border: 1px solid #c3e6cb;
}

.error {
    background: #f8d7da;
    color: #721c24;
    padding: 10px;
    border-radius: 5px;
    border: 1px solid #f5c6cb;
}'''
        
        # Generar requirements.txt
        requirements = '''Flask==2.3.3
Werkzeug==2.3.7
'''
        
        # Generar README.md
        readme = f'''# {app_name.title()}

Aplicación web generada automáticamente por **Vader**.

## 🚀 Instalación y Ejecución

### 1. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 2. Ejecutar la aplicación
```bash
python app.py
```

### 3. Abrir en navegador
```
http://localhost:5000
```

## 📝 Código Vader Original

```vader
{vader_code}
```

## 🛠️ Estructura del Proyecto

- `app.py` - Aplicación Flask principal
- `templates/index.html` - Plantilla HTML
- `static/style.css` - Estilos CSS
- `requirements.txt` - Dependencias Python
- `README.md` - Este archivo

## 📚 Documentación

Esta aplicación fue generada usando el transpilador Vader, que convierte código en español natural a aplicaciones web funcionales.

¡Disfruta programando en español con Vader! 🌟
'''
        
        # Escribir archivos
        with open(app_dir / 'app.py', 'w', encoding='utf-8') as f:
            f.write(flask_app)
        
        with open(app_dir / 'templates' / 'index.html', 'w', encoding='utf-8') as f:
            f.write(html_template)
        
        with open(app_dir / 'static' / 'style.css', 'w', encoding='utf-8') as f:
            f.write(css_styles)
        
        with open(app_dir / 'requirements.txt', 'w', encoding='utf-8') as f:
            f.write(requirements)
        
        with open(app_dir / 'README.md', 'w', encoding='utf-8') as f:
            f.write(readme)
        
        return app_dir
    
    def generate_calculadora(self, vader_code, app_name="calculadora_vader"):
        """Genera una calculadora web completa"""
        
        app_dir = Path(app_name)
        app_dir.mkdir(exist_ok=True)
        (app_dir / 'templates').mkdir(exist_ok=True)
        (app_dir / 'static').mkdir(exist_ok=True)
        
        # App Flask para calculadora
        flask_app = '''#!/usr/bin/env python3
"""
Calculadora Web generada por Vader
"""

from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('calculadora.html')

@app.route('/calcular', methods=['POST'])
def calcular():
    try:
        data = request.json
        operacion = data.get('operacion')
        num1 = float(data.get('num1', 0))
        num2 = float(data.get('num2', 0))
        
        if operacion == 'sumar':
            resultado = num1 + num2
        elif operacion == 'restar':
            resultado = num1 - num2
        elif operacion == 'multiplicar':
            resultado = num1 * num2
        elif operacion == 'dividir':
            if num2 == 0:
                return jsonify({"error": "No se puede dividir por cero"})
            resultado = num1 / num2
        else:
            return jsonify({"error": "Operación no válida"})
        
        return jsonify({"resultado": resultado})
    
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
'''
        
        # HTML para calculadora
        calc_html = '''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Calculadora Vader</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='calc.css') }}">
</head>
<body>
    <div class="calculadora">
        <h1>🧮 Calculadora Vader</h1>
        <p>Creada con código Vader en español natural</p>
        
        <div class="calc-container">
            <div class="pantalla">
                <input type="text" id="display" readonly>
            </div>
            
            <div class="botones">
                <button onclick="limpiar()" class="btn-clear">C</button>
                <button onclick="agregarNumero('/')" class="btn-operacion">÷</button>
                <button onclick="agregarNumero('*')" class="btn-operacion">×</button>
                <button onclick="borrar()" class="btn-clear">←</button>
                
                <button onclick="agregarNumero('7')" class="btn-numero">7</button>
                <button onclick="agregarNumero('8')" class="btn-numero">8</button>
                <button onclick="agregarNumero('9')" class="btn-numero">9</button>
                <button onclick="agregarNumero('-')" class="btn-operacion">-</button>
                
                <button onclick="agregarNumero('4')" class="btn-numero">4</button>
                <button onclick="agregarNumero('5')" class="btn-numero">5</button>
                <button onclick="agregarNumero('6')" class="btn-numero">6</button>
                <button onclick="agregarNumero('+')" class="btn-operacion">+</button>
                
                <button onclick="agregarNumero('1')" class="btn-numero">1</button>
                <button onclick="agregarNumero('2')" class="btn-numero">2</button>
                <button onclick="agregarNumero('3')" class="btn-numero">3</button>
                <button onclick="calcular()" class="btn-igual" rowspan="2">=</button>
                
                <button onclick="agregarNumero('0')" class="btn-numero btn-cero">0</button>
                <button onclick="agregarNumero('.')" class="btn-numero">.</button>
            </div>
        </div>
        
        <div class="info">
            <h3>Código Vader Original:</h3>
            <pre>''' + vader_code + '''</pre>
        </div>
    </div>
    
    <script src="{{ url_for('static', filename='calc.js') }}"></script>
</body>
</html>'''
        
        # JavaScript para calculadora
        calc_js = '''// Calculadora JavaScript generada por Vader
let display = document.getElementById('display');
let operacionActual = '';
let numeroAnterior = '';
let operador = '';

function agregarNumero(num) {
    if (display.value === '0' && num !== '.') {
        display.value = num;
    } else {
        display.value += num;
    }
}

function limpiar() {
    display.value = '0';
    operacionActual = '';
    numeroAnterior = '';
    operador = '';
}

function borrar() {
    if (display.value.length > 1) {
        display.value = display.value.slice(0, -1);
    } else {
        display.value = '0';
    }
}

async function calcular() {
    try {
        // Evaluar expresión matemática
        let resultado = eval(display.value);
        display.value = resultado;
    } catch (error) {
        display.value = 'Error';
    }
}

// Soporte para teclado
document.addEventListener('keydown', function(event) {
    const key = event.key;
    
    if (key >= '0' && key <= '9' || key === '.') {
        agregarNumero(key);
    } else if (key === '+' || key === '-' || key === '*' || key === '/') {
        agregarNumero(key);
    } else if (key === 'Enter' || key === '=') {
        calcular();
    } else if (key === 'Escape' || key === 'c' || key === 'C') {
        limpiar();
    } else if (key === 'Backspace') {
        borrar();
    }
});'''
        
        # CSS para calculadora
        calc_css = '''/* Estilos para Calculadora Vader */
body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    margin: 0;
    padding: 20px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
}

.calculadora {
    background: white;
    border-radius: 20px;
    padding: 30px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    max-width: 400px;
    width: 100%;
}

h1 {
    text-align: center;
    color: #333;
    margin-bottom: 10px;
}

p {
    text-align: center;
    color: #666;
    margin-bottom: 30px;
}

.calc-container {
    background: #f8f9fa;
    border-radius: 15px;
    padding: 20px;
    margin-bottom: 20px;
}

.pantalla {
    margin-bottom: 20px;
}

#display {
    width: 100%;
    height: 60px;
    font-size: 24px;
    text-align: right;
    border: 2px solid #ddd;
    border-radius: 10px;
    padding: 0 15px;
    background: white;
    box-sizing: border-box;
}

.botones {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 10px;
}

button {
    height: 50px;
    border: none;
    border-radius: 10px;
    font-size: 18px;
    font-weight: bold;
    cursor: pointer;
    transition: all 0.2s;
}

.btn-numero {
    background: #e9ecef;
    color: #333;
}

.btn-numero:hover {
    background: #dee2e6;
}

.btn-operacion {
    background: #007bff;
    color: white;
}

.btn-operacion:hover {
    background: #0056b3;
}

.btn-igual {
    background: #28a745;
    color: white;
    grid-row: span 2;
}

.btn-igual:hover {
    background: #1e7e34;
}

.btn-clear {
    background: #dc3545;
    color: white;
}

.btn-clear:hover {
    background: #c82333;
}

.btn-cero {
    grid-column: span 2;
}

.info {
    background: #f8f9fa;
    border-radius: 10px;
    padding: 15px;
    margin-top: 20px;
}

.info h3 {
    margin-top: 0;
    color: #333;
}

pre {
    background: white;
    border: 1px solid #ddd;
    border-radius: 5px;
    padding: 10px;
    font-size: 12px;
    overflow-x: auto;
}'''
        
        # Escribir archivos
        with open(app_dir / 'app.py', 'w', encoding='utf-8') as f:
            f.write(flask_app)
        
        with open(app_dir / 'templates' / 'calculadora.html', 'w', encoding='utf-8') as f:
            f.write(calc_html)
        
        with open(app_dir / 'static' / 'calc.js', 'w', encoding='utf-8') as f:
            f.write(calc_js)
        
        with open(app_dir / 'static' / 'calc.css', 'w', encoding='utf-8') as f:
            f.write(calc_css)
        
        with open(app_dir / 'requirements.txt', 'w', encoding='utf-8') as f:
            f.write('Flask==2.3.3\nWerkzeug==2.3.7\n')
        
        readme = f'''# Calculadora Vader

Calculadora web completa generada automáticamente por **Vader**.

## 🚀 Ejecución

```bash
pip install -r requirements.txt
python app.py
```

Abrir: http://localhost:5000

## 📝 Código Vader Original

```vader
{vader_code}
```

¡Calculadora funcional creada con código en español! 🧮
'''
        
        with open(app_dir / 'README.md', 'w', encoding='utf-8') as f:
            f.write(readme)
        
        return app_dir
    
    def generate_js_web_app(self, vader_code, output_dir, app_name="VaderApp"):
        """Genera una aplicación web JavaScript completa"""
        
        # Transpilar el código Vader a JavaScript
        js_transpiler = JavaScriptTranspiler()
        js_code = js_transpiler.transpile(vader_code)
        
        # Crear estructura de directorios
        app_dir = Path(output_dir) / app_name
        app_dir.mkdir(parents=True, exist_ok=True)
        (app_dir / 'css').mkdir(exist_ok=True)
        (app_dir / 'js').mkdir(exist_ok=True)
        
        # Generar index.html
        html_content = f'''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{app_name} - Aplicación Vader</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
    <div class="container">
        <header>
            <h1>🌟 {app_name}</h1>
            <p>Aplicación generada automáticamente con Vader</p>
        </header>
        
        <main>
            <div class="card">
                <h2>Código Vader Original:</h2>
                <pre><code>{vader_code}</code></pre>
            </div>
            
            <div class="card">
                <h2>Resultado de la Ejecución:</h2>
                <div id="output" class="output"></div>
                <button onclick="ejecutarCodigo()" class="btn-primary">Ejecutar Código</button>
            </div>
        </main>
    </div>
    
    <script src="js/app.js"></script>
</body>
</html>'''
        
        # Generar app.js
        js_app_content = f'''// Aplicación JavaScript generada por Vader

// Función para capturar console.log
function capturarConsole() {{
    const output = document.getElementById('output');
    const originalLog = console.log;
    
    console.log = function(...args) {{
        // Llamar al console.log original
        originalLog.apply(console, args);
        
        // Mostrar en la página
        const mensaje = args.map(arg => 
            typeof arg === 'object' ? JSON.stringify(arg) : String(arg)
        ).join(' ');
        
        const div = document.createElement('div');
        div.textContent = mensaje;
        div.className = 'log-line';
        output.appendChild(div);
    }};
}}

// Función para ejecutar el código Vader transpilado
function ejecutarCodigo() {{
    const output = document.getElementById('output');
    output.innerHTML = '<div class="log-line info">Ejecutando código...</div>';
    
    // Configurar captura de console.log
    capturarConsole();
    
    try {{
        // Código Vader transpilado:
{js_code}
        
        if (output.children.length === 1) {{
            output.innerHTML = '<div class="log-line success">✅ Código ejecutado correctamente (sin salida)</div>';
        }}
    }} catch (error) {{
        output.innerHTML = `<div class="log-line error">❌ Error: ${{error.message}}</div>`;
        console.error('Error ejecutando código:', error);
    }}
}}

// Ejecutar automáticamente al cargar la página
document.addEventListener('DOMContentLoaded', function() {{
    console.log('Aplicación Vader cargada correctamente');
}});'''
        
        # Generar style.css
        css_content = '''/* Estilos para aplicación Vader */

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
    padding: 20px;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    background: rgba(255, 255, 255, 0.95);
    border-radius: 20px;
    padding: 30px;
    box-shadow: 0 20px 40px rgba(0,0,0,0.1);
}

header {
    text-align: center;
    margin-bottom: 40px;
    padding-bottom: 20px;
    border-bottom: 2px solid #eee;
}

header h1 {
    color: #333;
    font-size: 2.5em;
    margin-bottom: 10px;
}

header p {
    color: #666;
    font-size: 1.2em;
}

.card {
    background: #f8f9fa;
    border-radius: 15px;
    padding: 25px;
    margin-bottom: 25px;
    border: 1px solid #e9ecef;
}

.card h2 {
    color: #333;
    margin-bottom: 15px;
    font-size: 1.5em;
}

pre {
    background: #2d3748;
    color: #e2e8f0;
    padding: 20px;
    border-radius: 10px;
    overflow-x: auto;
    font-family: 'Courier New', monospace;
    line-height: 1.5;
}

code {
    font-family: 'Courier New', monospace;
}

.output {
    background: #1a202c;
    color: #e2e8f0;
    padding: 20px;
    border-radius: 10px;
    min-height: 100px;
    margin-bottom: 20px;
    font-family: 'Courier New', monospace;
    line-height: 1.6;
}

.log-line {
    margin-bottom: 8px;
    padding: 5px 0;
}

.log-line.info {
    color: #63b3ed;
}

.log-line.success {
    color: #68d391;
}

.log-line.error {
    color: #fc8181;
    font-weight: bold;
}

.btn-primary {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    padding: 15px 30px;
    border-radius: 25px;
    font-size: 16px;
    font-weight: bold;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
}

.btn-primary:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
}

.btn-primary:active {
    transform: translateY(0);
}

@media (max-width: 768px) {
    .container {
        padding: 20px;
        margin: 10px;
    }
    
    header h1 {
        font-size: 2em;
    }
    
    .card {
        padding: 20px;
    }
}'''
        
        # Escribir archivos
        with open(app_dir / 'index.html', 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        with open(app_dir / 'js' / 'app.js', 'w', encoding='utf-8') as f:
            f.write(js_app_content)
        
        with open(app_dir / 'css' / 'style.css', 'w', encoding='utf-8') as f:
            f.write(css_content)
        
        # Generar package.json
        package_json = {
            "name": app_name.lower().replace(' ', '-'),
            "version": "1.0.0",
            "description": f"Aplicación web generada automáticamente por Vader",
            "main": "index.html",
            "scripts": {
                "start": "python -m http.server 8000",
                "serve": "python3 -m http.server 8000"
            },
            "keywords": ["vader", "javascript", "web-app"],
            "author": "Vader Generator",
            "license": "MIT"
        }
        
        with open(app_dir / 'package.json', 'w', encoding='utf-8') as f:
            json.dump(package_json, f, indent=2, ensure_ascii=False)
        
        # Generar README.md
        readme_content = f'''# {app_name}

Aplicación web JavaScript generada automáticamente por **Vader**.

## 🚀 Ejecución

### Opción 1: Servidor HTTP simple
```bash
python -m http.server 8000
# o
python3 -m http.server 8000
```

### Opción 2: Abrir directamente
Abrir `index.html` en tu navegador web.

## 🌐 Acceso

Si usas el servidor HTTP: http://localhost:8000

## 📝 Código Vader Original

```vader
{vader_code}
```

## 🛠️ Estructura del Proyecto

```
{app_name}/
├── index.html          # Página principal
├── css/
│   └── style.css       # Estilos
├── js/
│   └── app.js          # Lógica JavaScript
├── package.json        # Configuración del proyecto
└── README.md          # Este archivo
```

¡Aplicación web funcional creada con código en español! 🌟
'''
        
        with open(app_dir / 'README.md', 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        return app_dir
    
    def generate_js_web_calculator(self, output_dir, app_name="CalculadoraVader"):
        """Genera una calculadora web JavaScript completa"""
        
        # Crear estructura de directorios
        app_dir = Path(output_dir) / app_name
        app_dir.mkdir(parents=True, exist_ok=True)
        (app_dir / 'css').mkdir(exist_ok=True)
        (app_dir / 'js').mkdir(exist_ok=True)
        
        # HTML de la calculadora
        calc_html = f'''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{app_name} - Calculadora Vader</title>
    <link rel="stylesheet" href="css/calculator.css">
</head>
<body>
    <div class="container">
        <div class="calculadora">
            <h1>🧮 {app_name}</h1>
            <p>Calculadora generada con Vader</p>
            
            <div class="calc-container">
                <div class="pantalla">
                    <input type="text" id="display" readonly value="0">
                </div>
                
                <div class="botones">
                    <button onclick="limpiar()" class="btn-clear">C</button>
                    <button onclick="limpiarEntrada()" class="btn-clear">CE</button>
                    <button onclick="borrar()" class="btn-operacion">⌫</button>
                    <button onclick="operacion('/')" class="btn-operacion">÷</button>
                    
                    <button onclick="numero('7')" class="btn-numero">7</button>
                    <button onclick="numero('8')" class="btn-numero">8</button>
                    <button onclick="numero('9')" class="btn-numero">9</button>
                    <button onclick="operacion('*')" class="btn-operacion">×</button>
                    
                    <button onclick="numero('4')" class="btn-numero">4</button>
                    <button onclick="numero('5')" class="btn-numero">5</button>
                    <button onclick="numero('6')" class="btn-numero">6</button>
                    <button onclick="operacion('-')" class="btn-operacion">-</button>
                    
                    <button onclick="numero('1')" class="btn-numero">1</button>
                    <button onclick="numero('2')" class="btn-numero">2</button>
                    <button onclick="numero('3')" class="btn-numero">3</button>
                    <button onclick="operacion('+')" class="btn-operacion">+</button>
                    
                    <button onclick="numero('0')" class="btn-numero btn-cero">0</button>
                    <button onclick="decimal()" class="btn-numero">.</button>
                    <button onclick="calcular()" class="btn-igual">=</button>
                </div>
            </div>
            
            <div class="info">
                <h3>Funciones:</h3>
                <p>• Operaciones básicas: +, -, ×, ÷</p>
                <p>• Decimales y borrado</p>
                <p>• Generada automáticamente por Vader</p>
            </div>
        </div>
    </div>
    
    <script src="js/calculator.js"></script>
</body>
</html>'''
        
        # JavaScript de la calculadora
        calc_js = '''// Calculadora JavaScript generada por Vader

let display = document.getElementById('display');
let operacionActual = '';
let operadorAnterior = null;
let esperandoOperando = false;

function actualizarDisplay(valor) {
    display.value = valor;
}

function numero(num) {
    if (esperandoOperando) {
        actualizarDisplay(num);
        esperandoOperando = false;
    } else {
        const valorActual = display.value;
        actualizarDisplay(valorActual === '0' ? num : valorActual + num);
    }
}

function decimal() {
    if (esperandoOperando) {
        actualizarDisplay('0.');
        esperandoOperando = false;
    } else if (display.value.indexOf('.') === -1) {
        actualizarDisplay(display.value + '.');
    }
}

function operacion(siguienteOperador) {
    const valorEntrada = parseFloat(display.value);
    
    if (operacionActual === '') {
        operacionActual = valorEntrada;
    } else if (operadorAnterior) {
        const valorActual = operacionActual || 0;
        const resultado = realizarCalculo[operadorAnterior](valorActual, valorEntrada);
        
        actualizarDisplay(String(resultado));
        operacionActual = resultado;
    }
    
    esperandoOperando = true;
    operadorAnterior = siguienteOperador;
}

const realizarCalculo = {
    '+': (anterior, actual) => anterior + actual,
    '-': (anterior, actual) => anterior - actual,
    '*': (anterior, actual) => anterior * actual,
    '/': (anterior, actual) => actual !== 0 ? anterior / actual : 0
};

function calcular() {
    const valorEntrada = parseFloat(display.value);
    
    if (operacionActual !== '' && operadorAnterior) {
        const valorActual = operacionActual || 0;
        const resultado = realizarCalculo[operadorAnterior](valorActual, valorEntrada);
        
        actualizarDisplay(String(resultado));
        operacionActual = '';
        operadorAnterior = null;
        esperandoOperando = true;
    }
}

function limpiar() {
    actualizarDisplay('0');
    operacionActual = '';
    operadorAnterior = null;
    esperandoOperando = false;
}

function limpiarEntrada() {
    actualizarDisplay('0');
}

function borrar() {
    const valorActual = display.value;
    if (valorActual.length > 1) {
        actualizarDisplay(valorActual.slice(0, -1));
    } else {
        actualizarDisplay('0');
    }
}

// Soporte para teclado
document.addEventListener('keydown', function(event) {
    const key = event.key;
    
    if (key >= '0' && key <= '9') {
        numero(key);
    } else if (key === '.') {
        decimal();
    } else if (key === '+' || key === '-' || key === '*' || key === '/') {
        operacion(key);
    } else if (key === 'Enter' || key === '=') {
        calcular();
    } else if (key === 'Escape' || key === 'c' || key === 'C') {
        limpiar();
    } else if (key === 'Backspace') {
        borrar();
    }
});

console.log('Calculadora Vader cargada correctamente! 🧮');'''
        
        # CSS de la calculadora
        calc_css = '''/* Estilos para Calculadora Vader */

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    padding: 20px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
}

.container {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
}

.calculadora {
    background: white;
    border-radius: 20px;
    padding: 30px;
    box-shadow: 0 20px 40px rgba(0,0,0,0.2);
    max-width: 400px;
    width: 100%;
}

h1 {
    text-align: center;
    color: #333;
    margin-bottom: 10px;
    font-size: 2em;
}

p {
    text-align: center;
    color: #666;
    margin-bottom: 30px;
}

.calc-container {
    background: #f8f9fa;
    border-radius: 15px;
    padding: 20px;
    margin-bottom: 20px;
}

.pantalla {
    margin-bottom: 20px;
}

#display {
    width: 100%;
    height: 70px;
    font-size: 28px;
    text-align: right;
    border: 2px solid #ddd;
    border-radius: 10px;
    padding: 0 20px;
    background: white;
    box-sizing: border-box;
    font-family: 'Courier New', monospace;
    color: #333;
}

.botones {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
}

button {
    height: 60px;
    border: none;
    border-radius: 12px;
    font-size: 20px;
    font-weight: bold;
    cursor: pointer;
    transition: all 0.2s ease;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}

button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 10px rgba(0,0,0,0.2);
}

button:active {
    transform: translateY(0);
}

.btn-numero {
    background: #e9ecef;
    color: #333;
}

.btn-numero:hover {
    background: #dee2e6;
}

.btn-operacion {
    background: linear-gradient(135deg, #007bff, #0056b3);
    color: white;
}

.btn-operacion:hover {
    background: linear-gradient(135deg, #0056b3, #004085);
}

.btn-igual {
    background: linear-gradient(135deg, #28a745, #1e7e34);
    color: white;
    grid-row: span 2;
}

.btn-igual:hover {
    background: linear-gradient(135deg, #1e7e34, #155724);
}

.btn-clear {
    background: linear-gradient(135deg, #dc3545, #c82333);
    color: white;
}

.btn-clear:hover {
    background: linear-gradient(135deg, #c82333, #bd2130);
}

.btn-cero {
    grid-column: span 2;
}

.info {
    background: #f8f9fa;
    border-radius: 10px;
    padding: 20px;
    margin-top: 20px;
    border: 1px solid #e9ecef;
}

.info h3 {
    margin-top: 0;
    margin-bottom: 10px;
    color: #333;
}

.info p {
    margin: 5px 0;
    text-align: left;
    font-size: 14px;
}

@media (max-width: 480px) {
    .calculadora {
        padding: 20px;
        margin: 10px;
    }
    
    button {
        height: 50px;
        font-size: 18px;
    }
    
    #display {
        height: 60px;
        font-size: 24px;
    }
}'''
        
        # Escribir archivos
        with open(app_dir / 'index.html', 'w', encoding='utf-8') as f:
            f.write(calc_html)
        
        with open(app_dir / 'js' / 'calculator.js', 'w', encoding='utf-8') as f:
            f.write(calc_js)
        
        with open(app_dir / 'css' / 'calculator.css', 'w', encoding='utf-8') as f:
            f.write(calc_css)
        
        # Generar package.json
        package_json = {
            "name": app_name.lower().replace(' ', '-'),
            "version": "1.0.0",
            "description": "Calculadora web generada automáticamente por Vader",
            "main": "index.html",
            "scripts": {
                "start": "python -m http.server 8000",
                "serve": "python3 -m http.server 8000"
            },
            "keywords": ["vader", "calculator", "javascript"],
            "author": "Vader Generator",
            "license": "MIT"
        }
        
        with open(app_dir / 'package.json', 'w', encoding='utf-8') as f:
            json.dump(package_json, f, indent=2, ensure_ascii=False)
        
        # Generar README.md
        readme_content = f'''# {app_name}

Calculadora web JavaScript completa generada automáticamente por **Vader**.

## 🚀 Ejecución

### Opción 1: Servidor HTTP simple
```bash
python -m http.server 8000
# o
python3 -m http.server 8000
```

### Opción 2: Abrir directamente
Abrir `index.html` en tu navegador web.

## 🌐 Acceso

Si usas el servidor HTTP: http://localhost:8000

## ✨ Características

- ➕ Suma, resta, multiplicación y división
- 🔢 Soporte para números decimales
- ⌨️ Funciona con teclado y mouse
- 🎨 Interfaz moderna y responsiva
- 🧮 Funcionalidad completa de calculadora

## 🛠️ Estructura del Proyecto

```
{app_name}/
├── index.html              # Página principal
├── css/
│   └── calculator.css      # Estilos de la calculadora
├── js/
│   └── calculator.js       # Lógica de la calculadora
├── package.json           # Configuración del proyecto
└── README.md             # Este archivo
```

¡Calculadora funcional creada con Vader! 🧮✨
'''
        
        with open(app_dir / 'README.md', 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        return app_dir

    def generate_complete_app(self, vader_code, output_dir, app_name="VaderApp", target_language="python"):
        """Genera una aplicación completa basada en el código Vader"""
        
        # Detectar tipo de aplicación
        app_type = self.detect_app_type(vader_code)
        
        print(f"Generando aplicación tipo: {app_type} en {target_language}")
        
        if target_language == "javascript":
            if app_type == "web_calculator":
                return self.generate_js_web_calculator(output_dir, app_name)
            else:
                return self.generate_js_web_app(vader_code, output_dir, app_name)
        else:  # Python por defecto
            if app_type == "web_calculator":
                return self.generate_web_calculator(output_dir, app_name)
            elif app_type == "flask_web":
                return self.generate_flask_web_app(vader_code, output_dir, app_name)
            else:
                return self.generate_basic_flask_app(vader_code, output_dir, app_name)
