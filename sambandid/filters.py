from sambandid import app


def datetimeformat(value):
    return value.strftime('%d.%m.%y %H:%M')

app.jinja_env.filters['datetimeformat'] = datetimeformat



