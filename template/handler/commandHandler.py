from template.handler.handler import Handler
import subprocess
# Put every file in .list extension name in the directory AND subdirectories


class CommandHandler(Handler):

    def getInput(self):
        res = []
        process = subprocess.run(
            self.mainComponent, shell=True, stdout=subprocess.PIPE, universal_newlines=True)
        output = process.stdout
        return output
