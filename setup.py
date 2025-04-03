from setuptools import setup, find_packages

setup(
    name="comic-compiler",
    version="1.0",
    packages=find_packages(where='src'),
    entry_points={
        "console_scripts": [
            "comic-compile=main:main",
        ],
    },
)