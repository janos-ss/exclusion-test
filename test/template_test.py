import template.handler.handler
from template.template import Template
oldHandler= template.handler.handler.Handler

#TODO template class is off and should be redecouped 

class mockHandler(template.handler.handler.Handler):
    def __init__(*arg, **args):
        pass

    def getValues(self):
        return ['TEST','TEST2'] 

    def getHandler(*arg, **args):
        return mockHandler()

template.handler.handler.Handler= mockHandler


template1= Template([('key1',None)])
template2= Template([('key2',None), ('key1',None)])


def test_getValuesMono():
    assert template1.getValuesMono(('key1',None),{})== ['TEST','TEST2']

def test_getAllValues():
    assert template1.getAllValues({})== ['TEST','TEST2']
    assert template2.getAllValues({})== ['TEST','TEST2','TEST','TEST2']

def test_replace():
    #TODO truely test randomity?

    templateTest= Template([('key1',None)])
    templateTest.values=['test','test','test']
    assert templateTest.replace() == 'test'

Handler = oldHandler

    
    



