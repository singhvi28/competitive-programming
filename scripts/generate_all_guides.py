import os
import json
import re

DATA_PATH = "/home/singhvi28/competitive-programming/src/data/curriculumV2Data.json"
BASE_OUT_DIR = "/home/singhvi28/competitive-programming/curriculum-v2/guide"

def sanitize_filename(name: str) -> str:
    s = re.sub(r'[^\w\-\.]', '-', name.lower())
    s = re.sub(r'-+', '-', s).strip('-')
    return s

def format_equation(eq_str: str) -> str:
    eq = eq_str.strip()
    if eq.startswith("$$") and eq.endswith("$$"):
        return eq
    return f"$$\n{eq}\n$$"

def format_topic_markdown(t: dict, section_id: str, section_title: str, topic_idx: int) -> str:
    lines = []
    title = t.get("title", f"Topic {topic_idx}")
    lines.append(f"# {title}\n")
    
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

    # Section 1: Contest Payoff & Why It Matters
    if t.get("whyItMatters"):
        lines.append("## 1. Contest Payoff & Why It Matters\n")
        lines.append(f"{t.get('whyItMatters').strip()}\n\n---\n")

    # Section 2: Theoretical Deep-Dive & Mathematical Mechanics
    ext = t.get("extendedTheory")
    if ext:
        lines.append("## 2. Theoretical Deep-Dive & Mathematical Mechanics\n")
        if ext.get("overview"):
            lines.append(f"### Overview\n\n{ext.get('overview').strip()}\n")
        if ext.get("keyTheorems"):
            lines.append("### Fundamental Theorems & Invariants\n")
            for th in ext.get("keyTheorems", []):
                lines.append(f"- {th.strip()}")
            lines.append("")
        if ext.get("algorithmSteps"):
            lines.append("### Algorithmic Execution Blueprint\n")
            for idx, step in enumerate(ext.get("algorithmSteps", []), 1):
                lines.append(f"{idx}. {step.strip()}")
            lines.append("")
        if ext.get("invariantsAndFormulas"):
            lines.append(f"### Closed-Form Invariant Equations\n\n{format_equation(ext.get('invariantsAndFormulas'))}\n")
        if ext.get("edgeCases"):
            lines.append("### Structural Edge Cases & Assumptions\n")
            for ec in ext.get("edgeCases", []):
                lines.append(f"- {ec.strip()}")
            lines.append("")
        lines.append("---\n")

    # Section 3: Core Intuition & Problem Framing
    if t.get("coreIntuition"):
        lines.append(f"## 3. Core Intuition & Problem Framing\n\n{t.get('coreIntuition').strip()}\n\n---\n")

    # Section 4: Proof Sketches & Recurrences
    if t.get("derivation"):
        lines.append(f"## 4. Proof Sketches & Recurrences\n\n{t.get('derivation').strip()}\n\n---\n")

    # Section 5: Contest-Ready Implementation Templates
    if t.get("templateCpp") or t.get("templatePython") or t.get("complexity"):
        lines.append("## 5. Contest-Ready Implementation Templates\n")
        if t.get("complexity"):
            lines.append(f"**Operational Complexity:** `{t.get('complexity').strip()}`\n")
        if t.get("templateCpp"):
            lines.append("### C++17 Template\n\n```cpp\n" + t.get("templateCpp").strip() + "\n```\n")
        if t.get("templatePython"):
            lines.append("### Python 3 Template\n\n```python\n" + t.get("templatePython").strip() + "\n```\n")
        lines.append("---\n")

    # Section 6: Recognition Trigger Signals & Heuristics
    if t.get("recognitionPatterns"):
        lines.append("## 6. Recognition Trigger Signals & Heuristics\n")
        for rp in t.get("recognitionPatterns", []):
            lines.append(f"- {rp.strip()}")
        lines.append("\n---\n")

    # Section 7: Contest WA / TLE / RE Traps
    if t.get("commonBugs"):
        lines.append("## 7. Contest WA / TLE / RE Traps\n")
        for cb in t.get("commonBugs", []):
            lines.append(f"- {cb.strip()}")
        lines.append("\n---\n")

    # Section 8: Curated Practice Problem Bank
    if t.get("curatedProblems"):
        lines.append("## 8. Curated Practice Problem Bank\n")
        lines.append("| Platform | ID | Problem Name | Rating | Tags | Key Strategic Insight | Link |")
        lines.append("|---|---|---|---|---|---|---|")
        for p in t.get("curatedProblems", []):
            tags_str = ", ".join(p.get("tags", []))
            lines.append(f"| {p.get('platform', '')} | {p.get('id', '')} | {p.get('name', '')} | {p.get('rating', '')} | {tags_str} | {p.get('insight', '')} | [Solve Problem]({p.get('url', '')}) |")
        lines.append("\n---\n")

    # Section 9: External Theory & Deep-Dive References
    if t.get("externalLinks"):
        lines.append("## 9. External Theory & Deep-Dive References\n")
        for el in t.get("externalLinks", []):
            lines.append(f"- **[{el.get('source', 'Link')}]** [{el.get('title', 'Reference')}]({el.get('url', '')})")
        lines.append("\n---\n")

    # Optional Rich Additions
    if t.get("variants"):
        lines.append("## 10. Algorithmic Variants & Advanced Extensions\n")
        lines.append(f"{t.get('variants').strip()}\n\n---\n")

    if t.get("problemPatterns"):
        lines.append("## 11. Typical Problem Archetypes\n")
        lines.append(f"{t.get('problemPatterns').strip()}\n\n---\n")

    if t.get("recognitionExercises"):
        lines.append("## 12. Recognition & Identification Drills\n")
        lines.append(f"{t.get('recognitionExercises').strip()}\n\n---\n")

    if t.get("cheatSheet"):
        lines.append("## 13. Fast-Lookup Cheat Sheet\n")
        lines.append(f"{t.get('cheatSheet').strip()}\n\n---\n")

    return "\n".join(lines).strip() + "\n"

def main():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    os.makedirs(BASE_OUT_DIR, exist_ok=True)
    
    total_written = 0

    for m in data.get("modules", []):
        sec_id = m.get("sectionId", m.get("id", "00"))
        sec_title = m.get("title", "")
        mod_id = m.get("id", f"sec-{sec_id}")
        topics = m.get("topics", [])

        sec_dir = os.path.join(BASE_OUT_DIR, mod_id)
        os.makedirs(sec_dir, exist_ok=True)

        for t_idx, t in enumerate(topics, 1):
            t_id = t.get("id", f"topic-{t_idx}")
            clean_slug = sanitize_filename(t_id)
            idx_prefix = f"{t_idx:02d}"
            filename = f"{idx_prefix}-{clean_slug}.md"
            filepath = os.path.join(sec_dir, filename)

            content = format_topic_markdown(t, sec_id, sec_title, t_idx)
            with open(filepath, "w", encoding="utf-8") as out_f:
                out_f.write(content)
            total_written += 1

    print(f"Generated {total_written} markdown guide files across {len(data.get('modules', []))} modules.")

if __name__ == "__main__":
    main()
