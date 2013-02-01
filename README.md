Xerblin
=======

General User Interface Metaphor

## Summary

It provides a single metaphor for interacting with computers that's simple enough to teach to children yet provides facilities that are useful to programmers. It can integrate all levels of software from the desktop to assembly language.

There are three basic user-facing elements to a Xerblin system.

*    Stack - a place to put objects for user manipulation. This is similar to a Clipboard but it can hold more than one item at a time. Commands operate on the items on the Stack.
*    Dictionary - a place to keep commands. Any command that is inscribed in the Dictionary can be run from the user interface.
*    Interpreter - A very simple command interpreter that takes care of running commands with the Stack.

In addition to the above three UI elements there are discrete commands that provide the basic functionality of the system and that can be composed into more complex commands. They live in the Dictionary and act upon the Stack. They can be composed into compound commands using three primal relations:

*    Sequence - do one thing after another.
*    Loop - do something over again.
*    Branch - do one thing or another.

Using the above four relations compound commands can be composed to perform more involved tasks using the built-in or user-provided "primitives" and other compound commands.

Composition can be done by program, by command line, in the GUI using the mouse and keyboard, or by means of parsing languages.

With a rich set of basic commands and the four kinds of compound commands you have a completely general computer interface that allows for customization and flexibility and can be easily understood and mastered by the average user.

### Some links:

    The old project on Google Code. This is still the reference implementation.
    Pigeon Computer is a project I have to develop a simple system to teach computer programing. It includes both a low-level version in assembly language and a high-level version in Python with a Tkinter GUI.
    Experimental web versions. The Python version embedded in a Flask server, and a Javascript port of the Xerblin engine along with a couple of demo pages.

### Historical Info

Way back in the day, over a decade ago, the original source for what became "xerblin" was a book "System Design from Provably Correct Constructs" by Dr. James Martin founder, Oxford Martin School (personal website).

### Must mention:

*   Oberon (Wirth, et. al.)
*   Forth (Moore, et. al.)
*   Jef Raskin, "The Humane Interface"
*   Ted Nelson, "Dream Machines"/"Computer Lib"
*   Dynabook, (Kay et. al.) 
*   Chris Okasaki, "Purely Functional Data Structures"


