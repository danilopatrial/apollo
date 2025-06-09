import sys
import argparse

# Python 3.8+
from importlib.metadata import version, PackageNotFoundError

def get_version():
    try:
        return version("apollo")
    except PackageNotFoundError:
        return "unknown"

def main():
    parser = argparse.ArgumentParser(prog="apollo")
    parser.add_argument('--version', action='version', version=f'%(prog)s {get_version()}')

    # Add your subcommands if needed
    args = parser.parse_args()

    # Just for demonstration
    print("You ran apollo successfully.")

if __name__ == "__main__":
    main()
