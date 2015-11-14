from django.conf import settings

import os
import datetime
from math import log
import json


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
    # if os.path.exists(index_path):
    #     with open(index_path, 'rb') as f:
    #         return json.load(f)
    return generate_index(path)


def generate_index(path):
    index_path = get_index_path(path)
    index = dict(files={}, dirs={})
    for name in os.listdir(os.path.join(settings.MEDIA_ROOT, path)):
        fullpath = os.path.join(settings.MEDIA_ROOT, path, name)
        if os.path.isfile(fullpath):
            stat = os.stat(fullpath)
            index['files'][name] = dict(
                path=os.path.relpath(fullpath, settings.MEDIA_ROOT), 
                size=sizeof_fmt(stat.st_size), 
                modified=datetime.datetime.fromtimestamp(stat.st_mtime).isoformat(' ')[:16]
            )
        elif os.path.isdir(fullpath):
            index['dirs'][name] = dict()
    save_index(index, index_path)
    return index


def save_index(index, index_path):
    with open(index_path, 'wb') as f:
        json.dump(index, f, indent=4)


