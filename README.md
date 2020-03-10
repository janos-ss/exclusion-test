[![codecov](https://codecov.io/gh/crazyhouse33/templateSwitcher/branch/master/graph/badge.svg)](https://codecov.io/gh/crazyhouse33/templateSwitcher)


python template engine

# Motivations
I want to have a public piece of code to show that I can code.
So I just took a piece from one of my personal project than I cleaned out to publish it on github in order to show the world:

* I have somes dev/ops skills
* I can manage a python project

Procedure:

* Put auto linter, test checker, test coverage report on githook. (see dev directory)
* Defining clean architecture for my old code 
* Implement unitest for each class of the archi
* Change code to match architecture, run against the tests, commit test and class when it pass.

Hopefully this repo may be usefull for you. Here is the "online doc", each class function is documented by docstring. 

# Doc
TODO = I am gonna implement it when I am free.
The rest is allready there. I am actually coding tests. I will push the first release when every thing is okay.

## Exemple
The aim is to transform a template string such as that one:
```python
"""Hey {name}[sep=;], I want to talk about the {./animal}s at the zoo of {city}.  
Infortunately, one of them had been attacked a by a {./animal/dangerous.val}||{human/dangerous.val}"""
```
To output a string such as:
```python
"""Hey Jack, I want to talk about the cows at the zoo of New-York.
Infortunately, one of them had been attacked a by a tiger."""
```
or :

```python
"""Hey Michael, I want to talk about the parrots at the zoo of Washington.
Infortunately, one of them had been attacked a by a terrorist."""
```

## Template
Template follow this patern:

{content}[options]

A content can contain another template.

Content can be a:
* key you entered in the switcher dictionary
* file (desactivated by default)
* directory (desactivated)
* commandline (desactivated by default)

The parser by default check the type if it's match something existing in this order. 

TODO
If you want to avoid ambiguity, pass the type= key | file | dir | cli option.

### Key
Replace {key} by the value of the dico you set to the switcher. If the value is a list select a random one.

### File
Replace {path} by value present in the file at path. If multiple values are found, return one at random

**Options:**
#### sep
default = '\n'
Precise separator for finding multiple value in the file



#### sep2
TODO 
 <pre>default =' '</pre>
Precise the ponderator separator. Ie, in this file:
```bash
tiger 20
cow 80
```
Then the template {filename} is replaced 20% of the time by tiger
The unit is unchecked. You have to put something that can be interpreted as a float by python, followed by wathever the string until the first separator.

In this other exemple
```bash 
tiger 2
cow 4
tiger 1Mo
monkey
```
{file} is gonna be: 
* tiger 3/8 of the times.
* cow 4/8 of the times.
* monkey, 1/8 of the times


### Directory
Search recursively in the directory and return a random value among any present in any .val file. (TODO regexp selection)

### Command
Run command and parse output as a file.

## Special case

### Template Combination
A template can be combined by many one with ||. || must stick to the two templates (no space). The result is one from the union of all the composing templates: {flying}||{4legs}||{fish}

TODO (HARD, need a way more powerfull parser and architecture change)
Allow intersection an grouping notation:
{flying}||({4legs}&{hairy}

### Template refering
TODO
You can refer to the n template to reuse it in place:
```python
"""{salutation} $2.
blabla...
Anyway {name}, see you soon."""
```
Which translate to:
```python
"""Hey Jenny.
blabla...
Anyway Jenny, see you soon."""
```

## Security
The file and command replacement feature is desactivated for obvious security reason. You have to active it at instanciation in the switcher constructor (see doc).

### File
By setting the fileconstraint default variable ( either a path to accepted file/directory), either a list of them in the switcher constructor.

### Command
Set the default variable command at True in switcher constructor



