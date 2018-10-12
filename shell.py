#! /usr/bin/env python
from cmd2 import Cmd
from SCRIPTS.config_reader import config_reader


class Shell(Cmd):
    prompt = "$ "
    def __init__(self):
        Cmd.__init__(self)
        self.cr = config_reader()

    def do_loadaverage(self, line):
        with open('./text.txt') as fobj:
            data = fobj.read()
        print(data)

    def do_print_dir(self, location):
        print(self.cr.get_file_location(location))
        pass
    # short cut for this command
    do_pd = do_print_dir


if __name__ == '__main__':
    app = Shell()
    app.cmdloop()