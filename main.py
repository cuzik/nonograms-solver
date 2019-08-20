import pygame
import time

from pygame.locals import QUIT, KEYDOWN, K_ESCAPE

# describe consts

Colors = {
    "backgroud": ( 22,  22,  22),
    "line":      ( 94, 131, 139),
    "label":     (219, 143, 92),
}


class Main:
    def __init__(self):
        self.border = 50
        self.cell_border = 5
        self.line_size = 2
        self.game_run = True
        self.cell_internal_size = 25

        self.horizontal = [
            [4],
            [1],
            [2],
            [2],
            [4]
        ]

        self.vertical = [
            [3],
            [1,3],
            [1,1],
            [1,1],
            [2]
        ]

        self.matrix_mirror = [[1] * (len(self.vertical) + 1)] * (len(self.horizontal) + 1)

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

        x_base = self.label_size_horizontal() + self.border
        y_base = self.label_size_vertical() + self.border
        size = self.cell_size() + self.line_size

        for cell_index in range(len(self.vertical)):
            line_aux = []
            for line_index in range(len(self.horizontal)):
                x = x_base + size * cell_index
                y = y_base + size * line_index
                line_aux.append((x,y))
            self.matrix_position.append(line_aux)

    def start_dimension(self):
        self.height = self.internal_height() + 2 * self.border + self.label_size_vertical()
        self.width = self.internal_width() + 2 * self.border + self.label_size_horizontal()

    def max_elements(self, matrix):
        max_count = 0
        for array in matrix:
            array_len = len(array)
            if array_len > max_count:
                max_count = array_len
        return max_count

    def max_elements_horizontal(self):
        return self.max_elements(self.horizontal)

    def max_elements_vertical(self):
        return self.max_elements(self.vertical)

    def internal_height(self):
        return len(self.horizontal) * self.cell_size() + (len(self.vertical) + 1) * self.line_size

    def internal_width(self):
        return len(self.vertical) * self.cell_size() + (len(self.horizontal) + 1) * self.line_size

    def cell_size(self):
        return self.cell_internal_size + (2 * self.cell_border)

    def get_dimension(self):
        return self.width, self.height

    def set_backgroud(self):
        self.screen.fill(Colors["backgroud"])

    def get_events_draw(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.game_run = False
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                self.game_run = False

    def label_size_horizontal(self):
        return self.max_elements_horizontal() * (self.line_size + self.cell_size())

    def label_size_vertical(self):
        return self.max_elements_vertical() * (self.line_size + self.cell_size())

    def draw_board(self):
        self.draw_horizontal_labels()
        self.draw_vertical_labels()

        self.draw_matrix()

    def draw_matrix(self):
        for line_index in range(len(self.horizontal)):
            for cell_index in range(len(self.vertical)):
                self.draw_matrix_cell(self.matrix_position[cell_index][line_index][0], self.matrix_position[cell_index][line_index][1], self.matrix_mirror[cell_index][line_index])

    def draw_horizontal_labels(self):
        max_elements = self.max_elements_horizontal()
        size = self.cell_size() + self.line_size

        for line_index in range(len(self.horizontal)):
            array = self.horizontal[line_index]
            for cell_index in range(len(array)):
                cell = array[cell_index]

                x = self.border + (max_elements - (len(array) - cell_index)) * size
                y = self.border + self.label_size_vertical() + line_index * size

                self.draw_label_cell(x, y, cell)

    def draw_vertical_labels(self):
        max_elements = self.max_elements_vertical()
        size = self.cell_size() + self.line_size

        for line_index in range(len(self.vertical)):
            array = self.vertical[line_index]
            for cell_index in range(len(array)):
                cell = array[cell_index]

                x = self.border + self.label_size_horizontal() + line_index * size
                y = self.border + (max_elements - (len(array) - cell_index )) * size

                self.draw_label_cell(x, y, cell)

    def draw_label_cell(self, x, y, number):
        self.draw_cell(x, y, Colors["label"])

        text = self.font.render(str(number), True, Colors["label"])
        self.screen.blit(text, (x + self.cell_border, y + self.cell_border))

    def draw_matrix_cell(self, x, y, figure):
        self.draw_cell(x, y, Colors["line"])

        if figure == 0:
            pass
        if figure == 1:
            pygame.draw.rect(self.screen, Colors["label"], (x + self.cell_border, y + self.cell_border, self.cell_internal_size, self.cell_internal_size))


    def draw_cell(self, x, y, color):
        size = self.cell_size() + self.line_size

        self.draw_line([(x, y), (x, y + size)], color)
        self.draw_line([(x, y), (x + size, y)], color)
        self.draw_line([(x, y + size), (x + size, y + size)], color)
        self.draw_line([(x + size, y), (x + size, y + size)], color)

    def draw_line(self, points, color):
        pygame.draw.lines(self.screen, color, False, points, self.line_size)

    def execute(self):
        while self.game_run:
            self.get_events_draw()
            self.set_backgroud()
            # do some
            self.draw_board()

            time.sleep(.001)

            pygame.display.flip()


if __name__ == "__main__":
    a = Main()
    b = Main()

    a.execute()
    b.execute()
