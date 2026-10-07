import React, { useState, useMemo } from 'react';
import { Download, Upload, RotateCcw, Layers } from 'lucide-react';
import leetcodeDataRaw from '../data/leetcodeData.json';
import { LeetCodeCategory, LeetCodeProblem } from '../types/leetcode';
import { useLocalStorageSet } from '../hooks/useLocalStorageSet';
import { useToast } from '../context/ToastContext';
import { SearchBar } from '../components/common/SearchBar';
import { CategorySection } from '../components/leetcode/CategorySection';

const leetcodeCategories = leetcodeDataRaw as unknown as LeetCodeCategory[];

export const LeetCodeHardsPage: React.FC = () => {
  const { solvedSet, toggle, reset, exportJSON, importJSON } = useLocalStorageSet(
    'leetcode_hards_progress',
    'leetcode_hards_progress'
  );
  const { showToast } = useToast();

  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<number | 'all'>('all');
  const [selectedStatus, setSelectedStatus] = useState<'all' | 'unsolved' | 'solved'>('all');

  const allProblems = useMemo(() => {
    const list: LeetCodeProblem[] = [];
    leetcodeCategories.forEach((c) => list.push(...c.problems));
    return list;
  }, []);

  const totalProblems = allProblems.length;
  const totalSolved = allProblems.filter((p) => solvedSet.has(String(p.id))).length;
  const globalPct = totalProblems > 0 ? Math.round((totalSolved / totalProblems) * 100) : 0;

  // Filter problems per category
  const filteredCategories = useMemo(() => {
    const q = searchQuery.toLowerCase().trim();
    return leetcodeCategories.map((c, idx) => {
      const catId = idx + 1;
      const isCatSelected = selectedCategory === 'all' || selectedCategory === catId;

      if (!isCatSelected) {
        return {
          catId,
          category: c,
          problems: [],
        };
      }

      const filtered = c.problems.filter((p) => {
        const isSolved = solvedSet.has(String(p.id));

        const matchStatus =
          selectedStatus === 'all' ||
          (selectedStatus === 'solved' && isSolved) ||
          (selectedStatus === 'unsolved' && !isSolved);

        const matchSearch =
          !q ||
          p.name.toLowerCase().includes(q) ||
          String(p.id).toLowerCase().includes(q) ||
          (p.why && p.why.toLowerCase().includes(q)) ||
          (p.companies && p.companies.some((comp) => comp.toLowerCase().includes(q)));

        return matchStatus && matchSearch;
      });

      return {
        catId,
        category: c,
        problems: filtered,
      };
    });
  }, [searchQuery, selectedCategory, selectedStatus, solvedSet]);

  const totalVisible = useMemo(() => {
    return filteredCategories.reduce((acc, curr) => acc + curr.problems.length, 0);
  }, [filteredCategories]);

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
    if (window.confirm('Are you sure you want to reset all solved LeetCode checkboxes?')) {
      reset();
      showToast('All LeetCode progress has been reset.', 'rotate-ccw');
    }
  };

  return (
    <div className="min-h-screen">
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-8 pb-20">
        {/* Hero Section */}
        <div className="relative overflow-hidden rounded-2xl glass-panel p-6 sm:p-8 mb-8 glow-amber border border-amber-500/20">
          <div className="absolute -right-16 -bottom-16 w-64 h-64 bg-amber-500/10 rounded-full blur-3xl pointer-events-none" />
          <div className="absolute -left-16 -top-16 w-64 h-64 bg-red-500/10 rounded-full blur-3xl pointer-events-none" />

          <div className="relative z-10">
            <div className="flex flex-wrap items-center justify-between gap-4 mb-4">
              <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-amber-500/10 border border-amber-500/30 text-amber-400 text-xs font-mono">
                <span className="w-2 h-2 rounded-full bg-amber-400 animate-pulse" />
                <span>301 Classified Hard Problems &bull; 3 Signal Tiers</span>
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
              LeetCode Hard Classified Guide
            </h1>
            <p className="text-sm sm:text-base text-slate-300 max-w-3xl leading-relaxed mb-6">
              A high-signal classification of 301 LeetCode Hard problems categorized into{' '}
              <span className="text-emerald-400 font-semibold">Direct Interview Classics</span> (Tier-1 staples),{' '}
              <span className="text-amber-400 font-semibold">Niche Concept Problems</span> (transferable patterns), and{' '}
              <span className="text-rose-400 font-semibold">CP-Tier / Exotic Problems</span> (maximum signal).
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
                  {leetcodeCategories.map((c, idx) => {
                    const catId = idx + 1;
                    const catSolved = c.problems.filter((p) => solvedSet.has(String(p.id))).length;
                    const dotColors: Record<number, string> = {
                      1: 'bg-emerald-400',
                      2: 'bg-amber-400',
                      3: 'bg-rose-400',
                    };
                    const catLabels = ['Classics', 'Concepts', 'CP/Exotic'];
                    return (
                      <span key={catId}>
                        <span className={`inline-block w-2.5 h-2.5 rounded-full ${dotColors[catId]} mr-1`} />
                        Cat {catId} ({catLabels[idx]}):{' '}
                        <b className="text-slate-200">
                          {catSolved}/{c.problems.length}
                        </b>
                      </span>
                    );
                  })}
                </div>
              </div>
              <div className="w-full bg-slate-800 rounded-full h-2.5 overflow-hidden">
                <div
                  className="bg-gradient-to-r from-amber-500 via-orange-500 to-emerald-400 h-2.5 rounded-full transition-all duration-300"
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
              placeholder="Search problems by #ID, title, company tag (Google, Meta, Citadel, HRT), or concept..."
            />

            <div className="flex items-center space-x-1.5 bg-slate-900/90 p-1 rounded-lg border border-slate-800">
              {(['all', 'unsolved', 'solved'] as const).map((st) => (
                <button
                  key={st}
                  onClick={() => setSelectedStatus(st)}
                  className={`px-3 py-1.5 rounded-md text-xs font-medium transition cursor-pointer ${
                    selectedStatus === st
                      ? 'bg-amber-600 text-black font-semibold'
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
                <Layers className="w-3 h-3 mr-1" /> Category:
              </span>
              <button
                onClick={() => setSelectedCategory('all')}
                className={`px-2.5 py-1 rounded text-xs font-mono font-medium transition cursor-pointer ${
                  selectedCategory === 'all'
                    ? 'bg-amber-600 text-black font-semibold border border-amber-500'
                    : 'bg-slate-900 text-slate-300 border border-slate-800 hover:border-slate-700'
                }`}
              >
                All ({totalProblems})
              </button>
              {leetcodeCategories.map((c, idx) => {
                const catId = idx + 1;
                const catCount = c.problems.length;
                const catNames = ['Cat 1: Classics', 'Cat 2: Concepts', 'Cat 3: CP & Exotic'];
                return (
                  <button
                    key={catId}
                    onClick={() => setSelectedCategory(catId)}
                    className={`px-2.5 py-1 rounded text-xs font-mono font-medium transition cursor-pointer ${
                      selectedCategory === catId
                        ? 'bg-amber-600 text-black font-semibold border border-amber-500'
                        : 'bg-slate-900 text-slate-300 border border-slate-800 hover:border-slate-700'
                    }`}
                  >
                    {catNames[idx]} ({catCount})
                  </button>
                );
              })}
            </div>

            <div className="text-xs font-mono text-slate-400">
              Showing <span className="text-amber-400 font-bold">{totalVisible}</span> problems
            </div>
          </div>
        </div>

        {/* Categories Container */}
        <div className="space-y-8">
          {filteredCategories.map(({ catId, category, problems }) => (
            <CategorySection
              key={catId}
              categoryId={catId}
              category={category}
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
