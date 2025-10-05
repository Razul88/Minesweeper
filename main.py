import keyboard
import os
import threading

import MinesweeperSolver
from Configs_files.google.medium_level.config import *


def stop_listener():
    keyboard.wait("esc")
    print(">> ESC pressed, stoping...")
    os._exit(0)

def main():
    threading.Thread(target=stop_listener, daemon=True).start()
    MinesweeperSolver.solve()

if __name__ == '__main__':
    main()

stam = BOARD_WIDTH # so the import won't be gray
