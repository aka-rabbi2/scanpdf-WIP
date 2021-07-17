from django import template
register = template.Library()

@register.filter
def to_float(value):
    """converts int to string"""
    return float( value.replace(',','') )