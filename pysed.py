#!/usr/bin/env python3
__author__ = 'Mahmoud Adel <mahmoud.adel2@gmail.com>'
__version__ = 0.4
__license__ = "The MIT License (MIT)"

import re
from typing import List


class Pair:
    def __init__(self, oldstr, newstr):
        self.oldstr = oldstr
        self.newstr = newstr

    def __str__(self) -> str:
        return f'{{oldstr: {self.oldstr}, newstr: {self.newstr}}}'

    def __repr__(self) -> str:
        return self.__str__()


class PairListBuilder:
    def __init__(self):
        self.pairs = []

    def add(self, oldstr: str, newstr: str) -> None:
        self.pairs.append(Pair(oldstr, newstr))

    def list(self) -> Pair:
        return self.pairs


def replace_all(pairs: List[Pair], infile, dryrun=False):
    '''
    Sed-like Replace function.
    This version supports applying multiple replacements per line, which can
    reduce times for reading/writing files.
    '''
    linelist = []
    with open(infile) as f:
        for item in f:
            newitem = item
            for pair in pairs:
                newitem = re.sub(pair.oldstr, pair.newstr, newitem)
            linelist.append(newitem)
    if dryrun == False:
        with open(infile, "w") as f:
            f.truncate()
            for line in linelist:
                f.writelines(line)
    elif dryrun == True:
        for line in linelist:
            print(line, end='')
    else:
        exit("Unknown option specified to 'dryrun' argument, Usage: dryrun=<True|False>.")


def replace(oldstr, newstr, infile, dryrun=False):
    '''
    Sed-like Replace function..
    Usage: pysed.replace(<Old string>, <Replacement String>, <Text File>)
    Example: pysed.replace('xyz', 'XYZ', '/path/to/file.txt')
    Example 'DRYRUN': pysed.replace('xyz', 'XYZ', '/path/to/file.txt', dryrun=True) #This will dump the output to STDOUT instead of changing the input file.
    '''
    linelist = []
    with open(infile) as f:
        for item in f:
            newitem = re.sub(oldstr, newstr, item)
            linelist.append(newitem)
    if dryrun == False:
        with open(infile, "w") as f:
            f.truncate()
            for line in linelist:
                f.writelines(line)
    elif dryrun == True:
        for line in linelist:
            print(line, end='')
    else:
        exit("Unknown option specified to 'dryrun' argument, Usage: dryrun=<True|False>.")


def rmlinematch(oldstr, infile, dryrun=False):
    '''
    Sed-like line deletion function based on given string..
    Usage: pysed.rmlinematch(<Unwanted string>, <Text File>)
    Example: pysed.rmlinematch('xyz', '/path/to/file.txt')
    Example 'DRYRUN': pysed.rmlinematch('xyz', '/path/to/file.txt', dryrun=True) #This will dump the output to STDOUT instead of changing the input file.
    '''
    linelist = []
    with open(infile) as f:
        for item in f:
            rmitem = re.match(r'.*{}'.format(oldstr), item)
            if type(rmitem) == type(None):
                linelist.append(item)
    if dryrun == False:
        with open(infile, "w") as f:
            f.truncate()
            for line in linelist:
                f.writelines(line)
    elif dryrun == True:
        for line in linelist:
            print(line, end='')
    else:
        exit("Unknown option specified to 'dryrun' argument, Usage: dryrun=<True|False>.")


def rmlinenumber(linenumber, infile, dryrun=False):
    '''
    Sed-like line deletion function based on given line number..
    Usage: pysed.rmlinenumber(<Unwanted Line Number>, <Text File>)
    Example: pysed.rmlinenumber(10, '/path/to/file.txt')
    Example 'DRYRUN': pysed.rmlinenumber(10, '/path/to/file.txt', dryrun=True) #This will dump the output to STDOUT instead of changing the input file.
    '''
    linelist = []
    linecounter = 0
    if type(linenumber) != type(linecounter):
        exit("'linenumber' argument must be an integer.")
    with open(infile) as f:
        for item in f:
            linecounter = linecounter + 1
            if linecounter != linenumber:
                linelist.append(item)
    if dryrun == False:
        with open(infile, "w") as f:
            f.truncate()
            for line in linelist:
                f.writelines(line)
    elif dryrun == True:
        for line in linelist:
            print(line, end='')
    else:
        exit("Unknown option specified to 'dryrun' argument, Usage: dryrun=<True|False>.")


if __name__ == "__main__":
    import os
    from tempfile import mkstemp
    fd, filename = mkstemp()
    
    with os.fdopen(fd, 'w') as f:
        f.write('a = b\n')
    
    b = PairListBuilder()
    b.add('a', 'c')
    b.add(r'\s*=\s*', '=')
    # expects 'c=b'
    replace_all(b.list(), filename, dryrun=True)
