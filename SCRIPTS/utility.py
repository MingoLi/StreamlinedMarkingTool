#! /usr/bin/env python
# from config_reader import config_reader
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

    def move_to_next_directory(self, assignment_dir):
        dir_name = '/ASSIGNMENTS/'
        assignment_dir_list = next(os.walk(assignment_dir))[1] 
        cwd = os.getcwd()
        uomid = cwd.find(dir_name)

        # not in a student's assignment folder, go to the first folder
        if uomid == -1:
            os.chdir(assignment_dir_list[0])
        else:
            uomid_end = cwd[uomid+len(dir_name):].find('/')
            uomid = cwd[uomid+len(dir_name):] if uomid_end == -1 else cwd[uomid+len(dir_name):uomid+len(dir_name)+uomid_end]
            dir_index = assignment_dir_list.index(uomid)
            if dir_index == len(assignment_dir_list)-1:
                print("No more directories available after")
                os.chdir(assignment_dir)
            else:
                os.chdir(assignment_dir + '/' + assignment_dir_list[dir_index+1])
        pass

    def move_to_prev_directory(self, assignment_dir):
        dir_name = '/ASSIGNMENTS/'
        assignment_dir_list = next(os.walk(assignment_dir))[1] 
        cwd = os.getcwd()
        uomid = cwd.find(dir_name)

        # not in a student's assignment folder, go to the first folder
        if uomid == -1:
            os.chdir(assignment_dir_list[0])
        else:
            uomid_end = cwd[uomid+len(dir_name):].find('/')
            uomid = cwd[uomid+len(dir_name):] if uomid_end == -1 else cwd[uomid+len(dir_name):uomid+len(dir_name)+uomid_end]
            dir_index = assignment_dir_list.index(uomid)
            if dir_index == 0:
                print("No more directories available before")
                os.chdir(assignment_dir)
            else:
                os.chdir(assignment_dir + '/' + assignment_dir_list[dir_index-1])
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
        print '\n'.join(diff)


    def parse_test_filename(self, filename):
        if filename.endswith('.txt'):
            return_name = filename[:-4] + '_expected.txt'
        else:
            return_name = filename + '_expected'
        
        return return_name



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