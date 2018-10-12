# StreamlinedMarkingTool
This project is looking to streamline the marking process by using Python on Linux. A command-line tool will be introduced, where the marker can view the student’s files, run the code, view the output. Unit tests will be supported and can be accessed from a configurable location. As a result, a CSV file will be produced listing the student’s marks, and other related information.

# How to run
In shell, type `python shell.py` to start
- Linux commands are still available by adding `!` before the command, e.g. `!ls`
- Frequently used commands can be executed without `!`, including `ls`, `cd`

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


# Open source used:  
- cmd2    
https://pypi.org/project/cmd2/  
- configparser   
https://docs.python.org/3/library/configparser.html#supported-ini-file-structure
