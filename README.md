Display Neurological Data
=========================

## Installation

I use virtualenv and pip on an Ubuntu Linux system and installation from GitHub is straightforward:


    $ git clone git@github.com:gazzlab/neuropost.git
    $ virtualenv virt-env
    $ source ./virt-env/bin/activate
    (virt-env)$ cd neuropost/
    (virt-env)neuropost$ pip install -r requirements.txt

    ...snip...

    Successfully installed Flask dulwich Werkzeug Jinja2
    Cleaning up...
    (virt-env)neuropost$ python main.py
     * Running on http://127.0.0.1:5000/
     * Restarting with reloader


Or, if you prefer all the commands by themselves in a script:

    git clone git@github.com:gazzlab/neuropost.git
    virtualenv virt-env
    source ./virt-env/bin/activate
    cd neuropost/
    pip install -r requirements.txt
    python main.py


