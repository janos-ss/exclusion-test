import re
from template.template import Template

templateWordReg = re.compile(r'{([^{]*?)}(\[(.*?)\])?')


class TemplateSwitcher:

    def __init__(self):
        self.fixTemplate = {}

    # For each key of dico not in templates, add value
    def setDico(self, dico):
        """Set dico of switcher in order than {key} translate to one word among items of dico['key']"""
        self.fixTemplate = dico

    def switchOne(self, string):
        """ Resolve first finded template in string. Return resulted string"""
        template, start, end = self.findComposedTemplate(string)
        if template:
            template = Template(template, self.fixTemplate)
            return string[0:start] + template.replace() + string[end:]
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
