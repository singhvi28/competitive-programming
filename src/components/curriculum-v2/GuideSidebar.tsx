import React, { useState, useMemo } from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import { 
  Search, 
  ChevronDown, 
  ChevronRight, 
  CheckCircle2, 
  Circle, 
  BookOpen, 
  Sparkles,
  Layers,
  Network,
  Boxes,
  Share2,
  Cpu,
  Binary,
  Hash,
  Compass,
  ArrowLeft,
  X
} from 'lucide-react';
import { CurriculumV2Data } from '../../types/curriculumV2';

const PHASE_ICONS: Record<number, React.ElementType> = {
  1: Layers,
  2: Network,
  3: Boxes,
  4: Share2,
  5: Cpu,
  6: Binary,
  7: Hash,
  8: Compass,
};

interface GuideSidebarProps {
  data: CurriculumV2Data;
  activeTopicId: string;
  solvedSet: Set<string>;
  isOpenMobile: boolean;
  onCloseMobile: () => void;
}

export const GuideSidebar: React.FC<GuideSidebarProps> = ({
  data,
  activeTopicId,
  solvedSet,
  isOpenMobile,
  onCloseMobile,
}) => {
  const navigate = useNavigate();
  const [search, setSearch] = useState('');
  const [expandedModules, setExpandedModules] = useState<Record<string, boolean>>(() => {
    // Expand the module of the active topic initially
    const initial: Record<string, boolean> = {};
    for (const m of data.modules) {
      if (m.topics.some((t) => t.id === activeTopicId)) {
        initial[m.id] = true;
      }
    }
    return initial;
  });

  const toggleModule = (moduleId: string) => {
    setExpandedModules((prev) => ({
      ...prev,
      [moduleId]: !prev[moduleId],
    }));
  };

  // Filter modules and topics by search
  const filteredModules = useMemo(() => {
    const q = search.toLowerCase().trim();
    if (!q) return data.modules;

    return data.modules
      .map((m) => {
        const matchingTopics = m.topics.filter(
          (t) =>
            t.title.toLowerCase().includes(q) ||
            t.id.toLowerCase().includes(q) ||
            t.ratingRange.toLowerCase().includes(q) ||
            t.roi.toLowerCase().includes(q)
        );
        return {
          ...m,
          topics: matchingTopics,
        };
      })
      .filter((m) => m.topics.length > 0 || m.title.toLowerCase().includes(q));
  }, [search, data.modules]);

  const totalTopics = data.metadata.totalTopics;
  const totalSolved = solvedSet.size;
  const pct = totalTopics > 0 ? Math.round((totalSolved / totalTopics) * 100) : 0;

  const content = (
    <div className="flex flex-col h-full bg-slate-950 border-r border-slate-800 text-slate-200">
      {/* Sidebar Header */}
      <div className="p-4 border-b border-slate-800/90 space-y-3">
        <div className="flex items-center justify-between">
          <button
            onClick={() => navigate('/curriculum-v2')}
            className="flex items-center space-x-2 text-xs font-mono text-slate-400 hover:text-emerald-400 transition cursor-pointer"
          >
            <ArrowLeft className="w-3.5 h-3.5" />
            <span>Curriculum V2 Hub</span>
          </button>
          
          <button
            onClick={onCloseMobile}
            className="lg:hidden p-1.5 rounded-lg bg-slate-800 text-slate-400 hover:text-white"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        <div className="flex items-center space-x-2.5">
          <div className="w-8 h-8 rounded-lg bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-center text-emerald-400 font-bold font-mono text-xs">
            V2
          </div>
          <div>
            <h2 className="text-sm font-bold text-white tracking-tight">
              Masterclass Guides
            </h2>
            <div className="text-[11px] font-mono text-emerald-400">
              {totalSolved} / {totalTopics} Mastered ({pct}%)
            </div>
          </div>
        </div>

        {/* Quick Search */}
        <div className="relative">
          <Search className="w-3.5 h-3.5 text-slate-500 absolute left-2.5 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search all 496 guides..."
            className="w-full pl-8 pr-2.5 py-1.5 text-xs rounded-lg bg-slate-900 border border-slate-800 text-white placeholder-slate-500 focus:outline-none focus:border-emerald-500 font-mono"
          />
        </div>
      </div>

      {/* Module & Topic Tree */}
      <div className="flex-1 overflow-y-auto p-3 space-y-2 scrollbar-thin">
        {filteredModules.map((module) => {
          const isExpanded = search ? true : expandedModules[module.id] ?? false;
          const PhaseIcon = PHASE_ICONS[module.phaseId] || BookOpen;
          const moduleSolved = module.topics.filter((t) => solvedSet.has(t.id)).length;
          const hasActive = module.topics.some((t) => t.id === activeTopicId);

          return (
            <div
              key={module.id}
              className={`rounded-xl border transition-all ${
                hasActive
                  ? 'bg-slate-900/90 border-indigo-500/30 shadow-sm'
                  : 'bg-slate-900/40 border-slate-800/80 hover:border-slate-700'
              }`}
            >
              {/* Module Title Accordion Header */}
              <button
                onClick={() => toggleModule(module.id)}
                className="w-full p-2.5 flex items-center justify-between text-left transition cursor-pointer group"
              >
                <div className="flex items-center space-x-2 min-w-0 flex-1">
                  <div className="w-5 h-5 rounded-md bg-indigo-500/10 text-indigo-400 flex items-center justify-center flex-shrink-0 text-xs">
                    <PhaseIcon className="w-3 h-3" />
                  </div>

                  <div className="min-w-0 flex-1">
                    <div className="flex items-center space-x-1.5">
                      <span className="text-[10px] font-mono text-indigo-400 font-bold">
                        §{module.sectionId}
                      </span>
                      <h3 className="text-xs font-bold text-white truncate group-hover:text-emerald-300 transition">
                        {module.shortTitle}
                      </h3>
                    </div>
                  </div>
                </div>

                <div className="flex items-center space-x-1.5 flex-shrink-0 ml-2">
                  <span className="text-[10px] font-mono text-slate-400">
                    {moduleSolved}/{module.topics.length}
                  </span>
                  {isExpanded ? (
                    <ChevronDown className="w-3.5 h-3.5 text-slate-400" />
                  ) : (
                    <ChevronRight className="w-3.5 h-3.5 text-slate-400" />
                  )}
                </div>
              </button>

              {/* Topics List inside Module */}
              {isExpanded && (
                <div className="px-2 pb-2 pt-0.5 space-y-0.5 border-t border-slate-800/60">
                  {module.topics.map((topic) => {
                    const isActive = topic.id === activeTopicId;
                    const isSolved = solvedSet.has(topic.id);

                    return (
                      <NavLink
                        key={topic.id}
                        to={`/curriculum-v2/guide/${topic.id}`}
                        onClick={onCloseMobile}
                        className={`group px-2.5 py-1.5 rounded-lg text-xs flex items-center justify-between transition ${
                          isActive
                            ? 'bg-emerald-600 text-white font-bold shadow-sm'
                            : 'text-slate-300 hover:bg-slate-800/80 hover:text-white'
                        }`}
                      >
                        <div className="flex items-center space-x-2 min-w-0 flex-1">
                          {isSolved ? (
                            <CheckCircle2
                              className={`w-3.5 h-3.5 flex-shrink-0 ${
                                isActive ? 'text-white' : 'text-emerald-400'
                              }`}
                            />
                          ) : (
                            <Circle
                              className={`w-3.5 h-3.5 flex-shrink-0 ${
                                isActive ? 'text-white/60' : 'text-slate-600 group-hover:text-slate-400'
                              }`}
                            />
                          )}

                          <span className="truncate">{topic.title}</span>
                        </div>

                        <span
                          className={`text-[9px] font-mono ml-1.5 px-1.5 py-0.2 rounded flex-shrink-0 ${
                            isActive
                              ? 'bg-emerald-700 text-white'
                              : topic.roi.includes('S')
                              ? 'bg-emerald-500/10 text-emerald-400'
                              : topic.roi.includes('A')
                              ? 'bg-indigo-500/10 text-indigo-400'
                              : 'bg-slate-800 text-slate-400'
                          }`}
                        >
                          {topic.roi}
                        </span>
                      </NavLink>
                    );
                  })}
                </div>
              )}
            </div>
          );
        })}

        {filteredModules.length === 0 && (
          <div className="p-6 text-center text-xs text-slate-500 font-mono">
            No guides match &ldquo;{search}&rdquo;
          </div>
        )}
      </div>

      {/* Sidebar Footer */}
      <div className="p-3 border-t border-slate-800/80 bg-slate-950/90 text-center text-[11px] font-mono text-slate-400 flex items-center justify-between">
        <span className="flex items-center space-x-1">
          <Sparkles className="w-3.5 h-3.5 text-indigo-400" />
          <span>22 Master Modules</span>
        </span>
        <span className="text-emerald-400 font-bold">{data.metadata.totalTopics} Guides</span>
      </div>
    </div>
  );

  return (
    <>
      {/* Desktop Persistent Sidebar */}
      <aside className="hidden lg:block w-80 flex-shrink-0 h-[calc(100vh-4rem)] sticky top-16 overflow-hidden">
        {content}
      </aside>

      {/* Mobile Drawer */}
      {isOpenMobile && (
        <div className="lg:hidden fixed inset-0 z-50 flex">
          <div
            className="fixed inset-0 bg-slate-950/80 backdrop-blur-sm"
            onClick={onCloseMobile}
          />
          <div className="relative w-80 max-w-[85vw] h-full z-10 shadow-2xl">
            {content}
          </div>
        </div>
      )}
    </>
  );
};
