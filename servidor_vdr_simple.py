#!/usr/bin/env python3
"""
VADER 7.0 - SERVIDOR WEB SIMPLE PARA ARCHIVOS .VDR
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
            
            # HTML wrapper
            html = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Vader 7.0 - {file_path}</title>
    <style>
        body {{ font-family: monospace; background: #000; color: #00ff41; margin: 20px; }}
        .info {{ position: fixed; top: 10px; right: 10px; background: rgba(0,255,65,0.1); 
                border: 1px solid #00ff41; padding: 10px; border-radius: 5px; }}
    </style>
</head>
<body>
    <div class="info">
        <h4>🚀 Vader 7.0</h4>
        <div>Archivo: {file_path}</div>
        <div>Estado: Nativo</div>
    </div>
    
    <div id="content">
        <h1>⚡ Ejecutando Vader 7.0...</h1>
    </div>
    
    <script>{runtime_js}</script>
    
    <script>
        const vaderCode = `{vdr_content.replace("`", "\\`")}`;
        
        window.addEventListener('load', async function() {{
            try {{
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
                console.log('✅ .vdr ejecutado nativamente');
            }} catch (error) {{
                document.getElementById('content').innerHTML = 
                    '<h1>❌ Error: ' + error.message + '</h1>';
            }}
        }});
    </script>
</body>
</html>'''
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(html.encode('utf-8'))
            
        except Exception as e:
            self.send_error(500, str(e))

if __name__ == "__main__":
    print("🚀 VADER 7.0 - SERVIDOR .VDR NATIVO")
    print(f"🌐 http://localhost:{PORT}")
    print("📄 Archivos .vdr disponibles:")
    
    for file in os.listdir('.'):
        if file.endswith('.vdr'):
            print(f"   🔗 http://localhost:{PORT}/{file}")
    
    print("\n⚡ Presiona Ctrl+C para detener")
    
    with socketserver.TCPServer(("", PORT), VaderHandler) as httpd:
        httpd.serve_forever()
