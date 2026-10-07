import React, { useState, useMemo } from 'react';
import { Download, Upload, RotateCcw, Filter } from 'lucide-react';
import virtualContestsDataRaw from '../data/virtualContestsData.json';
import { VirtualContest } from '../types/virtualContests';
import { useLocalStorageSet } from '../hooks/useLocalStorageSet';
import { useToast } from '../context/ToastContext';
import { SearchBar } from '../components/common/SearchBar';
import { ContestCard } from '../components/virtual/ContestCard';

const contestsData = virtualContestsDataRaw as unknown as VirtualContest[];

export const VirtualContestsPage: React.FC = () => {
  const { solvedSet: practicedSet, toggle, reset, exportJSON, importJSON } = useLocalStorageSet(
    'cf_virtual_contests_progress',
    'cf_virtual_contests_progress'
  );
  const { showToast } = useToast();

  const [searchQuery, setSearchQuery] = useState('');
  const [selectedType, setSelectedType] = useState<string>('all');
  const [selectedStatus, setSelectedStatus] = useState<'all' | 'unpracticed' | 'practiced'>('all');
  const [sortMode, setSortMode] = useState<'id_desc' | 'id_asc' | 'name_asc'>('id_desc');

  const totalContests = contestsData.length;
  const totalPracticed = contestsData.filter((c) => practicedSet.has(c.id)).length;
  const globalPct = totalContests > 0 ? Math.round((totalPracticed / totalContests) * 100) : 0;

  const div2Total = useMemo(() => contestsData.filter((c) => c.type === 'Div. 2'), []);
  const div2Done = useMemo(
    () => div2Total.filter((c) => practicedSet.has(c.id)).length,
    [div2Total, practicedSet]
  );

  const eduTotal = useMemo(() => contestsData.filter((c) => c.type === 'Educational'), []);
  const eduDone = useMemo(
    () => eduTotal.filter((c) => practicedSet.has(c.id)).length,
    [eduTotal, practicedSet]
  );

  const combTotal = useMemo(() => contestsData.filter((c) => c.type === 'Combined / Global'), []);
  const combDone = useMemo(
    () => combTotal.filter((c) => practicedSet.has(c.id)).length,
    [combTotal, practicedSet]
  );

  const filteredContests = useMemo(() => {
    const q = searchQuery.toLowerCase().trim();

    const filtered = contestsData.filter((c) => {
      const matchType = selectedType === 'all' || c.type === selectedType;
      const isDone = practicedSet.has(c.id);
      const matchStatus =
        selectedStatus === 'all' ||
        (selectedStatus === 'practiced' && isDone) ||
        (selectedStatus === 'unpracticed' && !isDone);

      const matchSearch =
        !q ||
        c.id.includes(q) ||
        c.name.toLowerCase().includes(q) ||
        c.type.toLowerCase().includes(q);

      return matchType && matchStatus && matchSearch;
    });

    if (sortMode === 'id_desc') {
      filtered.sort((a, b) => parseInt(b.id) - parseInt(a.id));
    } else if (sortMode === 'id_asc') {
      filtered.sort((a, b) => parseInt(a.id) - parseInt(b.id));
    } else if (sortMode === 'name_asc') {
      filtered.sort((a, b) => a.name.localeCompare(b.name));
    }

    return filtered;
  }, [searchQuery, selectedType, selectedStatus, sortMode, practicedSet]);

  const handleExport = () => {
    exportJSON();
    showToast('Virtual contest progress exported!', 'download');
  };

  const handleImport = (e: React.ChangeEvent<HTMLInputElement>) => {
    importJSON(e, (count) => {
      showToast(`Imported ${count} practiced contests!`, 'upload');
    });
  };

  const handleReset = () => {
    if (window.confirm('Are you sure you want to reset all practiced virtual contest checkboxes?')) {
      reset();
      showToast('All virtual contest progress has been reset.', 'rotate-ccw');
    }
  };

  return (
    <div className="min-h-screen">
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-8 pb-20">
        {/* Hero Section */}
        <div className="relative overflow-hidden rounded-2xl glass-panel p-6 sm:p-8 mb-8 glow-cyan border border-cyan-500/20">
          <div className="absolute -right-16 -bottom-16 w-64 h-64 bg-cyan-500/10 rounded-full blur-3xl pointer-events-none" />
          <div className="absolute -left-16 -top-16 w-64 h-64 bg-teal-500/10 rounded-full blur-3xl pointer-events-none" />

          <div className="relative z-10">
            <div className="flex flex-wrap items-center justify-between gap-4 mb-4">
              <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-cyan-500/10 border border-cyan-500/30 text-cyan-400 text-xs font-mono">
                <span className="w-2 h-2 rounded-full bg-cyan-400 animate-pulse" />
                <span>237 Modern Contests &bull; Contest IDs 1315 to 2258</span>
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
                  onClick={handleReset}
                  className="text-xs font-mono px-3 py-1.5 rounded-lg bg-red-950/40 hover:bg-red-900/60 text-red-400 border border-red-800/40 flex items-center space-x-1.5 transition cursor-pointer"
                  title="Reset all saved progress"
                >
                  <RotateCcw className="w-3.5 h-3.5" />
                  <span>Reset</span>
                </button>
              </div>
            </div>

            <h1 className="text-2xl sm:text-4xl font-extrabold tracking-tight text-white mb-3">
              Codeforces Virtual Contests Library
            </h1>
            <p className="text-sm sm:text-base text-slate-300 max-w-3xl leading-relaxed mb-6">
              A high-yield collection of <span className="text-cyan-400 font-semibold">237 modern Codeforces rounds</span> for timed virtual simulation and contest speed drills. Practice under real 2-hour contest pressure, track completed rounds, and jump directly to virtual participation.
            </p>

            {/* Progress Overview Bar */}
            <div className="bg-slate-900/90 rounded-xl p-4 border border-slate-800">
              <div className="flex flex-wrap items-center justify-between gap-2 mb-2">
                <div className="flex items-center space-x-3">
                  <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">
                    Total Practiced
                  </span>
                  <span className="text-sm font-bold font-mono text-white">
                    {totalPracticed} / {totalContests} ({globalPct}%)
                  </span>
                </div>
                <div className="flex items-center space-x-4 text-xs font-mono text-slate-400">
                  <span>
                    <span className="inline-block w-2.5 h-2.5 rounded-full bg-cyan-400 mr-1" />
                    Div. 2: <b className="text-slate-200">{div2Done}/{div2Total.length}</b>
                  </span>
                  <span>
                    <span className="inline-block w-2.5 h-2.5 rounded-full bg-emerald-400 mr-1" />
                    Educational: <b className="text-slate-200">{eduDone}/{eduTotal.length}</b>
                  </span>
                  <span>
                    <span className="inline-block w-2.5 h-2.5 rounded-full bg-purple-400 mr-1" />
                    Combined/Global: <b className="text-slate-200">{combDone}/{combTotal.length}</b>
                  </span>
                </div>
              </div>
              <div className="w-full bg-slate-800 rounded-full h-2.5 overflow-hidden">
                <div
                  className="bg-gradient-to-r from-cyan-500 via-teal-500 to-emerald-400 h-2.5 rounded-full transition-all duration-300"
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
              placeholder="Search by contest ID (e.g. 2258), round number, or contest name..."
            />

            <div className="flex items-center space-x-2">
              <select
                value={sortMode}
                onChange={(e) => setSortMode(e.target.value as any)}
                className="bg-slate-900/90 text-xs font-mono text-slate-300 border border-slate-700/80 rounded-lg px-3 py-2 focus:outline-none focus:border-cyan-500 cursor-pointer"
              >
                <option value="id_desc">Newest First (ID ↓)</option>
                <option value="id_asc">Oldest First (ID ↑)</option>
                <option value="name_asc">Contest Name (A-Z)</option>
              </select>

              <div className="flex items-center space-x-1.5 bg-slate-900/90 p-1 rounded-lg border border-slate-800">
                {(['all', 'unpracticed', 'practiced'] as const).map((st) => (
                  <button
                    key={st}
                    onClick={() => setSelectedStatus(st)}
                    className={`px-3 py-1.5 rounded-md text-xs font-medium transition cursor-pointer ${
                      selectedStatus === st
                        ? 'bg-cyan-600 text-black font-semibold'
                        : 'text-slate-400 hover:text-white'
                    }`}
                  >
                    {st === 'all' ? 'All' : st === 'unpracticed' ? 'To-Do' : 'Done'}
                  </button>
                ))}
              </div>
            </div>
          </div>

          <div className="flex flex-wrap items-center justify-between gap-2 pt-2 border-t border-slate-800/80">
            <div className="flex flex-wrap items-center gap-1.5">
              <span className="text-xs font-semibold text-slate-400 mr-1 flex items-center">
                <Filter className="w-3 h-3 mr-1" /> Contest Type:
              </span>
              <button
                onClick={() => setSelectedType('all')}
                className={`px-2.5 py-1 rounded text-xs font-mono font-medium transition cursor-pointer ${
                  selectedType === 'all'
                    ? 'bg-cyan-600 text-black font-semibold border border-cyan-500'
                    : 'bg-slate-900 text-slate-300 border border-slate-800 hover:border-slate-700'
                }`}
              >
                All ({totalContests})
              </button>
              <button
                onClick={() => setSelectedType('Div. 2')}
                className={`px-2.5 py-1 rounded text-xs font-mono font-medium transition cursor-pointer ${
                  selectedType === 'Div. 2'
                    ? 'bg-cyan-600 text-black font-semibold border border-cyan-500'
                    : 'bg-slate-900 text-cyan-400 border border-slate-800 hover:border-cyan-500/50'
                }`}
              >
                Div. 2 ({div2Total.length})
              </button>
              <button
                onClick={() => setSelectedType('Educational')}
                className={`px-2.5 py-1 rounded text-xs font-mono font-medium transition cursor-pointer ${
                  selectedType === 'Educational'
                    ? 'bg-cyan-600 text-black font-semibold border border-cyan-500'
                    : 'bg-slate-900 text-emerald-400 border border-slate-800 hover:border-emerald-500/50'
                }`}
              >
                Educational ({eduTotal.length})
              </button>
              <button
                onClick={() => setSelectedType('Combined / Global')}
                className={`px-2.5 py-1 rounded text-xs font-mono font-medium transition cursor-pointer ${
                  selectedType === 'Combined / Global'
                    ? 'bg-cyan-600 text-black font-semibold border border-cyan-500'
                    : 'bg-slate-900 text-purple-400 border border-slate-800 hover:border-purple-500/50'
                }`}
              >
                Combined / Global ({combTotal.length})
              </button>
            </div>

            <div className="text-xs font-mono text-slate-400">
              Showing <span className="text-cyan-400 font-bold">{filteredContests.length}</span> contests
            </div>
          </div>
        </div>

        {/* Contests Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {filteredContests.map((contest) => (
            <ContestCard
              key={contest.id}
              contest={contest}
              isPracticed={practicedSet.has(contest.id)}
              onToggle={toggle}
            />
          ))}
        </div>
      </main>
    </div>
  );
};
