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

"""This class implements a BASIC interpreter that
presents a prompt to the user. The user may input
program statements, list them and run the program.
The program may also be saved to disk and loaded
again.

"""

from .basictoken import BASICToken as Token
from .lexer import Lexer
from .program import Program
from sys import stderr
from gc import collect


class Interpreter:
    """
    Implements an interactive interpreter which
    feeds commands to a PyBasic program object
    and allows running the program and listing
    lines
    """

    def __init__(self, terminal=None, debug=False):
        """
        Terminal must be a compatible class, see term.py for reference
        implementation

        If debug is True, the main exception handler is bypassed so
        full tracebacks can propigate
        """

        self.lexer = Lexer()
        if not terminal:
            from .term import SimpleTerm

            self._terminal = SimpleTerm()
        else:
            self._terminal = terminal

        # Garbage collect
        collect()
        self.program = Program(self._terminal)
        self.debug = debug

    def main(self):
        """
        Primary entry point for the interpretation
        loop. Can be overloaded in subclassing to
        implement custom startup behavior
        """
        banner = """
  ___   _   ___ ___ ___ ___ __  _ _   __
 | _ ) /_\\ / __|_ _/ __|_  )  \\| | | /  \\
 | _ \\/ _ \\\\__ \| | (__ / / () |_  _| () |
 |___/_/ \\_\\___/___\\___/___\\__/  |_| \\__/
              """
        self._terminal.print(banner)
        self._interpreter()

    def _list(self, start_line=None, end_line=None):
        """
        Handles textual listing of a program to the screen.
        can be overwritten to implement pagination or other
        hardware or use case specific behavior
        """
        line_numbers = self.program.line_numbers()
        if len(line_numbers) == 0:
            return

        if not start_line:
            start_line = int(line_numbers[0])

        if not end_line:
            end_line = int(line_numbers[-1])

        for line_number in line_numbers:
            if int(line_number) >= start_line and int(line_number) <= end_line:
                self._terminal.print(str(self.program.str_statement(line_number)))

    def _interpreter(self, prompt="> "):

        # Continuously accept user input and act on it until
        # the user enters 'EXIT'
        while True:
            self._terminal.write(prompt)
            stmt = self._terminal.input()

            try:
                tokenlist = self.lexer.tokenize(stmt)

                # Execute commands directly, otherwise
                # add program statements to the stored
                # BASIC program

                if len(tokenlist) > 0:

                    # Exit the interpreter
                    if tokenlist[0].category == Token.EXIT:
                        break

                    # Add a new program statement, beginning
                    # a line number
                    elif (
                        tokenlist[0].category == Token.UNSIGNEDINT
                        and len(tokenlist) > 1
                    ):
                        self.program.add_stmt(tokenlist)

                    # Delete a statement from the program
                    elif (
                        tokenlist[0].category == Token.UNSIGNEDINT
                        and len(tokenlist) == 1
                    ):
                        self.program.delete_statement(int(tokenlist[0].lexeme))

                    # Execute the program
                    elif tokenlist[0].category == Token.RUN:
                        try:
                            self.program.execute()

                        except KeyboardInterrupt:
                            self._terminal.print("Program terminated")

                    # List the program
                    elif tokenlist[0].category == Token.LIST:
                        if len(tokenlist) == 2:
                            self._list(
                                int(tokenlist[1].lexeme), int(tokenlist[1].lexeme)
                            )
                        elif len(tokenlist) == 3:
                            # if we have 3 tokens, it might be LIST x y for a range
                            # or LIST -y or list x- for a start to y, or x to end
                            if tokenlist[1].lexeme == "-":
                                self._list(None, int(tokenlist[2].lexeme))
                            elif tokenlist[2].lexeme == "-":
                                self._list(int(tokenlist[1].lexeme), None)
                            else:
                                self._list(
                                    int(tokenlist[1].lexeme), int(tokenlist[2].lexeme)
                                )
                        elif len(tokenlist) == 4:
                            # if we have 4, assume LIST x-y or some other
                            # delimiter for a range
                            self._list(
                                int(tokenlist[1].lexeme), int(tokenlist[3].lexeme)
                            )
                        else:
                            self._list()

                    # Save the program to disk
                    elif tokenlist[0].category == Token.SAVE:
                        filepath = tokenlist[1].lexeme
                        if "/" not in filepath:
                            filepath = "BAS/" + filepath
                        self.program.save(filepath)
                        self._terminal.print("Program written to file")

                    # Load the program from disk
                    elif tokenlist[0].category == Token.LOAD:
                        filepath = tokenlist[1].lexeme
                        if "/" not in filepath:
                            filepath = "BAS/" + filepath
                        self.program.load(filepath)
                        self._terminal.print("Program read from file")

                    # Delete the program from memory
                    elif tokenlist[0].category == Token.NEW:
                        self.program.delete()
                        self.program = None
                        # Opportunity for GC here
                        collect()
                        self.program = Program(self._terminal)

                    elif tokenlist[0].category == Token.CLEAR:
                        self._terminal.clear()

                    # Unrecognised input
                    else:
                        self._terminal.print("Unrecognised input")
                        for token in tokenlist:
                            self._terminal.print(str(token))

            # Trap all exceptions so that interpreter
            # keeps running
            except Exception as e:
                if self.debug == True:
                    raise (e)
                else:
                    self._terminal.print(str(e))
