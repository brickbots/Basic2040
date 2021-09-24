from basic2040 import interpreter
from cursesterm import CursesTerm
from curses import wrapper


def main(stdscr):
    terminal = CursesTerm(stdscr)
    interpreter.Interpreter(terminal).main()


if __name__ == "__main__":
    wrapper(main)
