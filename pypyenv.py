import os
import sys
import urllib2
import tarfile
import shutil
import stat
import getopt
import platform

__version__ = "0.1.2"

base = sys.prefix
srcdir = "src"
bindir = "bin"
binpypy = os.path.join(bindir, "pypy")
pypydir = "pypy"

version = sys.version[:3]
yes = ("y","yes")

def out(s):
    print " * " + s

def install(download):
    os.chdir(base)
    # Clean up if anything was left over
    uninstall()
    # Create src directory
    if not os.path.exists(srcdir):
        out("creating ENV/%s directory" % srcdir)
        os.mkdir(srcdir)
    archive = os.path.join(srcdir, download.split("/")[-1])
    # Download archive
    if os.path.exists(archive):
        out("using previously downloaded ENV/%s" % archive)
    else:
        out("downloading PyPy")
        urlfile = urllib2.urlopen(download)
        archivefile = open(archive, "w")
        while True:
            data = urlfile.read(4096)
            if not data:
                break
            archivefile.write(data)
        archivefile.close()
    # Unpack archive
    archiveobj = tarfile.open(archive, mode="r:bz2")
    unpacked = os.path.join(srcdir, archiveobj.next().name)
    if os.path.exists(unpacked):
        out("deleting ENV/%s" % unpacked)
        shutil.rmtree(unpacked)
    out("unpacking archive")
    archiveobj.extractall(srcdir)
    # Copying PyPy directory into virtualenv root
    out("copying PyPy directory into root")
    shutil.copytree(unpacked, pypydir)
    # Install PyPy executable symlink
    out("installing ENV/%s symlink" % binpypy)
    os.symlink(os.path.join("..", "pypy", "bin", "pypy"), binpypy)
    out("giving it execute permissions")
    os.chmod(binpypy, stat.S_IXUSR)
    # Install site-packages symlink
    pythonsite = os.path.join("..", "lib", "python" + version, "site-packages")
    pypysite = os.path.join("pypy", "site-packages")
    out("installing ENV/%s symlink" % pypysite)
    shutil.rmtree(pypysite)
    os.symlink(pythonsite, pypysite)

def uninstall():
    os.chdir(base)
    if os.path.exists(binpypy): 
        if confirm_deletion(binpypy):
            os.remove(binpypy)
        else:
            sys.exit(1)
    if os.path.exists(pypydir):
        if confirm_deletion(pypydir):
            shutil.rmtree(pypydir)
        else:
            sys.exit(1)

def confirm_deletion(tree):
    return raw_input("Delete ENV/%s? [y/N] " % tree) in yes

help_message = """   pypyenv install - installs PyPy in this virtualenv
 pypyenv uninstall - uninstalls PyPy from this virtualenv"""

def main():
    if version != "2.7":
        if not raw_input("PyPy implements Python 2.7, you are using a " \
                         "different version, continue? [y/N] ") in yes:
           sys.exit(1) 

    if len(args) != 1:
        print help_message
        sys.exit(2)

    osx = platform.system() == "Darwin"
    win = platform.system() == "Windows"
    linux = not osx and not win

    x86_64 = platform.machine() == "x86_64"
    x86 = not x86_64

    if win:
        print "Supports only Linux and OS X at this point"
        sys.exit(2)

    if linux and x86:
        download = "https://bitbucket.org/pypy/pypy/downloads/pypy-1.7-linux.tar.bz2"
    elif linux and x86_64:
        download = "https://bitbucket.org/pypy/pypy/downloads/pypy-1.7-linux64.tar.bz2"
    elif osx:
        download = "https://bitbucket.org/pypy/pypy/downloads/pypy-1.7-osx64.tar.bz2"

    if args[0] == "install":
        install(download)
    elif args[0] == "uninstall":
        uninstall()
    else:
        print help_message

