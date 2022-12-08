from pathlib import Path

def set(name, dir='data'):
    path = dir.removesuffix('/') + '/' + name
    if not Path(path).exists():
        Path(path).touch()
    else:
        raise FileExistsError

def exists(name, dir='data'):
    path = dir.removesuffix('/') + '/' + name
    if Path(path).exists():
        return True
    else:
        return False

def rm(name, dir='data'):
    path = dir.removesuffix('/') + '/' + name
    if Path(path).exists():
        Path(path).unlink()
    else:
        raise FileNotFoundError
