from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required

from index import get_index, generate_index


@login_required
def directory_view(request):
    parts = [part for part in request.path.split('/') if part]
    path = '/'.join(parts[1:])
    index = get_index(path)
    sorted_dirs = sorted(index['dirs'].items())
    sorted_files = sorted(index['files'].items())
    sorted_all = sorted_dirs + sorted_files
    thumbor_server = settings.THUMBOR_SERVER
    mode = request.GET.get('mode', 'list')
    return render(request, 'directory.html', locals())


@login_required
def refresh_view(request):
    parts = [part for part in request.path.split('/') if part]
    path = '/'.join(parts[1:])
    generate_index(path)
    mode = request.GET.get('mode', 'list')
    return redirect('/root/%s?mode=%s' % (path, mode))


def home_view(request):
    return redirect('/root/')

