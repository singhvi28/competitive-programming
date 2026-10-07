import React, { useState } from 'react';
import { ChevronDown, Flame, Sparkles, Zap, LucideIcon } from 'lucide-react';
import { LeetCodeCategory, LeetCodeProblem } from '../../types/leetcode';
import { LeetCodeCard } from './LeetCodeCard';

interface CategorySectionProps {
  categoryId: number;
  category: LeetCodeCategory;
  filteredProblems: LeetCodeProblem[];
  solvedSet: Set<string>;
  onToggle: (id: string) => void;
}

const catBadgeStyles: Record<number, { badge: string; icon: LucideIcon; color: string }> = {
  1: {
    badge: 'bg-emerald-950/80 text-emerald-400 border-emerald-800/60',
    icon: Flame,
    color: 'from-emerald-500 to-teal-400',
  },
  2: {
    badge: 'bg-amber-950/80 text-amber-400 border-amber-800/60',
    icon: Zap,
    color: 'from-amber-500 to-orange-400',
  },
  3: {
    badge: 'bg-rose-950/80 text-rose-400 border-rose-800/60',
    icon: Sparkles,
    color: 'from-rose-500 to-pink-500',
  },
};

export const CategorySection: React.FC<CategorySectionProps> = ({
  categoryId,
  category,
  filteredProblems,
  solvedSet,
  onToggle,
}) => {
  const [isOpen, setIsOpen] = useState(true);

  if (filteredProblems.length === 0) return null;

  const totalProblems = category.problems.length;
  const solvedCount = category.problems.filter((p) => solvedSet.has(String(p.id))).length;
  const pct = totalProblems > 0 ? Math.round((solvedCount / totalProblems) * 100) : 0;

  const style = catBadgeStyles[categoryId] || catBadgeStyles[1];
  const IconComponent = style.icon;

  return (
    <section className="glass-panel rounded-2xl p-6 border border-slate-800/90 transition">
      <div
        className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-4 border-b border-slate-800/80 cursor-pointer select-none"
        onClick={() => setIsOpen(!isOpen)}
      >
        <div className="flex items-center space-x-3.5">
          <div className="w-10 h-10 rounded-xl bg-amber-500/10 border border-amber-500/30 flex items-center justify-center text-amber-400 flex-shrink-0">
            <IconComponent className="w-5 h-5" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <span className={`text-xs font-mono font-bold px-2 py-0.5 rounded border ${style.badge}`}>
                Category {categoryId}
              </span>
            </div>
            <h2 className="text-lg sm:text-xl font-bold text-white mt-1">{category.title}</h2>
            <p className="text-xs text-slate-400 mt-0.5">{category.description}</p>
          </div>
        </div>

        <div className="flex items-center space-x-4 self-end md:self-auto">
          <div className="flex items-center space-x-3 text-xs font-mono">
            <span className="text-slate-400">
              Solved: <b className="text-emerald-400 font-bold">{solvedCount}</b> / {totalProblems}
            </span>
            <div className="w-24 bg-slate-800 rounded-full h-2 overflow-hidden">
              <div
                className={`bg-gradient-to-r ${style.color} h-2 rounded-full transition-all duration-300`}
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
            <LeetCodeCard
              key={String(problem.id)}
              problem={problem}
              isSolved={solvedSet.has(String(problem.id))}
              onToggle={onToggle}
            />
          ))}
        </div>
      )}
    </section>
  );
};
