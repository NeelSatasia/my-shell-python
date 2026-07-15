import sys


def main():

    while True:
        sys.stdout.write("$ ")

        command = input()
        command = command.strip()

        if command == "exit":
            break
        elif "echo" in command and command.find("echo") == 0:
            print(command[5:])
        else:
            sys.stdout.write(command + ": command not found\n")
    
    pass


if __name__ == "__main__":
    main()
