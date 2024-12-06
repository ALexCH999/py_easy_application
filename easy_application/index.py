#! /usr/bin/env python3


import math
import os
from random import randint
from collections import deque

import pygame
from pygame.locals import *


FPS = 60
ANIMATION_SPEED = 0.18  
WIN_WIDTH = 284 * 2     
WIN_HEIGHT = 512


class Bird(pygame.sprite.Sprite):
    
    WIDTH = HEIGHT = 32
    SINK_SPEED = 0.20
    CLIMB_SPEED = 0.25
    CLIMB_DURATION = 230.3

    def __init__(self, x, y, msec_to_climb, images):
        
        super(Bird, self).__init__()
        self.x, self.y = x, y
        self.msec_to_climb = msec_to_climb
        self._img_wingup, self._img_wingdown = images
        self._mask_wingup = pygame.mask.from_surface(self._img_wingup)
        self._mask_wingdown = pygame.mask.from_surface(self._img_wingdown)

    def update(self, delta_frames=1):
       
        if self.msec_to_climb > 0:
            frac_climb_done = 1 - self.msec_to_climb/Bird.CLIMB_DURATION
            self.y -= (Bird.CLIMB_SPEED * frames_to_msec(delta_frames) *
                       (1 - math.cos(frac_climb_done * math.pi)))
            self.msec_to_climb -= frames_to_msec(delta_frames)
        else:
            self.y += Bird.SINK_SPEED * frames_to_msec(delta_frames)

    @property
    def image(self):
       
        if pygame.time.get_ticks() % 500 >= 250:
            return self._img_wingup
        else:
            return self._img_wingdown

    @property
    def mask(self):
        
        if pygame.time.get_ticks() % 500 >= 250:
            return self._mask_wingup
        else:
            return self._mask_wingdown

    @property
    def rect(self):
       
        return Rect(self.x, self.y, Bird.WIDTH, Bird.HEIGHT)


class PipePair(pygame.sprite.Sprite):
   
    WIDTH = 80
    PIECE_HEIGHT = 52
    ADD_INTERVAL = 3000

    def __init__(self, pipe_end_img, pipe_body_img):
        
        self.x = float(WIN_WIDTH - 1)
        self.score_counted = False

        self.image = pygame.Surface((PipePair.WIDTH, WIN_HEIGHT), SRCALPHA)
        self.image.convert()   # speeds up blitting
        self.image.fill((0, 0, 0, 0))
        total_pipe_body_pieces = int(
            (WIN_HEIGHT -                  # fill window from top to bottom
             3 * Bird.HEIGHT -             # make room for bird to fit through
             3 * PipePair.PIECE_HEIGHT) /  # 2 end pieces + 1 body piece
            PipePair.PIECE_HEIGHT          # to get number of pipe pieces
        )
        self.bottom_pieces = randint(1, total_pipe_body_pieces)
        self.top_pieces = total_pipe_body_pieces - self.bottom_pieces

        # bottom pipe
        for i in range(1, self.bottom_pieces + 1):
            piece_pos = (0, WIN_HEIGHT - i*PipePair.PIECE_HEIGHT)
            self.image.blit(pipe_body_img, piece_pos)
        bottom_pipe_end_y = WIN_HEIGHT - self.bottom_height_px
        bottom_end_piece_pos = (0, bottom_pipe_end_y - PipePair.PIECE_HEIGHT)
        self.image.blit(pipe_end_img, bottom_end_piece_pos)

        # top pipe
        for i in range(self.top_pieces):
            self.image.blit(pipe_body_img, (0, i * PipePair.PIECE_HEIGHT))
        top_pipe_end_y = self.top_height_px
        self.image.blit(pipe_end_img, (0, top_pipe_end_y))

        # compensate for added end pieces
        self.top_pieces += 1
        self.bottom_pieces += 1

        # for collision detection
        self.mask = pygame.mask.from_surface(self.image)

    @property
    def top_height_px(self):
        return self.top_pieces * PipePair.PIECE_HEIGHT

    @property
    def bottom_height_px(self):
        return self.bottom_pieces * PipePair.PIECE_HEIGHT

    @property
    def visible(self):
        return -PipePair.WIDTH < self.x < WIN_WIDTH

    @property
    def rect(self):
        return Rect(self.x, 0, PipePair.WIDTH, PipePair.PIECE_HEIGHT)

    def update(self, delta_frames=1):
        self.x -= ANIMATION_SPEED * frames_to_msec(delta_frames)

    def collides_with(self, bird):
        return pygame.sprite.collide_mask(self, bird)


def load_images():
    def load_image(img_file_name):
        file_name = os.path.join('.', 'images', img_file_name)
        img = pygame.image.load(file_name)
        img.convert()
        return img

    return {'background': load_image('background.png'),
            'pipe-end': load_image('pipe.png'),
            'pipe-body': load_image('pipe.png'),
            
            'bird-wingup': load_image('bird.png'),
            'bird-wingdown': load_image('bird.png')}


def frames_to_msec(frames, fps=FPS):
    return 750.0 * frames / fps


def msec_to_frames(milliseconds, fps=FPS):
    return fps * milliseconds / 750.0


def main():

    pygame.init()

    display_surface = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption('Flappy Bird Game')

    clock = pygame.time.Clock()
    score_font = pygame.font.SysFont(None, 32, bold=True)  # default font
    images = load_images()

    # the bird stays in the same x position, so bird.x is a constant
    # center bird on screen
    bird = Bird(50, int(WIN_HEIGHT/2 - Bird.HEIGHT/2), 2,
                (images['bird-wingup'], images['bird-wingdown']))


################################################################
    # Функция для чтения максимального счета из файла
    def read_highscore(filename):
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                return int(file.read().strip())
        return 0  # Если файл не существует, возвращаем 0

    # Функция для записи максимального счета в файл
    def write_highscore(filename, score):
        with open(filename, 'w') as file:
            file.write(str(score))



    pipes = deque()

    frame_clock = 0  # this counter is only incremented if the game isn't paused
    score = 0
    max_score = read_highscore('highscore.txt')  # Читаем максимальный счет из файла
    done = paused = False
    while not done:
        clock.tick(FPS)

        # Handle this 'manually'.  If we used pygame.time.set_timer(),
        # pipe addition would be messed up when paused.
        if not (paused or frame_clock % msec_to_frames(PipePair.ADD_INTERVAL)):
            pp = PipePair(images['pipe-end'], images['pipe-body'])
            pipes.append(pp)

        for e in pygame.event.get():
            if e.type == QUIT or (e.type == KEYUP and e.key == K_ESCAPE):
                done = True
                break
            elif e.type == KEYUP and e.key in (K_PAUSE, K_p):
                paused = not paused
            elif e.type == MOUSEBUTTONUP or (e.type == KEYUP and
                    e.key in (K_UP, K_RETURN, K_SPACE)):
                bird.msec_to_climb = Bird.CLIMB_DURATION

        if paused:
            continue  # don't draw anything

        # check for collisions
        pipe_collision = any(p.collides_with(bird) for p in pipes)
        if pipe_collision or 0 >= bird.y or bird.y >= WIN_HEIGHT - Bird.HEIGHT:
            done = True

        for x in (0, WIN_WIDTH / 2):
            display_surface.blit(images['background'], (x, 0))

        while pipes and not pipes[0].visible:
            pipes.popleft()

        for p in pipes:
            p.update()
            display_surface.blit(p.image, p.rect)

        bird.update()
        display_surface.blit(bird.image, bird.rect)

        # update and display score
        for p in pipes:
            if p.x + PipePair.WIDTH < bird.x and not p.score_counted:
                score += 1
                p.score_counted = True
                ##################

        # Обновление максимального счета
        if score > max_score:
            max_score = score
            write_highscore('highscore.txt', max_score)  # Записываем новый максимальный счет в файл

        score_surface = score_font.render(str(score), True, (255, 255, 255))
        score_x = WIN_WIDTH / 2 - score_surface.get_width() / 2
        display_surface.blit(score_surface, (score_x, PipePair.PIECE_HEIGHT))

        pygame.display.flip()
        frame_clock += 1

        # Здесь выводим результаты после завершения игры
    display_surface.fill((0, 0, 0))  # Заполняем экран черным цветом
    game_over_surface = score_font.render('Game Over!', True, (255, 0, 0))
    max_score_surface = score_font.render(f'Max Score: {max_score}', True, (255, 255, 255))

    display_surface.blit(game_over_surface, (WIN_WIDTH / 2 - game_over_surface.get_width() / 2, WIN_HEIGHT / 2 - 30))
    display_surface.blit(max_score_surface, (WIN_WIDTH / 2 - max_score_surface.get_width() / 2, WIN_HEIGHT / 2 + 10))

    pygame.display.flip()

    # Ждем некоторое время перед выходом или до нажатия клавиши
    pygame.time.delay(3000)  # Задержка в 3 секунды перед закрытием окна

    print('Game over! Score: %i' % score, 'max score: %i' % max_score)
    pygame.quit()


if __name__ == '__main__':
    # If this module had been imported, __name__ would be 'flappybird'.
    # It was executed (e.g. by double-clicking the file), so call main.
    main()
