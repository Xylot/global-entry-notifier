from __future__ import annotations

import sys

if sys.version_info >= (3, 8):  # pragma: >=3.8 cover
    import importlib.metadata as importlib_metadata
else:  # pragma: <3.8 cover
    import importlib_metadata

VERSION = importlib_metadata.version('global_entry_notifier')

GLOBAL_ENTRY_BASE_URL = 'https://ttp.cbp.dhs.gov'
GLOBAL_ENTRY_QUERY_ENDPOINT = '/schedulerapi/slots'
GLOBAL_ENTRY_QUERY_URL = (
    f'{GLOBAL_ENTRY_BASE_URL}{GLOBAL_ENTRY_QUERY_ENDPOINT}'
)
GLOBAL_ENTRY_DEFAULT_PARAMETERS = {
    'orderBy': 'soonest',
    'minimum': 1,
    'limit': 3,
}
