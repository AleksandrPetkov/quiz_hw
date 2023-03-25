from django import template

register = template.Library()


def negative(value):
    return -value


def multi(value, arg):
    return value * arg


# filter
def dived(value, arg):
    return value // arg


register.filter('negative', negative)
register.filter('multi', multi)
register.filter('dived', dived)