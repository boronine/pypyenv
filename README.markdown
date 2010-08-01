As of this writing, PyPy isn't supported by virtualenv, fiddling with both,
I found a way to use them together and made this script to simplify it for
other developers. Supports Linux and (experimentally) OS X.

    workon myenv
    easy_install pypyenv
    pypyenv install # Tries to install PyPy with JIT
    pypyenv --nojit install # Forces non-JIT installation
    pypyenv uninstall # Uninstalls PyPy from virtualenv

pypyenv will create a `pypy` executable in your virtualenv's `bin` folder,
but will not change your current `python` executable by default. If you want
to use PyPy exclusively in your virtualenv, do the following:

    cd path/to/my/env
    cd bin
    mv python python.bak
    ln -s pypy python

Good luck!

