import numpy as np
import pygame
import logging

from threading import Thread

from Board import Board

COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_BROWN = (205, 128, 0)
COLOR_BOARD = (118, 86, 153)


# https://stackoverflow.com/a/19846691/1781821
def threaded(fn):
    def wrapper(*args, **kwargs):
        Thread(target=fn, args=args, kwargs=kwargs, daemon=False).start()
    return wrapper


class BoardGUI:
    def __init__(self, board: Board, screen_size: int) -> None:
        self.board = board
        self.size = (screen_size, screen_size)
        self.line_spacing = self.size[0] / (self.board.dim + 1)
        self.surface = None
        self.stop_loop = False
        self.click_pos = None
        logging.basicConfig(filename='gui.log', level=logging.DEBUG)

    @threaded
    def start_gui(self) -> None:
        pygame.init()
        pygame.display.set_caption('Gomoku')
        self.surface = pygame.display.set_mode(self.size)
        logging.info('starting loop...')
        self.loop()

    def loop(self) -> None:
        while not self.stop_loop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.stop_loop = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.click_pos = pygame.mouse.get_pos()
            self.draw_board()
            self.draw_board_pieces()
            self.draw_game_over_message()
            pygame.display.flip()
        else:
            logging.info('stopping loop...')
            pygame.quit()

    def draw_board(self) -> None:
        self.surface.fill(COLOR_BOARD)
        for i in range(self.board.dim):
            pygame.draw.line(self.surface, COLOR_BLACK, ((i + 1) * self.line_spacing, 0), ((i + 1) * self.line_spacing, self.size[1]), 2)
            pygame.draw.line(self.surface, COLOR_BLACK, (0, (i + 1) * self.line_spacing), (self.size[1], (i + 1) * self.line_spacing), 2)

    def draw_board_pieces(self) -> None:
        black_positions, white_positions = self.board.get_positions()
        for pos in black_positions:
            pos += np.array([1, 1])
            pos = pos * self.line_spacing
            pygame.draw.circle(surface=self.surface, color=COLOR_BLACK, center=pos, radius=self.line_spacing / 3)
        for pos in white_positions:
            pos += np.array([1, 1])
            pos = pos * self.line_spacing
            pygame.draw.circle(surface=self.surface, color=COLOR_WHITE, center=pos, radius=self.line_spacing / 3)

    def draw_game_over_message(self) -> None:
        font = pygame.font.SysFont(pygame.font.get_default_font(), 30)
        text_surface = font.render(self.board.game_over_str, True, COLOR_WHITE)
        temp_surface = pygame.Surface(text_surface.get_size())
        temp_surface.fill(COLOR_BLACK)
        temp_surface.blit(text_surface, (0, 0))
        x = self.size[0] / 2 - temp_surface.get_width() / 2
        y = self.size[1] / 2 - temp_surface.get_height() / 2
        self.surface.blit(temp_surface, (x, y))
