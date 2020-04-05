from django import template

register = template.Library()


@register.filter(name='subtract')
def subtract(value, arg):
    return value - arg

@register.simple_tag
def setvar(val=None):
  return val

@register.filter(name='split')
def split(value):
    return value.split(',')