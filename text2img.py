from pygments import highlight
from pygments.formatters import ImageFormatter
from pygments.lexers import get_lexer_by_name


def draw_highlighted_text(text, lexer_name):
    """Take a string as input, return an image of the string."""
    return highlight(text, get_lexer_by_name(lexer_name), ImageFormatter(font_name='UbuntuMono'))
