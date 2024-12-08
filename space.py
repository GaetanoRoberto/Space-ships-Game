import pygame
import random
import time

# Inizializza Pygame
pygame.init()

# Imposta le dimensioni della finestra
WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")

# Colori
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Carica immagini
player_img = pygame.image.load("img/player.png")
enemy_img = pygame.image.load("img/enemy.png")
bullet_img = pygame.image.load("img/bullet.png")
enemy_bullet_img = pygame.image.load("img/bullet2.png")
# background_img = pygame.Surface((WIDTH, HEIGHT))
# background_img.fill(BLACK)
background_img = pygame.image.load("img/bg.png").convert_alpha()
# Ridimensiona l'immagine dello sfondo dell'arena
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

# Dimensioni del giocatore e nemici
PLAYER_WIDTH, PLAYER_HEIGHT = 50, 50
ENEMY_WIDTH, ENEMY_HEIGHT = 40, 40

# Classe Giocatore
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        self.speed = 5
        self.bullets = []
        self.last_shot = 0
        self.lives = 3

    def draw(self):
        win.blit(player_img, (self.x, self.y))
        for bullet in self.bullets:
            bullet.draw()

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.x - self.speed > 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x + self.speed < WIDTH - self.width:
            self.x += self.speed
        if keys[pygame.K_SPACE]:
            self.shoot()

    def shoot(self):
        current_time = time.time()
        if len(self.bullets) < 1 and current_time - self.last_shot > 0.5:
            bullet = Bullet(self.x + self.width // 2 - 5, self.y)
            self.bullets.append(bullet)
            self.last_shot = current_time
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
# Classe Nemico
class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = ENEMY_WIDTH
        self.height = ENEMY_HEIGHT
        self.speed = 2
        self.move_counter = 0
        self.direction = 1  # Direzione iniziale
        self.shoot_chance = 0.005  # Probabilità di sparare ridotta

    def draw(self):
        win.blit(enemy_img, (self.x, self.y))

    def move(self):
        if self.move_counter < 50:
            self.x += self.speed * self.direction
            self.move_counter += 1
        else:
            self.direction *= -1
            self.move_counter = 0

    def shoot(self):
        if random.random() < self.shoot_chance:  # Sparo casuale
            return Bullet(self.x + self.width // 2 - 5, self.y + self.height, is_enemy=True)
        return None

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

# Classe Proiettile
class Bullet:
    def __init__(self, x, y, is_enemy=False):
        self.x = x
        self.y = y
        self.speed = 7 if not is_enemy else -5
        self.is_enemy = is_enemy
        self.width = 10
        self.height = 20

    def draw(self):
        if self.is_enemy:
            win.blit(enemy_bullet_img, (self.x, self.y))
        else:
            win.blit(bullet_img, (self.x, self.y))

    def move(self):
        self.y -= self.speed


    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width + 20, self.height)


# Funzione per disegnare tutto
def draw_game(player, enemies, enemy_bullets, score):
    win.blit(background_img, (0, 0))

    player.draw()
    for enemy in enemies:
        enemy.draw()
    for bullet in enemy_bullets:
        bullet.draw()
    draw_ui(player.lives, score)
    pygame.display.update()

# Funzione per disegnare la barra della vita e il punteggio
def draw_ui(lives, score):
    pygame.draw.rect(win, RED, (10, 10, 150, 20))
    pygame.draw.rect(win, GREEN, (10, 10, 50 * lives, 20))
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, WHITE)
    win.blit(score_text, (WIDTH - 150, 10))

# Funzione del menu iniziale
def main_menu(message="Press ENTER to Start"):
    title_font = pygame.font.Font(None, 74)
    instruction_font = pygame.font.Font(None, 36)
    
    run = True
    while run:
        win.fill(BLACK)
        title_text = title_font.render("Space Invaders", True, WHITE)
        instruction_text = instruction_font.render(message, True, WHITE)
        
        win.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 3))
        win.blit(instruction_text, (WIDTH // 2 - instruction_text.get_width() // 2, HEIGHT // 2))
        
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return

# Funzione principale
def main():
    clock = pygame.time.Clock()
    player = Player(WIDTH // 2, HEIGHT - 60)
    enemies = [Enemy(x, 100) for x in range(100, WIDTH - 100, 60)]
    enemy_bullets = []
    score = 0
    run = True

    while run:
        clock.tick(60)

        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        player.move(keys)

        # Aggiorna posizione proiettili del giocatore
        for bullet in player.bullets[:]:
            bullet.move()
            if bullet.y < 0:
                player.bullets.remove(bullet)

        # Movimento e gestione collisioni nemici
        for enemy in enemies[:]:
            enemy.move()
            enemy_bullet = enemy.shoot()
            if enemy_bullet:
                enemy_bullets.append(enemy_bullet)

            # Collisione tra proiettile del giocatore e nemico
            for bullet in player.bullets[:]:
                if bullet.get_rect().colliderect(enemy.get_rect()):
                    player.bullets.remove(bullet)
                    enemies.remove(enemy)
                    score += 10

        # Aggiorna posizione proiettili nemici
        for bullet in enemy_bullets[:]:
            bullet.move()
            if bullet.y > HEIGHT:
                enemy_bullets.remove(bullet)
            if player.get_rect().colliderect(bullet.get_rect()):
                player.lives -= 1
                enemy_bullets.remove(bullet)

            # Collisione tra proiettile nemico e proiettile giocatore
            for player_bullet in player.bullets[:]:
                if bullet.get_rect().colliderect(player_bullet.get_rect()):
                    enemy_bullets.remove(bullet)
                    player.bullets.remove(player_bullet)

        # Controllo fine partita
        if player.lives <= 0:
            main_menu("Game Over! Press ENTER to Restart")
            return

        if not enemies:
            main_menu("You won!!! Press ENTER to Restart")
            return

        draw_game(player, enemies, enemy_bullets, score)

if __name__ == "__main__":
    main_menu()
    while True:
        main()
