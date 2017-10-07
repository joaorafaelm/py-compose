import click
import crayons
import sys
from py_compose.configuration import Configuration

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(invoke_without_command=True, context_settings=CONTEXT_SETTINGS)
@click.pass_context
def cli(context):
    if context.invoked_subcommand is None:
        # Display help to user, if no commands were passed.
        click.echo(context.get_help())

    else:
        # Load up config file and pass along to the pipeline context
        if Configuration.exists():
            context.obj = Configuration()
        else:
            click.echo(crayons.red('Configuration file not found.'))
            sys.exit(1)


@click.command(help='Display the configuration file')
@click.pass_context
def config(context):
    click.echo(context.obj.services)


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
