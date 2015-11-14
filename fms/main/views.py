from django.shortcuts import render

from index import get_index


def directory_view(request):
    parts = request.path.split('/')
    path = '/'.join(parts[2:])
    index = get_index(path)
    return render(request, 'directory.html', locals())

