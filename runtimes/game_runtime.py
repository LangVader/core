#!/usr/bin/env python3
"""
Vader Game Runtime - Sistema completo para desarrollo de videojuegos
Soporta múltiples motores: Unity, Godot, Pygame, Phaser, etc.
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime

class VaderGameRuntime:
    """Runtime para desarrollo de videojuegos con Vader"""
    
    def __init__(self):
        self.supported_engines = {
            'unity': {'name': 'Unity Engine', 'language': 'csharp', 'extension': '.cs'},
            'godot': {'name': 'Godot Engine', 'language': 'gdscript', 'extension': '.gd'},
            'pygame': {'name': 'Pygame', 'language': 'python', 'extension': '.py'},
            'phaser': {'name': 'Phaser.js', 'language': 'javascript', 'extension': '.js'},
            'love2d': {'name': 'LÖVE 2D', 'language': 'lua', 'extension': '.lua'}
        }
        
        self.game_components = {
            'jugador': ['player', 'character', 'hero'],
            'enemigo': ['enemy', 'monster', 'villain'],
            'plataforma': ['platform', 'ground', 'floor'],
            'moneda': ['coin', 'collectible', 'pickup'],
            'powerup': ['power_up', 'boost', 'enhancement'],
            'proyectil': ['bullet', 'projectile', 'shot'],
            'obstáculo': ['obstacle', 'barrier', 'wall']
        }
        
        self.game_mechanics = {
            'movimiento': ['move', 'walk', 'run', 'speed'],
            'salto': ['jump', 'leap', 'bounce'],
            'combate': ['attack', 'fight', 'damage'],
            'colisión': ['collision', 'hit', 'overlap'],
            'puntuación': ['score', 'points', 'rating'],
            'física': ['physics', 'gravity', 'velocity'],
            'sonido': ['sound', 'audio', 'music']
        }
        
        print("🎮 Vader Game Runtime inicializado")
    
    def detect_game_elements(self, vader_code: str) -> Dict[str, List[str]]:
        """Detectar elementos de juego en código Vader"""
        code_lower = vader_code.lower()
        detected = {'components': [], 'mechanics': []}
        
        for component, keywords in self.game_components.items():
            if any(keyword in code_lower for keyword in keywords) or component in code_lower:
                detected['components'].append(component)
        
        for mechanic, keywords in self.game_mechanics.items():
            if any(keyword in code_lower for keyword in keywords) or mechanic in code_lower:
                detected['mechanics'].append(mechanic)
        
        return detected
    
    def generate_game_code(self, vader_code: str, engine: str, project_name: str = "mi_juego") -> Dict[str, str]:
        """Generar código de juego para motor específico"""
        if engine not in self.supported_engines:
            raise ValueError(f"Motor '{engine}' no soportado")
        
        elements = self.detect_game_elements(vader_code)
        print(f"🎮 Generando juego para {self.supported_engines[engine]['name']}")
        
        if engine == 'unity':
            return self._generate_unity_code(elements, project_name)
        elif engine == 'godot':
            return self._generate_godot_code(elements, project_name)
        elif engine == 'pygame':
            return self._generate_pygame_code(elements, project_name)
        elif engine == 'phaser':
            return self._generate_phaser_code(elements, project_name)
        
        return {}
    
    def _generate_unity_code(self, elements: Dict, project_name: str) -> Dict[str, str]:
        """Generar código Unity C#"""
        files = {}
        
        # GameManager principal
        game_manager = f"""using UnityEngine;

public class GameManager : MonoBehaviour
{{
    public static GameManager Instance;
    public int score = 0;
    public int lives = 3;
    
    void Awake()
    {{
        if (Instance == null)
        {{
            Instance = this;
            DontDestroyOnLoad(gameObject);
        }}
        else
        {{
            Destroy(gameObject);
        }}
    }}
    
    public void AddScore(int points)
    {{
        score += points;
        Debug.Log("Score: " + score);
    }}
    
    public void LoseLife()
    {{
        lives--;
        if (lives <= 0)
        {{
            Debug.Log("Game Over!");
        }}
    }}
}}"""
        files['GameManager.cs'] = game_manager
        
        # PlayerController si se detecta jugador
        if 'jugador' in elements['components']:
            player_controller = f"""using UnityEngine;

public class PlayerController : MonoBehaviour
{{
    public float moveSpeed = 5f;
    public float jumpForce = 10f;
    
    private Rigidbody2D rb;
    private bool isGrounded;
    
    void Start()
    {{
        rb = GetComponent<Rigidbody2D>();
    }}
    
    void Update()
    {{
        float horizontalInput = Input.GetAxis("Horizontal");
        rb.velocity = new Vector2(horizontalInput * moveSpeed, rb.velocity.y);
        
        if (Input.GetButtonDown("Jump") && isGrounded)
        {{
            rb.velocity = new Vector2(rb.velocity.x, jumpForce);
        }}
    }}
    
    void OnCollisionEnter2D(Collision2D collision)
    {{
        if (collision.gameObject.CompareTag("Ground"))
        {{
            isGrounded = true;
        }}
    }}
    
    void OnCollisionExit2D(Collision2D collision)
    {{
        if (collision.gameObject.CompareTag("Ground"))
        {{
            isGrounded = false;
        }}
    }}
}}"""
            files['PlayerController.cs'] = player_controller
        
        return files
    
    def _generate_pygame_code(self, elements: Dict, project_name: str) -> Dict[str, str]:
        """Generar código Pygame"""
        files = {}
        
        main_game = f"""import pygame
import sys

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLUE = (0, 100, 255)
RED = (255, 0, 0)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("{project_name}")
        self.clock = pygame.time.Clock()
        self.score = 0
        self.running = True
        
        # Create sprites
        self.all_sprites = pygame.sprite.Group()
        {'self.player = Player(100, 500)' if 'jugador' in elements['components'] else ''}
        {'self.all_sprites.add(self.player)' if 'jugador' in elements['components'] else ''}
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
    
    def update(self):
        self.all_sprites.update()
    
    def draw(self):
        self.screen.fill(WHITE)
        self.all_sprites.draw(self.screen)
        
        # Draw score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {{self.score}}", True, (0, 0, 0))
        self.screen.blit(score_text, (10, 10))
        
        pygame.display.flip()
    
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()

{'class Player(pygame.sprite.Sprite):' if 'jugador' in elements['components'] else ''}
{'    def __init__(self, x, y):' if 'jugador' in elements['components'] else ''}
{'        super().__init__()' if 'jugador' in elements['components'] else ''}
{'        self.image = pygame.Surface((32, 32))' if 'jugador' in elements['components'] else ''}
{'        self.image.fill(BLUE)' if 'jugador' in elements['components'] else ''}
{'        self.rect = self.image.get_rect()' if 'jugador' in elements['components'] else ''}
{'        self.rect.x = x' if 'jugador' in elements['components'] else ''}
{'        self.rect.y = y' if 'jugador' in elements['components'] else ''}
{'        self.speed = 5' if 'jugador' in elements['components'] else ''}
{'    ' if 'jugador' in elements['components'] else ''}
{'    def update(self):' if 'jugador' in elements['components'] else ''}
{'        keys = pygame.key.get_pressed()' if 'jugador' in elements['components'] else ''}
{'        if keys[pygame.K_LEFT]:' if 'jugador' in elements['components'] else ''}
{'            self.rect.x -= self.speed' if 'jugador' in elements['components'] else ''}
{'        if keys[pygame.K_RIGHT]:' if 'jugador' in elements['components'] else ''}
{'            self.rect.x += self.speed' if 'jugador' in elements['components'] else ''}

if __name__ == '__main__':
    game = Game()
    game.run()
"""
        files['main.py'] = main_game
        
        # Requirements
        files['requirements.txt'] = "pygame>=2.0.0"
        
        return files
    
    def _generate_godot_code(self, elements: Dict, project_name: str) -> Dict[str, str]:
        """Generar código Godot"""
        files = {}
        
        main_script = f"""extends Node2D

var score = 0

func _ready():
    print("Juego iniciado: {project_name}")

func add_score(points):
    score += points
    print("Score: ", score)
"""
        files['Main.gd'] = main_script
        
        if 'jugador' in elements['components']:
            player_script = """extends KinematicBody2D

export var speed = 200.0
var velocity = Vector2.ZERO

func _physics_process(delta):
    var input_vector = Vector2.ZERO
    input_vector.x = Input.get_action_strength("ui_right") - Input.get_action_strength("ui_left")
    
    velocity.x = input_vector.x * speed
    velocity = move_and_slide(velocity, Vector2.UP)
"""
            files['Player.gd'] = player_script
        
        return files
    
    def _generate_phaser_code(self, elements: Dict, project_name: str) -> Dict[str, str]:
        """Generar código Phaser.js"""
        files = {}
        
        main_js = f"""class GameScene extends Phaser.Scene {{
    constructor() {{
        super({{ key: 'GameScene' }});
        this.score = 0;
    }}
    
    preload() {{
        // Crear sprites simples con colores
        this.add.graphics()
            .fillStyle(0x0066ff)
            .fillRect(0, 0, 32, 32)
            .generateTexture('player', 32, 32);
    }}
    
    create() {{
        {'this.player = this.physics.add.sprite(100, 300, "player");' if 'jugador' in elements['components'] else ''}
        {'this.player.setCollideWorldBounds(true);' if 'jugador' in elements['components'] else ''}
        
        // UI
        this.scoreText = this.add.text(16, 16, 'Score: 0', {{
            fontSize: '32px',
            fill: '#000'
        }});
        
        // Controls
        this.cursors = this.input.keyboard.createCursorKeys();
    }}
    
    update() {{
        {'if (this.cursors.left.isDown) {' if 'jugador' in elements['components'] else ''}
        {'    this.player.setVelocityX(-160);' if 'jugador' in elements['components'] else ''}
        {'} else if (this.cursors.right.isDown) {' if 'jugador' in elements['components'] else ''}
        {'    this.player.setVelocityX(160);' if 'jugador' in elements['components'] else ''}
        {'} else {' if 'jugador' in elements['components'] else ''}
        {'    this.player.setVelocityX(0);' if 'jugador' in elements['components'] else ''}
        {'}' if 'jugador' in elements['components'] else ''}
    }}
    
    addScore(points) {{
        this.score += points;
        this.scoreText.setText('Score: ' + this.score);
    }}
}}

const config = {{
    type: Phaser.AUTO,
    width: 800,
    height: 600,
    physics: {{
        default: 'arcade',
        arcade: {{
            gravity: {{ y: 300 }},
            debug: false
        }}
    }},
    scene: GameScene
}};

const game = new Phaser.Game(config);
"""
        files['game.js'] = main_js
        
        # HTML
        html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{project_name}</title>
    <script src="https://cdn.jsdelivr.net/npm/phaser@3.70.0/dist/phaser.min.js"></script>
</head>
<body>
    <script src="game.js"></script>
</body>
</html>"""
        files['index.html'] = html_content
        
        return files
    
    def create_game_project(self, vader_code: str, engine: str, project_name: str, output_dir: str = './games') -> str:
        """Crear proyecto completo de juego"""
        # Crear directorio del proyecto
        project_path = Path(output_dir) / project_name
        project_path.mkdir(parents=True, exist_ok=True)
        
        # Generar código
        files = self.generate_game_code(vader_code, engine, project_name)
        
        # Escribir archivos
        for filename, content in files.items():
            file_path = project_path / filename
            file_path.write_text(content, encoding='utf-8')
        
        # Crear README
        readme_content = f"""# {project_name}

Juego generado con Vader Game Runtime usando {self.supported_engines[engine]['name']}.

## Código Vader original:
```
{vader_code}
```

## Instalación y ejecución:

### {self.supported_engines[engine]['name']}:
"""
        
        if engine == 'pygame':
            readme_content += """
1. Instalar dependencias: `pip install -r requirements.txt`
2. Ejecutar: `python main.py`
"""
        elif engine == 'phaser':
            readme_content += """
1. Abrir `index.html` en un navegador web
2. O usar un servidor local: `python -m http.server 8000`
"""
        elif engine == 'unity':
            readme_content += """
1. Abrir Unity Hub
2. Crear nuevo proyecto 2D
3. Copiar los scripts .cs a la carpeta Assets/Scripts/
4. Configurar la escena según los scripts
"""
        elif engine == 'godot':
            readme_content += """
1. Abrir Godot Engine
2. Importar el proyecto
3. Configurar las escenas según los scripts .gd
"""
        
        readme_content += f"""
## Generado el: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---
Creado con ❤️ usando Vader Game Runtime
"""
        
        (project_path / 'README.md').write_text(readme_content, encoding='utf-8')
        
        print(f"✅ Proyecto de juego creado en: {project_path}")
        return str(project_path)

def main():
    """Función principal para testing"""
    runtime = VaderGameRuntime()
    
    print("🧪 PROBANDO VADER GAME RUNTIME")
    print("=" * 50)
    
    # Código Vader de ejemplo
    vader_code = """# Juego de plataformas simple
crear jugador en posición 100, 500
crear enemigo que se mueve
crear plataforma para saltar
crear moneda para recoger

cuando jugador toca moneda entonces
    sumar 10 puntos
    eliminar moneda
fin

cuando jugador toca enemigo entonces
    perder vida
fin

si presionar tecla izquierda entonces
    mover jugador izquierda
fin

si presionar tecla derecha entonces
    mover jugador derecha  
fin

si presionar tecla espacio entonces
    jugador salta
fin"""
    
    # Probar detección de elementos
    elements = runtime.detect_game_elements(vader_code)
    print(f"\n🎯 ELEMENTOS DETECTADOS:")
    print(f"  Componentes: {elements['components']}")
    print(f"  Mecánicas: {elements['mechanics']}")
    
    # Generar código para diferentes motores
    engines_to_test = ['pygame', 'phaser', 'unity']
    
    for engine in engines_to_test:
        print(f"\n🎮 GENERANDO CÓDIGO PARA {engine.upper()}:")
        try:
            files = runtime.generate_game_code(vader_code, engine, "mi_juego_plataformas")
            print(f"  ✅ {len(files)} archivos generados")
            for filename in files.keys():
                print(f"    - {filename}")
        except Exception as e:
            print(f"  ❌ Error: {e}")
    
    # Crear proyecto completo de ejemplo
    try:
        project_path = runtime.create_game_project(
            vader_code, 
            'pygame', 
            'juego_plataformas_vader',
            './test_games'
        )
        print(f"\n✅ Proyecto de prueba creado en: {project_path}")
    except Exception as e:
        print(f"\n❌ Error creando proyecto: {e}")
    
    print("\n🎉 VADER GAME RUNTIME FUNCIONAL")
    return True

if __name__ == '__main__':
    success = main()
    import sys
    sys.exit(0 if success else 1)
