/**
 * 📱 VADER MOBILE RUNTIME - PRIMERA IMPLEMENTACIÓN MUNDIAL
 * Runtime nativo de Vader para aplicaciones móviles iOS/Android
 * Permite ejecutar código .vdr directamente en dispositivos móviles
 */

class VaderMobileRuntime {
    constructor() {
        this.variables = new Map();
        this.functions = new Map();
        this.outputElement = null;
        this.isDebug = false;
        this.mobileFeatures = {
            camera: null,
            gps: null,
            accelerometer: null,
            notifications: null
        };
        
        this.initializeMobileFeatures();
        console.log("🚀 Vader Mobile Runtime inicializado");
    }
    
    // Inicializar características móviles
    initializeMobileFeatures() {
        // Detección de plataforma móvil
        this.platform = this.detectMobilePlatform();
        
        // Inicializar APIs móviles disponibles
        if (navigator.geolocation) {
            this.mobileFeatures.gps = navigator.geolocation;
        }
        
        if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
            this.mobileFeatures.camera = navigator.mediaDevices;
        }
        
        if ('DeviceMotionEvent' in window) {
            this.mobileFeatures.accelerometer = true;
        }
        
        if ('Notification' in window) {
            this.mobileFeatures.notifications = Notification;
        }
    }
    
    detectMobilePlatform() {
        const userAgent = navigator.userAgent || navigator.vendor || window.opera;
        
        if (/android/i.test(userAgent)) {
            return 'android';
        }
        
        if (/iPad|iPhone|iPod/.test(userAgent) && !window.MSStream) {
            return 'ios';
        }
        
        return 'web';
    }
    
    // Ejecutar código Vader móvil
    async executeCode(code) {
        const lines = code.split('\n');
        
        for (let line of lines) {
            line = line.trim();
            if (line && !line.startsWith('#')) {
                try {
                    await this.executeLine(line);
                } catch (error) {
                    this.output(`❌ Error: ${error.message}`);
                    if (this.isDebug) console.error(error);
                }
            }
        }
    }
    
    // Ejecutar línea individual
    async executeLine(line) {
        // Comandos móviles específicos
        if (line.startsWith('tomar foto')) {
            await this.takePhoto();
        }
        else if (line.startsWith('obtener ubicacion')) {
            await this.getLocation();
        }
        else if (line.startsWith('vibrar')) {
            this.vibrate(line);
        }
        else if (line.startsWith('notificar')) {
            this.showNotification(line);
        }
        else if (line.startsWith('detectar movimiento')) {
            this.detectMotion();
        }
        else if (line.startsWith('reproducir sonido')) {
            this.playSound(line);
        }
        else if (line.startsWith('abrir app')) {
            this.openApp(line);
        }
        else if (line.startsWith('compartir')) {
            this.shareContent(line);
        }
        // Comandos básicos de Vader
        else if (line.startsWith('mostrar')) {
            this.output(this.extractString(line, 'mostrar'));
        }
        else if (line.includes(' = ')) {
            this.handleAssignment(line);
        }
        else if (line.startsWith('crear boton')) {
            this.createMobileButton(line);
        }
        else {
            // Evaluar expresiones
            const result = this.evaluateExpression(line);
            if (result !== undefined) {
                this.output(result);
            }
        }
    }
    
    // 📷 Tomar foto con la cámara
    async takePhoto() {
        if (!this.mobileFeatures.camera) {
            this.output("❌ Cámara no disponible");
            return;
        }
        
        try {
            const stream = await this.mobileFeatures.camera.getUserMedia({ 
                video: { facingMode: 'environment' } 
            });
            
            // Crear elemento de video temporal
            const video = document.createElement('video');
            video.srcObject = stream;
            video.play();
            
            // Crear canvas para captura
            const canvas = document.createElement('canvas');
            const context = canvas.getContext('2d');
            
            video.addEventListener('loadedmetadata', () => {
                canvas.width = video.videoWidth;
                canvas.height = video.videoHeight;
                context.drawImage(video, 0, 0);
                
                // Convertir a imagen
                const imageData = canvas.toDataURL('image/jpeg');
                this.variables.set('ultima_foto', imageData);
                
                // Detener stream
                stream.getTracks().forEach(track => track.stop());
                
                this.output("📷 Foto tomada y guardada en 'ultima_foto'");
            });
            
        } catch (error) {
            this.output("❌ Error al acceder a la cámara: " + error.message);
        }
    }
    
    // 📍 Obtener ubicación GPS
    async getLocation() {
        if (!this.mobileFeatures.gps) {
            this.output("❌ GPS no disponible");
            return;
        }
        
        return new Promise((resolve) => {
            this.mobileFeatures.gps.getCurrentPosition(
                (position) => {
                    const lat = position.coords.latitude;
                    const lng = position.coords.longitude;
                    
                    this.variables.set('latitud', lat);
                    this.variables.set('longitud', lng);
                    
                    this.output(`📍 Ubicación: ${lat.toFixed(6)}, ${lng.toFixed(6)}`);
                    resolve();
                },
                (error) => {
                    this.output("❌ Error al obtener ubicación: " + error.message);
                    resolve();
                }
            );
        });
    }
    
    // 📳 Vibrar dispositivo
    vibrate(line) {
        const match = line.match(/vibrar (\d+)/);
        const duration = match ? parseInt(match[1]) : 200;
        
        if (navigator.vibrate) {
            navigator.vibrate(duration);
            this.output(`📳 Vibrando por ${duration}ms`);
        } else {
            this.output("❌ Vibración no soportada");
        }
    }
    
    // 🔔 Mostrar notificación
    async showNotification(line) {
        const message = this.extractString(line, 'notificar');
        
        if (!this.mobileFeatures.notifications) {
            this.output("❌ Notificaciones no soportadas");
            return;
        }
        
        if (Notification.permission === 'granted') {
            new Notification('Vader App', { body: message });
            this.output(`🔔 Notificación enviada: ${message}`);
        } else if (Notification.permission !== 'denied') {
            const permission = await Notification.requestPermission();
            if (permission === 'granted') {
                new Notification('Vader App', { body: message });
                this.output(`🔔 Notificación enviada: ${message}`);
            }
        }
    }
    
    // 📱 Detectar movimiento del dispositivo
    detectMotion() {
        if (!this.mobileFeatures.accelerometer) {
            this.output("❌ Acelerómetro no disponible");
            return;
        }
        
        window.addEventListener('devicemotion', (event) => {
            const x = event.accelerationIncludingGravity.x;
            const y = event.accelerationIncludingGravity.y;
            const z = event.accelerationIncludingGravity.z;
            
            this.variables.set('aceleracion_x', x);
            this.variables.set('aceleracion_y', y);
            this.variables.set('aceleracion_z', z);
            
            // Detectar sacudida
            const totalAcceleration = Math.sqrt(x*x + y*y + z*z);
            if (totalAcceleration > 15) {
                this.output("📱 ¡Dispositivo sacudido!");
            }
        });
        
        this.output("📱 Detección de movimiento activada");
    }
    
    // 🔊 Reproducir sonido
    playSound(line) {
        const match = line.match(/reproducir sonido "([^"]+)"/);
        if (match) {
            const soundUrl = match[1];
            const audio = new Audio(soundUrl);
            audio.play().catch(error => {
                this.output("❌ Error al reproducir sonido: " + error.message);
            });
            this.output(`🔊 Reproduciendo: ${soundUrl}`);
        }
    }
    
    // 📱 Abrir otra aplicación
    openApp(line) {
        const match = line.match(/abrir app "([^"]+)"/);
        if (match) {
            const appUrl = match[1];
            window.open(appUrl, '_system');
            this.output(`📱 Abriendo app: ${appUrl}`);
        }
    }
    
    // 📤 Compartir contenido
    shareContent(line) {
        const content = this.extractString(line, 'compartir');
        
        if (navigator.share) {
            navigator.share({
                title: 'Compartido desde Vader',
                text: content
            }).then(() => {
                this.output(`📤 Contenido compartido: ${content}`);
            }).catch(error => {
                this.output("❌ Error al compartir: " + error.message);
            });
        } else {
            // Fallback para navegadores sin Web Share API
            if (navigator.clipboard) {
                navigator.clipboard.writeText(content);
                this.output(`📋 Copiado al portapapeles: ${content}`);
            } else {
                this.output("❌ Compartir no soportado");
            }
        }
    }
    
    // Crear botón móvil optimizado
    createMobileButton(line) {
        const match = line.match(/crear boton "([^"]+)" al hacer click (.+)/);
        if (match) {
            const buttonText = match[1];
            const action = match[2];
            
            const button = document.createElement('button');
            button.textContent = buttonText;
            button.className = 'vader-mobile-button';
            
            // Estilos móviles optimizados
            button.style.cssText = `
                background: linear-gradient(135deg, #FFD700, #FFA500);
                color: #000;
                border: none;
                padding: 15px 25px;
                font-size: 18px;
                font-weight: bold;
                border-radius: 25px;
                margin: 10px;
                min-height: 50px;
                min-width: 120px;
                box-shadow: 0 4px 15px rgba(255, 215, 0, 0.3);
                cursor: pointer;
                transition: all 0.3s ease;
                touch-action: manipulation;
            `;
            
            // Efectos táctiles
            button.addEventListener('touchstart', () => {
                button.style.transform = 'scale(0.95)';
            });
            
            button.addEventListener('touchend', () => {
                button.style.transform = 'scale(1)';
            });
            
            button.addEventListener('click', async () => {
                await this.executeLine(action);
            });
            
            if (this.outputElement) {
                this.outputElement.appendChild(button);
            }
        }
    }
    
    // Funciones auxiliares
    extractString(line, command) {
        const regex = new RegExp(`${command}\\s+"([^"]+)"`);
        const match = line.match(regex);
        return match ? match[1] : line.replace(command, '').trim();
    }
    
    handleAssignment(line) {
        const [variable, value] = line.split(' = ').map(s => s.trim());
        const evaluatedValue = this.evaluateExpression(value);
        this.variables.set(variable, evaluatedValue);
        
        if (this.isDebug) {
            this.output(`📝 ${variable} = ${evaluatedValue}`);
        }
    }
    
    evaluateExpression(expr) {
        // Reemplazar variables
        for (let [key, value] of this.variables) {
            expr = expr.replace(new RegExp(`\\b${key}\\b`, 'g'), value);
        }
        
        // Evaluar expresión simple
        try {
            return Function(`"use strict"; return (${expr})`)();
        } catch {
            return expr;
        }
    }
    
    output(message) {
        console.log(`📱 Vader Mobile: ${message}`);
        
        if (this.outputElement) {
            const div = document.createElement('div');
            div.textContent = message;
            div.style.cssText = `
                margin: 5px 0;
                padding: 10px;
                background: rgba(255, 215, 0, 0.1);
                border-left: 3px solid #FFD700;
                border-radius: 5px;
                font-family: 'Courier New', monospace;
            `;
            this.outputElement.appendChild(div);
            this.outputElement.scrollTop = this.outputElement.scrollHeight;
        }
    }
    
    setOutputElement(element) {
        this.outputElement = element;
    }
    
    setDebugMode(enabled) {
        this.isDebug = enabled;
    }
}

// Inicialización automática para PWA
if (typeof window !== 'undefined') {
    window.VaderMobileRuntime = VaderMobileRuntime;
    
    // Detectar si es PWA o app móvil
    if (window.matchMedia('(display-mode: standalone)').matches) {
        console.log('🚀 Vader ejecutándose como PWA');
    }
}

// Export para Node.js
if (typeof module !== 'undefined' && module.exports) {
    module.exports = VaderMobileRuntime;
}
