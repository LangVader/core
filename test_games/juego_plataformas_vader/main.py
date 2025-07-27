import pygame
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
        pygame.display.set_caption("juego_plataformas_vader")
        self.clock = pygame.time.Clock()
        self.score = 0
        self.running = True
        
        # Create sprites
        self.all_sprites = pygame.sprite.Group()
        self.player = Player(100, 500)
        self.all_sprites.add(self.player)
    
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
        score_text = font.render(f"Score: {self.score}", True, (0, 0, 0))
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

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((32, 32))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 5
    
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

if __name__ == '__main__':
    game = Game()
    game.run()
