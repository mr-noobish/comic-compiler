from setuptools import setup, find_packages


setup(
    name="comic-compiler",
    version="1.1",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.7, <4",
    keywords=['comic', 'manga', 'epub', 'pdf'],
    install_requires=[
        'PyPDF2',
        'Pillow>=5.2.0',
        'psutil>=5.9.5',
        'python-slugify>=1.2.1,<9.0.0',
        'raven>=6.0.0',
        'requests>=2.31.0',
        'mozjpeg-lossless-optimization>=1.1.2',
        'natsort>=8.4.0',
        'distro',
        'numpy>=1.22.4,<2.0.0'
    ],
    entry_points={
        "console_scripts": [
            "comic-compile=comic_compiler.main:main",
        ],
    },
     project_urls={
        "Bug Reports": "https://github.com/mr-noobish/comic-compiler/issues",
        "Source": "https://github.com/mr-noobish/comic-compiler",
    },
)