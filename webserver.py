import socket
import sys

def checkNumArgs(argv):
    if len(argv) != 1 and len(argv) != 2:
        print("Incorrect number of arguments")
        exit(1)

def main():
    args = sys.argv

    if len(args) > 1:
        port = args[1]
    else:
        port = 28333


if __name__ == "__main__":
    main()