from django import template

register = template.Library()


@register.filter(name='get')
def get(_dict, key):
	return _dict[key]
