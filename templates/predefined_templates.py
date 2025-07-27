#!/usr/bin/env python3
"""
Vader Predefined Templates - Sistema de plantillas predefinidas para aplicaciones comunes
Permite crear aplicaciones completas instantáneamente con configuración mínima
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime

class VaderTemplateManager:
    """Gestor de plantillas predefinidas para Vader"""
    
    def __init__(self):
        self.templates_dir = Path('./templates')
        self.templates_dir.mkdir(exist_ok=True)
        
        self.available_templates = {
            'web': {
                'landing_page': {
                    'name': 'Página de Aterrizaje',
                    'description': 'Página web moderna para promocionar productos/servicios',
                    'variables': ['titulo', 'empresa', 'descripcion', 'color_primario', 'email_contacto']
                },
                'blog_personal': {
                    'name': 'Blog Personal',
                    'description': 'Blog personal con sistema de posts',
                    'variables': ['nombre_autor', 'titulo_blog', 'descripcion_blog', 'tema_color']
                },
                'portfolio': {
                    'name': 'Portfolio Profesional',
                    'description': 'Portfolio para mostrar proyectos y habilidades',
                    'variables': ['nombre_completo', 'profesion', 'descripcion_personal', 'habilidades']
                }
            },
            'mobile': {
                'app_noticias': {
                    'name': 'App de Noticias',
                    'description': 'Aplicación móvil para leer noticias',
                    'variables': ['nombre_app', 'categorias_noticias', 'color_tema', 'idioma']
                },
                'app_tareas': {
                    'name': 'App de Tareas',
                    'description': 'Gestor de tareas y productividad',
                    'variables': ['nombre_app', 'categorias_tareas', 'tema_visual']
                }
            },
            'desktop': {
                'editor_texto': {
                    'name': 'Editor de Texto',
                    'description': 'Editor de texto simple con funciones básicas',
                    'variables': ['nombre_editor', 'formatos_archivo', 'tema_editor']
                },
                'calculadora': {
                    'name': 'Calculadora',
                    'description': 'Calculadora con funciones básicas y científicas',
                    'variables': ['nombre_calc', 'funciones_cientificas', 'tema_visual']
                }
            },
            'api': {
                'api_rest': {
                    'name': 'API REST Básica',
                    'description': 'API REST con CRUD completo',
                    'variables': ['nombre_api', 'entidades', 'base_datos', 'autenticacion']
                },
                'api_auth': {
                    'name': 'API de Autenticación',
                    'description': 'Sistema de autenticación con JWT',
                    'variables': ['secret_key', 'token_expiry', 'roles_usuario']
                }
            },
            'game': {
                'juego_plataformas': {
                    'name': 'Juego de Plataformas',
                    'description': 'Juego 2D de plataformas estilo Mario',
                    'variables': ['nombre_juego', 'personaje_principal', 'tipos_enemigos']
                },
                'puzzle_game': {
                    'name': 'Juego de Puzzles',
                    'description': 'Juego de rompecabezas y lógica',
                    'variables': ['tipo_puzzle', 'dificultades', 'sistema_puntos']
                }
            }
        }
        
        print("📋 Vader Template Manager inicializado")
    
    def list_templates(self, category: str = None) -> List[Dict]:
        """Listar plantillas disponibles"""
        templates = []
        
        if category and category in self.available_templates:
            for template_id, template_info in self.available_templates[category].items():
                templates.append({
                    'id': f"{category}_{template_id}",
                    'category': category,
                    **template_info
                })
        else:
            for cat, cat_templates in self.available_templates.items():
                for template_id, template_info in cat_templates.items():
                    templates.append({
                        'id': f"{cat}_{template_id}",
                        'category': cat,
                        **template_info
                    })
        
        return templates
    
    def create_from_template(self, template_id: str, project_name: str, 
                           variables: Dict[str, Any], output_dir: str = './') -> str:
        """Crear proyecto desde plantilla"""
        # Parsear template_id
        parts = template_id.split('_', 1)
        if len(parts) != 2:
            raise ValueError(f"ID de plantilla inválido: {template_id}")
        
        category, template_type = parts
        
        if category not in self.available_templates or template_type not in self.available_templates[category]:
            raise ValueError(f"Plantilla '{template_id}' no encontrada")
        
        # Crear directorio del proyecto
        project_path = Path(output_dir) / project_name
        project_path.mkdir(parents=True, exist_ok=True)
        
        template_info = self.available_templates[category][template_type]
        print(f"🚀 Creando proyecto '{project_name}' desde plantilla '{template_info['name']}'")
        
        # Generar archivos según el tipo
        if category == 'web':
            self._create_web_template(project_path, template_type, variables)
        elif category == 'mobile':
            self._create_mobile_template(project_path, template_type, variables)
        elif category == 'desktop':
            self._create_desktop_template(project_path, template_type, variables)
        elif category == 'api':
            self._create_api_template(project_path, template_type, variables)
        elif category == 'game':
            self._create_game_template(project_path, template_type, variables)
        
        # Crear README
        self._create_readme(project_path, template_info, variables)
        
        print(f"✅ Proyecto creado exitosamente en: {project_path}")
        return str(project_path)
    
    def _create_web_template(self, project_path: Path, template_type: str, variables: Dict):
        """Crear plantilla web"""
        if template_type == 'landing_page':
            html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{variables.get('titulo', 'Mi Página')}</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <header>
        <nav>
            <h1>{variables.get('empresa', 'Mi Empresa')}</h1>
            <ul>
                <li><a href="#inicio">Inicio</a></li>
                <li><a href="#servicios">Servicios</a></li>
                <li><a href="#contacto">Contacto</a></li>
            </ul>
        </nav>
    </header>
    
    <main>
        <section id="inicio" class="hero">
            <h2>{variables.get('titulo', 'Bienvenido')}</h2>
            <p>{variables.get('descripcion', 'Descripción de tu empresa')}</p>
            <button class="cta-button">Comenzar Ahora</button>
        </section>
        
        <section id="servicios">
            <h2>Servicios</h2>
            <div class="services-grid">
                <div class="service">
                    <h3>Servicio 1</h3>
                    <p>Descripción del servicio</p>
                </div>
                <div class="service">
                    <h3>Servicio 2</h3>
                    <p>Descripción del servicio</p>
                </div>
            </div>
        </section>
        
        <section id="contacto">
            <h2>Contacto</h2>
            <p>Email: {variables.get('email_contacto', 'contacto@empresa.com')}</p>
        </section>
    </main>
    
    <script src="script.js"></script>
</body>
</html>"""
            
            css_content = f"""/* Estilos para Landing Page */
* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: Arial, sans-serif;
    line-height: 1.6;
    color: #333;
}}

header {{
    background: {variables.get('color_primario', '#007bff')};
    color: white;
    padding: 1rem;
}}

nav {{
    display: flex;
    justify-content: space-between;
    align-items: center;
}}

nav ul {{
    display: flex;
    list-style: none;
    gap: 1rem;
}}

nav a {{
    color: white;
    text-decoration: none;
}}

.hero {{
    background: linear-gradient(135deg, {variables.get('color_primario', '#007bff')}, #0056b3);
    color: white;
    padding: 4rem 2rem;
    text-align: center;
}}

.hero h2 {{
    font-size: 2.5rem;
    margin-bottom: 1rem;
}}

.cta-button {{
    background: white;
    color: {variables.get('color_primario', '#007bff')};
    padding: 1rem 2rem;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 1.1rem;
}}

.services-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 2rem;
    padding: 2rem;
}}

.service {{
    background: #f8f9fa;
    padding: 2rem;
    border-radius: 10px;
    text-align: center;
}}

#contacto {{
    background: #f8f9fa;
    padding: 2rem;
    text-align: center;
}}"""
            
            js_content = """// Script para Landing Page
document.addEventListener('DOMContentLoaded', function() {
    const ctaButton = document.querySelector('.cta-button');
    
    ctaButton.addEventListener('click', function() {
        alert('¡Gracias por tu interés! Te contactaremos pronto.');
    });
    
    // Smooth scrolling
    const navLinks = document.querySelectorAll('nav a');
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            target.scrollIntoView({ behavior: 'smooth' });
        });
    });
});"""
            
            (project_path / 'index.html').write_text(html_content, encoding='utf-8')
            (project_path / 'styles.css').write_text(css_content, encoding='utf-8')
            (project_path / 'script.js').write_text(js_content, encoding='utf-8')
    
    def _create_mobile_template(self, project_path: Path, template_type: str, variables: Dict):
        """Crear plantilla móvil"""
        if template_type == 'app_noticias':
            app_content = f"""import React from 'react';
import {{ NavigationContainer }} from '@react-navigation/native';
import {{ createBottomTabNavigator }} from '@react-navigation/bottom-tabs';
import {{ Ionicons }} from '@expo/vector-icons';

import NewsScreen from './src/NewsScreen';
import CategoryScreen from './src/CategoryScreen';

const Tab = createBottomTabNavigator();

export default function App() {{
  return (
    <NavigationContainer>
      <Tab.Navigator
        screenOptions={{{{ ({ route }) => ({{
          tabBarIcon: ({{ focused, color, size }}) => {{
            let iconName = route.name === 'Noticias' ? 'newspaper' : 'list';
            return <Ionicons name={{iconName}} size={{size}} color={{color}} />;
          }},
          tabBarActiveTintColor: '{variables.get('color_tema', '#007bff')}',
        }})}}
      >
        <Tab.Screen name="Noticias" component={{NewsScreen}} />
        <Tab.Screen name="Categorías" component={{CategoryScreen}} />
      </Tab.Navigator>
    </NavigationContainer>
  );
}}"""
            
            package_content = f"""{{
  "name": "{variables.get('nombre_app', 'app-noticias').lower().replace(' ', '-')}",
  "version": "1.0.0",
  "main": "node_modules/expo/AppEntry.js",
  "scripts": {{
    "start": "expo start",
    "android": "expo start --android",
    "ios": "expo start --ios"
  }},
  "dependencies": {{
    "expo": "~49.0.0",
    "react": "18.2.0",
    "react-native": "0.72.6",
    "@react-navigation/native": "^6.0.0",
    "@react-navigation/bottom-tabs": "^6.0.0",
    "@expo/vector-icons": "^13.0.0"
  }}
}}"""
            
            (project_path / 'App.js').write_text(app_content, encoding='utf-8')
            (project_path / 'package.json').write_text(package_content, encoding='utf-8')
    
    def _create_desktop_template(self, project_path: Path, template_type: str, variables: Dict):
        """Crear plantilla desktop"""
        if template_type == 'editor_texto':
            main_content = f"""const {{ app, BrowserWindow }} = require('electron');

function createWindow() {{
  const mainWindow = new BrowserWindow({{
    width: 1200,
    height: 800,
    webPreferences: {{
      nodeIntegration: true,
      contextIsolation: false
    }}
  }});

  mainWindow.loadFile('editor.html');
}}

app.whenReady().then(createWindow);"""
            
            html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>{variables.get('nombre_editor', 'Mi Editor')}</title>
    <style>
        body {{ margin: 0; font-family: Arial, sans-serif; }}
        .toolbar {{ background: #333; color: white; padding: 10px; }}
        .editor {{ width: 100%; height: calc(100vh - 50px); border: none; padding: 20px; }}
    </style>
</head>
<body>
    <div class="toolbar">
        <button onclick="newFile()">Nuevo</button>
        <button onclick="saveFile()">Guardar</button>
    </div>
    <textarea class="editor" placeholder="Escribe aquí..."></textarea>
    
    <script>
        function newFile() {{
            document.querySelector('.editor').value = '';
        }}
        
        function saveFile() {{
            alert('Función de guardado - implementar según necesidades');
        }}
    </script>
</body>
</html>"""
            
            package_content = f"""{{
  "name": "{variables.get('nombre_editor', 'editor').lower().replace(' ', '-')}",
  "version": "1.0.0",
  "main": "main.js",
  "scripts": {{
    "start": "electron ."
  }},
  "devDependencies": {{
    "electron": "^22.0.0"
  }}
}}"""
            
            (project_path / 'main.js').write_text(main_content, encoding='utf-8')
            (project_path / 'editor.html').write_text(html_content, encoding='utf-8')
            (project_path / 'package.json').write_text(package_content, encoding='utf-8')
    
    def _create_api_template(self, project_path: Path, template_type: str, variables: Dict):
        """Crear plantilla API"""
        if template_type == 'api_rest':
            app_content = f"""from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Datos de ejemplo
{variables.get('entidades', 'items')} = []

@app.route('/api/{variables.get('entidades', 'items')}', methods=['GET'])
def get_items():
    return jsonify({variables.get('entidades', 'items')})

@app.route('/api/{variables.get('entidades', 'items')}', methods=['POST'])
def create_item():
    data = request.get_json()
    item = {{
        'id': len({variables.get('entidades', 'items')}) + 1,
        **data
    }}
    {variables.get('entidades', 'items')}.append(item)
    return jsonify(item), 201

@app.route('/api/{variables.get('entidades', 'items')}/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = next((i for i in {variables.get('entidades', 'items')} if i['id'] == item_id), None)
    if item:
        return jsonify(item)
    return jsonify({{'error': 'Item not found'}}), 404

if __name__ == '__main__':
    app.run(debug=True)"""
            
            requirements_content = """Flask==2.3.3
Flask-CORS==4.0.0
requests==2.31.0"""
            
            (project_path / 'app.py').write_text(app_content, encoding='utf-8')
            (project_path / 'requirements.txt').write_text(requirements_content, encoding='utf-8')
    
    def _create_game_template(self, project_path: Path, template_type: str, variables: Dict):
        """Crear plantilla de juego"""
        if template_type == 'juego_plataformas':
            game_content = f"""import pygame
import sys

# Inicializar Pygame
pygame.init()

# Configuración
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 100, 255)
RED = (255, 0, 0)

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 32
        self.height = 32
        self.vel_y = 0
        self.jumping = False
    
    def update(self):
        keys = pygame.key.get_pressed()
        
        # Movimiento horizontal
        if keys[pygame.K_LEFT]:
            self.x -= 5
        if keys[pygame.K_RIGHT]:
            self.x += 5
        
        # Salto
        if keys[pygame.K_SPACE] and not self.jumping:
            self.vel_y = -15
            self.jumping = True
        
        # Gravedad
        self.vel_y += 1
        self.y += self.vel_y
        
        # Colisión con el suelo
        if self.y >= SCREEN_HEIGHT - self.height:
            self.y = SCREEN_HEIGHT - self.height
            self.vel_y = 0
            self.jumping = False
    
    def draw(self, screen):
        pygame.draw.rect(screen, BLUE, (self.x, self.y, self.width, self.height))

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('{variables.get('nombre_juego', 'Mi Juego de Plataformas')}')
    clock = pygame.time.Clock()
    
    player = Player(100, SCREEN_HEIGHT - 64)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        player.update()
        
        screen.fill(WHITE)
        player.draw(screen)
        
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()"""
            
            requirements_content = """pygame==2.5.2"""
            
            (project_path / 'game.py').write_text(game_content, encoding='utf-8')
            (project_path / 'requirements.txt').write_text(requirements_content, encoding='utf-8')
    
    def _create_readme(self, project_path: Path, template_info: Dict, variables: Dict):
        """Crear README del proyecto"""
        readme_content = f"""# {template_info['name']}

{template_info['description']}

## Configuración

Este proyecto fue generado usando Vader Template Manager.

### Variables configuradas:
"""
        
        for var_name in template_info['variables']:
            value = variables.get(var_name, 'No configurado')
            readme_content += f"- **{var_name}**: {value}\n"
        
        readme_content += f"""
## Instalación

1. Navega al directorio del proyecto
2. Instala las dependencias (si aplica)
3. Ejecuta el proyecto

## Generado el

{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---
Creado con ❤️ usando Vader Template Manager
"""
        
        (project_path / 'README.md').write_text(readme_content, encoding='utf-8')

def main():
    """Función principal para testing"""
    manager = VaderTemplateManager()
    
    print("🧪 PROBANDO VADER TEMPLATE MANAGER")
    print("=" * 50)
    
    # Listar todas las plantillas
    templates = manager.list_templates()
    print(f"\n📋 PLANTILLAS DISPONIBLES ({len(templates)}):")
    for template in templates:
        print(f"  {template['id']}: {template['name']} - {template['description']}")
    
    # Crear proyecto de ejemplo
    variables = {
        'titulo': 'Mi Empresa Increíble',
        'empresa': 'TechCorp',
        'descripcion': 'Soluciones tecnológicas innovadoras',
        'color_primario': '#ff6b35',
        'email_contacto': 'contacto@techcorp.com'
    }
    
    try:
        project_path = manager.create_from_template(
            'web_landing_page',
            'mi_landing_page',
            variables,
            './test_templates'
        )
        print(f"\n✅ Proyecto de prueba creado en: {project_path}")
    except Exception as e:
        print(f"\n❌ Error creando proyecto: {e}")
    
    print("\n🎉 VADER TEMPLATE MANAGER FUNCIONAL")
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
