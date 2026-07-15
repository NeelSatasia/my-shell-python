import sys


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
                    print(in_commands[1] + ": not found")

        else:
            sys.stdout.write(command + ": command not found\n")
    
    pass


if __name__ == "__main__":
    main()
