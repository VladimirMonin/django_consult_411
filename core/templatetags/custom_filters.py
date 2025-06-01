from django import template
import markdown

from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def md_html(md_string):
    """
    Конвертирует Markdown в HTML.
    :param md_string: Строка в формате Markdown.
    :return: HTML-строка.
    """
    if not md_string:
        return ''
    
    # Создаем экземпляр Markdown с нужными расширениями
    md = markdown.Markdown(extensions=['fenced_code', 'codehilite', 'tables'])
    
    # Конвертируем Markdown в HTML
    html = md.convert(md_string)
    
    # Возвращаем HTML как безопасную строку
    return mark_safe(html)