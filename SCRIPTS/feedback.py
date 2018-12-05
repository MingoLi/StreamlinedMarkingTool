from config_reader import config_reader
from configparser import ConfigParser, ExtendedInterpolation
import io
import os
from utility import utility

class feedback:

    def __init__(self):
        self.FEEDBACK_LOG_NAME = 'feedback.ini'
        self.cr = config_reader()
        self.feedback_list = self.cr.get_rubrics()
        self.feedback_dir = self.cr.get_feedback()
        self.utility = utility()

    def print_all_rubric(self):
        # for name, value in self.feedback_list:
        #     print '  %s = %s' % (name, value)
        for option in self.feedback_list:
            value = self.feedback_list.get(option)
            print(option + ' : ' + value)
            # value = value.split('@')
            # print "%s: [ / %s] %s" %(option, value[1], value[0])
        pass

    # def print_sections(self):
    #     log_path = self.feedback_dir + '/' + 'feedback.ini'
    #     with open(log_path) as fd_log:
    #             config = fd_log.read()
    #             parser = ConfigParser(interpolation=ExtendedInterpolation())
    #             parser.readfp(io.BytesIO(config))
                
    #             sections = parser.sections()
    #             for sec in sections:
    #                 print sec

    #             print parser['lim34522']

    #     print 'DONE'

    #     pass

    def leave_feedback(self, feedback, deduction):
        uomid = self.utility.get_uomid_of_current_dir()
        if uomid == -1:
            print('Error: You have to be in a student directory')

        else:
            # Find pre-defined full feedback sentence
            feedback = self.feedback_list.get(feedback)
            if feedback is None:
                print('Error: give feedback sentence not defined in config')
                return

            # Convert deduction to negative int 
            if not deduction.startswith('-'):
                deduction = '-' + deduction

            log_path = self.feedback_dir + '/' + self.FEEDBACK_LOG_NAME
        
            # fd_log = open(log_path, 'r+')
            # config = fd_log.read()
            parser = ConfigParser(interpolation=ExtendedInterpolation())
            parser.read(log_path)
            
            if not parser.has_section(uomid):
                parser.add_section(uomid)

            if not parser.has_option(uomid, feedback):
                parser.set(uomid, feedback, deduction)
                
            else:
                value = parser.get(uomid, feedback)
                value = str(int(value) + int(deduction))
                parser.set(uomid, feedback, value)
                
            print('Feedback: %s \nMark deducted: %s' %(feedback, deduction))
            fd_log_update = open(log_path, 'w+')
            parser.write(fd_log_update)
            # fd_log.close()
            fd_log_update.close()        
        pass


    def get_curr_feedback(self):
        uomid = self.utility.get_uomid_of_current_dir()
        if uomid == -1:
            print('Error: You have to be in a student directory')
        else:
            try:
                log_path = self.feedback_dir + '/' + self.FEEDBACK_LOG_NAME
                # with open(log_path) as f:
                #     config = f.read()
                parser = ConfigParser(interpolation=ExtendedInterpolation())
                # parser.readfp(io.BytesIO(config))
                parser.read(log_path)
                
                for option in parser[uomid]:
                    print(option + ' : ' + parser.get(uomid, option))
            except:
                print('You currently have not assigned any feedback')
        pass

    def get_feedback_of(self, uomid):
        if uomid == -1:
            print('Invalid uomid')
        else:
            try:
                fd_list = {}
                log_path = self.feedback_dir + '/' + self.FEEDBACK_LOG_NAME
                # with open(log_path) as f:
                    # config = f.read()
                parser = ConfigParser(interpolation=ExtendedInterpolation())
                # parser.readfp(io.BytesIO(config))
                parser.read(log_path)

                for option in parser[uomid]:
                    fd_list[option] = parser.get(uomid, option)
                        # print(option + ' : ' + parser.get(uomid, option))
                
                return fd_list
            except:
                print('You currently have not assigned any feedback')
        pass

    # return the list of student id that has feedback associated
    def get_student_list(self):
        log_path = self.feedback_dir + '/' + self.FEEDBACK_LOG_NAME
        student_list = []
        try:
            # with open(log_path) as f:
            #     config = f.read()
            parser = ConfigParser(interpolation=ExtendedInterpolation())
            # parser.readfp(io.BytesIO(config))
            parser.read(log_path)
            
            for section in parser.sections():
                student_list.append(section)
        except:
            print('You currently have not assigned any feedback')
        
        return student_list

    def check_missing_student(self):
        all_student_list = next(os.walk(self.cr.get_assignemnts()))[1]
        student_with_feedback = self.get_student_list()

        missing_student = list(set(all_student_list) - set(student_with_feedback))
        if len(missing_student) > 0:
            print('You have ' + str(len(missing_student)) + ' student(s) that do not have any feedback, please check:')
            for s in missing_student:
                print(s)
                
        return len(missing_student)

    # Get all student id with the mark deducted
    def get_all_student_marks(self):
        log_path = self.feedback_dir + '/' + self.FEEDBACK_LOG_NAME
        all_student_list = next(os.walk(self.cr.get_assignemnts()))[1]
        feedback_list = {}
        try:
            # with open(log_path) as f:
            #     config = f.read()
            parser = ConfigParser(interpolation=ExtendedInterpolation())
            # parser.readfp(io.BytesIO(config))
            parser.read(log_path)

            for s in all_student_list:
                mark = 0
                if parser.has_section(s):
                    for options in parser.options(s):
                        mark += int(parser.get(s, options))
                feedback_list[s] = mark
                
                # for section in parser.sections():
                #     mark = 0
                #     for options in parser.options(section):
                #         mark += int(parser.get(section, options))
                #     feedback_list[section] = mark
        except:
            print('You currently have not assigned any feedback')
        
        return feedback_list

    def give_bonus(self, bonus, addition):
        uomid = self.utility.get_uomid_of_current_dir()
        if uomid == -1:
            print('Error: You have to be in a student directory')

        else:
            # Find pre-defined full feedback sentence
            bonus = self.feedback_list.get(bonus)
            if bonus is None:
                print('Error: give bonus sentence not defined in config')
                return

            log_path = self.feedback_dir + '/' + self.FEEDBACK_LOG_NAME
        
            # fd_log = open(log_path, 'r+')
            # config = fd_log.read()
            parser = ConfigParser(interpolation=ExtendedInterpolation())
            parser.read(log_path)
            
            if not parser.has_section(uomid):
                parser.add_section(uomid)

            if not parser.has_option(uomid, bonus):
                parser.set(uomid, bonus, addition)
                
            else:
                value = parser.get(uomid, bonus)
                value = str(int(value) + int(addition))
                parser.set(uomid, bonus, value)
                
            print('Bonus: %s \nMark added: %s' %(bonus, addition))
            fd_log_update = open(log_path, 'w+')
            parser.write(fd_log_update)
            # fd_log.close()
            fd_log_update.close()        
        pass

# fd = feedback()
# fd.print_sections()
# fd.print_rubric()
    