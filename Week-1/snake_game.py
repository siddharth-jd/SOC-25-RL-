import pygame, sys, random
from pygame.math import Vector2

class Button:
    def __init__(self, text, x, y, width, height, color, text_color, font):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text
        self.text_color = text_color
        self.font = font
        self.text_surface = font.render(text, True, text_color)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        surface.blit(self.text_surface, self.text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

class SNAKE:
    def __init__(self):
        self.body = [Vector2(9,10), Vector2(8,10), Vector2(7,10), Vector2(6,10), Vector2(5,10)]
        self.direction = Vector2(0,0)
        self.new_block = False

    def draw_snake(self):
        for block in self.body:
            block_rect = pygame.Rect(int(block.x * cell_size), int(block.y * cell_size), cell_size, cell_size)
            pygame.draw.rect(screen, (80, 80, 200), block_rect)

    def move_snake(self):
        if self.new_block:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

    def add_block(self):
        self.new_block = True

    def reset(self):
        self.__init__()

class Apple:
    def __init__(self):
        self.randomize()

    def draw_apple(self):
        apple_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        screen.blit(apple_img, apple_rect)

    def randomize(self):
        self.pos = Vector2(random.randint(0, cell_number - 1), random.randint(0, cell_number - 1))

class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.apple = Apple()

    def update(self):
        self.snake.move_snake()
        self.collision()
        self.lost()

    def elements(self):
        self.draw_grass()
        self.apple.draw_apple()
        self.snake.draw_snake()
        self.draw_score()

    def collision(self):
        if self.apple.pos == self.snake.body[0]:
            self.apple.randomize()
            self.snake.add_block()

    def lost(self):
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.gameover()
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.gameover()

    def gameover(self):
        global game_state
        game_state = 'end'

    def draw_grass(self):
        grass_color = (34, 139, 34)
        for row in range(cell_number):
            for col in range(cell_number):
                if (row + col) % 2 == 0:
                    grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                    pygame.draw.rect(screen, grass_color, grass_rect)

    def draw_score(self):
        score = str(len(self.snake.body) - 5)
        score_text = game_font.render("Score : " + score, True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(550, 570))
        screen.blit(score_text, score_rect)


pygame.init()
cell_size = 20
cell_number = 30
screen = pygame.display.set_mode((cell_size * cell_number, cell_size * cell_number))
clock = pygame.time.Clock()
apple_img = pygame.image.load('apple.png').convert_alpha()
apple_img = pygame.transform.scale(apple_img, (20, 20))
game_font = pygame.font.SysFont(None, 25)
menu_font = pygame.font.SysFont(None, 50)

main_game = MAIN()
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 100)

game_state = 'start'

start_button = Button("START", 220, 250, 160, 60, (50, 100, 60), (255, 255, 255), menu_font)
end_button = Button("END", 160, 250, 100, 60, (220, 40, 20), (255, 255, 255), menu_font)
restart_button = Button("RESTART", 320, 250, 170, 60, (80, 40, 139), (255, 255, 255), menu_font)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if game_state == 'running':
            if event.type == SCREEN_UPDATE:
                main_game.update()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and main_game.snake.direction.y != 1:
                    main_game.snake.direction = Vector2(0, -1)
                if event.key == pygame.K_DOWN and main_game.snake.direction.y != -1:
                    main_game.snake.direction = Vector2(0, 1)
                if event.key == pygame.K_LEFT and main_game.snake.direction.x != 1:
                    main_game.snake.direction = Vector2(-1, 0)
                if event.key == pygame.K_RIGHT and main_game.snake.direction.x != -1:
                    main_game.snake.direction = Vector2(1, 0)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_state == 'start' and start_button.is_clicked(event.pos):
                game_state = 'running'
                main_game.snake.direction = Vector2(1, 0)
            if game_state == 'end':
                if end_button.is_clicked(event.pos):
                    pygame.quit()
                    sys.exit()
                if restart_button.is_clicked(event.pos):
                    main_game = MAIN()
                    game_state = 'start'

    screen.fill((0, 128, 0))

    if game_state == 'start':
        start_button.draw(screen)
    elif game_state == 'running':
        main_game.elements()
    elif game_state == 'end':
        end_button.draw(screen)
        restart_button.draw(screen)

    pygame.display.update()
    clock.tick(60)
