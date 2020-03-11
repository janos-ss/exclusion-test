from template.handler.handler import Handler
from template.handler.fileHandler import FileHandler
import os
# Put every file in .list extension name in the directory AND subdirectories


class DirectoryHandler(Handler):

    def getInput(self):
        res = ''
        for dirpath, dirnames, filenames in os.walk(self.mainComponent):
            for f in filenames:
                if f.endswith('.val'):
                    with open(dirpath + '/' + f) as f2:
                        res += f2.read()
        return res
