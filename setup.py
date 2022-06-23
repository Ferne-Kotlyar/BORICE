#!/usr/bin/env python
import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname), encoding='utf-8').read()

setup(
    name = "BORICE",
    version = "2.0",
    author = "Vanessa Koelling, Patrick Monnahan, John Kelly (modified by Ferne Kotlyar and Adrien Givry)",
    description = "BORICE is a free software to estimate the mean outcrossing rate and inbreeding coefficient of populations using Bayesian methods.",
    license = "GNU",
    keywords = "outcrossing research bayesian analysis inbreeding mating",
    packages=['borice', 'borice_gui', 'tests'],
    long_description=read('README.md'),
    classifiers=[
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
    entry_points={
        'console_scripts': [
            'borice = borice.__main__:main',
        ],
        'gui_scripts': [
            'borice_gui = borice_gui.__main__:main',
        ],
    },
)