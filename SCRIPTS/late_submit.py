from datetime import datetime
from config_reader import config_reader
TIME_STAMP = 'Time Stamp: '
SUBMITTER = 'Submitter: '

class late_submit_checker:
    handin_log = {}
    late_submitter = {}

    def __init__(self):
        self.cr = config_reader()

    def read_handinlog(self):
        assignment_dir = self.cr.get_assignemnts()
        
        with open(assignment_dir+'/HANDIN_LOG') as fobj:
            lines = fobj.readlines()
        lines = [x.strip() for x in lines] 

        for line in lines:
            # id_index = line.find(SUBMITTER)
            id_end = line.find('@')
            uom_id = line[len(SUBMITTER):id_end]
            date_index = line.find(TIME_STAMP)
            date = line[date_index+len(TIME_STAMP):]
            # datetime_object = datetime.strptime('Jun 1 2005  1:33PM', '%b %d %Y %I:%M%p')
            datetime_object = datetime.strptime(date, '%a %b %d %H:%M:%S %Y')
            self.handin_log[uom_id] = datetime_object

        return self.handin_log

    def late_submitter_log(self):
        if len(self.handin_log) == 0:
            self.read_handinlog()
            
        deadline = datetime.strptime(self.cr.get_deadline(), '%a %b %d %H:%M:%S %Y')

        for uom_id, date in self.handin_log.items():
            if date > deadline:
                self.late_submitter[uom_id] = date

        # for x in late_submitter.keys():
        #     print(x)
        return self.late_submitter
        


c1 = late_submit_checker()
print(c1.read_handinlog())