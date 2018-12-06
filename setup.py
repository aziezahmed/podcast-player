"""Packaging settings."""

from codecs import open
from os.path import abspath, dirname, join
from subprocess import call

from setuptools import Command, find_packages, setup

from podcast_player import __version__


this_dir = abspath(dirname(__file__))
with open(join(this_dir, 'README.rst'), encoding='utf-8') as file:
    long_description = file.read()


class RunTests(Command):
    """Run all tests."""
    description = 'run tests'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        """Run all tests!"""
        errno = call(['py.test', '--cov=podcast', '--cov-report=term-missing'])
        raise SystemExit(errno)


setup(
    name = 'podcast-player',
    version = __version__,
    description = 'A Python command line podcast player.',
    long_description = long_description,
    url = 'https://github.com/aziezahmed/podcast-player',
    author = 'Aziez Ahmed Chawdhary',
    author_email = '',
    license = 'MIT License',
    classifiers = [
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        'License :: Public Domain',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Environment :: Console',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords = ["cli", "audio", "podcast", "stream"],
    packages = find_packages(exclude=['docs', 'tests*']),
    install_requires = ['docopt', 'pyinquirer', 'feedparser', 'listparser', 'sqlobject', 'configparser'],
    extras_require = {
        'test': ['coverage', 'pytest', 'pytest-cov'],
    },
    entry_points = {
        'console_scripts': [
            'podcast=podcast_player.cli:main',
        ],
    },
    cmdclass = {'test': RunTests},
)
