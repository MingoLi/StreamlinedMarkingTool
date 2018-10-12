#! /usr/bin/env python
import cmd2
from SCRIPTS.config_reader import config_reader
import os


class Shell(cmd2.Cmd):
    prompt = "$ "
    editor = "code"
    def __init__(self):
        cmd2.Cmd.__init__(self)
        self.cr = config_reader()
        os.chdir('ASSIGNMENTS')

    # def do_loadaverage(self, line):
    #     with open('./text.txt') as fobj:
    #         data = fobj.read()
    #     print(data)

    def do_print_dir(self, location):
        """Print directory path.
    Usage:
        pd <dir_name>

        dir_name:
            - ASSIGNMENTS
            - EMAILS
            - ...
        """
        print(self.cr.get_file_location(location))
        pass


    def do_ls(self, path):
        os.system('ls' + path)
        pass

    def do_cd(self, path):
        os.chdir(path)
        pass

    def do_exit(self,*args):
        return True


    # short cut for commands
    do_pd = do_print_dir


if __name__ == '__main__':
    app = Shell()
    app.cmdloop()