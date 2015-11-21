from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse

import json
import logging
import os

from index import get_index, generate_index
from path_utils import drop_path_base, delete_any, copy_any


def get_path(request):
    parts = [part for part in request.path.split('/') if part]
    if '..' in parts:
        raise Http404
    path = '/'.join(parts[1:]) + '/'
    if path == '/':
        path = ''
    return path


def verify_path(path):
    path = os.path.normpath(path)
    if not path.startswith(settings.MEDIA_ROOT):
        logging.error('Blocked access to invalid path: "%s"', path)
        raise Http404


def get_breadcrumbs(path):
    breadcrumbs = []
    parts = ('Home/' + path).split('/')[:-1]
    level = 0
    for part in reversed(parts):
        path = '../' * level
        breadcrumbs.append(dict(name=part, path=path))
        level += 1
    return reversed(breadcrumbs)


@login_required
def directory_view(request):
    path = get_path(request)
    breadcrumbs = get_breadcrumbs(path)
    index = get_index(path)
    sorted_dirs = sorted(index['dirs'].items())
    sorted_files = sorted(index['files'].items())
    sorted_all = sorted_dirs + sorted_files
    thumbor_server = settings.THUMBOR_SERVER
    mode = request.GET.get('mode', 'grid')
    return render(request, 'directory.html', locals())


@login_required
def refresh_view(request):
    path = get_path(request)
    generate_index(path)
    mode = request.GET.get('mode', 'grid')
    return redirect('/home/%s?mode=%s' % (path, mode))


@login_required
def cut_or_copy_view(request):
    try:
        data = json.loads(request.body)
        request.session['clipboard'] = data
    except:
        logging.exception('Error in cut_or_copy_view')
        return HttpResponse('Operation failed.')
    return HttpResponse('')


@login_required
def paste_view(request):
    from shutil import move
    data = request.session.get('clipboard', {})
    paths = data.get('paths', [])
    if not paths:
        return HttpResponse('Your clipboard is empty.')
    mode = data.get('mode', 'copy')
    method = copy_any if mode == 'copy' else move
    try:
        target_dir = os.path.join(settings.MEDIA_ROOT, get_path(request))
        for path in paths:
            source_path = os.path.join(settings.MEDIA_ROOT, drop_path_base(path))
            verify_path(source_path)
            file_name = [part for part in path.split('/') if part][-1]
            target_path = os.path.join(target_dir, file_name)
            while os.path.exists(target_path):
                file_name = '_' + file_name
                target_path = os.path.join(target_dir, file_name)
            verify_path(target_path)
            method(source_path, target_path)
    except Exception, e:
        logging.exception('Error in paste_view')
        return HttpResponse(unicode(e))
    request.session['clipboard'] = {}
    return HttpResponse('')


@login_required
def delete_view(request):
    try:
        data = json.loads(request.body)
        for path in data['paths']:
            full_path = os.path.join(settings.MEDIA_ROOT, drop_path_base(path))
            verify_path(full_path)
            delete_any(full_path)
    except Exception, e:
        logging.exception('Error in delete_view')
        return HttpResponse(unicode(e))
    return HttpResponse('')


@login_required
def new_folder_view(request):
    try:
        data = json.loads(request.body)
        name = data.get('name') or 'New Folder'
        target_dir = os.path.join(settings.MEDIA_ROOT, get_path(request), name)
        verify_path(target_dir)
        os.mkdir(target_dir)
    except Exception, e:
        logging.exception('Error in new_folder_view')
        return HttpResponse(unicode(e))
    return HttpResponse('')


def home_view(request):
    return redirect('/home/')

