import os

def project_root():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

def config_dir():
    return os.path.join(src_dir(), 'comic_compiler', 'config')

def src_dir():
    return os.path.join(project_root(), 'src')