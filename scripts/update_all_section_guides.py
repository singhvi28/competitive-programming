import os
import json
import re

DATA_PATH = "/home/singhvi28/competitive-programming/src/data/curriculumV2Data.json"
BASE_OUT_DIR = "/home/singhvi28/competitive-programming/curriculum-v2/guide"
SKIPPED_MODULES = {"sec-19", "sec-20", "sec-21"}

def sanitize_filename(name: str) -> str:
    s = re.sub(r'[^\w\-\.]', '-', name.lower())
    s = re.sub(r'-+', '-', s).strip('-')
    return s

def format_equation(eq_str: str) -> str:
    eq = eq_str.strip()
    if eq.startswith("$$") and eq.endswith("$$"):
        return eq
    return f"$$\n{eq}\n$$"

def format_topic_markdown(t: dict, section_id: str, section_title: str, topic_idx: int, is_embedded: bool = False) -> str:
    lines = []
    title = t.get("title", f"Topic {topic_idx}")
    h_prefix = "###" if is_embedded else "#"
    lines.append(f"{h_prefix} {topic_idx}. {title}\n")
    
    # Metadata badges / header
    sec_id = t.get("sectionId", section_id)
    sec_title = t.get("sectionTitle", section_title)
    phase_id = t.get("phaseId", 1)
    phase_name = t.get("phaseName", "Core Curriculum")
    roi = t.get("roi", "A-tier")
    rating_range = t.get("ratingRange", "1600–2200")
    frequency = t.get("frequency", "Common")
    prereqs = t.get("prerequisites", "")

    lines.append(f"> **Section:** §{sec_id} {sec_title}  ")
    lines.append(f"> **Phase:** Phase {phase_id} — {phase_name}  ")
    lines.append(f"> **Contest ROI:** {roi} | **Rating Range:** {rating_range} | **Frequency:** {frequency}  ")
    if prereqs:
        lines.append(f"> **Prerequisites:** {prereqs}  ")
    lines.append("\n---\n")

    sub_h = "####" if is_embedded else "##"

    # Section 1: Contest Payoff & Why It Matters
    if t.get("whyItMatters"):
        lines.append(f"{sub_h} 1. Contest Payoff & Why It Matters\n")
        lines.append(f"{t.get('whyItMatters').strip()}\n\n---\n")

    # Section 2: Theoretical Deep-Dive & Mathematical Mechanics
    ext = t.get("extendedTheory")
    if ext:
        lines.append(f"{sub_h} 2. Theoretical Deep-Dive & Mathematical Mechanics\n")
        sub_sub_h = "#####" if is_embedded else "###"
        if ext.get("overview"):
            lines.append(f"{sub_sub_h} Overview\n\n{ext.get('overview').strip()}\n")
        if ext.get("keyTheorems"):
            lines.append(f"{sub_sub_h} Fundamental Theorems & Invariants\n")
            for th in ext.get("keyTheorems", []):
                lines.append(f"- {th.strip()}")
            lines.append("")
        if ext.get("algorithmSteps"):
            lines.append(f"{sub_sub_h} Algorithmic Execution Blueprint\n")
            for idx, step in enumerate(ext.get("algorithmSteps", []), 1):
                lines.append(f"{idx}. {step.strip()}")
            lines.append("")
        if ext.get("invariantsAndFormulas"):
            lines.append(f"{sub_sub_h} Closed-Form Invariant Equations\n\n{format_equation(ext.get('invariantsAndFormulas'))}\n")
        if ext.get("edgeCases"):
            lines.append(f"{sub_sub_h} Structural Edge Cases & Assumptions\n")
            for ec in ext.get("edgeCases", []):
                lines.append(f"- {ec.strip()}")
            lines.append("")
        lines.append("---\n")

    # Section 3: Core Intuition & Problem Framing
    if t.get("coreIntuition"):
        lines.append(f"{sub_h} 3. Core Intuition & Problem Framing\n\n{t.get('coreIntuition').strip()}\n\n---\n")

    # Section 4: Proof Sketches & Recurrences
    if t.get("derivation"):
        lines.append(f"{sub_h} 4. Proof Sketches & Recurrences\n\n{t.get('derivation').strip()}\n\n---\n")

    # Section 5: Contest-Ready Implementation Templates
    if t.get("templateCpp") or t.get("templatePython") or t.get("complexity"):
        lines.append(f"{sub_h} 5. Contest-Ready Implementation Templates\n")
        if t.get("complexity"):
            lines.append(f"**Operational Complexity:** `{t.get('complexity').strip()}`\n")
        sub_sub_h = "#####" if is_embedded else "###"
        if t.get("templateCpp"):
            lines.append(f"{sub_sub_h} C++17 Template\n\n```cpp\n" + t.get("templateCpp").strip() + "\n```\n")
        if t.get("templatePython"):
            lines.append(f"{sub_sub_h} Python 3 Template\n\n```python\n" + t.get("templatePython").strip() + "\n```\n")
        lines.append("---\n")

    # Section 6: Recognition Trigger Signals & Heuristics
    if t.get("recognitionPatterns"):
        lines.append(f"{sub_h} 6. Recognition Trigger Signals & Heuristics\n")
        for rp in t.get("recognitionPatterns", []):
            lines.append(f"- {rp.strip()}")
        lines.append("\n---\n")

    # Section 7: Contest WA / TLE / RE Traps
    if t.get("commonBugs"):
        lines.append(f"{sub_h} 7. Contest WA / TLE / RE Traps\n")
        for cb in t.get("commonBugs", []):
            lines.append(f"- {cb.strip()}")
        lines.append("\n---\n")

    # Section 8: Curated Practice Problem Bank
    if t.get("curatedProblems"):
        lines.append(f"{sub_h} 8. Curated Practice Problem Bank\n")
        lines.append("| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |")
        lines.append("|---|---|---|---|---|---|---|")
        for p in t.get("curatedProblems", []):
            tags_str = ", ".join(p.get("tags", []))
            lines.append(f"| {p.get('platform', '')} | {p.get('id', '')} | {p.get('name', '')} | {p.get('rating', '')} | {tags_str} | {p.get('insight', '')} | [Solve Problem]({p.get('url', '')}) |")
        lines.append("\n---\n")

    # Section 9: External Theory & Deep-Dive References
    if t.get("externalLinks"):
        lines.append(f"{sub_h} 9. External Theory & Deep-Dive References\n")
        for el in t.get("externalLinks", []):
            lines.append(f"- **[{el.get('source', 'Link')}]** [{el.get('title', 'Reference')}]({el.get('url', '')})")
        lines.append("\n---\n")

    # Optional Rich Additions
    if t.get("variants"):
        lines.append(f"{sub_h} 10. Algorithmic Variants & Advanced Extensions\n")
        lines.append(f"{t.get('variants').strip()}\n\n---\n")

    if t.get("problemPatterns"):
        lines.append(f"{sub_h} 11. Typical Problem Archetypes\n")
        lines.append(f"{t.get('problemPatterns').strip()}\n\n---\n")

    if t.get("recognitionExercises"):
        lines.append(f"{sub_h} 12. Recognition & Identification Drills\n")
        lines.append(f"{t.get('recognitionExercises').strip()}\n\n---\n")

    if t.get("cheatSheet"):
        lines.append(f"{sub_h} 13. Fast-Lookup Cheat Sheet\n")
        lines.append(f"{t.get('cheatSheet').strip()}\n\n---\n")

    return "\n".join(lines).strip() + "\n"

def main():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    os.makedirs(BASE_OUT_DIR, exist_ok=True)

    # Filter out skipped modules
    active_modules = [m for m in data.get("modules", []) if m.get("id") not in SKIPPED_MODULES]
    total_modules = len(active_modules)
    total_topics = sum(len(m.get("topics", [])) for m in active_modules)

    print(f"Generating section files for {total_modules} active modules ({total_topics} topics).")

    # 1. Master README.md
    master_lines = [
        "# Advanced DSA & Competitive Programming Guide: Complete Masterclass",
        "",
        "> **Comprehensive Offline Markdown Reference & Curated Knowledge Base**  ",
        f"> **Total Modules:** {total_modules} | **Total Topics:** {total_topics}  ",
        "> **Modules Included:** `sec-01` through `sec-18`, and `sec-22` (Greedy Modules 19, 20, 21 excluded per configuration)  ",
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
    for m in active_modules:
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

        # Section comprehensive guide lines
        sec_guide_lines = [
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
            "## Table of Topics in this Section",
            "",
            "| # | Topic Title | ROI | Rating | Frequency | Individual Guide |",
            "|---|---|---|---|---|---|"
        ]

        # Topic markdown files inside sec-XX/
        for t_idx, t in enumerate(topics, 1):
            t_id = t.get("id", f"topic-{t_idx}")
            clean_slug = sanitize_filename(t_id)
            idx_prefix = f"{t_idx:02d}"
            filename = f"{idx_prefix}-{clean_slug}.md"
            filepath = os.path.join(sec_dir, filename)

            title = t.get("title", f"Topic {t_idx}")
            roi = t.get("roi", "A-tier")
            rating = t.get("ratingRange", "1600–2200")
            freq = t.get("frequency", "Common")

            # 1. Write standalone individual topic guide
            topic_md = format_topic_markdown(t, sec_id, sec_title, t_idx, is_embedded=False)
            with open(filepath, "w", encoding="utf-8") as tf:
                tf.write(topic_md)

            sec_guide_lines.append(f"| {t_idx} | [{title}](#topic-{t_idx}) | `{roi}` | {rating} | {freq} | [{filename}](./{filename}) |")
            master_lines.append(f"- [{title}](./{mod_id}/{filename}) — `{roi}` | `{rating}`")

        sec_guide_lines.append("\n---\n")
        sec_guide_lines.append("## Complete Section Content Deep-Dives\n")

        # 2. Append full 9 sections of every topic to the section document
        for t_idx, t in enumerate(topics, 1):
            sec_guide_lines.append(f"<a id=\"topic-{t_idx}\"></a>")
            sec_guide_lines.append(format_topic_markdown(t, sec_id, sec_title, t_idx, is_embedded=True))
            sec_guide_lines.append("\n---\n")

        sec_full_content = "\n".join(sec_guide_lines).strip() + "\n"

        # Write sec-XX/README.md
        with open(os.path.join(sec_dir, "README.md"), "w", encoding="utf-8") as sec_readme:
            sec_readme.write(sec_full_content)

        # Write standalone section file: curriculum-v2/guide/sec-XX.md
        sec_file_path = os.path.join(BASE_OUT_DIR, f"{mod_id}.md")
        with open(sec_file_path, "w", encoding="utf-8") as sec_file:
            sec_file.write(sec_full_content)

        master_lines.append("")

    with open(os.path.join(BASE_OUT_DIR, "README.md"), "w", encoding="utf-8") as master_f:
        master_f.write("\n".join(master_lines) + "\n")

    print(f"Master index, {total_modules} section READMEs, and {total_modules} standalone section files ({BASE_OUT_DIR}/sec-*.md) generated successfully.")

if __name__ == "__main__":
    main()
