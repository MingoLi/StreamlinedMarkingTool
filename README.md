# StreamlinedMarkingTool
This project is looking to streamline the marking process by using Python on Linux. A command-line tool will be introduced, where the marker can view the student’s files, run the code, view the output. Unit tests will be supported and can be accessed from a configurable location. As a result, a CSV file will be produced listing the student’s marks, and other related information. An notification email will be sent to each student including the feedback and the final mark they gained.

# How to run
- Install module `cmd2`, type `./start.sh` to start (you may need to run `chmod +x start.sh` first)  
- `quit` or `exit` to terminate
- Linux commands are still available by adding `!` before the command, e.g. `!ls`
- Frequently used commands can be executed without `!`, including `ls`, `cd`, `pwd`

# Function achieved

## General
- Configuration reader
    - All configurations integrated into a single file under CONFIGURATION/config.ini
    - Can be read from `class config_reader`
- Use costum editor by running `set editor <your editor>`, or change it with `editor = 'vim'` in shell.py
    - including `vim`, `code` ..., visual studio code by default
    - use editor with command `edit file.txt`...
- Late submit check
    - Will automatically generate a dictionary `<id, submition date>` object based on the `HANDIN_LOG`
    - `list_late_submit` to check exact id and submission time
- `Help` for commands
    - shortcuts: `?<cmd_name>`, e.g. `?pd`
- Add Tab-completion for build-in commands 
    - supported by `gnureadline`, module install required
  
## Directory Navigation
- `next` and `prev` helps you navigate between student's assignment folder without using `cd`s
    - use `resume` to quickly go back to the place you stopped last time

## Productivity Functions
- Automate compilation: if a makefile is contained in assignment folder, `make` can be used to compile the source code
    - `make` will search for makefile and compile accordingly, more info in `help make`
    - `-r` is supported to compile the sub-directory recursively
- Run executable through command `run`
    - e.g. `run ./a.out`
- Unit test with given input file and expected output. 
    - More details on command `?test`
    - e.g. `test <program> <input.txt> [-c]`
- Leave feedback to students using pre-define sentences. 
    - e,g. `fd <feedback> <mark deduction>`
    - `fdlist` to list all avaliable abbreviation for feedback sentences
    - `check` command to check which student(s) do not have any feedback yet, print nothing if no one is left
    - `fdhis` to show all the feedbacks assigned to a certain student, has to be used under a student's assignement direcotory
- `bonus` to support giving bonus mark, same usage as leaving a feedback

## Automation Functions
- Statistic generation: add the support of generating the csv file including the grade of all student based on given feedback and mark deducted
    - `gencsv` to generate the file and the file can be found under /GRADES/xxx.csv
    - Note: for students who have no feedback being assigned will be considered as full mark when using flag `-f` or `--force`

- Add Email Notification
    - `send_email` or `notify` will send each student an email include their feedback and mark gained
    - using flag `-c` or `--check` will ONLY create the email body in txt file and store under EMAIL BACKUP folder and will NOT actully send it, and will NOT be logged.

# Open source used:  
- cmd2    
https://pypi.org/project/cmd2/  
- gnureadline
https://pypi.org/project/gnureadline/