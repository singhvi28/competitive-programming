import React, { useState, useMemo } from 'react';
import { X, Search, Sparkles, BookOpen, ChevronDown, ChevronUp } from 'lucide-react';
import { CheatSheetSection } from '../../types/curriculumV2';
import { MathRenderer } from '../common/MathRenderer';

interface MasterCheatSheetModalProps {
  isOpen: boolean;
  onClose: () => void;
  cheatSheetData: CheatSheetSection[];
}

export const MasterCheatSheetModal: React.FC<MasterCheatSheetModalProps> = ({
  isOpen,
  onClose,
  cheatSheetData,
}) => {
  const [search, setSearch] = useState('');
  const [expandedSections, setExpandedSections] = useState<Record<string, boolean>>({});

  const toggleSection = (title: string) => {
    setExpandedSections((prev) => ({
      ...prev,
      [title]: prev[title] === undefined ? false : !prev[title],
    }));
  };

  const filteredData = useMemo(() => {
    const q = search.toLowerCase().trim();
    if (!q) return cheatSheetData;

    return cheatSheetData
      .map((sec) => {
        const filteredSubs = sec.subtopics.filter(
          (sub) =>
            sub.topic.toLowerCase().includes(q) ||
            sub.recognitionClue.toLowerCase().includes(q) ||
            sub.coreIdea.toLowerCase().includes(q) ||
            sub.complexity.toLowerCase().includes(q) ||
            sub.mainTemplate.toLowerCase().includes(q) ||
            sub.commonUseCase.toLowerCase().includes(q)
        );
        return {
          ...sec,
          subtopics: filteredSubs,
        };
      })
      .filter((sec) => sec.subtopics.length > 0);
  }, [search, cheatSheetData]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-6 bg-slate-950/80 backdrop-blur-md">
      <div className="bg-slate-900 border border-slate-800 rounded-2xl w-full max-w-5xl max-h-[90vh] flex flex-col shadow-2xl overflow-hidden">
        {/* Modal Header */}
        <div className="p-4 sm:p-6 border-b border-slate-800 flex items-center justify-between bg-slate-950/60">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 rounded-xl bg-purple-500/10 border border-purple-500/30 flex items-center justify-center text-purple-400">
              <Sparkles className="w-5 h-5" />
            </div>
            <div>
              <h2 className="text-lg sm:text-xl font-bold text-white">
                Pre-Contest Master Cheat Sheet
              </h2>
              <p className="text-xs text-slate-400">
                Rapid recognition clues, complexity guarantees, and template hooks across all 22 modules
              </p>
            </div>
          </div>

          <button
            onClick={onClose}
            className="p-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 transition cursor-pointer"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Search Toolbar */}
        <div className="p-4 border-b border-slate-800 bg-slate-900/90 flex items-center">
          <div className="relative flex-1">
            <Search className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Search recognition clues (e.g. Pick's, Sprague-Grundy, Dinic, CHT, 2-SAT, Suffix Automaton)..."
              className="w-full pl-9 pr-3 py-1.5 text-xs rounded-lg bg-slate-950 border border-slate-800 text-white placeholder-slate-500 focus:outline-none focus:border-purple-500"
            />
          </div>
        </div>

        {/* Content Body */}
        <div className="flex-1 overflow-y-auto p-4 sm:p-6 space-y-6 scrollbar-thin">
          {filteredData.map((sec) => {
            const isCollapsed = expandedSections[sec.sectionTitle] === false;
            return (
              <div
                key={sec.sectionTitle}
                className="bg-slate-950/60 border border-slate-800 rounded-xl overflow-hidden"
              >
                <div
                  onClick={() => toggleSection(sec.sectionTitle)}
                  className="p-3.5 bg-slate-900/80 border-b border-slate-800/80 flex items-center justify-between cursor-pointer hover:bg-slate-800/60 transition"
                >
                  <div className="flex items-center space-x-2">
                    <BookOpen className="w-4 h-4 text-purple-400" />
                    <h3 className="text-sm font-bold text-white font-mono">
                      {sec.sectionTitle}
                    </h3>
                    <span className="text-[10px] font-mono px-2 py-0.2 rounded bg-slate-800 text-slate-400">
                      {sec.subtopics.length} items
                    </span>
                  </div>

                  <button className="text-slate-400 hover:text-white">
                    {isCollapsed ? <ChevronDown className="w-4 h-4" /> : <ChevronUp className="w-4 h-4" />}
                  </button>
                </div>

                {!isCollapsed && (
                  <div className="p-4 grid grid-cols-1 md:grid-cols-2 gap-3.5">
                    {sec.subtopics.map((sub, idx) => (
                      <div
                        key={idx}
                        className="bg-slate-900/70 p-3.5 rounded-lg border border-slate-800/80 space-y-2 hover:border-slate-700 transition flex flex-col justify-between"
                      >
                        <div>
                          <h4 className="text-xs font-bold text-white font-sans flex items-center justify-between">
                            <span>
                              <MathRenderer text={sub.topic} />
                            </span>
                          </h4>

                          {sub.recognitionClue && (
                            <div className="text-[11px] text-slate-300 mt-1 leading-snug">
                              <span className="text-purple-400 font-mono font-semibold">Clue:</span>{' '}
                              <MathRenderer text={sub.recognitionClue} />
                            </div>
                          )}

                          {sub.coreIdea && (
                            <div className="text-[11px] text-slate-400 mt-1 leading-snug">
                              <span className="text-emerald-400 font-mono font-semibold">Idea:</span>{' '}
                              <MathRenderer text={sub.coreIdea} />
                            </div>
                          )}
                        </div>

                        <div className="pt-2 border-t border-slate-800/80 space-y-1 text-[10px] font-mono">
                          {sub.complexity && (
                            <div className="text-amber-300">
                              <span className="text-slate-500">Complexity:</span>{' '}
                              <MathRenderer text={sub.complexity} />
                            </div>
                          )}
                          {sub.mainTemplate && (
                            <div className="text-cyan-300 truncate" title={sub.mainTemplate}>
                              <span className="text-slate-500">Template:</span> {sub.mainTemplate}
                            </div>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            );
          })}

          {filteredData.length === 0 && (
            <div className="text-center py-12 text-slate-400 text-sm">
              No cheat sheet items matched your search query.
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
