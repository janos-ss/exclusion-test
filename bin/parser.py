import argparse
from template.handler.handler import Handler
import shlex

parser = argparse.ArgumentParser(
    'This program is a cli interface for this python libary : https://github.com/crazyhouse33/templateSwitcher')
# TODO in python 3.8 you can just use extend as action wich will remove
# the need for parseConstraint function
parser.add_argument('-f', '--file-constraint', action='append', nargs='*',
                    help='list of directory/files that where you allow readAccess')
parser.add_argument(
    "-c", "--allow-command", action='store_true', help="Allow command execution")
parser.add_argument("-d", "--debug", action='store_true',
                    help="print the states of your switcher before printing result")


parser.add_argument('--sep',
                    default=',',
                    help='Separator for the dictionnary keys values. Default is ,')

parser.add_argument('--sep2',
                    default=' ',
                    help='Separator for the dictionnary keys values and the associated probability. Default is " "')


parser.add_argument("template", help='The template to parse')
parser.add_argument("-s", "--set",
                    metavar="KEY=VALUE[sepVALUE[sepVALUE...]",
                    nargs='+',
                    action='append',
                    help="""Add to the dictionnarys value to the template switching
                        you need to use " around yours value: ex:
                        .mutemple -s toto="mom 3,dad 6" apple=fruit -s toto=tata apple=vegetable
                        result in this dictionnary:
                        {'toto': ['mom 3', 'dad 6', 'tata'], 'apple': ['fruit', 'vegetable']}
                        """
                    )


def getArgs(string=None):  # we allow string for testing purpose
    if string:
        args = parser.parse_args(shlex.split(string))
    else:
        args = parser.parse_args()
    args = vars(args)

    parsedCons = parseMultiOptions(args['file_constraint'])
    args['file_constraint'] = parsedCons

    parsedDico = parseDico(args['set'], args['sep'], args['sep2'])
    args['set'] = parsedDico
    return args


# Correcting argparse stuff
def parseMultiOptions(argparseproduct):
    res = []
    for liste in argparseproduct:
        res.extend(liste)
    return res


def parseDico(argparseProduct, sep, sep2):

    listEntry = parseMultiOptions(argparseProduct)
    handler = Handler('placeholder', {'sep': sep, 'sep2': sep2})
    # We use the same algo as handler do for the files syntax
    res = {}
    for entry in listEntry:
        key, values = entry.split('=', 1)
        values, ponderation, allEqual = handler.parseData(values)
        old = res.get(key, [])
        old.extend(values)
        res[key] = old
    return res
