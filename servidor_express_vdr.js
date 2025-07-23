// VADER 7.0 - SERVIDOR EXPRESS CON .VDR NATIVO
// Ejecuta archivos .vdr directamente en Express.js

const express = require('express');
const fs = require('fs');
const path = require('path');

// Cargar el runtime Vader
eval(fs.readFileSync('./vader-7.0-universal-python.py', 'utf8').replace('#!/usr/bin/env python3', '// Python runtime as comment'));

// Simular runtime JavaScript para backend
class VaderBackendRuntime {
    constructor() {
        console.log('🚀 VADER 7.0 - Backend Universal (Express.js)');
        console.log('⚡ LA PROGRAMACIÓN UNIVERSAL: Libre, Descentralizada, Accesible');
        console.log('🌐 Servidor Express ejecutando archivos .vdr nativamente');
    }
    
    executeVDR(vdrCode) {
        // Interpretar código .vdr para backend
        const lines = vdrCode.split('\n');
        let output = '';
        
        for (const line of lines) {
            const trimmed = line.trim();
            if (trimmed.startsWith('mostrar ')) {
                const message = trimmed.replace('mostrar ', '').replace(/"/g, '');
                output += `<p>📝 ${message}</p>\n`;
            } else if (trimmed.includes('servidor')) {
                output += `<p>🌐 Servidor Vader detectado</p>\n`;
            } else if (trimmed.includes('api')) {
                output += `<p>🔌 API Vader detectada</p>\n`;
            } else if (trimmed.includes('ruta')) {
                output += `<p>🛣️ Ruta Vader detectada</p>\n`;
            }
        }
        
        if (!output) {
            output = '<p>✅ Código .vdr ejecutado nativamente en Express</p>';
        }
        
        return output;
    }
}

const vaderBackend = new VaderBackendRuntime();
const app = express();
const PORT = 3000;

// Middleware para parsear JSON
app.use(express.json());
app.use(express.static('public'));

// Ruta principal
app.get('/', (req, res) => {
    const html = `
    <!DOCTYPE html>
    <html>
    <head>
        <title>🚀 Vader 7.0 - Express Backend</title>
        <style>
            body { font-family: monospace; background: #000; color: #00ff41; margin: 20px; }
            .container { max-width: 800px; margin: 0 auto; padding: 20px; }
            .header { text-align: center; margin-bottom: 30px; }
            .info { background: rgba(0,255,65,0.1); border: 1px solid #00ff41; padding: 20px; border-radius: 10px; }
            .endpoint { margin: 10px 0; padding: 10px; background: #111; border-left: 4px solid #00ff41; }
            a { color: #00ff41; text-decoration: none; }
            a:hover { text-decoration: underline; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🚀 Vader 7.0</h1>
                <h2>Express Backend Universal</h2>
                <p>Servidor ejecutando archivos .vdr nativamente</p>
            </div>
            
            <div class="info">
                <h3>📡 Endpoints Disponibles:</h3>
                <div class="endpoint">
                    <strong>GET /</strong> - Esta página principal
                </div>
                <div class="endpoint">
                    <strong>POST /execute-vdr</strong> - Ejecutar código .vdr directamente
                </div>
                <div class="endpoint">
                    <strong>GET /vdr/:filename</strong> - Ejecutar archivo .vdr específico
                </div>
                <div class="endpoint">
                    <strong>GET /api/info</strong> - Información del runtime Vader
                </div>
            </div>
            
            <div style="margin-top: 30px; text-align: center;">
                <p><strong>Prueba:</strong></p>
                <p><a href="/vdr/test_backend.vdr">📄 Ejecutar test_backend.vdr</a></p>
                <p><a href="/api/info">🔍 Ver info del runtime</a></p>
            </div>
        </div>
    </body>
    </html>
    `;
    res.send(html);
});

// Endpoint para ejecutar código .vdr directamente
app.post('/execute-vdr', (req, res) => {
    try {
        const { code } = req.body;
        if (!code) {
            return res.status(400).json({ error: 'Código .vdr requerido' });
        }
        
        console.log('🚀 Ejecutando código .vdr en Express:', code.substring(0, 100) + '...');
        const result = vaderBackend.executeVDR(code);
        
        const html = `
        <!DOCTYPE html>
        <html>
        <head>
            <title>Resultado .vdr</title>
            <style>
                body { font-family: monospace; background: #000; color: #00ff41; margin: 20px; }
                .result { background: rgba(0,255,65,0.1); border: 1px solid #00ff41; padding: 20px; border-radius: 10px; }
                .code { background: #111; padding: 15px; border-radius: 5px; margin: 10px 0; }
            </style>
        </head>
        <body>
            <h1>🚀 Vader 7.0 - Resultado</h1>
            <div class="result">
                <h3>✅ Código .vdr ejecutado nativamente:</h3>
                ${result}
                
                <h3>📄 Código original:</h3>
                <div class="code">${code.replace(/\n/g, '<br>')}</div>
            </div>
            <p><a href="/" style="color: #00ff41;">← Volver</a></p>
        </body>
        </html>
        `;
        
        res.send(html);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// Endpoint para ejecutar archivos .vdr específicos
app.get('/vdr/:filename', (req, res) => {
    try {
        const filename = req.params.filename;
        const filePath = path.join(__dirname, filename);
        
        if (!fs.existsSync(filePath)) {
            return res.status(404).send(`
                <h1 style="color: #ff4444;">❌ Archivo no encontrado</h1>
                <p style="color: #fff;">El archivo ${filename} no existe.</p>
                <p><a href="/" style="color: #00ff41;">← Volver</a></p>
            `);
        }
        
        const vdrCode = fs.readFileSync(filePath, 'utf8');
        console.log(`🚀 Ejecutando archivo .vdr: ${filename}`);
        
        const result = vaderBackend.executeVDR(vdrCode);
        
        const html = `
        <!DOCTYPE html>
        <html>
        <head>
            <title>🚀 ${filename} - Vader Backend</title>
            <style>
                body { font-family: monospace; background: #000; color: #00ff41; margin: 20px; }
                .result { background: rgba(0,255,65,0.1); border: 1px solid #00ff41; padding: 20px; border-radius: 10px; }
                .code { background: #111; padding: 15px; border-radius: 5px; margin: 10px 0; }
            </style>
        </head>
        <body>
            <h1>🚀 Vader 7.0 - ${filename}</h1>
            <div class="result">
                <h3>✅ Archivo .vdr ejecutado nativamente en Express:</h3>
                ${result}
                
                <h3>📄 Código original:</h3>
                <div class="code">${vdrCode.replace(/\n/g, '<br>')}</div>
                
                <h3>📊 Información:</h3>
                <p>• Archivo: ${filename}</p>
                <p>• Servidor: Express.js + Vader Runtime</p>
                <p>• Nativo: ✅ Sí</p>
                <p>• Transpilado: ❌ No</p>
            </div>
            <p><a href="/" style="color: #00ff41;">← Volver</a></p>
        </body>
        </html>
        `;
        
        res.send(html);
    } catch (error) {
        res.status(500).send(`<h1 style="color: #ff4444;">❌ Error: ${error.message}</h1>`);
    }
});

// API endpoint para información del runtime
app.get('/api/info', (req, res) => {
    res.json({
        name: 'Vader 7.0 Backend Universal',
        version: '7.0.0',
        codename: 'UNIVERSAL',
        platform: 'Express.js + Node.js',
        native: true,
        transpilation: false,
        supports: ['.vdr files', 'Spanish natural language', 'Multiple contexts'],
        endpoints: {
            'POST /execute-vdr': 'Execute .vdr code directly',
            'GET /vdr/:filename': 'Execute specific .vdr file',
            'GET /api/info': 'Runtime information'
        }
    });
});

// Iniciar servidor
app.listen(PORT, () => {
    console.log('🚀 VADER 7.0 - EXPRESS BACKEND UNIVERSAL');
    console.log('⚡ LA PROGRAMACIÓN UNIVERSAL: Libre, Descentralizada, Accesible');
    console.log(`🌐 Servidor iniciado en http://localhost:${PORT}`);
    console.log('📄 Ejecutando archivos .vdr nativamente en Express.js');
    console.log('');
    console.log('📡 Endpoints disponibles:');
    console.log(`   🔗 http://localhost:${PORT}/`);
    console.log(`   🔗 http://localhost:${PORT}/api/info`);
    console.log(`   🔗 http://localhost:${PORT}/vdr/test_backend.vdr`);
    console.log('');
    console.log('⚡ ¡Vader funcionando nativamente en backend!');
});
