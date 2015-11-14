from django.shortcuts import render, redirect
from django.conf import settings

from index import get_index


def directory_view(request):
    parts = request.path.split('/')[:-1]
    path = '/'.join(parts[2:])
    index = get_index(path)
    sorted_dirs = sorted(index['dirs'].items())
    sorted_files = sorted(index['files'].items())
    thumbor_server = settings.THUMBOR_SERVER
    return render(request, 'directory.html', locals())


def home_view(request):
    return redirect('/root/')
    
