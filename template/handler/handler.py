import os

#TODO This class should have been a factory class for class Handler. This would allow no hack to avoid circular dependency and would result also in cleaner architecture
class Handler:
    """ Handler parse acquired options and maincomponent, and create a subhandler in function of found options/component and security limitations. """
    def __init__(self, mainComponent, options, defaultTemplate, fileConstraint, allowCommand):
        if (type(self)== Handler):
            self.mainComponent = mainComponent
            self.options= self.parseOptionsString(options)
            self.defaultTemplate = defaultTemplate
            #security options 
            self.fileConstraint = fileConstraint
            self.allowCommand = allowCommand
        
    def parseOptionsString(string):
        """Parse option string and return associed dictionnary. Separator is ,. Options are in form key = value"""
        res= {}
        if not string: 
            return res
        striped = string.replace(" ", "")
        options = striped.split(',')
        for option in options:
            striped= option.split("=")
            left= striped[0]
            right= striped[1]
            res[left]=right
        return res
 
    
    # We import here in order to get out of circular imporation
    def getHandler(mainComponent, options, defaultTemplate, fileConstraint, allowCommand):
        """Chose and return appropriate handler for content if given condition are accepted, in this order:
        Test if key of defaultTemplate
        Test if it's a file
        Test if it's a directory
        Run a command 
        """
        #1 priority: Fixed
        if defaultTemplate.get(mainComponent):

            from template.handler.basicHandler import BasicHandler 
            return BasicHandler(mainComponent, options, defaultTemplate, fileConstraint, allowCommand)
        #2 priority File
        if Handler.checkFileAccess(mainComponent, fileConstraint):
            if os.path.isfile(mainComponent):
                from template.handler.fileHandler import FileHandler 
                return FileHandler(mainComponent, options, defaultTemplate, fileConstraint, allowCommand)
            #3 priority Directory
            if os.path.isdir(mainComponent):

                from template.handler.directoryHandler import DirectoryHandler
                return DirectoryHandler(mainComponent, options, defaultTemplate, fileConstraint, allowCommand)
        #4 CommandLine
        if allowCommand:

            from template.handler.commandHandler import CommandHandler
            return CommandHandler(mainComponent, options, defaultTemplate, fileConstraint, allowCommand)
        raise RuntimeError("Could not replace your template: " + mainComponent + "\nCheck your security options and try again")
    
    def checkFileAccess(path, constraint):
        """Check if a path is included in at least one path in a list of path"""
        path= os.path.abspath(path)
        for constraintpath in constraint:
            constraintpath=os.path.abspath(constraintpath)
            common=os.path.commonpath([path, constraintpath])
            if common == constraintpath:
                return True
        return False

