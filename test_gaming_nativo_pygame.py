# CÓDIGO GENERADO POR VADER 7.0 UNIVERSAL GAMING
# Archivo .vdr ejecutado nativamente con Pygame

import pygame
import sys
from pygame.locals import *

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Vader Game - Pygame Runtime")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Variables del juego
player_speed = 5
jump_force = 15
player_lives = 3
score = 0
clock = pygame.time.Clock()

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 32
        self.height = 32
        self.vel_y = 0
        self.on_ground = False
        self.rect = pygame.Rect(x, y, self.width, self.height)
    
    def update(self):
        # Gravedad
        if not self.on_ground:
            self.vel_y += 1
        
        self.y += self.vel_y
        self.rect.y = self.y
        
        # Límite del suelo
        if self.y >= SCREEN_HEIGHT - self.height - 50:
            self.y = SCREEN_HEIGHT - self.height - 50
            self.vel_y = 0
            self.on_ground = True
    
    def jump(self):
        if self.on_ground:
            self.vel_y = -jump_force
            self.on_ground = False
    
    def move_left(self):
        self.x -= player_speed
        self.rect.x = self.x
    
    def move_right(self):
        self.x += player_speed
        self.rect.x = self.x
    
    def draw(self, surface):
        pygame.draw.rect(surface, BLUE, self.rect)

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 32
        self.height = 32
        self.rect = pygame.Rect(x, y, self.width, self.height)
    
    def draw(self, surface):
        pygame.draw.rect(surface, RED, self.rect)

def main():
    global score, player_lives
    
    print("🎮 VADER 7.0 - Pygame Game Runtime")
    print("⚡ Ejecutando archivo .vdr nativamente con Pygame")
    
    # Crear objetos del juego
    player = Player(100, 400)
    enemies = [Enemy(300, 500), Enemy(500, 500)]
    
    running = True
    
    while running:
        # Eventos
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    player.jump()
        
        # Input continuo
        keys = pygame.key.get_pressed()
        if keys[K_LEFT] or keys[K_a]:
            player.move_left()
        if keys[K_RIGHT] or keys[K_d]:
            player.move_right()
        
        # Actualizar juego
        player.update()
        
        # Detectar colisiones
        for enemy in enemies:
            if player.rect.colliderect(enemy.rect):
                player_lives -= 1
                print(f"Player hit! Lives: {player_lives}")
                if player_lives <= 0:
                    print("Game Over!")
                    running = False
        
        # Dibujar todo
        screen.fill(WHITE)
        
        # Dibujar suelo
        pygame.draw.rect(screen, GREEN, (0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50))
        
        # Dibujar objetos
        player.draw(screen)
        for enemy in enemies:
            enemy.draw(screen)
        
        # Dibujar UI
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, BLACK)
        lives_text = font.render(f"Lives: {player_lives}", True, BLACK)
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (10, 50))
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
