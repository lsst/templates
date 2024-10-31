#!/usr/bin/env python3

#                         P a p e r  C h e c k . p y
#
#  This script runs a few basic checks on a paper ready to be submitted for
#  inclusion in the ADASS Proceedings. It can also be run by the ADASS
#  editors as a first quick check on a submitted paper. It does not attempt
#  to run LaTeX on the paper, so it does not catch any LaTeX errors, nor
#  is it able to check that the paper conforms to the quite stringent
#  length requirements for ADASS papers. However, it does attempt to catch
#  a number of the common problems that have been seen in the past with
#  ADASS papers. In particular it checks that the paper uses a BibTeX .bib
#  file for references, and that the references cited in the paper match
#  those defined in the .bib file. It checks that any figures used in the paper
#  have been supplied, and that these are .eps files as required.
#
#  This script should run under either Python 2 or Python 3, and has been
#  developed on OS X. It should work equally well under Linux. It has not been
#  tried under Windows. It is designed to be run from the command line, and
#  makes no effort to provide a fancy user interface.
#
#  To run this program, you need to have this PaperCheck.py script in a
#  directory together with the source files for the two additional Python
#  modules it uses, AdassChecks.py and TexScanner.py. It probably helps to
#  have that directory in the execution path. The script should be set as
#  executable using chmod +x.
#
#  The default directory should have all the files needed for the ADASS
#  paper. These should include the main .tex file, the .bib file that
#  defines any necessary BibTeX references, and any .eps graphics files used
#  by the .tex file. The files should be named following the ADASS conventions,
#  for example if the paper is for the oral presentation O3-4, the .tex file
#  should be called O3-4.tex. The script attempts to resolve cases where files
#  have been misnamed.
#
#  PaperCheck.py Paper Author
#
#  where
#
#  Paper is the designation for the paper, for example O3-4
#  Author is the surname of the first author.
#
#  The script looks for the main .tex file for the paper. If it finds it, it
#  runs a number of checks on the files for the paper, and eventually prints
#  out a summary of what it found. If the summary shows that problems were
#  found, more details will have been output as the script ran, and it should
#  be possible to find them by scrolling back in the terminal window.
#
#  If you have problems with this script, in particular if it crashes or
#  finds problems with a paper where non exist, please contact the author.
#
#  In a little more detail, the script performs the following tests:
#
#  o It makes sure it can find the main .tex file. If it cannot find a file
#    with the expected name but finds just one .tex file it will use that.
#  o It runs through the .tex file with the parser used for these checks.
#    There are times when this parser will report an unmatched '{' or '[' in
#    the .tex file. Sometimes this is due to something like an unescaped '%'
#    character, or some other similar problem.
#  o It checks to see if the .tex file uses any unsupported LaTeX packages.
#    These can have side effects that interfere with the typesetting of the
#    complete ADASS volume.
#  o It checks for unprintable characters. These tend to be used to typeset
#    names that use accents, but not all LaTeX implementations can handle them.
#    There are standard LaTeX sequences that can be used instead, and the
#    script will suggest using these.
#  o It makes sure references use a BibTeX .bib file and not \bibitem entries.
#    ADASS now requires a .bib file for references, and editors cannot be
#    expected to do the conversion from \bibitem entries.
#  o It checks the references for consistency. Are all the references cited in
#    the .tex file supplied in the .bib file? Are all the references supplied
#    in the .bib file used by the .tex file? Unused references may not seem
#    important, but a master .bib file for the whole volume is produced from
#    the individual .bib files, and unused references complicate the process.
#  o It checks for use of the old-style \cite for references. This can cause
#    problems and later commands such as \citep and \citet should be used
#    instead.
#  o It checks that all the figures used in the .tex file have their figures
#    supplied, and it checks that these are supplied as .eps files, as
#    required by ASP, who publish the Proceedings.
#  o It checks that the running heads specified in \markboth have been set
#    and not simply left as the defaults supplied by the template - a remarkably
#    common problem.
#  o It attempts to parse the author list given in the \author directive. Part
#    of the editing process involves generation of an author index, and as
#    far as possible this is done by automatically parsing the lists given
#    in \author. This is a complicated process, given the different forms of
#    names in the ADASS community, and this step is the one most likely to
#    generate warnings incorrectly. If the list of authors produced is in
#    fact correct, please add a comment line to the .tex file saying so. In
#    particular, the algorithm knows that some people have two unhyphenated
#    surnames, but cannot always be sure when that is the case.
#  o Finally, if it finds no problems, it checks to see if a copyright file
#    has been supplied. This is not necessary if a paper copy has been sent
#    to the authors, but it seems worth checking
#.
#  Author(s): Keith Shortridge (keith@knaveandvarlet.com.au)
#
#  History:
#     23rd Sep 2016. Original version, based on scripts used during editing
#                    the 2015 ADASS proceedings. KS.
#     26th Sep 2016. Now logs line number where an old-style bibliography
#                    reference was found. Enabled Trieste-style poster paper
#                    numbering. KS.
#     24th Jul 2017. Message about problems with the author list downgraded
#                    to one about 'possible issues'. The scan questions a
#                    number of cases (eg Spanish double surnames) that are
#                    in fact OK but need checking. Fixed spacing problem in
#                    'missing bib file' message. KS.
#     25th Jul 2017. CheckBibFileUsage() now handles the case where a .bib
#                    file is called, say, I1.3.bib and is specified in the
#                    .tex file using /bibliography{I1.3} without the .bib
#                    extension. Previously it was assumed the '.3' was a file
#                    extension in this case and the .bib file was not found. KS.
#     26th Jul 2017. The check on first author name in the main routine now
#                    allows for names with "\`" constructs. Introduced an
#                    initial check that the parser used by TexScanner doesn't
#                    find any problems with the .tex file. KS.
#     13th Aug 2017. Now includes checks for .tex files encoded in Unicode and
#                    Mac OS Roman as well as the original ASCII with Latin-1
#                    extensions. KS.
#     15th Aug 2017. Converted to run under Python3, using 2to3 and some minor
#                    reformatting of lines to keep to 80 characters. Added
#                    the importing of items from __future__ to allow this to
#                    run under either Python2 or Python3. KS.
#     11th Nov 2017. Added note about replacing FindTexFile() with the now
#                    available AdassChecks.LocateTexFile(). And a similar note
#                    about CheckPaperName(). KS.
#
#     31st Oct 2020. Fixed .add -> .append for ADASS2020
#     4 April 2022   Fixed pickup of vim temporary file buffers as tex files
#
#  Python 2 and Python 3.
#
#     This code should run under either python 2 or python 3, so long as
#     the python 2 version supports the "from __future__ import" used here.
#     It has been tested under 2.7 and 3.6.
#

from __future__ import (print_function,division,absolute_import)

import os
import sys
import string
import time

import AdassChecks
import TexScanner

# ------------------------------------------------------------------------------

#                         F i n d  T e x  F i l e
#
#  This routine looks for the main .tex file for the paper in the default
#  directory. If it finds one that can be used, it returns its name. If not,
#  it returns a nul string. A summary of any problems found is appened to
#  the list passed as Problems.
#
#  Note: AdassChecks.LocateTexFile() should really be used instead, now
#  that it is available.

def FindTexFile (Paper,Problems) :
   TexFileName = Paper + ".tex"
   print("The main .tex file for the paper should be called",TexFileName)

   #  There should be a main .tex file in the directory called <paper>.tex

   if (os.path.exists(TexFileName)) :
      print("Found main .tex file",TexFileName,"OK")
   else :
      print("** Could not find",TexFileName,"**")
      Problems.append("Could not find " + TexFileName + " file to use")

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


# ------------------------------------------------------------------------------

#                   F i n d  C o p y r i g h t  F o r m
#
#  This routine looks for the main .tex file for the paper in the default
#  directory. If it finds one that can be used, it returns its name. If not,
#  it returns a nul string. A summary of any problems found is appened to
#  the list passed as Warnings - copyright forms may have been submitted as
#  paper copies, so a missing one is not necessarily a problem.

def FindCopyrightForm (Paper,Author,Warnings) :

   Found = False

   CopyrightForm = "copyrightForm_" + Paper + "_" + Author + ".pdf"

   if (os.path.exists(CopyrightForm)) :
      print("Found copyright form",CopyrightForm,"OK")
      Found = True
   else :

      DirList = os.listdir(".")
      CopyrightFiles = []
      for File in DirList :
         if (not File.startswith('.')) :
            if (File.endswith(".pdf")) :
               if (File.lower().find("copyright") >= 0) :
                  CopyrightFiles.append(File)
      if (len(CopyrightFiles) == 1) :
         OnlyFileName = CopyrightFiles[0]
         print("There seems to be just one copyright file in the directory,")
         print("so we will assume",OnlyFileName,"is the one to use.")
         print("It should be renamed as",CopyrightForm)
         Warnings.append("Should rename " + OnlyFileName + " as " \
                                                           + CopyrightForm)
         CopyrightForm = OnlyFileName
         Found = True
      else :
         if (len(CopyrightFiles) == 0) :
            print("* Could not find any copyright forms in the directory *")
            print("Unless a paper copy has been submitted, there should be ")
            print("a copyright form called",CopyrightForm)
            Warnings.append("Could not find any copyright forms" +
                                                         " in the directory")
         else :
            print("The directory has the following possible copyright forms:")
            for CopyrightFile in CopyrightFiles :
               print("   ",CopyrightFile)
            print("Unable to know which is the correct one for the paper")
            Warnings.append("Cannot identify the correct copyright form to use")
         CopyrightForm = ""

   if (Found) :
      print("Note that copyright forms should not be signed electronically")

   return Found

# ------------------------------------------------------------------------------

#                   C h e c k  B i b  F i l e  U s a g e
#
#  This routine looks at the main .tex file for the paper and checks to see
#  if it is using a proper \bibliography directive rather than \bibitem
#  entries. If a .bib file is being used, it determines its name and checks
#  that it exists. If a.bib file is being used, it returns its name - and
#  returns a null string if not. Any problems found are appended to the list
#  of problems passed. Note that this is only checking that the paper is
#  using a proper .bib file for its references as opposed to the old-style
#  \bibitem-based bibliographies. VerifyRefs() is used to check that the
#  references cited actually match the entries in the bibliography, and that's
#  a different routine alltogether.

def CheckBibFileUsage (TexFileName,Problems) :

   BibFileName = ""
   HasSlashBibliography = False
   HasBibItemSection = False
   HasCitations = False
   BibFileExists = False
   ProblemLogged = False
   BibItemLine = 0

   LineNumber = 0
   TexFile = open(TexFileName,mode='r')
   for TexFileLine in TexFile :
      LineNumber = LineNumber + 1
      if (not TexFileLine.startswith("%")) :
         Index = TexFileLine.find("\\bibliography{")
         if (Index >= 0) :

            #  This is a \bibliography directive. Use it to get the name of
            #  the .bib file it refers to.

            HasSlashBibliography = True
            Left = TexFileLine[Index:].find("{")
            Right = TexFileLine[Index:].find("}")
            if (Left > 0 and Right > Left) :
               BibFileName = TexFileLine[Index + Left + 1:Index + Right]
               BibFileExt = os.path.splitext(BibFileName)[1]
               if (BibFileExt != ".bib") :
                  if (not os.path.exists(BibFileName)) :
                     BibFileName = BibFileName + ".bib"
                  else :
                     Problem = "\\bibliography directive specifies " + \
                        BibFileName + " not a .bib file"
                     print("**",Problem,"**")
                     Problems.append(Problem)
                     ProblemLogged = True

               #  See if the .bib file exists.

               print("BibTeX file specified using",TexFileLine[Index:Right + 1])
               if (os.path.exists(BibFileName)) :
                  BibFileExists = True
                  print("Found corresponding bibliography file",BibFileName)

         #  Look for an old-style \bibitem bibliography - these take a lot
         #  of time to fix up.

         BeginBibIndex = TexFileLine.find("\\begin{thebibliography")
         EndBibIndex = TexFileLine.find("\\end{thebibliography")
         BibitemIndex = TexFileLine.find("\\bibitem")
         if (BeginBibIndex >= 0 or EndBibIndex >= 0 or BibitemIndex >= 0) :

            #  These are all directives connected with an old-style bibliography
            #  section based on the use of \bibitem

            HasBibItemSection = True
            if (BibItemLine == 0) : BibItemLine = LineNumber

         if (TexFileLine.find("\\cite") >= 0) :

            #  This line contains some sort of citation directive. We expect
            #  almost all files to have some of these. If we don't find any,
            #  then the paper doesn't need a bibliography section at all.

            HasCitations = True

   TexFile.close()

   #  Having looked through the .tex file, where are we? There are a number of
   #  possible problems here, but really only one case that is exactly right..

   if (HasCitations and HasSlashBibliography and BibFileExists \
                          and not HasBibItemSection and not ProblemLogged) :

      #  This is the one that's exactly what we hope for. Citations use a
      #  .bib file and that .bib file exists.

      print("Citations use a .bib file and the .bib file exists OK")

   else :

      #  Having an old-style bibliography section is always going to be a
      #  problem.

      if (HasBibItemSection) :
         print("** Tex file has \\bibitem, or has a 'thebibliography'",\
                                            "section, at line",BibItemLine,"**")
         Problem = "Tex file must use a BibTeX file, not an old-style " + \
                                                       "bibliography section"
         print("**",Problem,"**")
         Problems.append(Problem)
         ProblemLogged = True

      #  Not having any references is unusual, but is actually OK

      if (not HasCitations) :

         #  That is, unless it has a bibliography

         if (HasSlashBibliography) :
            Problem = \
              "Tex file has a \\bibliography directive, but cites no references"
            print("**",Problem,"**")
            Problems.append(Problem)
         else:
            print("The Tex file does not appear to cite any references at all")
            ProblemLogged = True

      else :

         #  The file has references, but still has a problem. Was it with the
         #  Bib file section?

         if (not HasSlashBibliography) :

            Problem = "Tex file does not have a \\bibliography command"
            print("**",Problem,"**")
            Problems.append(Problem)
            ProblemLogged = True

         else :

            if (not BibFileExists) :
               Problem = "Bib file " + BibFileName + " specified by " + \
                                               "\\bibliography does not exist"
               print("**",Problem,"**")
               Problems.append(Problem)
               ProblemLogged = True

      #  At this point, we didn't have the perfect state we wanted, so just
      #  make sure we've logged an error - this is a catch-all section because
      #  checking all the possible combinations of errors can be tricky and I
      #  don't want to have missed one.

      if (not ProblemLogged) :
         Problem = "There is a problem with the way citations are referenced"
         print("**",Problem,"**")
         Problems.append(Problem)
         ProblemLogged = True

   return BibFileName

# ------------------------------------------------------------------------------

#                        C h e c k  P a p e r  N a m e
#
#  Checks that the paper name specified follows the ADASS conventions. This
#  adds a description of any problem to the Problems list it is passed, and
#  returns True if the name is valid, False otherwise.
#
#  This code looks quite messy, but so are the naming conventions for ADASS
#  papers. Also, if in places some of the string handling doesn't look very
#  Pythonesque, that's partly personal style, but its simple-minded scanning
#  through the strings allows me to generate the error reports I felt I needed.
#
#  Note: This could be completely replaced now by AdassChecks.CheckPaperName(),
#  which is essentially the same routine, except for the printing of the
#  problem descriptions.

def CheckPaperName(Paper,Problems) :

   #  There is a suggestion Trieste may number posters the same way Oral
   #  presentations are numbered, as P4-10, for example, rather than as
   #  P045 for example. If so, TriestePosters needs to be set true.

   # VictoriaPosters:
   # (B)BoF, (C)Contributed Talks, (F)Focus Demos, (I)Invited Talks, (P)Posters, (T)Tutorials
   # are two digits with a leading zero if necessary.

   TriestePosters = False
   CapeTownPosters = False
   VictoriaPosters = True
   XAllowed = True
   #  Some initial checks on the leading digit, which should be O for Oral,
   #  I for Invited (also oral), B for BoF, F for Focus Demo, 'D' for
   #  Demo booth or T for Tutorial.

   ValidSoFar = True
   if (len(Paper) <= 0) :
      Problem = "Paper name supplied is blank"
      print("**",Problem,"**")
      Problems.append(Problem)
      ValidSoFar = False

   if (ValidSoFar) :
      Letter = Paper[0]
      if (not Letter in ("BCFIPT" if VictoriaPosters else ("IOBFPDTHC" if not CapeTownPosters else "IOBFXDTH"))) :
         Problem = "'" + Letter + "' is not a valid prefix for a paper"
         print("**",Problem,"**")
         Problems.append(Problem)
         ValidSoFar = False

   if (ValidSoFar) :
      if (len(Paper) == 1) :
         Problem = "Paper does not have a number"
         print("**",Problem,"**")
         Problems.append(Problem)
         ValidSoFar = False

   if (ValidSoFar) :

      #  Valid leading letter, now decode the number, and there are different
      #  conventions for the different paper types.

      Number = Paper[1:]
      NumChars = len(Number)

      if (VictoriaPosters):
         if (NumChars != 2):
            Problem = \
               "Poster numbers must be two digits, with leading zeros if needed"
            print("**", Problem, "**")
            Problems.append(Problem)
            ValidSoFar = False
         else:
            N = 0
            for Char in Number:
               Value = ord(Char) - ord('0')
               if (Value < 0 or Value > 9):
                  Problem = "Non-numeric character (" + Char + \
                            ") in paper number"
                  print("**", Problem, "**")
                  Problems.append(Problem)
                  ValidSoFar = False
                  break
               N = N * 10 + Value
            if (ValidSoFar and N == 0):
               Problem = "Poster number cannot be zero"
               print("**", Problem, "**")
               Problems.append(Problem)
               ValidSoFar = False
      else:
         if (Letter == 'B' or Letter == 'F' or Letter == 'D' or Letter == 'T') :
           if not CapeTownPosters:
               #  BoFs, Focus Demos, Demo booths, and Tutorials just have a number,
               #  with no leading zeros.

               Leading = True
               for Char in Number :
                   if (Leading) :
                       if (Char == '0') :
                           Problem = "Paper number should not have leading zeros"
                           print("**",Problem,"**")
                           Problems.append(Problem)
                           ValidSoFar = False
                   Leading = False
                   Value = ord(Char) - ord('0')
                   if (Value < 0 or Value > 9) :
                       Problem = "Non-numeric character (" + Char + ") in paper number"
                   print("**",Problem,"**")
                   Problems.append(Problem)
                   ValidSoFar = False
                   break

         if (Letter == ('X' if CapeTownPosters else 'P') and not TriestePosters) :

            #  This section checks for a valid poster number using the style in
            #  use up to Trieste. This requires a poster number to be a 3 digit
            #  number, with leading zeros if necessary.
            if (NumChars != 3) :
               Problem = \
                "Poster numbers must be three digits, with leading zeros if needed"
               print("**",Problem,"**")
               Problems.append(Problem)
               ValidSoFar = False
            else :
               N = 0
               for Char in Number :
                  Value = ord(Char) - ord('0')
                  if (Value < 0 or Value > 9) :
                     Problem = "Non-numeric character (" + Char + \
                                                          ") in paper number"
                     print("**",Problem,"**")
                     Problems.append(Problem)
                     ValidSoFar = False
                     break
                  N = N * 10 + Value
               if (ValidSoFar and N == 0) :
                  Problem = "Poster number cannot be zero"
                  print("**",Problem,"**")
                  Problems.append(Problem)
                  ValidSoFar = False

         if (Letter == 'I' or Letter == 'O' or \
            (Letter == ('X' if CapeTownPosters else 'P') or (CapeTownPosters and Letter in "BFDT") and TriestePosters)) :

            #  Oral presentation numbers (and posters using the Trieste convention)
            #  have the form S-N where S is the session and N the number. Go
            #  through the digits, changing from session to number when a '-' is
            #  found.

            S = 0
            N = 0
            Session = True
            Leading = True
            if CapeTownPosters and len(Number) != 3:
                Problem = "PID number should be 3 digit and should have leading zeros if needed"
            for Char in Number :
               if (Leading) :
                  if (Char == '0' and not CapeTownPosters) :
                     if (Session) :
                        Problem = "Session number should not have leading zeros"
                     else :
                        Problem = "Paper number should not have leading zeros"
                     print("**",Problem,"**")
                     Problems.append(Problem)
                     ValidSoFar = False
                     break
                  Leading = False
               if (Char == '.' or Char == '_') :
                  Problem = \
                    "Use '-' instead of '_' or '.' to separate session and number"
                  print("**",Problem,"**")
                  Problems.append(Problem)
                  ValidSoFar = False
                  break
               if (Char == "-") :
                  if (Session) :
                     Session = False
                     Leading = True
                  else :
                     Problem = "Multiple '-' characters in paper number" + \
                                                       ") in paper number"
                     print("**",Problem,"**")
                     Problems.append(Problem)
                  continue
               Value = ord(Char) - ord('0')
               if (Value < 0 or Value > 9) :
                  Problem = "Non-numeric character (" + Char + \
                                                       ") in paper number"
                  print("**",Problem,"**")
                  Problems.append(Problem)
                  ValidSoFar = False
                  break
               if (Session) :
                  S = S * 10 + Value
               else :
                  N = N * 10 + Value
            if (ValidSoFar) :
               if (S == 0 or N == 0) and not CapeTownPosters:
                  Problem = "Session or paper number cannot be zero"
                  print("**",Problem,"**")
                  Problems.append(Problem)
                  ValidSoFar = False

   if (not ValidSoFar) :
      if (not (Paper[0] == 'X' and XAllowed)) :
         Problem = "Paper name '" + Paper + "' is invalid"
         Problems.append(Problem)

   return ValidSoFar


# ------------------------------------------------------------------------------

#                       C h e c k  U n p r i n t a b l e
#
#  This routine looks at the main .tex file for the paper and checks to see
#  if any of the lines in it contain unprintable characters. A number of
#  ADASS papers are submitted with character encodings for accented characters
#  that use an extended ASCII character set rather than the standard LaTeX
#  sequences for these accented characters. Some LaTeX installations seem to
#  handle these better than others, but it's probably best if they aren't used
#  at all. This returns True if any unprintable characters were found, False
#  otherwise.

def CheckUnprintable (TexFileName,Encoding) :

   ReturnOK = False
   LineNumber = 0
   TexFile = open(TexFileName,mode='r')
   for TexFileLine in TexFile :
      LineNumber = LineNumber + 1
      if (not TexFileLine.startswith("%")) :
         Problem = AdassChecks.CheckCharacters(TexFileLine,LineNumber, \
                                                             None,Encoding)
         if (Problem) : ReturnOK = True
   TexFile.close()

   return ReturnOK


# ------------------------------------------------------------------------------

#                       G e t  F i l e  E n c o d i n g s
#
#   This routine looks at the main .tex file and returns a set of possible
#   encodings that it may be using (ASCII, MacRoman, Latin1, UTF-8). It
#   reports any possible ambiguities.

def GetFileEncodings (TexFileName,Problems) :

   Report = []
   Encodings = []
   Certainty = AdassChecks.GetFileEncoding(TexFileName,Encodings,Report)
   if (len(Encodings) == 1) :
      print("")
      if (Encodings[0] == "ASCII") :
         print("File is encoded in standard ASCII")
      else :
         print("File contains characters that may not be supported" + \
                                              " by all LaTeX installations.")
         if (Certainty == 100) :
            print("File is encoded using",Encodings[0])
         else :
            print("File appears to be encoded using",Encodings[0])
            for Line in Report :
               print(Line)
            print("")
            Problems.append("File contains non-standard characters," + \
                     " and there is some uncertainty about the encoding used")
   else :
      print("File contains extended characters that may not be supported")
      print("by all LaTeX installations, and the encoding is ambiguous")
      Message = "File could be encoded using any of: "
      for Encoding in Encodings :
         Message = Message + ' ' + Encoding
      print(Message)
      for Line in Report :
         print(Line)
      Problems.append("File contains non-standard characters," + \
                                       " and the encoding is ambiguous")

   return Encodings

# ------------------------------------------------------------------------------

#       C h e c k  S u b j e c t I n d e x E n t r i e s
#
#  Checks all ssindex{} entries are valid, i.e. exist in the subject keyword lists
#  Does return True if no problems found at all
#
#  Harro Verkouter: 11 Feb 2020  Added this check
from   operator    import truth, methodcaller, __add__
from   functools   import reduce, partial
from   collections import deque
import re, AdassConfig, AdassIndex

compose       = lambda *fns   : (lambda x: reduce(lambda acc, f: f(acc), reversed(fns), x))
drain         = partial(deque, maxlen=0)
Filter        = lambda pred: partial(filter, pred)
Map           = lambda fn: partial(map, fn)
Reduce        = lambda r: partial(reduce, r)
# Read all "\ssindex{...}" and "%\ssindex{...}" entries from a tex file
get_ssindices = compose(set, Map(methodcaller('group', 1)), Filter(truth),
                        Map(re.compile(r'^%?\\ssindex{([^}]*)}.*$').match), open)

def CheckSubjectIndexEntries(Paper, Problems, TexFileName = "") :
    # Read the total list of keywords from subjectKeywords.txt and newKeywords.txt
    # Is there a better way to use AdassConfig.* methods to point at relative file paths?
    Entries = compose(set, Reduce(__add__), Map(AdassIndex.ReadIndexList))(
                      ['../Author_Template/subjectKeywords.txt', '../Author_Template/newKeywords.txt'] )
    if not Entries:
        Problems.append( "No subject keywords found **at all**?! (../Author_Template/{subject|new}Keywords.txt missing?" )
        return False

    # ssindex entries that are not in Entries pose a problem!
    missing = get_ssindices(Paper + ".tex" if TexFileName == "" else TexFileName) - Entries
    if missing:
        Problems.append( "Found ssindex{} entries that are not in subjectKeywords.txt/newKeywords.txt:\n" +
                         "".join( map("\t{0}\n".format, missing) ) )
    return not missing

# ------------------------------------------------------------------------------

#                   M a i n  P a p e r  C h e c k  P r o g r a m
#
#  This is the main code for the program. For details of how to invoke it,
#  see the header comments.

#  First, just check we have the necessary arguments.

NumberArgs = len(sys.argv)
if (NumberArgs < 3) :
   print(sys.argv)
   print("Usage: PaperCheck <paper> <author>")
   print("<paper> should be the identifier for the paper, eg O5-4")
   print("<author> should be the surname of the first author")
   print("e.g. PaperCheck 05-4 Jones")
else :

   Paper = sys.argv[1]
   PaperAuthor = sys.argv[2]
   if NumberArgs>3:
       PaperAuthor = " ".join(sys.argv[2:])

   print("")
   print("          A D A S S   P a p e r   C h e c k")
   print("")
   print("This program will run a number of checks on the files in the")
   print("default directory, assuming these include the main .tex file for")
   print("the paper",Paper,"and any associated .eps graphics files and any")
   print("supplied .bib BibTeX file.")
   print("")
   print("The surname of the main author is assumed to be",PaperAuthor)
   print("")
   print("This program cannot check all the possible problems with the paper.")
   print("It does not check that the paper typesets properly using LaTeX,")
   print("and it does not check the content of the paper or the references.")
   print("However, it does perform a number of basic checks that will also")
   print("be performed by the ADASS editors, and it will save a lot of time")
   print("if you submit .tex files that pass these checks.")
   print("")

   Problems = []
   Step = 0

   #  Should check that we have a conforming paper name.

   CheckPaperName(Paper,Problems)

   #  Locate the main .tex file for the paper.

   Step = Step + 1
   print("")
   print("Step",Step," - Locate main .tex file for paper -------------------")

   TexFileName = FindTexFile(Paper,Problems)
   if (TexFileName == "") :

      print("Unable to continue without a main .tex file for the paper")

   else :

      print("Found file ",TexFileName)


      #  Preliminary step. See if the TexParser used by AdassChecks has any
      #  problems with the .tex file. If so, it may well generate incorrect
      #  results.

      TexFile = open(TexFileName,mode='r')
      TheScanner = TexScanner.TexScanner()
      TheScanner.SetFile(TexFile)
      Finished = False
      while (not Finished) :
         Finished =  TheScanner.GetNextTexCommand(None,None,None)
      if (not TheScanner.ParsedOK()) :
         print("")
         print("The parser used for these tests reported a problem:")
         Report = TheScanner.GetReport()
         for Line in Report :
            print(Line)
         Problems.append("There was a problem parsing the .tex file")
      TexFile.close()

      #  Check to see if the main .tex file makes use of any non-standard
      #  LaTeX packages..

      Step = Step + 1
      print("")
      print("Step",Step," - Check for use of unsupported LaTeX packages -------")

      AllOK = AdassChecks.CheckPackages(Paper,TexFileName)
      if (AllOK) :
         print("No unsupported packages used")
      else :
         Problems.append("Problems were found with the use of LaTeX packages")

      #  Check to see if the main .tex file contains any characters some
      #  LaTeX installations might have problems with..

      Step = Step + 1
      print("")
      print("Step",Step," - Check for unprintable characters in the .tex file -")

      Encodings = GetFileEncodings(TexFileName,Problems)
      Warned = False
      for Encoding in Encodings :
         print(" ")
         print("Assuming file is encoded using",Encoding)
         Problem = CheckUnprintable(TexFileName,Encoding)
         if (Problem) :
            if (not Warned) : Problems.append( \
                     "Unprintable characters in the .tex file should be fixed")
            Warned = True
         else :
            print("No unprintable characters found - all OK")

      #  Check that a proper BibTeX file is being used, not an old-style
      #  bibliography using \bibitem entries..

      Step = Step + 1
      print("")
      print("Step",Step," - Check that bibliography entries use a BibTex file -")

      BibFileName = CheckBibFileUsage(TexFileName,Problems)

      #  Check on the references supplied and cited in .tex file.

      Step = Step + 1
      print("")
      print("Step",Step," - Check references against citations ---------------")

      AllOK = AdassChecks.VerifyRefs(Paper,False,TexFileName,BibFileName)
      if (AllOK) :
         print("No problems found")
      else :
         Problems.append("Problems were found with the use of references")


      #  Check explicitly on the use of \cite for any references.

      Step = Step + 1
      print("")
      print("Step",Step," - Check use of use of \cite for references ---------")

      AllOK = AdassChecks.CheckCite(Paper,TexFileName)
      if (AllOK) :
         print("No problems found")
      else :
         Problems.append(
            "References make use of \cite instead of \citep or \citet")

      #  Check on the graphics files supplied and used by the main .tex file.

      Step = Step + 1
      print("")
      print("Step",Step," - Check use of graphics files ----------------------")

      AllOK = AdassChecks.VerifyEps(Paper,TexFileName)
      if (AllOK) :
         print("No problems found")
      else :
         Problems.append("Problems were found with the use of graphics files")

      #  Check the running heads for the paper specified by the main .tex file.

      Step = Step + 1
      print("")
      print("Step",Step," - Check the running heads for the paper ------------")

      AllOK = AdassChecks.CheckRunningHeads(Paper,TexFileName)
      if (AllOK) :
         print("No problems found")
      else :
         Problems.append("Problems were found with the use of \\markboth")


      #  Check on the parsing of the author list from the .tex file.

      Step = Step + 1
      print("")
      print("Step",Step," - Check parsing of author list ---------------------")

      Notes = []
      AuthorList = AdassChecks.GetAuthors(Paper,Notes,TexFileName)
      print("Author list parsed as follows (as surname, then initials):")
      for Author in AuthorList :
         print("   ",Author)
      if (len(Notes) == 0) :
         print("No problems found")
      else :
         print("The following possible problems were found:")
         for Note in Notes :
            print("*",Note,"*")
         Problems.append("There may be issues with the author list")
      if (len(AuthorList) > 0) :
         FirstAuthor = AuthorList[0]
         if (not FirstAuthor.startswith(PaperAuthor)) :
            FirstAuthor = \
              FirstAuthor.replace("\\","").replace("'","").replace("`","")
            TrimPaperAuthor = \
              PaperAuthor.replace("\\","").replace("'","").replace("`","")
            if (not FirstAuthor.startswith(TrimPaperAuthor)) :
               Problem = "First author does not appear to be " + PaperAuthor
               print("**",Problem,"**")
               Problems.append(Problem)

      #  Check if the ssindex keywords in the file are valid

      Step = Step + 1
      print("")
      print("Step",Step," - Check ssindex entries ---------------------")

      if not CheckSubjectIndexEntries(Paper, Problems, TexFileName) :
          print("** There may be undefined ssindex keywords in the tex file")
      else:
          print("No problems found")

      #  Check if there is a copyright form
      Step = Step + 1
      print("")
      print("Step", Step, " - Check copyright form --------------------")
      if (not FindCopyrightForm(Paper, Author, Problems)):
         Problem = "CopyRight form not found"
      else:
         print("CopyRight form found")

      #  Summarise any problems.

      print("")
      print("---------------- Summary ----------------------------------------")
      if (len(Problems) <= 0) :
         print("")
         print("The paper has passed the very basic checks" \
                                                      " run by this program.")
         print("")
         print("You need to make sure you have followed the ADASS manuscript")
         print("instructions, and you need to make sure that your paper")
         print("typesets without any LaTeX errors or warnings, and is within")
         print("the page limits.")

      else :
         print("Some problems were found with this paper, as follows:")
         for Problem in Problems :
            print(Problem)
         print("For more details, see the earlier diagnostics from the", \
                                                          "various stages")

      #  See if there is a copyright form

      sys.exit( - len(Problems) )
