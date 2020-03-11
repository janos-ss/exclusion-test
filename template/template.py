# Need to e as it is to be able to monkey patch handler for tests
import template.handler.handlerFactory as handlerFactory

from random import random
# TODO Seperate MonoTemplate class and Expression class, add support for
# intersection/Union/parenthesis in expression. Make a powerfull parser
# that would use theses class


class Template:

    def __init__(self, orTemplate):
        self.composingTemplate = orTemplate

    def setSecurity(fileConstraints, allowCommand):
        Template.fileConstraints = fileConstraints
        Template.allowCommand = allowCommand
        Template.handlerFactory = handlerFactory.HandlerFactory(
            fileConstraints, allowCommand)

    def getAllValues(self, defaultKeys):
        """ Get all values of all composing templates"""

        values = []
        for template in self.composingTemplate:
            values.extend(self.getValuesMono(template, defaultKeys))
        return values

    def getValuesMono(self, template, defaultKeys):
        """Return all possible values for a MONO template"""
        mainComponent, optionString = template
        handler = Template.handlerFactory.getHandler(
            mainComponent, optionString, defaultKeys)
        return handler.getValues()

    def replace(self, defaultKeys={}):
        """Return a random value from the possibles values"""
        values = self.getAllValues(defaultKeys)
        randomIndex = int(len(values) * random())
        randomStr = values[randomIndex]
        return randomStr
