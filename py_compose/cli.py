import sys
import click
import click_completion
import crayons
from py_compose.configuration import Configuration
from py_compose.settings import SERVICE_ATTRIBUTES

click_completion.init()
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(invoke_without_command=True, context_settings=CONTEXT_SETTINGS)
@click.pass_context
def cli(context):

    if context.invoked_subcommand is None:
        # Display help to user, if no commands were passed.
        click.echo(context.get_help())

    else:
        # Load up config file and pass along to the pipeline context
        conf = Configuration()
        if conf.filename:
            context.obj = conf
        else:
            click.echo(crayons.red('Configuration file not found.'))
            sys.exit(1)


@click.command(help='Display configuration file')
@click.pass_context
def config(context):
    conf = context.obj
    click.echo('{}: {}'.format(crayons.blue('Filename'), conf.filename))
    click.echo('{}: {}'.format(crayons.blue('Extension'), conf.extension))
    click.echo('{}:'.format(crayons.blue('Services')))
    for service in conf.services:
        click.echo(crayons.white('\n · {}'.format(service), bold=True))
        for attribute in SERVICE_ATTRIBUTES:
            click.echo('    {}: {}'.format(
                crayons.white(attribute, bold=True),
                getattr(conf.services.get(service), attribute)
            ))


@click.command(help='Create and start services')
@click.argument('service_name', default=False)
@click.pass_context
def up(context, service_name=False):
    context.invoke(build, service_name=service_name)


@click.command(help='Create services')
@click.argument('service_name', default=False)
@click.pass_context
def build(context, service_name=False):
    configuration = context.obj
    if service_name:
        click.echo(configuration.services.get(service_name))
    else:
        click.echo(configuration.services)


cli.add_command(up)
cli.add_command(build)
cli.add_command(config)

# TODO: stop restart rm ls version logs config

if __name__ == '__main__':
    cli()
