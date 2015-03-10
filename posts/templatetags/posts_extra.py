from django import template
import CommonMark

register = template.Library()


@register.filter(name='commonmark', is_safe=True)
def markup(var):
    """Parse the input to commonmark format in template files

    This can be used like so:
    {{ some_string|commmonmark|safe }}

    As long as you {% load posts_extra %}

    """
    parser = CommonMark.DocParser()
    renderer = CommonMark.HTMLRenderer()
    ast = parser.parse(var)
    return renderer.render(ast)