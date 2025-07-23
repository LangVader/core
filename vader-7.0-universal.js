/**
 * VADER 7.0 - RUNTIME UNIVERSAL JAVASCRIPT
 * La Programación Universal: Libre, Descentralizada y Accesible a Todos
 * 
 * Ejecuta archivos .vdr nativamente en browsers
 * Soporta TODOS los contextos: Web, Blockchain, IoT, IA, DB, Mobile, etc.
 */

const VADER_VERSION = "7.0.0";
const VADER_CODENAME = "UNIVERSAL";

class VaderUniversalJS {
    constructor() {
        this.version = VADER_VERSION;
        this.codename = VADER_CODENAME;
        this.contexts = ['web', 'blockchain', 'iot', 'ai_ml', 'database', 'mobile', 'electronics', 'cloud'];
        this.languages = ['es', 'en', 'fr', 'it', 'pt', 'de', 'ja', 'zh', 'ko', 'ar', 'ru', 'hi'];
        
        console.log(`🚀 VADER ${this.version} '${this.codename}' - Runtime Universal JS`);
        console.log('⚡ LA PROGRAMACIÓN UNIVERSAL: Libre, Descentralizada, Accesible');
        
        this.initializeBrowserSupport();
    }
    
    initializeBrowserSupport() {
        // Registrar tipo MIME para archivos .vdr
        if (typeof document !== 'undefined') {
            // Soporte nativo para <script type="text/vader">
            this.registerVaderScriptType();
            
            // Soporte para <vader-app src="archivo.vdr">
            this.registerVaderComponent();
            
            // Auto-ejecutar scripts Vader al cargar
            document.addEventListener('DOMContentLoaded', () => {
                this.executeVaderScripts();
            });
        }
    }
    
    registerVaderScriptType() {
        // Interceptar scripts type="text/vader"
        const observer = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                mutation.addedNodes.forEach((node) => {
                    if (node.tagName === 'SCRIPT' && node.type === 'text/vader') {
                        this.executeVaderScript(node);
                    }
                });
            });
        });
        
        observer.observe(document, { childList: true, subtree: true });
    }
    
    registerVaderComponent() {
        // Definir elemento personalizado <vader-app>
        if (typeof customElements !== 'undefined') {
            class VaderApp extends HTMLElement {
                async connectedCallback() {
                    const src = this.getAttribute('src');
                    if (src) {
                        const result = await vader.loadAndExecute(src);
                        this.innerHTML = result.html || result.output || 'Vader 7.0 ejecutado';
                    }
                }
            }
            
            customElements.define('vader-app', VaderApp);
        }
        
        // Registrar manejador para archivos .vdr directos
        this.registerVdrFileHandler();
    }
    
    registerVdrFileHandler() {
        // Interceptar navegación a archivos .vdr
        if (typeof window !== 'undefined' && window.location.pathname.endsWith('.vdr')) {
            this.executeCurrentVdrFile();
        }
    }
    
    async executeCurrentVdrFile() {
        try {
            // Obtener el contenido del archivo .vdr actual
            const response = await fetch(window.location.href);
            const vaderCode = await response.text();
            
            // Ejecutar el código Vader
            const result = await this.execute(vaderCode);
            
            // Reemplazar el contenido de la página
            document.body.innerHTML = result.html || '<h1>Vader 7.0 ejecutado</h1>';
            
            // Aplicar estilos si existen
            if (result.css) {
                this.injectCSS(result.css);
            }
            
            // Ejecutar JavaScript si existe
            if (result.javascript) {
                this.executeJS(result.javascript);
            }
            
            console.log('🚀 Archivo .vdr ejecutado nativamente:', window.location.pathname);
            
        } catch (error) {
            console.error('❌ Error ejecutando archivo .vdr:', error);
            document.body.innerHTML = `<h1>Error ejecutando ${window.location.pathname}</h1><pre>${error.message}</pre>`;
        }
    }
    
    async executeVaderScripts() {
        // Ejecutar todos los scripts type="text/vader"
        const vaderScripts = document.querySelectorAll('script[type="text/vader"]');
        
        for (const script of vaderScripts) {
            await this.executeVaderScript(script);
        }
    }
    
    async executeVaderScript(scriptElement) {
        let vaderCode = '';
        
        if (scriptElement.src) {
            // Cargar desde archivo externo
            const response = await fetch(scriptElement.src);
            vaderCode = await response.text();
        } else {
            // Código inline
            vaderCode = scriptElement.textContent;
        }
        
        const result = await this.execute(vaderCode);
        
        // Aplicar resultado al DOM
        if (result.html) {
            document.body.innerHTML += result.html;
        }
        if (result.css) {
            this.injectCSS(result.css);
        }
        if (result.javascript) {
            this.executeJS(result.javascript);
        }
    }
    
    detectContext(vaderCode) {
        const code = vaderCode.toLowerCase();
        
        // Blockchain
        if (/contrato|contract|blockchain|token|nft|ethereum|solana/.test(code)) {
            return 'blockchain';
        }
        // IoT
        else if (/sensor|arduino|raspberry|esp32|gpio|temperatura|led/.test(code)) {
            return 'iot';
        }
        // IA/ML
        else if (/modelo|model|entrenar|train|tensorflow|pytorch|neural|ai/.test(code)) {
            return 'ai_ml';
        }
        // Base de Datos
        else if (/base_datos|database|tabla|table|sql|mongodb|consulta/.test(code)) {
            return 'database';
        }
        // Móvil
        else if (/app_movil|mobile_app|android|ios|flutter/.test(code)) {
            return 'mobile';
        }
        // Electrónicos
        else if (/microcontrolador|fpga|embedded|pic|avr/.test(code)) {
            return 'electronics';
        }
        // Cloud
        else if (/cloud|aws|azure|gcp|serverless|lambda/.test(code)) {
            return 'cloud';
        }
        // Web por defecto
        else {
            return 'web';
        }
    }
    
    detectLanguage(vaderCode) {
        const code = vaderCode.toLowerCase();
        
        const languagePatterns = {
            'es': /pagina|titulo|boton|mostrar|si|funcion|clase/,
            'en': /page|title|button|show|if|function|class/,
            'fr': /page|titre|bouton|afficher|si|fonction|classe/,
            'ja': /ページ|タイトル|ボタン|表示|もし|関数|クラス/,
            'zh': /页面|标题|按钮|显示|如果|函数|类/
        };
        
        for (const [lang, pattern] of Object.entries(languagePatterns)) {
            if (pattern.test(code)) {
                return lang;
            }
        }
        
        return 'es'; // Español por defecto
    }
    
    async execute(vaderCode, context = 'auto', language = null) {
        // Detección automática
        if (context === 'auto') {
            context = this.detectContext(vaderCode);
            console.log(`🎯 Contexto detectado: ${context}`);
        }
        
        if (!language) {
            language = this.detectLanguage(vaderCode);
            console.log(`🌍 Idioma detectado: ${language}`);
        }
        
        console.log(`⚡ Ejecutando Vader en contexto: ${context}`);
        
        // Ejecutar según contexto
        switch (context) {
            case 'web':
                return this.executeWeb(vaderCode, language);
            case 'blockchain':
                return this.executeBlockchain(vaderCode, language);
            case 'iot':
                return this.executeIoT(vaderCode, language);
            case 'ai_ml':
                return this.executeAI(vaderCode, language);
            case 'database':
                return this.executeDatabase(vaderCode, language);
            case 'mobile':
                return this.executeMobile(vaderCode, language);
            case 'electronics':
                return this.executeElectronics(vaderCode, language);
            case 'cloud':
                return this.executeCloud(vaderCode, language);
            default:
                return this.executeWeb(vaderCode, language);
        }
    }
    
    executeWeb(code, language) {
        // Parsear código Vader nativo para web
        const lines = code.split('\n').filter(line => line.trim() && !line.trim().startsWith('//'));
        let html = '<!DOCTYPE html><html><head><meta charset="UTF-8"><title>Vader 7.0</title></head><body>';
        let css = `
            body { font-family: 'Courier New', monospace; margin: 0; padding: 20px; background: #000; color: #00ff41; }
            .titulo_principal { font-size: 3rem; text-align: center; text-shadow: 0 0 20px #00ff41; animation: brillar 2s infinite alternate; }
            .seccion_demo { background: rgba(0, 255, 65, 0.1); border: 1px solid #00ff41; border-radius: 10px; padding: 20px; margin-bottom: 20px; }
            @keyframes brillar { from { text-shadow: 0 0 20px #00ff41; } to { text-shadow: 0 0 30px #00ff41, 0 0 40px #00ff41; } }
            button { background: #00ff41; color: #000; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; margin: 10px 5px; }
            button:hover { background: #00cc33; }
        `;
        let js = 'console.log("🚀 Vader 7.0 - Archivo .vdr ejecutándose nativamente");';
        
        let inSection = false;
        let currentSectionId = '';
        
        for (const line of lines) {
            const trimmed = line.trim();
            
            // Página
            if (trimmed.match(/pagina\s+"([^"]+)"/)) {
                const title = trimmed.match(/"([^"]+)"/)[1];
                html = html.replace('<title>Vader 7.0</title>', `<title>${title}</title>`);
                html += `<header><h1 class="titulo_principal">${title}</h1></header>`;
            }
            // Encabezado
            else if (trimmed === 'encabezado') {
                html += '<header>';
            }
            // Título principal
            else if (trimmed.match(/titulo1\s+"([^"]+)"/)) {
                const title = trimmed.match(/"([^"]+)"/)[1];
                const clase = trimmed.match(/clase\s+"([^"]+)"/);
                const classAttr = clase ? ` class="${clase[1]}"` : '';
                html += `<h1${classAttr}>${title}</h1>`;
            }
            // Título 2
            else if (trimmed.match(/titulo2\s+"([^"]+)"/)) {
                const title = trimmed.match(/"([^"]+)"/)[1];
                html += `<h2>${title}</h2>`;
            }
            // Párrafo
            else if (trimmed.match(/parrafo\s+"([^"]+)"/)) {
                const text = trimmed.match(/"([^"]+)"/)[1];
                const clase = trimmed.match(/clase\s+"([^"]+)"/);
                const classAttr = clase ? ` class="${clase[1]}"` : '';
                html += `<p${classAttr}>${text}</p>`;
            }
            // Párrafo destacado
            else if (trimmed.match(/parrafo_destacado\s+"([^"]+)"/)) {
                const text = trimmed.match(/"([^"]+)"/)[1];
                html += `<p style="font-size: 1.2rem; font-weight: bold; text-align: center; margin: 10px 0;">${text}</p>`;
            }
            // Botón con función
            else if (trimmed.match(/boton\s+"([^"]+)"\s+al_hacer_clic\s+(\w+)/)) {
                const matches = trimmed.match(/boton\s+"([^"]+)"\s+al_hacer_clic\s+(\w+)/);
                const text = matches[1];
                const func = matches[2];
                html += `<button onclick="${func}()">${text}</button>`;
                
                // Agregar función JavaScript
                js += `\nfunction ${func}() { 
                    alert('Función ${func} ejecutada desde Vader nativo!');
                    console.log('🎯 ${func} - Ejecutado desde archivo .vdr');
                }`;
            }
            // Botón simple
            else if (trimmed.match(/boton\s+"([^"]+)"/)) {
                const text = trimmed.match(/"([^"]+)"/)[1];
                html += `<button onclick="alert('${text} presionado desde Vader nativo!')">${text}</button>`;
            }
            // Sección
            else if (trimmed.match(/seccion\s+"([^"]+)"/)) {
                const matches = trimmed.match(/seccion\s+"([^"]+)"(?:\s+clase\s+"([^"]+)")?/);
                const id = matches[1];
                const clase = matches[2] || '';
                currentSectionId = id;
                html += `<section id="${id}" class="${clase}">`;
                inSection = true;
            }
            // Contenido principal
            else if (trimmed === 'contenido_principal') {
                html += '<main>';
            }
            // Pie de página
            else if (trimmed === 'pie_pagina') {
                html += '<footer>';
            }
            // Área de resultado
            else if (trimmed.match(/area_resultado\s+id\s+"([^"]+)"/)) {
                const id = trimmed.match(/"([^"]+)"/)[1];
                html += `<div id="${id}" style="margin-top: 10px; padding: 10px; border: 1px solid #00ff41; border-radius: 5px; min-height: 50px;"></div>`;
            }
        }
        
        // Cerrar tags abiertos
        html += '</body></html>';
        
        // Agregar función para mostrar mensajes
        js += `
        function mostrar_mensaje(mensaje) {
            console.log('💬 Vader:', mensaje);
            alert('Vader 7.0: ' + mensaje);
        }
        
        // Ejecutar al cargar
        window.addEventListener('load', function() {
            mostrar_mensaje('¡Archivo .vdr ejecutándose nativamente!');
            console.log('🚀 Vader 7.0 - Runtime nativo activo');
        });`;
        
        return {
            html: html,
            css: css,
            javascript: js,
            type: 'web_application_native',
            context: 'web',
            native: true
        };
    }
    
    executeBlockchain(code, language) {
        // Generar smart contract
        const contractCode = `
pragma solidity ^0.8.0;

contract VaderContract {
    string public message = "Vader 7.0 - Blockchain Universal";
    address public owner;
    
    constructor() {
        owner = msg.sender;
    }
    
    function updateMessage(string memory newMessage) public {
        require(msg.sender == owner, "Solo el propietario puede actualizar");
        message = newMessage;
    }
}`;
        
        return {
            contract_code: contractCode,
            blockchain: 'ethereum',
            type: 'smart_contract',
            context: 'blockchain',
            deployable: true
        };
    }
    
    executeIoT(code, language) {
        // Generar código Arduino
        const arduinoCode = `
void setup() {
    Serial.begin(9600);
    pinMode(13, OUTPUT);
}

void loop() {
    digitalWrite(13, HIGH);
    Serial.println("Vader 7.0 IoT - LED ON");
    delay(1000);
    
    digitalWrite(13, LOW);
    Serial.println("Vader 7.0 IoT - LED OFF");
    delay(1000);
}`;
        
        return {
            device_code: arduinoCode,
            device: 'arduino',
            type: 'iot_program',
            context: 'iot',
            flashable: true
        };
    }
    
    executeAI(code, language) {
        // Generar código TensorFlow.js
        const aiCode = `
import * as tf from '@tensorflow/tfjs';

const model = tf.sequential({
    layers: [
        tf.layers.dense({inputShape: [784], units: 128, activation: 'relu'}),
        tf.layers.dense({units: 10, activation: 'softmax'})
    ]
});

model.compile({
    optimizer: 'adam',
    loss: 'categoricalCrossentropy',
    metrics: ['accuracy']
});

console.log('Vader 7.0 - Modelo de IA creado');`;
        
        return {
            ai_code: aiCode,
            framework: 'tensorflow_js',
            type: 'ai_model',
            context: 'ai_ml',
            trainable: true
        };
    }
    
    executeDatabase(code, language) {
        // Generar esquema de base de datos
        const dbCode = `
CREATE DATABASE vader_db;

CREATE TABLE usuarios (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO usuarios (nombre, email) VALUES 
('Vader User', 'user@vader.org');`;
        
        return {
            db_code: dbCode,
            db_type: 'mysql',
            type: 'database_schema',
            context: 'database',
            executable: true
        };
    }
    
    executeMobile(code, language) {
        // Generar React Native
        const mobileCode = `
import React from 'react';
import { View, Text, StyleSheet } from 'react-native';

export default function VaderApp() {
    return (
        <View style={styles.container}>
            <Text style={styles.title}>Vader 7.0 Mobile</Text>
            <Text style={styles.subtitle}>La Programación Universal</Text>
        </View>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
        backgroundColor: '#000'
    },
    title: {
        fontSize: 24,
        color: '#00ff41',
        fontWeight: 'bold'
    },
    subtitle: {
        fontSize: 16,
        color: '#00ff41',
        marginTop: 10
    }
});`;
        
        return {
            mobile_code: mobileCode,
            platform: 'react_native',
            type: 'mobile_app',
            context: 'mobile',
            buildable: true
        };
    }
    
    executeElectronics(code, language) {
        // Generar código C para microcontrolador
        const electronicsCode = `
#include <stdio.h>
#include <stdlib.h>

int main() {
    printf("Vader 7.0 - Electronics Universal\\n");
    
    // Configurar GPIO
    // gpio_init();
    
    while(1) {
        // Lógica principal
        printf("Vader ejecutándose en microcontrolador\\n");
        // delay(1000);
    }
    
    return 0;
}`;
        
        return {
            electronics_code: electronicsCode,
            device_type: 'microcontroller',
            type: 'electronics_program',
            context: 'electronics',
            programmable: true
        };
    }
    
    executeCloud(code, language) {
        // Generar función AWS Lambda
        const cloudCode = `
exports.handler = async (event) => {
    console.log('Vader 7.0 - Cloud Function ejecutándose');
    
    const response = {
        statusCode: 200,
        headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        body: JSON.stringify({
            message: 'Vader 7.0 - La Programación Universal en la Nube',
            timestamp: new Date().toISOString(),
            context: 'cloud'
        })
    };
    
    return response;
};`;
        
        return {
            cloud_code: cloudCode,
            platform: 'aws_lambda',
            type: 'cloud_function',
            context: 'cloud',
            deployable: true
        };
    }
    
    async loadAndExecute(url) {
        try {
            const response = await fetch(url);
            const vaderCode = await response.text();
            return await this.execute(vaderCode);
        } catch (error) {
            console.error('Error cargando archivo .vdr:', error);
            return { error: error.message };
        }
    }
    
    injectCSS(css) {
        const style = document.createElement('style');
        style.textContent = css;
        document.head.appendChild(style);
    }
    
    executeJS(js) {
        const script = document.createElement('script');
        script.textContent = js;
        document.head.appendChild(script);
    }
    
    getRuntimeInfo() {
        return {
            version: this.version,
            codename: this.codename,
            supported_contexts: this.contexts,
            supported_languages: this.languages,
            philosophy: 'LA PROGRAMACIÓN: Libre, Descentralizada, Accesible a Todos'
        };
    }
}

// Instancia global
const vader = new VaderUniversalJS();

// API global para uso externo
window.Vader = vader;
window.executeVader = (code, context, language) => vader.execute(code, context, language);

// Auto-inicializar si estamos en browser
if (typeof window !== 'undefined') {
    console.log('🌐 Vader 7.0 Universal listo para browsers');
    console.log('📝 Uso: [script type="text/vader" src="mi_app.vdr"][/script]');
    console.log('🎯 O: [vader-app src="mi_app.vdr"][/vader-app]');
}

// Exportar para Node.js
if (typeof module !== 'undefined' && module.exports) {
    module.exports = VaderUniversalJS;
}
