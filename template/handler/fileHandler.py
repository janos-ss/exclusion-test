from template.handler.handler import Handler


class FileHandler(Handler):

    def getInput(self):
        with open(self.mainComponent, 'r') as f:
            return f.read()
