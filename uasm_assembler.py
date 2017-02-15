#!/usr/bin/env python2
# import sys

from assembler import asm

import argparse
import re
import os

parser = argparse.ArgumentParser(description='UASM assembler')
parser.add_argument('infiles', nargs='+',
                    help='assemble source files, in order')

parser.add_argument('-I', '--include-dir', nargs='+', type=str,
                    help='add a dir look for sources')

parser.add_argument('-o', '--outfile', type=str,
                    help='output file')

parser.add_argument('-le', '--little-endian',
                    action='store_true', help='use little endian byte order')

parser.add_argument('-be', '--big-endian',
                    action='store_true', help='use big endian byte order')

parser.add_argument('-v', '--verbose', dest='verbose',
                    action='store_true', help='show some details')

def bail(msg): raise Exception(msg)

class App(object):
    def __init__(self, as_main=True):
        self.verbose = False
        if as_main:
            self.main()
            return
        
    # -------------------------------------------------------
    # App is being used as an object in another program or
    # test suite. this will require explicit setup of these members:

    def set_includes(self, dirs):
        if type(dirs) != list:
            raise Exception("set_includes must take a list of directories")
        self.includes = dirs
    def set_infiles(self, infiles):
        self.infiles = infiles
    def set_endian_little(self):
        self.little_endian = True
        self.big_endian = False
    def set_endian_big(self):
        self.little_endian = False
        self.big_endian = True        
    def set_outfile(self, outfile):
        self.outfile = outfile


    # App is being used as if it were main().
    def main(self):
        args = parser.parse_args()
        
        if not any(vars(args).values()):
            parser.print_help()
            bail("No args supplied")

        # -------------------------------------------------------
        self.verbose = args.verbose
            
            
        # -------------------------------------------------------
        self.infiles = args.infiles
        if args.verbose:
            print
            print "using infiles:"
            for infile in self.infiles:
                print "  ", infile
        
        # -------------------------------------------------------
        self.include_dir = args.include_dir
        if args.verbose and self.include_dir:
            print
            print "using include directory:"
            for path in self.include_dir:
                print "  ", path
        
        # -------------------------------------------------------
        self.outfile = args.outfile
        if args.outfile and args.verbose:
            print
            print "outputting to file:"
            print "  ", self.outfile

        # -------------------------------------------------------
        self.little_endian = args.little_endian
        self.big_endian = args.big_endian
        if args.big_endian and args.little_endian:
            bail("Both little-endian and big-endian selected. Can only select one.")
        if not args.big_endian and not args.little_endian:
            # default to little_endian
            self.little_endian = True
        if args.verbose:
            print
            print "using endian:"
            if self.little_endian:
                print "  ", "little_endian"
            if self.big_endian:
                print "  ", "big_endian"


        
        # -------------------------------------------------------
        self.run()

        
    def discover_all_sources(self):
        '''Explore all the infiles and the .include directives in those
        infiles to find all the referenced source files.  This is
        unfortunately more complicated than expected because .includes
        can be commented out, which are important to ignore

        '''

        # -------------------------------------------------------
        def get_file_includes(txt):
            # search for includes.
            # regex for C_COMMENT found here.
            # http://blog.ostermiller.org/find-comment
            c_comment = r"/\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*+/"
            cpp_comment = r"//.*?(?=\n)"

            # remove comments from txt. (hack)
            for comment in [c_comment, cpp_comment]:
                # for each comment type
                pat = re.compile(comment)                
                for match in pat.finditer(txt):
                    # if a comment was found
                    span = match.span()
                    if span != None:
                        # replace the comment with spaces.
                        txt = blank_span(txt, span)
                        
            # search for includes
            # 
            pat = re.compile(r'.include[ ]+\"([^\n^\"]+)\"')
            found = pat.findall(txt)
            if found == None:
                return []
            return found
            
        # -------------------------------------------------------
        def find_file(fname):
            # look on cwd and the include paths. 
            if os.path.exists(fname):
                return fname
            
            for inc in self.includes: 
                p = os.path.join(inc, fname)
                if os.path.exists(p):
                    return p
            raise Exception("include file not found: " + fname)
                
        accum = set()
        for fname in self.infiles:            
            fn = find_file(fname)
            if fn == None: continue
            if fn in accum: continue
            accum.add(fn)
            
            try:
                txt = open(fn).read()
                found = get_file_includes(txt)
                self.infiles.extend(found)
            except (IOError, OSError) as e:
                print "Can't find include file: ", fn
        return accum
    
    def assemble(self):
        fileset = self.discover_all_sources()
        # cat these files.
        txt = ""
        for f in fileset:
            txt += open(f).read()

        bytes = asm.Assembler(txt).process_asm_inst()
        return bytes
    
    def output(self):
        print self.outfile

    def run(self):
        bs = self.assemble()
        outfile = open(self.outfile, 'wb')
        
        # pad if necessary
        while len(bs) % 4 != 0:
            bs.append((len(bs)-1, 0))

        while len(bs) > 0:
            chunk = [x[1] for x in bs[:4]]
            if self.little_endian:
                chunk.reverse()

            if self.verbose:
                temp = "%02x %02x %02x %02x" % tuple(chunk)
                addr = "%08x" % bs[0][0]
                print addr, "\t", temp

            outfile.write(bytearray(chunk))
            bs = bs[4:]
        
def blank_span(txt, span):
    space = " " * (span[1] - span[0])
    return txt[:span[0]] + space + txt[span[1]:]
        
if __name__ == "__main__":
    App(as_main=True)
