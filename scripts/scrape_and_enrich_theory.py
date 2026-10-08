import os
import json
import urllib.request
import urllib.parse
import re
import concurrent.futures

DATA_JSON = "/home/singhvi28/competitive-programming/src/data/curriculumV2Data.json"

with open(DATA_JSON, "r", encoding="utf-8") as f:
    curriculum = json.load(f)

print(f"Loaded curriculum data: {len(curriculum['modules'])} modules.")

# Map of target CP-Algorithms / educational pages to scrape
SCRAPE_TARGETS = {
    "01": [
        "https://cp-algorithms.com/data_structures/fenwick.html",
    ],
    "02": [
        "https://cp-algorithms.com/data_structures/segment_tree.html",
    ],
    "03": [
        "https://cp-algorithms.com/data_structures/segment_tree.html",
    ],
    "04": [
        "https://cp-algorithms.com/data_structures/sqrt_decomposition.html",
    ],
    "05": [
        "https://cp-algorithms.com/data_structures/treap.html",
        "https://cp-algorithms.com/data_structures/sparse-table.html",
    ],
    "06": [
        "https://cp-algorithms.com/graph/lca.html",
        "https://cp-algorithms.com/graph/hld.html",
    ],
    "07": [
        "https://cp-algorithms.com/graph/strongly-connected-components.html",
        "https://cp-algorithms.com/graph/2SAT.html",
    ],
    "08": [
        "https://cp-algorithms.com/graph/dijkstra.html",
        "https://cp-algorithms.com/graph/euler_path.html",
    ],
    "09": [
        "https://cp-algorithms.com/graph/dinic.html",
        "https://cp-algorithms.com/graph/min_cost_flow.html",
        "https://cp-algorithms.com/graph/kuhn_maximum_bipartite_matching.html"
    ],
    "10": [
        "https://cp-algorithms.com/geometry/convex_hull_trick.html",
        "https://cp-algorithms.com/dynamic_programming/divide-and-conquer-dp.html",
    ],
    "11": [
        "https://cp-algorithms.com/string/string-hashing.html",
        "https://cp-algorithms.com/string/prefix-function.html",
        "https://cp-algorithms.com/string/aho_corasick.html",
        "https://cp-algorithms.com/string/suffix-automaton.html",
    ],
    "12": [
        "https://cp-algorithms.com/algebra/prime-sieve-linear.html",
        "https://cp-algorithms.com/algebra/extended-euclid-algorithm.html",
        "https://cp-algorithms.com/algebra/discrete-log.html"
    ],
    "13": [
        "https://cp-algorithms.com/combinatorics/binomial-coefficients.html",
        "https://cp-algorithms.com/combinatorics/burnside.html",
    ],
    "14": [
        "https://cp-algorithms.com/linear_algebra/linear-system-gauss.html",
        "https://cp-algorithms.com/linear_algebra/determinant-gauss.html",
    ],
    "15": [
        "https://cp-algorithms.com/algebra/fft.html",
    ],
    "16": [
        "https://cp-algorithms.com/game_theory/sprague-grundy-nim.html",
    ],
    "17": [
        "https://cp-algorithms.com/geometry/basic-geometry.html",
        "https://cp-algorithms.com/geometry/convex-hull.html",
        "https://cp-algorithms.com/geometry/intersecting_segments.html"
    ],
    "18": [
        "https://cp-algorithms.com/others/parallel-binary-search.html",
    ],
    "19": [
        "https://cp-algorithms.com/schedules/schedule-with-completion-duration.html"
    ],
    "20": [
        "https://cp-algorithms.com/dynamic_programming/knuth-optimization.html"
    ],
    "21": [
        "https://cp-algorithms.com/graph/dinic.html"
    ],
    "22": [
        "https://cp-algorithms.com/geometry/intersecting_segments.html"
    ]
}

def fetch_url(url):
    try:
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read().decode('utf-8', errors='ignore')
            # Extract main text / markdown
            clean = re.sub(r'<script[\s\S]*?</script>', '', html)
            clean = re.sub(r'<style[\s\S]*?</style>', '', clean)
            clean = re.sub(r'<[^>]+>', ' ', clean)
            clean = re.sub(r'\s+', ' ', clean).strip()
            return url, clean[:10000]
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return url, ""

print("Scraping educational sources concurrently...")
all_urls = [url for urls in SCRAPE_TARGETS.values() for url in urls]
url_contents = {}

with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
    results = executor.map(fetch_url, set(all_urls))
    for url, content in results:
        if content:
            url_contents[url] = content
            print(f"  Scraped {url} ({len(content)} chars)")

print(f"Successfully scraped {len(url_contents)} web pages!")
