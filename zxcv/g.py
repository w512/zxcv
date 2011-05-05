from werkzeug.utils import cached_property
from werkzeug.contrib.securecookie import SecureCookie


class BaseG(object):

    def __init__(self, environ):
        # Is called for every request.
        self.urls = self.get_url_adapter(environ)
        self.request = self.request_cls(environ)
        self.templates.set_template_global('g', self)

    def get_url_adapter(self, environ):
        return self.url_map.bind_to_environ(environ)

    @cached_property
    def session(self):
        '''Return current signed cookie-based session.

        Allow to change SECRET_KEY more often by supporting
        old SECRET_KEYs.
        
        '''
        cls = SecureCookie
        old_keys = getattr(self.settings, 'OLD_SECRET_KEYS', None)
        key = self.settings.SESSION_COOKIE_NAME
        secret_key = self.settings.SESSION_COOKIE_SECRET
        
        data = self.request.cookies.get(key)
        
        if not data:
            return cls(secret_key=secret_key)
        
        decoded = cls.unserialize(data, secret_key)

        if not old_keys:
            return decoded
        
        if not decoded:
            old_decoded = None

            # Try old keys and convert data with new one.
            for old_key in old_keys:
                _decoded = cls.unserialize(data, old_key)
                if _decoded:
                    old_decoded = _decoded

            if old_decoded is None:
                return cls(secret_key=secret_key)

            decoded.update(old_decoded)

        return decoded
    
    def save(self, response):
        self.session.save_cookie(
            response,
            domain=self.settings.get('SESSION_COOKIE_DOMAIN', None),
            key=self.settings.SESSION_COOKIE_NAME,
            max_age=self.settings.SESSION_COOKIE_MAX_AGE,
            secure=self.settings.SESSION_COOKIE_SECURE,
            httponly=self.settings.SESSION_COOKIE_HTTP_ONLY
        )

