[![codecov](https://codecov.io/gh/crazyhouse33/templateSwitcher/branch/master/graph/badge.svg)](https://codecov.io/gh/crazyhouse33/templateSwitcher)


python template engine

# Motivations
This personal project had been published just to show I can produce clean project for potential recrutors.
So I just took a piece from one of my personal project than I cleaned out to publish on github.

This project had been created in the beginning to allow template modification based on value files. At that time I would only need to do union feature (se below). Now I would like to improve the parser to expose set arithmetic on value files.

Hopefully this repo may be usefull for you. Here is the "online doc", each function is documented by docstring. 

# Contribute
Any pr is welcome. Run dev/.githooks/shareHooks.bash to use my ci setup for this project (autolinting at comit and test before pushing)

For now I mainely want to create a true parser, and to divide the template class into expression and templates. The expression class would define what is the intersection of two expression, negation and so on. The parser would return an abstract tree that this expression would use to combinate simple template handler result in the good way.


# Doc

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

If you want to avoid ambiguity, pass the type= key | file | dir | cli option:
```python
"Hello {name}[type=file]"
```

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

## Parsing 
The parsing of your file and command entry start at first line and end at the first final white character. It mean that if you want empty string to be a possible value you cannot put it in the end, but you can put it in the begining or anywhere in the midle



