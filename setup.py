from setuptools import setup, find_packages

setup(
    name='apollo',
    version='0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'apollo = apollo.__main__:main',
        ],
    },
)
