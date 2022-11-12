import pygame

from gomoku import Board

COLOR_BLACK = (0, 0, 0)


class BoardGUI:
    def __init__(self) -> None:
        pygame.init()
        self.size = (100, 100)
        self.screen = pygame.display.set_mode(self.size)
        self.should_quit = False

    def loop(self) -> None:
        while not self.should_quit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.should_quit = True
            self.screen.fill(COLOR_BLACK)
            pygame.display.flip()

    # TODO fill in function
    def update_board(self, board: Board) -> None:
        pass
