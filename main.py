import os
import sys
import argparse
from argparse import ArgumentParser


def menu():
    parser = ArgumentParser(description="Choose option for fuzzing test", formatter_class=argparse.RawTextHelpFormatter,
                            epilog="For more details use the README file", add_help=False)
    required = parser.add_mutually_exclusive_group()
    required.title = "Required one of the following"
    required.add_argument('-u', "--url", type=str, default=None, help="Specify url to fuzz", metavar='', required=False)
    required.add_argument('-f', "-file", type=str, default=None, help="Specify file containing urls",
                          metavar='', required=False)
    required.add_argument('-o', "--output", type=str, default=None, help="Output the succeded fuzz test in console")
    optionalArgs = parser.add_argument_group('Optional')
    optionalArgs.add_argument('-h', '--help', action='help',
                              default=argparse.SUPPRESS, help='Show this help message and exit')
    optionalArgs.add_argument('-m', "--method", choices=['GET', 'POST'],
                              help="Specify request type ('GET' or 'POST')",
                              default='GET', metavar='', required=False)
    parser.print_help()
    pArgs = parser.parse_args()
    return pArgs


def main():
    args = menu()
    print(args.url)


if __name__ == "__main__":
    main()
