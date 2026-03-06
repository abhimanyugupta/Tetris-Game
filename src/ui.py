import pygame

from .piece import TETROMINOES
from .settings import (
    BG_COLOR,
    BOARD_BG_COLOR,
    BOARD_HEIGHT,
    BOARD_WIDTH,
    CELL_SIZE,
    GRID_COLOR,
    MUTED_TEXT_COLOR,
    OVERLAY_COLOR,
    PADDING,
    PIECE_COLORS,
    SIDE_PANEL_WIDTH,
    TEXT_COLOR,
)


class GameRenderer:
    def __init__(self):
        self.title_font = pygame.font.SysFont("consolas", 34, bold=True)
        self.body_font = pygame.font.SysFont("consolas", 24)
        self.small_font = pygame.font.SysFont("consolas", 18)

        self.board_rect = pygame.Rect(
            PADDING,
            PADDING,
            BOARD_WIDTH * CELL_SIZE,
            BOARD_HEIGHT * CELL_SIZE,
        )
        self.panel_rect = pygame.Rect(
            self.board_rect.right + PADDING,
            PADDING,
            SIDE_PANEL_WIDTH,
            BOARD_HEIGHT * CELL_SIZE,
        )

    def draw(self, surface, game):
        surface.fill(BG_COLOR)
        self._draw_board(surface, game)
        self._draw_panel(surface, game)

        if game.paused and not game.game_over:
            self._draw_overlay(surface, "Paused", "Press ESC to resume")
        elif game.game_over:
            self._draw_overlay(surface, "Game Over", "Press R to restart")

    def _draw_board(self, surface, game):
        pygame.draw.rect(surface, BOARD_BG_COLOR, self.board_rect, border_radius=6)

        for row in range(BOARD_HEIGHT):
            for col in range(BOARD_WIDTH):
                cell = game.board.grid[row][col]
                if cell is None:
                    continue
                self._draw_cell(surface, col, row, PIECE_COLORS[cell])

        if game.active_piece is not None:
            for x, y in game.active_piece.cells():
                if y < 0:
                    continue
                self._draw_cell(surface, x, y, PIECE_COLORS[game.active_piece.kind])

        for row in range(BOARD_HEIGHT + 1):
            y = self.board_rect.top + (row * CELL_SIZE)
            pygame.draw.line(surface, GRID_COLOR, (self.board_rect.left, y), (self.board_rect.right, y), 1)
        for col in range(BOARD_WIDTH + 1):
            x = self.board_rect.left + (col * CELL_SIZE)
            pygame.draw.line(surface, GRID_COLOR, (x, self.board_rect.top), (x, self.board_rect.bottom), 1)

    def _draw_panel(self, surface, game):
        title = self.title_font.render("TETRIS", True, TEXT_COLOR)
        surface.blit(title, (self.panel_rect.left, self.panel_rect.top))

        lines = [
            f"Score: {game.score.score}",
            f"Level: {game.score.level}",
            f"Lines: {game.score.lines}",
            "",
            "Controls",
            "Left/Right: Move",
            "Up/X: Rotate CW",
            "Z: Rotate CCW",
            "Down: Soft Drop",
            "Space: Hard Drop",
            "ESC: Pause",
        ]

        y = self.panel_rect.top + 52
        for line in lines:
            color = MUTED_TEXT_COLOR if line == "" else TEXT_COLOR
            text = self.small_font.render(line, True, color)
            surface.blit(text, (self.panel_rect.left, y))
            y += 24

        queue_title = self.body_font.render("Next", True, TEXT_COLOR)
        surface.blit(queue_title, (self.panel_rect.left, self.panel_rect.top + 320))

        queue = list(game.next_queue)[:5]
        preview_y = self.panel_rect.top + 360
        for kind in queue:
            self._draw_preview_piece(surface, kind, self.panel_rect.left, preview_y)
            preview_y += 52

    def _draw_preview_piece(self, surface, kind, x, y):
        cell_size = 14
        shape = TETROMINOES[kind][0]
        min_x = min(cell[0] for cell in shape)
        min_y = min(cell[1] for cell in shape)

        for cx, cy in shape:
            draw_x = x + ((cx - min_x) * cell_size)
            draw_y = y + ((cy - min_y) * cell_size)
            rect = pygame.Rect(draw_x, draw_y, cell_size - 1, cell_size - 1)
            pygame.draw.rect(surface, PIECE_COLORS[kind], rect, border_radius=3)

    def _draw_cell(self, surface, col, row, color):
        x = self.board_rect.left + (col * CELL_SIZE)
        y = self.board_rect.top + (row * CELL_SIZE)
        rect = pygame.Rect(x + 1, y + 1, CELL_SIZE - 2, CELL_SIZE - 2)
        pygame.draw.rect(surface, color, rect, border_radius=4)

    def _draw_overlay(self, surface, title, subtitle):
        overlay = pygame.Surface((self.board_rect.width, self.board_rect.height), pygame.SRCALPHA)
        overlay.fill(OVERLAY_COLOR)
        surface.blit(overlay, self.board_rect.topleft)

        title_text = self.title_font.render(title, True, TEXT_COLOR)
        subtitle_text = self.body_font.render(subtitle, True, TEXT_COLOR)

        title_pos = title_text.get_rect(center=(self.board_rect.centerx, self.board_rect.centery - 18))
        subtitle_pos = subtitle_text.get_rect(center=(self.board_rect.centerx, self.board_rect.centery + 22))

        surface.blit(title_text, title_pos)
        surface.blit(subtitle_text, subtitle_pos)
