#!/usr/bin/env python3
"""
VADER 7.0 - SERVIDOR WEB PARA ARCHIVOS .VDR NATIVOS
"""

import http.server
import socketserver
import os

PORT = 8000

class VaderHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.endswith('.vdr'):
            self.serve_vdr_file()
        else:
            super().do_GET()
    
    def serve_vdr_file(self):
        try:
            file_path = self.path.lstrip('/')
            
            if not os.path.exists(file_path):
                self.send_error(404)
                return
            
            # Leer archivo .vdr
            with open(file_path, 'r', encoding='utf-8') as f:
                vdr_content = f.read()
            
            # Leer runtime
            runtime_js = ''
            if os.path.exists('vader-7.0-universal.js'):
                with open('vader-7.0-universal.js', 'r', encoding='utf-8') as f:
                    runtime_js = f.read()
                print(f"✅ Runtime cargado: {len(runtime_js)} caracteres")
            else:
                print("❌ Runtime no encontrado: vader-7.0-universal.js")
                runtime_js = 'console.error("Runtime Vader no encontrado");'
            
            # Escapar contenido VDR para JavaScript (más seguro)
            vdr_escaped = vdr_content.replace('\\', '\\\\').replace('`', '\\`').replace('${', '\\${').replace('"', '\\"').replace("'", "\\'")
            
            # NO escapar el runtime JS - mantenerlo intacto
            # El runtime debe cargarse tal como está
            
            # HTML wrapper
            html_template = '''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Vader 7.0 - {filename}</title>
    <style>
        body {{ font-family: monospace; background: #000; color: #00ff41; margin: 20px; }}
        .info {{ position: fixed; top: 10px; right: 10px; background: rgba(0,255,65,0.1); 
                border: 1px solid #00ff41; padding: 10px; border-radius: 5px; }}
    </style>
</head>
<body>
    <div class="info">
        <h4>🚀 Vader 7.0</h4>
        <div>Archivo: {filename}</div>
        <div>Estado: Nativo</div>
    </div>
    
    <div id="content">
        <h1>⚡ Ejecutando Vader 7.0...</h1>
    </div>
    
    <!-- Vader 7.0 Universal Runtime -->
    <script>
{runtime}
    </script>
    
    <!-- Vader Code Execution -->
    <script>
        const vaderCode = `{vdr_code}`;
        
        window.addEventListener('load', async function() {{
            try {{
                console.log('🚀 Ejecutando archivo .vdr nativo:', '{filename}');
                
                // Verificar que vader esté disponible
                if (typeof vader === 'undefined') {{
                    console.error('❌ Error: vader is not defined');
                    console.log('🔧 Intentando inicializar Vader...');
                    window.vader = new VaderUniversalJS();
                }}
                
                const result = await vader.execute(vaderCode);
                
                if (result.html) {{
                    document.getElementById('content').innerHTML = result.html;
                }}
                if (result.css) {{
                    vader.injectCSS(result.css);
                }}
                if (result.javascript) {{
                    vader.executeJS(result.javascript);
                }}
                
                console.log('✅ Archivo .vdr ejecutado nativamente');
                
            }} catch (error) {{
                console.error('❌ Error:', error);
                document.getElementById('content').innerHTML = 
                    '<h1>❌ Error: ' + error.message + '</h1>';
            }}
        }});
    </script>
</body>
</html>'''
            
            html = html_template.format(
                filename=file_path,
                runtime=runtime_js,
                vdr_code=vdr_escaped
            )
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(html.encode('utf-8'))
            
            print(f"✅ Servido archivo .vdr nativo: {file_path}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            self.send_error(500, str(e))

if __name__ == "__main__":
    print("🚀 VADER 7.0 - SERVIDOR .VDR NATIVO")
    print(f"🌐 http://localhost:{PORT}")
    print("📄 Archivos .vdr disponibles:")
    
    vdr_files = [f for f in os.listdir('.') if f.endswith('.vdr')]
    for file in vdr_files:
        print(f"   🔗 http://localhost:{PORT}/{file}")
    
    if not vdr_files:
        print("   ⚠️  No se encontraron archivos .vdr")
    
    print("\n⚡ Presiona Ctrl+C para detener")
    print("="*50)
    
    try:
        with socketserver.TCPServer(("", PORT), VaderHandler) as httpd:
            print(f"🌐 Servidor iniciado en http://localhost:{PORT}")
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n⚠️  Servidor detenido")
    except Exception as e:
        print(f"❌ Error: {e}")
