.. lsst-task-topic:: lsst.example.ExampleTask

###########
ExampleTask
###########

.. Summary paragraph (a few sentences)
.. The aim is to say what the task is for

``ExampleTask`` [active tense verb] ...
.. If the task consumes or creates datasets, name those datasets here.
.. If there are many datasets, name the ones that people use more frequently.

.. _ExampleTask-summary:

Processing summary
==================

.. If the task does not break work down into multiple steps, don't use a list.
.. Instead, summarize the computation itself in a paragraph or two.

``ExampleTask`` runs this sequence of operations:

#. Runs this thing. (FIXME)

#. Processes processes that intermediate result. (FIXME)

#. Stores those results in this last step. (FIXME)

.. _ExampleTask-api:

Python API summary
==================

.. lsst-task-api-summary:: lsst.example.ExampleTask

.. _ExampleTask-subtasks:

Retargetable subtasks
=====================

.. lsst-task-config-subtasks:: lsst.pipe.tasks.processCcd.ProcessCcdTask

.. _ExampleTask-configs:

Configuration fields
====================

.. lsst-task-config-fields:: lsst.pipe.tasks.processCcd.ProcessCcdTask

.. _ExampleTask-examples:

Examples
========

.. Add a brief example here.
.. If there are multiple examples
.. (such as one from a command-line context and another that uses the Python API)
.. you can separate each example into a different subsection for clarity.

.. _ExampleTask-debug:

Debugging
=========

.. If the task provides debug variables document them here using a definition list.
