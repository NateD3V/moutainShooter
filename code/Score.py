import sys
from datetime import datetime

import pygame
from pygame import surface
from pygame.constants import KEYDOWN, K_RETURN, K_BACKQUOTE, K_BACKSLASH, K_BACKSPACE, K_ESCAPE
from pygame.font import Font
from pygame.rect import Rect
from pygame.surface import Surface

from code.Const import C_YELLOW, SCORE_POS, MENU_OPTION, C_WHITE
from code.DBProxy import DBProxy


class Score:
    def __init__(self, window: Surface):
        self.window = window
        self.surf = pygame.image.load('./asset/ScoreBg.png').convert_alpha()
        self.rect = self.surf.get_rect(left=0, top=0)

    def save(self, game_mode: str, player_score: list[int]):
        pygame.mixer_music.load('./asset/Score.mp3')
        pygame.mixer_music.play(-1)
        db_proxy = DBProxy('DbScore')
        name = ''
        while True:
            self.window.blit(source=self.surf, dest=self.rect)
            # Transparent surface for better visualization
            rect_width = 400
            rect_height = 300
            transparent_surface = pygame.Surface((rect_width, rect_height), pygame.SRCALPHA)
            transparent_surface.fill((50, 50, 50, 150))  # Cor com transparência ajustada #
            # rect center
            rect_x = (self.window.get_width() - rect_width) // 2
            rect_y = (self.window.get_height() - rect_height) // 2  # Blit a superfície transparente na janela principal
            self.window.blit(transparent_surface, (rect_x, rect_y))
            self.score_text(48, 'Você ganhou!', C_YELLOW, SCORE_POS['Title'])
            if game_mode == MENU_OPTION[0]:
                score = player_score[0]
                text = 'Player 1 digite seu nome (4 caracteres):'
            if game_mode == MENU_OPTION[1]:
                score = (player_score[0] + player_score[1]) / 2
                text = 'digite o nome do time (4 caracteres):'
            if game_mode == MENU_OPTION[2]:
                if player_score[0] >= player_score[1]:
                    score = max(player_score)
                    text = 'Player 1 digite seu nome (4 caracteres):'
                else:
                    score = max(player_score)
                    text = 'Player 2 digite seu nome (4 caracteres):'
            self.score_text(20, text, C_WHITE, SCORE_POS['EnterName'])
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_RETURN and len(name) == 4:
                        db_proxy.save({'name': name, 'score': score, 'date': get_formatted_date()})
                        self.show()
                        return
                    elif event.key == K_BACKSPACE:
                        name = name[:-1]
                    else:
                        if len(name) < 4:
                            name += event.unicode
            self.score_text(20, name, C_WHITE, SCORE_POS['Name'])
            pygame.display.flip()
            pass

    def show(self):
        pygame.mixer_music.load('./asset/Score.mp3')
        pygame.mixer_music.play(-1)
        self.window.blit(source=self.surf, dest=self.rect)

        # Transparent surface for better visualization
        rect_width = 400
        rect_height = 300
        transparent_surface = pygame.Surface((rect_width, rect_height), pygame.SRCALPHA)
        transparent_surface.fill((50, 50, 50, 150)) # Cor com transparência ajustada #
        # rect center
        rect_x = (self.window.get_width() - rect_width) // 2
        rect_y = (self.window.get_height() - rect_height) // 2 # Blit a superfície transparente na janela principal
        self.window.blit(transparent_surface, (rect_x, rect_y))

        self.score_text(48, 'TOP 10 SCORE', C_YELLOW, SCORE_POS['Title'])
        self.score_text(25, 'NAME     SCORE           DATE      ', C_YELLOW, SCORE_POS['Label'])
        db_proxy = DBProxy('DBScore')
        list_score = db_proxy.retrieve_top10()
        db_proxy.close()

        for player_score in list_score:
            id_,name, score, date = player_score
            self.score_text(22, f'{name}     {score:05d}     {date}', C_YELLOW,
                            SCORE_POS[list_score.index(player_score)])

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        return
            pygame.display.flip()


    def score_text(self, text_size: int, text: str, text_color: tuple, text_center_pos: tuple):
        text_font: Font = pygame.font.SysFont(name='lucida Sans Typewriter', size=text_size)
        text_surf: surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(center=text_center_pos)
        self.window.blit(source=text_surf, dest=text_rect)


def get_formatted_date():
    current_datetime = datetime.now()
    current_time = current_datetime.strftime("%H:%M")
    current_date = current_datetime.strftime("%d/%m/%y")
    return f"{current_time} - {current_date}"
