import re


def get_confirmation_url_from_email(email_message):
    exp = r'(\/activate\/([a-z0-9\-]+)\/([a-z0-9\-]+))\/'
    m = re.search(exp, email_message)
    confirmation_url = m.group()
    user_uuid = m.group(2)
    confirmation_code = m.group(3)

    return confirmation_url, user_uuid, confirmation_code


def get_reset_url_from_email(email_message):
    exp = r'(\/reset-password\/([a-z0-9\-]+)\/([a-z0-9\-]+))\/'
    m = re.search(exp, email_message)
    reset_url = m.group()
    user_uuid = m.group(2)
    reset_code = m.group(3)

    return reset_url, user_uuid, reset_code
