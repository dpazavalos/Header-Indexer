# HeaderIndexer
A simple system to create a dictionary containing given keys to needed header column indexes

In order to facilitate easier spreadsheet parsing, this module aims to simplify the process of 
indexing columns by their headers. This module finds particular use in situations where spreadsheet
 column orders are inconsistent.

## Installation

```
pip install headerindexer
```

## Using HeaderIndexer
 
 
Assume we're using a spreadsheet with the following header format:
```python
["Date", "Status", "TrackingID", "VulnTitle", "DNSHostname", "OperatingSystem"]
```

Provide HeaderIndexer a dictionary like so

```python
headers_dict = {
#   reference       Header name
    "hostname":     "DNSHostname",
    "stat":         "Status"
}
```

HeaderIndexer will compare the given dictionary against the above header row, converting the
dictionary's values into the actual column indexes. The returned dictionary can be used to 
reliably call on the appropriate column by given keys ("hostname") 
even if later formats shuffle columns

In situations where header names alter ("DNSHostname" becomes "Server Hostname") the only 
adjustment needed is in the headers_dict value section.


### HeaderIndexer options

HeaderIndexer has a small set of options to fine tune it to your needs. Below are the default 
settings and their purposes

```python
raise_error = False
"""Raise ValueError If any non_indexed or duplicate headers are found. If true, no query to fix 
and nothing will return"""

return_affected = False
"""If true, Returns a Tuple[dict] (ndx_calc, non_indexed, duplicates)
If false, returns only the new ndx_calc dictionary"""

check_nonindexed = True
"""Gathers non_indexed headers into Dict[str, int]. """

check_duplicates = False
"""Gathers duplicate headers into Dict[str, int]"""

prompt_fix = True
"""Call single stage menu to fix non indexed headers by Id-ing proper headers
Note, at this time it does not check for duplicate headers"""
```

### Prompt Fix

There are three inevitabilities in life: death, taxes, and something won't work. HeaderIndexer 
tries to help with the last

if prompt_fix = True, HeaderIndexer prompts if you wish to manually identify any nonindexed headers.
If yes, key calls will prompt with headers for you to manually assign. From the menu you can ID
the proper header, mark as not found (enters into non_indexed and returns in tuple 
(if return_affected)), or simply leave the value as None.  

### Sample code

```python
from headerindexer import HeaderIndexer

indexer = HeaderIndexer(prompt_fix=True, return_affected=False).run
spreadsheet = ["Date", "Status", "TrackingID", "Title", "DNSHostname"]
headers_dict = {
    "hostname":     "DNSHostname",
    "track":        "1TrackingID1",
    "OS":           "1OperatingSystem",
    "hostname2":    "1DNSHostname"
}
ndx_calc = indexer(sheet_headers=spreadsheet, head_names=headers_dict)

print(ndx_calc)
```

### Finally...
I am as open as the Texan sky when it comes to issues, comments, and concerns. Feel free to raise 
github issues or branch if desired. 
