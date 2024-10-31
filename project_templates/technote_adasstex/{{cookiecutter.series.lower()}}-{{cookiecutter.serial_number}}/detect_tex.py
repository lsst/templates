#!/usr/bin/env python3

import os, sys

# Kludge to detect the TEX file to use as makedefs don't seem to be picked up
# by GNU Make under zsh / at least not in combination with the csh scripts in the
# repo

def FindTexFile (Paper,Problems) :
   TexFileName = Paper + ".tex"
   print("%The main .tex file for the paper should be called",TexFileName)

   #  There should be a main .tex file in the directory called <paper>.tex

   if (os.path.exists(TexFileName)) :
      print("%Found main .tex file",TexFileName,"OK", file=sys.stderr)
   else :
      print("%** Could not find",TexFileName,"**", file=sys.stderr)

      #  See if there is just one .tex file in the directory, and if so use
      #  it.

      DirList = os.listdir(".")
      TexFiles = []
      for FileName in DirList :
         if os.path.splitext(FileName)[1] == ".tex" and \
            os.path.splitext(FileName)[0].find('.') != 0 and \
            not FileName.find('_inc.tex') >= 0:
            TexFiles.append(FileName)
      if (len(TexFiles) == 1) :
         OnlyFileName = TexFiles[0]
         print("%There is just one .tex file in the directory,", file=sys.stderr)
         print("%so we will assume",OnlyFileName,"is the one to use.", file=sys.stderr)
         print("%It should be renamed as",TexFileName, file=sys.stderr)
         Problems.append("Should rename " + OnlyFileName + " as " + TexFileName)
         TexFileName = OnlyFileName
      else :
         TexFileName = ""
         if (len(TexFiles) == 0) :
            print("%** There are no .tex files in the directory **", file=sys.stderr)
            Problems.append("Could not find any .tex files in the directory")
         else :
            print("%The directory has the following .tex files:", file=sys.stderr)
            for TexFile in TexFiles :
               print("%   ",TexFile, file=sys.stderr)
            print("%Unable to know which is the main .tex file for the paper", file=sys.stderr)
            Problems.append("Cannot identify the correct .tex file to use")
   return TexFileName

if __name__ == "__main__":
    guess = sys.argv[1] if len(sys.argv) > 1 else "" 
    guess = FindTexFile(guess, [])
    print(guess)
