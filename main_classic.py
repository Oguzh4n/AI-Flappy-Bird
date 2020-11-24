import pygame
import sys
import random

#-----------------------------------The classic Game without NEAT-------------------------------------------------

class FlappyBird:
    def __init__(self):
        self.screen = pygame.display.set_mode((576, 1024))
        self.BG_SURFACE = pygame.transform.scale2x(pygame.image.load("IMG/background-day.png").convert())
        self.bird_frames = [pygame.transform.scale2x(pygame.image.load("IMG/bluebird-downflap.png").convert_alpha()),
                            pygame.transform.scale2x(pygame.image.load("IMG/bluebird-midflap.png").convert_alpha()),
                            pygame.transform.scale2x(pygame.image.load("IMG/bluebird-upflap.png").convert_alpha())]
        self.PIPE_BOTTOM = pygame.transform.scale2x(pygame.image.load("IMG/pipe-green.png").convert())
        self.PIPE_TOP = pygame.transform.flip(self.PIPE_BOTTOM, False, True)
        self.FLOOR_SURFACE = pygame.transform.scale2x(pygame.image.load("IMG/base.png").convert())
        self.bird_index = 0
        self.BIRD_SURFACE = self.bird_frames[self.bird_index]
        self.bird_rect = self.BIRD_SURFACE.get_rect(center = (100, 512))
        self.BIRDFLAP = pygame.USEREVENT + 1  # +1 because we have one event already
        pygame.time.set_timer(self.BIRDFLAP, 200)

        self.gravity = 0.25
        self.game_active = True
        self.dead = False
        self.offset = random.randint(-200, 200)
        self.floor_x_position = 0

        self.pipe_list = []
        self.SPAWNPIPE = pygame.USEREVENT
        pygame.time.set_timer(self.SPAWNPIPE, 1200)
        self.pipe_height = [400, 600, 800]

        self.game_active = True
        self.bird_movement = 0
        self.score = 0
        self.high_score = 0
        self.gravity = 0.35

        self.GAME_OVER_SURFACE = pygame.transform.scale2x(pygame.image.load("IMG/message.png").convert_alpha())
        self.game_over_rect = self.GAME_OVER_SURFACE.get_rect(center=(288, 512))

    def isDead(self):
        return self.dead

    def totalDistance(self):
        return self.distance

    def draw_floor(self):
        self.screen.blit(self.FLOOR_SURFACE, (self.floor_x_position, 900))
        self.screen.blit(self.FLOOR_SURFACE, (self.floor_x_position + 576, 900))

    def create_pipe(self):
        random_pipe_position = random.choice(self.pipe_height)
        bottom_pipe = self.PIPE_BOTTOM.get_rect(midtop=(700, random_pipe_position))
        top_pipe = self.PIPE_TOP.get_rect(midbottom=(700, random_pipe_position - 300))
        return bottom_pipe, top_pipe

    def move_pipes(self, pipes):
        for pipe in pipes:
            pipe.centerx -= 5  # move pipes to left by 5
        return pipes

    def draw_pipes(self, pipes):
        for pipe in pipes:
            if pipe.bottom >= 1024:
                self.screen.blit(self.PIPE_BOTTOM, pipe)
            else:
                self.screen.blit(self.PIPE_TOP, pipe)

    def check_collision(self, pipes):
        for pipe in pipes:
            if self.bird_rect.colliderect(pipe):  # check if any of the pipe rect is colliding with the bird rect
                return False

        if self.bird_rect.top <= -100 or self.bird_rect.bottom >= 900:  # check if bird too high or too low
            return False
        return True

    def rotate_bird(self, bird):
        new_bird = pygame.transform.rotozoom(bird, self.bird_movement*3, 1)
        return new_bird

    def bird_animation(self):
        new_bird = self.bird_frames[self.bird_index]
        new_bird_rect = new_bird.get_rect(center=(100, self.bird_rect.centery))  # take centery from previouse bird rect
        return new_bird, new_bird_rect

    def score_display(self, game_state, font):
        if game_state == "main_game":
            score_surface = font.render(str(int(self.score)), True, (255, 255, 255))
            score_rect = score_surface.get_rect(center=(288, 100))
            self.screen.blit(score_surface, score_rect)
        if game_state == "game_over":
            score_surface = font.render(f"Score: {int(self.score)}", True, (255, 255, 255))
            score_rect = score_surface.get_rect(center=(288, 100))
            self.screen.blit(score_surface, score_rect)

            high_score_surface = font.render(f"High Score: {int(self.high_score)}", True, (255, 255, 255))
            high_score_rect = high_score_surface.get_rect(center=(288, 850))
            self.screen.blit(high_score_surface, high_score_rect)

    def update_score(self, score, high_score):
        if score > high_score:
            high_score = score
        return high_score



    def run(self):
        pygame.init()
        game_font = pygame.font.SysFont("04B_19.TTF", 50)
        clock = pygame.time.Clock()
        pygame.font.init()


        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and self.game_active:
                        self.bird_movement = 0  # else the bird will fly to high
                        self.bird_movement -= 12
                    if event.key == pygame.K_SPACE and self.game_active == False:
                        self.game_active = True
                        self.pipe_list.clear()
                        self.bird_rect.center = (100, 512)
                        self.bird_movement = 0
                        self.score = 0
                if event.type == self.SPAWNPIPE:
                    self.pipe_list.extend(self.create_pipe())  # create pipes and put them in pipe_list
                if event.type == self.BIRDFLAP:
                    if self.bird_index < 2:
                        self.bird_index += 1
                    else:
                        self.bird_index = 0

                    self.BIRD_SURFACE, self.bird_rect = self.bird_animation()  # takes item from bird_frames and puts frame around it

            self.screen.blit(self.BG_SURFACE, (0, 0))

            if self.game_active:
                #Bird
                self.bird_movement += self.gravity
                rotated_bird = self.rotate_bird(self.BIRD_SURFACE)  # take oroginal bird surface rotate it and make new surface
                self.bird_rect.centery += self.bird_movement
                self.screen.blit(rotated_bird, (self.bird_rect))
                self.game_active = self.check_collision(self.pipe_list)  # if false bird and pipe loop will stop

                # Pipes
                self.pipe_list = self.move_pipes(self.pipe_list)  # move pipes and override the pipelist
                self.draw_pipes(self.pipe_list)

                self.score += 0.005
            else:
                self.screen.blit(self.GAME_OVER_SURFACE, self.game_over_rect)
                self.high_score = self.update_score(self.score, self.high_score)
                self.score_display("game_over", game_font)

            #Floor
            self.floor_x_position -= 1
            self.draw_floor()
            if self.floor_x_position <= -576:
                self.floor_x_position = 0

            pygame.display.update()
            clock.tick(120)  # framerate


if __name__ == "__main__":
    FlappyBird().run()