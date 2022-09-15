from __future__ import annotations

import argparse
import typing

import global_entry_notifier.constants
from global_entry_notifier.notifier import notify_if_available


def get_args(argv: typing.Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog='global-entry-notifier')

    parser.add_argument(
        '-V', '--version',
        action='version',
        version=f'%(prog)s {global_entry_notifier.constants.VERSION}',
    )

    parser.add_argument(
        '-l', '--locations',
        type=str,
        nargs='+',
        required=True,
        help='Interview location code(s) to check for availability',
    )

    parser.add_argument(
        '-p', '--phone-number',
        type=str,
        required=True,
        help='Your phone number',
    )

    _add_twilio_arguments(parser)

    parsed_args = parser.parse_args(argv)

    return parsed_args


def _add_twilio_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        '--twilio-sid',
        type=str,
        required=True,
        help='Twilio account SID',
    )

    parser.add_argument(
        '--twilio-token',
        type=str,
        required=True,
        help='Twilio authentication token',
    )

    parser.add_argument(
        '--twilio-number',
        type=str,
        required=True,
        help='Twilio phone number',
    )


def main(argv: typing.Sequence[str] | None = None) -> int:
    args = get_args(argv)

    notify_if_available(
        args.locations,
        args.phone_number,
        args.twilio_sid,
        args.twilio_token,
        args.twilio_number,
    )

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
