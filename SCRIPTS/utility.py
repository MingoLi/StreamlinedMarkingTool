#! /usr/bin/env python
# from config_reader import config_reader
import os
import math

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

    # Return the uomid of current directory, return -1 if not in any of the directories
    def get_uomid_of_current_dir(self):
        dir_name = '/ASSIGNMENTS/'
        # Get the list of all students directory with uomid as directory name
        # assignment_dir_list = next(os.walk(path))[1] 
        cwd = os.getcwd()
        uomid = cwd.find(dir_name)

        if uomid != -1:
            uomid_end = cwd[uomid+len(dir_name):].find('/')
            uomid = cwd[uomid+len(dir_name):] if uomid_end == -1 else cwd[uomid+len(dir_name):uomid+len(dir_name)+uomid_end]
            # dir_index = assignment_dir_list.index(uomid)
        return uomid

    def move_to_next_directory(self, assignment_dir):
        # dir_name = '/ASSIGNMENTS/'
        assignment_dir_list = next(os.walk(assignment_dir))[1] 
        # cwd = os.getcwd()
        # uomid = cwd.find(dir_name)
        uomid = self.get_uomid_of_current_dir()

        # not in a student's assignment folder, go to the first folder
        if uomid == -1:
            os.chdir(assignment_dir_list[0])
        else:
            # uomid_end = cwd[uomid+len(dir_name):].find('/')
            # uomid = cwd[uomid+len(dir_name):] if uomid_end == -1 else cwd[uomid+len(dir_name):uomid+len(dir_name)+uomid_end]
            dir_index = assignment_dir_list.index(uomid)
            if dir_index == len(assignment_dir_list)-1:
                print("No more directories available after")
                os.chdir(assignment_dir)
            else:
                os.chdir(assignment_dir + '/' + assignment_dir_list[dir_index+1])
        pass

    def move_to_prev_directory(self, assignment_dir):
        # dir_name = '/ASSIGNMENTS/'
        assignment_dir_list = next(os.walk(assignment_dir))[1] 
        # cwd = os.getcwd()
        # uomid = cwd.find(dir_name)
        uomid = self.get_uomid_of_current_dir()

        # not in a student's assignment folder, go to the first folder
        if uomid == -1:
            os.chdir(assignment_dir_list[0])
        else:
            # uomid_end = cwd[uomid+len(dir_name):].find('/')
            # uomid = cwd[uomid+len(dir_name):] if uomid_end == -1 else cwd[uomid+len(dir_name):uomid+len(dir_name)+uomid_end]
            dir_index = assignment_dir_list.index(uomid)
            if dir_index == 0:
                print("No more directories available before")
                os.chdir(assignment_dir)
            else:
                os.chdir(assignment_dir + '/' + assignment_dir_list[dir_index-1])
        pass

    def resume(self, assignment_dir, fd):
        fdlist = fd.get_student_list()
        if len(fdlist) > 0:
            last = fdlist[-1]
            all_student_list = next(os.walk(assignment_dir))[1]
            last_index = all_student_list.index(last)
            

            ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(math.floor(n/10)%10!=1)*(n%10<4)*n%10::4])
            print("The record says you were working on student %s last time, the %s in the directory." %(last, ordinal(last_index+1)))
            if self.query_yes_no("Do you want to jump there? [y/n]"):
                os.chdir(assignment_dir + '/' + all_student_list[last_index])

        else:
            print("You haven't done any work yet")
        pass

    def unit_test(self, exe, testfile, context):
        import subprocess, difflib
        expected = self.parse_test_filename(testfile)
        out = subprocess.check_output([exe, testfile])
        out = out.splitlines() 
        with open(expected) as f:
            
            if context:
                diff = difflib.context_diff(out, f.read().splitlines())
            else:
                # diff = difflib.ndiff(out, f.read().splitlines())
                # diff = difflib.unified_diff(out, f.read().splitlines())
                d = difflib.Differ()
                diff = d.compare(out, f.read().splitlines())
        print('\n'.join(diff))


    def parse_test_filename(self, filename):
        if filename.endswith('.txt'):
            return_name = filename[:-4] + '_expected.txt'
        else:
            return_name = filename + '_expected'
        
        return return_name

    # Print iterations progress
    def printProgressBar (self, iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
        """
        Call in a loop to create terminal progress bar
        @params:
            iteration   - Required  : current iteration (Int)
            total       - Required  : total iterations (Int)
            prefix      - Optional  : prefix string (Str)
            suffix      - Optional  : suffix string (Str)
            decimals    - Optional  : positive number of decimals in percent complete (Int)
            length      - Optional  : character length of bar (Int)
            fill        - Optional  : bar fill character (Str)
        """
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
        # Print New Line on Complete
        if iteration == total: 
            print()

    def query_yes_no(self, question):
        print(question)
        # raw_input returns the empty string for "enter"
        yes = {'yes','y', 'ye', ''}
        no = {'no','n'}

        while True:
            choice = input().lower()
            if choice in yes:
                return True
            elif choice in no:
                return False
            else:
                print("Please respond with 'yes' or 'no'")
        pass



# u = utility()
# u.run_executable()
# u.compile_through_makefile('/Users/mingo/Desktop/StreamlinedMarkingTool/ASSIGNMENTS/lim34521', False)   
# cr = config_reader()
# assignment_dir = cr.get_assignemnts()
# # cwd = os.getcwd()
# dir_name = '/ASSIGNMENTS/'
# cwd = '/Users/mingo/Desktop/StreamlinedMarkingTool/ASSIGNMENTS'
# uomid = cwd.find(dir_name)
# uomid_end = cwd[uomid+len(dir_name):].find('/')
# uomid = cwd[uomid+len(dir_name):] if uomid_end == -1 else cwd[uomid+len(dir_name):uomid+len(dir_name)+uomid_end]  
# # print(index)
# print(uomid)
# for dirName, subdirList, fileList in os.walk(cwd):
#     print(next(subdirList))
#     break
# dr = next(os.walk(cwd))[1].index('lim34521')
# print(dr)