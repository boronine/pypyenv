(The most proper way of making a PyPy virtualenv is described 
[here](http://morepypy.blogspot.com/2010/08/using-virtualenv-with-pypy.html))

With this script you can easily install PyPy in a virtualenv side by side 
with CPython (they will share `site-packages`), it is useful if you want to experiment 
with PyPy without having to set up a dedicated virtualenv. There is one gotcha 
pointed out by
[Antonio Cuni](http://morepypy.blogspot.com/2010/08/using-virtualenv-with-pypy.html?showComment=1281032216014#c8756700725521226531):
you won't be able to run CPython's C extensions with PyPy (this gotcha does not
apply to the standard library, since it will not be shared).

This script supports Linux and (experimentally) OS X.

    source myenv/bin/activate
    easy_install pypyenv
    pypyenv install         # Tries to install PyPy with JIT
    pypyenv --nojit install # Forces non-JIT installation
    pypyenv uninstall       # Uninstalls PyPy from virtualenv

pypyenv will create a `pypy` executable in your virtualenv's `bin` folder,
but will not change your current `python` executable by default. If you want
to use PyPy exclusively in your virtualenv, do the following:

    cd path/to/my/env
    cd bin
    mv python python.bak
    ln -s pypy python

Good luck!

