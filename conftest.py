# empty file to trick py.test into adding the root folder to sys.path
# see https://github.com/pytest-dev/pytest/issues/911 for more info

try:
    import setuptools
except ImportError:
    # if setuptools is not available we register
    # the plugin manually.
    pytest_plugins = "xonsh.pytest_plugin",

