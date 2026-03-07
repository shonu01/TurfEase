from django import template
from datetime import date

register = template.Library()


@register.filter
def is_future_date(value):
    """Returns True if the date is today or in the future."""
    if isinstance(value, date):
        return value >= date.today()
    return False
