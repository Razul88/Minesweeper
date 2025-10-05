from typing import Any

import numpy as np
import ColorDetection

class Board(object):

    _FLAG_VALUE = -1
    _UNKNOWN_VALUE = None

    def __init__(self, width, height, templates_path, bg_colors, is_auto_open):
        self.bg_colors = bg_colors
        self.templates = ColorDetection.load_templates(templates_path)
        self.is_auto_open = is_auto_open

        self.board = [[None for x in range(width)] for y in range(height)]
        self.width = width
        self.height = height

    def updateByScreenshot(self, board_img, cell_pixels_width:int, cell_pixels_height: int, border_pixels=0):
        for x in range(0, self.width):
            for y in range(0, self.height):
                if self.board[y][x] is not None:
                    continue

                cell_x_pixel = x * cell_pixels_width
                cell_y_pixel = y * cell_pixels_height
                cell_image = board_img.crop((cell_x_pixel + border_pixels,
                                             cell_y_pixel + border_pixels,
                                             cell_x_pixel + cell_pixels_width - border_pixels,
                                             cell_y_pixel + cell_pixels_height - border_pixels))

                cell_image.save(f"Cells/{x}_{y}.png")

                cell_image = np.array(cell_image)
                cell_value = ColorDetection.detect_digit_in_cell(cell_image, self.bg_colors, self.templates)
                self.board[y][x] = cell_value

    def countFlags(self):
        flags = 0
        for y in range(0, self.height):
            for x in range(0, self.width):
                cell_value = self.board[y][x]
                if cell_value == self._FLAG_VALUE:
                    flags += 1
        return flags

    def getAllUnknownCells(self):
        cells = []
        for y in range(0, self.height):
            for x in range(0, self.width):
                cell_value = self.board[y][x]
                if cell_value == self._UNKNOWN_VALUE:
                    cells.append((x, y))
        return cells

    def getAllUndeclaredFlagsCells(self) -> set[tuple[int, int]]:
        cells_to_pop = set()
        self._setUpAllFlags()

        for x in range(0, self.width):
            for y in range(0, self.height):
                cell_value = self.board[y][x]
                if ((cell_value == self._UNKNOWN_VALUE) or
                        (self.is_auto_open and (cell_value == 0))):
                    continue

                flags_list = self._getAroundCellByValue(x, y, self._FLAG_VALUE)

                if len(flags_list) == cell_value:
                    unknown_list = self._getAroundCellByValue(x, y, self._UNKNOWN_VALUE)
                    if len(unknown_list) != 0:
                        for cell_index in unknown_list:
                            cells_to_pop.add(cell_index)
        return cells_to_pop

    def _setUpAllFlags(self) -> set[tuple[int, int]]:
        all_flags_list = set()
        for x in range(0, self.width):
            for y in range(0, self.height):
                cell_value = self.board[y][x]
                if cell_value is not None:
                    unknown_list = self._getAroundCellByValue(x, y, self._UNKNOWN_VALUE)
                    flags_list = self._getAroundCellByValue(x, y, self._FLAG_VALUE)
                    if (len(unknown_list) + len(flags_list)) == cell_value:
                        # locate flags
                        for new_flag_x, new_flag_y in unknown_list:
                            self.board[new_flag_y][new_flag_x] = self._FLAG_VALUE
                            all_flags_list.add((new_flag_x, new_flag_y))
        return all_flags_list

    def getRandomUnknownCell(self):
        for x in range(0, self.width):
            for y in range(0, self.height):
                if self.board[y][x] is self._UNKNOWN_VALUE:
                    return x, y
        return None

    def _getAroundCellByValue(self, cell_x, cell_y, wanted_value) -> list[tuple[int, int]]:
        value_indexes = []
        for x_diff in range(-1, 2):
            for y_diff in range(-1, 2):
                if ((x_diff == 0 and y_diff == 0) or
                        (x_diff + cell_x >= self.width) or
                        (y_diff + cell_y >= self.height) or
                        (x_diff + cell_x < 0) or
                        (y_diff + cell_y < 0)):
                    continue
                if self.board[cell_y + y_diff][cell_x + x_diff] == wanted_value:
                    value_indexes.append(((cell_x + x_diff),(cell_y + y_diff)))
        return value_indexes

    def printBoard(self):
        for row in self.board:
            print("|", end="")
            for cell in row:
                if cell is self._UNKNOWN_VALUE:
                    cell_str = "-"
                elif cell == self._FLAG_VALUE:
                    cell_str = "***"
                else:
                    cell_str = str(cell)
                print(f"{cell_str:^3}", end="|")
            print()
        print()