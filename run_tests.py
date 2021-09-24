import sys
from basic2040.term import TestTerm
from basic2040.program import Program


def main():
    try:
        print("+++++++++ TESTS STARTING +++++")
        terminal = TestTerm()
        test_program = Program(terminal)
        test_program.load("BAS/tests.bas")
        test_program.execute()
        print("+++++++++ TESTS COMPLETE +++++")
        # Exit with success code
        sys.exit(0)
    except Exception as e:
        print(str(e))
        print("Last line output:")
        print(terminal.get_last_line())
        # Exit with failure code
        sys.exit(-1)


if __name__ == "__main__":
    main()
