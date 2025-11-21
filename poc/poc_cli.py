#!/usr/bin/env python3

import argparse
import sys


def detect_weather_chart(image_path: str):
    print(f"[POC] Pretending to analyze: {image_path}")
    print("Result: This appears to be a weather chart.")


def main(argv=None):
    parser = argparse.ArgumentParser(description="POC CLI for weather project")

    parser.add_argument(
        "--image", type=str, required=True, help="Path to the input image"
    )

    args = parser.parse_args(argv)

    detect_weather_chart(args.image)


if __name__ == "__main__":
    main()
