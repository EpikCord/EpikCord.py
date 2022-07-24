import argparse

from .__init__ import  __version__


parser = argparse.ArgumentParser()
parser.add_argument(
    "-v","--version", help="displays the version of the library", action="store_true"
)


def info():
    print(
        f"Version {__version__} of EpikCord.py, written by the organization EpikCord. "
        "This is an unstable build and may contain bugs. "
        "Please report any bugs to https://github.com/EpikCord/EpikCord.py/issues."
    )


def parse_args(args: argparse.ArgumentParser):
    args = parser.parse_args()
    if args.version:
        info()
    else:
        print("Error: Program called with no switches")
        parser.print_help()
        parser.exit(0)






if __name__ == "__main__":
    parse_args(parser)
