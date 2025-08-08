import random
import pygame


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
SPEED = 10

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('Змейка')
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self) -> None:
        """Инициализация объекта с позицией по центру экрана."""
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = None

    def draw(self) -> None:
        """Метод отрисовки объекта (переопределяется в наследниках)."""
        pass


class Apple(GameObject):
    """Класс яблока, которое змейка должна съесть."""

    def __init__(self) -> None:
        """Инициализация яблока с рандомной позицией и цветом."""
        super().__init__()
        self.body_color = APPLE_COLOR
        self.randomize_position()

    def randomize_position(self) -> None:
        """Устанавливает случайную позицию яблока в пределах сетки."""
        random_x = random.randint(0, GRID_WIDTH - 1) * GRID_SIZE
        random_y = random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        self.position = (random_x, random_y)

    def draw(self) -> None:
        """Отрисовка яблока на экране."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс змейки."""

    def __init__(self) -> None:
        """Инициализация змейки и её состояния."""
        self._init_state()

    def _init_state(self) -> None:
        """Устанавливает начальное состояние змейки."""
        start_x = (SCREEN_WIDTH // 2) // GRID_SIZE * GRID_SIZE
        start_y = (SCREEN_HEIGHT // 2) // GRID_SIZE * GRID_SIZE
        start_pos = (start_x, start_y)

        super().__init__()
        self.position = start_pos

        self.length = 1
        self.positions = [start_pos]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.flag = False  # Флаг съедения яблока

    def move(self) -> None:
        """Обновляет позицию змейки, добавляя новую голову и
        убирая хвост, если нужно."""
        first_x, first_y = self.positions[0]
        delta_x, delta_y = self.direction
        new_head = (
            (first_x + delta_x * GRID_SIZE) % SCREEN_WIDTH,
            (first_y + delta_y * GRID_SIZE) % SCREEN_HEIGHT,
        )

        if new_head in self.positions[1:]:
            self.reset()
        else:
            self.positions.insert(0, new_head)

            if not self.flag:
                self.positions.pop()
            else:
                self.flag = False

        self.position = self.positions[0]

    def update_direction(self) -> None:
        """Обновляет направление движения змейки, если есть новая команда."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def draw(self) -> None:
        """Отрисовывает змейку на экране."""
        # Тело змейки без головы
        for position in self.positions[1:]:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Голова змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

    def get_head_position(self) -> tuple[int, int]:
        """Возвращает текущую позицию головы змейки."""
        return self.position

    def reset(self) -> None:
        """Сброс змеи в начальное состояние."""
        self._init_state()


def handle_keys(game_object: Snake) -> None:
    """Обработка нажатия на клавиши.

    Args:
        game_object (Snake): объект змейки для управления.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main() -> None:
    """Основная функция игры."""
    pygame.init()
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)

        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.positions[0] == apple.position:
            snake.flag = True
            apple.randomize_position()

        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        snake.draw()

        pygame.display.update()


if __name__ == '__main__':
    main()
