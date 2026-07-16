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

    valid_commands = set(["echo", "type"])

    builtin_cmnds = set(["echo", "exit", "type"])


    while True:
        sys.stdout.write("$ ")

        command = input()
        command = command.strip()

        if command == "exit":
            break

        elif "echo" in command and command.find("echo") == 0:
            print(command[5:])

        elif "type" in command and command.find("type") == 0:
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
