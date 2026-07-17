import sys
import os
from pathlib import Path
import subprocess as sp


def path_exec(filename: str):
    system_path = os.environ.get('PATH')
    path_list = system_path.split(os.pathsep)

    for directory in path_list:
        if not os.path.isdir(directory):
            continue
        
        target_dir = Path(directory)
        
        for item in target_dir.iterdir():
            if item.is_file() and item.name == filename:
                if os.access(item, os.X_OK):
                    return directory
    
    return ""
    

def main():

    builtin_cmnds = set(["echo", "exit", "type", "pwd", "cd"])

    TYPE = "type"
    ECHO = "echo"
    EXIT = "exit"
    PWD = "pwd"
    CD = "cd"
    HOME = "~"
    CAT = 'cat'


    while True:
        sys.stdout.write("$ ")

        command = input()
        command = command.strip()

        if command == EXIT:
            break

        elif ECHO in command and command.find(ECHO) == 0:
            result = ""
            open_quote = ''
            backslash = False
            
            for val in command[5:]:
                if backslash == False and (val == "'" or val == '"') and (len(open_quote) == 0 or open_quote == val):
                    if len(open_quote) > 0:
                        open_quote = ''
                    else:
                        open_quote = val

                elif val == '\\' and len(open_quote) == 0 and backslash == False:
                    backslash = True
                
                elif backslash:
                    result += val
                    backslash = False

                elif len(open_quote) > 0 or (len(open_quote) == 0 and ((val == ' ' and len(result) > 0 and result[-1] != ' ') or val != ' ')):
                    result += val

            print(result)

        elif TYPE in command and command.find(TYPE) == 0:
            in_commands = command.split(" ")

            if len(in_commands) == 2:
                if in_commands[1] in builtin_cmnds:
                    print(in_commands[1] + " is a shell builtin")

                else:
                    directory = path_exec(in_commands[1])

                    if directory == '':
                        print(in_commands[1] + ": not found")

                    else:
                        print(in_commands[1] + " is " + directory + "/" + in_commands[1])

        elif CAT in command and command.find(CAT) == 0:
            cat_params = []
            
            open_quote = ''
            backslash = False

            for i in range(4, len(command)):
                if backslash == False and (command[i] == "'" or command[i] == '"') and (len(open_quote) == 0 or open_quote == command[i]):
                    if len(open_quote) == 0:
                        open_quote = command[i]

                        if command[i-1] == ' ' and command[i-2] != ' ':
                            cat_params.append("")

                    else:
                        open_quote = ''

                elif command[i] == '\\' and backslash == False and len(open_quote) == 0:
                    backslash = True
                
                elif backslash:
                    cat_params[-1] += command[i]
                    backslash = False

                elif len(open_quote) > 0:
                    if command[i] == '\\':
                        cat_params[-1] += '\\'
                    else:
                        cat_params[-1] += command[i]
                
                elif command[i] != ' ':
                    if command[i-1] == ' ' and command[i-2] != '\\':
                        cat_params.append("")
                    
                    cat_params[-1] += command[i]

            sp.run(["cat"] + cat_params)

        elif command == PWD:
            print(Path.cwd())
        
        elif CD in command and command.find(CD) == 0:
            in_commands = command.split(" ")

            if in_commands[1] == HOME:
                os.chdir(Path.home())
                continue

            try:
                os.chdir(in_commands[1])

            except FileNotFoundError:
                print("cd: " + in_commands[1] + ": No such file or directory")

        else:
            ext_cmnd = command.split(" ")

            directory = path_exec(ext_cmnd[0])

            if directory == '':
                print(ext_cmnd[0] + ": not found")

            else:
                sp.run(ext_cmnd)
                continue


if __name__ == "__main__":
    main()
