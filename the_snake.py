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

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()

# Материнский класс объектов.


class GameObject:
    def __init__(self, position) -> None:
        self.position = position
        self.body_color = None

    def draw(self):
        pass
# Класс яблоки.


class Apple(GameObject):
    def __init__(self):
        super().__init__((0, 0))
        self.body_color = APPLE_COLOR
        self.randomize_position()
    # Создание рандомных точек появления яблока.

    def randomize_position(self):
        random_x = random.randint(
            0, (SCREEN_WIDTH // GRID_SIZE) - 1) * GRID_SIZE
        random_y = random.randint(
            0, (SCREEN_HEIGHT // GRID_SIZE) - 1) * GRID_SIZE
        self.position = (random_x, random_y)
    # Метод draw класса Apple.

    def draw(self):
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    def __init__(self):
        self._init_state()
    # создаю приватный метод, что бы его вызвать в reset и не повторять код

    def _init_state(self):
        start_x = (SCREEN_WIDTH // 2) // GRID_SIZE * GRID_SIZE
        start_y = (SCREEN_HEIGHT // 2) // GRID_SIZE * GRID_SIZE
        start_pos = (start_x, start_y)

        super().__init__(start_pos)

        self.length = 1
        self.positions = [start_pos]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.flag = False

    # Получение стартовой позиции змеи.

    def _get_start_pos(self):
        x = (SCREEN_WIDTH // 2) // GRID_SIZE * GRID_SIZE
        y = (SCREEN_HEIGHT // 2) // GRID_SIZE * GRID_SIZE
        return (x, y)
    # Движение змейки / добавление новой головы если съедено яблоко.
    # Удаление последнпоследнегоий элемента если длинна неувеличилась.

    def move(self):
        first_x, first_y = self.positions[0]
        delta_x, delta_y = self.direction
        new_head = (
            (first_x + delta_x * GRID_SIZE) % SCREEN_WIDTH,
            (first_y + delta_y * GRID_SIZE) % SCREEN_HEIGHT
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

    # Метод обновления направления после нажатия на кнопку.

    def update_direction(self):
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None
    # Метод draw класса Snake

    def draw(self):
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)
    # Получение позиции головы змеи

    def get_head_position(self):
        return self.position
    # Сбрасывание положение змеи в начальную позицию

    def reset(self):
        self._init_state()


def handle_keys(game_object):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
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
