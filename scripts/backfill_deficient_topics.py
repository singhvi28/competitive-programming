import os
import json
import sys

# Append scripts directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import backfill_data_g1
import backfill_data_g2
import backfill_data_g3
import backfill_data_g4

DATA_PATH = "/home/singhvi28/competitive-programming/src/data/curriculumV2Data.json"
BASE_OUT_DIR = "/home/singhvi28/competitive-programming/curriculum-v2/guide"

SKIPPED_MODULES = {"sec-19", "sec-20", "sec-21"}

def main():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    all_backfill = {}
    all_backfill.update(backfill_data_g1.G1_DATA)
    all_backfill.update(backfill_data_g2.G2_DATA)
    all_backfill.update(backfill_data_g3.G3_DATA)
    all_backfill.update(backfill_data_g4.G4_DATA)

    print(f"Loaded {len(all_backfill)} backfill topic definitions.")

    fields_to_check = [
        "whyItMatters",
        "coreIntuition",
        "derivation",
        "templateCpp",
        "recognitionPatterns",
        "commonBugs"
    ]

    updated_count = 0
    non_greedy_topics = 0

    for m in data.get("modules", []):
        m_id = m.get("id")
        if m_id in SKIPPED_MODULES:
            print(f"Skipping module {m_id} per user instruction.")
            continue

        for t in m.get("topics", []):
            non_greedy_topics += 1
            t_id = t.get("id")
            if t_id in all_backfill:
                bf = all_backfill[t_id]
                was_updated = False
                for field in fields_to_check:
                    val = t.get(field)
                    # Check if empty (None, empty str, empty list)
                    is_empty = False
                    if val is None:
                        is_empty = True
                    elif isinstance(val, str) and not val.strip():
                        is_empty = True
                    elif isinstance(val, list) and len(val) == 0:
                        is_empty = True

                    if is_empty and field in bf and bf[field]:
                        t[field] = bf[field]
                        was_updated = True

                if was_updated:
                    updated_count += 1

    print(f"Backfill applied to {updated_count} topics across {non_greedy_topics} non-greedy topics.")

    # Save updated data
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print("Successfully saved updated curriculumV2Data.json.")

if __name__ == "__main__":
    main()
