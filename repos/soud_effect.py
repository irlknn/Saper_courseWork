import pygame

def cliking():
    click = pygame.mixer.Sound("D:\\courseWork\\repos\\sounds\\clik.mp3")
    click.play()

def open_mine():
    open_mine = pygame.mixer.Sound("D:\\courseWork\\repos\\sounds\\mine_open.mp3")
    open_mine.play()

def win_sound():
    win_sound = pygame.mixer.Sound("D:\\courseWork\\repos\\sounds\\win_sound.mp3")
    win_sound.play()

def lose_sound():
    lose_sound = pygame.mixer.Sound("D:\\courseWork\\repos\\sounds\\losing_sound.mp3")
    lose_sound.play()

def arrow_slide():
    arrow_slide = pygame.mixer.Sound("D:\\courseWork\\repos\\sounds\\arrow_slide.mp3")
    arrow_slide.play()

