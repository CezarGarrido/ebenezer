# core/views/media.py

import mimetypes
from django.http import HttpResponse, Http404
from django.conf import settings
import os

def serve_media(request, path):
    full_path = os.path.join(settings.MEDIA_ROOT, path)

    if not os.path.isfile(full_path):
        raise Http404("Arquivo não encontrado")

    with open(full_path, 'rb') as f:
        file_data = f.read()

    content_type, _ = mimetypes.guess_type(full_path)
    return HttpResponse(file_data, content_type=content_type or 'application/octet-stream')
