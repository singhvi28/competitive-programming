import os
import json
import glob

DATA_PATH = "/home/singhvi28/competitive-programming/src/data/curriculumV2Data.json"
BASE_OUT_DIR = "/home/singhvi28/competitive-programming/curriculum-v2/guide"

def main():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    expected_topics = []
    for m in data.get("modules", []):
        for t in m.get("topics", []):
            expected_topics.append((m["id"], t["id"], t["title"]))

    print(f"Total expected topics across modules: {len(expected_topics)}")

    # Check directories
    module_dirs = [m["id"] for m in data.get("modules", [])]
    missing_dirs = []
    for md in module_dirs:
        dirpath = os.path.join(BASE_OUT_DIR, md)
        if not os.path.isdir(dirpath):
            missing_dirs.append(md)

    if missing_dirs:
        print(f"Missing module directories: {missing_dirs}")
    else:
        print("All 22 module directories exist.")

    # Check files
    all_md_files = glob.glob(os.path.join(BASE_OUT_DIR, "sec-*", "*.md"))
    # Filter out README.md
    topic_files = [f for f in all_md_files if not os.path.basename(f) == "README.md"]
    print(f"Found {len(topic_files)} topic markdown files on disk.")

    # Check for empty files
    empty_files = [f for f in topic_files if os.path.getsize(f) == 0]
    if empty_files:
        print(f"WARNING: Found {len(empty_files)} empty files!")
    else:
        print("All topic markdown files have non-zero size.")

    # Check Master README and Section READMEs
    master_readme = os.path.join(BASE_OUT_DIR, "README.md")
    if os.path.exists(master_readme):
        print(f"Master README exists ({os.path.getsize(master_readme)} bytes).")
    else:
        print("WARNING: Master README missing!")

    sec_readmes = [os.path.join(BASE_OUT_DIR, md, "README.md") for md in module_dirs]
    missing_readmes = [r for r in sec_readmes if not os.path.exists(r)]
    if missing_readmes:
        print(f"Missing section READMEs: {missing_readmes}")
    else:
        print(f"All {len(sec_readmes)} section READMEs exist.")

if __name__ == "__main__":
    main()
