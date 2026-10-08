import React, { useState } from 'react';
import { 
  Layers, 
  GitBranch, 
  Split, 
  Boxes, 
  Database, 
  Network, 
  Share2, 
  Route, 
  Activity, 
  Cpu, 
  Binary, 
  Hash, 
  Grid, 
  Table, 
  Sigma, 
  Gamepad2, 
  Compass, 
  Shuffle, 
  Zap, 
  TrendingUp, 
  Award, 
  Sliders,
  ChevronDown,
  ChevronUp,
  BookOpen
} from 'lucide-react';
import { CurriculumV2Module, CurriculumV2Topic } from '../../types/curriculumV2';
import { TopicCard } from './TopicCard';

const ICON_MAP: Record<string, React.ElementType> = {
  Layers,
  GitBranch,
  Split,
  Boxes,
  Database,
  Network,
  Share2,
  Route,
  Activity,
  Cpu,
  Binary,
  Hash,
  Grid,
  Table,
  Sigma,
  Gamepad2,
  Compass,
  Shuffle,
  Zap,
  TrendingUp,
  Award,
  Sliders,
  BookOpen,
};

interface ModuleSectionProps {
  module: CurriculumV2Module;
  filteredTopics: CurriculumV2Topic[];
  solvedSet: Set<string>;
  onToggle: (id: string) => void;
}

export const ModuleSection: React.FC<ModuleSectionProps> = ({
  module,
  filteredTopics,
  solvedSet,
  onToggle,
}) => {
  const [isOpen, setIsOpen] = useState(true);

  const Icon = ICON_MAP[module.icon] || BookOpen;

  const totalTopics = module.topics.length;
  const solvedCount = module.topics.filter((t) => solvedSet.has(t.id)).length;
  const pct = totalTopics > 0 ? Math.round((solvedCount / totalTopics) * 100) : 0;

  if (filteredTopics.length === 0) {
    return null;
  }

  return (
    <div
      id={`section-${module.sectionId}`}
      className="rounded-2xl glass-panel border border-slate-800 overflow-hidden transition duration-300 scroll-mt-24"
    >
      {/* Module Header */}
      <div className="p-5 sm:p-6 bg-slate-900/80 border-b border-slate-800/80 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div className="flex items-start space-x-4 flex-1">
          <div className="w-11 h-11 rounded-xl bg-indigo-500/10 border border-indigo-500/30 flex items-center justify-center text-indigo-400 flex-shrink-0 mt-0.5 shadow-sm">
            <Icon className="w-5 h-5" />
          </div>

          <div className="space-y-1">
            <div className="flex flex-wrap items-center gap-2">
              <span className="font-mono text-xs px-2.5 py-0.5 rounded bg-indigo-950 text-indigo-300 border border-indigo-800 font-bold">
                §{module.sectionId}
              </span>
              <span className="font-mono text-[11px] px-2 py-0.5 rounded bg-slate-800 text-slate-300 border border-slate-700">
                {module.phaseName}
              </span>
              <span className="text-xs font-mono text-slate-400">
                {module.topicsCount} Topics
              </span>
            </div>

            <h2 className="text-xl sm:text-2xl font-extrabold text-white tracking-tight">
              {module.title}
            </h2>

            <p className="text-xs sm:text-sm text-slate-300 max-w-3xl leading-relaxed">
              {module.summary}
            </p>
          </div>
        </div>

        {/* Progress and Toggle */}
        <div className="flex items-center space-x-4 self-end md:self-center">
          <div className="flex flex-col items-end space-y-1">
            <div className="text-xs font-mono text-slate-300">
              <span className="text-emerald-400 font-bold">{solvedCount}</span> / {totalTopics} Mastered ({pct}%)
            </div>
            <div className="w-28 bg-slate-800 rounded-full h-1.5 overflow-hidden">
              <div
                className="bg-emerald-400 h-1.5 rounded-full transition-all duration-300"
                style={{ width: `${pct}%` }}
              />
            </div>
          </div>

          <button
            onClick={() => setIsOpen(!isOpen)}
            className="p-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 transition cursor-pointer"
            title={isOpen ? 'Collapse Section' : 'Expand Section'}
          >
            {isOpen ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
          </button>
        </div>
      </div>

      {/* Topics List */}
      {isOpen && (
        <div className="p-4 sm:p-6 space-y-3.5 bg-slate-950/40">
          {filteredTopics.map((topic) => (
            <TopicCard
              key={topic.id}
              topic={topic}
              isSolved={solvedSet.has(topic.id)}
              onToggle={onToggle}
            />
          ))}
        </div>
      )}
    </div>
  );
};
