# -*- coding: utf-8 -*-
#
from codex.baseview import BaseView
from test_me import settings

from django.http import HttpResponse, Http404

import logging
import mimetypes
import os


__author__ = "Epsirom"


class FileView(BaseView):

    logger = logging.getLogger('Static')

    def get_file(self, fpath):
        if os.path.isfile(fpath):
            return open(fpath, 'rb').read()
        else:
            return None

    def cut_url_prefix(self, url, prefix):
        url = url[len(prefix)-1:];

    def do_dispatch(self, *args, **kwargs):
        rpath = self.request.path.replace('..', '.').strip('/')
        if '__' in rpath:
            raise Http404('Could not access private static file: ' + self.request.path)
        root = settings.STATIC_ROOT
        url_prefix = settings.STATIC_URL
        if rpath.startswith(('media/')):
            root = settings.MEDIA_ROOT
            url_prefix = settings.MEDIA_URL
        self.cut_url_prefix(rpath, url_prefix)
        content = self.get_file(os.path.join(root, rpath))
        if content is not None:
            return HttpResponse(content, content_type=mimetypes.guess_type(rpath)[0])
        content = self.get_file(os.path.join(root, rpath + '/index.html'))
        if content is not None:
            return HttpResponse(content, content_type=mimetypes.guess_type(rpath + '/index.html')[0])
        raise Http404('Could not found static file: ' + self.request.path)
