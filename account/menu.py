class Menu(object):

    def __init__(self):
        self._registry = {}

    def register(self, title, template):
        self._registry[title] = template

    def items(self):
        item_list = []
        for key, value in self._registry.iteritems():
            item_list.append(value)
        return item_list

menu = Menu()
