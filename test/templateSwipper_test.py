import pytest
import templateSwitcher
from template.template import Template


a = 2 * 'a'
mutator = templateSwitcher.TemplateSwitcher()


def mockReplace(self):
    return 'TEST'


def test_setTemplates():
    pass


def test_findTemplate():
    testString = a + \
        a.join(['{test}', '{test2}[]', '{test3}[op=19]',
                '{test4}[op=19,ap=tata]', '{test5{test5-2}}']) + a

    (content, options), start, end = mutator.findFirstTemplate(testString, 0)
    assert content == 'test'
    assert bool(options) == False
    assert start == 2
    assert end == 8

    (content, options), start, end = mutator.findFirstTemplate(testString, 8)
    assert content == 'test2'
    assert bool(options) == False
    assert start == 10
    assert end == 19

    (content, options), start, end = mutator.findFirstTemplate(testString, 17)
    assert content == 'test3'
    assert options == 'op=19'
    assert start == 21
    assert end == 35

    (content, options), start, end = mutator.findFirstTemplate(testString, 22)
    assert content == 'test4'
    assert options == 'op=19,ap=tata'
    assert start == 37
    assert end == 59

    # Testing than finished templated is detected first
    (content, options), start, end = mutator.findFirstTemplate(testString, 38)
    assert content == 'test5-2'
    assert bool(options) == False
    assert start == 67
    assert end == 74


def test_findComposedTemplate():
    testString = a.join(
        ['{test1}||{test2}[2]||{test3}[]||{test4}', '{test5}||{test6}'])
    composedTemplate, start, newEnd = mutator.findComposedTemplate(
        testString, 2)
    assert composedTemplate[0] == ('test1', None)
    assert composedTemplate[1] == ('test2', '2')
    assert composedTemplate[2] == ('test3', None)
    assert composedTemplate[3] == ('test4', None)

    composedTemplate, start, newEnd = mutator.findComposedTemplate(
        testString, 39)
    assert composedTemplate[0] == ('test5', None)
    assert composedTemplate[1] == ('test6', None)


def test_switchOne(monkeypatch):
    monkeypatch.setattr(Template, "replace", mockReplace)
    testString = 'Hey, this is a {watevs}[ops=7,tata=8]{another} and {another}'

    res = mutator.switchOne(testString)
    assert res == 'Hey, this is a TEST{another} and {another}'


def test_switchAll():
    monkeypatch.setattr(Template, "replace", mockReplace)
    testString = 'Hey, this is a {watevs}[ops=7,tata=8]{another} and {another}'

    res = mutator.switch(testString)
    assert res == 'Hey, this is a TESTTEST and TEST'
