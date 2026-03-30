from django import template
import locale

register = template.Library()

@register.filter
def currency(value):
    """Format number as Vietnamese currency (1.000.000,00 đ)"""
    try:
        from decimal import Decimal
        v = Decimal(value)
        v = v.quantize(Decimal('0.01'))

        # US style: 1,234,567.89
        formatted = f"{v:,.2f}"
        # Convert to Vietnamese style: 1.234.567,89
        formatted = formatted.replace(',', 'X').replace('.', ',').replace('X', '.')

        # Strip .00 decimals when whole number (optional)
        if formatted.endswith(',00'):
            formatted = formatted[:-3]

        return f"{formatted}đ"
    except Exception:
        try:
            iv = int(value)
            s = f"{iv:,}".replace(',', '.')
            return f"{s}đ"
        except Exception:
            return f"{value}đ"