import pygame

from src.game import TetrisGame
from src.settings import FPS, WINDOW_HEIGHT, WINDOW_WIDTH
from src.ui import GameRenderer


def main():
    pygame.init()
    pygame.display.set_caption("Tetris Clone")
    pygame.key.set_repeat(130, 40)

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()

    game = TetrisGame()
    renderer = GameRenderer()

    running = True
    while running:
        delta_seconds = clock.tick(FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            game.handle_event(event)

        game.update(delta_seconds)
        renderer.draw(screen, game)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
