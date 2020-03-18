from template.handler.handler import Handler


class BasicHandler(Handler):

    def __init__(self, mainComponent, options, dico):
        Handler.__init__(self, mainComponent, options)
        values = dico[mainComponent]
        if type(values) != list:
            values = [values]
        self.values = values

    def getInput(self):
        return self.values

    def getRows(self, data):
        """For the basic handler user give the rows directely"""
        return data

    def sanitize(self, values):
        """For basic handler there is nothing to sanitize"""
        return values

    def parseRow(self, row):
        """The basic handler take either tuple or string as entry."""
        if type(row) == tuple:
            return row[0], row[1]
        else:
            return row, 1.0
