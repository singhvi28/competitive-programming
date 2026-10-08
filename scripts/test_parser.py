import os
import glob
import re
import json

ADV_DSA_DIR = "/home/singhvi28/Desktop/adv-dsa"

# Section metadata
SECTION_METADATA = {
    "01": {"title": "Fenwick Tree (Binary Indexed Tree)", "phaseId": 1, "phaseName": "Range Queries & Sweeps", "icon": "Layers"},
    "02": {"title": "Segment Trees & Range Invariants", "phaseId": 1, "phaseName": "Range Queries & Sweeps", "icon": "GitBranch"},
    "03": {"title": "Merge Sort Trees & 2D Ranges", "phaseId": 1, "phaseName": "Range Queries & Sweeps", "icon": "Split"},
    "04": {"title": "Square Root Decomposition & Mo's Algorithm", "phaseId": 3, "phaseName": "Advanced Data Structures & Sqrt Techniques", "icon": "Boxes"},
    "05": {"title": "Advanced Data Structures (Treaps, LCT, PBDS)", "phaseId": 3, "phaseName": "Advanced Data Structures & Sqrt Techniques", "icon": "Database"},
    "06": {"title": "Tree Algorithms & Structural Decompositions", "phaseId": 2, "phaseName": "Tree Algorithms & Structural Hierarchies", "icon": "Network"},
    "07": {"title": "Graph Algorithms (SCC, Topo-DP, 2-SAT)", "phaseId": 4, "phaseName": "Graph Algorithms & Network Flow", "icon": "Share2"},
    "08": {"title": "Advanced Graphs (Shortest Paths, MST, Euler)", "phaseId": 4, "phaseName": "Graph Algorithms & Network Flow", "icon": "Route"},
    "09": {"title": "Network Flow & Matchings", "phaseId": 4, "phaseName": "Graph Algorithms & Network Flow", "icon": "Activity"},
    "10": {"title": "Dynamic Programming Optimizations", "phaseId": 5, "phaseName": "Dynamic Programming & Advanced Greedy", "icon": "Cpu"},
    "11": {"title": "String Algorithms & Automata", "phaseId": 6, "phaseName": "String Algorithms", "icon": "Binary"},
    "12": {"title": "Number Theory & Multiplicative Functions", "phaseId": 7, "phaseName": "Mathematics, Linear Algebra & Polynomials", "icon": "Hash"},
    "13": {"title": "Bit Manipulation & Advanced Combinatorics", "phaseId": 7, "phaseName": "Mathematics, Linear Algebra & Polynomials", "icon": "Grid"},
    "14": {"title": "Linear Algebra & Algebraic Graph Theory", "phaseId": 7, "phaseName": "Mathematics, Linear Algebra & Polynomials", "icon": "Table"},
    "15": {"title": "FFT, NTT & Formal Power Series", "phaseId": 7, "phaseName": "Mathematics, Linear Algebra & Polynomials", "icon": "Sigma"},
    "16": {"title": "Game Theory & Sprague-Grundy", "phaseId": 8, "phaseName": "Game Theory, Geometry & Meta-Algorithms", "icon": "Gamepad2"},
    "17": {"title": "Computational Geometry & Polygons", "phaseId": 8, "phaseName": "Game Theory, Geometry & Meta-Algorithms", "icon": "Compass"},
    "18": {"title": "Randomization & Meta-Techniques", "phaseId": 8, "phaseName": "Game Theory, Geometry & Meta-Algorithms", "icon": "Shuffle"},
    "19": {"title": "Greedy Fundamentals & Invariants", "phaseId": 1, "phaseName": "Range Queries & Sweeps", "icon": "Zap"},
    "20": {"title": "Greedy Intermediate (Slope Trick, WQS)", "phaseId": 5, "phaseName": "Dynamic Programming & Advanced Greedy", "icon": "TrendingUp"},
    "21": {"title": "Greedy Advanced (Matroids & Oracles)", "phaseId": 5, "phaseName": "Dynamic Programming & Advanced Greedy", "icon": "Award"},
    "22": {"title": "Line Sweep Algorithms & Reductions", "phaseId": 1, "phaseName": "Range Queries & Sweeps", "icon": "Sliders"}
}

PHASES = [
    {"id": 1, "name": "Phase 1: Linear Sweeps & Core Range Structures", "description": "Greedy exchange foundations, static/2D/geometric line sweeps, difference arrays, Fenwick trees, and Segment Trees.", "sections": ["19", "22", "01", "02", "03"]},
    {"id": 2, "name": "Phase 2: Tree Algorithms & Structural Hierarchies", "description": "Binary lifting, LCA, Euler tours, Tree DP, Rerooting, Heavy-Light Decomposition (HLD), Centroid Decomposition, and Sack.", "sections": ["06"]},
    {"id": 3, "name": "Phase 3: Advanced Data Structures & Sqrt Techniques", "description": "Sqrt decomposition, Mo's algorithm on arrays & trees, Persistent Segment Trees, Treaps, PBDS, and Link-Cut Trees.", "sections": ["04", "05"]},
    {"id": 4, "name": "Phase 4: Graph Algorithms & Network Flow", "description": "Shortest path variants, Topo-DP, Kosaraju/Tarjan SCC, 2-SAT, MST variants, Dinic max flow, Min-Cut modeling, and MCMF.", "sections": ["07", "08", "09"]},
    {"id": 5, "name": "Phase 5: Dynamic Programming & Advanced Greedy", "description": "Monotone queue/stack DP, CHT, Li Chao Tree, D&C DP, Knuth, SOS DP, Slope Trick, WQS/Aliens trick, and Matroid theory.", "sections": ["10", "20", "21"]},
    {"id": 6, "name": "Phase 6: String Algorithms", "description": "Rolling hash with anti-hash hygiene, KMP pi table, Z-algorithm, Manacher, Aho-Corasick, Suffix Array + LCP, and SAM.", "sections": ["11"]},
    {"id": 7, "name": "Phase 7: Mathematics, Linear Algebra & Polynomials", "description": "Linear sieve, SPF, Modular inverse, Möbius inversion, Bitwise transforms, Gaussian elimination, XOR basis, and FFT/NTT.", "sections": ["12", "13", "14", "15"]},
    {"id": 8, "name": "Phase 8: Game Theory, Geometry & Meta-Algorithms", "description": "Sprague-Grundy theorem, Nim, Computational geometry primitives, Convex hull, Half-plane intersection, and Parallel BS.", "sections": ["16", "17", "18"]}
]

def parse_all():
    from parse_adv_dsa import parse_roi_map, parse_master_cheat_sheet
    roi_map = parse_roi_map()
    cheat_sheet = parse_master_cheat_sheet()

    files = sorted(glob.glob(os.path.join(ADV_DSA_DIR, "*.md")))
    all_topics = []

    for fpath in files:
        fname = os.path.basename(fpath)
        if fname in ["00-roi-map.md", "99-master-cheat-sheet.md", "README.md", "_format-contract.md"]:
            continue
        
        # Determine section number
        m_sec = re.match(r"^(\d{2})", fname)
        sec_id = m_sec.group(1) if m_sec else "00"
        if sec_id not in SECTION_METADATA:
            continue
        
        sec_meta = SECTION_METADATA[sec_id]
        
        with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        
        # Split by ### heading
        # In files with atomic structure, each topic is ### <Topic Name>
        chunks = re.split(r"\n###\s+", content)
        if len(chunks) <= 1:
            continue
        
        for chunk in chunks[1:]:
            lines = chunk.strip().split("\n")
            topic_raw = lines[0].strip()
            topic_name = re.sub(r"^\d+[\.\)]\s*", "", topic_raw)
            if not topic_name or topic_name.startswith("Section") or topic_name.startswith("Hub:") or topic_name.startswith("Phase"):
                continue
            
            chunk_body = "\n".join(lines[1:])
            
            # Extract sub-sections A to L
            def get_sub_sec(letter, next_letter=None):
                pattern = rf"####\s+{letter}\.\s*([^\n]+)\n([\s\S]*?)(?=####\s+[A-Z]\.|\Z)"
                m = re.search(pattern, chunk_body)
                if m:
                    return m.group(2).strip()
                return ""

            why_text = get_sub_sec("A")
            intuition_text = get_sub_sec("B")
            recognition_text = get_sub_sec("C")
            derivation_text = get_sub_sec("D")
            cpp_text = get_sub_sec("E")
            py_text = get_sub_sec("F")
            complexity_text = get_sub_sec("G")
            bugs_text = get_sub_sec("H")
            variants_text = get_sub_sec("I")
            patterns_text = get_sub_sec("J")
            exercises_text = get_sub_sec("K")
            cheat_text = get_sub_sec("L")

            # Extract fields from why_text or roi_map fallback
            roi_val = "B-tier"
            m_roi = re.search(r"Contest ROI:\s*([^\n]+)", why_text)
            if m_roi:
                roi_val = m_roi.group(1).strip()
            
            freq_val = "Common"
            m_freq = re.search(r"Frequency:\s*([^\n]+)", why_text)
            if m_freq:
                freq_val = m_freq.group(1).strip()

            rating_val = "1600–2200"
            m_rat = re.search(r"Typical.*?rating range:\s*([^\n]+)", why_text)
            if m_rat:
                rating_val = m_rat.group(1).strip()

            prereq_val = ""
            m_pre = re.search(r"Prerequisites:\s*([^\n]+)", why_text)
            if m_pre:
                prereq_val = m_pre.group(1).strip()

            # Cross-reference with roi_map if missing
            norm_key = topic_name.lower().strip()
            if norm_key in roi_map:
                entry = roi_map[norm_key]
                if not m_roi: roi_val = entry["roi"]
                if not m_freq: freq_val = entry["frequency"]
                if not m_rat: rating_val = entry["ratingRange"]
                if not m_pre: prereq_val = entry["prerequisites"]

            # Extract C++ code
            cpp_code = ""
            m_cpp = re.search(r"```(?:cpp|c\+\+|c)\n([\s\S]*?)```", cpp_text if cpp_text else chunk_body)
            if m_cpp:
                cpp_code = m_cpp.group(1).strip()

            # Extract Python code
            py_code = ""
            m_py = re.search(r"```(?:python|py)\n([\s\S]*?)```", py_text if py_text else chunk_body)
            if m_py:
                py_code = m_py.group(1).strip()

            # Parse recognition bullet points
            rec_bullets = [line.strip().lstrip("-* ").strip() for line in recognition_text.split("\n") if line.strip().startswith(("-", "*", "1.", "2.", "3.", "4."))]
            
            # Parse bugs bullet points
            bug_bullets = [line.strip().lstrip("-* ").strip() for line in bugs_text.split("\n") if line.strip().startswith(("-", "*", "1.", "2.", "3.", "4."))]

            topic_id = f"{sec_id}-{re.sub(r'[^a-zA-Z0-9]+', '-', topic_name).strip('-').lower()}"

            all_topics.append({
                "id": topic_id,
                "title": topic_name,
                "sectionId": sec_id,
                "sectionTitle": sec_meta["title"],
                "phaseId": sec_meta["phaseId"],
                "phaseName": sec_meta["phaseName"],
                "icon": sec_meta["icon"],
                "sourceFile": fname,
                "roi": roi_val,
                "frequency": freq_val,
                "ratingRange": rating_val,
                "prerequisites": prereq_val,
                "whyItMatters": why_text,
                "coreIntuition": intuition_text,
                "recognitionPatterns": rec_bullets if rec_bullets else [recognition_text] if recognition_text else [],
                "derivation": derivation_text,
                "templateCpp": cpp_code,
                "templatePython": py_code,
                "complexity": complexity_text,
                "commonBugs": bug_bullets if bug_bullets else [bugs_text] if bugs_text else [],
                "variants": variants_text,
                "problemPatterns": patterns_text,
                "recognitionExercises": exercises_text,
                "cheatSheet": cheat_text
            })

    print(f"Extracted total {len(all_topics)} atomic topics across 22 sections!")
    return all_topics

topics = parse_all()
print("Sample extracted topics:")
for t in topics[:8]:
    print(f"[{t['sectionId']}] {t['title']} (ROI: {t['roi']}, Rating: {t['ratingRange']}, C++: {len(t['templateCpp'])} bytes, Recog: {len(t['recognitionPatterns'])})")
