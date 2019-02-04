""""""A simple system to create a dict containing key calls to header column indexes

In order to facilitate easier header enabled spreadsheet parsing, this module aims to simplify the
process of column indexing, by using a given dictionary of reference keys to header values and
returning a dictionary of those same reference keys with the stated headers' column index

    Assuming we're using header row...
header_row = ["Date", "Status", "TrackingID", "VulnTitle", "DNSHostname", "OperatingSystem"]
    Create and provide a head_names dict like so

headers_dict = {
    "hostname":     "DNSHostname",
    "stat":         "Status"
}

index_headers(sheet_headers=header_row, head_names=headers_dict) will return

ndx_calc = {
    "hostname": 4,
    "stat": 1
}
"""
from typing import List


def build_ndx_calc(csv_headers: List[str], head_names: dict) -> dict:
    """Builds and returns an Index calc dict based on the provided header row\n
    Provide headers row and head names dictionary"""

    # A dictionary of all header names from given CSV
    # For each column header, ndx_all[header] = header's index
    ndx_all = {}
    index = 0
    for header in csv_headers:
        ndx_all[header] = index
        index += 1

    # Create new NEW_NDX entries based on HEAD_NAMES entries, using indexes stored in ndx_all
    ndx_calc = {}
    for Key, Val in head_names.items():
        try:
            ndx_calc[Key] = ndx_all[Val]
        except (IndexError, KeyError):
            ndx_calc[Key] = None

    # Check for duplicate indexes or non indexed headers
    duplicates = []
    nonindexed = []
    dup_check = {}
    for key, val in ndx_calc.items():
        if val is None:
            nonindexed.append([key, val])
        dup_check.setdefault(val, set()).add(key)
    for Val in dup_check.values():
        if len(Val) > 1:
            for k in Val:
                duplicates.append([k, ndx_calc[k]])

    if duplicates:
        print("Error: Duplcate header indexes!")
        print('\n'.join(str(x) for x in duplicates), '\n')

    if nonindexed:
        print("Error: Non indexed headers!")
        print('\n'.join(str(x) for x in nonindexed), '\n')

    if duplicates or nonindexed:
        print('\n'.join(str([x, y]) for x, y in ndx_calc.items()), '\n')
        exit(1)

    return ndx_calc
