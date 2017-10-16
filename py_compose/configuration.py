from os.path import isfile
from py_compose.settings import (
    CONFIG_FILENAME, SUPORTED_EXTENSIONS, PARSERS,
    SERVICE_ATTRIBUTES
)
from subprocess import call, Popen
from os import (chdir, environ)
from os.path import dirname


class Configuration:
    filename = None
    extension = None
    services = {}

    def __init__(
            self, config_file=CONFIG_FILENAME, extensions=SUPORTED_EXTENSIONS
    ):
        if self.exists(config_file, extensions):
            self.config = self._parse()
            self._cast_services()

            # If a custom file is specified, changes the working dir.
            exec_dir = dirname(config_file)
            if exec_dir:
                chdir(exec_dir)

    def _cast_services(self):
        services = self.config.get('services')
        for name, attributes in services.items():
            filtered_attributes = {
                key: attributes.get(key) for key in SERVICE_ATTRIBUTES
            }
            self.services.update({
                name: Service(name, self, **filtered_attributes)
            })

    def _parse(self):
        return PARSERS.get(self.extension)(open(self.filename, 'r'))

    def exists(self, filename, extensions):
        for extension in extensions:
            if extension not in filename:
                filename = '{}.{}'.format(filename, extension)
            if isfile(filename):
                self.filename = filename
                self.extension = extension
                return True
        return False


class Service:

    def __init__(
            self, name=None, config=None, basedir=None,
            build=None, environment=None, run=None, test=None,
            depends_on=None
    ):
        self.name = name
        self.config = config
        self.basedir = basedir
        self.build = build
        self.run = run
        self.test = test
        self.depends_on = depends_on
        self.subprocess = None
        self._environ_encode(environment)

    def __repr__(self):
        return '<%s %s object at %s>' % (
            self.__class__.__name__,
            self.name,
            hex(id(self))
        )

    def _environ_encode(self, environ):
        if isinstance(environ, dict):
            self.environment = {
                key: str(value) for key, value in environ.items()
            }
        else:
            self.environment = {}

    def exec(self, stage):

        log_handler = open('{}-{}.log'.format(self.name, stage), 'w')

        params = {
            'env': dict(environ.copy(), **self.environment),
            'stdout': log_handler,
            'stderr': log_handler,
            'shell': True,
            'universal_newlines': True,
            'bufsize': 0,
            'cwd': self.basedir
        }

        if getattr(self, stage):
            command = ' && '.join(getattr(self, stage))
            self.subprocess = Popen(command, **params)
