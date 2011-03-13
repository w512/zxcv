'''Utilities for zxcv-powered applications.'''


DEFAULT_TEST_COOKIE_NAME = 't'
DEFAULT_TEST_COOKIE_VALUE = 'w'


def _get_test_cookie_name(g):
    return g.settings.get('TEST_COOKIE_NAME', DEFAULT_TEST_COOKIE_NAME)


def _get_test_cookie_settings(g):
    name = _get_test_cookie_name(g)
    value = g.settings.get('TEST_COOKIE_VALUE', DEFAULT_TEST_COOKIE_VALUE)
    return name, value


def set_test_cookie(g):
    name, value = _get_test_cookie_settings(g)
    g.session[name] = value


def delete_test_cookie(g):
    name = _get_test_cookie_name(g)
    del g.session[name]


def check_test_cookie(g):
    name, value = _get_test_cookie_settings(g)
    return g.session.get(name) == value

