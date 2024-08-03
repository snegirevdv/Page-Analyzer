from collections import defaultdict
from typing import List, Dict


def merge_entries(entries: List[Dict], checks: List[Dict]) -> List[Dict]:
    merged_dict = defaultdict(dict)

    for entry in entries:
        merged_dict[entry["id"]].update(entry)

    for check in checks:
        merged_dict[check["url_id"]].update(check)

    return [merged_dict[key] for key in sorted(merged_dict, reverse=True)]

