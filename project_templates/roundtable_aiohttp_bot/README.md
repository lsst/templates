# roundtable_aiohttp_bot

**Develop an aiohttp-based bot (built with [Safir](https://safir.lsst.io])), hosted on SQuaRE's Roundtable platform.**

This template builds a bot that can be deployed on [Roundtable](https://roundtable.lsst.io), SQuaRE's Kubernetes-based service platform.
Bots can take many forms and functions:

- A bot might have an HTTP API.
- A bot might consume or produce Kafka messages (SQuaRE Events).
- A bot might add functionality to sqrbot-jr (Slack bot).
- A bot might do something on a scheduled basis, like a cron-based task.
- A bot can do some combination of all of the above.

This template, in particular, gets you started building a Python-based bot with the [aiohttp.web](https://docs.aiohttp.org/en/stable/web.html) framework.
The template uses SQuaRE's [Safir](https://safir.lsst.io) framework to help you build the application and integrate with Roundtable's features.

To learn how to configure and develop an application using this template, see the tutorial [Creating an app from the template](https://safir.lsst.io/set-up-from-template.html).
Once you've created the template, feel free to develop and customize your application as you require.
Aside from needing to be Kubernetes-deployable, Roundtable doesn't require completely homogeneous app structures.

## Template variables

### cookiecutter.repo_name

This is the name of the GitHub repository.

### cookiecutter.package_name

This is the name of the bot's Python package.
By default, it is normalized from `repo_name`.

### cookiecutter.summary

A one-sentence summary of the bot.
This is used as the GitHub repository summary, and repeated in the README and various aspects of the bot's packaging.

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

The [example](example) directory is a bot created using only the template defaults.
