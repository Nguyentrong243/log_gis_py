from django import template
import locale

register = template.Library()

@register.filter
def currency(value):
    """Format number as Vietnamese currency with dots"""
    try:
        # Set locale to Vietnamese
        locale.setlocale(locale.LC_ALL, 'vi_VN.UTF-8')
        return locale.currency(value, grouping=True, symbol='đ').replace('₫', 'đ')
    except:
        # Fallback: format manually
        if isinstance(value, (int, float)):
            s = f"{int(value):,}".replace(",", ".")
            return f"{s}đ"
        return f"{value}đ"