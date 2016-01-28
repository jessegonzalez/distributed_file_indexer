try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

install_requires = [
    'redis',
    'rq',
]

tests_require = [
    'nose'
]

config = {
    'description': 'Simple Distributed File Indexer',
    'author': 'Jesse Gonzalez',
    'url': 'https://github.com/jessegonzalez/distributed_file_indexer',
    'author_email': 'jesse.gonzalez.jr@gmail.com',
    'version': '0.1',
    'install_requires': install_requires,
    'tests_require': tests_require,
    'test_suite': 'nose.collector',
    'packages': ['dfi'],
    'scripts': [],
    'name': 'dfi'
}

setup(**config)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
