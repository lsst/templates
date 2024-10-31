#!/usr/bin/env python3

#                    F i x  U n p r i n t a b l e . p y
#
#  A convenience script to help with processing the submissions for an
#  ADASS conference. This performs the single step of replacing any unprintable
#  characters in the main .tex file for a paper with the standard LaTeX
#  equivalents. These characters tend to appear when a file is prepared with
#  an editor that inserts extended (non-standard ASCII) characters into the
#  file to represent accented or other punctuation characters that would
#  normally require a more complex LaTeX sequence - for example "\'{e'}" to
#  generate an e-acute. The problem is that not all LaTeX installations can
#  handle such characters, and it is safer to replace these with the standard
#  LaTeX sequences, awkward though they are. A secondary problem is that there
#  are a number of possible encodings that can be used, and it is not always
#  clear which has in fact been used for any given .tex file.
#
#  Usage:
#     FixUnprintable filename <encoding>
#
#     where filename is the name of the .tex file in question, and encoding is
#     an optional argument that can be used to tell the script what encoding
#     should be assumed for the file.
#
#  If unprintable characters are found in the file, a new version of the file
#  will be created in which those unprintable characters that can be fixed
#  have been fixed, and the original file is renamed.
#
#  The 'encoding' argument can be any of 'ASCII', 'MacRoman', "Latin1" or
#  "UTF-8". Case is ignored. If this argument is omitted, the program will
#  attempt to determine the encoding automatically. Usually, it will get
#  this right. If it cannot determine the encoding, it will ask to be run
#  again with the encoding specified explicitly. (There are cases where the
#  program is sufficiently confident it knows the encoding, but there is
#  some uncertainty. In this case, it will go ahead, but the user may have to
#  recover the original file from its renamed version and run the program
#  again with the encoding specified explicitly.) In any cases of doubt, the
#  program outputs full details of what it found in the file.
#
#  Author(s): Keith Shortridge (keith@knaveandvarlet.com.au)
#
#  History:
#     15th Jan 2017. Original version.
#     15th Aug 2017. Added automatic determination of encoding, and the use
#                    of the 'encoding' argument for when this gets the wrong
#                    answer. KS.
#     23rd Nov 2018. Converted to run under Python3, using 2to3. Added
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

def NextVersion (FileName) :
   NextVersion = FileName + '_1'
   Number = 1
   while (os.path.exists(NextVersion)) :
      Number = Number + 1
      NextVersion = FileName + '_' + str(Number)
   return NextVersion

#  Defaults

UseAscii = False
UseMacRoman = False
UseLatin1 = False
UseUtf8 = False
CheckEncoding = True
ArgsValid = True

#  First, just check we have the necessary filename, and see if an encoding
#  was specified.

NumberArgs = len(sys.argv)
if (NumberArgs < 2) :
   print("Usage: FixUnprintable filename <encoding>")
   print("eg: FixUnprintable P10-3.tex")
   ArgsValid = False
if (NumberArgs > 2) :
   CheckEncoding = False
   Encoding = sys.argv[2]
   if (Encoding.lower() == "ascii") : UseAscii = True
   elif (Encoding.lower() == "macroman") : UseMacRoman = True
   elif (Encoding.lower() == "latin1") : UseLatin1 = True
   elif (Encoding.lower() == "utf-8") : UseUtf8 = True
   else :
      print("Encoding must be one of: ASCII, MacRoman, Latin1, UTF-8")
      ArgsValid = False
   if (ArgsValid) : print("Will assume file is encoded using",Encoding)

if (ArgsValid) :
   TexFileName = sys.argv[1]
   
   if (not os.path.exists(TexFileName)) :
      print("Cannot find file '" + TexFileName + "'")
   else :
   
      #  Unless we've been asked to use a specific encoding, try to determine
      #  the encoding automatically. GetFileEncoding() will do this.
      
      EncodingOK = True
      if (CheckEncoding) :
         Report = []
         Encodings = []
         Certainty = AdassChecks.GetFileEncoding(TexFileName,Encodings,Report)
         if (len(Encodings) == 1) :
            print("")
            if (Encodings[0] == "ASCII") :
               print("File is encoded in standard ASCII")
            else :
               if (Certainty == 100) :
                  print("File is encoded using",Encodings[0])
               else :
                  print("File appears to be encoded using",Encodings[0])
                  for Line in Report :
                     print(Line)
                  print("")
                  print("If necessary, restore the saved version an re-run")
                  print("specifying a different encoding explicitly, eg:")
                  if (Encodings[0] == "Latin1") :
                     print("FixUnprintable",TexFileName,"MacRoman")
                  else :
                     print("FixUnprintable",TexFileName,"Latin1")
            Encoding = Encodings[0].lower()

         else :
            EncodingOK = False
            Message = "File could be encoded using any of: "
            for Encoding in Encodings :
               Message = Message + ' ' + Encoding
            print(Message)
            for Line in Report :
               print(Line)
            print("")
            print("Re-run, specifying a different encoding explicitly.")
            print("For example, use one of:")
            for Encoding in Encodings :
               print("FixUnprintable",TexFileName,Encoding)

      if (EncodingOK) :
   
         #  An initial pass to see if we need to do anything. CheckCharacter()
         #  doesn't output any messages - it returns any it generates in Details,
         #  which we ignore - and returns True or False depending on whether
         #  it found any problem characters.
      
         LineNumber = 0
         FileOK = True
         InputFile = open(TexFileName,"r")
         for Line in InputFile :
            LineNumber = LineNumber + 1
            Details = []
            if (AdassChecks.CheckCharacters(Line,LineNumber,Details,Encoding)) :
               FileOK = False
               break

         #  If nothing needed doing, just close the file.

         if (FileOK) :
            print("Nothing needs doing,",TexFileName,"left unchanged")
            InputFile.close()
         else :

            #  A second pass, if necessary, to actually do the fixing.
            #  FixCharacters() returns a fixed line, and prints out details of
            #  what it did. If no changes were made, it returns None.

            InputFile.seek(0)
            WorkFileName = NextVersion("Work.tex")
            OutputFile = open(WorkFileName,"w")
            LineNumber = 0
            for Line in InputFile :
               LineNumber = LineNumber + 1
               FixedLine = AdassChecks.FixCharacters(Line,LineNumber,Encoding)
               if (FixedLine != None) : Line = FixedLine
               OutputFile.write(Line)
            OutputFile.close()
            InputFile.close()
            
            #  We now need to rename the files, so the original file becomes a
            #  saved version, and the work file we just created replaces the
            #  original file.

            SavedFileName = NextVersion(TexFileName)
            os.rename(TexFileName,SavedFileName)
            os.rename(WorkFileName,TexFileName)
            print("Original file saved as",SavedFileName)


