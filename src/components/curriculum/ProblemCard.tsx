import React from 'react';
import { ExternalLink, ChevronRight } from 'lucide-react';
import { CurriculumProblem } from '../../types/curriculum';
import { MathRenderer } from '../common/MathRenderer';

interface ProblemCardProps {
  problem: CurriculumProblem;
  isSolved: boolean;
  onToggle: (id: string) => void;
}

export const ProblemCard: React.FC<ProblemCardProps> = ({ problem, isSolved, onToggle }) => {
  const getRatingBadge = (rating: number) => {
    const styles: Record<number, string> = {
      1900: 'bg-purple-950/80 text-purple-300 border-purple-800/60',
      2000: 'bg-orange-950/80 text-orange-300 border-orange-800/60',
      2100: 'bg-amber-950/80 text-amber-300 border-amber-800/60',
      2200: 'bg-rose-950/80 text-rose-300 border-rose-800/60',
      2300: 'bg-red-950/80 text-red-300 border-red-800/60',
    };
    const style = styles[rating] || 'bg-slate-800 text-slate-300 border-slate-700';
    return (
      <span className={`px-2 py-0.5 rounded text-xs font-mono font-bold border ${style}`}>
        {rating}
      </span>
    );
  };

  return (
    <div
      className={`problem-card glass-card rounded-xl p-4 flex flex-col justify-between space-y-3 transition ${
        isSolved ? 'solved-card' : ''
      }`}
    >
      <div className="space-y-2">
        <div className="flex items-start justify-between gap-2">
          <div className="flex items-center space-x-2.5">
            <input
              type="checkbox"
              checked={isSolved}
              onChange={() => onToggle(problem.id)}
              className="checkbox-custom w-4 h-4 flex-shrink-0 cursor-pointer"
              title="Mark as solved"
            />
            <a
              href={problem.url}
              target="_blank"
              rel="noopener noreferrer"
              className="text-sm sm:text-base font-bold text-white hover:text-indigo-400 transition flex items-center space-x-1.5"
            >
              <span>{problem.name}</span>
              <ExternalLink className="w-3.5 h-3.5 opacity-70 flex-shrink-0" />
            </a>
          </div>
          {getRatingBadge(problem.rating)}
        </div>

        <div className="inline-block px-2 py-0.5 rounded text-[11px] font-mono bg-indigo-950/40 text-indigo-300 border border-indigo-900/50">
          🎯 <MathRenderer text={problem.technique} />
        </div>

        <p className="text-xs text-slate-300 leading-relaxed">
          <MathRenderer text={problem.insight} />
        </p>
      </div>

      <div className="pt-3 border-t border-slate-800/80 flex items-center justify-between gap-2">
        <div className="flex flex-wrap gap-1">
          {problem.tags.map((t) => (
            <span
              key={t}
              className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-slate-900 text-slate-400 border border-slate-800"
            >
              #{t}
            </span>
          ))}
        </div>
        <a
          href={problem.url}
          target="_blank"
          rel="noopener noreferrer"
          className="px-3 py-1.5 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-medium font-mono flex items-center space-x-1 shadow-lg shadow-indigo-600/20 transition whitespace-nowrap"
        >
          <span>Solve</span>
          <ChevronRight className="w-3 h-3" />
        </a>
      </div>
    </div>
  );
};
