from setuptools import setup

setup(
    name="comic-compiler",
    version="1.0",
    py_modules=["main"],
    entry_points={
        "console_scripts": [
            "comic-compile=main:main",
        ],
    },
)