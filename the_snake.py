import random

import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


# Цвета:
BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 15

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pg.display.set_caption('Змейка')
clock = pg.time.Clock()


class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self, body_color=None) -> None:
        """Иницилизауия объекта по центру экрана."""
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = body_color

    def draw_rect(self, position: tuple[int, int]) -> None:
        """Отрисовка квадрата объекта."""
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)

    def draw(self):
        """отрисовка"""


class Apple(GameObject):
    """Класс яблока, которое змейка должна  съесть."""

    def __init__(self, closed=None):
        """Инициализация яблока с рандомной позицией и цветом."""
        super().__init__()
        self.body_color = APPLE_COLOR
        self.randomize_position(closed)

    def randomize_position(self, closed=None) -> None:
        """Устанавливает случайную позицию яблока в пределах сетки."""
        while True:
            random_x = random.randint(0, GRID_WIDTH - 1) * GRID_SIZE
            random_y = random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            pos = (random_x, random_y)
            if closed is None or pos not in closed:
                self.position = pos
                break

    def draw(self):
        """Отрисовка яблока на экране."""
        self.draw_rect(self.position)


class Snake(GameObject):
    """Класс змейки."""

    def __init__(self) -> None:
        # Задаём цвет змейки по умолчанию при вызове родителя
        super().__init__(body_color=SNAKE_COLOR)
        self._init_state()

    def _init_state(self):
        start_x = (SCREEN_WIDTH // 2) // GRID_SIZE * GRID_SIZE
        start_y = (SCREEN_HEIGHT // 2) // GRID_SIZE * GRID_SIZE
        start_pos = (start_x, start_y)
        self.length = 1
        self.positions = [start_pos]
        self.direction = RIGHT
        self.next_direction = None
        self.flag = False

    def move(self) -> tuple[int, int] | None:
        """Обновляет позицию змейки.

        Возвращает позицию, которая была удалена (хвост),
        если змейка не растёт, иначе None.
        """
        first_x, first_y = self.get_head_position()
        delta_x, delta_y = self.direction
        new_head = (
            (first_x + delta_x * GRID_SIZE) % SCREEN_WIDTH,
            (first_y + delta_y * GRID_SIZE) % SCREEN_HEIGHT,
        )

        self.positions.insert(0, new_head)

        if not self.flag:
            removed = self.positions.pop()
            return removed
        else:
            self.flag = False
            return None

    def update_direction(self) -> None:
        """Обновляет направление движения змейки, если есть новая команда."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def draw(self):
        """Отрисовывает змейку на экране."""
        # Голова
        self.draw_rect(self.get_head_position())
        # Тело
        for position in self.positions[1:]:
            self.draw_rect(position)

    def get_head_position(self) -> tuple[int, int]:
        """Возвращает текущую позицию головы змейки."""
        return self.positions[0]

    def reset(self) -> None:
        """Сброс змеи в начальное состояние."""
        self._init_state()


def handle_keys(game_object: Snake) -> None:
    """Обработка нажатия на клавиши с использованием словаря переходов."""
    # словарь с кнопками под движение
    direction_changes = {
        (pg.K_UP, DOWN): DOWN,
        (pg.K_UP, LEFT): UP,
        (pg.K_UP, RIGHT): UP,
        (pg.K_DOWN, UP): UP,
        (pg.K_DOWN, LEFT): DOWN,
        (pg.K_DOWN, RIGHT): DOWN,
        (pg.K_LEFT, UP): LEFT,
        (pg.K_LEFT, DOWN): LEFT,
        (pg.K_LEFT, RIGHT): RIGHT,
        (pg.K_RIGHT, UP): RIGHT,
        (pg.K_RIGHT, DOWN): RIGHT,
        (pg.K_RIGHT, LEFT): LEFT,
    }

    valid_keys = {key for key, _ in direction_changes.keys()}
    # Guard block
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit

        if event.type != pg.KEYDOWN:
            continue
        # выход
        if event.key == pg.K_ESCAPE:
            pg.quit()
            raise SystemExit

        if event.key in valid_keys:
            new_dir = direction_changes.get(
                (event.key, game_object.direction),
                game_object.direction
            )
            game_object.next_direction = new_dir


def main() -> None:
    pg.init()
    snake = Snake()
    apple = Apple(closed=snake.positions)

    needs_full_redraw = True

    while True:
        clock.tick(SPEED)

        handle_keys(snake)
        snake.update_direction()

        # Передвижение змейки и получение позиции хвоста, которую надо очистить
        tail_to_clear = snake.move()

        # Проверка столкновения змейки с собой
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            apple.randomize_position(closed=snake.positions)
            needs_full_redraw = True  # Полная очистка при сбросе

        # Проверка поедания яблока
        if snake.get_head_position() == apple.position:
            snake.flag = True
            apple.randomize_position(snake.positions)

        if needs_full_redraw:
            screen.fill(BOARD_BACKGROUND_COLOR)
            needs_full_redraw = False
        else:
            # Очистка только области, где был хвост змейки
            if tail_to_clear:
                rect = pg.Rect(tail_to_clear, (GRID_SIZE, GRID_SIZE))
                pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, rect)

        apple.draw()
        snake.draw()

        pg.display.update()


if __name__ == '__main__':
    main()
