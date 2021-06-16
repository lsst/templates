# fastapi_safir_app

**Develop a FastAPI-based web application (built with [Safir](https://safir.lsst.io])).**

This template builds a Python-based Kubernetes application using the [FastAPI](https://fastapi.tiangolo.com/) frameowrk.
It is primarily intended for API services.
The template uses SQuaRE's [Safir](https://safir.lsst.io) framework to help you build the application.

To learn how to configure and develop an application using this template, see the tutorial [Creating an app from the template](https://safir.lsst.io/set-up-from-template.html).
Once you've created the template, feel free to develop and customize your application as you require.

## Template variables

### cookiecutter.name

This is the name of the GitHub repository.

### cookiecutter.package_name

This is the name of the application's Python package.
By default, it is normalized from `repo_name`.

### cookiecutter.summary

A one-sentence summary of the application.
This is used as the GitHub repository summary, and repeated in the README and various aspects of the application's packaging.

### cookiecutter.copyright_year

The year, or years that the named institution made contributions.
For consecutive years, use a dash (`2016-2018`).
For nonconsecutive years, use a comma (`2016, 2018`).

The default is the current year.

### cookiecutter.copyright_holder

Legal name of the institution that claims copyright.
The choice list covers all DM institutions.
If you need to assign a copyright to a different institution, you can modify the search-and-replace after the package is created.
For more details, see [Managing license and copyright in Stack packages](https://developer.lsst.io/stack/license-and-copyright.html).

### cookiecutter.github_org

The GitHub organization where the app resides.
For production applications, this should be `lsst-sqre`.
To test template production, use `lsst-sqre-testing`.

## Examples

The [example](example) directory is an application created using only the template defaults.
