import pygame
import os

# Инициализация звука
pygame.mixer.init()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SOUND_DIR = os.path.join(BASE_DIR, "sound")

shoot = None
win = None
lose = None


def bg_music():
    path = os.path.join(SOUND_DIR, "bg.mp3")
    if os.path.exists(path):
        pygame.mixer.music.load(path)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)


def stop_bg_music():
    pygame.mixer.music.stop()


def game_music():
    path = os.path.join(SOUND_DIR, "game.mp3")
    if os.path.exists(path):
        pygame.mixer.music.load(path)
        pygame.mixer.music.set_volume(0.6)
        pygame.mixer.music.play(-1)


def shoot_sound():
    global shoot
    path = os.path.join(SOUND_DIR, "shoot.wav")
    if os.path.exists(path):
        shoot = pygame.mixer.Sound(path)
        shoot.set_volume(0.7)


def play_shoot():
    if shoot:
        shoot.play()


def load_end_sounds():
    global win, lose

    win_path = os.path.join(SOUND_DIR, "win.wav")
    lose_path = os.path.join(SOUND_DIR, "lose.wav")

    if os.path.exists(win_path):
        win = pygame.mixer.Sound(win_path)
        win.set_volume(0.8)

    if os.path.exists(lose_path):
        lose = pygame.mixer.Sound(lose_path)
        lose.set_volume(0.8)


def play_win():
    if win:
        win.play()


def play_lose():
    if lose:
        lose.play()
