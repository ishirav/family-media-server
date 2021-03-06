from django.conf import settings

import os
import datetime
from math import log
import json
import logging
import mimetypes

mimetypes.init()


unit_list = zip(['bytes', 'kB', 'MB', 'GB', 'TB', 'PB'], [0, 0, 1, 2, 2, 2])
def sizeof_fmt(num):
    """Human friendly file size"""
    if num > 1:
        exponent = min(int(log(num, 1024)), len(unit_list) - 1)
        quotient = float(num) / 1024**exponent
        unit, num_decimals = unit_list[exponent]
        format_string = '{:.%sf} {}' % (num_decimals)
        return format_string.format(quotient, unit)
    if num == 0:
        return '0 bytes'
    if num == 1:
        return '1 byte'


def get_index_path(path):
    return os.path.join(settings.MEDIA_ROOT, path, 'index.json')


def get_index(path):
    index_path = get_index_path(path)
    try:
        if os.path.exists(index_path):
            with open(index_path, 'rb') as f:
                return update_index(path, json.load(f))
    except:
        logging.exception('Problem with index for "%s"', path)
        pass
    return generate_index(path)


def generate_index(path):
    fullpath = os.path.join(settings.MEDIA_ROOT, path)
    logging.info('Generating index for %s', fullpath)
    index_path = get_index_path(path)
    index = dict(files={}, dirs={})
    for name in os.listdir(fullpath):
        add_to_index(path, name, index)
    save_index(index, index_path)
    return index


def update_index(path, index):
    fullpath = os.path.join(settings.MEDIA_ROOT, path)
    updated = False
    files, dirs = index['files'], index['dirs']
    names = set(os.listdir(fullpath))
    for name in names:
        if name not in files and name not in dirs:
            updated = add_to_index(path, name, index)
    for name in files.keys():
        if name not in names:
            del files[name]
            updated = True
    for name in dirs.keys():
        if name not in names:
            del dirs[name]
            updated = True
    if updated:
        logging.info('Updating index for %s', fullpath)
        save_index(index, get_index_path(path))
    return index


def add_to_index(path, name, index):
    fullpath = os.path.join(settings.MEDIA_ROOT, path, name)
    if os.path.isfile(fullpath):
        info = get_file_info(fullpath)
        if info:
            index['files'][name] = info
            return True
    elif os.path.isdir(fullpath):
        index['dirs'][name] = dict(type="directory")
        return True
    return False


def get_file_info(fullpath):
    type = mimetypes.guess_type(fullpath)[0]
    if not (type and ('image' in type or 'video' in type)):
        return None
    stat = os.stat(fullpath)
    return dict(
        size=sizeof_fmt(stat.st_size), 
        modified=datetime.datetime.fromtimestamp(stat.st_mtime).isoformat(' ')[:16],
        type=type
    )


def save_index(index, index_path):
    with open(index_path, 'wb') as f:
        json.dump(index, f, indent=4)
