#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

# Read requirements
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

# Read the README file for the long description
with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="mp4-to-mp3-tool",
    version="0.1.0",
    description="A tool to convert MP4 videos to MP3 audio files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="MP4 to MP3 Converter Contributors",
    author_email="example@example.com",
    url="https://github.com/sawyer-shi/mp4-to-mp3-tool",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "mp4-to-mp3=app:main",
        ],
    },
) 