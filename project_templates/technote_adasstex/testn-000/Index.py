#!/usr/bin/env python

#                           I n d e x . p y
#
#  A convenience script to help with processing the submissions for the an
#  ADASS conference. It looks for index entries that have already
#  been used that match a supplied set of search terms.
#
#  This script can be run from anywhere. It works with a master subject index
#  list and a 'new' subject index list. The idea is that the master list has
#  all the entries used in previous ADASS volumes, and the new list has entries
#  for individual papers in the new volume. (Presumably at some point these
#  will be merged.)
#
#  Usage:
#      Index.py Term [Term2...]
#
#  any number of terms can be supplied on the command line, and these will be
#  looked up individually.
#
#  This program reads the current list of subject keywords from the master
#  subject index list and the new subject index list (if it exists). It
#  prints out any that match contain any of the search terms supplied as
#  arguments. The comparison is case-insensitive, and any terms found are
#  printed as a commented-out \ssindex{} directive that contains the matching
#  index entry. This can be copied and pasted directly into the .tex file
#  (preferably as a separate line).
#
#  Normally, the script uses the ADASS_Configuration file in the user's home
#  directory to locate these files. (The entries in question are
#  "MainSubjectIndexFile" and "NewSubjectIndexFile"). If the configuration
#  file does not exist, or these entries are undefined, this script will
#  look for files called "subjectKeywords.txt" and "newKeywords.txt" in
#  the default directory or in a Work subdirectory. (These fallback locations
#  make this compatible with the way an earlier version of this program ran
#  for the 2015 Sydney proceedings, but using the configuation file is much
#  more flexible.)
#
#  If the program cannot find an exising master subject index list file, it
#  prints out quite comprehensive details about where it looked and what it
#  found. It treats the new subject index list file as optional.
#
#  Author(s): Keith Shortridge (keith@knaveandvarlet.com.au)
#
#  History:
#     20th Jan 2016. Original version, KS.
#      8th Mar 2016. Now ignores lines starting with '#' in the keyword
#                    files. KS.
#     18th Jan 2017. Now uses the AdassConfig module to get the names of the
#                    subject index files from the ADASS_Configuration file.
#                    This means this can be run from anywhere, so long as the
#                    ADASS_Configuration file has been set up properly.
#     18th Aug 2017. Converted to run under Python3, using 2to3. Added
#                    the importing of items from __future__ to allow this to
#                    run under either Python2 or Python3. KS.
#     22nd Aug 2017. Now checks to make sure an item wasn't included in the
#                    mater index before listing it as in the 'new' index. KS.
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

import AdassIndex
import AdassConfig

#  See if we have any arguments (ignoring the zeroth).

Argc = len(sys.argv)
if (Argc < 2) :
   print("No search terms supplied on command line")
else :

   #  Get the path names for the master subject index list, and the new subject
   #  index list. We need there to be a master subject index list, so we
   #  complain if this doesn't exist. There may not be a new subject index
   #  list. Note that MainSubjectIndexFile() always returns the name of an
   #  existing file, and a null string if there isn't one. NewSubjectIndexFile()
   #  may return the name to be used if the file doesn't exist. ReadIndexList()
   #  returns the contents of each file in the "top level!2nd level!3rd level"
   #  form used by the actual entries inserted in the .tex file.

   Details = []
   MasterIndexPath = AdassConfig.MainSubjectIndexFile(Details)
   if (MasterIndexPath == "") :
      for Line in Details :
         print(Line)
   else :

      MasterIndexList = AdassIndex.ReadIndexList(MasterIndexPath)
      
      #  Now the new index list. If the file does not exist, ReadIndexList()
      #  would silently return an empty list, but it's easiest if we know
      #  if the file exists or not.
      
      NewIndexPath = AdassConfig.NewSubjectIndexFile()
      NewIndexExists = False
      if (os.path.exists(NewIndexPath)) :
         NewIndexList = sorted(AdassIndex.ReadIndexList(NewIndexPath))
         NewIndexExists = True
      else :
         NewIndexList = []

      #  Note that we assume the master index entries have already been
      #  sorted and will not contain duplicate entries. The new keyword file
      #  has separate sections for the various new papers and so are not
      #  likely to be in order and so have been sorted here.

      for Ind in range(1,len(sys.argv)) :

         Arg = sys.argv[Ind]

         print("")
         print("Looking for index entries matching '" + Arg + "'")
         print("")
         Arg = Arg.lower()

         #  Search the master index list. Note which ones we find.

         Count = 0
         MasterEntries = []
         for Entry in MasterIndexList :
            if (Entry.lower().find(Arg) >= 0) :
               print("%\\ssindex{" + Entry + "}")
               MasterEntries.append(Entry)
               Count = Count + 1
         if (Count == 1) :
            print("One entry in master index")
         elif (Count > 1) :
            print(Count,"entries in master index")
         else :
            print("No entries in master index")

         #  Search the new index list. Allow for the possibility of duplicate
         #  entries. (Different papers might have the same entries.) Also note
         #  that if a new second or third level entry is found in the new
         #  entry file, the new entry file will include the higher level entries
         #  as well, and those might have already been found in the master
         #  index - that's why we keep a list of ones already found in
         #  MasterEntries.

         if (NewIndexExists) :
            Count = 0
            LastEntry = ""
            for Entry in NewIndexList :
               if (Entry != LastEntry) :
                  LastEntry = Entry
                  if (Entry.lower().find(Arg) >= 0) :
                     if (not Entry in MasterEntries) :
                        Count = Count + 1
                        print("%\\ssindex{" + Entry + "}")
            if (Count == 1) :
               print("One entry in new index")
            elif (Count > 1) :
               print(Count,"entries in new index")
            else :
               print("No entries in new index")

