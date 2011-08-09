from werkzeug import Request, Response
from werkzeug.exceptions import HTTPException

from g import BaseG


class BaseApplication(object):
    response_cls = Response
    request_cls = Request
    template_adapter = None
    settings_cls = None

    def __init__(self, settings):
        self.settings = self.settings_cls(settings)
        self.url_map = self.settings.get('URL_MAP', imp=True)
        self.g_cls = self.get_g_cls()

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)

    def get_response(self, view, g, **kw):
        return view(g, **kw)

    def wsgi_app(self, environ, start_response):
        g = self.g_cls(environ)

        try:
            endpoint, values = g.urls.match()
            view = g.urls.map.get_view(endpoint)
            response = self.get_response(view, g, **values)
        except HTTPException as e:
            response = e
        else:
            if hasattr(g, 'save'):
                g.save(response)

        return response(environ, start_response)

    def get_g_cls(self):
        
        class G(BaseG):
            settings = self.settings
            url_map = self.url_map
            request_cls = self.request_cls

            if self.template_adapter:
                templates = self.template_adapter(
                    self.settings,
                    response_cls=self.response_cls
                )

        return G


Application = BaseApplication  # compat.

