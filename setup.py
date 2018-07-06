from setuptools import setup, find_packages

__version__ = '0.1'


setup(
    name='thisdayinmusic',
    version=__version__,
    packages=find_packages(exclude=['tests']),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'thisdayinmusic = thisdayinmusic.manage:cli'
        ]
    }
)
