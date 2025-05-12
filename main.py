import pygame
import random
import os

# Настройка игрового окна
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
ROWS = 6  # количество строк
COLS = 6  # количество столбцов
MARGIN = 2  # отступ между фрагментами
FRAME_PADDING = 20  # отступ коробки от пазла
SHADOW_COLOR = (0, 0, 0, 100)  # полупрозрачная тень внутри коробки

# Инициализация Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Пазл')
clock = pygame.time.Clock()

# Загрузка коробки
try:
    box_image = pygame.image.load(os.path.join('pictures', 'box.jpg'))
    # Масштабируем коробку до размеров окна (1000x700)
    box_image = pygame.transform.scale(box_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
except:
    box_image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))  # запасной прямоугольник
    box_image.fill((255, 255, 255))  # белый цвет, если фото не загрузилось

# Загрузка и подготовка изображения пазла
pictures = [f for f in os.listdir('pictures') if f.endswith(('.jpg', '.png')) and f != 'box.jpg']
picture = random.choice(pictures)
image = pygame.image.load(os.path.join('pictures', picture))

# Масштабируем изображение пазла, чтобы оно помещалось внутри коробки (максимум 700x700)
max_puzzle_size = 700
scale_factor = min(max_puzzle_size / image.get_width(), max_puzzle_size / image.get_height())
image = pygame.transform.scale(image, (int(image.get_width() * scale_factor), int(image.get_height() * scale_factor)))

# Рассчитайте размеры фрагментов
image_width, image_height = image.get_size()
TILE_WIDTH = image_width // COLS
TILE_HEIGHT = image_height // ROWS

# Рассчитайте размеры области пазла и центрирование
PUZZLE_WIDTH = COLS * (TILE_WIDTH + MARGIN) + MARGIN
PUZZLE_HEIGHT = ROWS * (TILE_HEIGHT + MARGIN) + MARGIN
PUZZLE_X = (SCREEN_WIDTH - PUZZLE_WIDTH) // 2  # центрирование по горизонтали
PUZZLE_Y = (SCREEN_HEIGHT - PUZZLE_HEIGHT) // 2  # центрирование по вертикали

# Положение коробки (теперь она занимает весь экран)
BOX_WIDTH = SCREEN_WIDTH
BOX_HEIGHT = SCREEN_HEIGHT
BOX_X = 0
BOX_Y = 0

# Разрежьте изображение на фрагменты
tiles = []
for i in range(ROWS):
    for j in range(COLS):
        rect = pygame.Rect(j * TILE_WIDTH, i * TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT)
        tile = image.subsurface(rect)
        tiles.append(tile)

# Сохраните оригинальный порядок и перемешайте фрагменты
origin_tiles = tiles.copy()
random.shuffle(tiles)

# Игровая логика
selected = None  # выбранный фрагмент
swaps = 0  # счетчик перестановок
running = True  # флаг работы игры

# Функция отрисовки фрагментов с коробкой
def draw_tiles():
    # Отрисовка коробки
    screen.blit(box_image, (BOX_X, BOX_Y))

    # Отрисовка внутренней области с тенью
    inner_rect = pygame.Rect(
        PUZZLE_X,
        PUZZLE_Y,
        PUZZLE_WIDTH,
        PUZZLE_HEIGHT
    )
    shadow_surface = pygame.Surface((inner_rect.width, inner_rect.height), pygame.SRCALPHA)
    shadow_surface.fill(SHADOW_COLOR)  # полупрозрачная тень
    screen.blit(shadow_surface, (inner_rect.x, inner_rect.y))

    # Отрисовка фрагментов
    for i in range(len(tiles)):
        row = i // ROWS
        col = i % COLS
        x = PUZZLE_X + col * (TILE_WIDTH + MARGIN) + MARGIN
        y = PUZZLE_Y + row * (TILE_HEIGHT + MARGIN) + MARGIN
        if i == selected:
            pygame.draw.rect(screen, (0, 255, 0),
                (x - MARGIN, y - MARGIN,
                 TILE_WIDTH + MARGIN * 2,
                 TILE_HEIGHT + MARGIN * 2))
        screen.blit(tiles[i], (x, y))

# Функции для отображения сообщений
def game_over():
    font = pygame.font.SysFont('Arial', 64)
    text = font.render('Ура, картинка собрана!', True, (255, 255, 255))
    text_rect = text.get_rect()
    text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    pygame.draw.rect(screen, (0, 0, 0), text_rect.inflate(4, 4))
    screen.blit(text, text_rect)

def draw_swaps():
    font = pygame.font.SysFont('Arial', 32)
    text = font.render(f'Количество перестановок: {swaps}', True, (255, 255, 255))
    text_rect = text.get_rect()
    # Размещаем надпись в нижней части фотографии, на столе
    text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30)
    pygame.draw.rect(screen, (0, 0, 0), text_rect.inflate(4, 4))
    screen.blit(text, text_rect)

# Основной игровой цикл
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for i in range(len(tiles)):
                row = i // ROWS
                col = i % COLS
                x = PUZZLE_X + col * (TILE_WIDTH + MARGIN) + MARGIN
                y = PUZZLE_Y + row * (TILE_HEIGHT + MARGIN) + MARGIN
                if x <= mouse_x <= x + TILE_WIDTH and y <= mouse_y <= y + TILE_HEIGHT:
                    if selected is not None and selected != i:
                        tiles[i], tiles[selected] = tiles[selected], tiles[i]
                        selected = None
                        swaps += 1
                    elif selected == i:
                        selected = None
                    else:
                        selected = i

    # Отрисовка и обновление экрана
    draw_tiles()
    draw_swaps()
    if tiles == origin_tiles:
        game_over()
    pygame.display.flip()
    clock.tick(60)

# Завершение работы
pygame.quit()