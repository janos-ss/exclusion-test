import os

# TODO This class should have been a factory class for class Handler. This
# would allow no hack to avoid circular dependency and would result also
# in cleaner architecture


class Handler:
    """ Abstract Handler class. Handler shares somes default, they can have special default by having a defaultclass attribute"""

    def __init__(self, mainComponent, options):
        self.mainComponent = mainComponent

        self.options = self.createOptions(options)

    def getValues(self):
        raise NotImplementedError(
            'Error: Handler is an abstract class, you should instantiate a subclasse with the HandlerFactoryClass')

    def createOptions(self, options):
        # this default can reasonably be shared accross all handlers. If you
        # have name/value conflic define a default in your class
        communDefault = {'sep': '\n', 'sep2': ' '}
        res = communDefault
        realclass = type(self)
        if getattr(realclass, 'default', None):
            res.update(realclass.default)
        if options:
            res.update(options)
        return res
