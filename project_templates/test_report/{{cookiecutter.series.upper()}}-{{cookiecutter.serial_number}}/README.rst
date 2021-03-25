.. image:: https://img.shields.io/badge/{{ cookiecutter.series.lower() }}--{{ cookiecutter.serial_number }}-lsst.io-brightgreen.svg
   :target: https://{{ cookiecutter.series.lower() }}-{{ cookiecutter.serial_number }}.lsst.io
.. image:: https://github.com/{{ cookiecutter.github_org }}/{{ cookiecutter.series.lower() }}-{{ cookiecutter.serial_number }}/workflows/CI/badge.svg
   :target: https://github.com/{{ cookiecutter.github_org }}/{{ cookiecutter.series.lower() }}-{{ cookiecutter.serial_number }}/actions/

{{ "#" * (cookiecutter.series|length + cookiecutter.serial_number|length + 1) }}
{{ cookiecutter.series.upper() }}-{{ cookiecutter.serial_number }}
{{ "#" * (cookiecutter.series|length + cookiecutter.serial_number|length + 1) }}

{{ cookiecutter.title }}

To regenerate from Jira use the github action "docgen from Jira" on your branch. 
