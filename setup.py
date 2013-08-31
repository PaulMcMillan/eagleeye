#!/usr/bin/env python
from setuptools import setup, find_packages

version = '0.1.2'

setup(
    name="eagleeye_te",
    version=version,
    description="Distributed tool for screenshotting webpages.",
    long_description=open("README.rst").read(),
    url='https://github.com/PaulMcMillan/eagleeye',
    license="Simplified BSD",
    author="Paul McMillan",
    author_email="paul@mcmillan.ws",

    entry_points={
        'console_scripts': [
            'eagleeye = eagleeye.cli:run',
            ],
        },

    install_requires=[
        "tasa",
        "selenium",
        "pyvirtualdisplay",
        "requests",
        ],
    extras_require={
        "tests": [
            "pep8",
            "pylint",
            "pytest",
            "pytest-cov",
            ],
        },
    tests_require=[
        "pep8",
        "pytest",
        "pytest-cov",
        ],

    packages=find_packages(),

    classifiers=[
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ])



