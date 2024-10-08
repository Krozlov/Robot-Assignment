import pygame
import random
import sys

#Initialize Pygame
pygame.init()

#Set up the screen
SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Star Shooter Game | Press 'R' to Reset, 'Q' to Quit")

#Define Colors
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
BLACK = (0,0,0)

# Set Up Fonts
font = pygame.font.SysFont(None, 36)
small_font = pygame.font.SysFont (None, 24)

# Set up clock
clock = pygame.time.Clock()

# Define classes
class Robot(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50,50))
        self.image.fill (GREEN)
        pygame.draw.rect(self.image, GREEN, (0,0,50,10))
        self.rect = self.image.get_rect ()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 10
        self.speed = 8

    def update(self):
        keys = pygame.key.get_pressed()
        if keys [pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys [pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys [pygame.K_UP]:
            self.rect.y -= self.speed
        if keys [pygame.K_DOWN]:
            self.rect.y += self.speed

        # Keep the shooter within the screen
        self.rect.clamp_ip(screen.get_rect())


# Create class for Target
class Cell (pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50,50))
        self.image.fill(YELLOW)
        pygame.draw.polygon(self.image, WHITE, [(25,0), (40, 40), (10,20)])
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange (0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = -self.rect.height
        self.speed = 6

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > SCREEN_HEIGHT:
            self.kill()


# Create class for Hazards
class Hazard (pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50,50))
        self.image.fill (RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange (0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = -self.rect.height
        self.speed = 6

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > SCREEN_HEIGHT:
            self.kill()

# Create class for Battery
class Battery (pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50,50))
        self.image.fill (BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange (0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = -self.rect.height
        self.speed = 6
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > SCREEN_HEIGHT:
            self.kill()

# Set up sprite groups
all_sprites = pygame.sprite.Group()
cells = pygame.sprite.Group()
hazards = pygame.sprite.Group()
batteries = pygame.sprite.Group()


# Create the Robot
robot = Robot()
all_sprites.add(robot)


# Set up game variables
score = 0
game_over = False
start_time = pygame.time.get_ticks()
game_duration = 15000
battery_start = 15000


# Main game Loop
while True:
    #Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                # Reset the game
                score = 0
                game_over = False
                start_time = pygame.time.get_ticks()
                all_sprites.empty()
                cells.empty()
                hazards.empty() 
                batteries.empty()

                # Recreate the robot 
                robot = Robot()
                all_sprites.add (robot)
            elif event.key == pygame.K_q:
                # Quit the game
                pygame.quit()
                sys.exit()     

    if not game_over:
        # Spawn batteries, cells  and obstacles
        if random.randrange(100) < 2:
            cell = Cell()
            all_sprites.add(cell)
            cells.add (cell)
        if random.randrange(100) < 2:
            hazard = Hazard()
            all_sprites.add(hazard)
            hazards.add(hazard)
        if random.randrange(100) < 2:
            battery = Battery()
            all_sprites.add(battery)
            batteries.add(battery)

        # Update sprites
        all_sprites.update()

        # Check for collisions between robot and hazard
        hits = pygame.sprite.spritecollide(robot, hazards, False)
        if hits:
            game_over = True   

        # Check for collisions between robot and cell
        hits = pygame.sprite.spritecollide(robot, cells, True)
        for hit in hits:
            score += 1
        
        #Check for collissions between robot and battery
        hits = pygame.sprite.spritecollide(robot, batteries, True)
        for hit in hits:
            battery_start += 2000
        
            
        # Draw everything
        screen.fill (BLACK)
        all_sprites.draw(screen)     

        # Display score 
        score_text = font.render ("Score: " + str(score), True, WHITE)
        screen.blit (score_text, (10,10))

        # Display battery remaining
        elapsed_time = pygame.time.get_ticks() - start_time
        battery_remaining = max(0, battery_start - pygame.time.get_ticks())
        battery_text = font.render ('Battery: ' + str(battery_remaining // 1000), True, WHITE)
        screen.blit (battery_text, (SCREEN_WIDTH - 170, 10))
       

        # Check if the battery is gone
        if battery_remaining == 0:
            game_over = True
    
    else:
        # Game over screen
        game_over_text = font.render ("Game Over", True, RED)
        screen.blit (game_over_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 20))
        final_score_text = font.render ("Final Score: " + str(score), True, WHITE)
        screen.blit (final_score_text, (SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 + 120))


    # Display instructions
    instructions_text = small_font.render("Press 'R' to Reset, 'Q' to Quit", True, WHITE)
    screen.blit (instructions_text, (SCREEN_WIDTH - 250, SCREEN_HEIGHT - 30))

    pygame.display.flip()
    clock.tick(60)
