import pygame, sys, random

class Pipes:
    def __init__(self):
        self.pipe_list = []
        self.pipe_heights = [475, 350, 200]

    def create_pipe(self):
        random_y = random.choice(self.pipe_heights)
        bottom_pipe = pipe_image.get_rect(midtop = (700, random_y))
        top_pipe =  pipe_image.get_rect(midbottom = (700, random_y - 165))
        self.pipe_list.extend((bottom_pipe, top_pipe))        

    def move_pipe(self):
        for pipe in self.pipe_list:
            pipe.centerx -= 3

    def display_pipes(self):
        for pipe in self.pipe_list:
            if pipe.top < 0:
                reverse_pipe = pygame.transform.flip(pipe_image, False, True)
                screen.blit(reverse_pipe, pipe)                
            else:
                screen.blit(pipe_image, pipe)

    def check_bird_collision(self):
        for pipe in self.pipe_list:
            if bird.bird_rectangle.colliderect(pipe):
                return False
                # pass

        if bird.bird_rectangle.top < -30 or bird.bird_rectangle.top > 530:
            return False

        return True

class Bird:
    def __init__(self):
        self.bird_downflap = pygame.transform.scale(pygame.image.load('images/bluebird-downflap.png').convert_alpha(), (47, 33))
        self.bird_midflap = pygame.transform.scale(pygame.image.load('images/bluebird-midflap.png').convert_alpha(), (47, 33))
        self.bird_upflap = pygame.transform.scale(pygame.image.load('images/bluebird-upflap.png').convert_alpha(), (47, 33))
        self.wing_positions = [self.bird_downflap, self.bird_midflap, self.bird_upflap]
        self.bird_index = 0 
        self.bird_image = self.wing_positions[self.bird_index]
        self.bird_rectangle = self.bird_image.get_rect(center = (70, 350))

        self.bird_movement = 0

    def rotate_bird(self):
        new_bird = pygame.transform.rotozoom(self.bird_image, -self.bird_movement*3, 1)
        return new_bird

    def animate_bird(self):
        new_bird = self.wing_positions[self.bird_index]
        new_bird_rectangle = new_bird.get_rect(center = (70, self.bird_rectangle.centery))
        return new_bird, new_bird_rectangle


def display_ground():
    screen.blit(ground_image, (ground_x_position, 567))
    screen.blit(ground_image, (ground_x_position + 409 , 567))

def display_score(game_state):
    if game_state == "Game Running":
        score_text = game_font.render(str(int(score)), True, 'white')
        score_rectangle = score_text.get_rect(center = (200, 70))
        screen.blit(score_text, score_rectangle)
    else:
        score_text = game_font.render(f"Score: {int(score)}", True, 'white')
        score_rectangle = score_text.get_rect(center = (200, 70))
        screen.blit(score_text, score_rectangle)

        high_score_text = game_font.render(f"High Score: {int(high_score)}", True, 'white')
        high_score_rectangle = high_score_text.get_rect(center = (200, 110))
        screen.blit(high_score_text, high_score_rectangle)



pygame.init()
screen = pygame.display.set_mode((400, 700))
clock = pygame.time.Clock()

background_image = pygame.image.load('images/background-day.png').convert()
background_image = pygame.transform.scale(background_image, (400, 700))

ground_image = pygame.image.load('images/ground.png').convert()
ground_image = pygame.transform.scale(ground_image, (409, 201))
ground_x_position = 0

pipe_image = pygame.image.load('images/pipe-green.png').convert()
pipe_image = pygame.transform.scale(pipe_image, (72, 438))
pipes = Pipes()

gravity = 0.25
bird = Bird()

BIRD_FLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRD_FLAP, 200)

SPAWN_PIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWN_PIPE, 1200)

game_running = True

score = len(pipes.pipe_list)
high_score = 0

game_font = pygame.font.Font('04B_19.ttf', 40)

game_menu_image = pygame.image.load('images/game_menu.png').convert()
# game_menu_rectangle = game_menu_image.get_rect(center = )


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird.bird_movement = 0
                bird.bird_movement -= 9
            if event.key == pygame.K_SPACE and game_running == False:
                game_running = True
                pipes.pipe_list.clear()
                bird.bird_rectangle.center = (70, 350)
                bird.bird_movement = 0 


        if event.type == SPAWN_PIPE:
            pipes.create_pipe()

        if event.type == BIRD_FLAP:
            if bird.bird_index == 2:
                bird.bird_index = 0
            else:
                bird.bird_index += 1

            bird.bird_image, bird.bird_rectangle = bird.animate_bird()


    screen.blit(background_image, (0, 0))

    if game_running:
        bird.bird_movement += gravity
        rotated_bird = bird.rotate_bird()
        bird.bird_rectangle.centery += bird.bird_movement
        screen.blit(rotated_bird, bird.bird_rectangle)
        game_running = pipes.check_bird_collision()

        pipes.move_pipe()
        pipes.display_pipes()

        score = (len(pipes.pipe_list) / 2) - 1

        if score < 0:
            score = 0

        if score > high_score:
            high_score = score

        # score += 0.01
        display_score("Game Running")
    else:
        display_score("Game Over")
    
    display_ground()
    ground_x_position -= 1
    if ground_x_position < -400:
        ground_x_position = 0    

    pygame.display.update()
    clock.tick(120)