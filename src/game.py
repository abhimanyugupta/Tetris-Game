import random
from collections import deque

import pygame

from .board import Board
from .piece import PIECE_TYPES, Piece
from .scoring import ScoreState, gravity_for_level
from .settings import BOARD_HEIGHT, BOARD_WIDTH


class TetrisGame:
    def __init__(self):
        self.board = Board(BOARD_WIDTH, BOARD_HEIGHT)
        self.score = ScoreState()
        self.bag = []
        self.next_queue = deque()
        self.active_piece = None

        self.game_over = False
        self.paused = False
        self.gravity_timer = 0.0

        self.reset()

    def reset(self):
        self.board.reset()
        self.score = ScoreState()
        self.bag = []
        self.next_queue = deque()
        self.active_piece = None

        self.game_over = False
        self.paused = False
        self.gravity_timer = 0.0

        self._fill_next_queue()
        self._spawn_piece()

    def _refill_bag(self):
        self.bag = list(PIECE_TYPES)
        random.shuffle(self.bag)

    def _draw_piece_type(self):
        if not self.bag:
            self._refill_bag()
        return self.bag.pop()

    def _fill_next_queue(self):
        while len(self.next_queue) < 5:
            self.next_queue.append(self._draw_piece_type())

    def _spawn_piece(self):
        kind = self.next_queue.popleft()
        self._fill_next_queue()

        self.active_piece = Piece(kind=kind, x=(self.board.width // 2) - 2, y=-2)
        if not self.board.is_valid_position(self.active_piece):
            self.game_over = True

    def _lock_and_continue(self):
        if self.active_piece is None:
            return

        top_out = self.board.lock_piece(self.active_piece)
        cleared = self.board.clear_lines()
        self.score.add_line_clear(cleared)

        if top_out:
            self.game_over = True
            return

        self._spawn_piece()

    def move_horizontal(self, dx):
        if self.active_piece is None or self.paused or self.game_over:
            return

        if self.board.is_valid_position(self.active_piece, dx=dx):
            self.active_piece.x += dx

    def rotate(self, direction):
        if self.active_piece is None or self.paused or self.game_over:
            return

        new_rotation = self.active_piece.rotated(direction)
        if self.board.is_valid_position(self.active_piece, rotation=new_rotation):
            self.active_piece.rotation = new_rotation

    def soft_drop(self):
        if self.active_piece is None or self.paused or self.game_over:
            return

        if self.board.is_valid_position(self.active_piece, dy=1):
            self.active_piece.y += 1
            self.score.add_soft_drop(1)
        else:
            self._lock_and_continue()

    def hard_drop(self):
        if self.active_piece is None or self.paused or self.game_over:
            return

        distance = self.board.hard_drop_distance(self.active_piece)
        self.active_piece.y += distance
        self.score.add_hard_drop(distance)
        self._lock_and_continue()

    def _apply_gravity_step(self):
        if self.active_piece is None:
            return False

        if self.board.is_valid_position(self.active_piece, dy=1):
            self.active_piece.y += 1
            return True

        self._lock_and_continue()
        return False

    def handle_event(self, event):
        if event.type != pygame.KEYDOWN:
            return

        if event.key == pygame.K_ESCAPE and not self.game_over:
            self.paused = not self.paused
            return

        if event.key == pygame.K_r and self.game_over:
            self.reset()
            return

        if self.paused or self.game_over:
            return

        if event.key in (pygame.K_LEFT, pygame.K_a):
            self.move_horizontal(-1)
        elif event.key in (pygame.K_RIGHT, pygame.K_d):
            self.move_horizontal(1)
        elif event.key in (pygame.K_DOWN, pygame.K_s):
            self.soft_drop()
        elif event.key == pygame.K_SPACE:
            self.hard_drop()
        elif event.key in (pygame.K_UP, pygame.K_x):
            self.rotate(1)
        elif event.key == pygame.K_z:
            self.rotate(-1)

    def update(self, delta_seconds):
        if self.paused or self.game_over:
            return

        speed = gravity_for_level(self.score.level)
        fall_interval = 1.0 / speed

        self.gravity_timer += delta_seconds
        while self.gravity_timer >= fall_interval:
            moved = self._apply_gravity_step()
            self.gravity_timer -= fall_interval
            if not moved:
                self.gravity_timer = 0.0
                break
