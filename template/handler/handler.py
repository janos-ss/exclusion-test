import os

# TODO This class should have been a factory class for class Handler. This
# would allow no hack to avoid circular dependency and would result also
# in cleaner architecture

import re
anyNumberReg = re.compile(r"\d+(\.\d+)?")


class Handler:
    """ Abstract Handler class. Handler shares somes default, they can have special default by having a defaultclass attribute"""

    def __init__(self, mainComponent, options):
        self.mainComponent = mainComponent

        self.options = self.createOptions(options)

    def getValues(self):
        data = self.getInput()
        data = self.sanitize(data)
        return self.parseData(data)

    def sanitize(self, string):
        """Strip right part of the string. This is mainely necessary cause a lot of stuff feel the urge to add \n in the end (of file because editors put auto eol at end of file or in commands (echo for exemple) and since \n is the default separator it cause a lot of problems"""
        return string.rstrip()

    def getRows(self, data):
        return data.split(self.options['sep'])

    def parseData(self, data):
        """Read the input of the handler and return the list of row with ponderation. Also return if all the rows have same ponderation"""
        rows = self.getRows(data)
        res = []
        if self.options['equalweight']:
            for row in rows:
                value, ponderation = self.parseRow(row)
                res.append((value, 1.0))
            return res, len(rows), True

        else:

            ponderationSum = 0
            allEqual = True
            oldPonderation = self.parseRow(rows[0])[1]
            for row in rows:
                value, ponderation = self.parseRow(row)
                allEqual &= ponderation == oldPonderation
                oldPonderation = ponderation
                ponderationSum += ponderation
                res.append((value, ponderation))
            return res, ponderationSum, allEqual

    def parseRow(self, string):
        """Parse a row of input to get value and ponderation, return 1 as ponderation if ponderation not found or equalweight option """
        parts = string.split(self.options['sep2'], 1)
        if self.options['equalweight']:
            return parts[0], 1.0

        if len(parts) == 1:
            return parts[0], 1.0
        searchres = anyNumberReg.search(parts[1])
        if searchres == None:
            return parts[0], 1.0
        return parts[0], float(searchres.group())

    def getInput(self):
        raise NotImplementedError(
            'Error: Handler is an abstract class, you should instantiate a subclasse with the HandlerFactoryClass')

    def createOptions(self, options):
        # this default can reasonably be shared accross all handlers. If you
        # have name/value conflic define a default in your class
        communDefault = {'sep': '\n', 'sep2': ' ', 'equalweight': False}
        res = communDefault
        realclass = type(self)
        if getattr(realclass, 'default', None):
            res.update(realclass.default)
        if options:
            res.update(options)
        return res
