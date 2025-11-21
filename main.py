#
# Weather Forecast + Salesforce
#
# License:
#   MIT License
#
# Enjoy coding! 🛸
# ==========================================

import argparse
import sys


def main(argv=None):
    parser = argparse.ArgumentParser(description="Weather Forecast + Salesforce")
    parser.add_argument(
        "--run",
        action="store_true",
        required=True,
        help="must have for every execution preventing accidental execution.",
    )
    parser.add_argument(
        "--force",
        default=False,
        action="store_true",
        required=False,
        help="force execution w/o checking the same PDF. good for demo and debug.",
    )

    args = parser.parse_args(argv)

    print(args.run)
    print(args.force)

    if args.force:
        pass


if __name__ == "__main__":
    main()
