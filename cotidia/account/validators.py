import re


#
# Contains letters, numbers, spaces and dashes only
#
def is_alphanumeric(value):
    regex = r'^[a-zA-Z0-9\ \-]+$'
    regex = re.compile(regex)

    if regex.match(value):
        return True
    else:
        return False


#
# Contains letters, spaces and dashes only
#
def is_alpha(value):
    regex = r'^[a-zA-Z\ \-]+$'
    regex = re.compile(regex)

    if regex.match(value):
        return True
    else:
        return False
