from os.path import isfile
from py_compose.settings import (
    CONFIG_FILENAME, SUPORTED_EXTENSIONS, PARSERS,
    SERVICE_ATTRIBUTES
)


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
        return PARSERS.get(self.extension)(
            open(self.filename, 'r')
        )

    def exists(self, filename, extensions):
        for extension in extensions:
            file = '{}.{}'.format(filename, extension)
            if isfile(file):
                self.filename = file
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
        self.environment = environment
        self.build = build
        self.run = run
        self.test = test
        self.depends_on = depends_on

    def __repr__(self):
        return '<%s %s object at %s>' % (
            self.__class__.__name__,
            self.name,
            hex(id(self))
        )

    def install_requirements(self):
        pass
