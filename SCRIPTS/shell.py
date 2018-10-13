#! /usr/bin/env python
import cmd2
import argparse
from config_reader import config_reader
from utility import utility
import os


class Shell(cmd2.Cmd):
    prompt = "$ "
    editor = "code"
    def __init__(self):
        cmd2.Cmd.__init__(self)
        self.cr = config_reader()
        self.utility = utility()
        os.chdir('../ASSIGNMENTS')

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


    compile_parser = argparse.ArgumentParser()
    compile_parser.add_argument('-r', '--recursive', action='store_true', help='compile the subdirectory recursively')
    @cmd2.with_argparser(compile_parser)
    def do_compile(self, args):
        """Run `make` in current directory if makefile founded.
        """
        work_dir = os.getcwd()

        if args.recursive:
            compiled = self.utility.compile_through_makefile(work_dir, True)
        else:
            compiled = self.utility.compile_through_makefile(work_dir, False)

        if not compiled:
            print('makefile not found')
        else:
            print('compilation done')
        pass 


    def do_ls(self, path):
        os.system('ls' + path)
        pass

    def do_cd(self, path):
        os.chdir(path)
        pass
    
    def do_pwd(self, *args):
        print(os.getcwd())
        pass

    def do_exit(self, *args):
        return True


    # short cut for commands
    do_pd = do_print_dir
    do_make = do_compile


if __name__ == '__main__':
    app = Shell()
    app.cmdloop()