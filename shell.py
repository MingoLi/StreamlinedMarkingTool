#! /usr/bin/env python
from cmd2 import Cmd
import config_reader


class Shell(Cmd):
    prompt = "$ "

    def __init__(self):
        Cmd.__init__(self)

    def do_loadaverage(self, line):
        with open('./text.txt') as fobj:
            data = fobj.read()
        print(data)

    


if __name__ == '__main__':
    app = Shell()
    app.cmdloop()