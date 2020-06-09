from templatekit.builder import cookiecutter_project_builder

env = Environment(BUILDERS={'Cookiecutter': cookiecutter_project_builder})

# First example
env.Cookiecutter(AlwaysBuild(Dir('example')),
                 'cookiecutter.json')
