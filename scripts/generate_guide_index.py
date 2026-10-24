import os
import json
import re

DATA_PATH = "/home/singhvi28/competitive-programming/src/data/curriculumV2Data.json"
BASE_OUT_DIR = "/home/singhvi28/competitive-programming/curriculum-v2/guide"

def sanitize_filename(name: str) -> str:
    s = re.sub(r'[^\w\-\.]', '-', name.lower())
    s = re.sub(r'-+', '-', s).strip('-')
    return s

def main():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    os.makedirs(BASE_OUT_DIR, exist_ok=True)
    
    total_modules = len(data.get("modules", []))
    total_topics = sum(len(m.get("topics", [])) for m in data.get("modules", []))

    # 1. Master README.md
    master_lines = [
        "# Advanced DSA & Competitive Programming Guide: Complete Masterclass",
        "",
        "> **Comprehensive Offline Markdown Reference & Curated Knowledge Base**  ",
        f"> **Total Modules:** {total_modules} | **Total Topics:** {total_topics}  ",
        "> **Extracted from:** `curriculum-v2/guide`  ",
        "",
        "Welcome to the complete offline Markdown edition of the **Competitive Programming & Interview Mastery Curriculum V2 Guide**. Every topic contains mathematical foundations, proof sketches, closed-form invariant recurrences, contest-ready C++17 and Python 3 templates, recognition heuristics, bug traps, curated practice problems, and external reference links.",
        "",
        "---",
        "",
        "## Table of Contents by Phase & Module",
        ""
    ]

    current_phase = None
    for m in data.get("modules", []):
        sec_id = m.get("sectionId", m.get("id", "00"))
        sec_title = m.get("title", "")
        mod_id = m.get("id", f"sec-{sec_id}")
        topics = m.get("topics", [])
        phase_id = topics[0].get("phaseId") if topics else None
        phase_name = topics[0].get("phaseName") if topics else None

        if phase_id != current_phase:
            current_phase = phase_id
            master_lines.append(f"### Phase {phase_id}: {phase_name}\n")

        sec_dir = os.path.join(BASE_OUT_DIR, mod_id)
        os.makedirs(sec_dir, exist_ok=True)

        master_lines.append(f"#### [§{sec_id} {sec_title}](./{mod_id}/README.md) ({len(topics)} topics)\n")

        # Create Section README.md
        sec_lines = [
            f"# Section §{sec_id}: {sec_title}",
            "",
            f"> **Module ID:** `{mod_id}`  ",
            f"> **Phase:** Phase {phase_id} — {phase_name}  ",
            f"> **Topic Count:** {len(topics)}  ",
            "",
            f"**Module Summary:** {m.get('summary', 'Advanced contest-level algorithms and data structures.')}",
            "",
            "---",
            "",
            "## Topics in this Section",
            "",
            "| # | Topic Title | ROI | Rating | Frequency | Markdown Guide |",
            "|---|---|---|---|---|---|"
        ]

        for t_idx, t in enumerate(topics, 1):
            t_id = t.get("id", f"topic-{t_idx}")
            clean_slug = sanitize_filename(t_id)
            idx_prefix = f"{t_idx:02d}"
            filename = f"{idx_prefix}-{clean_slug}.md"
            title = t.get("title", f"Topic {t_idx}")
            roi = t.get("roi", "A-tier")
            rating = t.get("ratingRange", "1600–2200")
            freq = t.get("frequency", "Common")

            sec_lines.append(f"| {t_idx} | {title} | `{roi}` | {rating} | {freq} | [{filename}](./{filename}) |")
            master_lines.append(f"- [{title}](./{mod_id}/{filename}) — `{roi}` | `{rating}`")

        master_lines.append("")

        with open(os.path.join(sec_dir, "README.md"), "w", encoding="utf-8") as sec_f:
            sec_f.write("\n".join(sec_lines) + "\n")

    with open(os.path.join(BASE_OUT_DIR, "README.md"), "w", encoding="utf-8") as master_f:
        master_f.write("\n".join(master_lines) + "\n")

    print(f"Master index and {total_modules} section READMEs generated successfully.")

if __name__ == "__main__":
    main()
