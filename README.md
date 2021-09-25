```
  ___   _   ___ ___ ___ ___ __  _ _   __
 | _ ) /_\ / __|_ _/ __|_  )  \| | | /  \
 | _ \/ _ \\__ \| | (__ / / () |_  _| () |
 |___/_/ \_\___/___\___/___\__/  |_| \__/

>
```
# A Modular BASIC Interpreter for Embedded Systems 

Read on for an overview or jump right to information on:
* [Integration into projects](docs/integration.md)
* [BASIC Dialect details](docs/dialect.md)

## Introduction

Originally forked from the excellent [PyBasic](https://github.com/richpl/PyBasic), this version has been 
restructured to make it easy to use as a module in other proejcts, specifically embedded systems running 
Circuit/Micro python.  It still runs in cPython, but has been optimized for lower memory environments.

The primary differences from PyBasic are:
* Core code in the basic2040 module so it can be used without modification in other projects
* I/O Abstration to allow various screen/keyboard setups
* Easy ability to add new BASIC functions/keywords for enabling hardware specific functions
* Lower memory usage at the expense of code complexity


The interpreter can be invoked as follows:

```
$ python example.py
```

Although this started of as a personal project, it has been enhanced considerably by some other Github users. You can see them in the list of contributors! It's very much a group endeavour now.

## Terminals

The command above will start the standard PyBasic interpreter connected to
stdio and should be compatible with all systems that can run python.  There are
some extra screen control features, such as CLEAR to clear the screen, and the
ability to print at specific screen locations that can be enabled by using a
curses enabled terminal.

```
$ python example_curses.py
```

This should work on most implementations of python on full OS's.  For specific
hardware situations the Terminal class in term.py can be implemented to handle
IO from non-standard keyboards/screens.  This is handy for specific hardware
projects using CircuitPython comptible microcontrollers.


## Architecture

The interpreter is implemented using the following Python classes:

* basictoken.py - This implements the tokens that are produced by the lexical analyser. The class mostly defines token categories
and provides a simple token pretty printing method.

* lexer.py - This class implements the lexical analyser. Lexical analysis is performed on one statement at a time, as each statement is
entered into the interpreter.

* basicparser.py - This class implements a parser for individual BASIC statements. This is somewhat inefficient in that statements,
for example those in a loop, must be re-parsed every time they are executed. However, such a model allows us to develop an
interactive interpreter where statements can be gradually added to the program between runs.
Since the parser is oriented to the processing of individual statements, it uses a
signalling mechanism (using FlowSignal objects) to its caller indicate when program level actions are required, such as recording the return address
following a subroutine jump. However, the parser does maintain a symbol table (implemented as a dictionary) in order to record
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

## Open issues

* It is not possible to renumber a program. This would require considerable extra functionality.
* Negative values are printed with a space (e.g. '- 5') in program listings because of tokenization. This does not affect functionality.
* Decimal values less than one must be expressed with a leading zero (i.e. 0.34 rather than .34)
* User input values cannot be directly assigned to array variables in an **INPUT** or **READ** statement
* Strings representing numbers (e.g. "10") can actually be assigned to numeric variables in **INPUT** and **READ** statements without an
error, Python will silently convert them to integers.

## License

PyBasic is made available under the GNU General Public License, version 3.0 or later (GPL-3.0-or-later).
