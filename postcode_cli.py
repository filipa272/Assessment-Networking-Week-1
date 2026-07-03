"""A CLI application for interacting with the Postcode API."""

from argparse import ArgumentParser
from postcode_functions import get_postcodes_details, validate_postcode, get_postcode_for_location, get_postcode_completions


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "--mode", "-m", choices=['validate', 'complete'], required=True)
    parser.add_argument("postcode", type=str)
    args = parser.parse_args()

    if args.mode == "validate":
        if validate_postcode(args.postcode):
            print(f'{args.postcode.upper().strip()} is a valid postcode.')
        else:
            print(f"{args.postcode.upper().strip()} is not a valid postcode.")

    if args.mode == "complete":

        if get_postcode_completions(args.postcode):
            for postcode in get_postcode_completions(args.postcode)[:5]:
                print(f"{postcode.upper().strip()}.")
        else:

            print(f'No matches for {args.postcode.upper().strip()}.')
