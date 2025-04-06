from setuptools import setup, find_packages, Command
from setuptools.command.install import install
import shutil
import os
from src.utils.paths import *

class CleanKccSubmodule(Command):
    description = "Remove unused stuff from the Kcc submodule"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        submodule_path = os.path.join(src_dir(), 'external', 'kcc')

        unwanted_paths = [
            os.path.join(submodule_path, 'gui'),
            os.path.join(submodule_path, 'icons'),
            os.path.join(submodule_path, 'kindlecomicconverter', 'KCC_gui.py'),
            os.path.join(submodule_path, 'kindlecomicconverter', 'KCC_ui.py'),
            os.path.join(submodule_path, 'kindlecomicconverter', 'KCC_ui_editor.py'),
            os.path.join(submodule_path, 'kindlecomicconverter', 'KCC_rc.py'),
            os.path.join(submodule_path, '.dockerignore'),
            os.path.join(submodule_path, '.github'),
            os.path.join(submodule_path, '.gitignore'),
            os.path.join(submodule_path, 'setup.py'),
            os.path.join(submodule_path, 'Dockerfile'),
            os.path.join(submodule_path, 'AppImageBuilder.yml'),
            os.path.join(submodule_path, 'application-vnd.appimage.svg'),
            os.path.join(submodule_path, 'kcc.json'),
            os.path.join(submodule_path, 'gen_ui_files.sh'),
            os.path.join(submodule_path, 'gen_ui_files.bat'),
            os.path.join(submodule_path, 'environment.yml'),
            os.path.join(submodule_path, 'Dockerfile-base'),
            os.path.join(submodule_path, 'CHANGELOG.md'),
            os.path.join(submodule_path, 'kcc-c2e.spec'),
            os.path.join(submodule_path, 'kcc-c2p.spec'),
            os.path.join(submodule_path, 'kcc.spec'),
            os.path.join(submodule_path, 'README.md'),
            os.path.join(submodule_path, 'requirements.txt'),
            os.path.join(submodule_path, 'MANIFEST.in'),
            os.path.join(submodule_path, 'kcc.c2p.py')
        ]

        for path in unwanted_paths:
            if os.path.exists(path):
                if os.path.isdir(path):
                    shutil.rmtree(path)
                else:
                    os.remove(path)
                print(f"Deleted: {path}")
            else:
                print(f"Path not found: {path}")



class InstallCommand(install):
    def run(self):
        install.run(self)

        self.run_command("clean_kcc")

setup(
    name="comic-compiler",
    version="1.1",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.7, <4",
    keywords=['comic', 'manga', 'epub', 'pdf'],
    cmdclass={
        "install": InstallCommand,
        "clean_kcc": CleanKccSubmodule
    },
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
            "comic-compile=main:main",
        ],
    },
     project_urls={
        "Bug Reports": "https://github.com/mr-noobish/comic-compiler/issues",
        "Source": "https://github.com/mr-noobish/comic-compiler",
    },
)