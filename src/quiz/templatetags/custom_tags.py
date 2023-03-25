from django import template

register = template.Library()


def expression(value, *args):
    for idx, arg in enumerate(args, 1):
        value = value.replace(f'%{idx}', str(arg))
    return eval(value)


register.simple_tag(func=expression, name='expression')
