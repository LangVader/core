#!/usr/bin/env python3
"""
🤖 VADER AI BACKEND - PRIMERA IMPLEMENTACIÓN MUNDIAL
Backend de IA real para Vader con múltiples proveedores de IA
Soporta OpenAI, Anthropic, Google, Ollama local y más
"""

import asyncio
import json
import os
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime
import aiohttp
from flask import Flask, request, jsonify
from flask_cors import CORS

# Configuración de proveedores de IA
AI_PROVIDERS = {
    'openai': {
        'api_key': os.getenv('OPENAI_API_KEY'),
        'base_url': 'https://api.openai.com/v1',
        'model': 'gpt-4'
    },
    'anthropic': {
        'api_key': os.getenv('ANTHROPIC_API_KEY'),
        'base_url': 'https://api.anthropic.com/v1',
        'model': 'claude-3-sonnet-20240229'
    },
    'ollama': {
        'base_url': 'http://localhost:11434/api',
        'model': 'llama2'
    },
    'google': {
        'api_key': os.getenv('GOOGLE_AI_API_KEY'),
        'base_url': 'https://generativelanguage.googleapis.com/v1beta',
        'model': 'gemini-pro'
    }
}

class VaderAIBackend:
    """Backend de IA real para Vader"""
    
    def __init__(self):
        self.app = Flask(__name__)
        CORS(self.app)
        
        self.conversation_history = {}
        self.vader_context = self.load_vader_context()
        self.active_provider = self.detect_available_provider()
        
        self.setup_logging()
        self.setup_routes()
        
        print(f"🤖 Vader AI Backend inicializado con {self.active_provider}")
    
    def setup_logging(self):
        """Configurar logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - VaderAI - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    def load_vader_context(self) -> str:
        """Cargar contexto sobre Vader para la IA"""
        return """
        Eres un asistente de IA especializado en el lenguaje de programación Vader.
        
        SOBRE VADER:
        - Vader es el primer lenguaje universal ejecutable nativo en español
        - Permite programar en español natural sin barreras técnicas
        - Tiene runtimes nativos para CLI, Web, Móvil, Cloud, Gaming e IoT
        - Democratiza la programación para cualquier persona
        
        SINTAXIS BÁSICA DE VADER:
        - mostrar "mensaje" - Mostrar texto
        - variable = valor - Asignar variable
        - si condicion entonces accion fin si - Condicional
        - repetir X veces accion fin repetir - Bucle
        - funcion nombre accion fin funcion - Definir función
        
        COMANDOS ESPECIALIZADOS:
        - Web: crear boton "texto" al hacer click accion
        - Móvil: tomar foto, obtener ubicacion, vibrar
        - Gaming: crear sprite, detectar colision, reproducir sonido
        - IoT: leer sensor, activar actuador, enviar mqtt
        - Cloud: subir archivo, guardar en base, invocar funcion
        
        RESPONDE SIEMPRE EN ESPAÑOL y ayuda con programación en Vader.
        """
    
    def detect_available_provider(self) -> str:
        """Detectar proveedor de IA disponible"""
        # Prioridad: OpenAI > Anthropic > Ollama local > Google
        if AI_PROVIDERS['openai']['api_key']:
            return 'openai'
        elif AI_PROVIDERS['anthropic']['api_key']:
            return 'anthropic'
        elif self.test_ollama_connection():
            return 'ollama'
        elif AI_PROVIDERS['google']['api_key']:
            return 'google'
        else:
            return 'mock'  # IA simulada como fallback
    
    def test_ollama_connection(self) -> bool:
        """Probar conexión con Ollama local"""
        try:
            import requests
            response = requests.get('http://localhost:11434/api/tags', timeout=2)
            return response.status_code == 200
        except:
            return False
    
    def setup_routes(self):
        """Configurar rutas de la API"""
        
        @self.app.route('/ai/chat', methods=['POST'])
        def chat():
            """Endpoint principal de chat"""
            try:
                data = request.get_json()
                message = data.get('message', '')
                session_id = data.get('session_id', 'default')
                action_type = data.get('action_type', 'chat')
                
                if not message:
                    return jsonify({'error': 'Mensaje requerido'}), 400
                
                # Procesar según tipo de acción
                if action_type == 'generate':
                    response = asyncio.run(self.generate_code(message, session_id))
                elif action_type == 'analyze':
                    response = asyncio.run(self.analyze_code(message, session_id))
                elif action_type == 'optimize':
                    response = asyncio.run(self.optimize_code(message, session_id))
                elif action_type == 'explain':
                    response = asyncio.run(self.explain_code(message, session_id))
                elif action_type == 'debug':
                    response = asyncio.run(self.debug_code(message, session_id))
                else:
                    response = asyncio.run(self.chat_response(message, session_id))
                
                return jsonify({
                    'response': response,
                    'provider': self.active_provider,
                    'timestamp': datetime.now().isoformat()
                })
                
            except Exception as e:
                self.logger.error(f"Error en chat: {e}")
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/ai/providers', methods=['GET'])
        def get_providers():
            """Obtener proveedores disponibles"""
            available = []
            for provider, config in AI_PROVIDERS.items():
                if provider == 'ollama':
                    if self.test_ollama_connection():
                        available.append(provider)
                elif config.get('api_key'):
                    available.append(provider)
            
            return jsonify({
                'available_providers': available,
                'active_provider': self.active_provider
            })
        
        @self.app.route('/ai/switch-provider', methods=['POST'])
        def switch_provider():
            """Cambiar proveedor de IA"""
            data = request.get_json()
            new_provider = data.get('provider')
            
            if new_provider in AI_PROVIDERS:
                self.active_provider = new_provider
                return jsonify({'success': True, 'active_provider': new_provider})
            else:
                return jsonify({'error': 'Proveedor no válido'}), 400
    
    async def chat_response(self, message: str, session_id: str) -> str:
        """Respuesta general de chat"""
        prompt = f"""
        {self.vader_context}
        
        Usuario: {message}
        
        Responde de manera útil y educativa sobre programación en Vader.
        Si el usuario pregunta algo no relacionado con programación, 
        redirige amablemente hacia temas de Vader.
        """
        
        return await self.call_ai_provider(prompt, session_id)
    
    async def generate_code(self, description: str, session_id: str) -> str:
        """Generar código Vader"""
        prompt = f"""
        {self.vader_context}
        
        TAREA: Generar código Vader para: {description}
        
        INSTRUCCIONES:
        1. Escribe código Vader funcional y completo
        2. Usa sintaxis correcta de Vader
        3. Incluye comentarios explicativos
        4. Asegúrate de que sea ejecutable
        5. Si es para web, usa comandos web de Vader
        6. Si es para móvil, usa comandos móviles
        7. Si es para IoT, usa comandos de sensores/actuadores
        
        RESPUESTA: Solo código Vader con comentarios, sin explicaciones adicionales.
        """
        
        return await self.call_ai_provider(prompt, session_id)
    
    async def analyze_code(self, code: str, session_id: str) -> str:
        """Analizar código Vader"""
        prompt = f"""
        {self.vader_context}
        
        TAREA: Analizar este código Vader:
        
        ```vader
        {code}
        ```
        
        ANÁLISIS REQUERIDO:
        1. ¿El código es sintácticamente correcto?
        2. ¿Qué hace el código paso a paso?
        3. ¿Hay errores potenciales?
        4. ¿Qué mejoras se pueden hacer?
        5. ¿Es eficiente y bien estructurado?
        
        Proporciona un análisis detallado y constructivo.
        """
        
        return await self.call_ai_provider(prompt, session_id)
    
    async def optimize_code(self, code: str, session_id: str) -> str:
        """Optimizar código Vader"""
        prompt = f"""
        {self.vader_context}
        
        TAREA: Optimizar este código Vader:
        
        ```vader
        {code}
        ```
        
        OPTIMIZACIONES:
        1. Mejorar eficiencia
        2. Simplificar lógica
        3. Hacer más legible
        4. Agregar mejores prácticas
        5. Optimizar para el runtime específico
        
        RESPUESTA: Código Vader optimizado con explicación de cambios.
        """
        
        return await self.call_ai_provider(prompt, session_id)
    
    async def explain_code(self, code: str, session_id: str) -> str:
        """Explicar código Vader"""
        prompt = f"""
        {self.vader_context}
        
        TAREA: Explicar este código Vader de manera educativa:
        
        ```vader
        {code}
        ```
        
        EXPLICACIÓN REQUERIDA:
        1. ¿Qué hace cada línea?
        2. ¿Cómo funciona la lógica general?
        3. ¿Qué conceptos de programación usa?
        4. ¿Para qué casos de uso es útil?
        5. ¿Cómo se puede extender o modificar?
        
        Explica de manera clara y educativa, como si fuera para alguien aprendiendo.
        """
        
        return await self.call_ai_provider(prompt, session_id)
    
    async def debug_code(self, code: str, session_id: str) -> str:
        """Depurar código Vader"""
        prompt = f"""
        {self.vader_context}
        
        TAREA: Depurar este código Vader que tiene errores:
        
        ```vader
        {code}
        ```
        
        DEPURACIÓN:
        1. Identificar errores de sintaxis
        2. Encontrar errores de lógica
        3. Detectar problemas potenciales
        4. Proporcionar código corregido
        5. Explicar qué estaba mal y por qué
        
        RESPUESTA: Código corregido + explicación de errores encontrados.
        """
        
        return await self.call_ai_provider(prompt, session_id)
    
    async def call_ai_provider(self, prompt: str, session_id: str) -> str:
        """Llamar al proveedor de IA activo"""
        try:
            if self.active_provider == 'openai':
                return await self.call_openai(prompt, session_id)
            elif self.active_provider == 'anthropic':
                return await self.call_anthropic(prompt, session_id)
            elif self.active_provider == 'ollama':
                return await self.call_ollama(prompt, session_id)
            elif self.active_provider == 'google':
                return await self.call_google(prompt, session_id)
            else:
                return self.mock_ai_response(prompt)
        
        except Exception as e:
            self.logger.error(f"Error llamando IA: {e}")
            return f"❌ Error de IA: {str(e)}. Usando respuesta simulada."
    
    async def call_openai(self, prompt: str, session_id: str) -> str:
        """Llamar a OpenAI GPT"""
        config = AI_PROVIDERS['openai']
        
        # Obtener historial de conversación
        history = self.conversation_history.get(session_id, [])
        
        messages = [
            {"role": "system", "content": self.vader_context},
            *history,
            {"role": "user", "content": prompt}
        ]
        
        async with aiohttp.ClientSession() as session:
            headers = {
                'Authorization': f"Bearer {config['api_key']}",
                'Content-Type': 'application/json'
            }
            
            data = {
                'model': config['model'],
                'messages': messages,
                'max_tokens': 1000,
                'temperature': 0.7
            }
            
            async with session.post(f"{config['base_url']}/chat/completions", 
                                  headers=headers, json=data) as response:
                result = await response.json()
                
                if response.status == 200:
                    ai_response = result['choices'][0]['message']['content']
                    
                    # Actualizar historial
                    if session_id not in self.conversation_history:
                        self.conversation_history[session_id] = []
                    
                    self.conversation_history[session_id].extend([
                        {"role": "user", "content": prompt},
                        {"role": "assistant", "content": ai_response}
                    ])
                    
                    # Limitar historial a últimas 10 interacciones
                    if len(self.conversation_history[session_id]) > 20:
                        self.conversation_history[session_id] = self.conversation_history[session_id][-20:]
                    
                    return ai_response
                else:
                    raise Exception(f"OpenAI API error: {result}")
    
    async def call_anthropic(self, prompt: str, session_id: str) -> str:
        """Llamar a Anthropic Claude"""
        config = AI_PROVIDERS['anthropic']
        
        async with aiohttp.ClientSession() as session:
            headers = {
                'x-api-key': config['api_key'],
                'Content-Type': 'application/json',
                'anthropic-version': '2023-06-01'
            }
            
            data = {
                'model': config['model'],
                'max_tokens': 1000,
                'messages': [
                    {"role": "user", "content": f"{self.vader_context}\n\n{prompt}"}
                ]
            }
            
            async with session.post(f"{config['base_url']}/messages", 
                                  headers=headers, json=data) as response:
                result = await response.json()
                
                if response.status == 200:
                    return result['content'][0]['text']
                else:
                    raise Exception(f"Anthropic API error: {result}")
    
    async def call_ollama(self, prompt: str, session_id: str) -> str:
        """Llamar a Ollama local"""
        config = AI_PROVIDERS['ollama']
        
        async with aiohttp.ClientSession() as session:
            data = {
                'model': config['model'],
                'prompt': f"{self.vader_context}\n\n{prompt}",
                'stream': False
            }
            
            async with session.post(f"{config['base_url']}/generate", 
                                  json=data) as response:
                result = await response.json()
                
                if response.status == 200:
                    return result['response']
                else:
                    raise Exception(f"Ollama error: {result}")
    
    async def call_google(self, prompt: str, session_id: str) -> str:
        """Llamar a Google Gemini"""
        config = AI_PROVIDERS['google']
        
        async with aiohttp.ClientSession() as session:
            url = f"{config['base_url']}/models/{config['model']}:generateContent"
            params = {'key': config['api_key']}
            
            data = {
                'contents': [{
                    'parts': [{
                        'text': f"{self.vader_context}\n\n{prompt}"
                    }]
                }]
            }
            
            async with session.post(url, params=params, json=data) as response:
                result = await response.json()
                
                if response.status == 200:
                    return result['candidates'][0]['content']['parts'][0]['text']
                else:
                    raise Exception(f"Google AI error: {result}")
    
    def mock_ai_response(self, prompt: str) -> str:
        """Respuesta de IA simulada como fallback"""
        responses = {
            'generate': """# Código Vader generado
mostrar "¡Hola desde Vader!"
nombre = "Usuario"
mostrar "Bienvenido " + nombre

# Ejemplo interactivo
crear boton "Saludar" al hacer click mostrar "¡Hola mundo!"
""",
            'analyze': """📊 Análisis del código:
✅ Sintaxis correcta
✅ Lógica clara y funcional
💡 Sugerencia: Agregar validación de entrada
🎯 Propósito: Programa de saludo interactivo""",
            'optimize': """# Código optimizado:
# Versión más eficiente con validaciones
si nombre no es vacio
    mostrar "Bienvenido " + nombre
sino
    mostrar "Bienvenido, usuario anónimo"
fin si""",
            'explain': """🎓 Explicación del código:
1. 'mostrar' - Imprime texto en pantalla
2. Variables se asignan con =
3. 'crear boton' - Crea elemento interactivo web
4. El código es ejecutable en runtime web de Vader""",
            'debug': """🐛 Errores encontrados y corregidos:
❌ Error: Falta 'fin si' en condicional
✅ Corregido: Agregado 'fin si'
❌ Error: Variable no definida
✅ Corregido: Inicializada variable"""
        }
        
        # Detectar tipo de solicitud
        if 'generar' in prompt.lower() or 'generate' in prompt.lower():
            return responses['generate']
        elif 'analizar' in prompt.lower() or 'analyze' in prompt.lower():
            return responses['analyze']
        elif 'optimizar' in prompt.lower() or 'optimize' in prompt.lower():
            return responses['optimize']
        elif 'explicar' in prompt.lower() or 'explain' in prompt.lower():
            return responses['explain']
        elif 'depurar' in prompt.lower() or 'debug' in prompt.lower():
            return responses['debug']
        else:
            return """🤖 ¡Hola! Soy el asistente de IA de Vader.

Puedo ayudarte con:
• 🔧 Generar código Vader
• 📊 Analizar tu código
• ⚡ Optimizar programas
• 🎓 Explicar conceptos
• 🐛 Depurar errores

¿En qué te gustaría que te ayude hoy?"""
    
    def run(self, host='localhost', port=5001, debug=False):
        """Ejecutar servidor de IA"""
        print(f"🚀 Iniciando Vader AI Backend en http://{host}:{port}")
        self.app.run(host=host, port=port, debug=debug)

# Punto de entrada
if __name__ == "__main__":
    backend = VaderAIBackend()
    backend.run(debug=True)
