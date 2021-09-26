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
The 2040 in Basic2040 refers to a popular Circuit Python compatible microcontroller, the Pi2040, which
is available as part of several different boards.

The primary differences from PyBasic are:
* Core BASIC engine code cleanly encapsulated in the basic2040 module so it can be used without modification in other projects
* I/O Abstration to allow various screen/keyboard setups
* Easy ability to add new BASIC functions/keywords for enabling hardware specific functions
* Lower memory usage at the expense of code complexity



## Example Implementations

An example interpreter can be invoked as follows:

```
$ python example.py
```

## Terminals


One of the key features of Basic2040 is a that all IO (Keyboard/Screen) is abstracted into
a terminal class that can be adapted to many specific use-cases.  The command above will 
start the standard Basic2040 interpreter connected to stdio and should be compatible with 
all systems that can run python.  

Also included is an example curses based terminal class.  Basic2040 includes some extra screen control 
features, such as CLEAR to clear the screen, and the `CURSOR` command allow printing at specific 
screen locations.  To use these features the terminal class used must support them.  The example
curses terminal does just this.

```
$ python example_curses.py
```

The curses based terminal class also has a scrollback and bell functionality.  Use the up/down
arrows to scroll back previous commands.  A left arrow will clear the current line.

For specific hardware situations the Terminal class in term.py can be implemented to handle
IO from non-standard keyboards/screens.  This is handy for specific hardware
projects using CircuitPython comptible microcontrollers.  See my [PicoBasic](https://github.com/brickbots/PicoBasic)
repo for examples using various screen/keyboard options for microcontrollers.

## Example programs

A number of example BASIC programs have been supplied in the repository, in the examples directory:

* *regression.bas* - A program to exercise the key programming language constructs
in such a way as to allow verification that the interpreter is functioning correctly.

* *factorial.bas* - A simple BASIC program to take a number, *N*, as input from the user and
calculate the corresponding factorial *N!*.

* *rock_scissors_paper.bas* - A BASIC implementation of the rock-paper-scissors game.

* *PyBStartrek.bas* - A port of the 1971 Star Trek text based strategy game.

* *adventure-fast.bas* - A port of a 1979 text based adventure game.

* *bagels.bas* - A guessing game.

* *eliza.bas* - A port of the early chatbot, posing as a therapist, originally created by Joseph Weizenbaum in 1964.

## Open issues

* It is not possible to renumber a program. This would require considerable extra functionality.
* Negative values are printed with a space (e.g. '- 5') in program listings because of tokenization. This does not affect functionality.
* Decimal values less than one must be expressed with a leading zero (i.e. 0.34 rather than .34)
* User input values cannot be directly assigned to array variables in an **INPUT** or **READ** statement
* Strings representing numbers (e.g. "10") can actually be assigned to numeric variables in **INPUT** and **READ** statements without an
error, Python will silently convert them to integers.

## License

Basic2040 is made available under the GNU General Public License, version 3.0 or later (GPL-3.0-or-later).
