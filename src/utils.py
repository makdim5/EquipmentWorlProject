from flask import render_template, make_response


def to_html_resource(template, code=200, **kwargs):
    return make_response(render_template(template, **kwargs), code, {'Content-Type': 'text/html'})
