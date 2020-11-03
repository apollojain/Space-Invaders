import pygame
import random

green = (0,200,0)
red = (200, 0, 0)
bright_green = (0,255,0)
white = (255, 255, 255)

pygame.font.init()
intro_font = pygame.font.SysFont('Arial', 60)
default_font = pygame.font.SysFont('Arial', 50)
score_font = pygame.font.SysFont('Arial', 10)

top_left = (60, 40)

hero_rocket_vel = -2
alien_rocket_vel = 2

class Alien:
    def __init__(self, game, x, y):
        self.x = x
        self.game = game
        self.y = y
        self.size = 30

    def draw(self):
        pygame.draw.rect(self.game.screen,
            (81, 43, 88),
            pygame.Rect(self.x, self.y, self.size, self.size))

        self.y += 0.05

    def maybeGenerateRocket(self, game):
        if random.randint(0, 10000) < 5:
            
            game.rockets.append(Rocket(game, self.x + self.size / 2, self.y + self.size, color=red, speed=alien_rocket_vel))

    
    def checkCollision(self, game):
        for rocket in game.rockets:
            if (rocket.color == green and
                    rocket.x < self.x + self.size and
                    rocket.x > self.x - self.size and
                    rocket.y < self.y + self.size and
                    rocket.y > self.y - self.size):

                game.rockets.remove(rocket)
                game.aliens.remove(self)
                game.score += 1

class Hero: 
    def __init__(self, game, x, y, width=16, height=10):
        self.x = x
        self.y = y
        self.game = game
        self.width = width
        self.height = height
    
    def draw(self):
        pygame.draw.rect(self.game.screen,
                         (210, 250, 251),
                         pygame.Rect(self.x, self.y, self.width, self.height))
    
    def checkCollision(self):
        for rocket in self.game.rockets:
            if (rocket.color == red and
                    rocket.x > self.x and
                    rocket.x < self.x + self.width and
                    rocket.y > self.y and
                    rocket.y < self.y + self.height):

                self.game.rockets.remove(rocket)
                self.game.lost = True

class Generator:
    def __init__(self, game):
        margin = 30
        width = 50
        for x in range(margin, game.width - margin, width):
            for y in range(margin, int(game.height / 2), width):
                game.aliens.append(Alien(game, x, y))

class Rocket:
    def __init__(self, game, x, y, color=green, speed=hero_rocket_vel):
        self.x = x
        self.y = y
        self.game = game
        self.color = color
        self.speed = speed
    
    def draw(self):
        pygame.draw.rect(self.game.screen,
                         self.color,
                         pygame.Rect(self.x, self.y, 2, 4))
        self.y += self.speed

class Game: 
    screen = None

    def __init__(self, width, height):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()

        self.intro = True
        def intro_false():
            self.intro = False

        while self.intro:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
            
            pygame.display.flip()
            self.clock.tick(60)
            self.screen.fill((0, 0, 0))
            self.displayText("SPACE INVADERS", font=intro_font, color=white)
            
            button_width = 80
            button_height = 30
            center_x = self.width / 2
            center_y = self.height / 2 + 100

            self.createButton(
                text="PLAY",
                left=center_x - button_width / 2,
                top=center_y - button_height / 2,
                width=button_width,
                height=button_height,
                initial_color=green,
                action_color=bright_green,
                action=intro_false
            )
        
        self.play_game()

    def play_game(self):

        self.aliens = []
        self.rockets = []
        self.lost = False
        self.score = 0

        done = False

        hero = Hero(self, self.width / 2, self.height - 20)
        generator = Generator(self)
        rocket = None

        button_width = 160
        button_height = 30
        center_x = self.width / 2
        center_y = self.height / 2 + 100

        while not done:

            if len(self.aliens) == 0:
                self.displayText("YOU WIN")

                self.createButton(
                    text="PLAY AGAIN",
                    left=center_x - button_width / 2,
                    top=center_y - button_height / 2,
                    width=button_width,
                    height=button_height,
                    initial_color=green,
                    action_color=bright_green,
                    action=self.play_game,
                )

            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_LEFT]:
                hero.x -= 2 if hero.x > 20 else 0
            elif pressed[pygame.K_RIGHT]:
                hero.x += 2 if hero.x < self.width - 20 else 0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True

                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.rockets.append(Rocket(self, hero.x + hero.width / 2, hero.y))
            
            pygame.display.flip()
            self.clock.tick(60)
            self.screen.fill((0, 0, 0))
            

            for alien in self.aliens:
                alien.draw()
                alien.checkCollision(self)
                if (alien.y + alien.size > hero.y):
                    self.lost = True
                    break
                alien.maybeGenerateRocket(self)

            if self.lost:
                self.displayText("GAME OVER")

                self.createButton(
                    text="PLAY AGAIN",
                    left=center_x - button_width / 2,
                    top=center_y - button_height / 2,
                    width=button_width,
                    height=button_height,
                    initial_color=green,
                    action_color=bright_green,
                    action=self.play_game,
                )

            for rocket in self.rockets: 
                rocket.draw()

            hero.checkCollision()
            if not self.lost: hero.draw()

            self.displayText("SCORE: {0}".format(self.score), font=score_font, color=white, center=top_left)
        
    def displayText(self, text, font=default_font, color = (44, 0, 62), center=None):
        if center == None:
            center = (self.width / 2, self.height / 2)

        textsurface = font.render(text, False, color)
        textrect = textsurface.get_rect(center=center)
        self.screen.blit(textsurface, textrect)

    def createButton(self, text, left, top, width, height, initial_color, action_color, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if left + width > mouse[0] > left and top + height > mouse[1] > top:
            pygame.draw.rect(self.screen, bright_green, (left,top,width,height))

            if click[0] == 1 and action != None:
                action()
        else:
            pygame.draw.rect(self.screen, initial_color, (left,top,width,height))
        
        font = pygame.font.SysFont('Arial', 25)
        textsurface = font.render(text, False, (44, 0, 62))
        self.screen.blit(textsurface, (left + 10, top))

if __name__ == '__main__':
    game = Game(600, 400)