import template.handler.handler as hand # Need to e as it is to be able to monkey patch handler for tests

from random import random
#TODO Seperate MonoTemplate class and Expression class, add support for intersection/Union/parenthesis in expression. Make a powerfull parser that would use theses class
class Template:
    def __init__ (self, orTemplate, fileConstraint=[], command=False):
        self.composingTemplate=orTemplate
        self.fileConstraint=fileConstraint
        self.allowCommand=command
        
    def getAllValues(self, defaultKeys):
        """ Get all values of all composing templates"""
        
        values=[]
        for template in self.composingTemplate:
            values.extend(self.getValuesMono(template, defaultKeys))
        return values


    def getValuesMono(self, template, defaultKeys):
        """Return all possible values for a MONO template"""
        mainComponent, optionString = template

        handler = hand.Handler.getHandler(mainComponent, optionString, defaultKeys, self.fileConstraint, self.allowCommand)

        return handler.getValues()


    def replace(self, defaultKeys={}):
        """Return a random value from the possibles values"""
        randomIndex=int(len(self.getAllValues(defaultKeys)) * random())
        randomStr= self.values[randomIndex]
        return randomStr
