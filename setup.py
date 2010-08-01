#!/usr/bin/python

# Use setuptools if we can
try:
    from setuptools.core import setup
except ImportError:
    from distutils.core import setup
from pypyenv import __version__

setup(
    name='pypyenv',
    version=__version__,
    description='Install PyPy in virtualenv',
    long_description="Install PyPy as an optional Python 2.5 interpretor "\
        "in a virtualenv on Linux and OS X systems.",
    author="Alexei Boronine",
    license="MIT",
    author_email="alexei.boronine@gmail.com",
    url="http://github.com/alexeiboronine/pypyenv",
    download_url="http://github.com/alexeiboronine/pypyenv/downloads",
    keywords="pypy virtualenv",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development"
    ],
    py_modules=["pypyenv"],
    entry_points = {
        'console_scripts': [
            'pypyenv = pypyenv:main'
        ]
    }
)
