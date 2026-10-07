import React, { useState, useMemo } from 'react';
import { Download, Upload, RotateCcw, Tag } from 'lucide-react';
import curriculumDataRaw from '../data/curriculumData.json';
import { CurriculumData, CurriculumProblem } from '../types/curriculum';
import { useLocalStorageSet } from '../hooks/useLocalStorageSet';
import { useToast } from '../context/ToastContext';
import { SearchBar } from '../components/common/SearchBar';
import { RoadmapSection } from '../components/curriculum/RoadmapSection';
import { GeometryCheatSheet } from '../components/curriculum/GeometryCheatSheet';
import { ModuleSection } from '../components/curriculum/ModuleSection';

const curriculumData = curriculumDataRaw as unknown as CurriculumData;

export const CurriculumPage: React.FC = () => {
  const { solvedSet, toggle, reset, exportJSON, importJSON } = useLocalStorageSet(
    'cf_curriculum_solved',
    'codeforces_master_progress'
  );
  const { showToast } = useToast();

  const [searchQuery, setSearchQuery] = useState('');
  const [selectedRating, setSelectedRating] = useState<number | 'all'>('all');
  const [selectedStatus, setSelectedStatus] = useState<'all' | 'unsolved' | 'solved'>('all');

  const allProblems = useMemo(() => {
    const list: CurriculumProblem[] = [];
    curriculumData.modules.forEach((m) => list.push(...m.problems));
    return list;
  }, []);

  const totalProblems = allProblems.length;
  const totalSolved = allProblems.filter((p) => solvedSet.has(p.id)).length;
  const globalPct = totalProblems > 0 ? Math.round((totalSolved / totalProblems) * 100) : 0;

  // Filter problems per module
  const filteredModules = useMemo(() => {
    const q = searchQuery.toLowerCase().trim();
    return curriculumData.modules.map((m) => {
      const filtered = m.problems.filter((p) => {
        const isSolved = solvedSet.has(p.id);

        const matchStatus =
          selectedStatus === 'all' ||
          (selectedStatus === 'solved' && isSolved) ||
          (selectedStatus === 'unsolved' && !isSolved);

        const matchRating = selectedRating === 'all' || p.rating === selectedRating;

        const matchSearch =
          !q ||
          p.name.toLowerCase().includes(q) ||
          p.id.toLowerCase().includes(q) ||
          p.technique.toLowerCase().includes(q) ||
          p.insight.toLowerCase().includes(q) ||
          String(p.rating).includes(q) ||
          p.tags.some((t) => t.toLowerCase().includes(q));

        return matchStatus && matchRating && matchSearch;
      });

      return {
        module: m,
        problems: filtered,
      };
    });
  }, [searchQuery, selectedRating, selectedStatus, solvedSet]);

  const totalVisible = useMemo(() => {
    return filteredModules.reduce((acc, curr) => acc + curr.problems.length, 0);
  }, [filteredModules]);

  const handleExport = () => {
    exportJSON();
    showToast('Progress exported successfully!', 'download');
  };

  const handleImport = (e: React.ChangeEvent<HTMLInputElement>) => {
    importJSON(e, (count) => {
      showToast(`Imported ${count} solved problems!`, 'upload');
    });
  };

  const handleReset = () => {
    if (window.confirm('Are you sure you want to reset all solved problems in this curriculum?')) {
      reset();
      showToast('All progress has been reset.', 'rotate-ccw');
    }
  };

  return (
    <div className="min-h-screen">
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-8 pb-20">
        {/* Hero Section */}
        <div className="relative overflow-hidden rounded-2xl glass-panel p-6 sm:p-8 mb-8 glow-indigo border border-indigo-500/20">
          <div className="absolute -right-16 -bottom-16 w-64 h-64 bg-indigo-500/10 rounded-full blur-3xl pointer-events-none" />
          <div className="absolute -left-16 -top-16 w-64 h-64 bg-purple-500/10 rounded-full blur-3xl pointer-events-none" />

          <div className="relative z-10">
            <div className="flex flex-wrap items-center justify-between gap-4 mb-4">
              <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-indigo-500/10 border border-indigo-500/30 text-indigo-400 text-xs font-mono">
                <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
                <span>144 Problems &bull; Contest ID &ge; 1300 &bull; Verified Official CF Ratings</span>
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
              Codeforces Candidate Master Curriculum
            </h1>
            <p className="text-sm sm:text-base text-slate-300 max-w-3xl leading-relaxed mb-6">
              A high-yield problem set engineered for the{' '}
              <span className="text-purple-400 font-semibold">Expert (1600–1899)</span> to{' '}
              <span className="text-purple-400 font-semibold">Candidate Master (1900–2300)</span> transition.
              Focuses on invariant transformations, HLD, dynamic segment reductions, 2-SAT, min-cost flows, and competitive geometry.
            </p>

            {/* Progress Overview Bar */}
            <div className="bg-slate-900/90 rounded-xl p-4 border border-slate-800">
              <div className="flex flex-wrap items-center justify-between gap-2 mb-2">
                <div className="flex items-center space-x-3">
                  <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">
                    Overall Mastery
                  </span>
                  <span className="text-sm font-bold font-mono text-white">
                    {totalSolved} / {totalProblems} ({globalPct}%)
                  </span>
                </div>
                <div className="flex items-center space-x-4 text-xs font-mono text-slate-400">
                  {[1900, 2000, 2100, 2200, 2300].map((r) => {
                    const rProbs = allProblems.filter((p) => p.rating === r);
                    const rSolved = rProbs.filter((p) => solvedSet.has(p.id)).length;
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
                  className="bg-gradient-to-r from-indigo-500 via-purple-500 to-emerald-400 h-2.5 rounded-full transition-all duration-300"
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
              placeholder="Search problems, techniques (e.g. Euler Tour, 2-SAT, Pick's, HLD, SegTree, Dinic)..."
            />

            <div className="flex items-center space-x-1.5 bg-slate-900/90 p-1 rounded-lg border border-slate-800">
              {(['all', 'unsolved', 'solved'] as const).map((st) => (
                <button
                  key={st}
                  onClick={() => setSelectedStatus(st)}
                  className={`px-3 py-1.5 rounded-md text-xs font-medium transition cursor-pointer ${
                    selectedStatus === st
                      ? 'bg-indigo-600 text-white font-semibold'
                      : 'text-slate-400 hover:text-white'
                  }`}
                >
                  {st === 'all' ? 'All' : st === 'unsolved' ? 'To-Do' : 'Solved'}
                </button>
              ))}
            </div>
          </div>

          <div className="flex flex-wrap items-center justify-between gap-2 pt-2 border-t border-slate-800/80">
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
                const count = allProblems.filter((p) => p.rating === r).length;
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
              Showing <span className="text-indigo-400 font-bold">{totalVisible}</span> problems
            </div>
          </div>
        </div>

        {/* 6-Week Structured Roadmap */}
        <RoadmapSection schedule={curriculumData.schedule} solvedSet={solvedSet} />

        {/* Computational Geometry Mastery Reference Card */}
        <GeometryCheatSheet />

        {/* Modules Container */}
        <div className="space-y-8">
          {filteredModules.map(({ module, problems }) => (
            <ModuleSection
              key={module.id}
              module={module}
              filteredProblems={problems}
              solvedSet={solvedSet}
              onToggle={toggle}
            />
          ))}
        </div>
      </main>
    </div>
  );
};
