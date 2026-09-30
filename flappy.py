import random 
import pygame
import os
import time

BIRD_IMGS = [
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird1.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird2.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird3.png')))
]

BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'base.png')))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bg.png')))
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'pipe.png')))
WIN_HEIGHT = 800
WIN_WIDTH = 600


class Bird:
    MAX_ROTATION = 25
    ANIMATION_TIME = 5
    ROTATION_VEL = 10
    IMGS = BIRD_IMGS
    def __init__(self,x , y):
        self.x = x
        self.y = y
        self.vel = 0
        self.tilt = 0 
        self.tick = 0
        self.height = y
        self.img_count = 0
        self.img = self.IMGS[0]
    def jump(self):
        self.vel = -13
        self.height = self.y
        self.tick = 0

    def move(self, win: pygame.Surface):
        self.tick += 1 
        d = self.vel * self.tick + 1.5 * self.tick**2
        if d >= 16:
            d = 16
        if d < 0:
            d -= 2

        

        self.y = self.y + d


        if self.y < self.height + 50 or d < 0:
            if self.tilt <= self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
                
        else:
            if  self.tilt > -90:
                self.tilt -=  self.ROTATION_VEL

        # win.blit(source=self.img, dest=(self.x, self.y))
        print('tilt',self.tilt)


    def draw(self, win: pygame.Surface):
        self.img_count += 1

        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME *2:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME *3:
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME *4:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME *4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0

        if self.tilt <= - 80:
            self.img = self.IMGS[1]
            self.img_count =  self.ANIMATION_TIME *2
            
        rotated_img = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_img.get_rect(center=self.img.get_rect(topleft= (self.x, self.y)).center)
        win.blit(rotated_img, new_rect.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)


class Base:
    VEL = -5
    IMG = BASE_IMG

    def __init__(self, y) -> None:
       self.x1 = 0
       self.x2 = self.IMG.get_width()
       self.y = y 

    def move(self):
        self.x1 += self.VEL
        self.x2 += self.VEL

        if self.x1 <= -self.IMG.get_width():
            self.x1 = self.x2 + self.IMG.get_width()
        
        if self.x2 <= -self.IMG.get_width():
            self.x2 = self.x1 + self.IMG.get_width()
        
    def draw(self, win: pygame.Surface):
        win.blit(self.IMG, (self.x1, win.get_height() - self.y))
        win.blit(self.IMG, (self.x2, win.get_height() - self.y))
        
class Pipe:
    GAP = 200
    VEL = -5
    IMG = PIPE_IMG
    
    def __init__(self, x) -> None:
        assert isinstance(x, (int, float)), f"Expected int for x, got {type(x)}"
        self.x = x
        # self.y = random.randint()  
        self.y = random.randint(50 + self.GAP, WIN_HEIGHT - 5)
        self.img = self.IMG
        self.tick = 0
        self.PIPE_TOP = pygame.transform.flip(self.img, 0, 1)
        self.PIPE_BOTTOM = self.img
        self.top = 0
        self.bottom = 0
        self.set_height()
        self.passed = False

    def move(self):
        self.x += self.VEL

    def set_height(self):
        self.height = random.randrange(50,450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP


    def draw(self,  win: pygame.Surface):
        assert isinstance(win, pygame.Surface), f"expected win = pygame.Surface not {type(win)}"
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))
        
    def collide(self, bird: Bird):
        bird_mask = bird.get_mask()
        top_pipe_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_pipe_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        offset_top_pipe = (self.x - bird.x, self.top - round(bird.y))
        offset_bottom_pipe = (self.x - bird.x, self.bottom - round(bird.y))

        t_point = bird_mask.overlap(top_pipe_mask, offset_top_pipe)
        b_point = bird_mask.overlap(bottom_pipe_mask, offset_bottom_pipe)

        if t_point or b_point:
            return True
        else:
            return False
        
def draw_window(win, bird, pipes):
    win.blit(BG_IMG, (0,0))
    for pipe in pipes:
        pipe.draw(win)
        
    bird.draw(win)    


def temp():
    pipe = Pipe(200)

if __name__  == '__main__':
    bird = Bird(200,200)
    base = Base(50)
    count = 0
    pygame.init()
    screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()
    running = True
    pipes = []

    while running:
        count += 1 
        
        print('count', count)
        
        
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                     bird.jump()
            if event.type == pygame.QUIT:
                        running = False
        # fill the screen with a color to wipe away anything from last frame
        # pygame.draw(BIRD_IMGS)
        # screen.fill("purple")    
        draw_window(screen, bird, pipes)
        base.draw(screen)
        base.move()
        bird.move(screen)
        # pipe.draw(screen)   
        for pipe in pipes:
            pipe.move()
                    
        
        if count == 50:
            pipe = Pipe(WIN_WIDTH)
            pipes.append(pipe)
            count = 0

       
       

        # RENDER YOUR GAME HERE

        
        # flip() the display to put your work on screen
        pygame.display.flip()

        clock.tick(30)  # limits FPS to 60

    pygame.quit()
