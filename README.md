# StreamlinedMarkingTool
This project is looking to streamline the marking process by using Python on Linux. A command-line tool will be introduced, where the marker can view the student’s files, run the code, view the output. Unit tests will be supported and can be accessed from a configurable location. As a result, a CSV file will be produced listing the student’s marks, and other related information.

# How to run
- Install module `cmd2`
Find `shell.py` in `SCRIPTS`, type `python shell.py` to start
- Linux commands are still available by adding `!` before the command, e.g. `!ls`
- Frequently used commands can be executed without `!`, including `ls`, `cd`, `pwd`

# Function achieved
- Configuration reader
    - All configurations integrated into a single file
    - Can be read from `class config_reader`
- Use costum editor by running `set editor <your editor>`, or change it with `editor = 'vim'` in shell.py
    - including `vim`, `code` ..., visual studio code by default
    - use editor with command `edit file.txt`...
- Late submit check
    - Will automatically generate a dictionary `<id, submition date>` object based on the `HANDIN_LOG`
- `Help` for commands
    - shortcuts: `?<cmd_name>`, e.g. `?pd`
- Automate compilation: if a makefile is contained in assignment folder, `make` can be used to compile the source code
    - `make` will search for makefile and compile accordingly, more info in `help make`
    - `-r` is supported to compile the sub-directory recursively
- `next` and `prev` helps you navigate between student's assignment folder
- Run executable through command `run`
    - e.g. `run ./a.out`
- Unit test with given input file and expected output. 
    - More details on command `?test`
    - e.g. `test <program> <input.txt> [-c]`
- Leave feedback to students using pre-define sentences. 
    - e,g. `fd <feedback> <mark deduction>`
    - `fdlist` to list all avaliable abbreviation for feedback sentences

# Yet to be finished
- Track the grading progress and be able to resume
- grades statistics
- Email notification

# Open source used:  
- cmd2    
https://pypi.org/project/cmd2/  
