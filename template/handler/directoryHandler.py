from template.handler.handler import Handler
from template.handler.fileHandler import FileHandler
import os
# Put every file in .list extension name in the directory AND subdirectories


class DirectoryHandler(Handler):

    def getInput(self):
        """Recursively explore directory and return joined .val terminated file adding separator between them"""
        resList = []
        for dirpath, dirnames, filenames in os.walk(self.mainComponent):
            for f in filenames:
                if f.endswith('.val'):
                    resList.append(
                        self.sanitize(FileHandler.readFile(dirpath + '/' + f)))

        return self.options['sep'].join(resList)
