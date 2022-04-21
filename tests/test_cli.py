"""Tests for our main skele CLI module."""


from subprocess import PIPE, Popen as popen
from unittest import TestCase

from podcast_player import __version__ as VERSION

class TestHelp(TestCase):
    def test_returns_usage_information(self):
        output = popen(['podcast', '-h'], stdout=PIPE).communicate()[0]
        self.assertTrue('Usage:'.encode('utf-8') in output)

        output = popen(['podcast', '--help'], stdout=PIPE).communicate()[0]
        self.assertTrue('Usage:'.encode('utf-8') in output)


class TestVersion(TestCase):
    def test_returns_version_information(self):
        output = popen(['podcast', '--version'], stdout=PIPE).communicate()[0]
        self.assertEqual(output.strip(), VERSION.encode('utf-8'))


