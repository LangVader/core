#!/usr/bin/env python3
"""
VADER 7.0 - SERVIDOR WEB PARA ARCHIVOS .VDR NATIVOS
Sirve archivos .vdr directamente con el runtime JavaScript incluido
"""

import http.server
import socketserver
import os
import mimetypes
from pathlib import Path

# Configuración del servidor
PORT = 8000
DIRECTORY = "."

class VaderHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Handler personalizado para servir archivos .vdr nativamente"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)
    
    def guess_type(self, path):
        """Determinar el tipo MIME, incluyendo archivos .vdr"""
        mimetype, encoding = mimetypes.guess_type(path)
        
        # Archivos .vdr se sirven como HTML con runtime incluido
        if path.endswith('.vdr'):
            return 'text/html', encoding
        
        return mimetype, encoding
    
    def do_GET(self):
        """Manejar peticiones GET, especialmente para archivos .vdr"""
        
        # Si es un archivo .vdr, servir con runtime incluido
        if self.path.endswith('.vdr'):
            self.serve_vdr_file()
        else:
            # Comportamiento normal para otros archivos
            super().do_GET()
    
    def serve_vdr_file(self):
        """Servir archivo .vdr con runtime JavaScript incluido"""
        try:
            # Obtener ruta del archivo
            file_path = self.path.lstrip('/')
            
            if not os.path.exists(file_path):
                self.send_error(404, f"Archivo no encontrado: {file_path}")
                return
            
            # Leer contenido del archivo .vdr
            with open(file_path, 'r', encoding='utf-8') as f:
                vdr_content = f.read()
            
            # Leer runtime JavaScript
            runtime_path = 'vader-7.0-universal.js'
            if os.path.exists(runtime_path):
                with open(runtime_path, 'r', encoding='utf-8') as f:
                    runtime_js = f.read()
            else:
                runtime_js = '// Runtime no encontrado'
            
            # Crear HTML que ejecuta el archivo .vdr
            html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Vader 7.0 - {file_path}</title>
    <style>
        body {{
            font-family: 'Courier New', monospace;
            background: #000;
            color: #00ff41;
            margin: 0;
            padding: 20px;
        }}
        .vader-info {{
            position: fixed;
            top: 10px;
            right: 10px;
            background: rgba(0, 255, 65, 0.1);
            border: 1px solid #00ff41;
            padding: 10px;
            border-radius: 5px;
            font-size: 0.8rem;
            z-index: 1000;
        }}
        .vader-info h4 {{
            margin: 0 0 5px 0;
            color: #00ff41;
        }}
    </style>
</head>
<body>
    <div class="vader-info">
        <h4>🚀 Vader 7.0</h4>
        <div>Archivo: {file_path}</div>
        <div>Estado: Ejecutándose nativamente</div>
        <div>Runtime: Activo</div>
    </div>
    
    <div id="vader-content">
        <h1>⚡ Cargando Vader 7.0...</h1>
        <p>Ejecutando archivo .vdr nativamente</p>
    </div>
    
    <!-- Vader Runtime -->
    <script>
{runtime_js}
    </script>
    
    <!-- Código Vader a ejecutar -->
    <script type="text/vader">
{vdr_content}
    </script>
    
    <script>
        // Ejecutar el código Vader automáticamente
        window.addEventListener('load', async function() {{
            try {{
                console.log('🚀 Ejecutando archivo .vdr:', '{file_path}');
                
                const vaderCode = `{vdr_content.replace('`', '\\`')}`;
                const result = await vader.execute(vaderCode);
                
                // Reemplazar contenido con resultado
                if (result.html) {{
                    document.getElementById('vader-content').innerHTML = result.html;
                }}
                
                // Aplicar estilos
                if (result.css) {{
                    vader.injectCSS(result.css);
                }}
                
                // Ejecutar JavaScript
                if (result.javascript) {{
                    vader.executeJS(result.javascript);
                }}
                
                console.log('✅ Archivo .vdr ejecutado exitosamente');
                
            }} catch (error) {{
                console.error('❌ Error ejecutando .vdr:', error);
                document.getElementById('vader-content').innerHTML = `
                    <h1>❌ Error ejecutando {file_path}</h1>
                    <pre>${{error.message}}</pre>
                `;
            }}
        }});
    </script>
</body>
</html>"""
            
            # Enviar respuesta
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.send_header('Content-Length', len(html_content.encode('utf-8')))
            self.end_headers()
            self.wfile.write(html_content.encode('utf-8'))
            
            print(f"✅ Servido archivo .vdr: {file_path}")
            
        except Exception as e:
            print(f"❌ Error sirviendo {self.path}: {e}")
            self.send_error(500, f"Error interno del servidor: {e}")
    
    def log_message(self, format, *args):
        """Log personalizado para el servidor"""
        message = format % args
        print(f"🌐 [{self.address_string()}] {message}")

def start_server():
    """Iniciar el servidor web para archivos .vdr"""
    
    print("🚀 VADER 7.0 - SERVIDOR WEB NATIVO")
    print("⚡ Sirviendo archivos .vdr nativamente")
    print(f"📁 Directorio: {os.path.abspath(DIRECTORY)}")
    print(f"🌐 Puerto: {PORT}")
    print(f"🔗 URL: http://localhost:{PORT}")
    print()
    
    # Verificar que existe el runtime
    if os.path.exists('vader-7.0-universal.js'):
        print("✅ Runtime JavaScript encontrado")
    else:
        print("⚠️  Runtime JavaScript no encontrado")
    
    # Listar archivos .vdr disponibles
    vdr_files = list(Path('.').glob('*.vdr'))
    if vdr_files:
        print("\n📄 Archivos .vdr disponibles:")
        for vdr_file in vdr_files:
            print(f"   🔗 http://localhost:{PORT}/{vdr_file}")
    else:
        print("\n⚠️  No se encontraron archivos .vdr en el directorio")
    
    print("\n" + "="*50)
    print("🎯 Para probar Vader 7.0:")
    print("1. Abre http://localhost:8000/demo_vader_7.0.vdr")
    print("2. O cualquier archivo .vdr en tu navegador")
    print("3. ¡Los archivos .vdr se ejecutarán nativamente!")
    print("="*50)
    print()
    
    try:
        with socketserver.TCPServer(("", PORT), VaderHTTPRequestHandler) as httpd:
            print(f"🌐 Servidor iniciado en http://localhost:{PORT}")
            print("⚡ Presiona Ctrl+C para detener")
            print()
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n⚠️  Servidor detenido por el usuario")
    except Exception as e:
        print(f"❌ Error iniciando servidor: {e}")

if __name__ == "__main__":
    start_server()
