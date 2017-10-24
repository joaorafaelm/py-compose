# coding=utf-8
import sys
import click
import click_completion
import crayons
from halo import Halo
from py_compose.configuration import Configuration
from py_compose.settings import (
    SERVICE_ATTRIBUTES, CONFIG_FILENAME, SUCCESS_EXIT_CODE
)

click_completion.init()
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
spinner = Halo(spinner='dots')


class ServiceName(click.ParamType):
    name = 'service_name'

    def convert(self, value, param, context):
        configuration = context.obj

        if value not in configuration.services:
            self.fail('"{}" is an invalid service name'.format(value))

        return value


SERVICE_NAME = ServiceName()


@click.group(invoke_without_command=True, context_settings=CONTEXT_SETTINGS)
@click.option('--file', default=CONFIG_FILENAME, nargs=1, help="Config file.")
@click.pass_context
def cli(context, file):

    if context.invoked_subcommand is None:
        # Display help to user, if no commands were passed.
        click.echo(context.get_help())

    else:
        # Load up config file and pass along to the pipeline context
        conf = Configuration(file)
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
    click.echo(crayons.blue('Services:'))
    for service in conf.services:
        click.echo(crayons.white('\n · {}'.format(service), bold=True))
        for attribute in SERVICE_ATTRIBUTES:
            click.echo('    {}: {}'.format(
                crayons.white(attribute, bold=True),
                getattr(conf.services.get(service), attribute)
            ))


@click.command(help='Create and start services')
@click.argument('service_names', nargs=-1, type=SERVICE_NAME)
@click.pass_context
def up(context, service_names):
    context.invoke(build, service_names=service_names)


@click.command(help='Create services')
@click.argument('service_names', nargs=-1, type=SERVICE_NAME)
@click.pass_context
def build(context, service_names):
    configuration = context.obj
    stage = 'build'

    # Filter services
    if service_names:
        services = configuration.services.filter(service_names).values()
    else:
        services = configuration.services.values()

    # Initiate subprocesses
    [s.exec(stage) for s in services]

    # Wait for all processes to finish
    for service in services:
        if service.subprocess:
            msg = '{} | Executing build stage.'
            spinner.start(text=crayons.white(msg.format(service.name)))

            service.subprocess.wait()

            if service.subprocess.returncode == SUCCESS_EXIT_CODE:
                msg = '{} | Successfully executed build stage.'
                spinner.succeed(crayons.green(msg.format(service.name)))
            else:
                msg = (
                    '{} | Error while executing build stage. '
                    'Checkout the error log for more details.'
                )
                spinner.fail(crayons.red(msg.format(service.name)))
        else:
            msg = '{} | No build stage defined.'
            click.echo(crayons.yellow(msg.format(service.name)))


cli.add_command(up)
cli.add_command(build)
cli.add_command(config)

# TODO: stop restart rm ls version logs config

if __name__ == '__main__':
    cli()
