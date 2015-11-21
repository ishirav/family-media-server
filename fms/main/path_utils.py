import os


def copy_any(source_path, target_path):
    '''
    Copy a file or directory
    '''
    from shutil import copy2, copytree
    if os.path.isdir(source_path):
        copytree(source_path, target_path)
    else:
        copy2(source_path, target_path)


def delete_any(path):
    '''
    Delete a file or directory
    '''
    from shutil import rmtree
    if os.path.exists(path):
        if os.path.isdir(path):
            rmtree(path)
        else:
            os.remove(path)


def drop_path_base(path):
    '''
    Removes the first segment of a given path.
    '''
    if path[0] == '/':
        path = path[1:]
    return '/'.join(path.split('/')[1:])
