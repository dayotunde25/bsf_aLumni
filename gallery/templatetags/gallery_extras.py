from django import template

register = template.Library()

@register.filter(name='endswith')
def endswith(value, arg):
    """
    Custom template filter to check if a string ends with a specific substring.
    """
    return str(value).endswith(arg)
