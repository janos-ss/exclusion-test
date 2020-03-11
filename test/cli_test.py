import bin.parser as parser
import subprocess


def test_parsing():
    argsStr = '"Hello word, my name is {testData}" --file-constraint /opt -f /etc /dodo -s family="toto, tata,toto=8" toto=18=36 --set toto="maman, papa 8"'
    args = parser.getArgs(argsStr)
    assert sorted(args['file_constraint']) == sorted(['/opt', '/etc', '/dodo'])
    dico = args['set']
    assert sorted(dico['family']) == sorted(['toto', ' tata', 'toto=8'])
    assert sorted(dico['toto']) == sorted(['18=36', 'maman', ' papa 8'])


def test_bin():

    command = 'python3.7 ../bin/mutemple "Hello word, my name is {maman}" --file-constraint /opt -f /etc /dodo -s family="toto, tata,toto=8" toto=18=36 --set toto="maman, papa 8" -s maman=papa'
    result = subprocess.run(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    assert result.stderr == b""
    assert result.stdout == b"Hello word, my name is papa"
