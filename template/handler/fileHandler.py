from template.handler.handler import Handler


class FileHandler(Handler):

    def getInput(self):
        return FileHandler.readFile(self.mainComponent)

    def readFile(f):
        """ Return content file"""
        with open(f, 'r') as f:
            return f.read()
