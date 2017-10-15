import os
import subprocess
import signal


class Command(object):

    def __init__(self, cmd, name=None, env=None):
        super(Command, self).__init__()
        self.cmd = cmd
        self.name = name
        self.env = env or os.environ.copy()
        self.subprocess = None

    def __repr__(self):
        return '<Command {!r}>'.format(self.cmd)

    @property
    def _popen_args(self):
        return self.cmd

    @property
    def _default_popen_kwargs(self):
        return {
            'env': self.env,
            'stdout': open('{}/{}.out'.format(os.getcwd(), self.name), 'w'),
            'stderr': open('{}/{}.err'.format(os.getcwd(), self.name), 'w'),
            'shell': True,
            'universal_newlines': True,
            'bufsize': 0
        }

    @property
    def std_out(self):
        return self.subprocess.stdout

    @property
    def out(self):
        """Std/out output (cached)"""
        return self.std_out.read()

    @property
    def std_err(self):
        return self.subprocess.stderr

    @property
    def err(self):
        """Std/err output (cached)"""
        return self.std_err.read()

    @property
    def pid(self):
        """The process' PID."""
        return self.subprocess.pid

    @property
    def return_code(self):
        # Standard subprocess method.
        return self.subprocess.returncode

    @property
    def std_in(self):
        return self.subprocess.stdin

    def run(self):
        popen_kwargs = self._default_popen_kwargs.copy()
        s = subprocess.Popen(self._popen_args, **popen_kwargs)
        self.subprocess = s

    def terminate(self):
        self.subprocess.terminate()

    def kill(self):
        self.subprocess.kill(signal.SIGINT)


def chain(commands, name=None, env=None):
    data = []

    for command in commands:
        c = Command(command, name, env)
        c.run()
        data.append(c)

    return data


if __name__ == '__main__':
    r = chain(['.', 'ls -lha'])
    print('ae')