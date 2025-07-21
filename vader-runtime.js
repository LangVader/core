/**
 * VADER WEB RUNTIME - Intérprete Nativo para Browsers
 * El primer runtime web para ejecutar archivos .vdr directamente en navegadores
 * 
 * Permite ejecutar código Vader sin transpilación, directamente en el browser
 * Autor: Vader Team
 * Versión: 1.0.0 - Web Native Runtime
 */

class VaderWebRuntime {
    constructor() {
        this.variables = new Map();
        this.functions = new Map();
        this.outputBuffer = [];
        this.debugMode = false;
        this.outputElement = null;
        this.inputCallback = null;
    }

    /**
     * Configura el elemento DOM donde mostrar la salida
     */
    setOutputElement(element) {
        this.outputElement = element;
    }

    /**
     * Configura el callback para input del usuario
     */
    setInputCallback(callback) {
        this.inputCallback = callback;
    }

    /**
     * Ejecuta código Vader desde un string
     */
    async executeCode(code, filename = '<web>') {
        try {
            const lines = code.split('\n');
            return await this.executeLines(lines, filename);
        } catch (error) {
            this.error(`Error en ${filename}: ${error.message}`);
            return false;
        }
    }

    /**
     * Ejecuta líneas de código Vader
     */
    async executeLines(lines, filename) {
        let i = 0;
        while (i < lines.length) {
            const line = lines[i].trim();
            
            // Saltar líneas vacías y comentarios
            if (!line || line.startsWith('#')) {
                i++;
                continue;
            }

            try {
                const nextI = await this.executeLine(line, lines, i, filename);
                i = nextI !== null ? nextI : i + 1;
            } catch (error) {
                this.error(`Error en línea ${i + 1} de ${filename}: ${error.message}`);
                this.error(`Línea: ${line}`);
                return false;
            }
        }
        return true;
    }

    /**
     * Ejecuta una línea individual de código Vader
     */
    async executeLine(line, lines, currentLine, filename) {
        // MOSTRAR - Imprimir en pantalla
        if (line.startsWith('mostrar ')) {
            const content = line.substring(8).trim();
            const value = this.evaluateExpression(content);
            this.output(value);
            return null;
        }

        // VARIABLE ASSIGNMENT - Asignación de variables
        if (line.includes('=') && !this.hasComparisonOperator(line)) {
            const parts = line.split('=', 2);
            const varName = parts[0].trim();
            const varValue = parts[1].trim();
            
            this.variables.set(varName, this.evaluateExpression(varValue));
            return null;
        }

        // PREGUNTAR - Input del usuario
        if (line.startsWith('preguntar ')) {
            const match = line.match(/preguntar "([^"]*)"(?:\s+guardar\s+(?:la\s+)?respuesta\s+en\s+(\w+))?/);
            if (match) {
                const prompt = match[1];
                const varName = match[2];
                
                const userInput = await this.getUserInput(prompt);
                if (varName) {
                    this.variables.set(varName, userInput);
                }
                return null;
            }
        }

        // LEER - Input simple
        if (line.startsWith('leer ')) {
            const varName = line.substring(5).trim();
            const userInput = await this.getUserInput('');
            this.variables.set(varName, userInput);
            return null;
        }

        // CONVERTIR - Conversiones de tipo
        if (line.startsWith('convertir ')) {
            const match = line.match(/convertir\s+(\w+)\s+a\s+(numero|texto)/);
            if (match) {
                const varName = match[1];
                const targetType = match[2];
                
                if (this.variables.has(varName)) {
                    const value = this.variables.get(varName);
                    if (targetType === 'numero') {
                        const numValue = parseFloat(value);
                        if (!isNaN(numValue)) {
                            this.variables.set(varName, numValue);
                        } else {
                            this.error(`No se puede convertir '${value}' a número`);
                        }
                    } else if (targetType === 'texto') {
                        this.variables.set(varName, String(value));
                    }
                }
                return null;
            }
        }

        // SI - Condicionales
        if (line.startsWith('si ')) {
            return await this.executeConditional(line, lines, currentLine, filename);
        }

        // FUNCION - Definición de funciones
        if (line.startsWith('funcion ')) {
            return this.executeFunctionDefinition(line, lines, currentLine, filename);
        }

        // REPETIR - Bucles
        if (line.startsWith('repetir ')) {
            return await this.executeLoop(line, lines, currentLine, filename);
        }

        // Llamada a función
        if (this.functions.has(line)) {
            await this.callFunction(line);
            return null;
        }

        // CREAR ELEMENTO WEB - Funcionalidad específica del browser
        if (line.startsWith('crear ')) {
            return this.executeWebCommand(line);
        }

        // Línea no reconocida
        if (this.debugMode) {
            this.debug(`Línea no reconocida: ${line}`);
        }

        return null;
    }

    /**
     * Ejecuta condicionales (si/sino/fin si)
     */
    async executeConditional(line, lines, currentLine, filename) {
        const condition = line.substring(3).trim();
        const conditionResult = this.evaluateCondition(condition);
        
        let i = currentLine + 1;
        let executedBlock = false;

        while (i < lines.length) {
            const current = lines[i].trim();
            
            if (current === 'fin si') {
                return i + 1;
            } else if (current === 'sino' || current.startsWith('sino si ')) {
                if (executedBlock) {
                    i = this.skipToNextElseOrEnd(lines, i);
                    continue;
                } else if (current === 'sino') {
                    i++;
                    while (i < lines.length && lines[i].trim() !== 'fin si') {
                        const nextI = await this.executeLine(lines[i].trim(), lines, i, filename);
                        i = nextI !== null ? nextI : i + 1;
                    }
                    executedBlock = true;
                } else {
                    const newCondition = current.substring(8).trim();
                    if (this.evaluateCondition(newCondition)) {
                        // Ejecutar este bloque
                        i++;
                        continue;
                    } else {
                        i = this.skipToNextElseOrEnd(lines, i);
                        continue;
                    }
                }
            } else if (conditionResult && !executedBlock) {
                const nextI = await this.executeLine(current, lines, i, filename);
                i = nextI !== null ? nextI : i + 1;
                executedBlock = true;
            } else {
                i++;
            }
        }
        return i;
    }

    /**
     * Define una función
     */
    executeFunctionDefinition(line, lines, currentLine, filename) {
        const funcName = line.substring(8).trim();
        const funcLines = [];
        
        let i = currentLine + 1;
        while (i < lines.length) {
            const current = lines[i].trim();
            if (current === 'fin funcion') {
                break;
            }
            funcLines.push(lines[i]);
            i++;
        }
        
        this.functions.set(funcName, funcLines);
        return i + 1;
    }

    /**
     * Ejecuta bucles
     */
    async executeLoop(line, lines, currentLine, filename) {
        // repetir X veces
        const timesMatch = line.match(/repetir\s+(\d+)\s+veces/);
        if (timesMatch) {
            const times = parseInt(timesMatch[1]);
            const loopLines = [];
            
            let i = currentLine + 1;
            while (i < lines.length) {
                const current = lines[i].trim();
                if (current === 'fin repetir') {
                    break;
                }
                loopLines.push(lines[i]);
                i++;
            }
            
            // Ejecutar el bucle
            for (let j = 0; j < times; j++) {
                await this.executeLines(loopLines, filename);
            }
            
            return i + 1;
        }
        
        return currentLine + 1;
    }

    /**
     * Llama a una función definida
     */
    async callFunction(funcName) {
        if (this.functions.has(funcName)) {
            await this.executeLines(this.functions.get(funcName), `<function:${funcName}>`);
        }
    }

    /**
     * Ejecuta comandos específicos del web
     */
    executeWebCommand(line) {
        if (line.startsWith('crear boton ')) {
            const match = line.match(/crear boton "([^"]*)"(?:\s+al\s+hacer\s+click\s+(.+))?/);
            if (match) {
                const buttonText = match[1];
                const clickAction = match[2];
                
                this.createButton(buttonText, clickAction);
                return null;
            }
        }
        
        if (line.startsWith('crear titulo ')) {
            const match = line.match(/crear titulo "([^"]*)"/);
            if (match) {
                const titleText = match[1];
                this.createTitle(titleText);
                return null;
            }
        }
        
        return null;
    }

    /**
     * Evalúa una expresión Vader
     */
    evaluateExpression(expr) {
        expr = expr.trim();
        
        // String literal
        if (expr.startsWith('"') && expr.endsWith('"')) {
            return expr.slice(1, -1);
        }
        
        // Número
        const numValue = parseFloat(expr);
        if (!isNaN(numValue)) {
            return numValue;
        }
        
        // Variable
        if (this.variables.has(expr)) {
            return this.variables.get(expr);
        }
        
        // Operaciones matemáticas simples
        if (expr.includes('+')) {
            const parts = expr.split('+', 2);
            if (parts.length === 2) {
                const left = this.evaluateExpression(parts[0].trim());
                const right = this.evaluateExpression(parts[1].trim());
                
                // Concatenación de strings o suma matemática
                if (typeof left === 'string' || typeof right === 'string') {
                    return String(left) + String(right);
                }
                return left + right;
            }
        }
        
        if (expr.includes('-') && !expr.startsWith('-')) {
            const parts = expr.split('-', 2);
            if (parts.length === 2) {
                const left = this.evaluateExpression(parts[0].trim());
                const right = this.evaluateExpression(parts[1].trim());
                return left - right;
            }
        }
        
        if (expr.includes('*')) {
            const parts = expr.split('*', 2);
            if (parts.length === 2) {
                const left = this.evaluateExpression(parts[0].trim());
                const right = this.evaluateExpression(parts[1].trim());
                return left * right;
            }
        }
        
        if (expr.includes('/')) {
            const parts = expr.split('/', 2);
            if (parts.length === 2) {
                const left = this.evaluateExpression(parts[0].trim());
                const right = this.evaluateExpression(parts[1].trim());
                return left / right;
            }
        }
        
        return expr;
    }

    /**
     * Evalúa una condición booleana
     */
    evaluateCondition(condition) {
        condition = condition.trim();
        
        // Operadores de comparación
        if (condition.includes(' es igual a ')) {
            const parts = condition.split(' es igual a ');
            const left = this.evaluateExpression(parts[0].trim());
            const right = this.evaluateExpression(parts[1].trim());
            return left == right;
        }
        
        if (condition.includes(' es mayor que ')) {
            const parts = condition.split(' es mayor que ');
            const left = this.evaluateExpression(parts[0].trim());
            const right = this.evaluateExpression(parts[1].trim());
            return left > right;
        }
        
        if (condition.includes(' es menor que ')) {
            const parts = condition.split(' es menor que ');
            const left = this.evaluateExpression(parts[0].trim());
            const right = this.evaluateExpression(parts[1].trim());
            return left < right;
        }
        
        // Condición simple
        const value = this.evaluateExpression(condition);
        return Boolean(value);
    }

    /**
     * Utilidades
     */
    hasComparisonOperator(line) {
        return line.includes('==') || line.includes('!=') || 
               line.includes('>=') || line.includes('<=') ||
               line.includes(' es igual a ') || line.includes(' es mayor que ') ||
               line.includes(' es menor que ');
    }

    skipToNextElseOrEnd(lines, start) {
        let i = start + 1;
        while (i < lines.length) {
            const current = lines[i].trim();
            if (current === 'sino' || current === 'fin si' || current.startsWith('sino si ')) {
                return i;
            }
            i++;
        }
        return i;
    }

    /**
     * Funciones de salida y entrada
     */
    output(message) {
        this.outputBuffer.push(String(message));
        if (this.outputElement) {
            this.outputElement.innerHTML += String(message) + '<br>';
            this.outputElement.scrollTop = this.outputElement.scrollHeight;
        } else {
            console.log(message);
        }
    }

    async getUserInput(prompt) {
        if (this.inputCallback) {
            return await this.inputCallback(prompt);
        } else {
            return prompt(prompt || 'Ingrese un valor:') || '';
        }
    }

    error(message) {
        const errorMsg = `❌ Error Vader: ${message}`;
        this.output(errorMsg);
        console.error(errorMsg);
    }

    debug(message) {
        if (this.debugMode) {
            const debugMsg = `🔍 Debug: ${message}`;
            this.output(debugMsg);
            console.log(debugMsg);
        }
    }

    /**
     * Funciones específicas del web
     */
    createButton(text, clickAction) {
        if (this.outputElement) {
            const button = document.createElement('button');
            button.textContent = text;
            button.style.cssText = `
                background: #ffd700;
                color: #000;
                border: none;
                padding: 10px 20px;
                margin: 5px;
                border-radius: 5px;
                cursor: pointer;
                font-weight: bold;
            `;
            
            if (clickAction) {
                button.onclick = async () => {
                    if (clickAction.startsWith('mostrar ')) {
                        const content = clickAction.substring(8).trim();
                        const value = this.evaluateExpression(content);
                        this.output(value);
                    } else {
                        await this.executeCode(clickAction);
                    }
                };
            }
            
            this.outputElement.appendChild(button);
        }
    }

    createTitle(text) {
        if (this.outputElement) {
            const title = document.createElement('h2');
            title.textContent = text;
            title.style.cssText = `
                color: #ffd700;
                font-family: Arial, sans-serif;
                margin: 20px 0 10px 0;
                text-shadow: 0 0 10px rgba(255, 215, 0, 0.3);
            `;
            this.outputElement.appendChild(title);
        }
    }

    /**
     * Limpiar runtime
     */
    clear() {
        this.variables.clear();
        this.functions.clear();
        this.outputBuffer = [];
        if (this.outputElement) {
            this.outputElement.innerHTML = '';
        }
    }
}

/**
 * Funciones globales para facilitar el uso
 */
window.VaderWebRuntime = VaderWebRuntime;

// Función para ejecutar código Vader desde un script tag
async function executeVaderScript(scriptElement) {
    const runtime = new VaderWebRuntime();
    const code = scriptElement.textContent;
    
    // Buscar elemento de salida
    const outputId = scriptElement.getAttribute('data-output');
    if (outputId) {
        const outputElement = document.getElementById(outputId);
        if (outputElement) {
            runtime.setOutputElement(outputElement);
        }
    }
    
    // Configurar input callback
    runtime.setInputCallback(async (prompt) => {
        return prompt(prompt || 'Ingrese un valor:') || '';
    });
    
    await runtime.executeCode(code);
}

// Auto-ejecutar scripts de tipo "text/vader" al cargar la página
document.addEventListener('DOMContentLoaded', () => {
    const vaderScripts = document.querySelectorAll('script[type="text/vader"]');
    vaderScripts.forEach(script => {
        executeVaderScript(script);
    });
});

console.log('🚀 Vader Web Runtime cargado - ¡El primer intérprete web nativo de Vader!');
