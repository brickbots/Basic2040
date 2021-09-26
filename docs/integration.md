# Basic2040 - Use in other projects

* [Home](../README.md)
* Integration into projects
* [Basic Dialect Details](dialect.md)

## Introduction

One of the goals of this project is to allow use of the BASIC engine in other projects without
needing to modify the basic2040 files.  That is to say the creating, loading, running, saving of BASIC
programs are fully implemented in the single basic2040 module and these can be 'wrapped' into various
interactive systems.

There are two classes that are intended to be base classes that can be subclassed to implement whatever
harware or implemtation changes you might want.

* `basic2040.term.SimpleTerm` - This class has all the methods and properties required to handle keyboard and
screen input.  If you are using an LCD screen display on a microcontroller, or doing your own keyboard matrix
scanning via GPIO pins, this is the place to implement that.


* `basic2040.interpreter.Interpreter` - This class implements an interactive basic shell that allows adding
of new program lines, listing the program, starting execution, saving and loading.  All of these actions
end up calling specific methods of the `basic2040.program.Program` class.  The Interpreter class is only
responsible for the user-experience of interacting with the basic program.  If you want to change the banner,
adjust how program listing works, such as adding pagination, or scrollback to edit... or otherwise change
the way the user interacts with the Basic2040 engine, this is the place.

The SimpleTerm and Interpreter class included are very functional and implement a complete solution for general
standard I/O systems.  Here is some example python code to fire them up:

```
from basic2040.interpreter import Interpreter
from basic2040.term import SimpleTerm


if __name__ == "__main__":
    # Create an instance of the Simple Terminal Class
    terminal = SimpleTerm()

    # Create an instance of the Interpreter class,
    # providing the terminal for IO
    i = Interpreter(terminal)

    # Call the main method of interpreter which
    # starts the interactive loop
    i.main()
```


For full details about other parts of Basic2040, see the Architecture section below.

## Architecture

The interpreter is implemented using the following Python classes:

* basictoken.py - This implements the tokens that are produced by the lexical analyser.
The class mostly defines token categories and provides a simple token pretty printing method.

* lexer.py - This class implements the lexical analyser. Lexical analysis is performed on
one statement at a time, as each statement is entered into the interpreter.

* basicparser.py - This class implements a parser for individual BASIC statements. This is
somewhat inefficient in that statements, for example those in a loop, must be re-parsed every
time they are executed. However, such a model allows us to develop an interactive interpreter
where statements can be gradually added to the program between runs.
Since the parser is oriented to the processing of individual statements, it uses a
signalling mechanism (using FlowSignal objects) to its caller indicate when program level actions
are required, such as recording the return address following a subroutine jump. However, the
parser does maintain a symbol table (implemented as a dictionary) in order to record
the value of variables as they are assigned.

* program.py - This class implements an actual basic program, which is represented as a dictionary. Dictionary keys are
statement line numbers and the corresponding value is the list of tokens that make up the statement with that line number.
Statements are executed by calling the parser to parse one statement at a time. This class
maintains a program counter, an indication of which line number should be executed next. The program counter is incremented to the next line
number in sequence, unless executed a statement has resulted in a branch. The parser indicates this by signalling to the program object that
calls it using a FlowSignal object.

* interpreter.py - This class provides the interface to the user. It allows the user to both input program statements and to execute
the resulting program. It also allows the user to run commands, for example to save and load programs, or to list them.

* flowsignal.py - Implements a FlowSignal object that allows the parser to signal a change in control flow. For example, as
the result of a jump defined in the statement just parsed (GOTO, conditional branch evaluation), a loop decision,
a subroutine call, or program termination. This paradigm of using the parser to simply parse individual statements, the Program
object to make control flow decisions and to track execution, and a signalling mechanism to allow the parser to signal
control flow changes to the Program object, is used consistently throughout the implementation.

* term.py - Implements a terminal for character based input/output.  This object is passed to other classes for use.  The simpleterm example uses normal python input/output but more sophisticated options are available with screen positioning and other features.

