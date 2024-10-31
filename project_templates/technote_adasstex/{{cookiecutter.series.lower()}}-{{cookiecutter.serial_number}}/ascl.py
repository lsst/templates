#! /usr/bin/env python3
#
#   quick helper code for ASCL editing (Teuben/Allen)
#   is really part of the git module 'teuben/ascl-tools' but placed here
#   for convenience
#
#   Typical usage:
#         ./ascl.py sample.tex
#   will return a somewhat noisy list of the lines that potentially need
#   a set of %\ooindex{} entries for the ADASS proceedings to make the ASCL index.
#         ./ascl.py codename
#   returns 
#
#   @todo:  terminal markers highlight?
#           use puncuation to break words?  NO
#           won't catch "MIRIAD's" - should we search for    KEYWORD's as well
#           won't catch MIRIAD\footnote
#
#   Version:     25-jan-2014 for ADASS2013 proceedings
#                21-aug-2016 try to find alternate ascl2.txt from the pathname if a local version not present
#                            convert to python3
#                12-dec-2018 integrating into ADASSProceedings/Author_Template for the 2018 proceedings
#                 6-oct-2020 allow asclKeywords with codes that contain a space (by using a 2nd :)

from __future__ import print_function

import sys
import os

debug   = False
punct   = ['.', ',', '/', ':', ';', '{', '}', '@', '(', ')', '[', ']', '\\', '\'', '"', '!']


def printf(format, *args):
    sys.stdout.write(format % args)

def parse1(file):
    fp = open(file,'r')
    lines = fp.readlines()
    fp.close()
    print("Found %d lines in %s" % (len(lines),file))
    # look for
    #     <tr><td>ascl:1102.023</td><td>21cmFAST:
    magic = '<tr><td>ascl:'
    len1 = len(magic)
    codes = {}
    for line in lines:
        if line[0:len1] == magic:
            line1 = line[len1:80]
            id = line1[0:8]
            tmp     = line1[17:80]
            # print "    ",line1[0:50]
            ic = tmp.find(':')
            code = tmp[0:ic]
            code_words = code.split()
            codes[code] = id
            if len(code_words) > 1:
                print('# ascl:'+id,code)
            else:
                print('ascl:'+id,code)
    print('Found %d code entries' % len(codes))
    return codes

def parse2(file):
    """ read quick index for ADASS """
    fp = open(file,'r')
    lines = fp.readlines()
    fp.close()
    codes = {}
    # file has     "ascl:1234.123 Code_Name"
    # oct-2020     "ascl:1234.123 Code Name:Comments" to deal with spaces in code names
    for line in lines:
        if line[0] == '#': continue
        words = line.split(':')
        aid = words[1].split()[0]                # ascl id, e.g.  "1234.123"
        acn = ' '.join(words[1].split()[1:])     # code name, but wow, look at this construct
        codes[acn.lower()] = "\\ooindex{%s, ascl:%s}" % (acn,aid)
        #print(aid,acn)
        #
        #   OLD pre-2020 style
        #codename = words[1].lower()
        #codes[codename] = "\\ooindex{%s, %s}" % (words[1],words[0])

    return codes

def parse3(file,codes):
    """
    codename ->   codename\ooindex{codename, ascl_id}
    """
    fp = open(file,'r')
    lines = fp.readlines()
    fp.close()
    if debug: print(codes)
    for line in lines:
        print('LINE: ',line)
        line2 = ''
        has_a_code = False
        words = line.split(' ,')
        for word in words:
            print('WORD: ',word)
            if word in codes: 
                has_a_code = True
                line2 = line2 + "%s\\ooindex{%s, %s} " % (word,word,codes[word])
            else:
                line2 = line2 + word + " "
        if has_a_code:
            print("# " + line)
            print(line2)
        else:
            print(line)


def wclean(word):
    """make clean punctuation-free words
    """
    w = word.lower()
    len1 = len(punct)
    # remove iteratively, all punctuation at the start
    while True:
        done = True
        for p in punct:
            if w[0] == p:
                w = w[1:]
                done = False
                if len(w) == 0:
                    return w
                break
        if done:
            break
    len2 = len(w)
    if len2 == 0:
        return w
    # remove iteratively, all punctuation from the end
    while True:
        done = True
        for p in punct:
            if w[-1:] == p:
                w = w[:-1]
                done = False
                break
        if done:
            break
    return w


def parse4(file,codes,comment):
    """
    codename ->   codename\ooindex{codename, ascl_id}

    codename ->
    %
    """
    fp = open(file,'r')
    lines = fp.readlines()
    fp.close()
    if debug: print(codes)
    ln = 0
    for line in lines:
        ln = ln + 1
        if debug: print('LINE: '+line)
        line2 = ''
        has_a_code = False
        words = line.split()
        for dword in words:
            word = wclean(dword)
            if debug: print('WORD: ',dword,word)
            #if codes.has_key(word):                        # not python3
            if word in codes:
                has_a_code = True
                line2 = line2 +  comment + "%s \n" % (codes[word])
        if has_a_code:
            print("#[%d] %s" % (ln,line))
            print(line2)
        else:
            if debug: print(line)
    ns = 0
    for line in lines:
        if line.find('\ooindex{') > 0:
            ns = ns + 1
    if ns>0:
        print("Warning: I already found %d ASCL entries" % ns)
        for line in lines:
            if line.find('\ooindex{') > 0:
                print(line.strip())
        


#parse3('sample.tex',codes)

if __name__ == '__main__':
    comment = '%'                        # pick '%' or ''
    afile = 'asclKeywords.txt'
    if len(sys.argv) == 1:
        print("Usage: %s tex_file" % sys.argv[0])
        print("")
        print("Scans tex_file for occurences of ASCL code names, and prints out the ")
        print("corresponding %\ooindex{NAME, ascl:yymm:nnn} to be cut and pasted into tex_file")
        print("including the line number and text that triggered the match")
        print("Lookup table of codes in %s" % afile)
        sys.exit(0)

        
    filename = sys.argv[1]
    if os.path.exists(filename):
        if False:
            codes = parse1('ascl.php')
        else:
            codes = parse2(afile)
        parse4(filename,codes,comment)
    else:
        # could try grepping this as a word in 'afile'
        codename = filename.lower()
        #
        codes = parse2(afile)
        if codename in codes:
            print(codename,codes[codename])
        
