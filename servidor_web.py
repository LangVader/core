#!/usr/bin/env python3
"""
VADER SERVIDOR WEB - Editor web funcional
"""

import http.server
import socketserver
import webbrowser
import os
import json
import urllib.parse
import mimetypes
from pathlib import Path

PORT = 8080

class VaderHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/editor':
            self.serve_editor()
        elif self.path == '/logo.png':
            # Servir el logo de Vader
            logo_path = os.path.join(os.path.dirname(__file__), 'assets', 'logo.png')
            print(f"🔍 Buscando logo en: {logo_path}")
            print(f"📁 Existe el archivo: {os.path.exists(logo_path)}")
            if os.path.exists(logo_path):
                print("✅ Sirviendo logo de Vader")
                self.send_response(200)
                self.send_header('Content-type', 'image/png')
                self.send_header('Cache-Control', 'no-cache')
                self.end_headers()
                with open(logo_path, 'rb') as f:
                    self.wfile.write(f.read())
            else:
                print("❌ Logo no encontrado")
                self.send_response(404)
                self.end_headers()
        else:
            super().do_GET()
    
    def serve_editor(self):
        html = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>VADER - Editor Web</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: Arial, sans-serif; background: #000; color: #fff; height: 100vh; }
        header { background: linear-gradient(135deg, #1a1a1a, #2d2d2d); padding: 20px; text-align: center; border-bottom: 2px solid #ffd700; box-shadow: 0 2px 10px rgba(255,215,0,0.3); display: flex; align-items: center; justify-content: center; gap: 20px; }
        header img { height: 60px; width: auto; filter: drop-shadow(0 0 10px rgba(255,215,0,0.3)); }
        header h1 { color: #ffd700; margin: 0; font-size: 2.5em; text-shadow: 0 0 20px rgba(255,215,0,0.5); font-weight: bold; }
        header p { color: #cccccc; margin: 10px 0 0 0; font-size: 1.1em; }
        .main { display: flex; height: calc(100vh - 100px); }
        .left, .right, .ai-panel { flex: 1; display: flex; flex-direction: column; }
        .left { border-right: 2px solid #333; }
        .right { border-right: 2px solid #333; }
        .panel-header { background: #1a1a1a; padding: 10px; font-weight: bold; color: #ffd700; }
        .editor, .preview { flex: 1; background: #0d1117; color: #fff; border: none; padding: 15px; font-family: monospace; font-size: 14px; resize: none; outline: none; }
        .preview { font-size: 12px; }
        .toolbar { background: #1a1a1a; padding: 10px; display: flex; gap: 10px; align-items: center; }
        .btn { background: #2d2d2d; color: #fff; border: none; padding: 8px 15px; border-radius: 3px; cursor: pointer; }
        .btn:hover { background: #404040; }
        .btn.primary { background: #ffd700; color: #000; }
        .select { background: #2d2d2d; color: #fff; border: 1px solid #444; padding: 5px; }
        .status { background: #111; padding: 8px 15px; border-top: 1px solid #333; font-size: 12px; color: #ccc; }
        .examples { padding: 10px; background: #1a1a1a; }
        .example-btn { background: #2d2d2d; color: #fff; border: none; padding: 5px 10px; margin: 2px; border-radius: 3px; cursor: pointer; font-size: 11px; }
        .chat-container { display: flex; flex-direction: column; height: 100%; }
        .chat-messages { flex: 1; padding: 10px; overflow-y: auto; background: #0d1117; }
        .message { margin-bottom: 10px; padding: 8px; border-radius: 5px; }
        .message.user { background: #1a1a1a; text-align: right; }
        .message.ai { background: #2d2d2d; }
        .chat-input { display: flex; padding: 10px; background: #1a1a1a; }
        .chat-input input { flex: 1; background: #2d2d2d; color: #fff; border: 1px solid #444; padding: 8px; border-radius: 3px; }
        .ai-actions { padding: 10px; background: #1a1a1a; display: flex; flex-wrap: wrap; gap: 5px; }
        .ai-btn { background: #2d2d2d; color: #ffd700; border: 1px solid #444; padding: 5px 8px; border-radius: 3px; cursor: pointer; font-size: 10px; }
        .ai-btn:hover { background: #ffd700; color: #000; }
    </style>
</head>
<body>
    <header>
        <img src="/logo.png" alt="Vader Logo">
        <div>
            <h1>VADER - Editor Web</h1>
            <p>Programación en Español Natural</p>
        </div>
    </header>
    
    <div class="main">
        <div class="left">
            <div class="panel-header">📝 Editor de Código Vader</div>
            <div class="examples">
                <button class="example-btn" onclick="loadExample('calculadora')">Calculadora</button>
                <button class="example-btn" onclick="loadExample('saludo')">Saludo</button>
                <button class="example-btn" onclick="loadExample('web')">Página Web</button>
                <button class="example-btn" onclick="clearEditor()">Limpiar</button>
            </div>
            <textarea id="editor" class="editor" placeholder="Escribe tu código Vader aquí..."># ¡Bienvenido a VADER! 🚀
# El Lenguaje Supremo Universal

# Ejemplo: Calculadora simple
funcion calculadora
    mostrar "=== CALCULADORA VADER ==="
    
    preguntar "Primer número:" guardar la respuesta en num1
    preguntar "Segundo número:" guardar la respuesta en num2
    preguntar "Operación (+, -, *, /):" guardar la respuesta en op
    
    convertir num1 a numero
    convertir num2 a numero
    
    si op es igual a "+"
        resultado = num1 + num2
    sino si op es igual a "-"
        resultado = num1 - num2
    sino si op es igual a "*"
        resultado = num1 * num2
    sino si op es igual a "/"
        resultado = num1 / num2
    sino
        mostrar "Operación no válida"
        terminar
    fin si
    
    mostrar "Resultado: " + resultado
fin funcion

calculadora()</textarea>
        </div>
        
        <div class="right">
            <div class="panel-header">👁️ Código Transpilado</div>
            <div class="toolbar">
                <label>Transpilar a:</label>
                <select id="targetLanguage" class="select">
                    <option value="python">Python</option>
                    <option value="javascript">JavaScript</option>
                    <option value="typescript">TypeScript</option>
                    <option value="html">HTML</option>
                    <option value="css">CSS</option>
                    <option value="java">Java</option>
                    <option value="csharp">C#</option>
                    <option value="php">PHP</option>
                    <option value="ruby">Ruby</option>
                    <option value="go">Go</option>
                    <option value="rust">Rust</option>
                    <option value="swift">Swift</option>
                    <option value="kotlin">Kotlin</option>
                    <option value="dart">Dart</option>
                    <option value="solidity">Solidity</option>
                    <option value="elixir">Elixir</option>
                    <option value="julia">Julia</option>
                </select>
                <button class="btn primary" onclick="transpileCode()">🔄 Transpilar</button>
                <button class="btn" onclick="copyCode()">📋 Copiar</button>
                <button class="btn" onclick="saveCode()">💾 Guardar</button>
            </div>
            <textarea id="preview" class="preview" readonly placeholder="El código transpilado aparecerá aquí..."></textarea>
        </div>
        
        <div class="ai-panel">
            <div class="panel-header">🤖 IA Assistant - Chat</div>
            <div class="ai-actions">
                <button class="ai-btn" onclick="askAI('generar')">✨ Generar Código</button>
                <button class="ai-btn" onclick="askAI('analizar')">🔍 Analizar</button>
                <button class="ai-btn" onclick="askAI('optimizar')">⚡ Optimizar</button>
                <button class="ai-btn" onclick="askAI('explicar')">📚 Explicar</button>
                <button class="ai-btn" onclick="askAI('errores')">🐛 Revisar Errores</button>
                <button class="ai-btn" onclick="clearChat()">🧹 Limpiar Chat</button>
            </div>
            <div class="chat-container">
                <div id="chatMessages" class="chat-messages">
                    <div class="message ai">
                        <strong>🤖 IA Vader:</strong><br>
                        ¡Hola! Soy tu asistente de IA para programar en Vader. Puedo ayudarte a:
                        <ul>
                            <li>✨ Generar código desde descripciones</li>
                            <li>🔍 Analizar y explicar tu código</li>
                            <li>⚡ Optimizar y mejorar el rendimiento</li>
                            <li>🐛 Encontrar y corregir errores</li>
                            <li>📚 Enseñarte sintaxis y mejores prácticas</li>
                        </ul>
                        ¿En qué puedo ayudarte hoy?
                    </div>
                </div>
                <div class="chat-input">
                    <input type="text" id="chatInput" placeholder="Pregúntame algo sobre tu código Vader..." onkeypress="if(event.key==='Enter') sendMessage()">
                    <button class="btn primary" onclick="sendMessage()">📤 Enviar</button>
                </div>
            </div>
        </div>
    </div>
    
    <div class="status">
        <span id="status">Listo para programar en español ✅</span>
    </div>

    <script>
        const examples = {
            calculadora: `# Calculadora en Vader
funcion calculadora
    preguntar "Primer número:" guardar la respuesta en num1
    preguntar "Segundo número:" guardar la respuesta en num2
    preguntar "Operación (+, -, *, /):" guardar la respuesta en op
    
    convertir num1 a numero
    convertir num2 a numero
    
    si op es igual a "+"
        resultado = num1 + num2
    sino si op es igual a "-"
        resultado = num1 - num2
    sino si op es igual a "*"
        resultado = num1 * num2
    sino si op es igual a "/"
        resultado = num1 / num2
    sino
        mostrar "Operación no válida"
        terminar
    fin si
    
    mostrar "Resultado: " + resultado
fin funcion

calculadora()`,
            
            saludo: `# Saludo personalizado
funcion saludar
    preguntar "¿Cómo te llamas?" guardar la respuesta en nombre
    preguntar "¿De dónde eres?" guardar la respuesta en ciudad
    
    mostrar "¡Hola " + nombre + "!"
    mostrar "Es un placer conocerte"
    mostrar "Saludos desde " + ciudad
fin funcion

saludar()`,
            
            web: `# Página web simple
pagina web
    titulo "Mi Primera Página con Vader"
    
    encabezado
        titulo1 "¡Bienvenido!"
        parrafo "Esta página fue creada con Vader"
    fin encabezado
    
    contenido
        titulo2 "Acerca de Vader"
        parrafo "Vader permite programar en español natural"
        
        lista
            elemento "Fácil de aprender"
            elemento "Sintaxis en español"
            elemento "Transpila a múltiples lenguajes"
        fin lista
    fin contenido
fin pagina`
        };
        
        function loadExample(type) {
            document.getElementById('editor').value = examples[type] || '';
            updateStatus('Ejemplo cargado: ' + type);
        }
        
        function clearEditor() {
            document.getElementById('editor').value = '';
            document.getElementById('preview').value = '';
            updateStatus('Editor limpiado');
        }
        
        function transpileCode() {
            const code = document.getElementById('editor').value;
            const target = document.getElementById('targetLanguage').value;
            
            if (!code.trim()) {
                alert('No hay código para transpilar');
                return;
            }
            
            let result = '';
            
            if (target === 'python') {
                result = transpileToPython(code);
            } else if (target === 'javascript') {
                result = transpileToJavaScript(code);
            } else if (target === 'html') {
                result = transpileToHTML(code);
            }
            
            document.getElementById('preview').value = result;
            updateStatus('Código transpilado a ' + target + ' ✅');
        }
        
        function transpileToPython(code) {
            let result = '# Código Vader transpilado a Python\\n\\n';
            const lines = code.split('\\n');
            let indentLevel = 0;
            
            for (let line of lines) {
                const stripped = line.trim();
                
                if (!stripped || stripped.startsWith('#')) {
                    result += line + '\\n';
                    continue;
                }
                
                if (stripped.startsWith('mostrar')) {
                    const content = stripped.replace('mostrar', 'print');
                    result += '    '.repeat(indentLevel) + content + '\\n';
                } else if (stripped.startsWith('funcion')) {
                    const funcName = stripped.replace('funcion', 'def') + '():';
                    result += '    '.repeat(indentLevel) + funcName + '\\n';
                    indentLevel++;
                } else if (stripped.startsWith('fin funcion')) {
                    indentLevel = Math.max(0, indentLevel - 1);
                    result += '\\n';
                } else if (stripped.includes('preguntar') && stripped.includes('guardar la respuesta en')) {
                    const parts = stripped.split(' guardar la respuesta en ');
                    if (parts.length === 2) {
                        const question = parts[0].replace('preguntar', 'input');
                        const varName = parts[1].trim();
                        result += '    '.repeat(indentLevel) + varName + ' = ' + question + '\\n';
                    }
                } else if (stripped.includes('convertir') && stripped.includes('a numero')) {
                    const varName = stripped.replace('convertir', '').replace('a numero', '').trim();
                    result += '    '.repeat(indentLevel) + varName + ' = int(' + varName + ')\\n';
                } else {
                    result += '    '.repeat(indentLevel) + stripped + '\\n';
                }
            }
            
            return result;
        }
        
        function transpileToJavaScript(code) {
            let result = '// Código Vader transpilado a JavaScript\\n\\n';
            const lines = code.split('\\n');
            
            for (let line of lines) {
                const stripped = line.trim();
                
                if (stripped.startsWith('mostrar')) {
                    const content = stripped.replace('mostrar', 'console.log');
                    result += content + ';\\n';
                } else if (stripped.startsWith('funcion')) {
                    const funcName = stripped.replace('funcion', 'function') + ' {';
                    result += funcName + '\\n';
                } else if (stripped.startsWith('fin funcion')) {
                    result += '}\\n\\n';
                } else if (stripped.startsWith('#')) {
                    result += '//' + stripped.substring(1) + '\\n';
                } else if (stripped) {
                    result += '    ' + stripped + ';\\n';
                }
            }
            
            return result;
        }
        
        function transpileToHTML(code) {
            let result = '<!DOCTYPE html>\\n<html lang="es">\\n<head>\\n    <meta charset="UTF-8">\\n    <title>Página Vader</title>\\n</head>\\n<body>\\n';
            const lines = code.split('\\n');
            
            for (let line of lines) {
                const stripped = line.trim();
                
                if (stripped.startsWith('titulo1')) {
                    const content = stripped.replace('titulo1', '').trim().replace(/"/g, '');
                    result += '    <h1>' + content + '</h1>\\n';
                } else if (stripped.startsWith('titulo2')) {
                    const content = stripped.replace('titulo2', '').trim().replace(/"/g, '');
                    result += '    <h2>' + content + '</h2>\\n';
                } else if (stripped.startsWith('parrafo')) {
                    const content = stripped.replace('parrafo', '').trim().replace(/"/g, '');
                    result += '    <p>' + content + '</p>\\n';
                }
            }
            
            result += '</body>\\n</html>';
            return result;
        }
        
        function copyCode() {
            const preview = document.getElementById('preview');
            preview.select();
            document.execCommand('copy');
            updateStatus('Código copiado al portapapeles ✅');
        }
        
        function saveCode() {
            const code = document.getElementById('preview').value;
            const target = document.getElementById('targetLanguage').value;
            const extension = target === 'python' ? '.py' : target === 'javascript' ? '.js' : '.html';
            
            const blob = new Blob([code], { type: 'text/plain' });
            const url = URL.createObjectURL(blob);
            
            const a = document.createElement('a');
            a.href = url;
            a.download = 'codigo_vader' + extension;
            a.click();
            
            URL.revokeObjectURL(url);
            updateStatus('Archivo guardado ✅');
        }
        
        function updateStatus(message) {
            document.getElementById('status').textContent = message;
        }
        
        // Funciones del Chat de IA
        function sendMessage() {
            console.log('sendMessage llamada');
            const input = document.getElementById('chatInput');
            const message = input.value.trim();
            console.log('Mensaje:', message);
            
            if (!message) {
                console.log('Mensaje vacío');
                return;
            }
            
            addMessage('user', message);
            input.value = '';
            updateStatus('Procesando mensaje... 🤖');
            
            // Simular respuesta de IA
            setTimeout(() => {
                const aiResponse = generateAIResponse(message);
                addMessage('ai', aiResponse);
                updateStatus('IA respondió ✅');
            }, 1500);
        }
        
        function askAI(action) {
            const code = document.getElementById('editor').value;
            let prompt = '';
            
            switch(action) {
                case 'generar':
                    prompt = 'Genera código Vader para: ';
                    break;
                case 'analizar':
                    prompt = 'Analiza este código Vader: ' + code.substring(0, 100) + '...';
                    break;
                case 'optimizar':
                    prompt = 'Optimiza este código Vader: ' + code.substring(0, 100) + '...';
                    break;
                case 'explicar':
                    prompt = 'Explica este código Vader: ' + code.substring(0, 100) + '...';
                    break;
                case 'errores':
                    prompt = 'Revisa errores en este código Vader: ' + code.substring(0, 100) + '...';
                    break;
            }
            
            document.getElementById('chatInput').value = prompt;
            document.getElementById('chatInput').focus();
        }
        
        function addMessage(sender, message) {
            const chatMessages = document.getElementById('chatMessages');
            const messageDiv = document.createElement('div');
            messageDiv.className = 'message ' + sender;
            
            if (sender === 'user') {
                messageDiv.innerHTML = '<strong>👤 Tú:</strong><br>' + message;
            } else {
                messageDiv.innerHTML = '<strong>🤖 IA Vader:</strong><br>' + message;
            }
            
            chatMessages.appendChild(messageDiv);
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
        
        function generateAIResponse(message) {
            const responses = {
                'generar': '✨ Para generar código, describe lo que quieres crear. Por ejemplo: "una función que calcule el área de un círculo" o "un programa que ordene una lista".',
                'analizar': '🔍 Tu código Vader se ve bien estructurado. Usa sintaxis natural en español que es fácil de leer y mantener.',
                'optimizar': '⚡ Algunas sugerencias para optimizar: usa nombres descriptivos, evita repetición de código, y considera usar funciones para tareas comunes.',
                'explicar': '📚 Este código Vader utiliza sintaxis natural en español. Las funciones se definen con "funcion", las variables se asignan directamente, y las estructuras de control usan palabras como "si", "sino", "repetir".',
                'errores': '🐛 Revisando tu código... No veo errores obvios. Asegúrate de que las variables estén definidas antes de usarlas y que la indentación sea consistente.'
            };
            
            // Respuestas inteligentes basadas en palabras clave
            const lowerMessage = message.toLowerCase();
            
            if (lowerMessage.includes('función') || lowerMessage.includes('funcion')) {
                return '✨ Para crear una función en Vader usa: "funcion nombre_funcion" seguido del código indentado. Ejemplo:\n\nfuncion saludar\n    mostrar "¡Hola mundo!"\nfin funcion';
            }
            
            if (lowerMessage.includes('variable')) {
                return '📝 En Vader las variables se crean simplemente asignando valores: "nombre = valor". También puedes usar "guardar valor en nombre".';
            }
            
            if (lowerMessage.includes('bucle') || lowerMessage.includes('repetir')) {
                return '🔄 Para bucles en Vader usa: "repetir X veces", "repetir mientras condicion", o "repetir con cada elemento en lista".';
            }
            
            if (lowerMessage.includes('condicional') || lowerMessage.includes('si')) {
                return '🤔 Para condicionales usa: "si condicion" seguido de "sino" para el else y "fin si" para cerrar.';
            }
            
            // Respuesta por defecto
            return '🤖 Entiendo tu pregunta. Vader es un lenguaje natural en español. ¿Podrías ser más específico sobre qué necesitas? Puedo ayudarte con sintaxis, ejemplos, optimización, o depuración.';
        }
        
        function clearChat() {
            const chatMessages = document.getElementById('chatMessages');
            chatMessages.innerHTML = `
                <div class="message ai">
                    <strong>🤖 IA Vader:</strong><br>
                    ¡Chat limpiado! ¿En qué puedo ayudarte ahora?
                </div>
            `;
        }
        
        // Auto-transpilar al cargar
        document.addEventListener('DOMContentLoaded', function() {
            transpileCode();
        });
    </script>
</body>
</html>"""
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))

def main():
    try:
        with socketserver.TCPServer(("", PORT), VaderHandler) as httpd:
            print(f"🌐 Servidor web de Vader iniciado en http://localhost:{PORT}")
            print("🚀 Abriendo editor en el navegador...")
            
            # Abrir navegador automáticamente
            webbrowser.open(f'http://localhost:{PORT}')
            
            print("✅ Editor web funcionando - Presiona Ctrl+C para cerrar")
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n👋 Cerrando servidor web...")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
