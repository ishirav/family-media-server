from thumbor.loaders import LoaderResult
from datetime import datetime
from os import fstat
from os.path import join, exists, abspath
from urllib import unquote
from tornado.concurrent import return_future
import mimetypes

mimetypes.init()


@return_future
def load(context, path, callback):
    file_path = join(context.config.FILE_LOADER_ROOT_PATH.rstrip('/'), unquote(path).lstrip('/'))
    file_path = abspath(file_path)
    inside_root_path = file_path.startswith(context.config.FILE_LOADER_ROOT_PATH)

    result = LoaderResult()

    if inside_root_path and exists(file_path):

        if is_video(file_path):
            file_path = get_video_frame(context, file_path)

        with open(file_path, 'r') as f:
            stats = fstat(f.fileno())

            result.successful = True
            result.buffer = f.read()

            result.metadata.update(
                size=stats.st_size,
                updated_at=datetime.utcfromtimestamp(stats.st_mtime)
            )
    else:
        result.error = LoaderResult.ERROR_NOT_FOUND
        result.successful = False

    callback(result)


def is_video(file_path):
    type = mimetypes.guess_type(file_path)[0]
    return type and type.startswith('video')


def get_video_frame(context, file_path):
    import subprocess, tempfile, os
    f, outfile = tempfile.mkstemp('.jpg')
    os.close(f)
    cmd = [
        context.config.FFMPEG_PATH,
        '-i', file_path,
        '-ss', '00:00:01.000',
        '-vframes', '1',
        '-y',
        outfile
    ]
    subprocess.call(cmd)
    return outfile
