import pygame

# Farben definieren
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Fenstergröße
WIDTH = 800
HEIGHT = 600

# Spielergröße
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 100

# Schlagreichweite
PUNCH_RANGE = 900
PUNCH_FORCE = 30

# Schwerkraft
GRAVITY = 1

# Initialisierung von Pygame
pygame.init()

# Fenster erstellen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("KnockOff")

clock = pygame.time.Clock()

# Spielerklasse
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, controls):
        super().__init__()
        self.image = pygame.Surface([PLAYER_WIDTH, PLAYER_HEIGHT])
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_x = 0
        self.vel_y = 0
        self.score = 0
        self.controls = controls
        self.punching = False
        self.punch_animation = False
        self.punch_animation_frame = 0

    def update(self, platforms):
        self.vel_y += GRAVITY  # Schwerkraft
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

        # Kollision mit dem Boden überprüfen
        if self.rect.y >= HEIGHT - PLAYER_HEIGHT:
            self.rect.y = HEIGHT - PLAYER_HEIGHT
            self.vel_y = 0

        # Kollision mit den Plattformen überprüfen
        platform_hit_list = pygame.sprite.spritecollide(self, platforms, False)
        for platform in platform_hit_list:
            if self.vel_y > 0 and self.rect.bottom < platform.rect.bottom:
                self.rect.y = platform.rect.y - PLAYER_HEIGHT
                self.vel_y = 0

        # Kollision mit anderen Spielern überprüfen
        for player in players:
            if player != self:
                if pygame.sprite.collide_rect(self, player):
                    if self.punching and not player.punch_animation:

                        player.punch_animation = True
                        # Spieler bekommt Rückstoß
                        print(str(self.vel_y), str(self.vel_x))
                        self.vel_y = +PUNCH_FORCE // 2
                        self.vel_x = +PUNCH_FORCE // 2 
                        self.update()
 
                            
                        print(str(self.vel_y), str(self.vel_x))
                        

    def reset_position(self):
        # Zurück zur Plattform teleportieren
        self.rect.x = WIDTH // 2 - PLAYER_WIDTH // 2
        self.rect.y = HEIGHT // 2 - PLAYER_HEIGHT // 2 - 150

        # Punkte vergeben
        for player in players:
            if player != self:
                player.score += 1

# Plattformklasse
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Spielergruppen erstellen
all_sprites = pygame.sprite.Group()
players = pygame.sprite.Group()
platforms = pygame.sprite.Group()

# Spieler erstellen
player1 = Player(WIDTH // 2 - PLAYER_WIDTH // 2, HEIGHT - PLAYER_HEIGHT, {"left": pygame.K_a, "right": pygame.K_d, "jump": pygame.K_w, "punch": pygame.K_m})
player2 = Player(WIDTH // 2 - PLAYER_WIDTH // 2, HEIGHT - PLAYER_HEIGHT, {"left": pygame.K_LEFT, "right": pygame.K_RIGHT, "jump": pygame.K_UP, "punch": pygame.K_SPACE})

# Plattform erstellen
platform_width = 600
platform_height = 20
platform = Platform(WIDTH // 2 - platform_width // 2, HEIGHT // 2 - platform_height // 2, platform_width, platform_height)

# Spieler zur Gruppe hinzufügen
all_sprites.add(player1)
all_sprites.add(player2)
players.add(player1)
players.add(player2)

# Plattform zur Gruppe hinzufügen
all_sprites.add(platform)
platforms.add(platform)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Tastatureingaben abfragen
    keys = pygame.key.get_pressed()
    for player in players:
        if keys[player.controls["left"]]:
            player.vel_x = -5
        elif keys[player.controls["right"]]:
            player.vel_x = 5
        else:
            player.vel_x = 0
        if keys[player.controls["jump"]] and player.rect.y == 190:
            player.vel_y = -15

        if keys[player.controls["punch"]]:
            player.punching = True
            player.punch_animation_frame = 0
        else:
            player.punching = False

    # Spieler und Plattformen aktualisieren
    all_sprites.update(platforms)

    # Kollision zwischen Spielern und Plattform überprüfen
    for player in players:
        if player.rect.y >= HEIGHT - PLAYER_HEIGHT:
            player.reset_position()

    # Fenster leeren
    screen.fill(WHITE)

    # Alle Sprites zeichnen
    all_sprites.draw(screen)

    # Punktestand anzeigen
    font = pygame.font.Font(None, 36)
    score_text = font.render("Punktestand: {} - {}".format(player1.score, player2.score), True, BLACK)
    score_rect = score_text.get_rect(center=(WIDTH // 2, 20))
    screen.blit(score_text, score_rect)

    # Schlaganimation anzeigen
    for player in players:
        if player.punch_animation:
            player.punch_animation_frame += 1
            if player.punch_animation_frame >= 30:
                player.punch_animation_frame = 0
                player.punch_animation = False
            elif player.rect.x < WIDTH // 2:
                pygame.draw.line(screen, BLACK, (player.rect.x + PLAYER_WIDTH, player.rect.y + PLAYER_HEIGHT // 2), (player.rect.x + PLAYER_WIDTH + player.punch_animation_frame, player.rect.y + PLAYER_HEIGHT // 2), 5)
            else:
                pygame.draw.line(screen, BLACK, (player.rect.x, player.rect.y + PLAYER_HEIGHT // 2), (player.rect.x - player.punch_animation_frame, player.rect.y + PLAYER_HEIGHT // 2), 5)

    # Fenster aktualisieren
    pygame.display.flip()
    clock.tick(60)

# Pygame beenden
pygame.quit()
