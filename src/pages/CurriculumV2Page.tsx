import React, { useState, useMemo, useEffect, useRef } from 'react';
import { 
  Download, 
  Upload, 
  RotateCcw, 
  Award, 
  Sparkles, 
  Search, 
  Filter, 
  BookOpen,
  Code2
} from 'lucide-react';
import curriculumV2DataRaw from '../data/curriculumV2Data.json';
import { CurriculumV2Data, CurriculumV2Topic } from '../types/curriculumV2';
import { useLocalStorageSet } from '../hooks/useLocalStorageSet';
import { useToast } from '../context/ToastContext';
import { ModuleSection } from '../components/curriculum-v2/ModuleSection';
import { PhaseRoadmap } from '../components/curriculum-v2/PhaseRoadmap';
import { RoiMatrixModal } from '../components/curriculum-v2/RoiMatrixModal';
import { MasterCheatSheetModal } from '../components/curriculum-v2/MasterCheatSheetModal';

const curriculumV2Data = curriculumV2DataRaw as unknown as CurriculumV2Data;

export const CurriculumV2Page: React.FC = () => {
  const { solvedSet, toggle, reset, exportJSON, importJSON } = useLocalStorageSet(
    'cf_curriculum_v2_solved',
    'codeforces_masterclass_v2_progress'
  );
  const { showToast } = useToast();

  const searchInputRef = useRef<HTMLInputElement>(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedRoi, setSelectedRoi] = useState<string>('all');
  const [selectedPhase, setSelectedPhase] = useState<number | 'all'>('all');
  const [selectedTrack, setSelectedTrack] = useState<string | 'all'>('all');
  const [selectedStatus, setSelectedStatus] = useState<'all' | 'unsolved' | 'solved'>('all');

  const [isRoiModalOpen, setIsRoiModalOpen] = useState(false);
  const [isCheatSheetModalOpen, setIsCheatSheetModalOpen] = useState(false);

  // Keyboard shortcut '/' for search
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === '/' && document.activeElement !== searchInputRef.current) {
        e.preventDefault();
        searchInputRef.current?.focus();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  // Compute all topics across all modules
  const allTopics = useMemo(() => {
    const list: CurriculumV2Topic[] = [];
    curriculumV2Data.modules.forEach((m) => list.push(...m.topics));
    return list;
  }, []);

  const totalTopics = allTopics.length;
  const totalSolved = allTopics.filter((t) => solvedSet.has(t.id)).length;
  const globalPct = totalTopics > 0 ? Math.round((totalSolved / totalTopics) * 100) : 0;

  // Track sections set for filtering
  const activeTrackSections = useMemo(() => {
    if (selectedTrack === 'all') return null;
    const track = curriculumV2Data.tracks.find((t) => t.id === selectedTrack);
    return track ? new Set(track.sections) : null;
  }, [selectedTrack]);

  // Topic counts by phase for roadmap
  const topicCountsByPhase = useMemo(() => {
    const counts: Record<number, { total: number; solved: number }> = {};
    curriculumV2Data.phases.forEach((p) => {
      counts[p.id] = { total: 0, solved: 0 };
    });

    curriculumV2Data.modules.forEach((m) => {
      const pid = m.phaseId;
      if (!counts[pid]) counts[pid] = { total: 0, solved: 0 };
      counts[pid].total += m.topics.length;
      counts[pid].solved += m.topics.filter((t) => solvedSet.has(t.id)).length;
    });

    return counts;
  }, [solvedSet]);

  // Filter modules and topics
  const filteredModules = useMemo(() => {
    const q = searchQuery.toLowerCase().trim();

    return curriculumV2Data.modules
      .filter((m) => {
        // Phase filter
        if (selectedPhase !== 'all' && m.phaseId !== selectedPhase) {
          return false;
        }
        // Track filter
        if (activeTrackSections && !activeTrackSections.has(m.sectionId)) {
          return false;
        }
        return true;
      })
      .map((m) => {
        const filteredTopics = m.topics.filter((t) => {
          const isSolved = solvedSet.has(t.id);

          // Status filter
          const matchStatus =
            selectedStatus === 'all' ||
            (selectedStatus === 'solved' && isSolved) ||
            (selectedStatus === 'unsolved' && !isSolved);

          // ROI filter
          const matchRoi =
            selectedRoi === 'all' ||
            t.roi.toLowerCase().includes(selectedRoi.toLowerCase());

          // Search query
          const matchSearch =
            !q ||
            t.title.toLowerCase().includes(q) ||
            t.id.toLowerCase().includes(q) ||
            t.sectionTitle.toLowerCase().includes(q) ||
            t.ratingRange.toLowerCase().includes(q) ||
            t.prerequisites.toLowerCase().includes(q) ||
            t.coreIntuition.toLowerCase().includes(q) ||
            t.recognitionPatterns.some((p) => p.toLowerCase().includes(q)) ||
            t.derivation.toLowerCase().includes(q);

          return matchStatus && matchRoi && matchSearch;
        });

        return {
          module: m,
          filteredTopics,
        };
      })
      .filter((item) => item.filteredTopics.length > 0);
  }, [searchQuery, selectedRoi, selectedPhase, selectedStatus, activeTrackSections, solvedSet]);

  const totalVisible = useMemo(() => {
    return filteredModules.reduce((acc, curr) => acc + curr.filteredTopics.length, 0);
  }, [filteredModules]);

  const handleExport = () => {
    exportJSON();
    showToast('Curriculum V2 progress exported successfully!', 'download');
  };

  const handleImport = (e: React.ChangeEvent<HTMLInputElement>) => {
    importJSON(e, (count) => {
      showToast(`Imported ${count} mastered topics!`, 'upload');
    });
  };

  const handleReset = () => {
    if (window.confirm('Are you sure you want to reset all mastered progress in Curriculum V2?')) {
      reset();
      showToast('All progress has been reset.', 'rotate-ccw');
    }
  };

  return (
    <div className="min-h-screen">
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-8 pb-24">
        {/* Hero Banner */}
        <div className="relative overflow-hidden rounded-2xl glass-panel p-6 sm:p-8 mb-8 glow-emerald border border-emerald-500/20">
          <div className="absolute -right-20 -bottom-20 w-80 h-80 bg-emerald-500/10 rounded-full blur-3xl pointer-events-none" />
          <div className="absolute -left-20 -top-20 w-80 h-80 bg-indigo-500/10 rounded-full blur-3xl pointer-events-none" />

          <div className="relative z-10">
            {/* Top Toolbar in Banner */}
            <div className="flex flex-wrap items-center justify-between gap-4 mb-4">
              <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs font-mono">
                <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
                <span>
                  22 Sections &bull; 8 Phases &bull; 1400–2800+ Masterclass &bull; Complete Adv-DSA
                </span>
              </div>

              <div className="flex items-center space-x-2">
                <button
                  onClick={() => setIsRoiModalOpen(true)}
                  className="text-xs font-mono px-3 py-1.5 rounded-lg bg-indigo-950/70 hover:bg-indigo-900/80 text-indigo-300 border border-indigo-700/60 flex items-center space-x-1.5 transition cursor-pointer"
                >
                  <Award className="w-3.5 h-3.5 text-indigo-400" />
                  <span>ROI Matrix</span>
                </button>

                <button
                  onClick={() => setIsCheatSheetModalOpen(true)}
                  className="text-xs font-mono px-3 py-1.5 rounded-lg bg-purple-950/70 hover:bg-purple-900/80 text-purple-300 border border-purple-700/60 flex items-center space-x-1.5 transition cursor-pointer"
                >
                  <Sparkles className="w-3.5 h-3.5 text-purple-400" />
                  <span>Cheat Sheet</span>
                </button>

                <button
                  onClick={handleExport}
                  className="text-xs font-mono px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 flex items-center space-x-1.5 transition cursor-pointer"
                >
                  <Download className="w-3.5 h-3.5" />
                  <span className="hidden sm:inline">Export</span>
                </button>

                <label className="text-xs font-mono px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 flex items-center space-x-1.5 cursor-pointer transition">
                  <Upload className="w-3.5 h-3.5" />
                  <span className="hidden sm:inline">Import</span>
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
                  <span className="hidden sm:inline">Reset</span>
                </button>
              </div>
            </div>

            <h1 className="text-2xl sm:text-4xl font-extrabold tracking-tight text-white mb-3">
              Advanced Competitive Programming Masterclass (Curriculum V2)
            </h1>
            <p className="text-sm sm:text-base text-slate-300 max-w-4xl leading-relaxed mb-6">
              Complete theoretical, mathematical, and contest-calibrated system from{' '}
              <span className="text-emerald-400 font-semibold font-mono">adv-dsa</span>. Covers 22 modules across 8 thematic phases from linear sweeps, difference arrays, and monoid segment trees to matroid intersection, Slope Trick, formal power series, and geometric reductions.
            </p>

            {/* Overall Mastery Bar */}
            <div className="bg-slate-900/90 rounded-xl p-4 border border-slate-800 space-y-3">
              <div className="flex flex-wrap items-center justify-between gap-2">
                <div className="flex items-center space-x-3">
                  <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">
                    Masterclass Progress
                  </span>
                  <span className="text-sm font-bold font-mono text-white">
                    {totalSolved} / {totalTopics} Topics ({globalPct}%)
                  </span>
                </div>

                <div className="flex flex-wrap items-center gap-3 text-xs font-mono text-slate-300">
                  <span className="flex items-center space-x-1">
                    <span className="w-2 h-2 rounded-full bg-emerald-400" />
                    <span>S-Tier: {curriculumV2Data.metadata.roiDistribution['S-tier']}</span>
                  </span>
                  <span className="flex items-center space-x-1">
                    <span className="w-2 h-2 rounded-full bg-indigo-400" />
                    <span>A-Tier: {curriculumV2Data.metadata.roiDistribution['A-tier']}</span>
                  </span>
                  <span className="flex items-center space-x-1">
                    <span className="w-2 h-2 rounded-full bg-purple-400" />
                    <span>B-Tier: {curriculumV2Data.metadata.roiDistribution['B-tier']}</span>
                  </span>
                  <span className="flex items-center space-x-1">
                    <Code2 className="w-3.5 h-3.5 text-cyan-400" />
                    <span>{curriculumV2Data.metadata.totalTemplates} C++ Templates</span>
                  </span>
                </div>
              </div>

              <div className="w-full bg-slate-800 rounded-full h-2.5 overflow-hidden">
                <div
                  className="bg-gradient-to-r from-emerald-500 via-teal-400 to-indigo-500 h-2.5 rounded-full transition-all duration-300"
                  style={{ width: `${globalPct}%` }}
                />
              </div>
            </div>
          </div>
        </div>

        {/* Phase & Track Roadmap Selector */}
        <PhaseRoadmap
          phases={curriculumV2Data.phases}
          tracks={curriculumV2Data.tracks}
          selectedPhase={selectedPhase}
          onSelectPhase={setSelectedPhase}
          selectedTrack={selectedTrack}
          onSelectTrack={setSelectedTrack}
          topicCountsByPhase={topicCountsByPhase}
        />

        {/* Filters & Search Toolbar */}
        <div className="glass-panel p-4 rounded-xl mb-8 border border-slate-800 space-y-4">
          <div className="flex flex-col md:flex-row items-stretch md:items-center justify-between gap-3">
            <div className="relative flex-1">
              <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
              <input
                ref={searchInputRef}
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search topics, formulas, invariant clues, rating range (Press '/' to focus)..."
                className="w-full pl-10 pr-4 py-2 text-xs sm:text-sm rounded-lg bg-slate-900 border border-slate-800 text-white placeholder-slate-500 focus:outline-none focus:border-emerald-500"
              />
            </div>

            <div className="flex items-center space-x-1.5 bg-slate-900 p-1 rounded-lg border border-slate-800 flex-shrink-0">
              {(['all', 'unsolved', 'solved'] as const).map((st) => (
                <button
                  key={st}
                  onClick={() => setSelectedStatus(st)}
                  className={`px-3 py-1.5 rounded-md text-xs font-medium transition cursor-pointer ${
                    selectedStatus === st
                      ? 'bg-emerald-600 text-white font-semibold'
                      : 'text-slate-400 hover:text-white'
                  }`}
                >
                  {st === 'all' ? 'All' : st === 'unsolved' ? 'To Learn' : 'Mastered'}
                </button>
              ))}
            </div>
          </div>

          <div className="flex flex-wrap items-center justify-between gap-3 pt-2 border-t border-slate-800/80">
            <div className="flex flex-wrap items-center gap-1.5">
              <span className="text-xs font-semibold text-slate-400 mr-1 flex items-center">
                <Filter className="w-3.5 h-3.5 mr-1" /> ROI Tier:
              </span>
              {(['all', 'S-tier', 'A-tier', 'B-tier', 'C-tier', 'Niche'] as const).map((tier) => (
                <button
                  key={tier}
                  onClick={() => setSelectedRoi(tier)}
                  className={`px-2.5 py-1 rounded text-xs font-mono font-medium transition cursor-pointer ${
                    selectedRoi === tier
                      ? 'bg-emerald-600 text-white border border-emerald-500'
                      : 'bg-slate-900 text-slate-300 border border-slate-800 hover:border-slate-700'
                  }`}
                >
                  {tier === 'all' ? 'All Tiers' : tier}
                </button>
              ))}
            </div>

            <div className="text-xs font-mono text-slate-400">
              Showing <span className="text-emerald-400 font-bold">{totalVisible}</span> topics in{' '}
              <span className="text-indigo-400 font-bold">{filteredModules.length}</span> modules
            </div>
          </div>
        </div>

        {/* Modules Sections */}
        <div className="space-y-8">
          {filteredModules.map(({ module, filteredTopics }) => (
            <ModuleSection
              key={module.id}
              module={module}
              filteredTopics={filteredTopics}
              solvedSet={solvedSet}
              onToggle={toggle}
            />
          ))}

          {filteredModules.length === 0 && (
            <div className="glass-panel p-12 text-center rounded-xl border border-slate-800 space-y-3">
              <BookOpen className="w-8 h-8 text-slate-500 mx-auto" />
              <h3 className="text-base font-bold text-white">No topics match your current filters</h3>
              <p className="text-xs text-slate-400 max-w-md mx-auto">
                Try clearing your search query or selecting &ldquo;All Tiers&rdquo; / &ldquo;All Phases&rdquo; above.
              </p>
              <button
                onClick={() => {
                  setSearchQuery('');
                  setSelectedRoi('all');
                  setSelectedPhase('all');
                  setSelectedTrack('all');
                  setSelectedStatus('all');
                }}
                className="mt-2 text-xs font-mono px-4 py-2 rounded-lg bg-emerald-600 text-white font-semibold hover:bg-emerald-500 transition cursor-pointer"
              >
                Reset All Filters
              </button>
            </div>
          )}
        </div>

        {/* Modals */}
        <RoiMatrixModal
          isOpen={isRoiModalOpen}
          onClose={() => setIsRoiModalOpen(false)}
          roiData={curriculumV2Data.roiMap}
        />

        <MasterCheatSheetModal
          isOpen={isCheatSheetModalOpen}
          onClose={() => setIsCheatSheetModalOpen(false)}
          cheatSheetData={curriculumV2Data.cheatSheet}
        />
      </main>
    </div>
  );
};
