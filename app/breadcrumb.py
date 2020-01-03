import functools
import collections
import flask

BreadCrumb = collections.namedtuple('BreadCrumb', ['path', 'title'])


def breadcrumb(view_title):
    def decorator(f):
        @functools.wraps(f)
        def decorated_function(*args, **kwargs):
            flask.g.title = view_title
            session_crumbs = flask.session.setdefault('crumbs', [])
            flask.g.breadcrumbs = []
            for path, title in session_crumbs:
                flask.g.breadcrumbs.append(BreadCrumb(path, title))
            rv = f(*args, **kwargs)
            flask.session.modified = True
            session_crumbs.append((flask.request.path, view_title))
            if len(session_crumbs) > 5:
                session_crumbs.pop(0)
            return rv
        return decorated_function
    return decorator