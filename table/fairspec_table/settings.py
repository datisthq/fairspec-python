from __future__ import annotations

NUMBER_COLUMN_NAME = "fairspec:number"
ERROR_COLUMN_NAME = "fairspec:error"

# Each check scans the whole source file, and polars materializes a CSV in full
# however the query is collected, so peak memory is the file size times the number
# of checks in flight. Validating a 1 GB file needed 12GB at one check per core
# against 2.0GB serially, for 5.0s against 7.4s.
INSPECT_COLUMN_CONCURRENCY = 1
INSPECT_ROW_CONCURRENCY = 1

BASE64_REGEX = (
    r"^$|^(?:[0-9a-zA-Z+/]{4})*(?:(?:[0-9a-zA-Z+/]{2}==)|(?:[0-9a-zA-Z+/]{3}=))?$"
)
HEX_REGEX = r"^[0-9a-fA-F]*$"
RFC5322_EMAIL_REGEX = r'^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$'
URL_REGEX = r"^https?://.+"
