"""Small CLI helpers for managing Perplexity API key and session."""
import os
import sys
from argparse import ArgumentParser

from .config import save_api_key_to_keyring, get_api_key


def store_key(args):
    key = args.key
    if not key:
        print("Please provide an API key using --key")
        return 2
    ok = save_api_key_to_keyring(key)
    if ok:
        print("API key saved to system keyring.")
        return 0
    else:
        print("Failed to save API key to keyring. Consider setting PERPLEXITY_API_KEY env var.")
        return 1


def show_key(args):
    key = get_api_key()
    if key:
        print("API key is configured (hidden for safety).")
    else:
        print("No API key found in env or keyring.")


def main(argv=None):
    p = ArgumentParser(prog="perplexity-cli")
    sub = p.add_subparsers(dest="cmd")

    s = sub.add_parser("store-key", help="Store API key in system keyring")
    s.add_argument("--key", help="API key to store")
    s.set_defaults(func=store_key)

    g = sub.add_parser("show-key", help="Check if API key is configured")
    g.set_defaults(func=show_key)

    args = p.parse_args(argv)
    if not hasattr(args, "func"):
        p.print_help()
        return 2
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
