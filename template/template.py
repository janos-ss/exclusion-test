# Need to e as it is to be able to monkey patch handler for tests
import template.handler.handlerFactory as handlerFactory

import random
# TODO Seperate MonoTemplate class and Expression class, add support for
# intersection/Union/parenthesis in expression. Make a powerfull parser
# that would use theses class


class Template:

    def __init__(self, orTemplate):
        self.composingTemplate = orTemplate

    def setSecurity(fileConstraints, allowCommand):
        """Set security settings of the class. File constraint is the list of accessible directories (recursive) and allowCommand is  bool"""
        Template.fileConstraints = fileConstraints
        Template.allowCommand = allowCommand
        Template.handlerFactory = handlerFactory.HandlerFactory(
            fileConstraints, allowCommand)

    def getAllValues(self, defaultKeys):
        """ Get all values of composed templates and the sum of the ponderation in a tuple"""

        values = []
        ponderationTotal = 0
        allEqual = True
        for template in self.composingTemplate:
            newValues, ponderation, everyPondEqual = self.getValuesMono(
                template, defaultKeys)
            allEqual &= everyPondEqual
            ponderationTotal += ponderation
            values.extend(newValues)
        return values, ponderationTotal, allEqual

    def getValuesMono(self, template, defaultKeys):
        """Return all possible values for a MONO template and the sum of ponderations in a tuple"""
        mainComponent, optionString = template
        handler = Template.handlerFactory.getHandler(
            mainComponent, optionString, defaultKeys)
        return handler.getValues()

    def replace(self, defaultKeys={}):
        """Return a random value from the possibles values. If handler return ponderation as well as the value, the randomization respect this ponderation"""
        values, ponderationSum, allEqual = self.getAllValues(defaultKeys)
        if not allEqual:
            return Template.inequalWeightReplace(values, ponderationSum)
        else:
            return Template.equalWeightReplace(values)

    def equalWeightReplace(values):
        randomIndex = int(len(values) * random.random())
        randomStr = values[randomIndex][0]
        return randomStr

    # Notes: In our case, it's useless to use a more complex weigthed
    # randomization such as alias method or binary tree cause we draw once per
    # template. Any such technique product ( dart target, sum table) would be
    # need to be cached for potential later user. The memory cost of caching
    # it probably wont ever justify the gain on consecutive replacement. The
    # speed gain on low number of use would also be negative (binary tree
    # creation + 1 use: (n+1) log2(n)). Which would be greater than 2n ("naive
    # algo" construction + 1 use cost)
    def inequalWeightReplace(values, ponderationSum):
        rand = random.random() * ponderationSum
        cpt = 0
        while rand > 0:
            rand -= values[cpt][1]
            cpt += 1
        return values[cpt - 1][0]
