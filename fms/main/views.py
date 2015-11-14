from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required

from index import get_index


@login_required
def directory_view(request):
    parts = request.path.split('/')[:-1]
    path = '/'.join(parts[2:])
    index = get_index(path)
    sorted_dirs = sorted(index['dirs'].items())
    sorted_files = sorted(index['files'].items())
    sorted_all = sorted_dirs + sorted_files
    thumbor_server = settings.THUMBOR_SERVER
    mode = request.GET.get('mode', 'list')
    return render(request, 'directory.html', locals())


def home_view(request):
    return redirect('/root/')

