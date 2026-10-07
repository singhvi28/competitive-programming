import React, { useState, useMemo, useEffect, useCallback } from 'react';
import { Download, Upload, RefreshCw, Users, Tag } from 'lucide-react';
import mirrorDataRaw from '../data/mirrorData.json';
import { MirrorRawProblem } from '../types/mirror';
import { useLocalStorageSet } from '../hooks/useLocalStorageSet';
import { useToast } from '../context/ToastContext';
import { SearchBar } from '../components/common/SearchBar';
import { MirrorProblemCard } from '../components/mirror/MirrorProblemCard';

const CF_HANDLES = ['akkisinghvi28', 'akshitsinghvi28'];
const mirrorData = mirrorDataRaw as unknown as MirrorRawProblem[];

export const MirrorPage: React.FC = () => {
  const { solvedSet, setSolvedSet, toggle, exportJSON, importJSON } = useLocalStorageSet(
    'cf_mirror_solved',
    'cf_mirror_progress'
  );
  const { showToast } = useToast();

  const [searchQuery, setSearchQuery] = useState('');
  const [selectedUser, setSelectedUser] = useState<'all' | 'both' | 'a.out' | 'Queue'>('all');
  const [selectedRating, setSelectedRating] = useState<number | 'all'>('all');
  const [selectedStatus, setSelectedStatus] = useState<'all' | 'unsolved' | 'solved'>('all');
  const [sortMode, setSortMode] = useState<
    'id_desc' | 'id_asc' | 'rating_desc' | 'rating_asc' | 'name_asc'
  >('id_desc');
  const [isSyncing, setIsSyncing] = useState(false);

  const totalProblems = mirrorData.length;
  const totalSolved = mirrorData.filter((p) => solvedSet.has(p.problem_id)).length;
  const globalPct = totalProblems > 0 ? Math.round((totalSolved / totalProblems) * 100) : 0;

  // Sync with Codeforces API
  const syncCF = useCallback(
    async (silent = false) => {
      if (isSyncing) return;
      setIsSyncing(true);

      let newlySolved = 0;
      let successfulAccounts = 0;

      try {
        const fetchPromises = CF_HANDLES.map(async (handle) => {
          try {
            const res = await fetch(`https://codeforces.com/api/user.status?handle=${handle}`);
            if (!res.ok) throw new Error(`HTTP ${res.status}`);
            const json = await res.json();
            if (json.status === 'OK' && Array.isArray(json.result)) {
              successfulAccounts++;
              return json.result;
            }
          } catch (err) {
            console.warn(`Could not sync handle ${handle}:`, err);
          }
          return [];
        });

        const results = await Promise.all(fetchPromises);
        const cfSolvedMap = new Set<string>();

        results.flat().forEach((sub) => {
          if (
            sub &&
            sub.verdict === 'OK' &&
            sub.problem &&
            sub.problem.contestId &&
            sub.problem.index
          ) {
            const pid = `${sub.problem.contestId}${sub.problem.index}`.toUpperCase();
            cfSolvedMap.add(pid);
          }
        });

        setSolvedSet((prev) => {
          const next = new Set(prev);
          mirrorData.forEach((p) => {
            const pid = String(p.problem_id).toUpperCase();
            if (cfSolvedMap.has(pid)) {
              if (!next.has(p.problem_id)) {
                next.add(p.problem_id);
                newlySolved++;
              }
            }
          });
          return next;
        });

        if (!silent) {
          if (successfulAccounts === 0) {
            showToast('Codeforces API is currently unreachable. Check your connection.', 'alert-circle');
          } else if (newlySolved > 0) {
            showToast(
              `Synced! Marked ${newlySolved} new problem(s) solved by your accounts.`,
              'check-circle-2'
            );
          } else {
            showToast(
              `Synced with accounts (${CF_HANDLES.join(', ')}). Progress is up to date!`,
              'check-circle-2'
            );
          }
        }
      } catch (err) {
        console.error('Error during CF sync:', err);
        if (!silent) {
          showToast('Error querying Codeforces API.', 'alert-circle');
        }
      } finally {
        setIsSyncing(false);
      }
    },
    [isSyncing, setSolvedSet, showToast]
  );

  // Initial silent background sync
  useEffect(() => {
    syncCF(true);
  }, []);

  const filteredProblems = useMemo(() => {
    const q = searchQuery.toLowerCase().trim();

    const filtered = mirrorData.filter((p) => {
      const isDone = solvedSet.has(p.problem_id);

      const matchStatus =
        selectedStatus === 'all' ||
        (selectedStatus === 'solved' && isDone) ||
        (selectedStatus === 'unsolved' && !isDone);

      const matchRating = selectedRating === 'all' || p.rating === selectedRating;

      let matchUser = true;
      if (selectedUser === 'both') {
        matchUser = p.solved_by && p.solved_by.length === 2;
      } else if (selectedUser === 'a.out') {
        matchUser = p.solved_by && p.solved_by.includes('a.out');
      } else if (selectedUser === 'Queue') {
        matchUser = p.solved_by && p.solved_by.includes('Queue');
      }

      const matchSearch =
        !q ||
        p.problem_id.toLowerCase().includes(q) ||
        p.name.toLowerCase().includes(q) ||
        (p.tags && p.tags.toLowerCase().includes(q)) ||
        String(p.rating).includes(q);

      return matchStatus && matchRating && matchUser && matchSearch;
    });

    if (sortMode === 'id_desc') {
      filtered.sort((a, b) => b.contest_id - a.contest_id || b.index.localeCompare(a.index));
    } else if (sortMode === 'id_asc') {
      filtered.sort((a, b) => a.contest_id - b.contest_id || a.index.localeCompare(b.index));
    } else if (sortMode === 'rating_desc') {
      filtered.sort((a, b) => b.rating - a.rating || b.contest_id - a.contest_id);
    } else if (sortMode === 'rating_asc') {
      filtered.sort((a, b) => a.rating - b.rating || a.contest_id - b.contest_id);
    } else if (sortMode === 'name_asc') {
      filtered.sort((a, b) => a.name.localeCompare(b.name));
    }

    return filtered;
  }, [searchQuery, selectedRating, selectedUser, selectedStatus, sortMode, solvedSet]);

  const handleExport = () => {
    exportJSON();
    showToast('Mirror progress exported!', 'download');
  };

  const handleImport = (e: React.ChangeEvent<HTMLInputElement>) => {
    importJSON(e, (count) => {
      showToast(`Imported ${count} solved problems!`, 'upload');
    });
  };

  return (
    <div className="min-h-screen">
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-8 pb-20">
        {/* Hero Section */}
        <div className="relative overflow-hidden rounded-2xl glass-panel p-6 sm:p-8 mb-8 glow-fuchsia border border-fuchsia-500/20">
          <div className="absolute -right-16 -bottom-16 w-64 h-64 bg-fuchsia-500/10 rounded-full blur-3xl pointer-events-none" />
          <div className="absolute -left-16 -top-16 w-64 h-64 bg-purple-500/10 rounded-full blur-3xl pointer-events-none" />

          <div className="relative z-10">
            <div className="flex flex-wrap items-center justify-between gap-4 mb-4">
              <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-fuchsia-500/10 border border-fuchsia-500/30 text-fuchsia-400 text-xs font-mono">
                <span className="w-2 h-2 rounded-full bg-fuchsia-400 animate-pulse" />
                <span>321 Filtered Problems &bull; Contest ID &gt; 1300 &bull; Ratings 1900–2300</span>
              </div>
              <div className="flex items-center space-x-2">
                <button
                  onClick={handleExport}
                  className="text-xs font-mono px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 flex items-center space-x-1.5 transition cursor-pointer"
                >
                  <Download className="w-3.5 h-3.5" />
                  <span>Export</span>
                </button>
                <label className="text-xs font-mono px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 flex items-center space-x-1.5 cursor-pointer transition">
                  <Upload className="w-3.5 h-3.5" />
                  <span>Import</span>
                  <input
                    type="file"
                    className="hidden"
                    onChange={handleImport}
                    accept=".json"
                  />
                </label>
                <button
                  onClick={() => syncCF(false)}
                  disabled={isSyncing}
                  className="text-xs font-mono px-3 py-1.5 rounded-lg bg-fuchsia-950/70 hover:bg-fuchsia-900/90 text-fuchsia-300 border border-fuchsia-800/80 flex items-center space-x-1.5 shadow-lg shadow-fuchsia-950/40 transition active:scale-95 cursor-pointer disabled:opacity-50"
                  title="Sync solves from CF accounts: akkisinghvi28 & akshitsinghvi28"
                >
                  <RefreshCw
                    className={`w-3.5 h-3.5 text-fuchsia-400 ${isSyncing ? 'animate-spin' : ''}`}
                  />
                  <span>{isSyncing ? 'Syncing...' : 'Sync CF'}</span>
                </button>
              </div>
            </div>

            <h1 className="text-2xl sm:text-4xl font-extrabold tracking-tight text-white mb-3">
              Codeforces Master Mirror
            </h1>
            <p className="text-sm sm:text-base text-slate-300 max-w-3xl leading-relaxed mb-6">
              The curated collection of <span className="text-fuchsia-400 font-semibold">321 modern problems</span> solved by top competitive programmers <span className="text-purple-400 font-mono font-bold">a.out</span> and <span className="text-teal-400 font-mono font-bold">Queue</span> with direct links to AC submissions and official tags. Solves by your CF accounts (<span className="text-fuchsia-300 font-mono">akkisinghvi28</span> / <span className="text-fuchsia-300 font-mono">akshitsinghvi28</span>) are synchronized and marked as completed.
            </p>

            {/* Progress Overview Bar */}
            <div className="bg-slate-900/90 rounded-xl p-4 border border-slate-800">
              <div className="flex flex-wrap items-center justify-between gap-2 mb-2">
                <div className="flex items-center space-x-3">
                  <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">
                    Total Solved
                  </span>
                  <span className="text-sm font-bold font-mono text-white">
                    {totalSolved} / {totalProblems} ({globalPct}%)
                  </span>
                </div>
                <div className="flex items-center space-x-4 text-xs font-mono text-slate-400">
                  {[1900, 2000, 2100, 2200, 2300].map((r) => {
                    const rProbs = mirrorData.filter((p) => p.rating === r);
                    const rSolved = rProbs.filter((p) => solvedSet.has(p.problem_id)).length;
                    const dotColors: Record<number, string> = {
                      1900: 'bg-purple-400',
                      2000: 'bg-orange-400',
                      2100: 'bg-amber-400',
                      2200: 'bg-rose-400',
                      2300: 'bg-red-500',
                    };
                    return (
                      <span key={r}>
                        <span className={`inline-block w-2.5 h-2.5 rounded-full ${dotColors[r]} mr-1`} />
                        {r}: <b className="text-slate-200">{rSolved}/{rProbs.length}</b>
                      </span>
                    );
                  })}
                </div>
              </div>
              <div className="w-full bg-slate-800 rounded-full h-2.5 overflow-hidden">
                <div
                  className="bg-gradient-to-r from-fuchsia-500 via-purple-500 to-emerald-400 h-2.5 rounded-full transition-all duration-300"
                  style={{ width: `${globalPct}%` }}
                />
              </div>
            </div>
          </div>
        </div>

        {/* Filters & Search Toolbar */}
        <div className="glass-panel p-4 rounded-xl mb-8 border border-slate-800 space-y-4">
          <div className="flex flex-col md:flex-row items-stretch md:items-center justify-between gap-3">
            <SearchBar
              value={searchQuery}
              onChange={setSearchQuery}
              placeholder="Search problems by ID (e.g. 2249C), title, or tag (dp, trees, greedy, math, graphs)..."
            />

            <div className="flex items-center space-x-2">
              <select
                value={sortMode}
                onChange={(e) => setSortMode(e.target.value as any)}
                className="bg-slate-900/90 text-xs font-mono text-slate-300 border border-slate-700/80 rounded-lg px-3 py-2 focus:outline-none focus:border-fuchsia-500 cursor-pointer"
              >
                <option value="id_desc">Newest Contest (ID ↓)</option>
                <option value="id_asc">Oldest Contest (ID ↑)</option>
                <option value="rating_desc">Rating (High to Low)</option>
                <option value="rating_asc">Rating (Low to High)</option>
                <option value="name_asc">Problem Name (A-Z)</option>
              </select>

              <div className="flex items-center space-x-1.5 bg-slate-900/90 p-1 rounded-lg border border-slate-800">
                {(['all', 'unsolved', 'solved'] as const).map((st) => (
                  <button
                    key={st}
                    onClick={() => setSelectedStatus(st)}
                    className={`px-3 py-1.5 rounded-md text-xs font-medium transition cursor-pointer ${
                      selectedStatus === st
                        ? 'bg-fuchsia-600 text-white font-semibold'
                        : 'text-slate-400 hover:text-white'
                    }`}
                  >
                    {st === 'all' ? 'All' : st === 'unsolved' ? 'To-Do' : 'Solved'}
                  </button>
                ))}
              </div>
            </div>
          </div>

          <div className="flex flex-wrap items-center justify-between gap-3 pt-2 border-t border-slate-800/80">
            {/* User Solver Pills */}
            <div className="flex flex-wrap items-center gap-1.5">
              <span className="text-xs font-semibold text-slate-400 mr-1 flex items-center">
                <Users className="w-3 h-3 mr-1" /> Solved By:
              </span>
              <button
                onClick={() => setSelectedUser('all')}
                className={`px-2.5 py-1 rounded text-xs font-mono font-medium transition cursor-pointer ${
                  selectedUser === 'all'
                    ? 'bg-fuchsia-600 text-white font-semibold border border-fuchsia-500'
                    : 'bg-slate-900 text-slate-300 border border-slate-800 hover:border-slate-700'
                }`}
              >
                All (321)
              </button>
              <button
                onClick={() => setSelectedUser('both')}
                className={`px-2.5 py-1 rounded text-xs font-mono font-medium transition cursor-pointer ${
                  selectedUser === 'both'
                    ? 'bg-fuchsia-600 text-white font-semibold border border-fuchsia-500'
                    : 'bg-slate-900 text-amber-400 border border-slate-800 hover:border-amber-500/50'
                }`}
              >
                Both (21)
              </button>
              <button
                onClick={() => setSelectedUser('a.out')}
                className={`px-2.5 py-1 rounded text-xs font-mono font-medium transition cursor-pointer ${
                  selectedUser === 'a.out'
                    ? 'bg-fuchsia-600 text-white font-semibold border border-fuchsia-500'
                    : 'bg-slate-900 text-purple-400 border border-slate-800 hover:border-purple-500/50'
                }`}
              >
                a.out (204)
              </button>
              <button
                onClick={() => setSelectedUser('Queue')}
                className={`px-2.5 py-1 rounded text-xs font-mono font-medium transition cursor-pointer ${
                  selectedUser === 'Queue'
                    ? 'bg-fuchsia-600 text-white font-semibold border border-fuchsia-500'
                    : 'bg-slate-900 text-teal-400 border border-slate-800 hover:border-teal-500/50'
                }`}
              >
                Queue (138)
              </button>
            </div>

            {/* Rating Pills */}
            <div className="flex flex-wrap items-center gap-1.5">
              <span className="text-xs font-semibold text-slate-400 mr-1 flex items-center">
                <Tag className="w-3 h-3 mr-1" /> Rating:
              </span>
              <button
                onClick={() => setSelectedRating('all')}
                className={`px-2.5 py-1 rounded text-xs font-mono font-medium transition cursor-pointer ${
                  selectedRating === 'all'
                    ? 'bg-indigo-600 text-white border border-indigo-500'
                    : 'bg-slate-900 text-slate-300 border border-slate-800 hover:border-slate-700'
                }`}
              >
                All
              </button>
              {[1900, 2000, 2100, 2200, 2300].map((r) => {
                const count = mirrorData.filter((p) => p.rating === r).length;
                return (
                  <button
                    key={r}
                    onClick={() => setSelectedRating(r)}
                    className={`px-2.5 py-1 rounded text-xs font-mono font-medium transition cursor-pointer ${
                      selectedRating === r
                        ? 'bg-indigo-600 text-white border border-indigo-500'
                        : 'bg-slate-900 text-slate-300 border border-slate-800 hover:border-slate-700'
                    }`}
                  >
                    {r} ({count})
                  </button>
                );
              })}
            </div>

            <div className="text-xs font-mono text-slate-400">
              Showing <span className="text-fuchsia-400 font-bold">{filteredProblems.length}</span> problems
            </div>
          </div>
        </div>

        {/* Problems Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {filteredProblems.map((problem) => (
            <MirrorProblemCard
              key={problem.problem_id}
              problem={problem}
              isSolved={solvedSet.has(problem.problem_id)}
              onToggle={toggle}
            />
          ))}
        </div>
      </main>
    </div>
  );
};
