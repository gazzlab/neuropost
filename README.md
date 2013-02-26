Display Neurological Data
=========================

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


