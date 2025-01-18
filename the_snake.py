from random import choice, randint
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
SPEED = 2

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Базовый класс, описывающий игровые объекты."""

    def __init__(self):
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = (255, 255, 255)

    def draw(self):
        """Метод отрисовки объектов."""
        pass


class Apple(GameObject):
    """Класс, описывающий яблоко."""

    @classmethod
    def randomize_position(cls):
        """Метод, возращающий рандомные координаты для яблока."""
        x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        return (x, y)

    def __init__(self):
        self.position = Apple.randomize_position()
        self.body_color = (255, 0, 0)

    def draw(self):
        """Метод отрисовки яблока."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс, описывающий змейку."""

    def __init__(self):
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.positions = [self.position]
        self.body_color = (0, 255, 0)
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def update_direction(self):
        """Метод, обновляющий направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """
        Метод, отвечающий за перемещение змейки. Добавляет одну клетку,
        в зависимости от направления и удаляет последнюю,
        если яблоко не съедено.
        """
        x, y = self.get_head_position
        dx, dy = self.direction
        x = (x + dx * GRID_SIZE) % SCREEN_WIDTH
        y = (y + dy * GRID_SIZE) % SCREEN_HEIGHT
        if (x, y) in self.positions:
            self.reset()
        self.positions.insert(0, (x, y))
        if len(self.positions) > self.length + 1:
            self.positions.pop()

    def draw(self):
        """Метод отрисовки змейки."""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    @property
    def get_head_position(self):
        """Метод, возвращающий координаты 'головы' змейки."""
        return self.positions[0]

    def reset(self):
        """
        Метод, сбрасывающий положение и длину змейки
        при столкновении с самой собой.
        """
        self.positions = [self.position]
        self.length = 1
        self.direction = choice([RIGHT, LEFT, UP, DOWN])
        self.next_direction = None


def handle_keys(game_object):
    """Функция обработки нажатия клавиш."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and \
                    game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and \
                    game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and \
                    game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and \
                    game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Метод, описывающий логику игры."""
    pygame.init()
    apple = Apple()
    snake = Snake()

    while True:
        clock.tick(SPEED)
        screen.fill(color=(0, 0, 0))

        handle_keys(snake)
        snake.update_direction()
        snake.move()
        if snake.get_head_position == apple.position:
            snake.length += 1
            apple = Apple()

        apple.draw()
        snake.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
