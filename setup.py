from setuptools import setup, find_packages

VERSION = (1, 0, 0, 'dev')

setup(
    name = "sambandid",
    version = ".".join(map(str, VERSION)),
    url = 'http://bjor.sambandid.is',
    license = 'BSD',
    description = "Beer fridge management system. In Icelandic.",
    author = 'Gagnavarslan',
    packages = find_packages('.'),
    package_dir = {'': '.'},
    include_package_data = True,
    zip_safe = False,
    setup_requires = ['setuptools_git'],
    install_requires = ['setuptools'],
)