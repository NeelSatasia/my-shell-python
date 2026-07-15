import sys


def main():

    while True:
        sys.stdout.write("$ ")

        command = input()

        if command.strip() == "exit":
            break

        sys.stdout.write(command + ": command not found\n")
    
    pass


if __name__ == "__main__":
    main()
