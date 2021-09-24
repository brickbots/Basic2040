# SPDX-License-Identifier: GPL-3.0-or-later
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


"""
This file implements a simple stdio based terminal class compatible with
Basic2040.  A terminal object needs to be provided to the
program class to enable BASIC print/input and other character
based IO operations.

Also included here is the 'testing' terminal that uses the input/output
of a basic program for validating the basic module functionality
"""


class SimpleTerm:
    def __init__(self):
        return

    def print(self, to_print):
        """
        Print send the provided string to the terminal
        followed by a CR/LF
        """
        print(to_print)

    def write(self, to_write):
        """
        write sends the provided string to the terminal
        but does not include any other control chars
        """
        print(to_write, end="")

    def enter(self):
        """
        Move down one line, and all the wya to the left.
        Equivilent of CR/LF combo
        """
        print()

    def clear(self):
        """
        Clears the screen.
        Not Implemented here
        """
        raise Exception("Not Implemented by terminal")

    def home(self):
        """
        Returns the cursor to home position
        Not implemented here
        """
        raise Exception("Not Implemented by terminal")

    def cursor(self, x, y):
        """
        Moves the cursor to the specified x (column)
        and y (row) position on screen
        Not implemented here
        """
        raise Exception("Not Implemented by terminal")

    def input(self):
        """
        Retrieves a string terminated by CR from the termnial
        This will echo to the screen
        """
        return input()

    def get_char(self):
        """
        Retrieves a single character from the terminal
        and returns it ASCII code as integer.  This is
        to allow for various special codes/characters for
        buttons/arrows.

        Block until recieved, does not echo

        Not implemented well here as it requires more
        OS specific code or curses
        """
        return ord(input()[0])

    def poll_char(self):
        """
        Checks keyboard state.  Returns zero if no key is pressed
        or integer representing the key (ASCII code for most keys).
        This allows special keys/buttons to be returned above or
        below normal ASCII code range

        Not implemnted here as it requires more OS specific
        business
        """
        return 0

    def is_esc(self):
        """
        Returns true if escape is currently pressed.  Used to generate
        keyboard interrupt of a running program on devices without
        ctrl-c capbilities
        """
        return False


class TestTerm(SimpleTerm):
    """
    A class that serves as a test harness for
    running basic programs to test functionality


    Intercepts any print statements and behaves
    as follows depending on line start:
        * Test name

        : Expected value
        line following expected value is compared

    """

    def __init__(self):

        self.__testname = None
        self.__expected = None
        self.__result = None

        self.__currentstring = ""

    def eval_line(self):
        """
        Called after each line end
        """
        line_token = self.__currentstring[:1]
        if line_token == "*":
            if self.__testname or self.__expected:
                raise Exception(
                    "TEST ERROR: New Test Started before previous test complete"
                )
            else:
                self.__testname = self.__currentstring[1:]
        elif line_token == ":":
            if self.__testname == None:
                raise Exception(
                    "TEST ERROR: Not ready for expected value no test started"
                )
            if self.__expected:
                raise Exception(
                    "TEST ERROR: Expected value provided, but test still pending"
                )
            self.__expected = self.__currentstring[1:]
        else:
            if self.__testname == None or self.__expected == None:
                raise Exception("TEST ERROR: Undelimited string without test setup")
            self.__result = self.__currentstring
            self.eval_test()

        self.__currentstring = ""

    def eval_test(self):
        """
        Called for each test after result is gathered
        """
        print("TEST: " + self.__testname)
        if self.__result != self.__expected:
            print("\tFAILED")
            print("\tExpected: " + self.__expected)
            print("\tResult:   " + self.__result)
            raise Exception("TEST FAILED")

        if self.__result == self.__expected:
            print("\tPASSED")

        self.__testname = None
        self.__expected = None
        self.__result = None

    def print(self, to_print):
        """
        Print send the provided string to the terminal
        followed by a CR/LF
        """
        self.__currentstring += str(to_print)[:-1]
        self.eval_line()

    def write(self, to_write):
        """
        write sends the provided string to the terminal
        but does not include any other control chars
        """
        self.__currentstring += str(to_write)

    def enter(self):
        """
        Move down one line, and all the way to the left.
        Equivilent of CR/LF combo
        """
        self.eval_line()

    def get_last_line(self):
        return self.__currentstring
