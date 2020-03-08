import re
from template.template import Template

templateWordReg = re.compile(r'{([^{]*?)}(\[(.*?)\])?')


class TemplateSwitcher:

    def __init__(self, fileConstraint=[], command=False):
        
        """fileConstraint: set it to a path or a list of path the template switcher is allowed to read files. By default nothing is accessible.
        
        command: set it to True if you want to provide bash execution to the switcher. (DANGEROUS, if you do so, provide an isolation mechanism. For exemple you can create a fakeuser on your system with a setuid on an executable. The $PATH of your user link only to a directory whith symlink to binary you allow the switcher to use. ) 
        """
        self.fixTemplate = {}
        self.fileConstraint = fileConstraint
        self.allowCommand = command

    # For each key of dico not in templates, add value
    def setDico(self, dico):
        """Set dico of switcher in order than {key} translate to one word among items of dico['key']"""
        self.fixTemplate = dico

    def switchOne(self, string):
        """ Resolve first finded template in string. Return resulted string"""
        template, start, end = self.findComposedTemplate(string)
        if template:
            template = Template(
                template,  self.fileConstraint, self.allowCommand)
            return string[0:start] + template.replace(self.fixTemplate) + string[end:]
        else:
            return string

    def findComposedTemplate(self, string, start=0):
        """ Find composed template in string starting from start."""
        template, start, end = self.findFirstTemplate(string, start)
        if not template:
            return None, -1, -1
        composedTemplate = [template]
        newEnd = end
        while string[newEnd:newEnd + 3] == '||{':
            newTemplate, newStart, newEnd = self.findFirstTemplate(
                string, newEnd + 2)
            if newTemplate == None:
                exit('Problem with template composition ||')
            composedTemplate.append(newTemplate)
        return composedTemplate, start, newEnd

    def findFirstTemplate(self, string, start=0):
        """ Find first finished template in string starting from start. Return parsed options, content, and position in string."""

        groups = templateWordReg.search(string, start)
        if not groups:
            return None, -1, -1
        wholeTemplate = groups[0]
        content = groups[1]
        options = groups[3]
        start = groups.start()
        end = groups.end()

        return (content, options), start, end

# TODO Use re.searchall instead
    def switch(self, string):
        """ Resolve every template of the string. Return the result string"""
        found = True
        res = string
        tmp = string
        while found:
            tmp = res
            res = self.switchOne(res)
            found = res != tmp
        return res
