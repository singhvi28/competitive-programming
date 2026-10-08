import os
import glob
import re
import json

ADV_DSA_DIR = "/home/singhvi28/Desktop/adv-dsa"

# 1. Parse 00-roi-map.md
def parse_roi_map():
    path = os.path.join(ADV_DSA_DIR, "00-roi-map.md")
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    roi_dict = {}
    table_match = re.search(r"## Full Technique Table\s*\n\s*\|[^\n]+\|\s*\n\s*\|[-|\s]+\|\s*\n([\s\S]+?)(?=\n##|\Z)", content)
    if table_match:
        rows = table_match.group(1).strip().split("\n")
        for row in rows:
            cols = [c.strip() for c in row.split("|")[1:-1]]
            if len(cols) >= 6:
                topic, roi, freq, diff, prereq, rating = cols[:6]
                key = topic.lower().strip()
                roi_dict[key] = {
                    "topic": topic,
                    "roi": roi,
                    "frequency": freq,
                    "difficulty": diff,
                    "prerequisites": prereq,
                    "ratingRange": rating
                }
    return roi_dict

roi_map = parse_roi_map()
print(f"Parsed {len(roi_map)} ROI map entries")
for k, v in list(roi_map.items())[:10]:
    print(f"  {v['topic']}: {v['roi']} | {v['frequency']} | {v['ratingRange']}")

def parse_master_cheat_sheet():
    path = os.path.join(ADV_DSA_DIR, "99-master-cheat-sheet.md")
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    sections = []
    # Split by ## Section
    sec_chunks = re.split(r"\n##\s+", content)
    for chunk in sec_chunks[1:]: # Skip header
        lines = chunk.strip().split("\n")
        sec_header = lines[0].strip()
        
        # Subtopics by ###
        sub_chunks = re.split(r"\n###\s+", "\n".join(lines[1:]))
        subtopics = []
        for s in sub_chunks:
            s_lines = s.strip().split("\n")
            topic_name = s_lines[0].strip()
            if not topic_name or topic_name.startswith("Hub:"):
                continue
            
            body = "\n".join(s_lines[1:])
            
            rec_match = re.search(r"→\s*Recognition clue:\s*(.+)", body)
            idea_match = re.search(r"→\s*Core idea:\s*(.+)", body)
            comp_match = re.search(r"→\s*Complexity:\s*(.+)", body)
            tmpl_match = re.search(r"→\s*Main template/function name:\s*(.+)", body)
            use_match = re.search(r"→\s*Most common use case:\s*(.+)", body)
            file_match = re.search(r"→\s*Section:\s*\[([^\]]+)\]\(([^)]+)\)", body)
            
            subtopics.append({
                "topic": topic_name,
                "recognitionClue": rec_match.group(1).strip() if rec_match else "",
                "coreIdea": idea_match.group(1).strip() if idea_match else "",
                "complexity": comp_match.group(1).strip() if comp_match else "",
                "mainTemplate": tmpl_match.group(1).strip() if tmpl_match else "",
                "commonUseCase": use_match.group(1).strip() if use_match else "",
                "sectionFile": file_match.group(2).strip() if file_match else ""
            })
            
        sections.append({
            "sectionTitle": sec_header,
            "subtopics": subtopics
        })
    return sections

cheat_sheet = parse_master_cheat_sheet()
print(f"Parsed {len(cheat_sheet)} cheat sheet sections with total {sum(len(s['subtopics']) for s in cheat_sheet)} subtopics")
for s in cheat_sheet[:5]:
    print(f"  Section: {s['sectionTitle']} -> {len(s['subtopics'])} subtopics")
