#
# Weather Forecast + Salesforce
#
# License:
#   MIT License
#
# Enjoy coding! 🛸
# ==========================================

import argparse


def main(argv=None):
    parser = argparse.ArgumentParser(description="Weather Forecast + Salesforce")
    parser.add_argument(
        "--run",
        action="store_true",
        help="Must have for every execution; prevents accidental execution.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force execution without checking the same PDF; good for demo and debug.",
    )

    args = parser.parse_args(argv)

    print(args.run)
    print(args.force)

    if not args.run:
        parser.error("Missing --run. This flag is required to execute the program.")

    if args.force:
        # Placeholder for force execution logic
        pass


if __name__ == "__main__":
    main()
