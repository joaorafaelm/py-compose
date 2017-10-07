from setuptools import setup

requires = ['click', 'crayons', 'PyYAML']


setup(
    name="py-compose",
    version='0.0.0',
    description="",
    long_description="\n\n".join([open("README.rst").read()]),
    license='MIT',
    author="João Rafael",
    author_email="seb@roadsi.de",
    url="https://py-compose.readthedocs.org",
    packages=['py_compose'],
    install_requires=requires,
    entry_points={
        'console_scripts': [
            'py-compose = py_compose.cli:cli'
        ]
    },
    classifiers=[
        'Development Status :: 1 - Planning',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: CPython']
)