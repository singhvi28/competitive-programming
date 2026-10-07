import React, { useState } from 'react';
import { 
  ChevronDown, 
  GitBranch, 
  Layers, 
  Shuffle, 
  Cpu, 
  Network, 
  Share2, 
  Shapes, 
  Binary,
  Code
} from 'lucide-react';
import { CurriculumModule, CurriculumProblem } from '../../types/curriculum';
import { ProblemCard } from './ProblemCard';

interface ModuleSectionProps {
  module: CurriculumModule;
  filteredProblems: CurriculumProblem[];
  solvedSet: Set<string>;
  onToggle: (id: string) => void;
}

const iconMap: Record<string, React.FC<{ className?: string }>> = {
  tree: GitBranch,
  stack: Layers,
  hash: Shuffle,
  cpu: Cpu,
  graph: Network,
  flow: Share2,
  geometry: Shapes,
  binary: Binary,
};

export const ModuleSection: React.FC<ModuleSectionProps> = ({
  module,
  filteredProblems,
  solvedSet,
  onToggle,
}) => {
  const [isOpen, setIsOpen] = useState(true);

  const totalProblems = module.problems.length;
  const solvedCount = module.problems.filter((p) => solvedSet.has(p.id)).length;
  const pct = totalProblems > 0 ? Math.round((solvedCount / totalProblems) * 100) : 0;

  const IconComponent = iconMap[module.icon] || Code;

  if (filteredProblems.length === 0) {
    return null;
  }

  return (
    <section className="glass-panel rounded-2xl p-6 border border-slate-800/90 transition">
      <div
        className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-4 border-b border-slate-800/80 cursor-pointer select-none"
        onClick={() => setIsOpen(!isOpen)}
      >
        <div className="flex items-center space-x-3.5">
          <div className="w-10 h-10 rounded-xl bg-indigo-500/10 border border-indigo-500/30 flex items-center justify-center text-indigo-400 flex-shrink-0">
            <IconComponent className="w-5 h-5" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <span className="text-xs font-mono text-indigo-400 font-bold uppercase">
                Module {module.id}
              </span>
            </div>
            <h2 className="text-lg sm:text-xl font-bold text-white">{module.title}</h2>
            <p className="text-xs text-slate-400 mt-0.5">{module.description}</p>
          </div>
        </div>

        <div className="flex items-center space-x-4 self-end md:self-auto">
          <div className="flex items-center space-x-3 text-xs font-mono">
            <span className="text-slate-400">
              Solved:{' '}
              <b className="text-emerald-400 font-bold">{solvedCount}</b> / {totalProblems}
            </span>
            <div className="w-24 bg-slate-800 rounded-full h-2 overflow-hidden">
              <div
                className="bg-gradient-to-r from-indigo-500 to-emerald-400 h-2 rounded-full transition-all duration-300"
                style={{ width: `${pct}%` }}
              />
            </div>
          </div>
          <button className="p-1 rounded-lg hover:bg-slate-800 text-slate-400 transition">
            <ChevronDown
              className={`w-4 h-4 transition-transform duration-200 ${
                isOpen ? 'rotate-180' : ''
              }`}
            />
          </button>
        </div>
      </div>

      {isOpen && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mt-6">
          {filteredProblems.map((problem) => (
            <ProblemCard
              key={problem.id}
              problem={problem}
              isSolved={solvedSet.has(problem.id)}
              onToggle={onToggle}
            />
          ))}
        </div>
      )}
    </section>
  );
};
