#
#                       A d a s s  C h e c k s . p y
#
#  This is the code for a module that contains a number of checking
#  routines that are potentially used by a number of scripts involved in
#  editing the ADASS proceedings. Over time the interfaces to these routines
#  have evolved to make the routines more flexible, generally through the
#  addition of optional parameters. A number of these routines take one or more
#  of a fairly standard set of optional parameters.
#
#  Common optional parameters:
#     TexFileName can be used to supply the name of the .tex file, instead
#                 of assuming it will be the paper name with a .tex extension.
#     BatchMode   can be set true to indicate the routine is being called from
#                 a batch program and should not print out diagnostics as it
#                 might if it were run more interactively. Usually, if BatchMode
#                 is true, diagnostics can be appended to a list such as
#                 Problems, also passed as an optional argument.
#     Problems    can be used to pass a list of strings, to which the routine
#                 can add descriptions of any problems it encounters.
#     Warnings    can be used to pass a list of strings, to which the routine
#                 can add warnings about any questionable issues it encounters.
#
#
#  VerifyRefs (Paper,AllowBibitems = True,TexFileName = "",BibFileName = "",
#                                       Problems = None, Warnings = None)
#     Checks that the references used in the main .tex file and those
#     in the .bib file are consistent. It accepts references defined in the
#     .tex file using \bibitem for purposes of consistency checking, but
#     warns about these. This can be controlled using the optional parameter
#     AllowBibItems. BibFileName can optionally be used to explicitly specify
#     the name of the .bib file.
#
#  VerifyEps (Paper,TexFileName = "",Problems = None,Warnings = None)
#     Checks that any graphics files used in the main .tex file are
#     supplied, and that any graphics files supplied are used by the
#     main .tex file.
#
#  CheckPackages (Paper,TexFileName = "",Problems = None)
#     Checks any packages used by the main .tex file, and notes the use of
#     any standard packages - these can be included, but it's unnecessary -
#     and warns about any non-standard packages.
#
#  GetBibFileRefs (BibFileName,BatchMode = False)
#     Returns a list of strings giving the names of the various references
#     defined in the named .bib file.
#
#  TrimBibFile (Paper,Keep = True)
#     Looks in the .bib file used by the main .tex file and comments out
#     any unused references. It assumes the .bib file has the same name as
#     the common .bib file returned by GetBibFileName(). If the optional
#     Keep argument is False, the unused references are deleted rather than
#     just commented out.
#
#  GetAuthors (Paper,Notes,TexFileName = "")
#     Looks in the main .tex file and generates a list of the authors
#     suitable for generating \aindex entries.
#
#  FixCharacters (Line,LineNumber,Encoding = "Latin1")
#     Replaces any of the common non-printable accented characters in a line
#     with the LaTeX equivalent sequence and returns the corrected line.
#
#  CheckCharacters (Line,LineNumber,Problems = None,Encoding = "Latin1")
#     Is a version of FixCharacters that only checks for non-printable
#     characters rather than actually fixing them.
#
#  CheckRunningHeads (Paper,TexFileName = "",Problems = None)
#     Checks for a number of common errors in the way the running heads
#     for the paper are specified using \markboth.
#
#  GetArchiveList (Path,Paper)
#     Looks in the specified path for any archive file that might be being
#     used for the specified paper and returns a list of such files.
#
#  GetArchiveTime (Filename,FileList = None)
#     Returns the latest modification date (as a time in seconds since the
#     epoch) of any file contained in the named archive file. If passed an
#     optional list, it will add the names of all the files it finds to that
#     list.
#
#  GetBibFileName() returns a string giving the name of the common .bib
#     file used for all the papers, eg "adassXXVreferences.bib".
#
#  AuthorChars (Author) returns a simplified version of an author's surname,
#     with any accenting LaTeX directives removed.
#
#  GetConferenceNumber() returns a string with the Romal numerals for the
#     current ADASS conference, eg "XXV".
#
#  GetEditors() returns a string giving the names of the editors of the
#     current Proceedings, in a form suitable for a .bib file entry.
#
#  GetVolume() returns the number of the current ADASS volume - the ASP
#     volume number, as needed by a .bib file entry.
#
#  CheckCite (Paper,TexFileName = "",Problems = None)
#     Checks to see if the specified paper is using any \cite commands
#     instead of the preferred comamnds \citep, \citet etc.
#
#  GetFileEncoding (TexFileName,Result,Report)
#     Returns a list of possible character encodings used by the .tex file.
#
#  Author(s): Keith Shortridge (keith@knaveandvarlet.com.au)
#
#  History:
#     16th Feb 2016. Now checks for all natbib \cite options. KS.
#     19th Feb 2016. Added GetAuthors() (and AuthorScanCallback()). KS.
#     22nd Feb 2016. Fixed recently introduced problem generating message
#                    about a "\cite" reference. TrimBibFile() is now a
#                    little cleverer about locating the end of an entry. KS.
#     29th Feb 2016. Added FixCharacters(). KS.
#      1st Mar 2016. Had managed to lose the test for lower case initial
#                    letters (generally an indication something has gone
#                    wrong) in GetInitial(). Fixed. KS.
#      3rd Mar 2016. AuthorScanCallback() now allows for forced line-breaks -
#                    "\\" or "\\*". KS.
#      4th Mar 2016. Added GetArchiveTime(). Also fixed a problem where
#                    TrimBibFile() was not stripping blanks from the ends of
#                    references before comparing them. Really, RefScanCallback()
#                    should return references ready stripped, which would 
#                    allow both RefCheck() and TrimBibFile() to get rid of
#                    a number of calls to strip(). KS.
#      7th Mar 2016. Added GetArchiveList(). KS.
#      8th Mar 2016. GetArchiveTime() no longer fails if an archive contains
#                    links to files that don't exist. KS.
#     29th Mar 2016. Fixed diacritical tilde problem in author names. KS.
#      1st Apr 2016. Added GetBibFileName() and CheckPackages(). KS.
#      4th Apr 2016. Added AuthorChars(), GetConferenceNumber(), Editors() and
#                    Volume(). KS.
#      6th Apr 2016. Corrected a couple of .index() calls that should have
#                    been .find(), so they don't raise exceptions if the string
#                    isn't found. KS.
#      7th Apr 2016. Improved parsing in GetBibFileRefs() so it can handle
#                    cases where the reference type and name are not all
#                    specified on the first line of the reference. 
#                    TrimBibFile() still has problems with such files, but at
#                    least it now prints out a warning when this happens. KS.
#     28th Apr 2016. Fixed problem in author list parsing caused by extraneous
#                    trailing blanks, which was generating an erroneous 
#                    possible missing comma warning. KS.
#      7th May 2016. Added check for upper case characters in body of surname
#                    when collecting author names. KS. 
#      8th May 2016. The author name scan code now tries to spot both the
#                    'Spanish surname' case and the 'on behalf of the team'
#                    case, and makes a note of a possible problem. KS.
#     23rd May 2016. RefCheck no longer complains that a .eps file is not
#                    used if the .tex file does use it but has allowed the 
#                    extension to default to .eps. KS.
#     24th May 2016. Now allows 'le' as part of a surname. KS.
#      7th Jun 2016. Now checks for surnames that don't seem to have any
#                    associated initials. KS.
#     14th Sep 2016. VerifyEps() now returns an overall status value and takes
#                    an optional main .tex file name. The same change has been
#                    made for CheckPackages(). KS.
#     18th Sep 2016. VerifyRefs() now takes a number of additional optional
#                    arguments, and returns an overall status value. The
#                    GetAuthors() routine now also takes an optional main
#                    TeX file name. KS.
#     20th Sep 2016. Added CheckCharacters() and CheckRunningHeads() and
#                    CheckCite(). KS.
#     23rd Sep 2016. Check on author names now no longer complains about
#                    the capital in Scottish names like MacDonald. KS.
#     23rd Nov 2016. Modified the conference details so they apply to the
#                    2016 Trieste conference. KS.
#     27th Nov 2016. GetArchiveTime() now allows for spaces and quotes in the
#                    names of archive files or their directories. Also now 
#                    ignores __MACOSX files when counting files to see if there
#                    is just a single sub-directory at top level. KS.
#      9th Dec 2016. Added support for 'batch mode' operation - eg when
#                    used by PaperCheckBatch.py - to VerifyRefs() and to
#                    VerifyEps(), CheckCharacters(), CheckPackages(),
#                    CheckCite(), GetTexFileRefs() and CheckRunningHeads(). KS.
#     10th Dec 2016. CheckPackages() now allows "./asp2014". KS.
#     19th Dec 2016. GetArchiveTime() can now optionally return a list of the
#                    files in the archive and ignores the dates on any files
#                    that are directories. (It really ought to do a proper
#                    recursive search through the file structure.) KS.
#     18th Feb 2017. Changed the mapping of the unprintable character 0xd5.
#                    See comments to FixCharacters{} for more detail. KS.
#     25th Mar 2017. VerifyRefs() and TrimBibFile() now use the new routine
#                    FindBibFile() to fall back on <paper>.bib as the name
#                    for the .bib file if the standard .bib file cannot be
#                    found. KS.
#     14th Jul 2017. VerifyEps() now checks for file names that match but only
#                    if case is ignored. KS.
#     16th Jul 2017. RunningHeadsCallback() now checks the running title against
#                    that from the current template and the older template. KS.
#     17th Jul 2017. VerifyEps() now checks subdirectories as well as the
#                    default directory for graphics files. If graphics files
#                    are in subdirectories, it regards this as a problem. The
#                    highlighting used for problem logging in this routine is
#                    now a little more consistent. KS.
#     24th Jul 2017. GetBibFileRefs() now checks for - and ignores - unexpected
#                    entry types. Updated the routine descriptions at the start
#                    of this file to include the various optional parameters
#                    that have been added over time. VerifyEps() now checks for
#                    files specified in the .tex file with leading "./", and
#                    now checks for image files used more than once in the
#                    .tex file. Improved the way VerifyRefs() handles the case
#                    where a .bib file is supplied, but the .tex file has a
#                    \bibliography entry that specifies the wrong name. KS.
#     25th Jul 2017. Improved VerifyRefs() diagnostics where a .tex file has
#                    no citations at all. Discovered BibTeX doesn't ignore
#                    unexpected entry types, so now GetBibFileRefs() only warns
#                    about them. The original problem ignoring them was supposed
#                    to solve is now solved by resetting the parser on lines
#                    that start with '@'. KS.
#     26th Jul 2017. Corrected spacing in "will default to .eps" message. Now
#                    tries to pick the case where an author name has been given
#                    with the surname first instead of last. FindBibFile() now
#                    looks for any .bib file in the directory if it cannot find
#                    the one it expects, and reports on what it found. The
#                    code that checks author names now allows 'da' as part of
#                    a surname - eg "da Silva". KS.
#      9th Aug 2017. TrimBibFile() was putting out a misleading message when
#                    deleting (not commenting) unused entries. Fixed. KS.
#     10th Aug 2017. The code handling author names now allows 'di' as part of
#                    a surname - eg "di Marco". KS.
#     13th Aug 2017. Added GetFileEncoding(). Substantial changes to the code
#                    for FixCharacters() and CheckCharacters() to support the
#                    use of UTF-8 Unicode characters and the old Mac OS Roman
#                    encodings as well as the original ASCII with LATIN-1
#                    extended characters. (I now understand the problem with
#                    the 0xd5 character - see 18th Feb 2017. The files using
#                    this as an apostrophe were using Mac Roman encoding.) KS.
#     15th Aug 2017. Converted to run under Python3, using 2to3 and some minor
#                    reformatting of lines to keep to 80 characters. Added
#                    the importing of items from __future__ to allow this to
#                    run under either Python2 or Python3. Had to modify the code
#                    in VerifyEps() that used os.path.walk (deprecated under
#                    Python 3) to use os.walk instead. Tested under 2.7 and
#                    under 3.6. KS.
#     18th Aug 2017. Modified the Unicode equivalence dictionary so all Greek
#                    letters - which are math mode in LaTeX - are enclosed in
#                    $..$ symbols. Realised GetArchiveList() also used
#                    os.path.walk() and needed re-working for Python 3. KS.
#     31st Oct 2017. Code was not waiting properly for os.popen() commands to
#                    complete. This only showed up when run under Python 3, and
#                    has been fixed by adding the required close() calls. KS.
#      2nd Nov 2017. Added ExtractArchive(), CollapseDir() and LocateTexFile(),
#                    all of which are utilities useful for looking at unknown
#                    archive files. KS.
#      3rd Nov 2017. Added GetTitle(), AuthorSurname() and GetLatestFileDate().
#                    Also added the RunCommand() utility routine. KS.
#      5th Nov 2017. Added CheckPaperName(). KS.
#     12th Nov 2017. VerifyRefs() was printing one blank line even in batch
#                    mode. So was VerifyEps(). Fixed. FixCharacters() and
#                    CheckCharacters() could fail if passed unprintable chars
#                    in ASCII encoding. Also fixed. KS.
#     24th Nov 2017. Trapped output coming from FindBibFile() when called from
#                    VerifyRefs(), even in batch mode. KS.
#     25th Nov 2017. Added CheckTemplateLines(). KS.
#     28th Nov 2017. Added SubjectIndexEntries(). KS.
#      1st Dec 2017. LocateTexFile() will now accept any .tex file that
#                    contains the PaperID somewhere in its name. CollapseDir()
#                    will now also expand intermediate archive files, and now
#                    can return the names or removed directories and archives
#                    if passed lists for this purpose. KS.
#     17th Jun 2019  Prepare file for ADASS 2019 JdP.

from __future__ import (print_function,division,absolute_import)

import sys
import string
import os
import tempfile
import shutil
import subprocess

import TexScanner

# ------------------------------------------------------------------------------

#                 A d a s s  C o n f e r e n c e  D e t a i l s
#
#  These should be the only items in the ADASS proceedings Python modules that
#  needs to be changed from year to year. (Note that these are not used by the
#  PaperCheck.py script distributed with the manuscript instructions. They are
#  used by the various utility scripts used in the editing process for the
#  proceedings.)

__AdassConference__ = "XXXII"

__AdassEditors__    = "Pizzo,~R. and Deul,~E. and Mol,~J. and de Plaa,~J. and Verkouter,~H. and Williams,~R."

__AdassVolume__     = "TBD"

# ------------------------------------------------------------------------------

#                   G e t  C o n f e r e n c e  N u m b e r
#
#   Returns the ADASS conference number in Roman numerals.

def GetConferenceNumber() :

   return __AdassConference__
   
# ------------------------------------------------------------------------------

#                         E d i t o r s
#
#   Returns a string giving the typeset names of the editors of the ADASS
#   proceedings in a form suitable for a BibTeX entry.

def Editors() :

   return __AdassEditors__
   
# ------------------------------------------------------------------------------

#                         V o l u m e
#
#   Returns a string giving the volume number for the ADASS proceedings in 
#   a form suitable for a BibTeX entry.

def Volume() :

   return __AdassVolume__
   
# ------------------------------------------------------------------------------

#                      G e t  B i b  F i l e  N a m e
#
#  GetBibFileName() returns the name of the common ADASS .bib file being used.
#  Conventionally, this varies depending on the conference number, being
#  "adass<conf>references.bib", where <conf> is the conference number in
#  Roman numerals.

def GetBibFileName() :

   return ("adass" + __AdassConference__ + "references.bib")

# ------------------------------------------------------------------------------

#                         E x t r a c t  R e f s
#
#  ExtractRefs() is a utility routine for VerifyRefs() which looks at a list
#  of the words found in a LaTeX \cite -type directive and returns the
#  list of what seem to be the actual references - it assumes these are
#  in the first non-optional argument (in {braces}) and are separated by
#  commas.

def ExtractRefs (Words) :
   Refs = ""
   for Word in Words[1:] :
      if (Word != "") :
         if (Word[0] == '{') :
            Refs = Word.strip("{}")
            Refs.replace(" ","")
            RefList = Refs.split(",")
            break
   return Refs

# ------------------------------------------------------------------------------

#                        G e t  B i b  F i l e  R e f s
#
#   Looks in the current directory for the  specified .bib file, and
#   returns a list of all the references it defines.

def GetBibFileRefs (BibFileName,BatchMode = False):

   #  Later versions of Python have better support for enums, but this
   #  works on old versions too.
   
   def enum(**enums):
      return type('Enum', (), enums)
   
   #  These parse states are fairly simplisitic, and really assume that
   #  the bib file is valid and laid out in a relativly straightforward way.
   #  Most files will just have a line at the start of each reference
   #  @type{name,
   #  and in this case we go through all the states in the one line.
   #  If the file starts with
   #  @type{
   #     name,
   #  then the first line will take us from needing an @ to needing a 
   #  comma, and the second line will provide the reference and move us
   #  back to needing an @. 
   #  If the file starts with
   #  @type
   #     {name,
   #  or even
   #  @type
   #  {
   #      name,
   #  Then successive lines take us to needing a brace, then needing a 
   #  comma, then getting the reference and back to needing an @.
   #  Anything else it won't handle properly. And it won't pick up cases
   #  where there's someting before the '@' on a line, and will get confused
   #  if the reference is incomlete, without a closing brace, say.
   
   States = enum(NEED_AT = 0, NEED_BRACE = 1, NEED_COMMA = 2)
   
   #  The set of expected entry types
   
   ExpectedTypes = ["article","book","booklet","conference","inbook",
                  "incollection","inproceedings","manual","mastersthesis",
                  "misc","phdthesis","proceedings","techreport","unpublished"]
   
   BibFileRefs = []
   State = States.NEED_AT
   Found = False
   if (os.path.exists(BibFileName)) :
      BibFile = open(BibFileName,mode='r')
      
      for BibFileLine in BibFile :
      
         #  There are some odd .bib fies around that this code doesn't parse
         #  properly, and we can end up still looking for something in a
         #  reference definition when we hit a line that starts with '@'.
         #  It's more likely that we've mis-parsed the file than that
         #  there is such a line in the middle of a legitimate reference,
         #  so we restart at this point.
         
         if (BibFileLine.strip().startswith('@')) : State = States.NEED_AT
      
         #  In most cases, we'll be looking for the '@' that starts a
         #  reference definition, and will find all we need on the one line.
         #  If not, we end up in one of the intermediate states.
         
         if (State == States.NEED_AT) :
            BibFileLine = BibFileLine.strip().rstrip("\r\n")
            if (BibFileLine.startswith("@")) :
               State = States.NEED_BRACE
               Brace = BibFileLine.find("{")
               if (Brace > 0) :
                  EntryType = BibFileLine[1:Brace]
                  State = States.NEED_COMMA
                  Comma = BibFileLine.find(",")
                  if (Comma > 0) :
                     Ref = BibFileLine[Brace + 1:Comma].strip()
                     State = States.NEED_AT
                     BibFileRefs.append(Ref)
               else :
                  EntryType = BibFileLine[1:]
      
               #  Check the entry type and warn about any non-standard types.
               
               if (not (EntryType.lower().strip() in ExpectedTypes)) :
                  Problem = "Unexpected .bib file entry '" + EntryType + \
                                                 "' - will default to 'MISC'"
                  if (not BatchMode) : print("*",Problem,"*")
                  State = States.NEED_AT
      
         else :
         
            #  If we need a brace, look for it and if we have one, we then
            #  want the reference and its terminating comma - we assume these
            #  will be on the same line. Then we will probably find the comma
            #  in the next block. If not, on the next line.

            if (State == States.NEED_BRACE) :
               Brace = BibFileLine.find('{')
               if (Brace >= 0) :
                  BibFileLine = BibFileLine[Brace + 1:]
                  State = States.NEED_COMMA

            #  If we're looking for the reference name itself followed by
            #  a comma, see if we have that. This does assume the comma is
            #  on the same line as the name (how many odd formats are we
            #  trying to handle?)

            if (State == States.NEED_COMMA) :
               BibFileLine = BibFileLine.lstrip()
               Comma = BibFileLine.find(",")
               if (Comma > 0) :
                  Ref = BibFileLine[:Comma].strip()
                  State = States.NEED_AT
                  BibFileRefs.append(Ref)
         
      BibFile.close()
   else:
      if (not BatchMode) : print("**No bib file called",BibFileName,"found**")
      
   return BibFileRefs

# ------------------------------------------------------------------------------

#                        G e t  T e x  F i l e  R e f s
#
#   Looks in the current directory for the specified .tex file, and
#   adds the identifiers of all the references it cites to the list
#   passed as TexFileRefs, and adds any bibitems it finds to the list
#   passed as BibItemRefs. The final optional Problems argument allows this to
#   be used in batch mode, where direct output from this routine is suppressed
#   and instead a set of report lines are added to the list of problems passed.

def GetTexFileRefs (TexFileName,TexFileRefs,BibItemRefs,Problems = None):

   TexFile = open(TexFileName,mode='r')
   TheScanner = TexScanner.TexScanner()
   TheScanner.SetFile(TexFile)

   #  GetNextTexCommand() will call RefsScanCallback for each command it
   #  finds in the file, and RefsScanCallback will check the command
   #  and add any cited references to TexFileRefs and any items defined
   #  using \bibitem to BibItemRefs.

   Finished = False
   Refs = (TexFileRefs,BibItemRefs)
   while (not Finished) :
      Finished = TheScanner.GetNextTexCommand(RefsScanCallback,Refs,Problems)

   TexFile.close()

# ------------------------------------------------------------------------------

#                        F i n d  B i b  F i l e
#
#   Looks in the current directory for the .bib file associated with the
#   specified paper. This should either be the standard .bib file used by
#   all the papers when in their final form, as returned by GetBibFileName(),
#   or it should have the same name as the main paper but with a .bib
#   extension, eg O1-3.bib. This routine looks first for the standard .bib
#   file, and if cannot find that, looks for the one with the same name as
#   the paper. It returns the first of these that it finds. If neither
#   exists, it looks for any .bib file in the directory. If it finds none, it
#   returns blank.
#
#   Note that it is possible that the .tex file is using a .bib file with
#   neither of these names, eg with a \bibliography{example} directive. This
#   routine could check for that, but at the moment it doesn't.
#
#   The optional Details parameter can be a list of strings to which this
#   routine will append a description of the file it is using.

def FindBibFile (Paper,Details = None) :

   BatchMode = False
   if (Details != None) : BatchMode = True
   
   Found = False
   BibFileName = GetBibFileName()
   if (BibFileName != "") : Found = os.path.exists(BibFileName)
   if (Found) :
      Report = "Using standard .bib file " + BibFileName
      if (BatchMode) :
         Details.append(Report)
      else :
         print(Report)
   else :
      BibFileName = Paper + ".bib"
      Found = os.path.exists(BibFileName)
      if (Found) :
         Report = "Using .bib file " + BibFileName + " (based on paper name)"
         if (BatchMode) :
            Details.append(Report)
         else :
            print(Report)
      else :
         BibFileCount = 0
         FileList = os.listdir(".")
         for File in FileList :
            if (File.endswith(".bib")) :
               if (BibFileCount == 0) : BibFileName = File
               BibFileCount = BibFileCount + 1
               Found = True
         if (Found) :
            Report = "Using .bib file " + BibFileName
            if (BibFileCount > 1) :
               Report = Report + " (first of " + str(BibFileCount) + \
                                                   " .bib files found)"
            if (BatchMode) :
               Details.append(Report)
            else :
               print(Report)
   if (not Found) : BibFileName = ""

   return BibFileName

# ------------------------------------------------------------------------------

#                            V e r i f y  R e f s
#
#   This routine looks in the current directory for a file called 
#   Paper.tex (where Paper will be a string such as "O1-4"), assuming
#   this is the main .tex file for the paper, and also looks for the
#   file called "adass<conf>references.bib" which it assumes contains the
#   BibTeX references for the paper. If this file cannot be found, it will
#   check for a file called Paper.bib. It checks that all the references in
#   the .bib file are used by the .tex file, and that all the references
#   used by the .tex file are defined in the .bib file (or, being tolerant,
#   defined using \bibitem directives in the .tex file, although it warns
#   about these). It lists all the references, so the user can see what
#   (if any) naming convention is being used.
#
#   The optional arguments allow this to be used with the PaperCheck
#   initial verification code, where the paper name and the bib file name
#   may not be the standard names expected, and allow control over whether
#   or not we allow the use of \bibitem entries or not. It also now returns
#   True if no problems were found, False otherwise. The final optional
#   Problems and Warnings arguments allow this to be used in batch mode, where
#   direct output from this routine is suppressed and instead a set of report
#   lines are added to the list of problems passed.

def VerifyRefs (Paper,AllowBibitems = True,TexFileName = "",BibFileName = "", \
                                            Problems = None, Warnings = None) :

   ReturnOK = True
   
   BatchMode = False
   if (Problems != None and Warnings != None) : BatchMode = True
   
   if (TexFileName == "") : TexFileName = Paper + ".tex"
   TexFileName = os.path.abspath(TexFileName)
   if (not os.path.exists(TexFileName)) :
      Problem = "Cannot find main .tex file: " + TexFileName
      if (BatchMode) : Problems.append(Problem)
      else : print(Problem)
      ReturnOK = False
   else :

      #  Assume that the .bib file to use (if any) has the same name as
      #  the common reference .bib file. Get a list of all the references it
      #  contains so we can see what soft of naming convention is used,
      #  and so we can check them against the references in the .tex file.
      #  If we have to fall back on FindBibFile(), any details it reports
      #  should be treated as warnings.

      LookForBibFile = False
      if (BibFileName == "") :
         LookForBibFile = True
      else :
         if (not os.path.exists(BibFileName)) : LookForBibFile = True
      if (LookForBibFile) : BibFileName = FindBibFile(Paper,Warnings)

      if (BibFileName == "") :
         BibFileRefs = []
      else :
         BibFileRefs = GetBibFileRefs(BibFileName,BatchMode)
         if (not BatchMode) :
            print("")
            print("References in",BibFileName," :")
            for BibRef in BibFileRefs :
               print("   ",BibRef)
            print("")

      #  The .bib file name we've ended up with may not be the one specified
      #  in the .tex file, and we check for that.

      if (not BatchMode) :
         Warn = False
         TexFile = open(TexFileName,mode='r')
         for TexFileLine in TexFile :
            if (not TexFileLine.startswith("%")) :
               if (TexFileLine.find("\\usepackage{./asp2014}") >= 0) :
                  print("** .tex file has \\usepackage{./asp2014} directive **")
                  Warn = True
               Index = TexFileLine.find("\\bibliography{")
               if (Index >= 0) :
                  Right = TexFileLine[Index:].find("}")
                  if (Right > 0) :
                     OldBib = TexFileLine[Index:Index + Right + 1]
                     BibFileBase = os.path.splitext(BibFileName)[0]
                     if (OldBib != "\\bibliography{" + BibFileBase + "}" and \
                          OldBib != "\\bibliography{" + BibFileName + "}") :
                        print("** Note: Tex file includes",OldBib,\
                                                             "directive **")
                        Warn = True
         TexFile.close()
         if (Warn) :
            print("** .tex file directives may need correcting **")
            ReturnOK = False

      #  Now get a list of the \citet and \citep commands in the .tex file
      #  We also see if there are any \bibitem definitions, although people
      #  aren't supposed to be using these.

      TexFileRefs = []
      BibItemRefs = []

      GetTexFileRefs(TexFileName,TexFileRefs,BibItemRefs,Problems)

      if (not BatchMode) :
         if (len(TexFileRefs) > 0) :
            print("References cited in",TexFileName,":")
            for TexRef in TexFileRefs :
               print("   ",TexRef.strip())
            print(" ")
      BibItemCount = len(BibItemRefs)
      if (BibItemCount > 0) :
         if (BatchMode) :
            if (not AllowBibitems) :
               Problems.append( \
                        "Tex file has the following \\bibitem directives:")
               for BibItem in BibItemRefs :
                  Problems.append(BibItem.strip())
         else :
            print("** Note: Tex file has",BibItemCount,\
                                                    "\\bibitem directives **")
            for BibItem in BibItemRefs :
               print("    ",BibItem.strip())
            if (not AllowBibitems) :
               ReturnOK = False
               print("** These need to be replaced by a .bib file", \
                                                     "with BibTex entries **")

      #  See if all the references defined in the .bib file are used
      #  in the .tex file.

      if (len(BibFileRefs) == 0) :
         if (not BatchMode) : print("No Bib file references supplied")
      else :
         AllUsed = True
         for BibRef in BibFileRefs :
            BibRef = BibRef.strip()
            BibRefLower = BibRef.lower()
            Found = False
            CaseCheck = False
            for TexRef in TexFileRefs :
               TexRef = TexRef.strip()
               if (BibRef == TexRef) :
                  Found = True
                  CaseCheck = True
                  break
               if (BibRefLower == TexRef.lower()) :
                  Found = True
                  break
            if (not Found) :
               Warning = "Bib file reference " + BibRef + \
                                                    " not used in .tex file"
               if (BatchMode) : Warnings.append(Warning)
               else : print(Warning)
               AllUsed = False
            if (Found and (not CaseCheck)) :
               Problem = "Bib file reference " + BibRef + \
                                   " used with different case in .tex file"
               if (BatchMode) : Problems.append(Problem)
               else : print(Problem)
         if (AllUsed) :
            if (not BatchMode) :
               print("All Bib file references used in .tex file")
         else :
            ReturnOK = False

      #  And the same for the \bibitem definitions - not that we approve -
      #  if there were any.

      if (BibItemCount > 0) :
         AllUsed = True
         for BibItem in BibItemRefs :
            BibItem = BibItem.strip()
            Found = False
            for TexRef in TexFileRefs :
               TexRef = TexRef.strip()
               if (BibItem == TexRef) :
                  Found = True
                  break
            if (not Found) :
               Problem = "\\bibitem reference " + BibItem + \
                                             " not used in .tex file"
               if (BatchMode) : Problems.append(Problem)
               else : print(Problem)
               AllUsed = False
         if (AllUsed) :
            if (not BatchMode) :
               print("All \\bibitem references used in .tex file")
         else :
            ReturnOK = False

      #  See if all the references cited in the .tex file are defined
      #  in the .bib file or at least in the \bibitem definitions (not 
      #  that we approve of those).

      if (len(TexFileRefs) == 0) :
         if (not BatchMode) : print("No citations found in tex file")
      else :
         AllFound = True
         for TexRef in TexFileRefs :
            TexRef = TexRef.strip()
            TexRefLower = TexRef.lower()
            Found = False
            AsBibitem = False
            CaseCheck = False
            for BibRef in BibFileRefs :
               BibRef = BibRef.strip()
               if (TexRef == BibRef) :
                  Found = True
                  CaseCheck = True
                  break
               if (TexRefLower == BibRef.lower()) :
                  Found = True
                  break
            if (not Found) :
               for BibItem in BibItemRefs :
                  BibItem = BibItem.strip()
                  if (TexRef == BibItem) :
                     Found = True
                     CaseCheck = True
                     AsBibitem = True
                     break
                  if (TexRefLower == BibItem.lower()) :
                     Found = True
                     AsBibItem = True
                     break
            if (not Found) :
               Problem = ".tex file reference " + TexRef + " undefined"
               if (BatchMode) : Problems.append(Problem)
               else : print(Problem)
               AllFound = False
            if (Found and (not CaseCheck)) :
               Problem = ".tex file reference " + TexRef + \
                                     " defined but with different case"
               if (BatchMode) : Problems.append(Problem)
               else : print(Problem)
            if (Found and AsBibitem and not AllowBibitems) :
               Problem = ".tex file reference " + TexRef + \
                                     " defined but as a \\bibitem entry"
               if (BatchMode) : Problems.append(Problem)
               else : print(Problem)
      
         if (AllFound) :
            if (not BatchMode) : print("All .tex file citations defined")
         else :
            ReturnOK = False
         
   if (not BatchMode) : print("")
   
   return ReturnOK
   
# ------------------------------------------------------------------------------

#                       R e f  S c a n  C a l l b a c k
#
#   Used as the callback routine for the TexScanner when it is used to scan
#   the .tex file for citations to references that should be in the .bib
#   file. Also scans for references defined within the .tex file using
#   \bibitem entries. Words are the components of a LaTeX directive parsed 
#   by the TexScanner. The second argument, Refs, should be a list of two
#   lists, the first being TexFileRefs (a list of cited references in the file)
#   and the second being BibItemRefs (a list of any \bibitem entries in the
#   file - which we don't approve of, but need to know about). If this is a
#   recognised citation, the cited references are added to TexFileRefs. If it
#   is a \bibitem entry, the name of the reference is added to BibItemRefs.
#   TexFileRefs and BibItemRefs are both lists of strings. The final optional
#   Problems argument allows this to be used in batch mode, where direct output
#   from this routine is suppressed and instead a set of report lines are added
#   to the list of problems passed.

def RefsScanCallback (Words,Refs,Problems = None) :
   
   TexFileRefs = Refs[0]
   BibItemRefs = Refs[1]
   
   BatchMode = (Problems != None)

   if (len(Words) > 0) :
   
      #  See if we have "\cite" or "\Cite". If so, this is should be one of the
      #  citation options provided by the natbib package. This provides a
      #  large number of options - see 
      #  http://texdoc.net/texmf-dist/doc/latex/natbib/natbib.pdf
      #  and this code checks for all of them, splitting things into the
      #  options that start with "\cite" and those that start with "\Cite".
      #  All of these commands take a non-optional argument that is one or
      #  more references that should be defined in a .bib file (or perhaps
      #  using \bibitem entries). The "\cite" command is expressly warned
      #  about in the natbib documentation, and ADASS doesn't allow it, so
      #  it's trapped here. The only legitimate natbib option not included
      #  here is "\citetext" which does not take a reference argument - it
      #  takes literal text - and this will end up generating a warning.
      
      if (Words[0][:5].lower() == "\\cite") :
         Match = False
         Refs = ExtractRefs(Words)
         if (Words[0][1] == 'c') :
         
            #  Check the upper case options \citexxx
            
            if (len(Words[0]) == 5) :
               Problem = "Note use of \cite for reference '" + Refs + \
                                                        "' in .tex file"
               if (BatchMode) : Problems.append(Problem)
               else : print("**",Problem,"**")
               Match = True
            else :
               LowerCaseOptions = ["t","p","t*","p*","alt","alt*","alp","alp*",\
                         "num","author","author*","year","yearpar","fullauthor"]
               Option = Words[0][5:]
               for Opt in LowerCaseOptions :
                  if (Option == Opt) :
                     Match = True
                     break
         else :
         
            #  Check the upper case options \Citexxx
            
            if (len(Words[0]) > 5) :
               UpperCaseOptions = ["t","p","t*","p*","alt","alt*","alp","alp*",\
                                                             "author","author*"]
               Option = Words[0][5:]
               for Opt in UpperCaseOptions :
                  if (Option == Opt) :
                     Match = True
                     break
         if (not Match) :
            Problem = "Note: use of " + ' '.join(Words) + " in .tex file"
            if (BatchMode) : Problems.append(Problem)
            else : print("**",Problem,"**")
         else :
         
            #  If we found one of the \cite commands, get the references from
            #  its arguments.
            
            if (Refs != "") :
               RefList = Refs.split(",")
               TexFileRefs.extend(RefList)
            else :
               Problem = "Note: no reference list in " + ' '.join(Words) + \
                                                            " in .tex file"
               if (BatchMode) : Problems.append(Problem)
               else : print("**",Problem,"**")

      #  Finally, pick up any \bibitem entries, while we're at it.
      
      if (Words[0] == "\\bibitem") :
         Refs = ExtractRefs(Words)
         if (Refs != "") :
            BibItemRefs.append(Refs.strip("{}"))
         else :
            Problem = "Note: no reference list in " + ' '.join(Words) + \
                                                            "in .tex file"
            if (BatchMode) : Problems.append(Problem)
            else : print("**",Problem,"**")

# ------------------------------------------------------------------------------

#                            V e r i f y  E p s
#
#   This routine looks in the current directory for a file called 
#   Paper.tex (where Paper will be a string such as "O1-4"), assuming
#   this is the main .tex file for the paper. It looks for any plotting
#   commands (\plotone, \plottwo, \plotfiddle, or \includegraphics, which
#   should cover all the commands used in ADASS papers) and collects the
#   names of the files used by these commands. It then looks at the files
#   in the current directory and checks that all of them are present, and
#   also checks that there are no additional .eps files that are unused.
#   To allow this to be used for preliminary checking, where the main .tex
#   file has been misnamed, the actual .tex file name can be supplied as
#   an optional argument. The final optional Problems and Warnings arguments
#   allow this to be used in batch mode, where direct output from this routine
#   is suppressed and instead a set of report lines are added to the lists of
#   problems and warnings passed.
#
#   This routine returns True if everything looks OK, False otherwise.


def VerifyEps (Paper,TexFileName = "",Problems = None,Warnings = None) :

   #  Originally, for early versions of Python 2, CalledFromWalk() was a
   #  function passed to os.path.walk() in order to build up a full list of the
   #  files in the current directory. Now it is called more directly from the
   #  main code for each directory found by os.walk(). Each file found is added
   #  to FileList. We strip off any leading './' as this is (we assume) not
   #  going to be included when the .tex file refers to the file.
   
   def CalledFromWalk(FileList,DirPath,Namelist) :
      if (DirPath.find("__MACOSX") < 0) :
         for Name in Namelist :
            Path = os.path.join(DirPath,Name)
            if (Path.startswith("./")) : Path = Path[2:]
            FileList.append(Path)
   
   ReturnOK = True
   
   BatchMode = False
   if (Problems != None and Warnings != None) : BatchMode = True
   
   if (TexFileName == "") : TexFileName = Paper + ".tex"
   TexFileName = os.path.abspath(TexFileName)
   if (not os.path.exists(TexFileName)) :
      Problem = "Cannot find main .tex file: " + TexFileName
      if (BatchMode) : Problems.append(Problem)
      else : print("**",Problem,"**")
      ReturnOK = False
   else :

      #  Now get a list of the files used by the graphics commands in the .tex
      #  file.

      FileListFromTex = []
      TexFile = open(TexFileName,mode='r')
      TheScanner = TexScanner.TexScanner()
      TheScanner.SetFile(TexFile)
      
      #  GetNextTexCommand() will call EpsScanCallback for each command it
      #  finds in the file, and EpsScanCallback will check the command
      #  and add any specified graphic file names used to FileListFromTex.
      
      Finished = False
      while (not Finished) :
         Finished =  TheScanner.GetNextTexCommand(EpsScanCallback,\
                                                      FileListFromTex,None)
                                                         
      TexFile.close()

      #  See if any of the graphics files are in sub-directories. They shouldn't
      #  be, but people often do put them there.
      
      DirListFromTex = []
      for FileName in FileListFromTex :
         DirName = os.path.dirname(FileName)
         if (DirName != "") :
            if (not (DirName in DirListFromTex)) :
               DirListFromTex.append(DirName)

      #  Get a list of all the files in the directory and its subdirectories.
      #  (os.walk() returns details for each directory found, and we pass the
      #  directory name and its list of files to CalledFromWalk() - defined
      #  above - and this adds the paths for all files - minus any leading './'
      #  - to FileList.)
      
      FileList = []
      for Details in os.walk('.') :
          CalledFromWalk(FileList,Details[0],Details[2])

      #  First, simply list all the graphics files specified by the .tex file.
      
      if (len(FileListFromTex) > 0) :
         if (not BatchMode) :
            print("Graphics files used by",TexFileName,":")
            for FileName in FileListFromTex :
               print("    ",FileName)
         if (len(DirListFromTex) > 0) :
            Problem = "Some graphics files are in sub-directories"
            if (BatchMode) : Problems.append(Problem)
            else : print("**",Problem,"**")
         
         #  Now run through them again, checking for files with .eps extensions.
         #  If so, see if they were supplied. 
         
         for FileName in FileListFromTex :
            if (not FileName.endswith(".eps")) :
            
               #  It didn't end with .eps. See what it did end with.
               
               Ext = os.path.splitext(FileName)[1]
               if (Ext == "") :
               
                  #  Here, the .tex file did not specify an extension. It will
                  #  default to any graphics file in the directory, which may
                  #  or may not be a .eps file. There are a number of tricky
                  #  possibilities here.
                  
                  MatchedFiles = []
                  EpsMatch = False
                  for File in FileList :
                     if (File.startswith(FileName + '.')) :
                        MatchedFiles.append(File)
                        if (os.path.splitext(File)[1] == ".eps") :
                           EpsMatch = True
                  if (len(MatchedFiles) != 1) : ReturnOK = False;
                  if (len(MatchedFiles) > 1) :
                     Problem = FileName + " may default to any of:"
                     if (BatchMode) : Problems.append(Problem)
                     else : print("**",Problem,"**")
                     Files = ""
                     for Match in MatchedFiles :
                        Files = Files + Match + " "
                     if (BatchMode) : Problems.append(Files)
                     else : print("    ",Files)
                     if (EpsMatch) :
                        Problem = "Only one of which is an eps file"
                     else :
                        Problem = "None of which seem to be suitable"
                        if (BatchMode) : Problems.append(Problem)
                        else : print("**",Problem,"**")
                  elif (len(MatchedFiles) == 1) :
                     if (EpsMatch) :
                        Note = "(Note: " + FileName + \
                                                      " will default to .eps )"
                        if (not BatchMode) : print(Note)
                     else :
                        Problem = FileName + \
                         " will default to the non-eps file " + MatchedFiles[0]
                        ReturnOK = False
                        if (BatchMode) : Problems.append(Problem)
                        else : print("**",Problem,"**")
                  else :
                     Problem = "No files match " + FileName
                     if (BatchMode) : Problems.append(Problem)
                     else : print("**",Problem,"**")

               else :
               
                  #  A non-eps extension needs to be noted. See if the
                  #  file exists and if not warn about that as well.
                  
                  Problem = FileName + " does not have a .eps extension"
                  if (BatchMode) : Problems.append(Problem)
                  else : print("**",Problem,"**")
                  if (not os.path.exists(FileName)) :
                     Problem = FileName + " has not been supplied"
                     if (BatchMode) : Problems.append(Problem)
                     else : print("**",Problem,"**")
                  ReturnOK = False
                     
         if (not BatchMode) : print(" ")
      
      #  List all the .eps files in the current directory.
      
      EpsFileList = []
      for File in FileList :
         if (not File.startswith('.')) :
            if (File.endswith(".eps")) : EpsFileList.append(File)
      if (not BatchMode) :
         print(".eps files supplied:")
         if (len(EpsFileList) > 0) :
            for FileName in EpsFileList :
               print("    ",FileName.strip())
            print(" ")
      
      #  See if all the .eps files are used by the .tex file.
      
      if (len(EpsFileList) == 0) :
         if (not BatchMode) : print("No .eps files found")
      else :
         AllFound = True
         for EpsFile in EpsFileList :
            Found = False
            for GraphicsFile in FileListFromTex :
               if (GraphicsFile == EpsFile) :
                  Found = True
                  break
               if (GraphicsFile.lower() == EpsFile.lower()) :
                  Found = True
                  CaseProblems = True
                  Problem = GraphicsFile + " matches " + EpsFile + \
                                                       " but has different case"
                  if (BatchMode) : Problems.append(Problem)
                  else : print("**",Problem,"**")
                  break
               if (GraphicsFile.find('.') < 0) :
                  if (GraphicsFile + ".eps" == EpsFile) :
                     Found = True
                     break
                  if (GraphicsFile.lower() + ".eps" == EpsFile.lower()) :
                     Found = True
                     CaseProblems = True
                     Problem = GraphicsFile + " matches " + EpsFile + \
                                                      " but has different case"
                     if (BatchMode) : Problems.append(Problem)
                     else : print("**",Problem,"**")
                     break
            if (not Found) :
               Warning = EpsFile + " is not used in the .tex file"
               if (BatchMode) : Warnings.append(Warning)
               else : print("*",Warning,"*")
               AllFound = False
         if (AllFound) :
            if (not BatchMode) :
               print( \
                   "All .eps files in the directory are used by the .tex file")
         else :
            ReturnOK = False
      
      #  See if all the files used by the .tex file are in the directory.
      #  At this point, we assume that if no extension was specified, it
      #  will default to .eps. Note that if we are running on a file system that
      #  is case-insensitive (eg OS X in most cases), you can get away with case
      #  errors in the file names that will cause problems on other systems.
      #  File names should match properly, but we don't want to flag a file as
      #  missing just because of a case error.
      
      if (len(FileListFromTex) == 0) :
         if (not BatchMode) : print("No graphics files used by the .tex file")
      else :
         AllFound = True
         AllEps = True
         CaseProblems = False
         for GraphicsFile in FileListFromTex :
            if (os.path.splitext(GraphicsFile)[1] == "") :
               GraphicsFile = GraphicsFile + ".eps"
            Found = False
            for EpsFile in EpsFileList :
               if (EpsFile == GraphicsFile) :
                  Found = True
                  break
               if (EpsFile.lower() == GraphicsFile.lower()) :
                  Found = True
                  CaseProblems = True
                  Problem = EpsFile + " matches " + GraphicsFile + \
                                                       " but has different case"
                  if (BatchMode) : Problems.append(Problem)
                  else : print("**",Problem,"**")
                  break
            if (not Found) :
               for File in FileList :
                  if (File == GraphicsFile) :
                     Found = True
                     AllEps = False
                     break
                  if (File.lower() == GraphicsFile.lower()) :
                     Found = True
                     AllEps = False
                     CaseProblems = True
                     Problem = File + " matches " + GraphicsFile + \
                                                       " but has different case"
                     if (BatchMode) : Problems.append(Problem)
                     else : print("**",Problem,"**")
                     break
            if (not Found) :
               Problem = GraphicsFile + " is missing from the directory"
               if (BatchMode) : Problems.append(Problem)
               else : print("**",Problem,"**")
               AllFound = False
               ReturnOK = False
         if (AllFound) :
            if (not BatchMode) :
               print("All graphics files used by the .tex file are supplied")
            if (not AllEps) :
               Problem = "Not all graphics files are .eps files"
               if (BatchMode) : Problems.append(Problem)
               else : print("**",Problem,"**")
               ReturnOK = False
            if (len(DirListFromTex) > 0) :
               Problem = "Graphics files should not be in subdirectories"
               if (BatchMode) : Problems.append(Problem)
               else : print("**",Problem,"**")
               ReturnOK = False

         if (CaseProblems) :
            Problem = \
                 "Some graphics files names have problems with upper/lower case"
            if (BatchMode) : Problems.append(Problem)
            else : print("**",Problem,"**")
            ReturnOK = False

   return ReturnOK
               
# ------------------------------------------------------------------------------

#                       E p s  S c a n  C a l l b a c k
#
#   Used as the callback routine for the TexScanner when it is used to scan
#   the .tex file for references to figures that should be supplied in files.
#   Words are the components of a LaTeX directive parsed by the TexScanner. If
#   this is a recognised graphics command, the specified file name will be
#   added to FileListFromTex, which is a list of strings. TexScanner supplies
#   an additional argument when it makes the callback, but this is unused here.
#   File names already in the list are not added to it - some .tex files use
#   the same image more than once. Any leading "./" characters are removed from
#   the file names; I don't think they should really be there, but this makes
#   things consistent with the way the files found in the directory are handled
#   when the two are compared by VerifyEps().

def EpsScanCallback (Words,FileListFromTex,Unused) :
   if (len(Words) > 0) :
      if (Words[0] == "\\includegraphics" or \
            Words[0] == "\\articlefigure" or \
               Words[0] == "\\articlefiguretwo" or \
                  Words[0] == "\\articlefigurethree" or \
                     Words[0] == "\\articlefigurefour" or \
                        Words[0] == "\\articlelandscapefigure" or \
                           Words[0] == "\\articlelandscapefiguretwo" or \
                              Words[0] == "\\plotone" or \
                                 Words[0] == "\\plottwo" or \
                                    Words[0] == "\\plotfiddle") :
         FileCount = 0
         MaxFiles = 1
         if (Words[0].find("two") > 0) : MaxFiles = 2;
         if (Words[0].find("three") > 0) : MaxFiles = 3;
         if (Words[0].find("four") > 0) : MaxFiles = 4;
         for Word in Words[1:] :
            if (Word != "") :
               if (Word[0] == '{') :
                  FileCount = FileCount + 1
                  File = Word.strip("{}")
                  if (File.startswith("./")) : File = File[2:]
                  File = File.strip()
                  if (not File in FileListFromTex) :
                     FileListFromTex.append(File)
                  if (FileCount >= MaxFiles) : break
                  
# ------------------------------------------------------------------------------

#                        T r i m  B i b  F i l e
#
#  A rather crude utility that comments out any references defined in the
#  adass conference .bib file in the default directory that are unused by
#  the main .tex file for the specified paper in the same default directory.
#  The unused entries can be either commented out or deleted entirely, 
#  depending on the Keep argument.
#
#  Note that BibTeX has unusual commenting arrangements. Strictly, it does 
#  not recognise '%' as introducing a comment, but rather treats anything
#  not included in a reference (introduced by a line with an @) as a comment.
#  So you can't comment out a line within a reference by starting it with '%'.
#  More unusually, if a line starts, for example, '%@inproceedings' it treats
#  the % as a comment outside the reference block, which it assumes starts 
#  with the @inproceedings. So this program puts % characters at the start
#  of each commented out block, as this makes it stand out in most LaTeX-aware
#  editors, which can be useful, but it also replaces that crucial '@'
#  with '_AT_' (which strictly is all that it needs to do).
#
#  Really, of course, there's no need to comment out the unused items, once
#  we can be confident the program works properly - they could just be
#  deleted entirely, and that's an option here that can triggered by setting
#  the Keep argument false.

def TrimBibFile (Paper,Keep = True) :

   BibFileName = FindBibFile(Paper)
   BibFileRefs = GetBibFileRefs(BibFileName)
   print("")
   print("References in",BibFileName," :")
   for BibRef in BibFileRefs :
      print("   ",BibRef)
   print("")
   
   if (len(BibFileRefs) > 0) :
   
      TexFileRefs = []
      BibItemRefs = []
      
      ParsedOK = True
   
      TexFileName = os.path.abspath(Paper + ".tex")
      if (not os.path.exists(TexFileName)) :
         print("Cannot find main .tex file",TexFileName)
      else :
   
         GetTexFileRefs (TexFileName,TexFileRefs,BibItemRefs)
         
         BibFile = open(BibFileName,mode='r')
         ModBibFileName = "oldReferences.bib"
         ModBibFile = open(ModBibFileName,mode='w')
         Changed = False
         CommentingOut = False
         BraceCount = 0
         LineCount = 0
         for BibFileLine in BibFile :
         
            #  The parsing here is rather crude. It assumes that each
            #  starts with a line that begins "@type{name" and goes on
            #  to count '{' and '}' characters and assumes the entry 
            #  ends when these are balanced. There may be files that
            #  break this, but most should be OK.
            
            LineCount = LineCount + 1
            ThisIsAComment = False
            if (not BibFileLine.strip().startswith('%')) :
               if (CommentingOut) :
                  BraceCount = BraceCount + BibFileLine.count('{') - \
                                              BibFileLine.count('}')
                  if (BraceCount <= 0) :
                     CommentingOut = False
                     BraceCount = 0
                  BibFileLine = '%' + BibFileLine
                  ThisIsAComment = True
               else :
                  if (BibFileLine.strip().startswith("@")) :
                  
                     #  Lines starting with '@' indicate a new reference.
                     #  Extract the name, then see if this is one that's in
                     #  the list of those used by the .tex file. This 
                     #  parsing has problems with cases where the name is on
                     #  the next line. Handling this is tricky, as we don't
                     #  know if we want to keep the reference until we've read
                     #  the second line. For the moment, we just flag the
                     #  problem and keep the reference.
                     
                     Brace = BibFileLine.find("{")
                     if (Brace > 0) :
                        Comma = BibFileLine.find(",")
                        if (Comma > 0) :
                           Ref = BibFileLine[Brace + 1:Comma]
                        else :
                           Ref = BibFileLine[Brace + 1:]
                        Ref = Ref.strip()
                        Used = False
                        if (Ref == "") :
                           print("** Blank name in .bib file at line",\
                                                              LineCount,"**")
                           ParsedOK = False
                           Used = True
                        for TexFileRef in TexFileRefs :
                           if (Ref == TexFileRef.strip()) :
                              Used = True
                              print("Keeping reference",Ref)
                              break
                        if (not Used) :
                           BibFileLine = '%' + BibFileLine.replace('@',"_AT_")
                           if (Keep) :
                              print("Commenting out unused reference",Ref)
                           else :
                              print("Deleting unused reference",Ref)
                           Changed = True
                           CommentingOut = True
                           ThisIsAComment = True
                           BraceCount = BibFileLine.count('{') - \
                                              BibFileLine.count('}')
            WriteThis = True
            if (ThisIsAComment and (not Keep)) : WriteThis = False
            if (WriteThis) : ModBibFile.write(BibFileLine)
         ModBibFile.close()
         BibFile.close()
         
         if (Changed) :
            os.rename(BibFileName,BibFileName + ".old")
            os.rename(ModBibFileName,BibFileName)
         else :
            os.unlink(ModBibFileName)
            
         if (not ParsedOK) :
            print("")
            print("** Problem parsing the file may mean an unused reference")
            print("has been kept. Suggest running RefCheck and editing the")
            print("file to fix the parsing problem if necessary **")

# ------------------------------------------------------------------------------

#                           G e t  I n i t i a l
#
#  Given a forename, and an index into it (which will usually be 0, but
#  might be more if there is hyphenation involved), returns the initial letter
#  at that index position in the forename. Usually, this will just be the
#  character at Forename[Index], but this allows for initials using one of 
#  the special character sequences of the form "\x{c}" such as \c{c} for a 
#  c-cedilla. Notes is a list to which any message may be appended.
 
def GetInitial (Forename,Index,Notes) :
   Initial = Forename[Index]
   Letter = Initial
   if (Initial == '\\') :
      Initial = '?'
      Len = len(Forename)
      if (len(Forename) > Index + 4) :
         if (Forename[Index + 2] == '{' and Forename[Index + 4] == '}') :
            Initial = Forename[Index:Index + 5]
            Letter = Forename[Index + 3]
   if (Initial == '?') :
      Note = "Unexpected control sequence for initial in " + Forename
      Notes.append(Note)
   else :
      if (Letter.islower()) :
         Note = "Initial letter in '" + Forename + "' is in lower case"
         Notes.append(Note)
            
   return Initial
            
# ------------------------------------------------------------------------------

#                       A u t h o r  S c a n  C a l l b a c k
#
#   Used as the callback routine for the TexScanner when it is used to scan
#   the .tex file for an author list. Words are the components of a LaTeX
#   directive parsed by the TexScanner. If this is the list of authors in
#   the paper (the \author directive) this parses the arguments to that
#   directive and adds to the supplied AuthorList argument one string for
#   each author, formatted in the <Surname><Initials> format required - eg
#   "Shortridge,~K." Notes should be a list to which this will append strings
#   briefly describing any possible problems the routine has spotted while
#   processing the author list. If there are any such notes, the raw author
#   list will be appended as a final note.
#
#   (This originally quite simple code got messier and messier as more and
#   more edge cases - hyphenated names, accented names, suffixes like Jr.,
#   van der This and von That, etc. - turned up and were handled. It really
#   would benefit from a redesign, but it seems to work fairly well now, so
#   long as you have a good look at what it produces and don't trust it
#   implicitly to get every name perfect. At the moment, the main ones I've
#   seen that it gets wrong are a) cases such as 'An Author, for the rest of
#   the team', which really don't fit the standard format, and b) Spanish names
#   where the surname is two separate names, not hyphenated, where there really
#   is no obvious way to tell if a 'middle' name is a forename or part of the
#   surname. Think Mario Vargas Llosa. At least both these cases are picked up
#   by the code and reported in Notes.)
#   

def AuthorScanCallback(Words,AuthorList,Notes) :

   if (len(Words) > 1) :
      if (Words[0] == "\\author") :
         Authors = Words[1].strip()
         Len = len(Authors)
         if (Len > 0) :
            if (Authors.startswith('{')) :
            
               #  Trim down to just the list of authors. Lose the leading '{'
               #  and then anything following \affil. There ought to be an
               #  \affil, but if there isn't, lose the trailing '}'.
               
               EndIndex = Authors.find("\\affil")
               if (EndIndex < 0) :
                  EndIndex = Authors.rfind('}')
               if (EndIndex <= 0) :
                  Notes.append("Misformed author list")
               else :
                  Authors = Authors[1:EndIndex]
                  
                  #  For our purposes, "\ " is just a space. And we aren't 
                  #  interested in forced line breaks - "\\" or "\\*". (It's
                  #  important to do these in the right order!)
                  
                  Authors = Authors.replace("\\\\*",'')
                  Authors = Authors.replace("\\\\",'')
                  Authors = Authors.replace("\\ ",' ')
                  
                  #  If we have any issues, it helps to report the author
                  #  list in as raw a form as possible. What we have at this 
                  #  point will probably do.
                  
                  RawAuthors = Authors
                  
                  #  Some constructs involving a space are confusing. If
                  #  anyone has set c-cedilla as '\c c' we replace it with
                  #  the equivalent '\c{c}'. There are others.
                  
                  Accents = "`'^\"H~ckl=b.druv"
                  for Char in Accents :
                     More = True
                     while (More) :
                        Index = Authors.find('\\'+Char+' ')
                        if (Index >= 0) :
                           Cposn = Index + 3
                           if (Cposn < len(Authors)) :
                              Str = '\\'+Char+' '+Authors[Cposn]
                              Repl = '\\'+Char+'{'+Authors[Cposn]+'}'
                              Authors = Authors.replace(Str,Repl)
                        else :
                           More = False
                                                
                  #  We should now have a comma-separated author list.
                  #  Lose anything in math (between $signs$) because these
                  #  will be the affiliation superscripts (and if they contain
                  #  commas, eg "$^{1,2}$" this confuses the splitting into
                  #  individual names). We replace any math expression by a 
                  #  single space, so that it acts as a separator. We only 
                  #  expect one math expression per author - more may be
                  #  an indication of a missing comma.
                  #
                  #  Replacing the math expression with a comma instead of a
                  #  space would allow us to get the index entries right, but
                  #  might confuse the comma count, including the check for
                  #  a missing serial comma, and that's not a good thing.
                  
                  Authors = Authors.strip()
                  Len = len(Authors)
                  InMath = False
                  AString = ""
                  MathCount = 0
                  Posn = 0
                  for Index in range(Len) :
                     Char = Authors[Index]
                     if (Char == '$') :
                        if (InMath) :
                           InMath = False
                           if (MathCount > 0 and Index < (Len - 1)) :
                              Notes.append("Possible missing comma near '" + \
                                               Authors[Posn:Index] + "'")
                           MathCount = MathCount + 1
                           Posn = Index
                        else :
                           InMath = True
                           AString = AString + ' '
                     else :
                        if (not InMath) :
                           if (Char == ',') : MathCount = 0 
                           AString = AString + Char
                        
                  #  The exception to the rule that all names are separated
                  #  by commas is the two author case, where they are separated
                  #  by 'and'. Trap that case and insert the comma to make
                  #  the split work properly.
                  
                  if (AString.find(',') < 0) :
                     AndIndex = AString.find(" and ")
                     if (AndIndex > 0) :
                        AString = AString[:AndIndex] + ',' + \
                                              AString[AndIndex:]
                  
                  #  And I've seen people get carried away with commas at the
                  #  end of the each author in the list.
                  
                  AString = AString.strip()
                  Len = len(AString)
                  if (Len > 0) :                       
                     if (AString[Len - 1] == ',') :
                        Note = "Extraneous comma at end of author list"
                        Notes.append(Note)
                        AString = AString[:Len - 1]
                  
                  #  Split the string as we have it now into what we hope 
                  #  are the individual name sections - the bits separated
                  #  by commas.
                            
                  AList = AString.split(",")
                  
                  #  Missing out the final serial comma is a common mistake
                  #  in multi-author lists. It's worth going to the trouble
                  #  of checking for that and pointing it out. If we find
                  #  the last 'author' has an 'and' other than at the start,
                  #  we replace it with a comma and redo the splitting.
                  
                  NAuthors = len(AList)
                  if (NAuthors > 0) :
                     Author = AList[NAuthors - 1]
                     if (Author == "") :
                        if (NAuthors > 1) : Author = AList[NAuthors - 2]
                     Author = Author.replace('~',' ').replace('.',' ').strip()
                     if ( not Author.startswith("and")) :
                        if (Author.find(" and ") >= 0) :
                           Note = "Note: '" + Author + \
                                           "' may have a missing serial comma."
                           Notes.append(Note)
                           AString = AString.replace(" and ",',')
                           AList = AString.split(",")
                  
                  #  Now go through all of what should be individual authors.
                  
                  OrderWarning = False
                  Len = len(AList)
                  for Index in range(Len) :
                  
                     Author = AList[Index]
                  
                     #  '~' and '.' characters just confuse things. We want the
                     #  individual names (or initials, we don't care which).
                     #  So "Yet Another Author" will split into the list
                     #  "Yet","Another" and "Author" and "A.~N.~Other" will
                     #  split into "A","N" and "Other". The idea then is
                     #  that we take the last item as the surname, and we use
                     #  the first characters from the others as the initials.
                     
                     #  To complicate things, we need to distinguish between
                     #  "\~" (which we need to keep; it generates a diacritical
                     #  tilde, or virgulilla, for Spanish words) and '~' which
                     #  is just a space and which we want to drop. What's done
                     #  here is messy - turn "\~" into "\twiddle" and then
                     #  revert - but it works.
                     
                     SlashTwiddle = Author.find("\\~")
                     if (SlashTwiddle >= 0) :
                        Author = Author.replace("\\~","\\twiddle")
                        
                     Author = Author.replace('~',' ').replace('.',' ').strip()
                     
                     if (SlashTwiddle >= 0) :
                        Author = Author.replace("\\twiddle","\\~")
                     
                     #  Ignore any leading 'and', but there ought to be one
                     #  for the last of more than one author, and not in any
                     #  other case.
                     
                     AndExpected = (Index == (Len - 1) and Len > 1)
                     if (Author.startswith("and")) :
                        Author = Author[4:]
                        if (not AndExpected) :
                           Note = "Note: unexpected 'and' before last author"
                           Notes.append(Note)
                     else :
                        if (AndExpected) :
                           Note = "Note: 'and' missing from last of " + \
                                                       "multiple authors"
                           Notes.append(Note)
                            
                     NameList = Author.split()
                     
                     #  Check for some of the more obvious examples of
                     #  the 'on behalf of the rest of the team' type of
                     #  final 'author'.
                     
                     IffyNames = ""
                     IffyCount = 0
                     for Name in NameList :
                        LowerName = Name.lower()
                        if (LowerName == "on" or LowerName == "behalf" or 
                              LowerName == "team" or LowerName == "the" or
                                 LowerName == "of") :
                           if (IffyCount == 0) :
                              IffyNames = Name
                           else : 
                              IffyNames = IffyNames + ', ' + Name
                           IffyCount = IffyCount + 1
                     if (IffyCount > 0) :
                        Notes.append("The following may not be real names: " + \
                                                                      IffyNames)
                                            
                     #  We assume the last is the surname. We then look back
                     #  from that, looking for possible multi-name surnames,
                     #  like "Van der Waals". Each time we find one, we
                     #  prepend it and go back one more. A variation on this 
                     #  is if there is a suffix like "Jr", "Sr", or even "II"
                     #  or "III" or more.
                     
                     NumNames = len(NameList)
                     if (NumNames > 0) :
                     
                        Suffix = ""
                        Surname = NameList[NumNames - 1]
                        if (NumNames > 1) :
                           if (Surname.lower() == "jr") :
                              Suffix = "Jr."
                           elif (Surname.lower() == "sr") :
                              Suffix = "Sr."
                           elif (Surname == "II" or Surname == "III" or
                                    Surname == "IV" or Surname == "V") :
                              Suffix = Surname
                           if (Suffix != "") :
                              NumNames = NumNames - 1
                              Surname = NameList[NumNames - 1]
                        
                        #  Check for unusual examples of upper or lower case
                        #  in the surname. (This picks up cases such as
                        #  "and all my co-workers".)
                        
                        FirstLetter = True
                        PrevChar = ''
                        PrevChars = ""
                        for Char in Surname :
                           if (FirstLetter) : 
                              if (Char.islower()) :
                                 Notes.append("Surname '" + Surname + "'" + \
                                                      " starts in lower case")
                              FirstLetter = False
                           else :
                              if (Char.isupper() and PrevChar != '-' and \
                                    PrevChar != "'" and PrevChars != "Mac" \
                                                       and PrevChars != "Mc") :
                                 Notes.append("Surname '" + Surname + "'" + \
                                            " contains upper case characters")
                                 break
                           PrevChar = Char
                           PrevChars = PrevChars + Char
                                    
                        NumNames = NumNames - 1
                        Multiple = False
                        while (NumNames > 0) :
                           PrevName = NameList[NumNames - 1]
                           if (PrevName.lower() == "van" or \
                                 PrevName.lower() == "de" or \
                                   PrevName.lower() == "den" or \
                                     PrevName.lower() == "von" or \
                                       PrevName.lower() == "le" or \
                                          PrevName.lower() == "da" or \
                                             PrevName.lower() == "di" or \
                                                PrevName.lower() == "der") :
                              Surname = PrevName + ' ' + Surname
                              Multiple = True
                              NumNames = NumNames - 1
                           else :
                              break
                        if (Multiple) :
                           Notes.append(Surname + " assumed to be a surname")
                        
                        #  At this point we have the surname, and NumNames
                        #  should be the number of forenames/initials.
                        
                        NameString = Surname + ','
                        
                        #  This is an attempt to trap the 'Spanish surname'
                        #  case, where Mario Vargas Llosa's surname is actually
                        #  Vargas Llosa. If there is more than one forename,
                        #  and if the last is spelled out, we may have such a
                        #  name. We should at least make a note of it.
                        
                        if (NumNames > 1) :
                           LastForename = NameList[NumNames - 1]
                           Letters = 0
                           for Char in LastForename :
                              if (Char.isupper() or Char.islower()) :
                                 Letters = Letters + 1
                           if (Letters > 1) :
                              Notes.append("Might '" + LastForename + ' ' \
                                             + Surname + "' be a surname?")
                     
                        #  If the surname is a single letter and the forename(s)
                        #  are longer, this might be a case where the names
                        #  have been given with the surname last instead of
                        #  first.
                        
                        if (len(Surname) == 1) :
                           if (NumNames > 0) :
                              if (len(NameList[0]) > 1) :
                                 if (not OrderWarning) :
                                    Notes.append(
                                       "Names should end with the surname")
                                    OrderWarning = True
                                 Notes.append("Might " + NameList[0] + ' ' + \
                                    Surname + " have been given surname first?")
                        
                        #  Now reduce the forenames to initials.
                        
                        InitialCount = 0
                        for Forename in NameList[:NumNames] :
                           Initial = GetInitial(Forename,0,Notes)
                           InitialCount = InitialCount + 1
                           
                           #  This bit is being clever and combining pairs
                           #  of hyphenated initials, catching cases like
                           #  Jean-Luc Picard or even J.-L. Picard (the
                           #  former will have been split into two strings,
                           #  the latter into three).
                           
                           if (Initial == '-') :
                              Initial = GetInitial(Forename,1,Notes)
                              NameString = NameString + '-' + Initial + '.'
                           else :
                              NameString = NameString + '~' + Initial + '.'
                              DashIndex = Forename.find('-')
                              if (DashIndex > 0) :
                                 Initial = \
                                    GetInitial(Forename,DashIndex + 1,Notes)
                                 NameString = NameString + '-' + Initial + '.'
                        if (Suffix != "") :
                           NameString = NameString + ",~" + Suffix
                        AuthorList.append(NameString)
                        if (InitialCount == 0) :
                           if (len(Surname) == 1) :
                              Notes.append("Might " + Surname + \
                                                     " be a misplaced initial?")
                           else :
                              Notes.append(
                                        Surname + " seems to be just a surname")
                  
                  #  If we had any problems, we append the raw author list
                  
                  if (len(Notes) > 0) :
                     Notes.append(RawAuthors)
                     
# ------------------------------------------------------------------------------

#                         G e t   A u t h o r s
#
#   This routine looks in the current directory for a file called 
#   Paper.tex (where Paper will be a string such as "O1-4"), assuming
#   this is the main .tex file for the paper. It looks for the author list
#   in the paper and returns a list of authors (as generated by the callback
#   routine AuthorScanCallback) with an entry for each author in the form
#   required as the argument to an \aindex directive, eg "Shortridge,~K.".
#   Notes is a list to which this adds a brief description of anything 
#   possibly amiss that it comes across when processing the author list.



def GetAuthors (Paper,Notes,TexFileName = "") :

   AuthorList = []
   
   if (TexFileName == "") : TexFileName = Paper + ".tex"
   TexFileName = os.path.abspath(TexFileName)
   if (not os.path.exists(TexFileName)) :
      print("Cannot find main .tex file",TexFileName)
   else :

      #  Now get a list of the authors from the .tex file.

      TexFile = open(TexFileName,mode='r')
      TheScanner = TexScanner.TexScanner()
      TheScanner.SetFile(TexFile)
      
      #  GetNextTexCommand() will call AuthorScanCallback for each command it
      #  finds in the file, and AuthorScanCallback will check the command
      #  and add the list of authors to AuthorList.
      
      Finished = False
      while (not Finished) :
         Finished =  TheScanner.GetNextTexCommand(AuthorScanCallback,\
                                                      AuthorList,Notes)
                                                         
      TexFile.close()

   return AuthorList

# ------------------------------------------------------------------------------

#                   C h a r a c t e r  E n c o d i n g s
#
#   Latin1_LaTeX_Chars is a dictionary giving LaTeX sequences equivalent to
#   various characters in the LATIN-1 character set that are often seen in
#   ADASS papers. The characters are given by their hex values. Note that
#   these codes are also used for these characters in Unicode, so this can
#   also be used to get the LaTeX sequences equivalent to this subset of
#   Unicode characters (ones in the range U+00C0 to U+00FF). This is not a
#   complete set, but it should include any likely to appear in ADASS papers.
#
__Latin1_LaTeX_Chars__ = \
    { 0xc0:"\\`{A}", 0xc1:"\\'{A}", 0xc2:"\\^{A}", 0xc3:"\\~{A}", \
      0xc4:'\\"{A}', 0xc5:"\\.{A}", \
      0xc7:"\\c{C}", \
      0xc8:"\\`{E}", 0xc9:"\\'{E}", 0xca:"\\^{E}", 0xcb:"\\~{E}", \
      0xcc:"\\`{I}", 0xcd:"\\'{I}", 0xce:"\\^{I}", 0xcf:"\\~{I}", \
      0xd1:"\\~{N}", \
      0xd2:"\\`{O}", 0xd3:"\\'{O}", 0xd4:"\\^{O}", 0xd5:"\~{O}",  \
      0xd6:'\\"{O}', 0xd8:'\\o{O}', \
      0xd9:"\\`{U}", 0xda:"\\'{U}", 0xdb:"\\^{U}", 0xdc:'\\"{U}', \
      0xdd:"\\'{Y}", 0xdf:"{\\ss}", \
      0xe0:"\\`{a}", 0xe1:"\\'{a}", 0xe2:"\\^{a}", 0xe3:"\\~{a}", \
      0xe4:'\\"{a}', 0xe5:"\\.{a}", \
      0xe7:"\\c{c}", \
      0xe8:"\\`{e}", 0xe9:"\\'{e}", 0xea:"\\^{e}", 0xeb:"\\~{e}", \
      0xec:"\\`{i}", 0xed:"\\'{i}", 0xee:"\\^{i}", 0xef:"\\~{i}", \
      0xf1:"\\~{n}", \
      0xf2:"\\`{o}", 0xf3:"\\'{o}", 0xf4:"\\^{o}", 0xf5:"\\~{o}", \
      0xf6:'\\"{o}', 0xf8:'\\o{o}', \
      0xf9:"\\`{u}", 0xfa:"\\'{u}", 0xfb:"\\^{u}", 0xfc:'\\"{u}', \
      0xfd:"\\'{y}", 0xff:'\\"{y}' }

#  Macintosh_LaTeX_Chars is another dictionary, like Latin1_LaTeX_Chars, this
#  time giving the LaTeX sequences equivalent to various characters in the
#  old Mac OS Roman character set. Files encoded in Mac OS Roman are relatively
#  rare among ADASS papers, but are still seen from time to time, although
#  generally very few of the characters are used. The em- and en-dashes are
#  seen, as is the posessive apostrophe (at 0xd5, occasionally mis-converted
#  into the Latin-1 upper case O with a tilde).

__Macintosh_LaTeX_Chars__ = \
   {  0x80:'\\"{A}', 0x81:"\\.{A}", 0x82:"\\c{C}", 0x83:"\\'{E}", \
      0x84:"\\~{N}", 0x85:'\\"{O}', 0x86:'\\"{U}', 0x87:"\\'{a}", \
      0x88:"\\`{a}", 0x89:"\\^{a}", 0x8a:'\\"{a}', 0x8b:"\\~{a}", \
      0x8c:"\\.{a}", 0x8d:"\\c{c}", 0x8e:"\\'{e}", 0x8f:"\\`{e}", \
      0x90:"\\^{e}", 0x91:'\\"{e}', 0x92:"\\'{i}", 0x93:"\\`{i}", \
      0x94:"\\^{i}", 0x95:'\\"{i}', 0x96:"\\~{n}", 0x97:"\\'{o}", \
      0x98:"\\`{o}", 0x99:"\\^{o}", 0x9a:'\\"{o}', 0x9b:"\\~{o}", \
      0x9c:"\\'{u}", 0x9d:"\\`{u}", 0x9e:"\\^{u}", 0x9f:'\\"{u}', \
      0xca:"~", \
      0xcb:"\\`{A}", 0xcc:"\\~{A}", 0xcd:"\\~{O}", \
      0xd0:"--",     0xd1:"---", \
      0xd2:"``",     0xd3:"''",     0xd4:"`",      0xd5:"'", \
      0xd8:'\\"{y}', 0xd9:'\\"{Y}',
      0xe5:"\\^{A}", 0xe6:"\\^{E}", 0xe7:"\\'{A}", 0xe8:'\\"{E}', \
      0xe9:"\\`{E}", 0xea:"\\'{I}", 0xeb:"\\^{I}", 0xec:'\\"{I}', \
      0xee:"\\'{O}", 0xef:"\\^{O}", 0xf1:"\\`{O}", \
      0xf2:"\\'{U}", 0xf3:"\\^{U}", 0xf4:"\\`{U}" }

#  Unicode_LaTeX_Chars is yet another dictionary, this time for Unicode
#  characters. It clearly doesn't cover the whole of the Unicode character
#  set. Instead it covers those characters that have been seen to date in
#  ADASS papers, together with some others that seem like plausible options.
#  Note that Unicode and Latin-1 overlap, so characters in the U+80 to U+FF
#  are covered by the Latin1 directory, in the same way that Unicode characters
#  in the range U+00 to U+7F are standard ASCII characters. So if a character
#  is not found in this dictionary, it might be in Latin1_LaTeX_Chars.
#  The U+FFFD replacement character is rendered as '???' which is probably
#  the best we can do.

__Unicode_LaTeX_Chars__ = \
   {  0x0391:"A",         0x0392:"B",           0x0393:"$\\Gamma$",  \
      0x0394:"$\\Delta$", 0x0395:"E",           0x0396:"Z",      \
      0x0397:"H",         0x0398:"$\\Theta$",   0x0399:"I",  \
      0x039a:"K",         0x039b:"$\\Lambda$",  0x039c:"M", \
      0x039d:"N",         0x039e:"$\\Xi$",      0x039f:"O",    \
      0x03a0:"$\\Pi$",    0x03a1:"P",
      0x03a3:"$\\Sigma$", 0x03a4:"T",           0x03a5:"$\\Upsilon$",
      0x03a6:"$\\Phi$",   0x03a7:"X",           0x03a8:"$\\Psi$",
      0x03a9:"$\\Omega$", \
      0x03b1:"$\\alpha$", 0x03b2:"$\\beta$",    0x03b3:"$\\gamma$", \
      0x03b4:"$\\delta$", 0x03b5:"$\\epsilon$", 0x03b6:"$\\zeta$", \
      0x03b7:"$\\eta$",   0x03b8:"$\\theta$",   0x03b9:"$\\iota$",    \
      0x03ba:"$\\kappa$", 0x03bb:"$\\lambda$",  0x03bc:"$\\mu$", \
      0x03bd:"$\\nu$",    0x03be:"$\\xi$",      0x03bf:"$\\omicron$", \
      0x03c0:"$\\pi$",    0x03c1:"$\\rho$",     0x03c2:"$\\varsigma$", \
      0x03c3:"$\\sigma$", 0x03c4:"$\\tau$",     0x03c5:"$\\upsilon$", \
      0x03c6:"$\\phi$",   0x03c7:"$\\chi$",     0x03c8:"$\\psi$", \
      0x03c9:"$\\omega$", \
      0x2010:"-",         0x2013:"--",          0x2014:"---",     0x2018:"`", \
      0x2019:"'",         0x201c:"``",          0x201d:"''", \
      0xfffd:"???" }


#  Note: 0x03a2 is missing - there isn't an upper case equivalent of \varsigma,
#  which is itself only used in Greek writing, so probably isn't going to
#  turn up in many ADASS papers. Note that in LaTeX, Greek letters are all
#  math symbols.

# ------------------------------------------------------------------------------

#                         F i x  C h a r a c t e r s
#
#   This routine scans a Line read from a .tex file and checks for some of 
#   the more common foreign accented characters that can cause problems for an
#   English implementation of LaTeX. If it finds any that it recognises, it
#   replaces them with the equivalent LaTeX sequence - for example, it will
#   replace 0xe7 (the Ascii code for c-cedilla) with "\c{c}". If it makes no
#   changes to the string, it will return None. Otherwise it returns the 
#   modified string. The line number passed is used to output a message 
#   describing any changes made. (Pass it as zero to suppress such messages.)

def FixCharacters (Line,LineNumber,Encoding = "Latin1") :
   
   NewLine = None
   
   #  Quick pass to see if we have a problem
   
   Problem = False
   for Char in Line :
      if (not Char in string.printable) :
         Problem = True
         break
   
   if (Problem) :
      NewLine = ""

      LowEncoding = Encoding.lower()
      UseLatin1 = (LowEncoding == "latin1")
      UseMacRoman = (LowEncoding == "macroman")
      UseUnicode = (LowEncoding == "utf-8")
      UseAscii = (LowEncoding == "ascii")

      NChars = len(Line)
      Index = 0;
      while (Index < NChars) :
      
         Char = Line[Index]
         if (Char in string.printable) :
            NewLine = NewLine + Char
         else:
            Num = ord(Char)
            Repl = None
            Descrip = None
            IndexWas = Index
            if (UseAscii) :
               Descrip = "ASCII character (" + hex(Num) + ")"
            elif (UseLatin1) :
               Repl = __Latin1_LaTeX_Chars__.get(Num)
               Descrip = "Latin1 character (" + hex(Num) + ")"
            elif (UseMacRoman) :
               Repl = __Macintosh_LaTeX_Chars__.get(Num)
               Descrip = "Mac Roman character (" + hex(Num) + ")"
            elif (UseUnicode) :
               (IsUnicode, Unicode, NewIndex) = \
                                        CheckForUTF8Unicode(Line,Index,NChars)
               Index = NewIndex
               if (IsUnicode) :
                  Descrip = "Unicode character U+" + hex(Unicode)[2:]
                  Repl = __Unicode_LaTeX_Chars__.get(Unicode)
                  if (Repl == None) :
                     Repl = __Latin1_LaTeX_Chars__.get(Unicode)
               else :
                  Descrip = "Unexpected character (" + hex(Num) + \
                                                 " - not valid UTF-8 Unicode)"
            if (Descrip == None) :
               Descrip = "Unexpected character (" + hex(Num) + \
                            ") in unexpected encoding (" + Encoding + ")"
            if (Repl == None) :
               Text = Descrip + " in .tex file at line " + str(LineNumber) + \
                                                  " : LaTeX equivalent unknown"
               NewLine = NewLine + Char
               Index = IndexWas
            else :
               Text = Descrip + " in .tex file at line " + str(LineNumber) + \
                                                         " replaced by " + Repl
               NewLine = NewLine + Repl
            if (LineNumber != 0) : print(Text)
         Index = Index + 1

   return NewLine

# ------------------------------------------------------------------------------

#                    C h e c k  F o r  U T F  8  U n i c o d e
#
#   This utility routine is passed a byte string, which should be a line read
#   from what is assumed to be a LaTeX source file, which might be encoded
#   using UTF-8, together with the length of the line and an index into that
#   line. It returns a tuple (IsUnicode, Unicode, NewIndex) where IsUnicode is
#   true if a valid UTF-8 encoding of a Unicode character starts at the given
#   index value, Unicode is the integer value of that Unicode character, and
#   NewIndex is the index into of the last byte of that encoded Unicode
#   character, allowing the caller to skip over it. If no Unicode character was
#   found, NewIndex will simply be Index.
#
#   There may be ways of coding this up using Python modules designed to
#   handle UTF-8, but I thought this gave me more control, and was less likely
#   to have problems caused by the different ways strings are handled in
#   Python 2 and Python 3. Maybe I just like doing things the hard way.

def CheckForUTF8Unicode (Line,Index,Length) :

   #  Default return values
   
   NewIndex = Index + 1
   IsUnicode = False
   Unicode = 0
   
   #  Look at the character indicated by Index. This will normally be an
   #  ordinary ASCII (or possibly LATIN-1) single byte character. However,
   #  it might be the start of an encoded Unicode character. The way UTF-8
   #  encodes such characters in very clever, and quite complex. A good place
   #  to look for the details is https://en.wikipedia.org/wiki/UTF-8.
   #  UTF-8 encodes Unicode characters into an initial byte whose upper bits
   #  fit one of four bit patterns and whose lower bits contain some of the
   #  bits of the Unicode character. Depending on which of the four patterns
   #  that first byte has, it may be followed by a number of continuation
   #  bytes, all of which have the bit pattern 10xxxxxx where the 10 identifies
   #  the byte as a continuation characteer and the six xxxxxx bits contain
   #  more of the buts of the Unicode character.
   #  If he byte indicated by Index is the start of a Unicode sequence, it must
   #  fit one of the following bit patterns:
   #  0xxxxxxx - the low 7 bits gives a Unicode character in the range
   #             U+0000 to U+007F - these map directly onto ASCII characters
   #             and we don't count these as Unicode characters - you can
   #             treat this as an ordinary ASCII character.
   #  110xxxxx - this will be followed by one continuation byte, and the two
   #             specify a Unicode character in the range U+0080 to U+07FF.
   #             Note that the 5 xxxxxx bits in the first byte and the six
   #             xxxxxx bits in the continuation byte provide 11 bits, which
   #             is enough to hold numbers in the hex range 0080 to 07FF.
   #  1110xxxx - will be followed by two continuation bytes, and the three
   #             specify a Unicode character in the range U+0800 to U+FFFF.
   #             Note that the first byte supplies four xxxx bits, each of the
   #             continuation bytes supplies six xxxxxx bits, making a total
   #             of 16 bits, enough to hold numbers up to hex FFFF.
   #  1111xxxx - will be followed by three continuation bytes. You should have
   #             the idea by now. These four bytes specify a Unicode character
   #             in the range U+10000 to U+10FFFF. The four xxxx bits from
   #             the first byte and six xxxxxx bits from the three continuation
   #             bytes make 21 bits, which is enough to hold hex 10FFFF.
   #   So, we almost certainly have an encoded Unicode character if our first
   #   byte fits one of those patterns. If it's the first, then we treat it as
   #   an ordinary ASCII character. If it's one of the other three, then we
   #   see if the proper number of subsequent bytes start with the 10xxxxxx
   #   bit pattern that marks them as continuation bytes. If they do, then
   #   we do the required bit shuffling to get the Unicode value out of the
   #   various xxxx bits.
   
   Char = Line[Index]
   Num = ord(Char)
      
   #  See if this character is in the range of any of those last three
   #  patterns. If so, set ExtraBytes to the number of expected continuation
   #  bytes.
   
   ExtraBytes = 0
   if (Num >= 0xc0 and Num <= 0xdf) : ExtraBytes = 1
   if (Num >= 0xe0 and Num <= 0xef) : ExtraBytes = 2
   if (Num >= 0xF0 and Num <= 0xff) : ExtraBytes = 3
   if (ExtraBytes > 0) :
   
      #  Build up in Bytes a list of the bytes that we expect to form the
      #  encoded Unicode character. As we go, we check that any continuation
      #  bytes match the expected 10xxxxxx pattern - mask off the top two
      #  bits and the result should be 0x80. If this isn't true for any
      #  continuation byte, this isn't a Unicode character. (There are
      #  theoretical cases where a pattern of ordinary extended ASCII
      #  characters could mimic an encoded Unicode character, but they're
      #  extremely contrived and highly unlikely in practice.)
      
      Bytes = [Num]
      LastIndex = Index + ExtraBytes
      if (LastIndex < Length) :
         IsUnicode = True
         for I in range(ExtraBytes) :
            Extra = Line[Index + I + 1]
            NumExtra = ord(Extra)
            if ((NumExtra & 0xc0) != 0x80) :
               IsUnicode = False
               break
            Bytes.append(NumExtra)
   
      #  If it still looks like an encoded Unicode character, then we do the
      #  bit twiddling needed to get the bits - those xxxxx bits - out of the
      #  bytes that we now have in Bytes. Character values up to U+FFFF can
      #  be held in two bytes (UByte0 and UByte1 here). Larger values - the
      #  ones that needed three continuation bytes - will fit into three
      #  bytes. This code pulls those two or three bytes of the final value
      #  out of the encoded bytes, then combines them to get the final
      #  Unicode value. (It could be done more directly, but the shifts
      #  needed would be even harder to follow.) I believe I have these
      #  right - at the time of writing I don't have any test files with
      #  characters that need three continuation bytes.
      
      if (IsUnicode) :
         if (ExtraBytes == 1) :
            UByte0 = ((Bytes[0] & 0x1c) >> 2)
            UByte1 = ((Bytes[0] & 0x03) << 6) | (Bytes[1] & 0x3f)
            Unicode = (UByte0 << 8) | UByte1
         elif (ExtraBytes == 2) :
            UByte0 = ((Bytes[0] & 0x0f) << 4) | ((Bytes[1] & 0x3c) >> 2)
            UByte1 = ((Bytes[1] & 0x03) << 6) | (Bytes[2] & 0x3f)
            Unicode = (UByte0 << 8) | UByte1
         elif (ExtraBytes == 3) :
            UByte0 = ((Bytes[0] & 0x07) << 2) | ((Bytes[1] & 0x30) >> 4)
            UByte1 = ((Bytes[1] & 0x0f) << 4) | ((Bytes[2] & 0x3c) >> 2)
            UByte2 = ((Bytes[2] & 0x03) >> 6) | (Bytes[3] & 0x3f)
            Unicode = (UByte0 << 16) | (UByte1 << 8) | UByte2
         NewIndex = Index + ExtraBytes

   return (IsUnicode, Unicode, NewIndex)

# ------------------------------------------------------------------------------

#                         G e t  F i l e  E n c o d i n g
#
#   ADASS papers are usually supplied in simple ASCII, using standard LaTeX
#   sequences to get special characters such as accented letters or dashes
#   of different lengths. However, some files turn up that have clearly been
#   prepared using editors that insert extended character encodings for such
#   characters. This makes sense for anyone writing in a language that makes
#   use of such characters - many authors have names that need accents.
#   However, not all LaTeX versions are able to handle such characters, and
#   we may need to replace such characters with the standard sequences. The
#   problem is that a number of incompatible extended character sets have been
#   developed over the years, and it is not always obvious just what encoding
#   has been used. This routine is passed the name of a file and attempts to
#   determine which of a number of possible encodings it uses. It should also
#   be passed a list (usually empty) to which this routine appends strings
#   describing what it found in the file.
#
#   This routine should be able to pick the following:
#   o A file using standard ASCII - the lowest common denominator.
#   o A file using ASCII with the extended LATIN-1 set of characters.
#   o A file using the old Mac OS Roman encoding.
#   o A file with Unicode characters encoded using UTF-8.
#
#   There are a number of other possible encodings, but these cover those
#   seen for recent ADASS papers.
#
#   The Result argument should be an empty list. This routine returns this as
#   a list of strings, giving the encodings that the file might have. (Usually,
#   we'd hope there's only be one item in the list, but there are ambiguous
#   cases. In those cases, it's probaby worth outputting the full report.) The
#   possible options returned are:
#
#   "ASCII"     File contains nothing but standard ASCII characters.
#   "UTF-8"     File contains Unicode characters encoded using UTF-8.
#   "MacRoman"  File contains characters encoded in Mac OS Roman.
#   "Latin1"    File contains characters using the LATIN-1 extension.
#
#   If there is a problem opening the file, the list returned will be empty.
#
#   The function value returned by this routine is a measure of the certainty
#   of its returned results, essentially a percentage certainly. If this is
#   100, then the resut is perfectly clear. Any lesser value indicates that
#   there is some uncertainty, best handled by the calling routine displaying
#   the full Report that this routine also returns.

def GetFileEncoding (TexFileName,Result,Report) :

   Certainty = 100
   
   if (not os.path.exists(TexFileName)) :
      Report.append("The file " + TexFileName + " does not exist")
      Certainty = 0
   
   else :
      HasUnicode = False       # File does contain Unicode characters
      AllAscii = True          # All chars so fat are standard ASCII
      HasMacRoman = False      # File has chars that could be Mac Roman
      HasLatin1 = False        # File has chars that could be Latin1
      HasAmbiguous = False     # File has chars that could be Mac or Latin1
      HasUnknown = False       # File has chars that can't be classified
      HasUFFFD = False         # File has the Unicode replacement character
      
      LineNumber = 0
      TexFile = open(TexFileName,"r")
      for Line in TexFile :
         LineNumber = LineNumber + 1
         Index = 0
         LineLength = len(Line)
         while (Index < LineLength) :

            IsUnicode = False       # Almost certainly Unicode
            IsLatin1 = False        # Probably Latin1
            IsMacRoman = False      # Probably Mac Roman
            IsAscii = False         # Definitely standard ASCII
            IsUnknown = False       # Not Unicode, not a usual Latin or Mac char
            IsAmbiguous = False     # Not Unicode, known in both Latin & Mac
            
            Char = Line[Index]
            CharNum = ord(Char)
            
            #  First, an easy test. Any character in the range 0..7F is an
            #  ordinary ASCII character.
            
            if (CharNum <= 0x7f) :
               IsAscii = True
            else :
            
               #  A character greater than 7F might be a Latin-1 character,
               #  a Mac OS Roman character (and these can be hard to tell apart)
               #  or it might be the start of a UTF-8 Unicode multi-byte
               #  character. Such Unicode characters have a distinctive
               #  signature, that CheckForUTF8Unicode() will spot pretty
               #  unambiguously, so we check that next. If this is such a
               #  character, we increment Index to skip over the rest of the
               #  bytes that make up the multi-byte character.
               
               (IsUnicode, Unicode, NewIndex) = \
                                 CheckForUTF8Unicode(Line,Index,LineLength)
               if (IsUnicode) :
               
                  #  This is clearly Unicode. See if we can get the LaTeX
                  #  equivalent for the report.
                  
                  Index = NewIndex
                  Message = "Line " + str(LineNumber) + \
                              " : has Unicode char U+" + hex(Unicode)[2:]

                  #  Unicode U+FFFD is the Unicode replacement character. If the
                  #  file has this, then it indicates that it has been read by
                  #  another program and converted into Unicode, but that some
                  #  characters could not be converted - probably becasue the
                  #  program assumed the wrong input format. Some versions of
                  #  TexWorks used to do this to files they read in different
                  #  formats.
                  
                  if (Unicode == 0xfffd) :
                     HasUFFFD = True
                     Message = Message + " (the Unicode replacement character)"
                  else :
                  
                     #  See if we canget the LaTeX equivalent string, and add
                     #  that to the report.
                     
                     Repl = __Unicode_LaTeX_Chars__.get(Unicode)
                     if (Repl == None) :
                        Repl = __Latin1_LaTeX_Chars__.get(Unicode)
                     if (Repl != None) :
                        Message = Message + ' (LaTeX: "' + Repl + '")'
                     else :
                        Message = Message + ' (LaTeX: Unknown)'
                  Report.append(Message)
                  
      
               else :

                  #  It wasn't a Unicode character. What we have now is a
                  #  single character in the range 80..FF. This will usually be
                  #  a LATIN-1 character, but it just might be Mac Roman.

                  Message = "Line " + str(LineNumber) + " : has char " + \
                                                         hex(CharNum)[2:]
                  
                  #  We see if this is a character we know how to convert
                  #  into LaTeX in either of the encodings. (LATIN-1 doesn't use
                  #  the range 80-9F, and we note that.) If we have a LaTeX
                  #  equivalent for this character in either of the encodings,
                  #  that's a pretty good hint as to which encoding is being
                  #  used. However, some characters have encodings in both
                  #  Latin-1 and Mac Roman. We use the LaTeX equivalents in
                  #  the lines we generate for the reports.

                  MacRepl = __Macintosh_LaTeX_Chars__.get(CharNum)
                  if (MacRepl != None) :
                     Message = Message + ' (LaTeX: "' + MacRepl + \
                                                              '" if Mac Roman)'
                  LatinRepl = __Latin1_LaTeX_Chars__.get(CharNum)
                  if (LatinRepl != None) :
                     Message = Message + ' (LaTeX: "' + LatinRepl + \
                                                                 '" if Latin1)'
                  if (CharNum >= 0x80 and CharNum <= 0x9F) :
                     Message = Message + " (not used in Latin-1)"
                  Report.append(Message)
                  if (MacRepl == None and LatinRepl != None) :
                     IsLatin1 = True
                  elif (MacRepl != None and LatinRepl == None) :
                     IsMacRoman = True
                  elif (MacRepl == None and LatinRepl == None) :
                     IsUnknown = True
                  else :
                     IsAmbiguous = True
      

            #  Now we've classified that character, how does that fit with what
            #  we've seen so far?

            if (not IsAscii) : AllAscii = False
            if (IsUnicode) : HasUnicode = True
            if (IsLatin1) : HasLatin1 = True
            if (IsMacRoman) : HasMacRoman = True
            if (IsAmbiguous) : HasAmbiguous = True
            if (IsUnknown) : HasUnknown = True

            Index = Index + 1

      #  And once we've passed through the whole file, let's see what we've
      #  got.

      TexFile.close()

      if (HasAmbiguous) :
      
         #  We had ambiguous characters. If we had any that were not ambiguous,
         #  that pretty much tells us that the ambiguous characters must be
         #  the same, and that ties down the encoing and we can drop the
         #  'ambiguous' flag.
   
         if (HasMacRoman and not HasLatin1) :
            HasAmbiguous = False
            Report.append( \
             "Assuming Mac Roman encoding, as not all characters are ambiguous")
            Certainty = 80
         if (HasLatin1 and not HasMacRoman) :
            HasAmbiguous = False
            Report.append( \
                "Assuming Latin1 encoding, as not all characters are ambiguous")
            Certainty = 80
               
      #  Finally, we set up the Result list, which we hope will only have
      #  one entry, and add some final explantations to the Report. FIrst,
      #  if everything was ASCII, that's easy.
      
      if (AllAscii) :
         Result.append("ASCII")
         Report.append( \
                  "Assuming ASCII encoding - all characters are standard ASCII")
      else :
      
         #  Otherwise, there were encoded characters. Put all the possible
         #  encodings we found into the result list that we return.
         
         if (HasUnicode) : Result.append("UTF-8")
         if (HasMacRoman or HasAmbiguous) : Result.append("MacRoman")
         if (HasLatin1 or HasAmbiguous) : Result.append("Latin1")
         
         #  And now see if we can explain our final conclusions.
         
         if (len(Result) > 1) :
            Report.append("File seems to have a mixture of possible encodings")
            Certainty = 50
         else :
         
            #  This is the happy case were, although there were non-standard
            #  ASCII characters found, they were unambiguously encoded all
            #  using the same encoding - as far as we can tell! But note the
            #  proviso if the U_FFFD replacement character was spotted.
            
            if (HasUnicode) :
               Report.append("File uses Unicode characters encoded using UTF-8")
               if (HasUFFFD) :
                  Certainty = 90
                  Report.append("But appears to to be the result of a " + \
                                                   "mis-conversion into UTF-8.")
                  Report.append("An earlier program may have mis-identified" + \
                                                      " the original encoding.")
                  Report.append("Unfortunately, the original character value" \
                                                      + " cannot be recovered.")
            if (HasLatin1) :
               Report.append("File uses ASCII with LATIN-1 extended characters")
            if (HasMacRoman) :
               Report.append("File uses ASCII with Mac OS Roman characters")

   return Certainty

# ------------------------------------------------------------------------------

#                         C h e c k  C h a r a c t e r s
#
#   This is a version of FixCharacters() that only checks to see there are
#   any potential unprintable-character problems in the line it is passed.
#   It returns True if there were such characters, False otherwise. If there
#   is a known-fix for the problem character, it notes it. The final optional
#   Problems argument allows this to be used in batch mode, where direct output
#   from this routine is suppressed and instead a set of report lines are added
#   to the list of problems passed.
#

def CheckCharacters (Line,LineNumber,Problems = None,Encoding = "Latin1") :

   BatchMode = False
   if (Problems != None) : BatchMode = True
   LowEncoding = Encoding.lower()
   UseLatin1 = (LowEncoding == "latin1")
   UseMacRoman = (LowEncoding == "macroman")
   UseUnicode = (LowEncoding == "utf-8")
   UseAscii = (LowEncoding == "ascii")
   
   Problem = False
   NChars = len(Line)
   Index = 0;
   while (Index < NChars) :
   
      Char = Line[Index]
      if (not Char in string.printable) :
         Problem = True
         Num = ord(Char)
         Repl = None
         Descrip = None
         if (UseAscii) :
            Descrip = "ASCII character (" + hex(Num) + ")"
         elif (UseLatin1) :
            Repl = __Latin1_LaTeX_Chars__.get(Num)
            Descrip = "Latin1 character (" + hex(Num) + ")"
         elif (UseMacRoman) :
            Repl = __Macintosh_LaTeX_Chars__.get(Num)
            Descrip = "Mac Roman character (" + hex(Num) + ")"
         elif (UseUnicode) :
            (IsUnicode, Unicode, NewIndex) = \
                                     CheckForUTF8Unicode(Line,Index,NChars)
            Index = NewIndex
            if (IsUnicode) :
               Descrip = "Unicode character U+" + hex(Unicode)[2:]
               Repl = __Unicode_LaTeX_Chars__.get(Unicode)
               if (Repl == None) :
                  Repl = __Latin1_LaTeX_Chars__.get(Unicode)
            else :
               Descrip = "Unexpected character (" + hex(Num) + \
                                              ") - not valid UTF-8 Unicode)"
         if (Descrip == None) :
            Descrip = "Unexpected character (" + hex(Num) + \
                            ") in unexpected encoding (" + Encoding + ")"
         if (Repl == None) :
            Text = Descrip + " in .tex file at line " + str(LineNumber) + \
                                               " : LaTeX equivalent unknown"
         else :
            Text = Descrip + " in .tex file at line " + str(LineNumber) + \
                                             " should be replaced by " + Repl
         if (BatchMode) : Problems.append(Text)
         else : print(Text)
      Index = Index + 1
   
   return Problem 
 
# ------------------------------------------------------------------------------

#                         A u t h o r  C h a r s
#
#   AuthorChars() is passed an author name replete with LaTeX formatting,
#   generally for accented characters. It returns a simplified version of
#   the name, with any of the common accenting syntaxes replaced by, in most
#   cases, just the unaccented character. The exception is the unlaut, where
#   it appends an extra 'e', following the usual convention for writing 
#   German words where the umlaut is too awkward. The author name is also
#   truncated at a comma, so "Surname, I." is truncated to "Surname".
#
#   The idea here is to generate a name that would match that used for the
#   directory name used for a paper by this author, so that this can be
#   checked.
#
#   LaTeX uses a number of special constructs of the form \<char>{<letter>}
#   which modify a single letter to produce an accented character. For example,
#   \c{c} which generates a c-cedilla, or \"{u} which generates a 'u' with an
#   umlaut. LaTeX also accepts the simplified form \<char><letter> in most
#   cases. This code handles \` \' \^ \~ \" \. \c \o \v \H \k \= \b \d \r \u
#   There are probably some other obscure cases out there, but that's a 
#   good start.

def AuthorChars (Author) :

   #  Truncate at a comma - assuming this clips off any trailing initials.
   
   Index = Author.find(',')
   if (Index >= 0) : Author = Author[:Index]
   
   #  If there are no LaTeX directives at all, that's all we have to do.
   
   if (Author.find('\\') >= 0):
   
      #  Work through all the possible values for <char> in \<char>
       
      for Char in "`'^~\".covHk=bdru" :
      
         #  For each character, we try twice, once for the case where the
         #  accented letter is in {braces} and then once where it isn't.
         #  Offset is the number of characters after the '\' where we find
         #  the accented letter itself.
         
         for Try in [1,2] :
            if (Try == 1) :
               Directive = '\\' + Char + '{'
               Offset = 3
            else :
               Directive = '\\' + Char
               Offset = 2
               
            #  We keep going until we've removed each instance of the
            #  directive we're looking for,
            
            while (True) :
               Index = Author.find(Directive)
               if (Index < 0) : break
               
               #  Normally, we just replace the accenting directive with
               #  the single letter. For an umlaut, we append an 'e'
               
               Letter = Author[Index + Offset]
               FullString = Directive + Letter
               if (Try == 1) : FullString = FullString + '}'
               if (Char == '"') : Letter = Letter + 'e'
               Author = Author.replace(FullString,Letter)
               
         #  And we quit once there are no LaTeX directives left.
         
         if (Author.find('\\') < 0): break
         
   return Author

# ------------------------------------------------------------------------------

#                          R u n  C o m m a n d
#
#  RunCommand() is a utility that runs a single command, waiting for it
#  to cpmplete. It ignores any output from the command, but returns an
#  error string if the command terminates with bad status. Command should
#  be a single string or a list of strings, but if it is a single string
#  it will be split (using spaces as delimiters) into a list, rather than
#  being passed to a shell to interpret.
#
#  This is packaged as a separate routine because it's actually tricky to
#  get right, particularly using the subprocess module. (The recent routine
#  subprocess.call() does most of this, but only dates from Python 3.5. Also
#  note that a lot of the things this might be used for, like extracting
#  archives using tar, can be done using ordinary python modules.)

def RunCommand (Command) :

   Status = None
   
   #  We don't want to use a shell to interpret the command, since that
   #  has security implications (if Command is built up using outside input
   #  nasty stuff can be embedded in it), so we need to pass Popen() an
   #  argument list rather than a command. (Note: in Python 2 the test
   #  should really be for basestring rather than str, as this misses
   #  unicode strings, but basestring isn't defined in Python 3).
   
   if (isinstance(Command,str)) : CommandList = Command.split()
   else : CommandList = Command
   
   #  Setting up stdout and stderr like this allows the output from the
   #  subprocess to be absorbed. (You may not want to do this, in which
   #  case you don't want this routine. It took a bit of experimenting
   #  to get this sequence right - if I left stderr as None, unzip would
   #  output the list of files, for example.)
   
   Proc = subprocess.Popen(CommandList,stdout=subprocess.PIPE, \
                                                stderr=subprocess.STDOUT)
   Output = Proc.communicate()
   Proc.stdout.close()
   Result = Proc.wait()
   if (Result != 0) :
      Status = "Error executing '" + Command + "'"

   return Status

# ------------------------------------------------------------------------------

#                       E x t r a c t  A r c h i v e
#
#  ExtractArchive() is passed the name of an archive file - either a tar or
#  a zip file - and extracts it into the current directory. If there are any
#  problems, it returns a string describing the error. Normally, it returns
#  None.

def ExtractArchive (Filename) :

   Status = None
   if (Filename.endswith(".tar") or Filename.endswith(".tar.gz") or \
           Filename.endswith(".zip") or Filename.endswith(".tgz")) :
      
      #  We're going to use a subprocess command to execute the extraction
      #  command, so we need to handle any blanks or quote characters in the
      #  filename. (Actually, this should use the Python archive modules.)
      
      AbsFilename = os.path.abspath(Filename)
      AbsFilename = AbsFilename.replace("'","\\'")
      AbsFilename = AbsFilename.replace(" ","\\ ")
      
      if (AbsFilename.endswith(".zip")) :
         Command = "unzip " + AbsFilename
      else :
         Command = "tar -xf " + AbsFilename
      Result = RunCommand(Command)
      if (Result) : Status = Result
   else :
      Status = "Type of archive file " + Filename + " is unclear"

   return Status


# ------------------------------------------------------------------------------

#                         G e t  A r c h i v e  T i m e
#
#   GetArchiveTime() returns the latest modification date (as a time in seconds
#   since the epoch) of any file contained in the named archive file, which
#   can be a .tar, .tar.gz or a .zip file.  If it cannot determine the date
#   it returns None. Optionally, it can also be passed a list to which will
#   be added the names of all the files in the archive.

def GetArchiveTime (Filename,FileList = None) :

   LatestTime = None
   if (Filename.endswith(".tar") or Filename.endswith(".tar.gz") or \
           Filename.endswith(".zip") or Filename.endswith(".tgz")) :
      
      #  Remember the current directory and the absolute path of the file
      #  we've been passed (which may have been a relative name)
         
      OriginalDir = os.getcwd()
      AbsFilename = os.path.abspath(Filename)
      AbsFilename = AbsFilename.replace("'","\\'")
      AbsFilename = AbsFilename.replace(" ","\\ ")
      
      #  Create a temporary directory for the files in the archive, move
      #  to it and copy the archive files into it. (This is slower but more
      #  reliable than trying to interpret the output from commands like
      #  "tar -tvf") (This code should now use the newer ExtractArchive()
      #  routine.)
      
      TempDir = tempfile.mkdtemp()
      os.chdir(TempDir)
      if (AbsFilename.endswith(".zip")) :
         Proc = os.popen("unzip " + AbsFilename)
      else :   
         Proc = os.popen("tar -xf " + AbsFilename)
      Proc.close()
      
      #  Now we'll go through all the files looking at the dates. One
      #  complication - the top level of the archive may be a single
      #  directory which itself holds the files. If so, we dive into that
      #  intermediate directory. (It would probably be better to do a 
      #  recursive search through the whole of the directory.) Also ignore
      #  the __MACOSX files that sometimes end up in OS X archives.
      
      FilesInDir = os.listdir(".")
      FileCount = 0
      IntermediateDir = ""
      LastFile = ""
      for File in FilesInDir :
         if (not File.startswith('.') and File != "__MACOSX") :
            LastFile = File
            FileCount = FileCount + 1
      if (FileCount == 1) :
         IntermediateDir = os.path.abspath(LastFile)
         if (os.path.isdir(IntermediateDir)) :
            os.chdir(IntermediateDir)
            FilesInDir = os.listdir(".") 
            
      #  Now look at the modification dates of all the files. (The test for
      #  exists() is because a file may be a link to a file that does not
      #  exist on this system.) And directories will have the current date,
      #  and we don't expect them anyway.
              
      First = True
      for File in FilesInDir :
         if (os.path.exists(File)) :
            if (not os.path.isdir(File)) :
               FileTime = os.stat(File).st_mtime
               if (First) :
                  LatestTime = FileTime
                  First = False
               else :
                  if (FileTime > LatestTime) : LatestTime = FileTime
               
      #  If the caller passed us a file list, add the file names to it.
      
      if (FileList != None) :
         FileList.extend(FilesInDir)
         
      #  Cleaup up after outselves, and return to the directory we started from.
      
      if (TempDir != "") :
         Proc = os.popen("rm -rf " + TempDir)
         Proc.close()
      os.chdir(OriginalDir)
   return LatestTime
   
# ------------------------------------------------------------------------------

#                      G e t  A r c h i v e  L i s t
#
#   GetArchiveList() walks through every file in the tree whose root is 
#   the directory passed as Path. It looks for any file that might be an 
#   archive file for the paper whose name is passed as Paper. That is, any
#   .tar, .tar.gz or .zip file whose name contains the paper name in some
#   way. It returns a list of the paths of each candidate file, relative to
#   the current directory.

def GetArchiveList (Path,Paper) :

   #  ArchiveWalkCallback() is a nested callback routine that does most of 
   #  the work. It's nested because that's the easiest way for it to get
   #  access to Paper. It gets called for each directory in Path with DirPath
   #  as the directory path and FileList a list of files in the directory. It
   #  adds any candidate files to the list passed as ArchivePath. (This
   #  structure dates back to Python2 days, when this actually was a routine
   #  called back from os.path.walk(). Now we use os.walk() instead, and the
   #  structure could be rather simpler.)
    
   def ArchiveWalkCallback(ArchiveList,DirPath,FileList) :
      for File in FileList :
         if (File.endswith(".tar") or File.endswith(".tar.gz") \
                                               or File.endswith(".zip")) :
            Match = False
            Filelower = File.lower()
            Paperlower = Paper.lower()
            
            #  The basic test is to see if the paper name appears in the file
            #  name - as a case-insensitive test.
            
            if (Filelower.find(Paperlower) >= 0) :
               Match = True
            else :
            
               #  Some people call their files O1.4 instead of O1_4, so we
               #  check for that.
               
               if (Filelower.find(Paperlower.replace('-','.')) >= 0) :
                  Match = True
               else :
               
                  #  And some people miss leading zeros from paper numbers,
                  #  using P71 instead of P071.
                  
                  if (Paperlower.startswith("p00")) :
                     if (Filelower.find(Paperlower.replace('p00','p')) >= 0) :
                        Match = True
                  elif (Paperlower.startswith("p0")) :
                     if (Filelower.find(Paperlower.replace('p0','p')) >= 0) :
                        Match = True
            if (Match) :
               FilePath = os.path.join(DirPath,File)
               ArchiveList.append(FilePath)
   
   #  This is the main body of GetArchiveList(). Walk through the supplied
   #  directory structure, calling ArchiveWalkCallback() for each directory 
   #  it contains. This used to use os.path.walk, but this was removed from
   #  Python 3.
              
   ArchiveList = []
   os.path.walk(Path,ArchiveWalkCallback,ArchiveList)
   for Details in os.walk(Path) :
      ArchiveWalkCallback(ArchiveList,Details[0],Details[2])
   
   return ArchiveList

# ------------------------------------------------------------------------------

#                         C o l l a p s e  D i r
#
#  Often, an archive will turn out not to have all the files for a paper
#  at the top level, but instead will have a single directory at top level
#  which then contains the files for the paper. This is actually a sensible
#  thing for the author to do, but it isn't quite what we're looking for,
#  This routine looks to see if the current directory effectively contains
#  only a single directory, and if so it moves the contents of that directory
#  up to the top level and removes the directory, so producing the layout
#  we expect. If the current directory effectively contains more than one file,
#  this routine does nothing. (Note the word 'effectively' here - we don't
#  count hidden files - ones beginning with '.', nor do we count the
#  __MACOSX file that OS X systems often include in tar archives for their own
#  purposes.)
#
#  This routine can also handle another case that has been seen occasionally.
#  Sometimes, the archive file turns out to contain just one file, and
#  that file is itself an archive file. In that case, this routine extracts
#  the files from that archive, removes the archive, and then checks for
#  a single directory at top level.
#
#  If DirList or ArchiveList are supplied, this routine adds the name of
#  any removed intermediate directory or archive file to the appropriate
#  list.

def CollapseDir (DirList = None, ArchiveList = None) :

   FilesInDir = os.listdir(".")
   FileCount = 0
   LastFile = ""
   
   #  See how many files we have (effectively - see header comments)
   
   for File in FilesInDir :
      if (not File.startswith('.') and File != "__MACOSX") :
         LastFile = File
         FileCount += 1

   #  If we only have one file, and it is itself an archive file, expand
   #  it into the current directory first, then call this routine again
   #  recursively.

   if (FileCount == 1) :
      Filename = LastFile
      if (Filename.endswith(".tar") or Filename.endswith(".tar.gz") or \
                 Filename.endswith(".zip") or Filename.endswith(".tgz")) :
         Status = ExtractArchive(Filename)
         if (Status == None) :
            os.remove(Filename)
            if (ArchiveList != None) : ArchiveList.append(Filename)
            CollapseDir (DirList,ArchiveList)

   #  If we only have one file, and it is a directory, move its contents
   #  up to the current directory and remove that now empty directory.
   
   if (FileCount == 1) :
      IntermediateDir = os.path.abspath(LastFile)
      if (os.path.isdir(IntermediateDir)) :
         os.chdir(IntermediateDir)
         Proc = os.popen("mv *.* ..")
         Proc.close()
         os.chdir("..")
         shutil.rmtree(IntermediateDir,ignore_errors = True)
         if (DirList != None) : DirList.append(LastFile)

# ------------------------------------------------------------------------------

#                       L o c a t e  T e x  F i l e
#
#  LocateTexFile() searches the current directory, assuming it contains the
#  files for an ADASS paper, looking for the main .tex file for the paper.
#  Ideally, we will know the PaperID for the paper in question, and can pass
#  this to this routine, in which case the file should be PaperID.tex, eg
#  O10-3.tex. If this file is found as expected, this routine returns its
#  name. Authors are occasionally careless with their naming of files, or we
#  may not know the PaperID (in which case it should be passed as None, which
#  is the default). In this case, this routine attempts to do its best with
#  what it has, which is just the file list. If there is only one .tex file,
#  it will return that, for example. To allow for the possibility that more
#  than one plausible candidate is found, this routine returns a list of
#  files, although usually this will have only a single entry - or none, if
#  no file can be found. If the caller wants to limit the returned list to
#  just one file, passing the optional Single parameter as True will force
#  this routine to return just the most recently modified of the files that
#  would otherwise have been returned.

def LocateTexFile (PaperID = None, Details = None, Single = False) :

   Files = []
   Found = False
   Report = (Details != None)
   
   #  First, if we have a PaperID, see if we have the file we expect.
   
   if (PaperID) :
      TexFileName = PaperID + ".tex"
      if (os.path.exists(TexFileName)) :
         Files.append(TexFileName)
         Found = True
         if (Report) : Details.append("Found " + TexFileName + " as expected")
      else :
         if (Report) :
            Details.append("Expected file " + TexFileName + " not found")
   if (not Found) :
   
      #  Not that easy. We need to look at the files we have. See how
      #  many .tex files we have.
      
      FilesInDir = os.listdir(".")
      TexFiles = 0
      for File in FilesInDir :
         if (File.endswith(".tex") and not File.startswith('.')) :
            TexFiles += 1
            LastTexFile = File

      if (TexFiles == 0) :
      
         #  No .tex files at all. That's all we can do.
         
         if (Report) : Details.append("No .tex files found in directory")

      elif (TexFiles == 1) :
      
         #  Just one .tex file. We'll settle for that.
         
         if (Report) :
            Details.append("Only one .tex file (" + LastTexFile + \
                                                ") found in directory")
         Files.append(LastTexFile)
      else :

         #  Multiple .tex files. This gets tricky. See if any of them look
         #  anything like a properly named ADASS .tex file.

         #  First, try for any .tex file that has the paperID in its name
         
         if (PaperID) :
            for File in FilesInDir :
               if (File.endswith(".tex") and not File.startswith('.')) :
                  LFile = File.lower()
                  if (LFile.find(PaperID.lower()) >= 0) :
                     Files.append(File)
                     if (Report) :
                        Details.append(File + " contains " + PaperID)
                     Found = True
         
         if (not Found) :

            #  Failing that, any file that seems to have a properly named
            #  .tex file.
            
            for File in FilesInDir :
               if (File.endswith(".tex") and not File.startswith('.')) :
                  Paper = File[:-4]
                  Problems = []
                  if (CheckPaperName(Paper,Problems)) :
                     Files.append(File)
                     if (Report) :
                        Details.append(File + " is a properly named .tex file")
                     Found = True

         if (Found) :
            if (Report) : Details.append("Found " + str(len(Files)) + \
                                          " plausibly named .tex file(s)")
         else :
         
            #  There weren't any plausibly named files. All we can do is
            #  include any .tex file we find.
            
            for File in FilesInDir :
               if (File.endswith(".tex") and not File.startswith('.')) :
                  Files.append(File)
                  if (Report) :
                     Details.append("Found .tex file " + File)
            if (Report) : Details.append("Found " + str(len(Files)) + \
                                                  " .tex files")
               
   #  If we end up with multiple .tex files, there is one more thing we can
   #  do. We can see if any of them have an author list and a title. If only
   #  one does, we can be reasonably sure it's what we're looking for. Even
   #  if more than one does, this might remove some spurious files.
   
   if (len(Files) > 1) :
      PaperFiles = []
      for File in Files :
         Ignore = []
         Authors = GetAuthors(None,Ignore,File)
         if (len(Authors) > 0) :
            Surname = AuthorSurname(Authors[0])
            Title = GetTitle(None,Ignore,File)
            if (Title != "") :
               if (Report) :
                  Details.append("File " + File + " appears to be a paper by " \
                                                                     + Surname)
               PaperFiles.append(File)
      if (len(PaperFiles) > 0) : Files = PaperFiles

   #  Finally, if the Single parameter has been set to force us to return only
   #  a single file, we can check the modification times of the files and
   #  return just the most recently modified file.
   
   if (len(Files) > 1 and Single) :
      TexFileName = Files[0]
      LatestTexTime = os.stat(TexFileName).st_mtime
      for File in Files[1:] :
         FileTime = os.stat(File).st_mtime
         if (FileTime > LatestTexTime) :
            TexFileName = File
            LatestTexTime = FileTime
      Details.append("Using last modified .tex file: " + TexFileName)
      Files = [TexFileName]

   return Files


# ------------------------------------------------------------------------------

#                   P a c k a g e  S c a n  C a l l b a c k
#
#   Used as the callback routine for the TexScanner when it is used to scan
#   the .tex file for any packages used. Words are the components of a LaTeX
#   directive parsed by the TexScanner. If this is a "\usepackage" directive,
#   this parses the arguments to that directive and checks to see if any of
#   these are non-standard packages. StandardList is a list of any standard
#   packages found, to which this routine appends. Similarly, NonStandard is
#   a list of any non-standard packages found. In fact, no .tex file should
#   need any \usepackage directives, other than \usepackage{asp2014} as that
#   the standard package itself includes all the standard packages.

__StandardPackages__ = \
   {"array","txfonts","ifthen","lscape","index","graphicx","asmsymb", \
    "wrapfig","chapterbib","url","ncccropmark","watermark"}

def PackageScanCallback(Words,StandardList,NonStandard) :

   NumberWords = len(Words)
   if (NumberWords > 1) :
      if (Words[0] == "\\usepackage") :
         for Word in Words[1:NumberWords] :
            if (Word.startswith('{')) :
               Packages = Word.strip("{}").replace(' ','').split(',')
               Len = len(Packages)
               if (Len > 0) :
                  for Package in Packages :
                     if (Package != "asp2014" and Package != "./asp2014") :
                        Standard = False
                        for StandardPkg in __StandardPackages__ :
                           if (Package == StandardPkg) :
                              Standard = True
                        if (Standard) :
                           StandardList.append(Package)
                        else :
                           NonStandard.append(Package)

# ------------------------------------------------------------------------------

#                        C h e c k   P a c k a g e s
#
#   This routine looks in the current directory for a file called 
#   Paper.tex (where Paper will be a string such as "O1-4"), assuming
#   this is the main .tex file for the paper. It looks for any LaTeX packages
#   used by this .tex file. It lists all the packages found, noting the use
#   of standard packages (which is OK, but unnecessary), and warning about
#   the use of any non-standard packages.
# 
#   To allow this to be used for preliminary checking, where the main .tex
#   file has been misnamed, the actual .tex file name can be supplied as
#   an optional argument. The final optional Problems argument allows this to
#   be used in batch mode, where direct output from this routine is suppressed
#   and instead a set of report lines are added to the list of problems passed.
#
#   This routine returns True if everything looks OK, False otherwise.


def CheckPackages (Paper,TexFileName = "",Problems = None) :
   
   ReturnOK = True
   
   BatchMode = False
   if (Problems != None) : BatchMode = True
   
   if (TexFileName == "") : TexFileName = Paper + ".tex"
   TexFileName = os.path.abspath(TexFileName)
   if (not os.path.exists(TexFileName)) :
      Problem = "Cannot find main .tex file: " + TexFileName
      if (BatchMode) : Problems.append(Problem)
      else : print(Problem)
      ReturnOK = False
   else :

      #  Now get a list of the packages from the .tex file.

      TexFile = open(TexFileName,mode='r')
      TheScanner = TexScanner.TexScanner()
      TheScanner.SetFile(TexFile)
      
      #  GetNextTexCommand() will call PackageScanCallback for each command it
      #  finds in the file, and PackageScanCallback will check the command
      #  and add any packages to one of the two lists.
      
      Finished = False
      StandardList = []
      NonStandard = []
      while (not Finished) :
         Finished =  TheScanner.GetNextTexCommand(PackageScanCallback,\
                                                   StandardList,NonStandard)
                                                         
      TexFile.close()
      
      if (len(StandardList) > 0) :
         if (not BatchMode) :
            print("")
            print("Note:",TexFileName,\
                                 "includes the following standard package(s):")
            for Package in StandardList :
               print("   ",Package)
            print("this is OK, but unnecessary.")
      if (len(NonStandard) > 0) :
         if (not BatchMode) : print("")
         Problem = TexFileName + \
                         " includes the following non-standard package(s):"
         if (BatchMode) : Problems.append(Problem)
         else : print("**",Problem)
         Packages = ""
         for Package in NonStandard :
            Packages = Packages + Package + " "
         if (BatchMode) : Problems.append(Packages)
         else : print(Packages)
         Problem = "this may be a problem"
         if (BatchMode) : Problems.append(Problem)
         else : print(Problem,"**")
         ReturnOK = False

   return ReturnOK

# ------------------------------------------------------------------------------

#                   R u n n i n g  H e a d s  C a l l b a c k
#
#   Used as the callback routine for the TexScanner when it is used to scan
#   the .tex file for the \markboth directive used to generate the running
#   heads for the paper. Words are the components of a LaTeX directive parsed
#   by the TexScanner. If this is a "\markboth" directive, this parses the 
#   arguments to that directive and checks them for the sort of problems that
#   have occasionally shown up in ADASS papers. Notes should be a list of 
#   strings, initially set empty. Each time the callback encounters a
#   \markboth directive it appends to Notes two strings giving the author
#   list and the paper title. It then adds strings describing any problems
#   it has found. Since any paper should only include one \markboth directive,
#   after the paper has been scanned, Notes should contain exactly two strings. 
#   If Notes is empty, no \markboth has been found, If it contains more than
#   two strings, some problem has been found.

def RunningHeadsCallback(Words,Notes,Unused) :

   NumberWords = len(Words)
   if (NumberWords > 1) :
      if (Words[0] == "\\markboth") :
         if (len(Notes) > 0) :
            Problem = "Paper contains multiple \\markboth directives"
         if (NumberWords != 3) :
            Problem = "\\markboth directive has wrong number of arguments"
            Problems.append(Problem)
         else :
            Authors = Words[1].strip('{}')
            Title = Words[2].strip('{}')
            Note = "Author list for running header is '" + Authors + "'"
            Notes.append(Note)
            Note = "Paper title for running header is '" + Title + "'"
            Notes.append(Note)
            if (Authors == "Author1, Author2, and Author3") :
               Problem = "Author list is unchanged from the template"
               Notes.append(Problem)
            if (Authors.strip() == "") :
               Problem = "Author list is blank"
               Notes.append(Problem)
            if (Title == "Author's Final Checklist") :
               Problem = "Paper title is unchanged from an out-of-date template"
               Notes.append(Problem)
            if (Title == "Short Title") :
               Problem = "Paper title is unchanged from the template"
               Notes.append(Problem)
            if (Title.strip() == "") :
               Problem = "Paper title is blank"
               Notes.append(Problem)
            if (Authors == Title) :
               Problem = "Paper title is the same as the author list"
               Notes.append(Problem)
               
# ------------------------------------------------------------------------------

#                   C h e c k   R u n n i n g  H e a d s
#
#   This routine looks in the current directory for a file called 
#   Paper.tex (where Paper will be a string such as "O1-4"), assuming
#   this is the main .tex file for the paper. It looks for any \markboth
#   directive that specifies the running heads for the paper (author and
#   title), and checks for any problems with them. (A surprising number of
#   ADASS papers leave the \markboth directive unchanged from the template, or
#   manage to get it wrong in other ways. This routine spots some of the
#   issues that have been seen. The final optional Problems argument allows
#   this to be used in batch mode, where direct output from this routine is
#   suppressed and instead a set of report lines are added to the list of
#   problems passed.
# 
#   To allow this to be used for preliminary checking, where the main .tex
#   file has been misnamed, the actual .tex file name can be supplied as
#   an optional argument.
#
#   This routine returns True if everything looks OK, False otherwise.


def CheckRunningHeads (Paper,TexFileName = "",Problems = None) :
   
   ReturnOK = True
   
   BatchMode = False
   if (Problems != None) : BatchMode = True
   
   if (TexFileName == "") : TexFileName = Paper + ".tex"
   TexFileName = os.path.abspath(TexFileName)
   if (not os.path.exists(TexFileName)) :
      Problem = "Cannot find main .tex file: " + TexFileName
      if (BatchMode) : Problems.append(Problem)
      else : print(Problem)
      ReturnOK = False
   else :

      #  Now set up to check the .tex file.

      TexFile = open(TexFileName,mode='r')
      TheScanner = TexScanner.TexScanner()
      TheScanner.SetFile(TexFile)
      
      #  GetNextTexCommand() will call RunningHeadsCallback for each command it
      #  finds in the file, and RunningHeadsCallback will check the command
      #  and will process any \markboth directive it finds.
      
      Finished = False
      Notes = []
      while (not Finished) :
         Finished =  TheScanner.GetNextTexCommand(RunningHeadsCallback,\
                                                               Notes,None)
                                                         
      TexFile.close()
      
      #  See comments for RunningHeadsCallback() for details of how it handles
      #  Notes. Essentially, if all is well, Notes will have two entries,
      #  which will be the author list and the title list.Anything else
      #  will be an error.
      
      if (not BatchMode) : print("")
      if (len(Notes) == 2) :
         if (not BatchMode) :
            print(Notes[0])
            print(Notes[1])
      else :
         ReturnOK = False
         if (len(Notes) == 0) :
            Problem = TexFileName + " has no \\markboth directive"
            if (BatchMode) : Problems.append(Problem)
            else : print("**",Problem,"**")
         else :
            Problem = TexFileName + \
             " has problems with the running heads specified using \\markboth:"
            if (BatchMode) : Problems.append(Problem)
            else : print(Problem)
            for Note in Notes :
               if (BatchMode) : Problems.append(Note)
               else : print("   ",Note)
      if (not BatchMode) : print("")

   return ReturnOK

# ------------------------------------------------------------------------------

#                           T i t l e  C a l l b a c k
#
#   Used as the callback routine for the TexScanner when it is used to scan
#   the .tex file for the \title directive used to supply the title for
#   paper. Words are the components of a LaTeX directive parsed by the
#   TexScanner. If this is a "\title" directive, this parses what should be
#   the single argument to that directive and adds it to the Titles list. Titles
#   should be a list of strings, initially set empty. Since any paper should
#   only include one \title directive, after the paper has been scanned, Titles
#   should just a single title string. If Titles is empty, no \title has been
#   found.

def TitleCallback(Words,Titles,Unused) :

   NumberWords = len(Words)
   if (NumberWords > 1) :
      if (Words[0] == "\\title") :
         Title = Words[1].strip('{}')
         Titles.append(Title)

# ------------------------------------------------------------------------------

#                           G e t   T i t l e
#
#   This routine looks in the current directory for a file called
#   Paper.tex (where Paper will be a string such as "O1-4"), assuming
#   this is the main .tex file for the paper. It looks for the title of
#   the paper and returns it as a string. Notes is a list to which this adds
#   a brief description of anything possibly amiss that it comes across when
#   searching for the title. If it doesn't find a title, for example, it will
#   return an empty string and will say so in Notes. If it finds multiple
#   titles, it will return the first and mention this in notes.

def GetTitle (Paper,Notes,TexFileName = "") :

   Title = ""
   Titles = []
   
   if (TexFileName == "") : TexFileName = Paper + ".tex"
   TexFileName = os.path.abspath(TexFileName)
   if (not os.path.exists(TexFileName)) :
      print("Cannot find main .tex file",TexFileName)
   else :

      #  Now get a list of any title entries from the .tex file.

      TexFile = open(TexFileName,mode='r')
      TheScanner = TexScanner.TexScanner()
      TheScanner.SetFile(TexFile)
      
      #  GetNextTexCommand() will call TitleCallback for each command it
      #  finds in the file, and TitleCallback will check the command
      #  and add any title to Titles.
      
      Finished = False
      while (not Finished) :
         Finished =  TheScanner.GetNextTexCommand(TitleCallback,\
                                                      Titles,None)
      
      TexFile.close()

      NumberTitles = len(Titles)
      if (NumberTitles == 1) :
         Title = Titles[0]
      elif (NumberTitles == 0) :
         Notes.append("No title specified in the .tex file")
      else :
         Notes.append("The .tex file specifies multiple titles:")
         Title = Titles[0]
         for Entry in Titles :
            Notes.append(Entry)

   return Title

# ------------------------------------------------------------------------------

#                          C i t e  C a l l b a c k
#
#   Used as the callback routine for the TexScanner when it is used to scan
#   the .tex file to see if any references use the old \cite directive. For
#   more details, see RefScanCallback(). This routine adds to CiteRefs the
#   names of any references cited using \cite..

def CiteCallback (Words,CiteRefs,Unused) :

   if (len(Words) > 0) :
      if (Words[0] == "\\cite") :
         Refs = ExtractRefs(Words)
         CiteRefs.append(Refs)
            
# ------------------------------------------------------------------------------

#                          C h e c k   C i t e
#
#   This routine looks in the current directory for a file called 
#   Paper.tex (where Paper will be a string such as "O1-4"), assuming
#   this is the main .tex file for the paper. It looks for any \cite
#   directive and warns about its use.
# 
#   To allow this to be used for preliminary checking, where the main .tex
#   file has been misnamed, the actual .tex file name can be supplied as
#   an optional argument. The final optional Problems argument allows this to
#   be used in batch mode, where direct output from this routine is suppressed
#   and instead a set of report lines are added to the list of problems passed.
#
#   This routine returns True if everything looks OK, False otherwise.


def CheckCite (Paper,TexFileName = "",Problems = None) :
   
   BatchMode = False
   if (Problems != None) : BatchMode = True
   
   ReturnOK = True
   
   if (TexFileName == "") : TexFileName = Paper + ".tex"
   TexFileName = os.path.abspath(TexFileName)
   if (not os.path.exists(TexFileName)) :
      Problem = "Cannot find main .tex file: " + TexFileName
      if (BatchMode) : Problems.append(Problem)
      else : print(Problem)
      ReturnOK = False
   else :

      #  Now set up to check the .tex file.

      TexFile = open(TexFileName,mode='r')
      TheScanner = TexScanner.TexScanner()
      TheScanner.SetFile(TexFile)
      
      #  GetNextTexCommand() will call CiteCallback for each command it
      #  finds in the file, and CiteCallback will check the command
      #  and will add any reference cited using \cite to CiteRefs..
      
      Finished = False
      CiteRefs = []
      while (not Finished) :
         Finished =  TheScanner.GetNextTexCommand(CiteCallback,CiteRefs,None)
                                                         
      TexFile.close()
      
      if (len(CiteRefs) > 0) :
         Problem = "The .tex file cites the following references using \cite:"
         if (BatchMode) : Problems.append(Problem)
         else : print("**",Problem,"**")
         Refs = ""
         for Ref in CiteRefs :
            Refs = Refs + Ref + " "
         if (BatchMode) : Problems.append(Refs)
         else : print(Refs)
         Problem = "These should be changed to use \citep or \citet"
         if (BatchMode) : Problems.append(Problem)
         else : print("**",Problem,"**")
         ReturnOK = False

   return ReturnOK

# ------------------------------------------------------------------------------

#                          A u t h o r  S u r n a m e
#
#   Passed an author name, as it might be extracted by GetAuthors(), this
#   routine extracts the surname, cleaning up any LaTeX constructions used
#   to generate properly accented characters. The intent is to generate a
#   reasonably clean name that can be used as part of the directory name for
#   the paper. It does, of course, lose some of the detail of the name, and
#   in an ideal world it would return a Unicode version of the name, but
#   for the moment this simpler scheme works well enough. I apologise to
#   authors whose accented names are mangled by this routine. Using this
#   routine also provides a consistent way of handling author's names.

def AuthorSurname (Author) :
   Comma = Author.find(',')
   if (Comma > 0) :
      Surname = Author[:Comma]
   else :
      Surname = Author
   Surname = Surname.replace("\\","").replace("'","").replace("`","") \
                  .replace("{","").replace("}","")
   Surname = Surname.replace('"u',"ue").replace('"o',"oe").replace(' ','')
   Surname = Surname.replace('"','')
   return Surname

# ------------------------------------------------------------------------------

#                    G e t  L a t e s t  F i l e  D a t e
#
#  This routine looks recursively at all the files in the current directory
#  and any sub-directories, and returns a tuple with the date and name of the
#  latest modified file that it finds. If it finds no files, it returns a date
#  of zero and a null name. The time is in seconds past the epoch.

def GetLatestFileDate () :

   First = True
   LatestFile = ""
   LatestTime = 0

   #  For each directory, os.walk returns the directory path, a list of
   #  sub-directories, and a list of files.

   for Details in os.walk('.',onerror = None) :
      DirPath = Details[0]
      
      #  We ignore files in the special directories OS X inserts under some
      #  circumstances.
      
      if (DirPath.find("__MACOSX") < 0) :
         for Name in Details[2] :
            File = os.path.join(DirPath,Name)
            
            #  We are also only interested in real files (not links to files
            #  that are missing, and not directories)
            
            if (os.path.exists(File)) :
               if (not os.path.isdir(File)) :
                  FileTime = os.stat(File).st_mtime
                  if (First) :
                     LatestTime = FileTime
                     LatestFile = File
                     First = False
                  else :
                     if (FileTime > LatestTime) :
                        LatestTime = FileTime
                        LatestFile = File

   #  I think file names look neater without a leading './'.

   if (LatestFile.startswith("./")) : LatestFile = LatestFile[2:]
   return (LatestTime,LatestFile)

# ------------------------------------------------------------------------------

#                        C h e c k  P a p e r  N a m e
#
#  Checks that the paper name specified follows the ADASS conventions. This
#  adds a description of any problem to the Problems list it is passed, and
#  returns True if the name is valid, False otherwise. The PaperName is the
#  same thing as the PaperID often referred to, and should look like B3,
#  O10-3, P8-37 etc.
#
#  This code looks quite messy, but so are the naming conventions for ADASS
#  papers. Also, if in places some of the string handling doesn't look very
#  Pythonesque, that's partly personal style, but its simple-minded scanning
#  through the strings allows me to generate the error reports I felt I needed.
#
#  Note: This code was taken originally from the code used for the script
#  PaperCheckBatch.py used for the Trieste proceedings. The use of 'X' as a
#  prefix for papers whose paper ID could not be determined is a quirk of the
#  Trieste processing, and has been left in here but disabled. The convention
#  used for poster numbering for Trieste was also used for Santiago in 2017.

def CheckPaperName(Paper,Problems) :

   #  There is a suggestion Trieste may number posters the same way Oral
   #  presentations are numbered, as P4-10, for example, rather than as
   #  P045 for example. If so, TriestePosters needs to be set true.
   #  This has been the convention now for both Trieste 2016 and Santiago
   #  2018.
   
   TriestePosters = False
   CapeTownPosters = False
   VictoriaNames = True
   
   #  Disable the use of 'X' as a prefix.
   
   XAllowed = FALSE
   
   #  Some intital checks on the leading digit, which should be O for Oral,
   #  I for Invited (also oral), B for BoF, F for Focus Demo, 'D' for
   #  Demo booth or T for Tutorial.
   
   ValidSoFar = True
   if (len(Paper) <= 0) :
      Problem = "Paper name supplied is blank"
      Problems.append(Problem)
      ValidSoFar = False
   if (ValidSoFar) :
      Letter = Paper[0]
      if (not Letter in ("IOBFPDTH" if not CapeTownPosters else "IOBFXDTH")) :
         if (Letter == 'X' and XAllowed) :
            Problems.append(
               "It seems that the paper ID could not be determined from the")
            Problems.append("name used for the submitted .tar or .zip file")
         else :
            Problem = "'" + Letter + "' is not a valid prefix for a paper"
            Problems.append(Problem)
         ValidSoFar = False
   
   if (ValidSoFar) :
      if (len(Paper) == 1) :
         Problem = "Paper does not have a number"
         Problems.append(Problem)
         ValidSoFar = False

   if (ValidSoFar) :
   
      #  Valid leading letter, now decode the number, and there are different
      #  conventions for the different paper types.
      
      Number = Paper[1:]
      NumChars = len(Number)

      if (Letter == 'B' or Letter == 'F' or Letter == 'D' or Letter == 'T') :

         #  BoFs, Focus Demos, Demo booths, and Tutorials just have a number,
         #  with no leading zeros.

         Leading = True
         for Char in Number :
            if (Leading) :
               if (Char == '0') :
                  Problem = "Paper number should not have leading zeros"
                  Problems.append(Problem)
                  ValidSoFar = False
               Leading = False
            Value = ord(Char) - ord('0')
            if (Value < 0 or Value > 9) :
               Problem = "Non-numeric character (" + Char + ") in paper number"
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
            Problems.append(Problem)
            ValidSoFar = False
         else :
            N = 0
            for Char in Number :
               Value = ord(Char) - ord('0')
               if (Value < 0 or Value > 9) :
                  Problem = "Non-numeric character (" + Char + \
                                                       ") in paper number"
                  Problems.append(Problem)
                  ValidSoFar = False
                  break
               N = N * 10 + Value
            if (ValidSoFar and N == 0) :
               Problem = "Poster number cannot be zero"
               Problems.append(Problem)
               ValidSoFar = False

      if (Letter == 'I' or Letter == 'O' or \
                                   (Letter == ('X' if CapeTownPosters else 'P') and TriestePosters)) :
         
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
                  Problems.append(Problem)
                  ValidSoFar = False
                  break
               Leading = False
            if (Char == '.' or Char == '_') :
               Problem = \
                 "Use '-' instead of '_' or '.' to separate session and number"
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
                  Problems.append(Problem)
               continue
            Value = ord(Char) - ord('0')
            if (Value < 0 or Value > 9) :
               Problem = "Non-numeric character (" + Char + \
                                                    ") in paper number"
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
               Problems.append(Problem)
               ValidSoFar = False
   
   if (not ValidSoFar) :
      if (not (Paper[0] == 'X' and XAllowed)) :
         Problem = "Paper name '" + Paper + "' is invalid"
         Problems.append(Problem)

   return ValidSoFar

# ------------------------------------------------------------------------------

#                  C h e c k  T e m p l a t e  L i n e s
#
#   This routine looks in the current directory for a file called
#   Paper.tex (where Paper will be a string such as "O1-4") - or for a
#   file called TexFileName, if this is not a null string - assuming
#   this is the main .tex file for the paper. It checks each line in
#   the file to see if it matches any of the strings passed in the
#   list of TestStrings, in the sense of starting with that test string.
#   It returns the number of matches it found. The idea is that the test
#   strings will come from the template .tex file, and this gives an
#   idea of the extent to which the .tex file in question is really just
#   a lightly modified version of the template file.

def CheckTemplateLines (Paper,TestStrings,TexFileName = "") :

   Count = 0
   
   if (TexFileName == "") : TexFileName = Paper + ".tex"
   TexFileName = os.path.abspath(TexFileName)
   if (not os.path.exists(TexFileName)) :
      print("Cannot find main .tex file",TexFileName)
   else :
   
      #  Often all the test lines will be Latex directives, starting with
      #  '\'. If so, we can speed up the tests considerably.
      
      AllSlash = True
      for Chars in TestStrings :
         if (not Chars.startswith('\\')) :
            AllSlash = False
            break

      #  Now read through the .tex file, looking for any of the lines
      #  we've been passed. Ignore comment lines, and, perhaps, lines
      #  that don't begin with '/'.

      TexFile = open(TexFileName,mode='r')
      for Line in TexFile :
         if (not Line.startswith('%')) :
            if (AllSlash and not Line.startswith('\\')) : continue
            for Chars in TestStrings :
               if (Line.startswith(Chars)) :
                  Count += 1
                  break
      TexFile.close()

   return Count

# ------------------------------------------------------------------------------

#                  S u b j e c t  I n d e x  E n t r i e s
#
#   This routine looks in the current directory for a file called
#   Paper.tex (where Paper will be a string such as "O1-4") - or for a
#   file called TexFileName, if this is not a null string - assuming
#   this is the main .tex file for the paper. It looks in the file for any
#   \ssindex entries, and returns a list of all the entries it finds.
#   Note that this includes entries that are commented out as well as
#   those that are not - this is unusual, but \ssindex is not normally
#   defined until the final stages when then full volume is created, and
#   so these entries are normally commented out in the early stages. If
#   IgnoreThese is specified, it should be a list of index entries that
#   are to be ignored (these are usually those given as examples in the
#   template file; these may still be present, but we don't generally
#   want to include them).

def SubjectIndexEntries (Paper,IgnoreThese = None,TexFileName = "") :

   Entries = []
   
   if (TexFileName == "") : TexFileName = Paper + ".tex"
   TexFileName = os.path.abspath(TexFileName)
   if (not os.path.exists(TexFileName)) :
      print("Cannot find main .tex file",TexFileName)
   else :

      #  Ideally, we'd use a TexScanner to parse subject index entries
      #  properly, but unfortunately TexScanner ignores commented out lines,
      #  and this is one case where we don't want to do this. Fortunately,
      #  because of the commening aspects of these entries, they really
      #  do have to be on separate lines, and \ssindex only takes one
      #  argument, so parsing the file directly is fairly easy.

      TexFile = open(TexFileName,mode='r')
      for Line in TexFile :
         Line = Line.strip()
         if (Line.startswith("\\ssindex") or Line.startswith("%\\ssindex")) :
            LBrace = Line.find('{')
            if (LBrace > 0) :
               RBrace = Line.find('}')
               if (RBrace > LBrace) :
                  Entry = Line[LBrace + 1:RBrace]
                  if (IgnoreThese) :
                     if (not Entry in IgnoreThese) :
                        Entries.append(Entry)
      TexFile.close()

   return Entries



