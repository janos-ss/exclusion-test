from template.handler.handler import Handler
from template.handler.fileHandler import FileHandler
import os
# Put every file in .list extension name in the directory AND subdirectories


class DirectoryHandler(Handler):

    def __init__(self, *arg, **args):
        Handler.__init__(self, *arg, **args)
        self.fileHandler = FileHandler(*arg, **args)

    def getValues(self):
        res = []
        for dirpath, dirnames, filenames in os.walk(self.mainComponent):
            for f in filenames:
                if f.endswith('.list'):
                    self.fileHandler.mainComponent = dirpath + f
                    res.extend(self.fileHandler.getValues())
        return res
