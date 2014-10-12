from jinja2 import Markup, evalcontextfilter, escape


def init_app(app):
    app.jinja_env.filters['date'] = do_date
    app.jinja_env.filters['datetime'] = do_datetime
    app.jinja_env.filters['duration'] = do_duration
    app.jinja_env.filters['nl2br'] = evalcontextfilter(do_nl2br)


def do_datetime(dt, format=None):
    """
    >>> do_datetime(None)
    ''
    >>> from datetime import datetime
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

    >>> from datetime import datetime
    >>> do_date(datetime(1990, 07, 01, 07, 06, 00))
    '1990-07-01 - Sunday'
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
    tokens.append(Dia(d))
    tokens.append(Hora(h))
    tokens.append(Minuto(m))
    tokens.append(Segundo(s))
    template = ', '.join(tokens)
    return template.format(d=d, h=h, m=m, s=s)


def Dia(d):
    if(d > 1):
        return '{d} days'
    return '{d} day'


def Hora(h):
    if(h > 1):
        return '{h} hours'
    return '{h} hour'


def Minuto(m):
    if(m > 1):
        return '{m} minutes'
    return '{m} minute'


def Segundo(s):
    if(s > 1):
        return '{s} seconds'
    return '{s} second'


def do_nl2br(context, value):
    formatted = u'<br />'.join(escape(value).split('\n'))
    if context.autoescape:
        formatted = Markup(formatted)
    return formatted

if __name__ == '__main__':  # pragma: no cover
    import doctest
    doctest.testmod()
