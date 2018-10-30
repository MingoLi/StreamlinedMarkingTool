from config_reader import config_reader
from configparser import ConfigParser, ExtendedInterpolation
import io
from utility import utility

class feedback:

    def __init__(self):
        self.cr = config_reader()
        self.feedback_list = self.cr.get_rubrics()
        self.feedback_dir = self.cr.get_feedback()
        self.utility = utility()

    def print_all_rubric(self):
        # for name, value in self.feedback_list:
        #     print '  %s = %s' % (name, value)
        for option in self.feedback_list:
            value = self.feedback_list.get(option)
            print option + ' : ' + value 
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
            print 'Error: You have to be in a student directory'

        else:
            # Find pre-defined full feedback sentence
            feedback = self.feedback_list.get(feedback)
            if feedback is None:
                print 'Error: give feedback sentence not defined in config'
                return

            # Convert deduction to negative int 
            if not deduction.startswith('-'):
                deduction = '-' + deduction

            log_path = self.feedback_dir + '/' + 'feedback.ini'
        
            fd_log = open(log_path, 'r+')
            config = fd_log.read()
            parser = ConfigParser(interpolation=ExtendedInterpolation())
            parser.readfp(io.BytesIO(config))
            
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
            fd_log.close()
            fd_log_update.close()        
        pass


# fd = feedback()
# fd.print_sections()
# fd.print_rubric()
    