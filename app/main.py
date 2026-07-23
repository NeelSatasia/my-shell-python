import sys
import os
from pathlib import Path
import subprocess as sp


builtin_cmnds = ("echo", "exit", "type", "pwd", "cd")

TYPE = "type"
ECHO = "echo"
EXIT = "exit"
PWD = "pwd"
CD = "cd"
HOME = "~"
CAT = 'cat'
LS = 'ls'
STDOUT_REDIRECTS = ('>', '1>', '>>', '1>>')
STDERR_REDIRECTS = ('2>', '2>>')

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


def clean_raw_cmnd(full_cmnd: str):
    cmnd_params = []
    open_quote = ''
    backslash = False
    empty_space = False

    for i in range(len(full_cmnd)):
        if backslash == False and (full_cmnd[i] == "'" or full_cmnd[i] == '"') and (len(open_quote) == 0 or open_quote == full_cmnd[i]):
            if len(open_quote) == 0:
                open_quote = full_cmnd[i]
                
                if i == 0 or empty_space:
                    cmnd_params.append("")
                    empty_space = False

            else:
                open_quote = ''

        elif full_cmnd[i] == '\\' and backslash == False and (len(open_quote) == 0 or (open_quote == '"' and i + 1 < len(full_cmnd) and (full_cmnd[i+1] == '"' or full_cmnd[i+1] == '\\'))):
            backslash = True
        
        elif backslash:
            if empty_space:
                cmnd_params.append("")
                empty_space = False

            cmnd_params[-1] += full_cmnd[i]
            backslash = False

        elif len(open_quote) > 0:
            cmnd_params[-1] += full_cmnd[i]
        
        elif full_cmnd[i] == ' ' and empty_space == False:
            empty_space = True

        elif full_cmnd[i] != ' ':
            if i == 0 or empty_space:
                cmnd_params.append("")
                empty_space = False
            
            cmnd_params[-1] += full_cmnd[i]

    return cmnd_params


def find_redirect(cmnd: list[str]):
    i = 1
    while i < len(cmnd):
        if cmnd[i] in STDOUT_REDIRECTS or cmnd[i] in STDERR_REDIRECTS:
            return i
        else:
            i += 1
    
    return -1

def main():

    while True:
        sys.stdout.write("$ ")

        raw_cmnd = input()
        raw_cmnd = raw_cmnd.strip()

        clean_cmnd = clean_raw_cmnd(raw_cmnd)

        if len(clean_cmnd) == 0:
            continue

        redirect_idx = find_redirect(clean_cmnd)

        if clean_cmnd[0] == EXIT:
            break

        elif clean_cmnd[0] == ECHO:           
            if redirect_idx > -1:
                input_txt = " ".join(clean_cmnd[1:redirect_idx])

                file_path = Path(clean_cmnd[-1])

                mode = 'w'

                if clean_cmnd[redirect_idx] in STDOUT_REDIRECTS[2:] or clean_cmnd[redirect_idx] == STDERR_REDIRECTS[1]:
                    mode = 'a'

                if clean_cmnd[redirect_idx] in STDERR_REDIRECTS:
                    with open(file_path, mode) as f:
                        f.write("")

                    print(" ".join(clean_cmnd[1:redirect_idx]))
                
                else:
                    with open(file_path, mode) as f:
                        f.write(input_txt + "\n")

            else:
                print(" ".join(clean_cmnd[1:]))


        elif clean_cmnd[0] == TYPE:

            if len(clean_cmnd) == 2:
                if clean_cmnd[1] in builtin_cmnds:
                    print(clean_cmnd[1] + " is a shell builtin")

                else:
                    directory = path_exec(clean_cmnd[1])

                    if directory == '':
                        print(clean_cmnd[1] + ": not found")

                    else:
                        print(clean_cmnd[1] + " is " + directory + "/" + clean_cmnd[1])

        elif clean_cmnd[0] == CAT:

            if redirect_idx > -1:
                combined_text = ""

                valid_params = [CAT]

                for j in range(1, redirect_idx):
                    
                    file_path = Path(clean_cmnd[j])
                    error_message = CAT + ": " + clean_cmnd[j] + ": No such file or directory"

                    file_exists = file_path.is_file()

                    if file_exists:
                        if clean_cmnd[redirect_idx] in STDOUT_REDIRECTS:
                            f = open(file_path)
                            combined_text += f.read()
                        
                        else:
                            valid_params.append(clean_cmnd[j])

                    elif clean_cmnd[redirect_idx] in STDERR_REDIRECTS:
                        combined_text += error_message + "\n"
                        
                    else:
                        print(error_message)

                if len(valid_params) > 1:
                    sp.run(valid_params)

                mode = 'w'

                if clean_cmnd[redirect_idx] in STDOUT_REDIRECTS[2:] or clean_cmnd[redirect_idx] == STDERR_REDIRECTS[1]:
                    mode = 'a'

                with open(clean_cmnd[-1], mode) as file:
                    file.write(combined_text)

            else:
                sp.run(clean_cmnd)

        elif clean_cmnd[0] == PWD:
            print(Path.cwd())
        
        elif clean_cmnd[0] == CD:
            if clean_cmnd[1] == HOME:
                os.chdir(Path.home())
                continue
            
            try:
                os.chdir(clean_cmnd[1])

            except FileNotFoundError:
                print(CD + ": " + clean_cmnd[1] + ": No such file or directory")

        elif len(clean_cmnd) >= 2 and clean_cmnd[0] == LS and clean_cmnd[1] == "-1":
            if redirect_idx > -1:
                dir_items = []
                errors = []

                for j in range(2, redirect_idx):
                
                    dir_path = Path(clean_cmnd[j])
                    dir_exists = os.path.isdir(dir_path)

                    if dir_exists:
                        dir_items.extend(os.listdir(dir_path))
                    
                    else:
                        errors.append(LS + ": " + clean_cmnd[j] + ": No such file or directory")
                        

                dir_items.sort()

                file_path = Path(clean_cmnd[-1])

                mode = 'w'

                if clean_cmnd[redirect_idx] in STDOUT_REDIRECTS[2:] or clean_cmnd[redirect_idx] == STDERR_REDIRECTS[1]:
                    mode = 'a'

                if clean_cmnd[redirect_idx] in STDOUT_REDIRECTS:
                    for error in errors:
                        print(error)

                    with open(file_path, mode) as file:
                        for dir_item in dir_items:
                            file.write(dir_item + "\n")
                
                elif clean_cmnd[redirect_idx] in STDERR_REDIRECTS:
                    for dir_item in dir_items:
                        print(dir_item)

                    with open(file_path, mode) as file:
                        for error in errors:
                            file.write(error + "\n")
        
        else:
            directory = path_exec(clean_cmnd[0])

            if directory == '':
                print(clean_cmnd[0] + ": not found")

            else:
                sp.run(clean_cmnd)


if __name__ == "__main__":
    main()
