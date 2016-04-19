import importlib
import os
import json

from django.conf import settings
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.apps import apps

from account import settings as account_settings

#
# Allow permission checking for class based views
#

class UserCheckMixin(object):

    def check_user(self, user):
        return True

    def dispatch(self, request, *args, **kwargs):
        if not self.check_user(request.user):
            if request.user.is_authenticated():
                raise PermissionDenied
            else:
                return redirect(account_settings.ADMIN_LOGIN_URL)
        return super(UserCheckMixin, self).dispatch(request, *args, **kwargs)


class StaffPermissionRequiredMixin(UserCheckMixin):
    permission_required = None

    #
    # The user must be staff and have the required permissions
    #
    def check_user(self, user):
        if user.is_superuser:
            return True
        return user.is_staff and user.has_perm(self.permission_required)

#
# Import a model using a dotted string value
#
def import_model(name, clsName):
    module = importlib.import_module(name)
    return getattr(module, clsName)


#
# Send the user activation email
#
def send_activation_email(user):
    from django.contrib.auth.tokens import default_token_generator
    from account.notices import NewUserActivationNotice

    token = default_token_generator.make_token(user)
    url = reverse('account-public:activate', kwargs={
        'uuid':user.uuid,
        'token':token
        })


    notice = NewUserActivationNotice(
        recipients = ['%s <%s>' % (user.get_full_name(), user.email) ],
        context = {
            'url':"%s%s" % (settings.SITE_URL, url),
            'first_name':user.first_name
        }
    )
    notice.send(force_now=True)


class Doc():

    def __init__(self, file_name, title):
        
        self.file_path = os.path.join(
            settings.PROJECT_DIR, '../../docs/api/{0}'.format(file_name))
        
        self.file_handle = open(self.file_path, 'w')
        self.file_handle.write(
            "# {0}\n"
            "\n".format(title))
        # self.close()

    def write_section(self, content):

        payload = json.dumps(content['payload'], indent=4)
        response = json.dumps(content['response'], indent=4)

        self.file_handle = open(self.file_path, 'a')
        self.file_handle.write(
            "## {0}\n"
            "\n"
            "    [{6}] {1}{2}\n"
            "\n"
            "{5}\n"
            "\n"
            "\n"
            "### Payload\n"
            "\n"
            "```json\n"
            "{3}\n"
            "```\n"
            "\n"
            "### Response\n"
            "\n"
            "```json\n"
            "{4}\n"
            "```\n".format(
                content['title'], 
                settings.SITE_URL, 
                content['url'], 
                payload, 
                response,
                content.get('description', ''),
                content['http_method']
                )
            )
        # self.close()

    def close(self):
        self.file_handle.close()