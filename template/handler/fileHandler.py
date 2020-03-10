from template.handler.handler import Handler


class FileHandler(Handler):

    def getValues(self):
        with open(self.mainComponent, 'r') as f:
            return f.read().split(self.options['sep'])
