import pygame
import time
import random

from pygame.locals import QUIT, KEYDOWN, K_ESCAPE, K_SPACE

# describe consts

Colors = {
    "backgroud": ( 22,  22,  22),
    "cell":      ( 94, 131, 139),
    "label":     (219, 143,  92),
    "x":         (163,  47,  47),
    "full":      ( 51,  99,  42),
}

carlos = 1

class Board:
    def __init__(self, x_base, y_base, vertical, horizontal):
        global carlos
        self.number = carlos
        carlos = carlos + 1

        print(self.number)

        self.x_base = x_base
        self.y_base = y_base
        self.vertical = vertical
        self.horizontal = horizontal
        self.fetness = 0


        self.matrix_mirror = [[random.choices([True, False])[0] for i in range(len(self.vertical))] for j in range(len(self.horizontal))]

    def shuffle(self):
        # self.matrix_mirror = [[random.choices([True, False])[0] for i in range(len(self.vertical))] for j in range(len(self.horizontal))]
        for i in range(10):
            x = random.randint(0,len(self.horizontal) -1)
            y = random.randint(0,len(self.vertical) -1)

            self.matrix_mirror[x][y] = random.choices([True, False])[0]

    def evaluate(self):
        aux_horizontal = []
        aux_vertical = []

        for i in range(len(self.horizontal)):
            count = 0
            parcial = []
            for j in range(len(self.vertical)):
                if self.matrix_mirror[j][i]:
                    count = count + 1
                elif (self.matrix_mirror[j][i] == False or self.matrix_mirror[j][i] == None) and count != 0:
                    parcial.append(count)
                    count = 0
            if len(parcial) == 0:
                aux_horizontal.append([count])
            else:
                if count != 0:
                    parcial.append(count)
                aux_horizontal.append(parcial)

        for i in range(len(self.vertical)):
            count = 0
            parcial = []
            for j in range(len(self.horizontal)):
                if self.matrix_mirror[i][j]:
                    count = count + 1
                elif (self.matrix_mirror[i][j] == False or self.matrix_mirror[i][j] == None) and count != 0:
                    parcial.append(count)
                    count = 0
            if len(parcial) == 0:
                aux_vertical.append([count])
            else:
                if count != 0:
                    parcial.append(count)
                aux_vertical.append(parcial)

        if aux_horizontal == self.horizontal and aux_vertical == self.vertical:
            print('>>>' + str(self.number) + '<<<')
            return True

        return False


class Main:
    def __init__(self):
        self.border = 5
        self.cell_border = 2
        self.line_size = 1
        self.game_run = True
        self.pause_game = False
        self.cell_internal_size = 50

        self.boards_horizontal = 1
        self.boards_vertical = 1
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
            elif event.type == KEYDOWN and event.key == K_SPACE:
                self.pause_game = not self.pause_game

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
            self.get_events_draw()

            if not self.pause_game:
                pygame.display.set_caption(str(i))
                self.set_backgroud()


                for board in boards:
                    board.shuffle()
                    if board.evaluate():
                        self.pause_game = True

                for board in boards:
                    self.draw_board(board)

                # time.sleep(1)

                i = i + 1
                pygame.display.flip()


if __name__ == "__main__":
    a = Main()
    a.execute()
