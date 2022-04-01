######################################################
Rubin Observatory Personal SIT-Com Notebook Repository
######################################################

This repository is to store and organize notebooks and any associated methods which contain Rubin related work but are not meant for public consumption and are not expected to be supported by the author.
The reason for creation of this repo is to ensure work is documented and stored in a place that is available by all SIT-Com personnel.
This is important to ensure content is available to others in the event that the original author cannot support the activity.

To keep the size of the repository small and therefore faster to clone/manage, it is recommended to clear the notebooks of rendered content before committing via git.
It is also recommended that notebooks and/or associated methods that may need to be used by others contain a minimal amount of documentation and/or comments to provide context and/or instructions.

Notebooks
=========

User notebooks should be stored in the notebooks directory.
Many users find it useful to organize their notebooks according to the site in which they are meant to be used and/or the platform from which they are meant to be run (e.g. summit, tts, usdf, ncsa).
For this reason, the example notebook is in a site-specific folder (summit).

Methods
=======

User methods developed to support notebooks should be stored in the python directory.
It is strongly recommended to follow Rubin development formats/practices to standardize behavior and minimize the overhead when sharing/running each others code.
This repo is eups compatible.
If a user wishes to develop their own support methods, this repo must be setup prior to importing them.

One way to setup this repo is to add the following to the ``~/notebooks/.user_setups`` file::

    setup -j notebooks_{{ cookiecutter.username }} -r ~/develop/notebooks_{{ cookiecutter.username }}

Tests
=====

Unit tests should be stored in the tests directory.
