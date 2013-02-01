Xerblin
=======

General User Interface Metaphor

## Summary

It provides a single metaphor for interacting with computers that's simple enough to teach to children yet provides facilities that are useful to programmers. It integrates all levels of software from the desktop to assembly language.

There are three basic user-facing elements to a Xerblin system.

*    Stack - a place to put objects for user manipulation. This is similar to a Clipboard but it can hold more than one item at a time. Commands operate on the items on the Stack.
*    Dictionary - a place to keep commands. Any command that is inscribed in the Dictionary can be run from the user interface.
*    Interpreter - A very simple command interpreter that takes care of running commands with the Stack.

In addition to the above three UI elements there are discrete commands that provide the basic functionality of the system and that can be composed into more complex commands. They live in the Dictionary and act upon the Stack. They can be composed into compound commands using three primal relations:

*    Sequence - do one thing after another.
*    Loop - do something over again.
*    Branch - do one thing or another.

Using the above three relations compound commands can be composed to perform more involved tasks using the built-in or user-provided "primitives" and other compound commands.  Composition can be done by program, by command line, in the GUI using the mouse and keyboard, or by means of parsing languages.

With a rich set of basic commands and the three kinds of compound commands you have a completely general computer interface that allows for customization and flexibility and can be easily understood and mastered by the average user.

### Some links:

*   The [old project on Google Code][a]. This is still the reference implementation.
*   [Pigeon Computer][b] is a project I have to develop a simple system to teach computer programing. It includes both a low-level version in assembly language and a high-level version in Python with a Tkinter GUI.

### Historical Info

Way back in the day, over a decade ago, the original source for what became "xerblin" was a book ["System Design from Provably Correct Constructs"][c] by [Dr. James Martin][d] [founder, Oxford Martin School][e] ([personal website][f]).

### Must mention:

I need to expand on each of these eventually.

*   Oberon (Wirth, et. al.)
*   Forth (Moore, et. al.)
*   Jef Raskin, "The Humane Interface"
*   Ted Nelson, "Dream Machines"/"Computer Lib"
*   Alan Kay, Dynabook, VPRI et. al.
*   Chris Okasaki, "Purely Functional Data Structures"



[a]: https://code.google.com/p/xerblin/
[b]: http://thinkpigeon.blogspot.com/?view=mosaic

[c]: http://lccn.loc.gov/84016063 "System Design from Provably Correct Constructs"
[d]: https://en.wikipedia.org/wiki/James_Martin_%28author%29 "Dr. Martin on Wikipedia"
[e]: http://www.oxfordmartin.ox.ac.uk/founder/
[f]: http://www.jamesmartin.com/



## Installation

I use virtualenv and pip on an Ubuntu Linux system and installation from GitHub is straightforward:


    sforman@callix:~$ git clone git@github.com:PhoenixBureau/Xerblin.git
    sforman@callix:~$ virtualenv virt-env
    sforman@callix:~$ source ./virt-env/bin/activate
    (virt-env)sforman@callix:~$ cd Xerblin/
    (virt-env)sforman@callix:~/Xerblin$ pip install -r requirements.txt

    ...snip...

    Successfully installed Flask dulwich Werkzeug Jinja2
    Cleaning up...
    (virt-env)sforman@callix:~/Xerblin$ python main.py
     * Running on http://127.0.0.1:5000/
     * Restarting with reloader


Or, if you prefer all the commands by themselves in a script:

    git clone git@github.com:PhoenixBureau/Xerblin.git
    virtualenv virt-env
    source ./virt-env/bin/activate
    cd Xerblin/
    pip install -r requirements.txt
    python main.py

### Three Xerblins.

There are *two* entry points to the server, `main.py` which runs a Xerblin interpreter in the server but does _not_ store the history to disk, and `run.py` which _does_ store history to disk and uses the Dulwich git library to store the history in a git repository.

If you start either version a Flask server is created that serves two versions of a webpage that contains an interface to a Xerblin interpreter

*  The "root" URL ('/') serves a self-contained webpage (dependencies are loaded from a CDN) that has the interpreter in Javascript.  You can save this page and edit it to play with a one-page web-based Xerblin.
* The `/foo` URL serves a varient of the same page that connects (with AJAX) to the server-based Python Xerblin interpreter, which allows the webpage to serve as an interface to it.

If you use the `run.py` entry point you can tell it which directory to use. The _first_ time you run the server with the git history store you must use the `--init` switch, after that you must leave it off. (I know that's a little clumsy, I may change it in the future.)

Here is the output of the `-h` switch which shows the command line options for the `run.py` server entry point:

    (virt-env)sforman@callix:~/Xerblin$ python run.py -h
    usage: run.py [-h] [-r ROOST] [-i]

    optional arguments:
      -h, --help            show this help message and exit
      -r ROOST, --roost ROOST
                            Use this directory as home for the Pigeon system.
                            (default: $HOME/.pigeon). (I apologize for the
                            terrible pun.)
      -i, --init            Initialize the "roost" directory with git repo, log,
                            system.pickle and default config file. If '--no-
                            config' is passed the default config file will NOT be
                            created.)









