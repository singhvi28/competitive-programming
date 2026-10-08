import os
import glob
import re
import json

ADV_DSA_DIR = "/home/singhvi28/Desktop/adv-dsa"
OUTPUT_JSON = "/home/singhvi28/competitive-programming/src/data/curriculumV2Data.json"
OUTPUT_TS = "/home/singhvi28/competitive-programming/src/types/curriculumV2.ts"

SECTION_METADATA = {
    "01": {
        "id": "sec-01",
        "number": 1,
        "title": "Fenwick Tree (Binary Indexed Tree)",
        "shortTitle": "Fenwick Tree",
        "phaseId": 1,
        "phaseName": "Range Queries & Sweeps",
        "icon": "Layers",
        "summary": "Prefix invertible operations, binary lifting on BIT in O(log N), 2D Fenwick trees, range adds/range sums, and offline contribution counting."
    },
    "02": {
        "id": "sec-02",
        "number": 2,
        "title": "Segment Trees & Range Invariants",
        "shortTitle": "Segment Trees",
        "phaseId": 1,
        "phaseName": "Range Queries & Sweeps",
        "icon": "GitBranch",
        "summary": "Monoid segment trees, lazy propagation tags, range assign/add, iterative bottom-up trees, segment tree beats, persistent, and dynamic trees."
    },
    "03": {
        "id": "sec-03",
        "number": 3,
        "title": "Merge Sort Trees & 2D Ranges",
        "shortTitle": "Merge Sort Trees",
        "phaseId": 1,
        "phaseName": "Range Queries & Sweeps",
        "icon": "Split",
        "summary": "Static 2D range frequency counting in O(log^2 N), fractional cascading for O(log N) queries, and order statistics."
    },
    "04": {
        "id": "sec-04",
        "number": 4,
        "title": "Square Root Decomposition & Mo's Algorithm",
        "shortTitle": "Sqrt Decomp & Mo",
        "phaseId": 3,
        "phaseName": "Advanced Data Structures & Sqrt Techniques",
        "icon": "Boxes",
        "summary": "Block decomposition, range updates with O(sqrt(N)) blocks, Mo's algorithm on arrays in O((N+Q)sqrt(N)), Hilbert curve sorting, and Mo's on trees."
    },
    "05": {
        "id": "sec-05",
        "number": 5,
        "title": "Advanced Data Structures (Treaps, LCT, PBDS)",
        "shortTitle": "Advanced DS",
        "phaseId": 3,
        "phaseName": "Advanced Data Structures & Sqrt Techniques",
        "icon": "Database",
        "summary": "Sparse tables, Cartesian trees, Implicit & explicit Treaps, PBDS ordered statistics, DSU with rollback, and Link-Cut Trees."
    },
    "06": {
        "id": "sec-06",
        "number": 6,
        "title": "Tree Algorithms & Structural Decompositions",
        "shortTitle": "Tree Algorithms",
        "phaseId": 2,
        "phaseName": "Tree Algorithms & Structural Hierarchies",
        "icon": "Network",
        "summary": "Binary lifting, LCA, Euler tours, Tree DP, Tree rerooting DP, Heavy-Light Decomposition (HLD), Centroid Decomposition, and Sack (DSU on Tree)."
    },
    "07": {
        "id": "sec-07",
        "number": 7,
        "title": "Graph Algorithms (SCC, Topo-DP, 2-SAT)",
        "shortTitle": "Graph Algorithms",
        "phaseId": 4,
        "phaseName": "Graph Algorithms & Network Flow",
        "icon": "Share2",
        "summary": "Kosaraju and Tarjan SCC algorithms, Condensation DAG, Topological DP, 2-SAT variable implication graphs, and offline dynamic connectivity."
    },
    "08": {
        "id": "sec-08",
        "number": 8,
        "title": "Advanced Graphs (Shortest Paths, MST, Euler)",
        "shortTitle": "Advanced Graphs",
        "phaseId": 4,
        "phaseName": "Graph Algorithms & Network Flow",
        "icon": "Route",
        "summary": "Dijkstra variants, 0-1 BFS, Floyd-Warshall, DAG paths, Functional graphs, Kruskal reconstruction tree, and Eulerian path construction."
    },
    "09": {
        "id": "sec-09",
        "number": 9,
        "title": "Network Flow & Matchings",
        "shortTitle": "Network Flow",
        "phaseId": 4,
        "phaseName": "Graph Algorithms & Network Flow",
        "icon": "Activity",
        "summary": "Dinic's blocking flow algorithm, Min-Cut theorem & project selection closures, Bipartite matching (Kuhn / Hopcroft-Karp), MCMF with SPFA/Potentials, and Demands."
    },
    "10": {
        "id": "sec-10",
        "number": 10,
        "title": "Dynamic Programming Optimizations",
        "shortTitle": "DP Optimizations",
        "phaseId": 5,
        "phaseName": "Dynamic Programming & Advanced Greedy",
        "icon": "Cpu",
        "summary": "Monotone Queue/Stack DP, Convex Hull Trick (CHT), Li Chao Tree, Divide-and-Conquer DP, Knuth Quadrangle Inequality, SOS DP, Bitset DP, and Profile DP."
    },
    "11": {
        "id": "sec-11",
        "number": 11,
        "title": "String Algorithms & Automata",
        "shortTitle": "String Algorithms",
        "phaseId": 6,
        "phaseName": "String Algorithms",
        "icon": "Binary",
        "summary": "Rolling hash with anti-hash hygiene, KMP pi-table, Z-algorithm, Manacher palindrome radius, Aho-Corasick automaton, Suffix Array + LCP, and Suffix Automaton (SAM)."
    },
    "12": {
        "id": "sec-12",
        "number": 12,
        "title": "Number Theory & Multiplicative Functions",
        "shortTitle": "Number Theory",
        "phaseId": 7,
        "phaseName": "Mathematics, Linear Algebra & Polynomials",
        "icon": "Hash",
        "summary": "Extended Euclidean, Linear Diophantine, Linear Sieve with Smallest Prime Factor (SPF), Euler Totient phi, Dirichlet convolution, Möbius Inversion, and BSGS."
    },
    "13": {
        "id": "sec-13",
        "number": 13,
        "title": "Bit Manipulation & Advanced Combinatorics",
        "shortTitle": "Bits & Combinatorics",
        "phaseId": 7,
        "phaseName": "Mathematics, Linear Algebra & Polynomials",
        "icon": "Grid",
        "summary": "Bitmask tricks, submask enumeration in 3^n, Binomial coefficients mod P, Lucas theorem, Catalan/Stirling numbers, and Burnside's Lemma."
    },
    "14": {
        "id": "sec-14",
        "number": 14,
        "title": "Linear Algebra & Algebraic Graph Theory",
        "shortTitle": "Linear Algebra",
        "phaseId": 7,
        "phaseName": "Mathematics, Linear Algebra & Polynomials",
        "icon": "Table",
        "summary": "Gaussian elimination over R and F_2, XOR linear basis insertion & maximization, Matrix exponentiation, Matrix Tree Theorem Laplacian determinants, and BEST theorem."
    },
    "15": {
        "id": "sec-15",
        "number": 15,
        "title": "FFT, NTT & Formal Power Series",
        "shortTitle": "FFT / Polynomials",
        "phaseId": 7,
        "phaseName": "Mathematics, Linear Algebra & Polynomials",
        "icon": "Sigma",
        "summary": "Fast Fourier Transform, Number Theoretic Transform (NTT mod 998244353), Divide-and-Conquer NTT, Fast Walsh-Hadamard Transform (FWHT), and Formal Power Series operations."
    },
    "16": {
        "id": "sec-16",
        "number": 16,
        "title": "Game Theory & Sprague-Grundy",
        "shortTitle": "Game Theory",
        "phaseId": 8,
        "phaseName": "Game Theory, Geometry & Meta-Algorithms",
        "icon": "Gamepad2",
        "summary": "Impartial games, Nim-sum XOR, Sprague-Grundy theorem with MEX transitions, Game graph DAG DP, and Misere Nim modifications."
    },
    "17": {
        "id": "sec-17",
        "number": 17,
        "title": "Computational Geometry & Polygons",
        "shortTitle": "Geometry",
        "phaseId": 8,
        "phaseName": "Game Theory, Geometry & Meta-Algorithms",
        "icon": "Compass",
        "summary": "Vector cross/dot products, Orientation tests, Monotone Chain Convex Hull, Rotating Calipers, Point-in-polygon, Half-plane intersection, and Circle geometry."
    },
    "18": {
        "id": "sec-18",
        "number": 18,
        "title": "Randomization & Meta-Techniques",
        "shortTitle": "Randomization & Meta",
        "phaseId": 8,
        "phaseName": "Game Theory, Geometry & Meta-Algorithms",
        "icon": "Shuffle",
        "summary": "Meet-in-the-Middle 2^(N/2), Randomized 64-bit splitmix hashing hygiene, Offline query processing, Parallel Binary Search, and Tree Mo's algorithm."
    },
    "19": {
        "id": "sec-19",
        "number": 19,
        "title": "Greedy Fundamentals & Invariants",
        "shortTitle": "Greedy Basics",
        "phaseId": 1,
        "phaseName": "Range Queries & Sweeps",
        "icon": "Zap",
        "summary": "Greedy exchange arguments, Sorting criteria derivation, Priority queue regret/undo maintenance, and structural invariants."
    },
    "20": {
        "id": "sec-20",
        "number": 20,
        "title": "Greedy Intermediate (Slope Trick, WQS)",
        "shortTitle": "Greedy Intermediate",
        "phaseId": 5,
        "phaseName": "Dynamic Programming & Advanced Greedy",
        "icon": "TrendingUp",
        "summary": "Decoupled dimension sweeps, Median cost minimization, Slope Trick with two priority queues, and WQS Binary Search / Aliens Trick."
    },
    "21": {
        "id": "sec-21",
        "number": 21,
        "title": "Greedy Advanced (Matroids & Oracles)",
        "shortTitle": "Greedy Advanced",
        "phaseId": 5,
        "phaseName": "Dynamic Programming & Advanced Greedy",
        "icon": "Award",
        "summary": "Axiomatic Matroid theory, Rado-Edmonds greedy optimality, Matroid Intersection augmenting paths in O(R^3 Q), Antimatroids, and Dynamic Verification Oracles."
    },
    "22": {
        "id": "sec-22",
        "number": 22,
        "title": "Line Sweep Algorithms & Reductions",
        "shortTitle": "Line Sweep",
        "phaseId": 1,
        "phaseName": "Range Queries & Sweeps",
        "icon": "Sliders",
        "summary": "Event abstraction, coordinate compression, 1D/2D difference arrays, 2D Fenwick dominance, Klee's Measure rectangle union area, and Bentley-Ottmann line sweep."
    }
}

PHASES_METADATA = [
    {
        "id": 1,
        "number": 1,
        "name": "Phase 1: Linear Sweeps & Core Range Structures",
        "shortName": "Range Queries & Sweeps",
        "badge": "S-Tier Core",
        "color": "emerald",
        "description": "Greedy exchange foundations, static/2D/geometric line sweeps, difference arrays, Fenwick trees (BIT), Segment Trees (lazy, beats, persistent), and Merge Sort Trees.",
        "sections": ["19", "22", "01", "02", "03"]
    },
    {
        "id": 2,
        "number": 2,
        "name": "Phase 2: Tree Algorithms & Structural Hierarchies",
        "shortName": "Tree Decompositions",
        "badge": "S & A-Tier Mastery",
        "color": "blue",
        "description": "Binary lifting, LCA, Euler tours, Tree DP, Tree rerooting DP, Heavy-Light Decomposition (HLD), Centroid Decomposition, and Sack (DSU on Tree).",
        "sections": ["06"]
    },
    {
        "id": 3,
        "number": 3,
        "name": "Phase 3: Advanced Data Structures & Sqrt Techniques",
        "shortName": "Sqrt & Advanced DS",
        "badge": "High Payoff",
        "color": "violet",
        "description": "Sqrt decomposition, Mo's algorithm on arrays & trees, Sparse Tables, Cartesian Trees, Persistent Segment Trees, Treaps, PBDS, and Link-Cut Trees.",
        "sections": ["04", "05"]
    },
    {
        "id": 4,
        "number": 4,
        "name": "Phase 4: Graph Algorithms & Network Flow",
        "shortName": "Graphs & Flows",
        "badge": "Core & Advanced",
        "color": "indigo",
        "description": "Dijkstra variants, 0-1 BFS, Floyd-Warshall, Topo-DP, Kosaraju/Tarjan SCC, 2-SAT, MST variants, Dinic max flow, Min-Cut modeling, and MCMF.",
        "sections": ["07", "08", "09"]
    },
    {
        "id": 5,
        "number": 5,
        "name": "Phase 5: Dynamic Programming & Advanced Greedy",
        "shortName": "DP & Advanced Greedy",
        "badge": "Master Climb",
        "color": "amber",
        "description": "Monotone queue/stack DP, Convex Hull Trick (CHT), Li Chao Tree, D&C DP, Knuth Optimization, SOS DP, Slope Trick, WQS/Aliens trick, and Matroid theory.",
        "sections": ["10", "20", "21"]
    },
    {
        "id": 6,
        "number": 6,
        "name": "Phase 6: String Algorithms",
        "shortName": "String Algorithms",
        "badge": "Automata & Hashes",
        "color": "pink",
        "description": "Rolling hash with randomized anti-hash hygiene, KMP pi table, Z-algorithm, Manacher, Aho-Corasick automaton, Suffix Array + LCP, and Suffix Automaton (SAM).",
        "sections": ["11"]
    },
    {
        "id": 7,
        "number": 7,
        "name": "Phase 7: Mathematics, Linear Algebra & Polynomials",
        "shortName": "Math & Polynomials",
        "badge": "Algebra & Convolutions",
        "color": "cyan",
        "description": "Linear sieve, SPF, Modular inverse, Möbius inversion, Bitwise transforms, Gaussian elimination, XOR basis, Matrix Tree Theorem, and FFT/NTT.",
        "sections": ["12", "13", "14", "15"]
    },
    {
        "id": 8,
        "number": 8,
        "name": "Phase 8: Game Theory, Geometry & Meta-Algorithms",
        "shortName": "Games, Geometry & Meta",
        "badge": "Grandmaster Mastery",
        "color": "rose",
        "description": "Sprague-Grundy theorem, Nim, Computational geometry primitives, Monotone chain convex hull, Half-plane intersection, Meet-in-the-Middle, and Parallel BS.",
        "sections": ["16", "17", "18"]
    }
]

# Canonical topic to section mapping for cross-filed topics
CANONICAL_SECTION_MAP = {
    "fenwick tree (binary indexed tree)": "01",
    "2d fenwick tree": "01",
    "binary lifting on bit": "01",
    "binary lifting on fenwick tree": "01",
    "fenwick tree for beyond just sums": "01",
    "fenwick tree variants": "01",
    "merge sort tree": "03",
    "mst with fractional cascading": "03",
    "fractional cascading": "03",
    "additional abilities of the mst": "03",
    "square root decomposition": "04",
    "square root decomposition basics": "04",
    "block updates and queries": "04",
    "mo's algorithm": "04",
    "mo's algorithm on trees": "04",
}

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

def parse_master_cheat_sheet():
    path = os.path.join(ADV_DSA_DIR, "99-master-cheat-sheet.md")
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    sections = []
    sec_chunks = re.split(r"\n##\s+", content)
    for chunk in sec_chunks[1:]:
        lines = chunk.strip().split("\n")
        sec_header = lines[0].strip()
        
        sub_chunks = re.split(r"\n###\s+", "\n".join(lines[1:]))
        subtopics = []
        for s in sub_chunks:
            s_lines = s.strip().split("\n")
            topic_name = s_lines[0].strip()
            if not topic_name or topic_name.startswith("Hub:") or topic_name.startswith("Note:"):
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

def build_data():
    roi_map = parse_roi_map()
    cheat_sheet = parse_master_cheat_sheet()

    files = sorted(glob.glob(os.path.join(ADV_DSA_DIR, "*.md")))
    all_extracted_topics = []

    for fpath in files:
        fname = os.path.basename(fpath)
        if fname in ["00-roi-map.md", "99-master-cheat-sheet.md", "README.md", "_format-contract.md"]:
            continue
        
        m_sec = re.match(r"^(\d{2})", fname)
        default_sec_id = m_sec.group(1) if m_sec else "00"
        
        with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        
        # In files with atomic structure, each topic is ### <Topic Name>
        chunks = re.split(r"\n###\s+", content)
        if len(chunks) <= 1:
            continue
        
        for chunk in chunks[1:]:
            lines = chunk.strip().split("\n")
            topic_raw = lines[0].strip()
            topic_name = re.sub(r"^\d+[\.\)]\s*", "", topic_raw)
            topic_name = topic_name.replace("**", "").strip()
            if not topic_name or topic_name.startswith("Section") or topic_name.startswith("Hub:") or topic_name.startswith("Phase") or topic_name.startswith("Track"):
                continue
            
            norm_topic = topic_name.lower().strip()
            
            # Determine canonical section
            if norm_topic in CANONICAL_SECTION_MAP:
                sec_id = CANONICAL_SECTION_MAP[norm_topic]
            elif default_sec_id in SECTION_METADATA:
                sec_id = default_sec_id
            else:
                continue
            
            sec_meta = SECTION_METADATA[sec_id]
            
            chunk_body = "\n".join(lines[1:])
            
            def get_sub_sec(letter):
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

            if norm_topic in roi_map:
                entry = roi_map[norm_topic]
                if not m_roi: roi_val = entry["roi"]
                if not m_freq: freq_val = entry["frequency"]
                if not m_rat: rating_val = entry["ratingRange"]
                if not m_pre: prereq_val = entry["prerequisites"]

            cpp_code = ""
            m_cpp = re.search(r"```(?:cpp|c\+\+|c)\n([\s\S]*?)```", cpp_text if cpp_text else chunk_body)
            if m_cpp:
                cpp_code = m_cpp.group(1).strip()

            py_code = ""
            m_py = re.search(r"```(?:python|py)\n([\s\S]*?)```", py_text if py_text else chunk_body)
            if m_py:
                py_code = m_py.group(1).strip()

            rec_bullets = [line.strip().lstrip("-* ").strip() for line in recognition_text.split("\n") if line.strip().startswith(("-", "*", "1.", "2.", "3.", "4."))]
            bug_bullets = [line.strip().lstrip("-* ").strip() for line in bugs_text.split("\n") if line.strip().startswith(("-", "*", "1.", "2.", "3.", "4."))]

            topic_id = f"{sec_id}-{re.sub(r'[^a-zA-Z0-9]+', '-', topic_name).strip('-').lower()}"

            all_extracted_topics.append({
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
                "recognitionPatterns": rec_bullets if rec_bullets else ([recognition_text] if recognition_text else []),
                "derivation": derivation_text,
                "templateCpp": cpp_code,
                "templatePython": py_code,
                "complexity": complexity_text,
                "commonBugs": bug_bullets if bug_bullets else ([bugs_text] if bugs_text else []),
                "variants": variants_text,
                "problemPatterns": patterns_text,
                "recognitionExercises": exercises_text,
                "cheatSheet": cheat_text
            })

    # Group topics into Modules by Section
    modules = []
    for sec_id, meta in sorted(SECTION_METADATA.items(), key=lambda x: int(x[0])):
        sec_topics = [t for t in all_extracted_topics if t["sectionId"] == sec_id]
        
        # Deduplicate topics with same title keeping the richer one
        dedup_map = {}
        for t in sec_topics:
            key = t["title"].lower().strip()
            score = len(t["templateCpp"]) * 2 + len(t["coreIntuition"]) + len(t["derivation"]) + len(t["templatePython"])
            if key not in dedup_map or score > dedup_map[key]["_score"]:
                t["_score"] = score
                dedup_map[key] = t

        cleaned_topics = list(dedup_map.values())
        for t in cleaned_topics:
            del t["_score"]

        modules.append({
            "id": meta["id"],
            "sectionNumber": meta["number"],
            "sectionId": sec_id,
            "title": meta["title"],
            "shortTitle": meta["shortTitle"],
            "phaseId": meta["phaseId"],
            "phaseName": meta["phaseName"],
            "icon": meta["icon"],
            "summary": meta["summary"],
            "topicsCount": len(cleaned_topics),
            "topics": cleaned_topics
        })

    # Build Study Tracks
    tracks = [
        {
            "id": "track-a",
            "name": "Track A: The Core S-Tier Foundation",
            "ratingRange": "1400 → 1900+",
            "badge": "Div.2 C/D & ICPC Prelims",
            "color": "emerald",
            "description": "Essential high-ROI techniques that decide modern rated contests consistently. Focus on muscle memory for C++ templates and pattern recognition.",
            "sections": ["19", "22", "01", "02", "07", "08", "09", "06", "11", "12", "13", "16", "17", "18"]
        },
        {
            "id": "track-b",
            "name": "Track B: Candidate Master & Master Climb",
            "ratingRange": "1900 → 2300+",
            "badge": "Div.1 A/B/C & ICPC Regionals",
            "color": "purple",
            "description": "Advanced structural decompositions, dynamic range structures, HLD, Centroid, Mo's, Dinic flow, CHT, Slope trick, and Aho-Corasick.",
            "sections": ["06", "22", "03", "02", "05", "04", "09", "10", "20", "11", "14", "12", "17", "18"]
        },
        {
            "id": "track-c",
            "name": "Track C: Grandmaster Mastery",
            "ratingRange": "2300 → 2800+",
            "badge": "Div.1 D/E/F & ICPC World Finals",
            "color": "rose",
            "description": "Axiomatic matroid theory, Matroid intersection, NTT, Formal Power Series, Matrix Tree Theorem, Segment Tree Beats, LCT, and SAM.",
            "sections": ["21", "15", "14", "02", "05", "06", "04", "11", "17", "13", "12"]
        }
    ]

    all_final_topics = [t for m in modules for t in m["topics"]]
    total_topics = len(all_final_topics)
    total_templates = sum(1 for t in all_final_topics if t["templateCpp"])
    
    roi_counts = {"S-tier": 0, "A-tier": 0, "B-tier": 0, "C-tier": 0, "Niche": 0}
    for t in all_final_topics:
        roi = t["roi"]
        if roi in roi_counts:
            roi_counts[roi] += 1
        elif "S" in roi: roi_counts["S-tier"] += 1
        elif "A" in roi: roi_counts["A-tier"] += 1
        elif "B" in roi: roi_counts["B-tier"] += 1
        elif "C" in roi: roi_counts["C-tier"] += 1
        elif "Niche" in roi: roi_counts["Niche"] += 1
        else: roi_counts["B-tier"] += 1

    curriculum_v2_data = {
        "metadata": {
            "title": "Advanced Competitive Programming Masterclass",
            "subtitle": "22 Sections · 8 Thematic Phases · 1400–2800+ Rating Invariants, Templates & Recognition",
            "version": "2.0.0",
            "totalModules": len(modules),
            "totalTopics": total_topics,
            "totalTemplates": total_templates,
            "roiDistribution": roi_counts
        },
        "phases": PHASES_METADATA,
        "tracks": tracks,
        "modules": modules,
        "roiMap": list(roi_map.values()),
        "cheatSheet": cheat_sheet
    }

    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(curriculum_v2_data, f, indent=2, ensure_ascii=False)

    print(f"Generated {OUTPUT_JSON} successfully ({os.path.getsize(OUTPUT_JSON)} bytes)!")

    # TypeScript definitions
    ts_content = """export type RoiTier = 'S-tier' | 'A-tier' | 'B-tier' | 'C-tier' | 'Niche';

export interface CurriculumV2Topic {
  id: string;
  title: string;
  sectionId: string;
  sectionTitle: string;
  phaseId: number;
  phaseName: string;
  icon: string;
  sourceFile: string;
  roi: RoiTier | string;
  frequency: string;
  ratingRange: string;
  prerequisites: string;
  whyItMatters: string;
  coreIntuition: string;
  recognitionPatterns: string[];
  derivation: string;
  templateCpp: string;
  templatePython: string;
  complexity: string;
  commonBugs: string[];
  variants: string;
  problemPatterns: string;
  recognitionExercises: string;
  cheatSheet: string;
}

export interface CurriculumV2Module {
  id: string;
  sectionNumber: number;
  sectionId: string;
  title: string;
  shortTitle: string;
  phaseId: number;
  phaseName: string;
  icon: string;
  summary: string;
  topicsCount: number;
  topics: CurriculumV2Topic[];
}

export interface CurriculumV2Phase {
  id: number;
  number: number;
  name: string;
  shortName: string;
  badge: string;
  color: string;
  description: string;
  sections: string[];
}

export interface CurriculumV2Track {
  id: string;
  name: string;
  ratingRange: string;
  badge: string;
  color: string;
  description: string;
  sections: string[];
}

export interface RoiMapEntry {
  topic: string;
  roi: string;
  frequency: string;
  difficulty: string;
  prerequisites: string;
  ratingRange: string;
}

export interface CheatSheetSubtopic {
  topic: string;
  recognitionClue: string;
  coreIdea: string;
  complexity: string;
  mainTemplate: string;
  commonUseCase: string;
  sectionFile: string;
}

export interface CheatSheetSection {
  sectionTitle: string;
  subtopics: CheatSheetSubtopic[];
}

export interface CurriculumV2Data {
  metadata: {
    title: string;
    subtitle: string;
    version: string;
    totalModules: number;
    totalTopics: number;
    totalTemplates: number;
    roiDistribution: Record<string, number>;
  };
  phases: CurriculumV2Phase[];
  tracks: CurriculumV2Track[];
  modules: CurriculumV2Module[];
  roiMap: RoiMapEntry[];
  cheatSheet: CheatSheetSection[];
}
"""
    with open(OUTPUT_TS, "w", encoding="utf-8") as f:
        f.write(ts_content)

    print(f"Generated {OUTPUT_TS} successfully!")

if __name__ == "__main__":
    build_data()
