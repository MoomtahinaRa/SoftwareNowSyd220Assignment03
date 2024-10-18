import pygame
import random

# Initialize Pygame
pygame.init()

# Game settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
BG_COLOR = (135, 206, 235)  # Sky blue

# Setup screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Animal Hero Side-Scrolling Game")

# Define clock
clock = pygame.time.Clock()

# Load images using simple colored surfaces
player_img = pygame.Surface((50, 50))
player_img.fill((255, 0, 0))  # Red color for player
enemy_img = pygame.Surface((40, 40))
enemy_img.fill((0, 0, 255))  # Blue color for enemy
projectile_img = pygame.Surface((20, 10))
projectile_img.fill((0, 255, 0))  # Green color for projectile
booster_img = pygame.Surface((30, 30))
booster_img.fill((255, 255, 0))  # Yellow color for booster

GROUND_LEVEL = SCREEN_HEIGHT - 100  # Set the ground level consistently for both player and enemies

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = GROUND_LEVEL - self.rect.height
        self.speed = 5
        self.jump_speed = -15
        self.gravity = 1
        self.is_jumping = False
        self.velocity_y = 0
        self.health = 100
        self.score = 0

    def move(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

    def jump(self):
        if not self.is_jumping:
            self.is_jumping = True
            self.velocity_y = self.jump_speed

    def update(self):
        # Apply gravity
        if self.is_jumping:
            self.velocity_y += self.gravity
            self.rect.y += self.velocity_y
            if self.rect.y >= GROUND_LEVEL - self.rect.height:  # Ground level
                self.rect.y = GROUND_LEVEL - self.rect.height
                self.is_jumping = False

    def shoot(self):
        projectile = Projectile(self.rect.right, self.rect.centery)
        all_sprites.add(projectile)
        projectiles.add(projectile)

# Projectile class
class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = projectile_img
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speed = 10

    def update(self):
        self.rect.x += self.speed
        if self.rect.left > SCREEN_WIDTH:
            self.kill()

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(SCREEN_WIDTH, SCREEN_WIDTH + 100)
        self.rect.y = GROUND_LEVEL - self.rect.height
        self.speed = random.randint(3, 6)

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()

# Booster class
class Booster(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = booster_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH)
        self.rect.y = GROUND_LEVEL - self.rect.height - 20  # Place booster slightly above the ground level

# Main game loop
def game_loop():
    running = True
    player = Player()
    all_sprites.add(player)

    level = 1
    enemies = pygame.sprite.Group()
    boosters = pygame.sprite.Group()

    def start_new_level():
        nonlocal level
        level += 1
        # Add more enemies for new levels
        for _ in range(5 + level * 2):
            enemy = Enemy()
            all_sprites.add(enemy)
            enemies.add(enemy)
        # Add a booster for every level
        booster = Booster()
        all_sprites.add(booster)
        boosters.add(booster)

    start_new_level()  # Start the first level

    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot()

        # Get key presses for player movement
        keys = pygame.key.get_pressed()
        player.move(keys)
        if keys[pygame.K_UP]:
            player.jump()

        # Update all sprites
        all_sprites.update()

        # Collision detection: projectiles hit enemies
        hits = pygame.sprite.groupcollide(projectiles, enemies, True, True)
        player.score += len(hits) * 10

        # Collision detection: player collects boosters
        booster_hits = pygame.sprite.spritecollide(player, boosters, True)
        for booster in booster_hits:
            player.health = min(100, player.health + 20)  # Health boost

        # Collision detection: player jumps on enemies or collides
        enemy_hits = pygame.sprite.spritecollide(player, enemies, False)
        for enemy in enemy_hits:
            if player.velocity_y > 0 and player.rect.bottom >= enemy.rect.top:
                player.is_jumping = False
                player.velocity_y = -10  # Bounce off enemy
                enemy.kill()
                player.score += 10
            else:
                # Player loses health if hit without jumping or shooting
                player.health -= 1
                if player.health <= 0:
                    draw_text(screen, "Game Over!", 50, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                    pygame.display.flip()
                    pygame.time.delay(3000)
                    running = False

        # Check if level is completed
        if len(enemies) == 0:
            draw_text(screen, f"Level {level} Completed!", 40, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
            pygame.display.flip()
            pygame.time.delay(2000)  # Show level completed message
            start_new_level()

        # Draw background
        screen.fill(BG_COLOR)

        # Draw all sprites
        all_sprites.draw(screen)

        # Draw Score and Health
        draw_text(screen, f"Score: {player.score}", 30, 70, 10)
        draw_text(screen, f"Health: {player.health}", 30, SCREEN_WIDTH - 100, 10)

        pygame.display.flip()

    pygame.quit()

def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, (0, 0, 0))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

# Groups for sprites
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
projectiles = pygame.sprite.Group()
boosters = pygame.sprite.Group()

# Start the game
if __name__ == "__main__":
    game_loop()
