import re


def is_alphanumeric(value):
    """Match letters, numbers, spaces and dashes only."""

    regex = r'^[a-zA-Z0-9\ \-]+$'
    regex = re.compile(regex)

    if regex.match(value):
        return True
    else:
        return False


def is_alpha(value):
    """Match letters, spaces, apostrophe and hyphens only."""

    regex = r'^[a-zA-ZàèìòùÀÈÌÒÙáéíóúýÁÉÍÓÚÝâêîôûÂÊÎÔÛãñõÃÑÕäëïöüÿÄËÏÖÜŸçÇßØøÅåÆæœ \'-]+$'

    if re.match(regex, value, re.UNICODE):
        return True
    else:
        return False
