from setuptools import setup

setup(
    name='apollo',
    version='0.1',
    packages=['apollo'],
    entry_points={
        'console_scripts': [
            'apollo = apollo.__main__:main',
        ],
    },
)
