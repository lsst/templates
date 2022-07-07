#!/usr/bin/env python

#                           A i n d e x . p y
#
#  A convenience script to help with processing the submissions for the
#  Sydney ADASS conference. This reads the main .tex file and prints out
#  the list of authors in a form that can be copied and pasted into the
#  .tex file as the set of \aindex{} directives needed to generate the
#  author index.
# 
#  Invoke using:
#
#  Aindex.py <paper>
#
#  where <paper> is the Paper ID, eg O1-4.
#
#  (the program could look in the directory and find the main .tex file for
#  itself, but having to specify it on the command line serves as a check
#  that this is being run in the correct directory).
#
#  History:
#     18th Feb 2016. Original version, KS.
#     22nd Sep 2017. Converted to run under Python3, using 2to3. Added
#                    the importing of items from __future__ to allow this to
#                    run under either Python2 or Python3. KS.
#
#  Python versions:
#     This code should run under either python 2 or python 3, so long as
#     the python 2 version supports the "from __future__ import" used here.
#     It has been tested under 2.7 and 3.6.
# 

from __future__ import (print_function,division,absolute_import)


import sys
import string

import AdassChecks

NumberArgs = len(sys.argv)
if (NumberArgs < 2) :
   print("Usage: Aindex <paper>")
   print("eg: Aindex O1-4")
else :
   Paper = sys.argv[1]
   Notes = []
   
   print("")
   print("Generating author index entries for paper",Paper)
   print("")
   AuthorList = AdassChecks.GetAuthors (Paper,Notes)
   if (len(AuthorList) <= 0) :
      print("** No authors found for",Paper,"**")
   else :
      for Author in AuthorList :
         print("%\\aindex{" + Author + "}")
      print("")
      for Note in Notes :
         print("*",Note,"*")  
