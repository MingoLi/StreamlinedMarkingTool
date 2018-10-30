#! /usr/bin/env python
import cmd2
import argparse
from config_reader import config_reader
from utility import utility
from feedback import feedback
import os


class Shell(cmd2.Cmd):
    prompt = "$ "
    editor = "code"
    def __init__(self):
        cmd2.Cmd.__init__(self)
        self.cr = config_reader()
        self.utility = utility()
        self.feedback = feedback()
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

    def do_next(self, *args):
        """Move to the next student's assignment folder

        Note: if you are in ASSIGNMENTS root directory, next will cd to the first available directory

        """
        self.utility.move_to_next_directory(self.cr.get_assignemnts())
        print('cd: ' + os.getcwd())
        pass

    def do_prev(self, *args):
        """Move to the previous student's assignment folder

        Note: if you are in ASSIGNMENTS root directory, prev will cd to the first available directory
        """
        self.utility.move_to_prev_directory(self.cr.get_assignemnts())
        print('cd: ' + os.getcwd())
        pass


    argparser_test = argparse.ArgumentParser(epilog='input unit test files are placed under UNIT TESTS folder, and the files contain their corresponding expeceted output should be named as [filename]_expected plus extension')
    argparser_test.add_argument('exe', help='executable name')
    argparser_test.add_argument('input', help='unit test input filename')
    argparser_test.add_argument('-c', '--context', action='store_true', help='show the diff with context of both file')
    @cmd2.with_argparser(argparser_test)
    def do_test(self, args):
        """Run unit test on executable file, compare the output with pre-defined expecteed output.
        """
        inputfile_path = self.cr.get_unit_test() + '/' + args.input
        exe_path = os.getcwd() + '/' + args.exe
        self.utility.unit_test(exe_path, inputfile_path, args.context)
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


    argparser_feedback = argparse.ArgumentParser()
    # argparser_feedback.add_argument('-m', '--message', type=str, help='use customized feedback sentence')
    # argparser_feedback.add_argument('-d', '--deduct', type=int, help='marks to be deducted')
    argparser_feedback.add_argument('feedback', help='use feedback abbreviations defined in config file')
    argparser_feedback.add_argument('deduct', help='marks to be deducted')
    @cmd2.with_argparser(argparser_feedback)
    def do_feedback(self, args):
        """Leave feedback to current student. Feedbacks are stored in FEEDBACK/feedback.ini, and will be used to generate email template"""
        print args.feedback + ': ' + args.deduct
        self.feedback.leave_feedback(args.feedback, args.deduct)
        pass


    def do_feedbacklist(self, args):
        """List all available feedback sentences"""
        self.feedback.print_all_rubric()
        pass
    
    

    def do_ls(self, path):
        os.system('ls ' + path)
        pass

    def do_cd(self, path):
        os.chdir(path)
        pass
    
    def do_pwd(self, *args):
        print(os.getcwd())
        pass

    def do_exit(self, *args):
        return True

    def do_run(self, args):
        """Run executable file with given arguments.
        """
        from subprocess import call
        argv = args.split()
        if not argv[0].startswith('./'):
            argv[0] = './' + argv[0]
        call(argv)

    # short cut for commands
    do_pd = do_print_dir
    do_make = do_compile
    do_fd = do_feedback
    do_fdlist = do_feedbacklist


if __name__ == '__main__':
    app = Shell()
    app.cmdloop()