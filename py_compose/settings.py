from json import load as json_loader
from yaml import load as yaml_loader

CONFIG_FILENAME = 'py-compose'
SUPORTED_EXTENSIONS = ('yaml', 'yml', 'json')

PARSERS = {
    # YAML
    'yaml': yaml_loader,
    'yml': yaml_loader,

    # JSON
    'json': json_loader
}

SERVICE_ATTRIBUTES = (
    'basedir', 'environment', 'requirements', 'run',
    'test', 'depends_on'
)
