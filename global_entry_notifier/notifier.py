from __future__ import annotations

import datetime

import requests
import twilio.rest

import global_entry_notifier.constants


def notify_if_available(
    locations: list[str],
    phone_number: str,
    twilio_sid: str,
    twilio_token: str,
    twilio_number: str,
) -> None:
    available_slots = {}

    for location in locations:
        location_slots = _get_location_availability(location)

        if location_slots:
            available_slots[location] = [
                _sanitize_timestamp(slot['startTimestamp'])
                for slot in location_slots
            ]

    if available_slots:
        _notify_sms(
            available_slots,
            phone_number,
            twilio_sid,
            twilio_token,
            twilio_number,
        )


def _get_location_availability(location: str) -> list[dict[str, str]]:
    parameters = {
        **global_entry_notifier.constants.GLOBAL_ENTRY_DEFAULT_PARAMETERS,
        **{'locationId': location},
    }

    response = requests.get(
        global_entry_notifier.constants.GLOBAL_ENTRY_QUERY_URL,
        params=parameters,  # type: ignore
    )

    if not response.ok:
        raise SystemExit(
            'Could not obtain availability information. Exiting...',
        )

    return response.json()


def _sanitize_timestamp(timestamp: str) -> str:
    original_timestamp = datetime.datetime.strptime(
        timestamp, '%Y-%m-%dT%H:%M',
    )
    sanitized_timestamp = original_timestamp.strftime('%a, %b %d @ %I:%M%p')

    return sanitized_timestamp


def _notify_sms(
    available_slots: dict[str, list[str]],
    phone_number: str,
    twilio_sid: str,
    twilio_token: str,
    twilio_number: str,
) -> None:
    twilio_client = twilio.rest.Client(twilio_sid, twilio_token)
    message_body = _create_sms_message_body(available_slots)

    twilio_client.messages.create(
        body=message_body, to=phone_number, from_=twilio_number,
    )


def _create_sms_message_body(available_slots: dict[str, list[str]]) -> str:
    message_body = 'New Global Entry appointments:\n\n'

    for location, slots in available_slots.items():
        message_body += f'Location {location}:\n'

        for slot in slots:
            message_body += f'\t{slot}\n'

        message_body += '\n'

    message_body += (
        f'Schedule: {global_entry_notifier.constants.GLOBAL_ENTRY_BASE_URL}'
    )

    return message_body
