"""Main command-line interface for templatekit.
"""

__all__ = ('main',)

import click

from ..repo import Repo
from .listtemplates import list_templates
from .make import make


# Add -h as a help shortcut option
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.option(
    '-r', '--template-repo', 'template_repo',
    type=click.Path(exists=True, file_okay=False, dir_okay=True,
                    resolve_path=True),
    default='.',
    help='Path to the cloned templates Git repository, or a sub directory '
         'within the clone templates repository. Default is \'.\', the '
         'current working directory.')
@click.pass_context
def main(ctx, template_repo):
    """templatekit is a CLI for lsst/templates, LSST's project template
    repository.

    Use templatekit to learn about available templates, and to create a new
    project or file snippet based on a template.
    """
    # Subcommands should use the click.pass_obj decorator to get this
    # ctx.obj object as the first argument. Subcommands shouldn't create their
    # own Repo instance.
    ctx.obj = {'repo': Repo.discover_repo(dirname=template_repo)}


# The help command implementation is taken from
# https://www.burgundywall.com/post/having-click-help-subcommand

@main.command()
@click.argument('topic', default=None, required=False, nargs=1)
@click.pass_context
def help(ctx, topic, **kw):
    """Show help for any command.
    """
    if topic is None:
        click.echo(ctx.parent.get_help())
    else:
        click.echo(main.commands[topic].get_help(ctx))


# Add subcommands from other modules
main.add_command(list_templates, name='list')
main.add_command(make)
