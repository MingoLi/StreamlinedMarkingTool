#! /usr/bin/env python
import cmd2
import argparse
from config_reader import config_reader
from utility import utility
from feedback import feedback
from statistics import statistics
from email_sender import email_sender
from late_submit import late_submit_checker
import os


class Shell(cmd2.Cmd):
    prompt = "$ "
    editor = "code"
    debug = "True"
    def __init__(self):
        cmd2.Cmd.__init__(self)
        self.cr = config_reader()
        self.utility = utility()
        self.feedback = feedback()
        self.statistics = statistics()
        self.es = email_sender()
        self.late_submit_checker = late_submit_checker()
        os.chdir('ASSIGNMENTS')    

    # def do_print_dir(self, location):
    #     """Print directory path.
    # Usage:
    #     pd <dir_name>

    #     dir_name:
    #         - ASSIGNMENTS
    #         - EMAILS
    #         - ...
    #     """
    #     print(self.cr.get_file_location(location))
    #     pass

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

    def do_resume(self, args):
        """Lead you to the directory you were working on last time"""
        self.utility.resume(self.cr.get_assignemnts(), self.feedback)
        print(os.getcwd())
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
    argparser_feedback.add_argument('feedback', help='use feedback abbreviations defined in config file')
    argparser_feedback.add_argument('deduct', help='marks to be deducted')
    @cmd2.with_argparser(argparser_feedback)
    def do_feedback(self, args):
        """Leave feedback to current student. Feedbacks are stored in FEEDBACK/feedback.ini, and will be used to generate email template"""
        print(args.feedback + ': ' + args.deduct)
        self.feedback.leave_feedback(args.feedback, args.deduct)
        pass

    argparser_bonus = argparse.ArgumentParser()
    argparser_bonus.add_argument('bonus', help='use bonus abbreviations defined in config file')
    argparser_bonus.add_argument('add', help='marks to be added')
    @cmd2.with_argparser(argparser_bonus)
    def do_bonus(self, args):
        """Give bonus to current student. Bonus are stored in FEEDBACK/feedback.ini, and will be used to generate email template"""
        print(args.bonus + ': ' + args.add)
        self.feedback.give_bonus(args.bonus, args.add)
        pass

    def do_feedbacklist(self, args):
        """List all available feedback sentences"""
        self.feedback.print_all_rubric()
        pass

    def do_feedbackHistory(self, args):
        """Show all the feedbacks assigned to current student"""
        self.feedback.get_curr_feedback()
        pass

    def do_check(self, args):
        """List all students who do not have any feedback assigned"""
        self.feedback.check_missing_student()
        pass

    generate_csv_parser = argparse.ArgumentParser()
    generate_csv_parser.add_argument('-f', '--force', action='store_true', help="""ignore the warning and force generating the csv file.\n 
    Note: by doing this, the system will consider that the students who have no feedback associated as full mark""")
    @cmd2.with_argparser(generate_csv_parser)
    def do_generate_csv(self, args):
        if args.force:
            self.statistics.generate_csv(True)
        else:
            self.statistics.generate_csv(False)
        pass

    send_email_parser = argparse.ArgumentParser()
    send_email_parser.add_argument('-c', '--check', action='store_true', help="""This will ONLY create txt file under EMAIL BACKUP folder and will NOT
    actully send it, and will NOT be logged""")
    @cmd2.with_argparser(send_email_parser)
    def do_send_email(self, args):
        """Only call this when you done all the marking. This command will send each student a email including the feedbacks and marks they gained. Send log can be found 
        under LOG/email_log.ini, and one copy of each email being sent will be saved under EMAIL BACKUP"""
        all_student_list = next(os.walk(self.cr.get_assignemnts()))[1]
        l = len(all_student_list)

        if not args.check:
            if not self.utility.query_yes_no('Are you sure you want to send emails to ' + str(l) + ' students? [y/n]'):
                return

        self.utility.printProgressBar(0, l, prefix = '', suffix = 'Complete', length = 50)
        for i, s in enumerate(all_student_list):
            prefix = 'sending to ' + s + ':'
            if not args.check:
                if not self.es.send_email(s):
                    print("Stop sending email")
                    break
            else:
                if not self.es.send_email_fake(s):
                    print("Stop sending email")
                    break
            self.utility.printProgressBar(i + 1, l, prefix = prefix, suffix = 'Complete', length = 50)
        pass
    
    
    def do_list_late_submit(self, args):
        print(self.late_submit_checker.late_submitter_log())
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
    do_make = do_compile
    do_fd = do_feedback
    do_fdlist = do_feedbacklist
    do_fdhis = do_feedbackHistory
    do_quit = do_exit
    do_gencsv = do_generate_csv
    do_notify = do_send_email

if __name__ == '__main__':
    app = Shell()
    app.cmdloop()