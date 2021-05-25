#!/bin/python3

import sys

def main(name):
    print(f'Hello { name }')

if __name__ == '__main__':
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        print('Usage: hello-python.py <name>')