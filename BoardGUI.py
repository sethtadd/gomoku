import logging
import os
from threading import Thread
from typing import cast

import numpy as np
import pygame

from Board import BLACK, DRAW, WHITE, Board

COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_BROWN = (205, 128, 0)
COLOR_GRAY = (30, 30, 30)
COLOR_BOARD = (118, 86, 153)


# https://stackoverflow.com/a/19846691/1781821
def threaded(fn):
    def wrapper(*args, **kwargs):
        Thread(target=fn, args=args, kwargs=kwargs, daemon=False).start()

    return wrapper


class BoardGUI:
    def __init__(self, board: Board, screen_size: int) -> None:
        logging.info("initializing BoardGUI")
        self.board = board
        self.size = (screen_size, screen_size)
        self.line_spacing = self.size[0] / (self.board.dim + 1)
        self.surface = None
        self.stop_loop = False
        self.click_pos = None
        self.load_images()

    def load_images(self) -> None:
        logging.info("loading images")
        # board
        self.img_wood_background = pygame.image.load(
            os.path.join("resources", "cherry_wood.png")
        )
        self.img_wood_background = pygame.transform.scale(
            self.img_wood_background, (self.size)
        )
        # pieces
        piece_dims = (self.line_spacing / 1.5, self.line_spacing / 1.5)
        self.img_black_piece = pygame.image.load(
            os.path.join("resources", "go_piece_black.png")
        )
        self.img_black_piece = pygame.transform.scale(self.img_black_piece, piece_dims)
        self.img_white_piece = pygame.image.load(
            os.path.join("resources", "go_piece_white.png")
        )
        self.img_white_piece = pygame.transform.scale(self.img_white_piece, piece_dims)
        # yumeko
        yumeko_size = (self.size[0] * 900 / 1025, self.size[0])
        self.img_yumeko = pygame.image.load(os.path.join("resources", "yumeko.png"))
        self.img_yumeko = pygame.transform.scale(self.img_yumeko, yumeko_size)

    @threaded
    def start_gui(self) -> None:
        logging.info("starting GUI on separate thread")
        pygame.init()
        pygame.display.set_caption("Gomoku")
        self.surface = pygame.display.set_mode(self.size)
        logging.info("starting loop")
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
            if self.board.winner is not None:
                self.draw_game_over_surface()
            pygame.display.flip()
        else:
            logging.info("stopping loop")
            pygame.quit()

    def draw_board(self) -> None:
        self.surface = cast(pygame.Surface, self.surface)

        self.surface.blit(source=self.img_wood_background, dest=(0, 0))
        # self.surface.fill(COLOR_BOARD)
        # draw position grid lines
        for i in range(self.board.dim):
            pygame.draw.line(
                self.surface,
                COLOR_GRAY,
                ((i + 1) * self.line_spacing, 0),
                ((i + 1) * self.line_spacing, self.size[1]),
                2,
            )
            pygame.draw.line(
                self.surface,
                COLOR_GRAY,
                (0, (i + 1) * self.line_spacing),
                (self.size[1], (i + 1) * self.line_spacing),
                2,
            )

    def draw_board_pieces(self) -> None:
        self.surface = cast(pygame.Surface, self.surface)

        black_positions, white_positions = self.board.get_closed_positions()
        for pos in black_positions:
            pos += np.array([1, 1])
            pos = pos * self.line_spacing
            center = np.array(self.img_black_piece.get_size()) / 2
            pos = pos - center
            self.surface.blit(source=self.img_black_piece, dest=tuple(pos))
            # pygame.draw.circle(surface=self.surface, color=COLOR_BLACK, center=pos, radius=self.line_spacing / 3)
        for pos in white_positions:
            pos += np.array([1, 1])
            pos = pos * self.line_spacing
            center = np.array(self.img_white_piece.get_size()) / 2
            pos = pos - center
            self.surface.blit(source=self.img_white_piece, dest=tuple(pos))
            # pygame.draw.circle(surface=self.surface, color=COLOR_WHITE, center=pos, radius=self.line_spacing / 3)

    def draw_game_over_surface(self) -> None:
        self.surface = cast(pygame.Surface, self.surface)

        # winner image
        self.surface.blit(source=self.img_yumeko, dest=(0, 0))

        if self.board.winner != DRAW:
            img_winner_piece = (
                self.img_black_piece
                if self.board.winner == BLACK
                else self.img_white_piece
            )
            img_winner_piece = pygame.transform.scale(
                img_winner_piece, (0.11 * self.size[0], 0.11 * self.size[0])
            )
            self.surface.blit(
                source=img_winner_piece,
                dest=(0.61 * self.size[0], 0.108 * self.size[1]),
            )

        # winner text
        text = (
            "black wins"
            if self.board.winner == BLACK
            else "white wins"
            if self.board.winner == WHITE
            else "draw"
        )
        text_surface = pygame.font.Font("resources/rodchenkoctt.ttf", 50).render(
            text, True, COLOR_WHITE
        )
        text_dims = (
            0.5
            * self.size[0]
            * np.array(text_surface.get_size())
            / text_surface.get_size()[0]
        )
        text_surface = pygame.transform.scale(text_surface, tuple(text_dims))
        x = self.size[0] / 2 - text_surface.get_width() / 2
        y = self.size[1] / 2 - text_surface.get_height() / 2
        self.surface.blit(source=text_surface, dest=(x, y))
