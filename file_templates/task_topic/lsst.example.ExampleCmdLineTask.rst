.. lsst-task-topic:: lsst.example.ExampleCmdLineTask

##################
ExampleCmdLineTask
##################

.. Summary paragraph (a few sentences)
.. The aim is to say what the task is for

``ExampleCmdLineTask`` [active tense verb] ...
.. If the task consumes or creates datasets, name those datasets here.
.. If there are many datasets, name the ones that people use more frequently.
``ExampleCmdLineTask`` is available as a :ref:`command-line task <pipe-tasks-command-line-tasks>`, :command:`exampleCmdLineTask.py`.

.. _ExampleCmdLineTask-summary:

Processing summary
==================

.. If the task does not break work down into multiple steps, don't use a list.
.. Instead, summarize the computation itself in a paragraph or two.

``ExampleCmdLineTask`` runs this sequence of operations:

#. Runs this thing. (FIXME)

#. Processes processes that intermediate result. (FIXME)

#. Stores those results in this last step. (FIXME)

.. ExampleCmdLineTask-cli:

exampleCmdLineTask.py command-line interface
============================================

.. code-block:: text

   exampleCmdLineTask.py REPOPATH [@file [@file2 ...]] [--output OUTPUTREPO | --rerun RERUN] [--id] [other options]

Key arguments:

:option:`REPOPATH`
   The input Butler repository's URI or file path.

Key options:

:option:`--id`:
   The data IDs to process.

.. seealso::

   See :ref:`command-line-task-argument-reference` for details and additional options.

.. _ExampleCmdLineTask-api:

Python API summary
==================

.. lsst-task-api-summary:: lsst.example.ExampleCmdLineTask

.. _ExampleCmdLineTask-butler:

Butler datasets
===============

When run as the ``exampleCmdLineTask.py`` command-line task, or directly through the `~lsst.example.ExampleCmdLineTask.runDataRef` method, ``ExampleCmdLineTask`` obtains datasets from the input Butler data repository and persists outputs to the output Butler data repository.
Note that configurations for ``ExampleCmdLineTask``, and its subtasks, affect what datasets are persisted and what their content is.

.. _ExampleCmdLineTask-butler-inputs:

Input datasets
--------------

``fixmeDatasetName``
    Brief description of the dataset.

.. _ExampleCmdLineTask-butler-outputs:

Output datasets
---------------

``fixmeOutputDatasetName``
    Brief description of this output dataset.


.. _ExampleCmdLineTask-subtasks:

Retargetable subtasks
=====================

.. lsst-task-config-subtasks:: lsst.pipe.tasks.processCcd.ProcessCcdTask

.. _ExampleCmdLineTask-configs:

Configuration fields
====================

.. lsst-task-config-fields:: lsst.pipe.tasks.processCcd.ProcessCcdTask

.. _ExampleCmdLineTask-examples:

Examples
========

.. Add a brief example here.
.. If there are multiple examples
.. (such as one from a command-line context and another that uses the Python API)
.. you can separate each example into a different subsection for clarity.

.. _ExampleCmdLineTask-debug:

Debugging
=========

.. If the task provides debug variables document them here using a definition list.
