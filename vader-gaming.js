/**
 * 🎮 VADER GAMING RUNTIME - PRIMERA IMPLEMENTACIÓN MUNDIAL
 * Runtime especializado de Vader para desarrollo de juegos
 * Soporta sprites, animaciones, física, sonido y controles
 */

class VaderGamingRuntime {
    constructor(canvasId) {
        this.canvas = document.getElementById(canvasId);
        this.ctx = this.canvas.getContext('2d');
        this.variables = new Map();
        this.functions = new Map();
        this.gameObjects = new Map();
        this.animations = new Map();
        this.sounds = new Map();
        this.keys = new Set();
        this.mouse = { x: 0, y: 0, clicked: false };
        this.gameLoop = null;
        this.fps = 60;
        this.isRunning = false;
        this.score = 0;
        this.level = 1;
        
        this.initializeCanvas();
        this.setupEventListeners();
        
        console.log("🎮 Vader Gaming Runtime inicializado");
    }
    
    initializeCanvas() {
        // Configurar canvas para juegos
        this.canvas.width = 800;
        this.canvas.height = 600;
        this.canvas.style.border = '2px solid #FFD700';
        this.canvas.style.background = '#000011';
        this.canvas.style.display = 'block';
        this.canvas.style.margin = '0 auto';
        
        // Configurar contexto
        this.ctx.imageSmoothingEnabled = false; // Pixel art
        this.ctx.textAlign = 'left';
        this.ctx.textBaseline = 'top';
    }
    
    setupEventListeners() {
        // Controles de teclado
        document.addEventListener('keydown', (e) => {
            this.keys.add(e.code);
            e.preventDefault();
        });
        
        document.addEventListener('keyup', (e) => {
            this.keys.delete(e.code);
            e.preventDefault();
        });
        
        // Controles de mouse
        this.canvas.addEventListener('mousemove', (e) => {
            const rect = this.canvas.getBoundingClientRect();
            this.mouse.x = e.clientX - rect.left;
            this.mouse.y = e.clientY - rect.top;
        });
        
        this.canvas.addEventListener('mousedown', (e) => {
            this.mouse.clicked = true;
            e.preventDefault();
        });
        
        this.canvas.addEventListener('mouseup', (e) => {
            this.mouse.clicked = false;
            e.preventDefault();
        });
    }
    
    // Ejecutar código Vader gaming
    async executeCode(code) {
        const lines = code.split('\n');
        
        for (let line of lines) {
            line = line.trim();
            if (line && !line.startsWith('#')) {
                try {
                    await this.executeLine(line);
                } catch (error) {
                    console.error(`❌ Error: ${error.message}`);
                }
            }
        }
    }
    
    // Ejecutar línea individual
    async executeLine(line) {
        // Comandos de juego específicos
        if (line.startsWith('crear sprite')) {
            this.createSprite(line);
        }
        else if (line.startsWith('mover sprite')) {
            this.moveSprite(line);
        }
        else if (line.startsWith('animar sprite')) {
            this.animateSprite(line);
        }
        else if (line.startsWith('detectar colision')) {
            this.detectCollision(line);
        }
        else if (line.startsWith('reproducir sonido')) {
            this.playGameSound(line);
        }
        else if (line.startsWith('dibujar texto')) {
            this.drawText(line);
        }
        else if (line.startsWith('dibujar rectangulo')) {
            this.drawRectangle(line);
        }
        else if (line.startsWith('dibujar circulo')) {
            this.drawCircle(line);
        }
        else if (line.startsWith('limpiar pantalla')) {
            this.clearScreen();
        }
        else if (line.startsWith('iniciar juego')) {
            this.startGame();
        }
        else if (line.startsWith('pausar juego')) {
            this.pauseGame();
        }
        else if (line.startsWith('terminar juego')) {
            this.endGame();
        }
        else if (line.startsWith('si tecla')) {
            this.handleKeyInput(line);
        }
        else if (line.startsWith('si mouse')) {
            this.handleMouseInput(line);
        }
        else if (line.startsWith('aumentar puntaje')) {
            this.increaseScore(line);
        }
        else if (line.startsWith('cambiar nivel')) {
            this.changeLevel(line);
        }
        // Comandos básicos de Vader
        else if (line.startsWith('mostrar')) {
            console.log(this.extractString(line, 'mostrar'));
        }
        else if (line.includes(' = ')) {
            this.handleAssignment(line);
        }
    }
    
    // 🎨 Crear sprite
    createSprite(line) {
        // crear sprite "jugador" en x=100 y=200 ancho=50 alto=50 color="azul"
        const match = line.match(/crear sprite "([^"]+)" en x=(\d+) y=(\d+) ancho=(\d+) alto=(\d+) color="([^"]+)"/);
        
        if (match) {
            const [, name, x, y, width, height, color] = match;
            
            const sprite = {
                name: name,
                x: parseInt(x),
                y: parseInt(y),
                width: parseInt(width),
                height: parseInt(height),
                color: this.getColor(color),
                velocityX: 0,
                velocityY: 0,
                visible: true,
                rotation: 0,
                scale: 1,
                health: 100,
                type: 'sprite'
            };
            
            this.gameObjects.set(name, sprite);
            console.log(`🎨 Sprite creado: ${name}`);
        }
    }
    
    // 🏃 Mover sprite
    moveSprite(line) {
        // mover sprite "jugador" x=10 y=5
        const match = line.match(/mover sprite "([^"]+)" x=(-?\d+) y=(-?\d+)/);
        
        if (match) {
            const [, name, deltaX, deltaY] = match;
            const sprite = this.gameObjects.get(name);
            
            if (sprite) {
                sprite.x += parseInt(deltaX);
                sprite.y += parseInt(deltaY);
                
                // Mantener dentro del canvas
                sprite.x = Math.max(0, Math.min(this.canvas.width - sprite.width, sprite.x));
                sprite.y = Math.max(0, Math.min(this.canvas.height - sprite.height, sprite.y));
            }
        }
    }
    
    // 🎭 Animar sprite
    animateSprite(line) {
        // animar sprite "jugador" rotacion=45 escala=1.5 duracion=1000
        const match = line.match(/animar sprite "([^"]+)" rotacion=(\d+) escala=([\d.]+) duracion=(\d+)/);
        
        if (match) {
            const [, name, rotation, scale, duration] = match;
            const sprite = this.gameObjects.get(name);
            
            if (sprite) {
                const startRotation = sprite.rotation;
                const startScale = sprite.scale;
                const targetRotation = parseInt(rotation);
                const targetScale = parseFloat(scale);
                const animDuration = parseInt(duration);
                
                const startTime = Date.now();
                
                const animate = () => {
                    const elapsed = Date.now() - startTime;
                    const progress = Math.min(elapsed / animDuration, 1);
                    
                    sprite.rotation = startRotation + (targetRotation - startRotation) * progress;
                    sprite.scale = startScale + (targetScale - startScale) * progress;
                    
                    if (progress < 1) {
                        requestAnimationFrame(animate);
                    }
                };
                
                animate();
            }
        }
    }
    
    // 💥 Detectar colisión
    detectCollision(line) {
        // detectar colision entre "jugador" y "enemigo"
        const match = line.match(/detectar colision entre "([^"]+)" y "([^"]+)"/);
        
        if (match) {
            const [, sprite1Name, sprite2Name] = match;
            const sprite1 = this.gameObjects.get(sprite1Name);
            const sprite2 = this.gameObjects.get(sprite2Name);
            
            if (sprite1 && sprite2) {
                const collision = this.checkCollision(sprite1, sprite2);
                this.variables.set('colision_detectada', collision);
                
                if (collision) {
                    console.log(`💥 Colisión detectada: ${sprite1Name} ↔ ${sprite2Name}`);
                    return true;
                }
            }
        }
        return false;
    }
    
    checkCollision(sprite1, sprite2) {
        return sprite1.x < sprite2.x + sprite2.width &&
               sprite1.x + sprite1.width > sprite2.x &&
               sprite1.y < sprite2.y + sprite2.height &&
               sprite1.y + sprite1.height > sprite2.y;
    }
    
    // 🔊 Reproducir sonido de juego
    playGameSound(line) {
        const soundName = this.extractString(line, 'reproducir sonido');
        
        // Sonidos predefinidos del juego
        const gameSounds = {
            'salto': this.generateTone(440, 0.2),
            'explosion': this.generateNoise(0.3),
            'moneda': this.generateTone(880, 0.1),
            'game_over': this.generateTone(220, 1.0)
        };
        
        if (gameSounds[soundName]) {
            gameSounds[soundName].play();
            console.log(`🔊 Sonido reproducido: ${soundName}`);
        }
    }
    
    generateTone(frequency, duration) {
        const audioContext = new (window.AudioContext || window.webkitAudioContext)();
        const oscillator = audioContext.createOscillator();
        const gainNode = audioContext.createGain();
        
        oscillator.connect(gainNode);
        gainNode.connect(audioContext.destination);
        
        oscillator.frequency.value = frequency;
        oscillator.type = 'square';
        
        gainNode.gain.setValueAtTime(0.3, audioContext.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + duration);
        
        return {
            play: () => {
                oscillator.start(audioContext.currentTime);
                oscillator.stop(audioContext.currentTime + duration);
            }
        };
    }
    
    generateNoise(duration) {
        const audioContext = new (window.AudioContext || window.webkitAudioContext)();
        const bufferSize = audioContext.sampleRate * duration;
        const buffer = audioContext.createBuffer(1, bufferSize, audioContext.sampleRate);
        const data = buffer.getChannelData(0);
        
        for (let i = 0; i < bufferSize; i++) {
            data[i] = Math.random() * 2 - 1;
        }
        
        return {
            play: () => {
                const source = audioContext.createBufferSource();
                source.buffer = buffer;
                source.connect(audioContext.destination);
                source.start();
            }
        };
    }
    
    // 📝 Dibujar texto
    drawText(line) {
        // dibujar texto "SCORE: 100" en x=10 y=10 tamaño=20 color="blanco"
        const match = line.match(/dibujar texto "([^"]+)" en x=(\d+) y=(\d+) tamaño=(\d+) color="([^"]+)"/);
        
        if (match) {
            const [, text, x, y, size, color] = match;
            
            this.ctx.font = `${size}px 'Courier New', monospace`;
            this.ctx.fillStyle = this.getColor(color);
            this.ctx.fillText(text, parseInt(x), parseInt(y));
        }
    }
    
    // 🟦 Dibujar rectángulo
    drawRectangle(line) {
        // dibujar rectangulo en x=100 y=100 ancho=50 alto=30 color="rojo"
        const match = line.match(/dibujar rectangulo en x=(\d+) y=(\d+) ancho=(\d+) alto=(\d+) color="([^"]+)"/);
        
        if (match) {
            const [, x, y, width, height, color] = match;
            
            this.ctx.fillStyle = this.getColor(color);
            this.ctx.fillRect(parseInt(x), parseInt(y), parseInt(width), parseInt(height));
        }
    }
    
    // ⭕ Dibujar círculo
    drawCircle(line) {
        // dibujar circulo en x=200 y=200 radio=25 color="verde"
        const match = line.match(/dibujar circulo en x=(\d+) y=(\d+) radio=(\d+) color="([^"]+)"/);
        
        if (match) {
            const [, x, y, radius, color] = match;
            
            this.ctx.beginPath();
            this.ctx.arc(parseInt(x), parseInt(y), parseInt(radius), 0, 2 * Math.PI);
            this.ctx.fillStyle = this.getColor(color);
            this.ctx.fill();
        }
    }
    
    // 🧹 Limpiar pantalla
    clearScreen() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        
        // Fondo estrellado opcional
        this.ctx.fillStyle = '#000011';
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
    }
    
    // ⌨️ Manejar entrada de teclado
    handleKeyInput(line) {
        // si tecla "ArrowUp" presionada entonces mover sprite "jugador" x=0 y=-5
        const match = line.match(/si tecla "([^"]+)" presionada entonces (.+)/);
        
        if (match) {
            const [, key, action] = match;
            
            if (this.keys.has(key)) {
                this.executeLine(action);
            }
        }
    }
    
    // 🖱️ Manejar entrada de mouse
    handleMouseInput(line) {
        // si mouse clickeado entonces crear sprite "bala" en x=mouse_x y=mouse_y
        const match = line.match(/si mouse clickeado entonces (.+)/);
        
        if (match) {
            const [, action] = match;
            
            if (this.mouse.clicked) {
                // Reemplazar coordenadas del mouse
                const actionWithMouse = action
                    .replace('mouse_x', this.mouse.x)
                    .replace('mouse_y', this.mouse.y);
                
                this.executeLine(actionWithMouse);
                this.mouse.clicked = false; // Evitar repetición
            }
        }
    }
    
    // 🎯 Aumentar puntaje
    increaseScore(line) {
        const match = line.match(/aumentar puntaje (\d+)/);
        const points = match ? parseInt(match[1]) : 10;
        
        this.score += points;
        this.variables.set('puntaje', this.score);
        console.log(`🎯 Puntaje: ${this.score} (+${points})`);
    }
    
    // 🆙 Cambiar nivel
    changeLevel(line) {
        const match = line.match(/cambiar nivel (\d+)/);
        if (match) {
            this.level = parseInt(match[1]);
            this.variables.set('nivel', this.level);
            console.log(`🆙 Nivel: ${this.level}`);
        }
    }
    
    // 🎮 Iniciar juego
    startGame() {
        if (this.isRunning) return;
        
        this.isRunning = true;
        console.log("🎮 Juego iniciado");
        
        this.gameLoop = setInterval(() => {
            this.update();
            this.render();
        }, 1000 / this.fps);
    }
    
    // ⏸️ Pausar juego
    pauseGame() {
        if (this.gameLoop) {
            clearInterval(this.gameLoop);
            this.gameLoop = null;
            this.isRunning = false;
            console.log("⏸️ Juego pausado");
        }
    }
    
    // 🏁 Terminar juego
    endGame() {
        this.pauseGame();
        
        // Mostrar pantalla de game over
        this.ctx.fillStyle = 'rgba(0, 0, 0, 0.8)';
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
        
        this.ctx.font = '48px Courier New';
        this.ctx.fillStyle = '#FFD700';
        this.ctx.textAlign = 'center';
        this.ctx.fillText('GAME OVER', this.canvas.width / 2, this.canvas.height / 2 - 50);
        
        this.ctx.font = '24px Courier New';
        this.ctx.fillText(`Puntaje Final: ${this.score}`, this.canvas.width / 2, this.canvas.height / 2 + 20);
        this.ctx.fillText(`Nivel Alcanzado: ${this.level}`, this.canvas.width / 2, this.canvas.height / 2 + 60);
        
        console.log("🏁 Juego terminado");
    }
    
    // 🔄 Actualizar lógica del juego
    update() {
        // Actualizar posiciones de sprites con velocidad
        for (let [name, obj] of this.gameObjects) {
            if (obj.type === 'sprite') {
                obj.x += obj.velocityX;
                obj.y += obj.velocityY;
                
                // Mantener dentro del canvas
                obj.x = Math.max(0, Math.min(this.canvas.width - obj.width, obj.x));
                obj.y = Math.max(0, Math.min(this.canvas.height - obj.height, obj.y));
            }
        }
    }
    
    // 🎨 Renderizar juego
    render() {
        this.clearScreen();
        
        // Renderizar todos los sprites
        for (let [name, obj] of this.gameObjects) {
            if (obj.visible && obj.type === 'sprite') {
                this.ctx.save();
                
                // Aplicar transformaciones
                this.ctx.translate(obj.x + obj.width / 2, obj.y + obj.height / 2);
                this.ctx.rotate(obj.rotation * Math.PI / 180);
                this.ctx.scale(obj.scale, obj.scale);
                
                // Dibujar sprite
                this.ctx.fillStyle = obj.color;
                this.ctx.fillRect(-obj.width / 2, -obj.height / 2, obj.width, obj.height);
                
                this.ctx.restore();
            }
        }
        
        // Renderizar UI
        this.renderUI();
    }
    
    // 🖥️ Renderizar interfaz de usuario
    renderUI() {
        this.ctx.font = '20px Courier New';
        this.ctx.fillStyle = '#FFD700';
        this.ctx.textAlign = 'left';
        this.ctx.fillText(`Puntaje: ${this.score}`, 10, 30);
        this.ctx.fillText(`Nivel: ${this.level}`, 10, 60);
        this.ctx.fillText(`FPS: ${this.fps}`, 10, 90);
    }
    
    // Funciones auxiliares
    getColor(colorName) {
        const colors = {
            'rojo': '#FF0000',
            'verde': '#00FF00',
            'azul': '#0000FF',
            'amarillo': '#FFFF00',
            'blanco': '#FFFFFF',
            'negro': '#000000',
            'dorado': '#FFD700',
            'naranja': '#FFA500',
            'morado': '#800080',
            'rosa': '#FF69B4'
        };
        
        return colors[colorName] || colorName;
    }
    
    extractString(line, command) {
        const regex = new RegExp(`${command}\\s+"([^"]+)"`);
        const match = line.match(regex);
        return match ? match[1] : line.replace(command, '').trim();
    }
    
    handleAssignment(line) {
        const [variable, value] = line.split(' = ').map(s => s.trim());
        const evaluatedValue = this.evaluateExpression(value);
        this.variables.set(variable, evaluatedValue);
    }
    
    evaluateExpression(expr) {
        // Reemplazar variables
        for (let [key, value] of this.variables) {
            expr = expr.replace(new RegExp(`\\b${key}\\b`, 'g'), value);
        }
        
        try {
            return Function(`"use strict"; return (${expr})`)();
        } catch {
            return expr.replace(/"/g, '');
        }
    }
}

// Inicialización automática
if (typeof window !== 'undefined') {
    window.VaderGamingRuntime = VaderGamingRuntime;
}

// Export para Node.js
if (typeof module !== 'undefined' && module.exports) {
    module.exports = VaderGamingRuntime;
}
