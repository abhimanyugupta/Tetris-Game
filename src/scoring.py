from dataclasses import dataclass

from . import settings


@dataclass
class ScoreState:
    score: int = 0
    lines: int = 0
    level: int = 1
    combo: int = -1
    last_clear: int = 0

    def add_line_clear(self, cleared):
        self.last_clear = cleared

        if cleared > 0:
            self.combo += 1
        else:
            self.combo = -1

        base_points = settings.LINE_CLEAR_SCORES.get(cleared, 0)
        self.score += base_points * self.level

        if cleared > 0 and self.combo > 0:
            self.score += 50 * self.combo * self.level

        self.lines += cleared
        self.level = 1 + (self.lines // 10)

    def add_soft_drop(self, cells=1):
        self.score += settings.SOFT_DROP_POINTS * max(0, cells)

    def add_hard_drop(self, cells):
        self.score += settings.HARD_DROP_POINTS * max(0, cells)


def gravity_for_level(level):
    speed = settings.BASE_GRAVITY_CELLS_PER_SEC + ((level - 1) * settings.GRAVITY_INCREASE_PER_LEVEL)
    return min(settings.MAX_GRAVITY_CELLS_PER_SEC, speed)
