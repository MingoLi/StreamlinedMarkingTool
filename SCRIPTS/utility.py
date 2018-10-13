#! /usr/bin/env python
from config_reader import config_reader
import os

class utility:

    # Traverse the student's directory and see if there is makefile
    def compile_through_makefile(self, path, recursive):
        compiled = False
        # cr = config_reader()
        # assignment_dir = cr.get_assignemnts()
        # student_dir = assignment_dir + "/" + uomid
        rootDir = path 
        if recursive:
            for dirName, subdirList, fileList in os.walk(rootDir):
                for fname in fileList:
                    if fname == 'makefile':
                        os.chdir(dirName)
                        os.system('make')
                        compiled = True
                    # print(fname)
        else:
            for f in os.listdir(rootDir):
                if f == 'makefile':
                        os.chdir(rootDir)
                        os.system('make')
                        compiled = True

        # back to student's root dir
        os.chdir(rootDir)
        return compiled


# u = utility()
# u.compile_through_makefile('/Users/mingo/Desktop/StreamlinedMarkingTool/ASSIGNMENTS/lim34521', False)        