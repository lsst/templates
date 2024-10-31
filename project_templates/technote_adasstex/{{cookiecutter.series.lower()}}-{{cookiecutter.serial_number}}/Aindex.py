#!/usr/bin/env python3

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

import os
import sys
import string

import AdassChecks

def FindTexFile (Paper,Problems) :
   TexFileName = Paper + ".tex"
   print("The main .tex file for the paper should be called",TexFileName)

   #  There should be a main .tex file in the directory called <paper>.tex

   if (os.path.exists(TexFileName)) :
      print("Found main .tex file",TexFileName,"OK")
   else :
      print("** Could not find",TexFileName,"**")

      #  See if there is just one .tex file in the directory, and if so use
      #  it.

      DirList = os.listdir(".")
      TexFiles = []
      for FileName in DirList :
         if os.path.splitext(FileName)[1] == ".tex" and os.path.splitext(FileName)[0].find('.') != 0:
            TexFiles.append(FileName)
      if (len(TexFiles) == 1) :
         OnlyFileName = TexFiles[0]
         print("There is just one .tex file in the directory,")
         print("so we will assume",OnlyFileName,"is the one to use.")
         print("It should be renamed as",TexFileName)
         Problems.append("Should rename " + OnlyFileName + " as " + TexFileName)
         TexFileName = OnlyFileName
      else :
         TexFileName = ""
         if (len(TexFiles) == 0) :
            print("** There are no .tex files in the directory **")
            Problems.append("Could not find any .tex files in the directory")
         else :
            print("The directory has the following .tex files:")
            for TexFile in TexFiles :
               print("   ",TexFile)
            print("Unable to know which is the main .tex file for the paper")
            Problems.append("Cannot identify the correct .tex file to use")
   return TexFileName



NumberArgs = len(sys.argv)
if (NumberArgs < 2) :
   print("Usage: Aindex <paper>")
   print("eg: Aindex O1-4")
else :
   Paper = sys.argv[1]
   if not os.path.exists(Paper):
        print("Paper {} not found... looking for main .tex".format(Paper))
        Paper = FindTexFile(Paper, [])
   Notes = []
   if os.path.splitext(Paper)[1] == '.tex':
       Paper = Paper[:-4]
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
