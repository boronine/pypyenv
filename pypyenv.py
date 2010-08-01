import os
import sys
import urllib2
import tarfile
import shutil
import stat
import getopt
import platform

__version__ = "0.1"

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
    # Unpack archive
    archiveobj = tarfile.open(archive, mode="r:bz2")
    unpacked = os.path.join(srcdir, archiveobj.next().name)
    if os.path.exists(unpacked):
        out("deleting ENV/%s" % unpacked)
        shutil.rmtree(unpacked)
    out("unpacking archive")
    try:
        archiveobj.extractall(srcdir)
    except EOFError:
        # FIXME: Investigate why this sometimes only works on the second try
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
 pypyenv uninstall - uninstalls PyPy from this virtualenv
           --nojit - Install non-JIT version."""

def main():
    if version != "2.5":
        if not raw_input("PyPy implements Python 2.5, you are using a " \
                         "different version, continue? [y/N] ") in yes:
           sys.exit(1) 
    try:
        opts, args = getopt.getopt(sys.argv[1:], "", ["nojit"])
    except getopt.GetoptError:
        print help_message
        sys.exit(2)

    if len(args) != 1:
        print help_message
        sys.exit(2)

    nojit = False
    for o, a in opts:
        if o == "--nojit": 
            nojit = True
    jit = not nojit

    osx = platform.system() == "Darwin"
    win = platform.system() == "Windows"
    linux = not osx and not win

    x86_64 = platform.machine() == "x86_64"
    x86 = not x86_64

    if win:
        print "Supports only Linux and OS X at this point"
        sys.exit(2)
    if x86_64 and jit:
        print "JIT is not supported on x86_64, rerun with --nojit"
        sys.exit(2) 

    if linux and x86 and jit:
        download = "http://pypy.org/download/pypy-1.3-linux.tar.bz2"
    if linux and x86 and nojit:
        download = "http://pypy.org/download/pypy-1.3-linux-nojit.tar.bz2"
    elif linux and x86_64:
        download = "http://pypy.org/download/pypy-1.3-linux64-nojit.tar.bz2"
    elif osx and jit:
        download = "http://pypy.org/download/pypy-1.3-osx.tar.bz2"
    elif osx and nojit:
        download = "http://pypy.org/download/pypy-1.3-osx-nojit.tar.bz2"

    if args[0] == "install":
        install(download)
    elif args[0] == "uninstall":
        uninstall()
    else:
        print help_message

