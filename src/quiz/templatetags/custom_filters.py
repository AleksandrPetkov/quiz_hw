from django import template

register = template.Library()


def negative(value):
    return -value


def multi(value, arg):
    return value * arg


# filter
def dived(value, arg):
    return value // arg


def get_point_sum(correct, incorrect):
    point = correct - incorrect
    if point > 0:
        return point
    return 0


register.filter('negative', negative)
register.filter('multi', multi)
register.filter('dived', dived)
register.filter('get_ppoint_sum', get_point_sum)
