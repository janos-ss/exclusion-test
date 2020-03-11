from template.handler.handler import Handler


class BasicHandler(Handler):

    def __init__(self, mainComponent, options, dico):
        Handler.__init__(self, mainComponent, options)
        values = dico[mainComponent]
        if type(values) != list:
            values = [values]
        self.values = values

    def getValues(self):
        return self.values
