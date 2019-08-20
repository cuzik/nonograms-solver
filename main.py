import pygame
import time
import random

from pygame.locals import QUIT, KEYDOWN, K_ESCAPE

# describe consts

Colors = {
    "backgroud": ( 22,  22,  22),
    "cell":      ( 94, 131, 139),
    "label":     (219, 143,  92),
    "x":         (163,  47,  47),
    "full":      ( 51,  99,  42),
}

print(pygame.display.get_num_displays())

class Board:
    def __init__(self, x_base, y_base, vertical, horizontal):
        self.x_base = x_base
        self.y_base = y_base
        self.vertical = vertical
        self.horizontal = horizontal

        self.matrix_mirror = [[True for i in range(len(self.vertical))] for j in range(len(self.horizontal))]

    def shuffle(self):
        for i in range(1):
            x = random.randint(0,len(self.horizontal) -1)
            y = random.randint(0,len(self.vertical) -1)

            self.matrix_mirror[x][y] = random.choices([True, False, None])[0]










class Main:
    def __init__(self):
        self.border = 5
        self.cell_border = 3
        self.line_size = 2
        self.game_run = True
        self.cell_internal_size = 25

        self.boards_horizontal = 5
        self.boards_vertical = 2
        self.cell_size = self.cell_internal_size + (2 * self.cell_border)
        self.cell_full_size = self.cell_size + self.line_size

        self.horizontal = [
            [2],
            [1,1],
            [3],
            [2],
            [2,2]
        ]
        self.vertical = [
            [4],
            [1,3],
            [3],
            [1],
            [1]
        ]

        self.max_elements_horizontal = self.max_elements(self.horizontal)
        self.max_elements_vertical = self.max_elements(self.vertical)

        self.label_size_horizontal = self.max_elements_horizontal * (self.line_size + self.cell_size)
        self.label_size_vertical = self.max_elements_vertical * (self.line_size + self.cell_size)

        self.start_dimension()

        pygame.init()
        self.screen = pygame.display.set_mode(self.get_dimension(), pygame.RESIZABLE)

        pygame.font.init()
        self.font = pygame.font.SysFont('Comic Sans MS', self.cell_internal_size)

        # set initial color
        self.set_backgroud()
        self.define_matrix_position()

    def define_matrix_position(self):
        self.matrix_position = []

        x_base = self.label_size_horizontal + self.border
        y_base = self.label_size_vertical + self.border
        size = self.cell_size + self.line_size

        for cell_index in range(len(self.vertical)):
            line_aux = []
            for line_index in range(len(self.horizontal)):
                x = x_base + size * cell_index
                y = y_base + size * line_index
                line_aux.append((x,y))
            self.matrix_position.append(line_aux)

    def start_dimension(self):
        self.height = self.internal_height() + 2 * self.border + self.label_size_vertical
        self.width = self.internal_width() + 2 * self.border + self.label_size_horizontal

    def max_elements(self, matrix):
        max_count = 0
        for array in matrix:
            array_len = len(array)
            if array_len > max_count:
                max_count = array_len
        return max_count

    def internal_height(self):
        return len(self.horizontal) * self.cell_size + (len(self.vertical) + 1) * self.line_size

    def internal_width(self):
        return len(self.vertical) * self.cell_size + (len(self.horizontal) + 1) * self.line_size

    def get_dimension(self):
        return (self.boards_horizontal * self.width, self.boards_vertical * self.height)

    def set_backgroud(self):
        self.screen.fill(Colors["backgroud"])

    def get_events_draw(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.game_run = False
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                self.game_run = False

    def draw_board(self, board):
        self.draw_horizontal_labels(board)
        self.draw_vertical_labels(board)

        self.draw_matrix(board)

    def draw_matrix(self, board):
        for line_index in range(len(self.horizontal)):
            for cell_index in range(len(self.vertical)):
                self.draw_matrix_cell(
                    self.matrix_position[cell_index][line_index][0] + board.x_base,
                    self.matrix_position[cell_index][line_index][1] + board.y_base,
                    board.matrix_mirror[cell_index][line_index]
                )

    def draw_horizontal_labels(self, board):
        max_elements = self.max_elements_horizontal

        for line_index in range(len(self.horizontal)):
            array = self.horizontal[line_index]
            for cell_index in range(len(array)):
                cell = array[cell_index]

                x = self.border + (max_elements - (len(array) - cell_index)) * self.cell_full_size + board.x_base
                y = self.border + self.label_size_vertical + line_index * self.cell_full_size + board.y_base

                self.draw_label_cell(x, y, cell)

    def draw_vertical_labels(self, board):
        max_elements = self.max_elements_vertical
        size = self.cell_size + self.line_size

        for line_index in range(len(self.vertical)):
            array = self.vertical[line_index]
            for cell_index in range(len(array)):
                cell = array[cell_index]

                x = self.border + self.label_size_horizontal + line_index * size + board.x_base
                y = self.border + (max_elements - (len(array) - cell_index )) * size + board.y_base

                self.draw_label_cell(x, y, cell)

    def draw_label_cell(self, x, y, number):
        self.draw_cell(x, y, Colors["label"])

        text = self.font.render(str(number), True, Colors["label"])
        self.screen.blit(text, (x + self.cell_border, y + self.cell_border))

    def draw_matrix_cell(self, x, y, figure):
        border_end_crop = - (self.cell_border + self.line_size % 2) + self.cell_full_size
        border_start_crop = self.cell_border + 1
        square_size = self.cell_full_size - 2 * self.cell_border - self.line_size % 2
        if figure:
            pygame.draw.rect(
                self.screen, Colors["full"],
                (
                    x + border_start_crop,
                    y + border_start_crop,
                    square_size,
                    square_size
                )
            )
        elif figure is None:
            self.draw_line([
                (x + border_start_crop, y + border_start_crop),
                (x + border_end_crop, y + border_end_crop)
            ], Colors["x"])
            self.draw_line([
                (x + border_end_crop, y + border_start_crop),
                (x + border_start_crop, y + border_end_crop)
            ], Colors["x"])
        self.draw_cell(x, y, Colors["cell"])

    def draw_cell(self, x, y, color):
        self.draw_line([(x, y), (x, y + self.cell_full_size)], color)
        self.draw_line([(x, y), (x + self.cell_full_size, y)], color)
        self.draw_line([(x, y + self.cell_full_size), (x + self.cell_full_size, y + self.cell_full_size)], color)
        self.draw_line([(x + self.cell_full_size, y), (x + self.cell_full_size, y + self.cell_full_size)], color)

    def draw_line(self, points, color):
        pygame.draw.lines(self.screen, color, False, points, self.line_size)

    def execute(self):
        boards = []

        for i in range(self.boards_vertical):
            for j in range(self.boards_horizontal):
                boards.append(Board(self.width * j, self.height * i, self.vertical, self.horizontal))

        i = 0

        while self.game_run:
            pygame.display.set_caption(str(i))

            self.get_events_draw()
            self.set_backgroud()

            for board in boards:
                self.draw_board(board)

            for board in boards:
                board.shuffle()

            # time.sleep(.1)

            i = i + 1
            pygame.display.flip()


if __name__ == "__main__":
    a = Main()
    a.execute()
