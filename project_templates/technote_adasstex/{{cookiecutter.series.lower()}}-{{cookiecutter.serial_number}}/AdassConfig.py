#
#                       A d a s s  C o n f i g . p y
#
#  This is the code for a module that contains a number of utility routines
#  that handle configuratrion setting for the various utility programs that
#  are used in processing the papers submitted for ADASS Proceedings.
#
#  MainSubjectIndexFile ()
#     Returns the path to the main subject index file.
#
#  If the configuration file exists, it is called ADASS_Configuration and
#  is in the user's home directory. This file has a simple format: each line
#  is a pair of strings, an entry name and a value for that entry, separated
#  by one or more spaces. Strings with spaces can be quoted, using either
#  'single' or "double" quotes. Anything on the line following the second
#  string is taken as a comment. Blank lines, and lines where the first non-
#  blank character is '#', are ignored. Note that it is possible for the value
#  of an entry to be an empty string, specified in the file as "".
#
#  Author(s): Keith Shortridge (keith@knaveandvarlet.com.au)
#
#  History:
#     17th Jan 2017. Original version. KS.
#     18th Aug 2017. Converted to run under Python3, using 2to3. Added
#                    the importing of items from __future__ to allow this to
#                    run under either Python2 or Python3. (Actually, 2to3
#                    made no changes, but the import from __future__ was put
#                    in anyway, in case it turns out to be needed later.) KS.
#     19th Aug 2017. Added NewSubjectIndexLocation(). KS.
#     22nd Nov 2017. Added AspDirectory(). KS.
#
#  Python versions:
#     This code should run under either python 2 or python 3, so long as
#     the python 2 version supports the "from __future__ import" used here.
#     It has been tested under 2.7 and 3.6.
# 

from __future__ import (print_function,division,absolute_import)

import sys
import string
import os
import shlex

_AdassConfigDict = {}
_AdassConfigFileTried = False
_AdassConfigDir = "~"
_AdassConfigFile = "ADASS_Configuration"

# ------------------------------------------------------------------------------

#                     L o a d  C o n f i g  E n t r i e s
#
#  This routine makes sure that any definitions in the user's ADASS
#  configuration file (if it exists) have been read into _AdassConfigDict.
#  The first time this is called, it tries to read the entries into the file.
#  On subsequent calls, it doesn't - so if the file has changed, or appeared,
#  since that first call, this will be missed. It only tries to read the file
#  once.

def LoadConfigEntries (Details = None) :

   global _AdassConfigFileTried      # Needed because this routine 'updates' it
   
   #  The first time this routine is called, it tries to open the configuration
   #  file and read the entries from it. This code ignores blank lines and
   #  comment lines (lines where the first non-blank character is '#') and
   #  uses shlex.split() to handle quoted strings properly. All entries and
   #  their values are set into _AdassConfigDict.
   
   if (not _AdassConfigFileTried) :
      _AdassConfigFileTried = True
      if (ConfigFileExists(Details)) :
         HomeDir = os.path.expanduser(_AdassConfigDir)
         ConfigFileName = os.path.join(HomeDir,_AdassConfigFile)
         ConfigFile = open(ConfigFileName,"r")
         for Line in ConfigFile :
            Line = Line.strip(" \r\n")
            if (Line != "") :
               if (not Line.startswith('#')) :
                  Entries = shlex.split(Line)
                  if (len(Entries) >= 2) :
                     _AdassConfigDict[Entries[0]] = Entries[1]

# ------------------------------------------------------------------------------

#                     C o n f i g  F i l e  E x i s t s
#
#  Returns true if the ADASS configuration file exists, false otherwise. If
#  Details is supplied, it should be a list of strings, to which this routine
#  will add details of the file and whether it could be found.

def ConfigFileExists(Details = None) :

   Exists = False
   Log = (Details != None)
   HomeDir = os.path.expanduser(_AdassConfigDir)
   ConfigFileName = os.path.join(HomeDir,_AdassConfigFile)
   if (os.path.exists(ConfigFileName)) : Exists = True
   if (Log) :
      if (Exists) :
         Details.append("Configuration file is " + _AdassConfigFile + " in " + \
                                                                        HomeDir)
      else :
         Details.append("Configuration file should be " + _AdassConfigFile + \
                                                              " in " + HomeDir)
         Details.append("but this file does not exist")
   return Exists


# ------------------------------------------------------------------------------

#                     L o o k u p  C o n f i g  E n t r y
#
#  Returns the value of a named entry in the user's ADASS configuration file,
#  if possible.  If the file cannot be opened, or if the specified entry has
#  not been defined in it, this routine returns None. The optional
#  Details argument is a list of strings to which this appends a description
#  of its results.

def LookupConfigEntry (EntryName,Details = None) :
   
   LoadConfigEntries(Details)
   
   #  Assuming we've read the configuration file entries into the dictionary,
   #  if possible, look up the entry in there, returning None if it's missing.

   Value = _AdassConfigDict.get(EntryName,None)
   
   #  If the entry isn't defined, this may be because the configuration file
   #  doesn't exist, or becasue it didn't have the entry we were looking for.
   
   if (Details != None) :
      if (Value == None) :
         if (ConfigFileExists()) :
            Details.append(EntryName + \
                               " is not defined in the configuration file")
         else :
            Details.append("No configuration file: Cannot look up " + EntryName)
      else :
         Details.append(EntryName + " is defined as '" + Value + \
                                                "' in the configuration file")

   return Value

# ------------------------------------------------------------------------------

#                           L o c a t e   F i l e
#
#  This is a general-purpose file finding routine. It is passed the name of
#  a configuration item that should define the file location in the main
#  ADASS configuration file. It looks up that item and looks for the file
#  it specifies. If it fails to find the configuration file, or the item,
#  it will look for the file using the name passed, first in the default
#  directory, then in a set of other directories passed as a list. The optional
#  Details argument is a list of strings to which this appends a description
#  of the steps it took and the results.

def LocateFile (Description,ConfigEntryName,FileName,DirectoryList,\
                                                             Details = None) :
   
   Path = ""
   
   #  Most of the code in this routine is to do with logging the details.
   #  But I think that can be useful, particularly if the file can't be found.
   
   Log = False
   if (Details != None) : Log = True
   
   if (Log) :
      Details.append("Looking for " + Description)
   
   #  If there is a specification for this file in the main ADASS configuration
   #  file, we should use it, and we should expect the specified file to exist.
   #  LookupConfigEntry() itself will fill in Details if the config file
   #  doesn't exist or if it doesn't have the entry defined.
   
   ConfigPath = LookupConfigEntry(ConfigEntryName,Details)
   if (ConfigPath != None and ConfigPath != "") :
      if (ConfigPath.startswith('~')) :
         ConfigPath = os.path.expanduser(ConfigPath)
      if (os.path.exists(ConfigPath)) :
         Path = ConfigPath
         if (Log) :
            Details.append( \
                 "The file specified in the configuration file exists")
      else :
         if (Log) :
            Details.append( \
               "The file specified in the configuration file does not exist")

   if (Path == "") :
   
      #  If we can't find an entry in a configuration file, see if there
      #  is a file in the default directory.
      
      if (Log) :
         Details.append("Will look in specific locations for the file.")
      
      if (os.path.exists(FileName)) :
         Path = FileName
         if (Log) : Details.append("Using file found in default directory")
         
   if (Path == "") :

      #  If we can't find a file in the default directory, work through the
      #  various other directories passed in the directory list.
      
      if (Log) :
         Details.append(FileName + " not found in the default directory")
      
      for Dir in DirectoryList :

         DirFileName = os.path.join(Dir,FileName)
         if (os.path.exists(DirFileName)) :
            if (Log) :
               Details.append("Using file found in " + Dir + " directory")
            Path = DirFileName
            break
         else :
            if (Log) :
               Details.append( \
                     FileName + " not found in " + Dir + " directory")
         
   if (Path == "" and Log) :
      Details.append("Cannot locate " + Description)

   return Path



# ------------------------------------------------------------------------------

#                  M a i n  S u b j e c t  I n d e x  F i l e
#
#  This routine returns a path to the main subject index file. This is a file
#  containing the various subject index topics that have been used for
#  previous ADASS conferences, in an alphabetical hierarchical format. (For
#  more details about subject index file formats see the comments to the
#  AdassIndex.py module.) It may be that during the course of editing of a
#  new Proceedings volume, this file is updated from time to time.
#  Alternatively, it may be supplemented by a 'new' subject index file,
#  containing new entries used for the current conference.
#
#  This routine looks in various places for such a file.
#  If no such file can be found, an empty string is returned. Note that if
#  a non-empty string is returned, this is the pathname of a file that exists.
#  An optional Details list can be passed. If so, this routine appends to it a
#  set of strings describing its progress and where it looked for the file.
#  This gives the caller the option of printing these out if the file cannot be
#  found.

def MainSubjectIndexFile (Details = None) :

   #  For historical reasons, we fall back on looking in a Work sub-directory
   #  for the file - this is where it was for the Sydney ADASS processing.
   
   Path = LocateFile ("main subject index file","MainSubjectIndexFile", \
                                      "subjectKeywords.txt",["Work"],Details)
   return Path

# ------------------------------------------------------------------------------

#                  N e w  S u b j e c t  I n d e x  F i l e
#
#  This routine returns a path to the new subject index file. This is a file
#  containing the various subject index topics that have been used for
#  papers in the current volume, in an alphabetical hierarchical format, with
#  a separate section for each paper. (For more details about subject index file
#  formats see the comments to the AdassIndex.py module.)
#
#  This routine looks in various places for such a file. If an existing file
#  can be found, this will be used. However, especially at the start of the
#  editing process for a new volume, such a file may not exist and a new
#  one will have to be created. If no file is found in the expected places,
#  but there is a file name defined in the configuration file, this routine
#  will return that configuration file name. An emptry string will be returned
#  if no existing file can be found and there was no specification given in
#  the configuration file.
#
#  An optional Details list can be passed. If so, this routine appends to it a
#  set of strings describing its progress and where it looked for the file.
#  This gives the caller the option of printing these out if the file cannot be
#  found.

def NewSubjectIndexFile (Details = None) :

   #  For historical reasons, we fall back on looking in a Work sub-directory
   #  for the file - this is where it was for the Sydney ADASS processing.
   
   ConfigEntryName = "NewSubjectIndexFile"
   Path = LocateFile ("new subject index file",ConfigEntryName, \
                                      "newKeywords.txt",["Work"],Details)
   if (Path == "") :
   
      #  Couldn't find an existing file. See if the configuration file gave
      #  the name for a new file we can create. (We could fall back on
      #  'newKeywords.txt' in the default directory, but I don't think we
      #  should.)
      
      ConfigPath = LookupConfigEntry(ConfigEntryName,Details)
      if (ConfigPath != None and ConfigPath != "") :
         if (Details != None) :
            Details.append("Using file name defined in configuration file")
         if (ConfigPath.startswith('~')) :
            ConfigPath = os.path.expanduser(ConfigPath)
         Path = ConfigPath
      else :
         if (Details != None) :
            Details.append("A configuration file entry is needed to supply" + \
                                                       " the file name to use")
   
   return Path

# ------------------------------------------------------------------------------

#              N e w  S u b j e c t  I n d e x  L o c a t i o n
#
#  This routine returns a description of where this code looks for the new
#  subject index file. The idea is that if the user might want to change the
#  file used, or if they might be wondering why it can't be found, it would
#  be useful to print out a brief summary of the details of its location.
#  This routine returns a list of text strings that contain the required
#  information.

def NewSubjectIndexLocation () :

   Details = []
   Details.append("The 'new' subject index file is found as follows:")
   HomeDir = os.path.expanduser(_AdassConfigDir)
   Details.append("There is normally a configuration file " + \
                                        _AdassConfigFile + " in " + HomeDir)
   Details.append("A 'NewSubjectIndexFile' entry in the configuration file" \
                                            " gives the index file location")
   Details.append("If this fails, a 'Work/newKeywords.txt' will be used if" \
                                                              " this exists")
   return Details

# ------------------------------------------------------------------------------

#                        A s p  P i r e c t o r y
#
#  This routine returns a path to a directory that contains the asp2014.bst
#  and asp2014.sty files needed by an ADASS paper.
#
#  This routine looks in various places for these files. It will start by
#  looking for them in the current default directory. If it cannot find them
#  there it looks in the configuration file for an item called AspDirectory.
#  If that defines a directory that contains the asp2014 files, it will
#  return that. If it still cannot find the asp2014 files, it will return
#  an empty string. If it does find the files, it returns the absolute path
#  of the directory that contains them.
#
#  An optional Details list can be passed. If so, this routine appends to it a
#  set of strings describing its progress and where it looked for the files.
#  This gives the caller the option of printing these out if the file cannot be
#  found.

def AspDirectory (Details = None) :

   Found = False
   Directory = os.path.abspath(".")

   #  Start by looking in the current default directory.

   if (os.path.exists("asp2014.sty") and os.path.exists("asp2014.bst")) :
      if (Details != None) :
         Details.append ("asp2014.sty and asp2014.bst both found in " \
                                                              + Directory)
      Found = True
   else :
      if (Details != None) :
         Details.append ("asp2014.sty and asp2014.bst are not both in " \
                                                              + Directory)

      #  See if we have a configuration specification for AspDirectory

      if (Details != None) :
         Details.append( \
            "Looking for AspDirectory specification in configuration file")
      ConfigDetails = []
      Directory = LookupConfigEntry("AspDirectory",ConfigDetails)
      if (Directory == None or Directory == "") :
         if (Details != None) : Details.extend (ConfigDetails)
      else :
         if (Directory.startswith('~')) :
            Directory = os.path.expanduser(Directory)
         StyFile = os.path.join(Directory,"asp2014.sty")
         BstFile = os.path.join(Directory,"asp2014.bst")
         if (os.path.exists(StyFile) and os.path.exists(BstFile)) :
            if (Details != None) : Details.append ( \
               "asp2014.sty and asp2014.bst both found in " + Directory)
            Found = True
         else :
            if (Details != None) : Details.append ( \
               "asp2014.sty and asp2014.bst are not both in " + Directory)

   if (not Found) : Directory = ""

   return Directory



