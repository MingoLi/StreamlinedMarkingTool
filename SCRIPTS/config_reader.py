from configparser import ConfigParser, ExtendedInterpolation
import io

class config_reader:

    def __init__(self):
        self.parser = ConfigParser(interpolation=ExtendedInterpolation())
        self.parser.read('CONFIGURATION/config.ini')

    def get_assignemnts(self):
        return self.parser.get('paths', 'assignments_dir')

    def get_unit_test(self):
        return self.parser.get('paths', 'unit_test_dir')
    
    def get_rubrics(self):
        return self.parser['rubric']

    def get_feedback(self):
        return self.parser.get('paths', 'feedback_dir')

    def get_grades(self):
        return self.parser.get('paths', 'grades_dir')
    
    def get_courseInfo(self):
        return self.parser['courseInfo']

    def get_email_settings(self):
        return self.parser['email']

    def get_email_log(self):
        return self.parser.get('paths', 'email_log_dir')

    def get_email_backup(self):
        return self.parser.get('paths', 'email_backup_dir')
    
    def get_late_submit_penalty(self):
        return self.parser.get('deadlines', 'penalty')
        
    def get_deadline(self):
        return self.parser.get('deadlines', 'deadline')
