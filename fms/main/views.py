from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import Http404

from index import get_index, generate_index


def get_path(request):
    parts = [part for part in request.path.split('/') if part]
    if '..' in parts:
        raise Http404
    path = '/'.join(parts[1:]) + '/'
    if path == '/':
        path = ''
    print 'PATH: "%s"' % path
    return path


def get_breadcrumbs(path):
    breadcrumbs = []
    parts = ('home/' + path).split('/')[:-1]
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
    mode = request.GET.get('mode', 'list')
    return render(request, 'directory.html', locals())


@login_required
def refresh_view(request):
    path = get_path(request)
    generate_index(path)
    mode = request.GET.get('mode', 'list')
    return redirect('/root/%s?mode=%s' % (path, mode))


def home_view(request):
    return redirect('/root/')

