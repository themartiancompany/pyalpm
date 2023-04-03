import pytest

from pycman.config import init_with_config, init_with_config_and_options, InvalidSyntax
from pycman.pkginfo import format_attr


BAD_CONFIG = """
Invalid
NonExistant = /
"""

CONFIG = """
[options]
RootDir = {rootdir}
DBPath = {dbpath}
"""

CONFIG_WITH_INCLUDE = """
Include = {config}
[core]
Server = https://example.com/archlinux/$repo/os/$arch/
"""

CONFIG_WITH_INCLUDE_SECTION = """
[options]
Include = {config}

[core]
Server = https://example.com/archlinux/$repo/os/$arch/
"""

OPTIONS_SECTION_CONFIG = """
RootDir = {rootdir}
DBPath = {dbpath}
"""

INCLUDED_CONFIG = """
[options]
RootDir = {rootdir}
DBPath = {dbpath}
"""


def test_init_with_config_invalid(tmpdir):
    configfile = tmpdir.join("bad.cfg")
    configfile.write(BAD_CONFIG)

    with pytest.raises(InvalidSyntax) as exc_info:
        init_with_config(str(configfile))
    assert "statement outside of a section: 'Invalid'" in str(exc_info.value)


def test_init_with_config(tmpdir):
    rootdir = "/"
    dbpath = str(tmpdir)

    configfile = tmpdir.join("good.cfg")
    configfile.write(CONFIG.format(rootdir=rootdir, dbpath=dbpath))
    handle = init_with_config(str(configfile))

    assert handle.dbpath == dbpath + '/'
    assert handle.root == rootdir


def test_init_with_config_include(tmpdir):
    rootdir = "/"
    dbpath = str(tmpdir)

    configfile = tmpdir.join("good.cfg")
    include_configfile = tmpdir.join("repos.cfg")

    configfile.write(CONFIG_WITH_INCLUDE.format(config=str(include_configfile)))
    include_configfile.write(INCLUDED_CONFIG.format(rootdir=rootdir, dbpath=dbpath))

    handle = init_with_config(str(configfile))

    assert handle.dbpath == dbpath + '/'
    assert handle.root == rootdir

    configfile.write(CONFIG_WITH_INCLUDE_SECTION.format(config=str(include_configfile)))
    include_configfile.write(INCLUDED_CONFIG.format(rootdir=rootdir, dbpath=dbpath))
    handle = init_with_config(str(configfile))

    assert handle.dbpath == dbpath + '/'
    assert handle.root == rootdir


class MockConfig:
    config = None
    root = "/"
    dbpath = "/tmp"
    gpgdir = "/"
    arch = "x86_64"
    logfile = "/var/log/pacman.log"
    cachedir = "/"
    debug = False


def test_init_with_options():
    options = MockConfig()
    handle = init_with_config_and_options(options)

    assert handle.dbpath == options.dbpath + '/'
    assert handle.root == options.root
