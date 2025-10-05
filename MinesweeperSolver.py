from time import time, sleep
from Adapters import ScreenAdapter
from Adapters.mouseAdapter import *
from Board import Board
from main import *

def _convertBoardIndexesToScreenPixels(cell_x, cell_y):
    screen_x = SCREEN_START_X + (cell_x * SCREEN_CELL_WIDTH) + (SCREEN_CELL_WIDTH / 2)
    screen_y = SCREEN_START_Y + (cell_y * SCREEN_CELL_HEIGHT) + (SCREEN_CELL_HEIGHT / 2)
    return screen_x, screen_y

def solve():
    cells_clicked = 0
    algorithm_rounds = 0
    randoms_picks = 0 # first pick doesnt count
    board = Board(BOARD_WIDTH, BOARD_HEIGHT, BOARD_TEMPLATES_PATH, BOARD_BG_COLORS, IS_AUTO_OPEN)

    start_time = time()

    # first pick
    clickCellsOnScreen([(int(board.width / 2), int(board.height / 2))])
    sleep(ANIMATION_TIME)

    while board.countFlags() < FLAGS_AMOUNT:
        algorithm_rounds += 1
        MouseMove((10,10))
        syncBoard(board)

        cells_to_pop = board.getAllUndeclaredFlagsCells()

        # Random pick
        while len(cells_to_pop) == 0:
            # sync again maybe the pop hist problem
            sleep(ANIMATION_TIME)
            syncBoard(board)
            cells_to_pop = board.getAllUndeclaredFlagsCells()

            if (len(cells_to_pop) != 0) or (board.countFlags() == FLAGS_AMOUNT):
                break

            board.printBoard()
            input("I think i have no valid cells,\nPlease pop a cell on the board and then Press Enter to continue...")
            syncBoard(board)

        cells_clicked += len(cells_to_pop)
        clickCellsOnScreen(cells_to_pop)
        print(f"We founded: {board.countFlags()}/{FLAGS_AMOUNT} flags")

    # click all unknown left cells
    left_cells = board.getAllUnknownCells()
    clickCellsOnScreen(left_cells)

    print(f"{">" * (BOARD_WIDTH * 2 - 3)} Done {"<" * (BOARD_WIDTH * 2 - 3)}")
    board.printBoard()
    print(f"""
stats:
  > time: {time() - start_time}
  > random picks: {randoms_picks}
  > algorithm rounds: {algorithm_rounds}
  > cells clicked: {cells_clicked}
""")

def clickCellsOnScreen(cells_to_click):
    try:
        for x, y in cells_to_click:
            cell_pixels = _convertBoardIndexesToScreenPixels(x, y)
            MouseLeftClick(cell_pixels)
    except TypeError:
        pass

def putFlagsInBoard(flags_to_put):
    try:
        for x, y in flags_to_put:
            cell_pixels = _convertBoardIndexesToScreenPixels(x, y)
            MouseRightClick(cell_pixels)
    except TypeError:
        pass

def syncBoard(board):
    board_screenshot = ScreenAdapter.ScreenShot(SCREEN_START_X, SCREEN_START_Y, BOARD_WIDTH * SCREEN_CELL_WIDTH, BOARD_HEIGHT * SCREEN_CELL_HEIGHT)
    board.updateByScreenshot(board_screenshot, SCREEN_CELL_WIDTH, SCREEN_CELL_HEIGHT, SCREEN_CELL_BORDER)