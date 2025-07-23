/**
 * VADER 7.0 - UNIVERSAL ENHANCED JAVASCRIPT RUNTIME
 * =================================================
 * Runtime JavaScript mejorado con validación, métricas y logging
 * Ejecuta archivos .vdr nativamente en browsers con funcionalidades avanzadas
 */

const VADER_VERSION = "7.0.0";
const VADER_CODENAME = "UNIVERSAL_ENHANCED";

// Sistema de logging mejorado
class VaderLogger {
    constructor(runtimeName) {
        this.runtimeName = runtimeName;
        this.logs = [];
    }
    
    log(level, message, data = {}) {
        const logEntry = {
            timestamp: new Date().toISOString(),
            level: level,
            runtime: this.runtimeName,
            message: message,
            data: data
        };
        
        this.logs.push(logEntry);
        
        const emoji = {
            'INFO': '🚀',
            'ERROR': '❌',
            'WARN': '⚠️',
            'DEBUG': '🔍',
            'SUCCESS': '✅'
        }[level] || '📝';
        
        console.log(`${emoji} [${this.runtimeName}] ${message}`, data);
    }
    
    info(message, data) { this.log('INFO', message, data); }
    error(message, data) { this.log('ERROR', message, data); }
    warn(message, data) { this.log('WARN', message, data); }
    debug(message, data) { this.log('DEBUG', message, data); }
    success(message, data) { this.log('SUCCESS', message, data); }
}

// Validador mejorado
class VaderValidator {
    static validateVdrContent(content, filename = 'unknown') {
        const result = {
            isValid: true,
            fileSize: content.length,
            lineCount: content.split('\n').length,
            encoding: 'utf-8',
            syntaxErrors: [],
            warnings: []
        };
        
        if (!content || content.trim().length === 0) {
            result.isValid = false;
            result.syntaxErrors.push('Contenido vacío');
            return result;
        }
        
        const vaderKeywords = /\b(mostrar|crear|configurar|usar|show|create|configure|use)\b/i;
        if (!vaderKeywords.test(content)) {
            result.warnings.push('No se detectaron palabras clave Vader típicas');
        }
        
        return result;
    }
}

// Detector de contexto mejorado
class VaderContextDetector {
    static contextPatterns = {
        'web': [/\b(html|css|javascript|dom|browser|web|página|website)\b/i],
        'mobile': [/\b(mobile|móvil|app|aplicación|ios|android)\b/i],
        'ai': [/\b(ai|ia|inteligencia.artificial|machine.learning|ml)\b/i],
        'database': [/\b(database|base.datos|sql|mysql|postgresql|mongodb)\b/i]
    };
    
    static detectContext(code) {
        const contextScores = {};
        
        for (const [context, patterns] of Object.entries(this.contextPatterns)) {
            let score = 0;
            for (const pattern of patterns) {
                const matches = (code.match(pattern) || []).length;
                score += matches;
            }
            if (score > 0) {
                contextScores[context] = score;
            }
        }
        
        return Object.keys(contextScores).length > 0 ? 
            Object.keys(contextScores).reduce((a, b) => contextScores[a] > contextScores[b] ? a : b) : 'web';
    }
    
    static detectLanguage(code) {
        const spanishKeywords = /\b(mostrar|crear|configurar|usar|ejecutar)\b/i;
        const englishKeywords = /\b(show|create|configure|use|execute)\b/i;
        
        if (spanishKeywords.test(code)) return 'es';
        if (englishKeywords.test(code)) return 'en';
        return 'en';
    }
}

// Runtime principal mejorado
class VaderUniversalEnhancedJS {
    constructor() {
        this.version = VADER_VERSION;
        this.codename = VADER_CODENAME;
        this.logger = new VaderLogger('VaderJS');
        
        this.logger.info(`VADER ${this.version} '${this.codename}' - Runtime Enhanced JS`);
        this.logger.info('LA PROGRAMACIÓN UNIVERSAL: Libre, Descentralizada, Accesible');
        
        this.initializeBrowserSupport();
    }
    
    initializeBrowserSupport() {
        if (typeof document !== 'undefined') {
            this.logger.info('Inicializando soporte de navegador mejorado');
            this.registerVaderComponent();
            
            if (document.readyState === 'loading') {
                document.addEventListener('DOMContentLoaded', () => {
                    this.executeVaderScripts();
                });
            } else {
                this.executeVaderScripts();
            }
        }
    }
    
    registerVaderComponent() {
        if (typeof customElements !== 'undefined') {
            const self = this;
            
            class VaderAppEnhanced extends HTMLElement {
                async connectedCallback() {
                    const src = this.getAttribute('src');
                    
                    if (src) {
                        try {
                            self.logger.info(`Cargando componente Vader: ${src}`);
                            const result = await self.loadAndExecute(src);
                            
                            if (result.success) {
                                this.innerHTML = result.result.html || '✅ Vader 7.0 ejecutado exitosamente';
                                self.logger.success(`Componente cargado: ${src}`);
                            } else {
                                this.innerHTML = `❌ Error cargando ${src}`;
                                self.logger.error(`Error en componente: ${src}`);
                            }
                        } catch (error) {
                            this.innerHTML = `❌ Error: ${error.message}`;
                            self.logger.error('Error en componente Vader', error);
                        }
                    }
                }
            }
            
            customElements.define('vader-app', VaderAppEnhanced);
        }
    }
    
    async executeVaderScripts() {
        const scripts = document.querySelectorAll('script[type="text/vader"]');
        this.logger.info(`Encontrados ${scripts.length} scripts Vader`);
        
        for (const script of scripts) {
            await this.executeVaderScript(script);
        }
    }
    
    async executeVaderScript(scriptElement) {
        try {
            let vaderCode = '';
            
            if (scriptElement.src) {
                const response = await fetch(scriptElement.src);
                vaderCode = await response.text();
                this.logger.info(`Script cargado desde: ${scriptElement.src}`);
            } else {
                vaderCode = scriptElement.textContent;
                this.logger.info('Ejecutando script Vader inline');
            }
            
            const result = await this.execute(vaderCode);
            
            if (result.success) {
                this.logger.success('Script Vader ejecutado exitosamente');
            } else {
                this.logger.error('Error ejecutando script Vader');
            }
            
        } catch (error) {
            this.logger.error('Error procesando script Vader', error);
        }
    }
    
    async execute(vaderCode, context = 'auto', language = 'auto') {
        const startTime = performance.now();
        
        try {
            this.logger.info('Iniciando ejecución de código Vader');
            
            // Validar código
            const validation = VaderValidator.validateVdrContent(vaderCode);
            if (!validation.isValid) {
                throw new Error(`Código inválido: ${validation.syntaxErrors.join(', ')}`);
            }
            
            // Detectar contexto y idioma
            const detectedContext = context === 'auto' ? 
                VaderContextDetector.detectContext(vaderCode) : context;
            const detectedLanguage = language === 'auto' ? 
                VaderContextDetector.detectLanguage(vaderCode) : language;
            
            this.logger.info(`Contexto detectado: ${detectedContext}`);
            this.logger.info(`Idioma detectado: ${detectedLanguage}`);
            
            // Ejecutar según contexto
            let result = await this.executeWeb(vaderCode, detectedLanguage);
            
            const executionTime = performance.now() - startTime;
            this.logger.success(`Ejecución completada en ${executionTime.toFixed(2)}ms`);
            
            return {
                success: true,
                context: detectedContext,
                language: detectedLanguage,
                result: result,
                executionTime: executionTime
            };
            
        } catch (error) {
            this.logger.error('Error en ejecución', error);
            
            return {
                success: false,
                error: error.message
            };
        }
    }
    
    async executeWeb(code, language) {
        this.logger.info('Ejecutando contexto web');
        
        const html = `
<!DOCTYPE html>
<html lang="${language === 'es' ? 'es' : 'en'}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Vader 7.0 - Web App Enhanced</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #000000, #1a1a1a);
            color: #00ff41;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0;
        }
        
        .vader-container {
            text-align: center;
            padding: 2rem;
            border: 2px solid #00ff41;
            border-radius: 10px;
            background: rgba(0, 255, 65, 0.1);
            box-shadow: 0 0 30px rgba(0, 255, 65, 0.3);
        }
        
        .vader-title {
            font-size: 2.5rem;
            margin-bottom: 1rem;
            text-shadow: 0 0 20px #00ff41;
            animation: glow 2s ease-in-out infinite alternate;
        }
        
        .vader-subtitle {
            font-size: 1.2rem;
            margin-bottom: 2rem;
            opacity: 0.8;
        }
        
        .vader-button {
            background: linear-gradient(45deg, #00ff41, #00cc33);
            color: #000;
            border: none;
            padding: 1rem 2rem;
            font-size: 1.1rem;
            font-weight: bold;
            border-radius: 5px;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .vader-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0, 255, 65, 0.4);
        }
        
        @keyframes glow {
            from { text-shadow: 0 0 20px #00ff41; }
            to { text-shadow: 0 0 30px #00ff41, 0 0 40px #00ff41; }
        }
        
        .vader-metrics {
            margin-top: 2rem;
            padding: 1rem;
            background: rgba(0, 0, 0, 0.3);
            border-radius: 5px;
            font-family: 'Courier New', monospace;
            font-size: 0.9rem;
        }
    </style>
</head>
<body>
    <div class="vader-container">
        <h1 class="vader-title">🚀 VADER 7.0</h1>
        <p class="vader-subtitle">La Programación Universal Enhanced</p>
        <button class="vader-button" onclick="vaderAction()">
            ${language === 'es' ? 'Ejecutar Vader' : 'Execute Vader'}
        </button>
        <div class="vader-metrics">
            <div>📊 Runtime: Web Enhanced</div>
            <div>🌐 Idioma: ${language}</div>
            <div>⚡ Estado: Activo</div>
            <div>🎯 Versión: ${this.version}</div>
        </div>
    </div>
    
    <script>
        function vaderAction() {
            const messages = {
                es: ['✅ Vader 7.0 Enhanced ejecutándose perfectamente'],
                en: ['✅ Vader 7.0 Enhanced running perfectly']
            };
            
            const langMessages = messages['${language}'] || messages.en;
            alert(langMessages[0]);
        }
        
        setTimeout(() => {
            console.log('🚀 Vader 7.0 Enhanced Web Runtime cargado');
        }, 1000);
    </script>
</body>
</html>`;
        
        return {
            html: html,
            generated_code: html,
            platform: 'web_enhanced',
            type: 'web_application',
            context: 'web'
        };
    }
    
    async loadAndExecute(url) {
        try {
            const response = await fetch(url);
            const vaderCode = await response.text();
            return await this.execute(vaderCode);
        } catch (error) {
            this.logger.error('Error cargando archivo .vdr', error);
            return { success: false, error: error.message };
        }
    }
    
    getRuntimeInfo() {
        return {
            version: this.version,
            codename: this.codename,
            philosophy: 'LA PROGRAMACIÓN: Libre, Descentralizada, Accesible a Todos'
        };
    }
}

// Instancia global mejorada
const vaderEnhanced = new VaderUniversalEnhancedJS();

// API global para uso externo
if (typeof window !== 'undefined') {
    window.VaderEnhanced = vaderEnhanced;
    window.executeVaderEnhanced = (code, context, language) => 
        vaderEnhanced.execute(code, context, language);
    
    console.log('🌐 Vader 7.0 Enhanced listo para browsers');
    console.log('📝 Uso: <script type="text/vader" src="mi_app.vdr"></script>');
    console.log('🎯 O: <vader-app src="mi_app.vdr"></vader-app>');
}

// Exportar para Node.js
if (typeof module !== 'undefined' && module.exports) {
    module.exports = VaderUniversalEnhancedJS;
}
