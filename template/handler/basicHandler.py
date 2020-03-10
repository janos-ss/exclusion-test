from template.handler.handler import Handler


class BasicHandler(Handler):

    def __init__(self, mainComponent, options, values):
        Handler.__init__(self, mainComponent, options)
        if type(values) != list:
            values = [values]
        self.values = values

    def getValues(self):
        return self.values
