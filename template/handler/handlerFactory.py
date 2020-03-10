import os
from template.handler.commandHandler import CommandHandler
from template.handler.directoryHandler import DirectoryHandler
from template.handler.fileHandler import FileHandler
from template.handler.basicHandler import BasicHandler
# TODO This class should have been a factory class for class Handler. This
# would allow no hack to avoid circular dependency and would result also
# in cleaner architecture


class HandlerFactory:
    # optionMap defined just after class creation (avoiding egg and chicken)
    """ HandlerFactory parse acquired options and maincomponent, and create a subhandler in function of found options/component and security limitations. """

    def __init__(self, fileConstraint=[], allowCommand=False):
        if type(fileConstraint) != list:
            fileConstraint = [fileConstraint]
        self.fileConstraint = fileConstraint
        self.allowCommand = allowCommand

    def parseOptionsString(string):
        """Parse option string and return associed dictionnary. Separator is ,. Options are in form key = value"""
        res = {}
        if not string:
            return res
        striped = string.replace(" ", "")
        options = striped.split(',')
        for option in options:
            striped = option.split("=")
            left = striped[0]
            right = striped[1]
            res[left] = right
        return res

    def getHandler(self, mainComponent, optionstr, defaultTemplate):
        """ Parse option and look for 'file' option to return the good sub class handler. If there is no file option, guess one"""
        options = HandlerFactory.parseOptionsString(optionstr)
        templateType = options.get('type', None)
        if not templateType:
            return self.guessHandler(mainComponent, options, defaultTemplate)
        else:
            return self._switchType(templateType, mainComponent, options, defaultTemplate)

    def _switchType(self, optType, mainComponent, options, defaultTemplate):
        """ Create the handler in function of the string arg you give """
        try:
            return HandlerFactory.optionMap[optType](self, mainComponent, options, defaultTemplate)
        except ValueError as v:
            v.msg = 'The specified type option "' + optType + \
                '" is not in the subset: dir, cli, dic, file'

    def guessHandler(self, mainComponent, options, defaultTemplate):
        """ Guess and return appropriate handler for content if given condition are accepted, in this order:
        Test if key of defaultTemplate
        Test if it's a file
        Test if it's a directory
        Run a command 
        """
        # 1 priority: Fixed
        if defaultTemplate.get(mainComponent):
            return BasicHandler(mainComponent, options, defaultTemplate)
        # 2 priority File
        if os.path.isfile(mainComponent):
            return self.getFile(mainComponent, options)
            # 3 priority Directory
        if os.path.isdir(mainComponent):
            return self.getDirectory(mainComponent, options)
        # 4 CommandLine
        return self.getCommand(mainComponent, options)

    def checkFileAccess(self, path):
        """Check if a path is included in at least one path in a list of path"""
        path = os.path.abspath(path)
        for constraintpath in self.fileConstraint:
            constraintpath = os.path.abspath(constraintpath)
            common = os.path.commonpath([path, constraintpath])
            if common == constraintpath:
                return True
        return False

    def getFile(self, mainComponent, options, placeHolder=None):
        """Consider mainComponent as a file and executing proper security checking before returning a file handler"""
        if self.checkFileAccess(mainComponent):
            return FileHandler(mainComponent, options)
        else:
            raise PermissionError('Error: The asked file ' + mainComponent +
                                  ' is not in any path from the constraints:' + ', '.join(self.fileConstraint))

    def getDirectory(self, mainComponent, options, placeHolder=None):
        """Consider mainComponent as a directory and executing proper security checking before returning a dir handler"""
        if self.checkFileAccess(mainComponent):
            return DirectoryHandler(mainComponent, options)
        else:
            raise PermissionError('Error: The asked directory ' + mainComponent +
                                  ' is not in any path from the constraints:' + ', '.join(self.fileConstraint))

    def getCommand(self, mainComponent, options, placeHolder=None):
        """Consider mainComponent as a command and executing proper security checking before returning a command handler"""
        if self.allowCommand:
            return CommandHandler(mainComponent, options)
        else:
            raise PermissionError(
                'Error: You cannot execute a command. Set allowCommand to True')

HandlerFactory.optionMap = {'file': HandlerFactory.getFile, 'dir':
                            HandlerFactory.getDirectory, 'cli': HandlerFactory.getCommand, 'dic': BasicHandler}
