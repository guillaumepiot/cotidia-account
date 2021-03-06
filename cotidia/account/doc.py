import os
import json

from cotidia.account.conf import settings

class Doc():

    def init_file(self, file_name, title):

        self.file_path = os.path.join(
            settings.BASE_DIR, '../docs/api/{0}'.format(file_name))

        self.file_handle = open(self.file_path, 'w')
        self.file_handle.write(
            "# {0}\n"
            "\n".format(title))
        # self.close()

    def write_section(self, content):

        payload = json.dumps(content['payload'], indent=4)
        response = json.dumps(content['response'], indent=4)
        response_status = content.get('response_status', "")

        self.file_handle = open(self.file_path, 'a')

        if content.get('description', ''):
            description = (
                "\n"
                "{0}\n"
                "\n"
                ).format(content['description'])
        else:
            description = ''

        self.file_handle.write(
            "## {0}\n"
            "\n"
            "    [{7}] {1}{2}\n"
            "{6}"
            "\n"
            "### Payload\n"
            "\n"
            "```json\n"
            "{3}\n"
            "```\n"
            "\n"
            "### Response\n"
            "\n"
            "Status: {4}"
            "\n"
            "```json\n"
            "{5}\n"
            "```\n".format(
                content['title'],
                settings.SITE_URL,
                content['url'],
                payload,
                response_status,
                response,
                description,
                content['http_method']
                )
            )

    def display_section(self, content):

        payload = json.dumps(content['payload'], indent=4)
        response = json.dumps(content['response'], indent=4)
        response_status = content.get('response_status', "")

        if content.get('description', ''):
            description = (
                "\n"
                "{0}\n"
                "\n"
                ).format(content['description'])
        else:
            description = ''

        print(
            "## {0}\n"
            "\n"
            "    [{7}] {1}{2}\n"
            "{6}"
            "\n"
            "### Payload\n"
            "\n"
            "```json\n"
            "{3}\n"
            "```\n"
            "\n"
            "### Response\n"
            "\n"
            "Status: {4}"
            "\n"
            "```json\n"
            "{5}\n"
            "```\n".format(
                content['title'],
                settings.SITE_URL,
                content['url'],
                payload,
                response_status,
                response,
                description,
                content['http_method']
                )
            )


    def close(self):
        self.file_handle.close()
