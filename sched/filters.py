from jinja2 import Markup, evalcontextfilter, escape
from datetime import datetime

def init_app(app):
    app.jinja_env.filters['date'] = do_date
    app.jinja_env.filters['datetime'] = do_datetime
    app.jinja_env.filters['duration'] = do_duration
    app.jinja_env.filters['nl2br'] = evalcontextfilter(do_nl2br)


def do_datetime(dt, format=None):
    """
    >>> do_datetime(None)
    ''
    
    >>> do_datetime(datetime(1990, 07, 01, 07, 06, 00))
    '1990-07-01 - Sunday at 7:06am'
    """
    if dt is None:
        return ''
    if format is None:
        formatted_date = dt.strftime('%Y-%m-%d - %A')
        formatted_time = dt.strftime('%I:%M%p').lstrip('0').lower()
        formatted = '%s at %s' % (formatted_date, formatted_time)
    else:
        formatted = dt.strftime(format)
    return formatted


def do_date(dt, format='%Y-%m-%d - %A'):
    """
    >>> do_date(None)
    ''

    >>> do_datetime(datetime(1990, 07, 01, 07, 06, 00))
    '1990-07-01 - Sunday at 7:06am'
    """
    if dt is None:
        return ''
    return dt.strftime(format)


def do_duration(seconds):
    """
    >>> do_duration(1080)
    '18 minutes'
    
    >>> do_duration(259578)
    '3 days, 6 minutes, 18 seconds'
    """
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    tokens = []
    if d > 1:
        tokens.append('{d} days')
    elif d:
        tokens.append('{d} day')
    if h > 1:
        tokens.append('{h} hours')
    elif h:
        tokens.append('{h} hour')
    if m > 1:
        tokens.append('{m} minutes')
    elif m:
        tokens.append('{m} minute')
    if s > 1:
        tokens.append('{s} seconds')
    elif s:
        tokens.append('{s} second')
    template = ', '.join(tokens)
    return template.format(d=d, h=h, m=m, s=s)


def do_nl2br(context, value):
    formatted = u'<br />'.join(escape(value).split('\n'))
    if context.autoescape:
        formatted = Markup(formatted)
    return formatted

if __name__ == '__main__':  # pragma: no cover
    import doctest
    doctest.testmod()
