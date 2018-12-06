from config_reader import config_reader
from feedback import feedback
from late_submit import late_submit_checker
import os.path

class statistics:

    def __init__(self):
        self.cr = config_reader()
        self.feedback_dir = self.cr.get_feedback()
        self.feedbeck = feedback()
        self.late_submission_list = late_submit_checker().late_submitter_log()
        self.late_penalty = int(self.cr.get_late_submit_penalty())
        
    def generate_csv(self, force):
        log_path = self.feedback_dir + '/' + 'feedback.ini'

        # check if feedback.ini exists
        if os.path.exists(log_path):
            missing = self.feedbeck.check_missing_student()
            if missing > 0 and not force:
                print('WARNING: use -f to force generating csv file')
                return
            
            grades_dir = self.cr.get_grades()
            course_info = self.cr.get_courseInfo()
            csv_file = grades_dir + '/' + course_info.get('coursenumber') + course_info.get('section') + '.csv'

            full_mark = int(self.cr.get_rubrics().get('fullmark'))
            feedback_list = self.feedbeck.get_all_student_marks()

            for i in self.late_submission_list:
                feedback_list[i] = str(int(feedback_list[i]) + self.late_penalty)

            f = open(csv_file,"w+")
            f.write('student id, mark\n')
            for uomid, mark in feedback_list.items():
                f.write("%s, %d\n" % (uomid, full_mark + int(mark)))
            f.close()

        else:
            print('feedback log not found')
        pass
