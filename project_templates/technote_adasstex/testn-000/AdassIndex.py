#
#                       A d a s s  I n d e x . p y
#
#  This is the code for a module that contains a number of utility routines
#  that handle operations connected with subject index entries for ADASS
#  Proceedings.
#
#  WriteSubjectIndex (IndexEntries,OutputFile)
#     Writes a list of entries in ssindex format to a file in hierarchical
#     format.
#
#  ReadIndexList (FilePath)
#     Reads a file in hierarchical format and returns a list of entries in
#     ssindex format.
#
#  'ssindex' format refers to the "topic!sub-topic!sub-topic" form used in
#  subject index entries in a .tex file, where the index string is the argument
#  to an \ssindex{} command.
#
#  'Hierarchical' format refers to the alphabetical hierarchical format used
#  in the text files usually used to record the subject entries used. This
#  looks like the way the entries will appear in the volume index, eg:
#  topic
#     sub-topic
#        sub-topic
#
#  Author(s): Keith Shortridge (keith@knaveandvarlet.com.au)
#
#  Python versions:
#      This code is compatible with both Python 2 and Python 3.
#
#  History:
#     15th Jan 2017. Original version, based on some code in the Index.py and
#                    Finish.py ADASS scripts. KS.
#     18th Aug 2017. Added comment about Python 3. KS.
#     11th Oct 2017. Corrected initial comments - duplicate words removed. KS.

import sys
import string
import os

# ------------------------------------------------------------------------------

#                     W r i t e  S u b j e c t  I n d e x
#
#  This routine is passed a list containing a set of subject entries in the
#  "topic!sub-topic!sub-topic" form. They may contain duplicates, and need
#  not be sorted. It writes these out in alphabetical hierarchical format, eg
#  topic
#     sub-topic
#        sub-topic
#  to the specified file.
#
#  Note that what is passed should be an open file, not the name of the file.
#  This allows the caller to add additional material - comments, for example -
#  before or after the entries written by this routine.

def WriteSubjectIndex (IndexEntries,OutputFile) :

   #  Writing the output file is easy enough, once we have the entries
   #  in the list sorted - which sorted() does nicely. We can then spot
   #  duplicate entries - they'll the same as the previous entry - and
   #  we can see where the various levels change. We only support three
   #  levels of entry.

   LastEntry = ""
   LastTop = ""
   LastSecond = ""
   Count = 0
   for Entry in sorted(IndexEntries) :
      if (Entry != LastEntry) :
         LastEntry = Entry
         Count = Count + 1
         Levels = Entry.split("!")
         if (Levels[0] != LastTop) :
            OutputFile.write(Levels[0] + "\r\n")
            LastTop = Levels[0]
            LastSecond = ""
         if (len(Levels) > 1) :
            if (Levels[1] != LastSecond) :
               OutputFile.write("    " + Levels[1] + "\r\n")
               LastSecond = Levels[1]
         if (len(Levels) > 2) :
            OutputFile.write("        " + Levels[2] + "\r\n")

# ------------------------------------------------------------------------------

#                     R e a d  I n d e x  L i s t
#
#  This routine is passed the name of a file containing subject index entries
#  in alphabetical hierarchical format, eg
#  topic
#     sub-topic
#        sub-topic
#  It reads these and returns a list containing these subject entries in the
#  "topic!sub-topic!sub-topic" form. Blank lines and lines beginning with
#  '#' are ignored.
#
#  Note that if the file does not exist, this routine returns an empty list
#  but does not output any error messages. If you need to know if the file
#  exists, check this before calling this routine.

def ReadIndexList (FilePath) :
   IndexList = []
   if (os.path.exists(FilePath)) :
      IndexFile = open(FilePath,mode='r')
      TopLevel = ""
      SecondLevel = ""
      for Entry in IndexFile :
         if (not Entry.startswith('#')) :
            FullEntry = ""
            if (Entry.startswith("        ")) :
               FullEntry = TopLevel + '!' + SecondLevel + '!' + \
                                    Entry.rstrip(" \r\n").lstrip()
            elif (Entry.startswith("    ")) :
               SecondLevel = Entry.rstrip(" \r\n").lstrip()
               FullEntry = TopLevel + '!' + SecondLevel
            else :
               if (Entry.strip() != "") :
                  TopLevel = Entry.rstrip(" \r\n").lstrip()
                  FullEntry = TopLevel
            if (FullEntry != "") :
               IndexList.append(FullEntry)
      IndexFile.close()
   return IndexList
