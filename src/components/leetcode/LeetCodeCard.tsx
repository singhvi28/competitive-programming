import React from 'react';
import { ExternalLink, ChevronRight, Building2 } from 'lucide-react';
import { LeetCodeProblem } from '../../types/leetcode';
import { MathRenderer } from '../common/MathRenderer';

interface LeetCodeCardProps {
  problem: LeetCodeProblem;
  isSolved: boolean;
  onToggle: (id: string) => void;
}

export const LeetCodeCard: React.FC<LeetCodeCardProps> = ({ problem, isSolved, onToggle }) => {
  const pid = String(problem.id);

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
              onChange={() => onToggle(pid)}
              className="checkbox-custom w-4 h-4 flex-shrink-0 cursor-pointer"
              title="Mark as solved"
            />
            <a
              href={problem.url}
              target="_blank"
              rel="noopener noreferrer"
              className="text-sm sm:text-base font-bold text-white hover:text-amber-400 transition flex items-center space-x-1.5"
            >
              <span>{problem.name}</span>
              <ExternalLink className="w-3.5 h-3.5 opacity-70 flex-shrink-0" />
            </a>
          </div>
          <span className="text-[11px] font-mono px-2 py-0.5 rounded bg-slate-800 text-slate-300 border border-slate-700 whitespace-nowrap">
            #{problem.id}
          </span>
        </div>

        {problem.why && (
          <p className="text-xs text-slate-300 leading-relaxed bg-slate-900/60 p-2.5 rounded-lg border border-slate-800/80">
            <MathRenderer text={problem.why} />
          </p>
        )}

        {problem.companies && problem.companies.length > 0 && (
          <div className="flex flex-wrap gap-1.5 pt-1">
            {problem.companies.map((c) => (
              <span
                key={c}
                className="inline-flex items-center space-x-1 px-2 py-0.5 rounded text-[10px] font-mono bg-amber-950/40 text-amber-300 border border-amber-800/40"
              >
                <Building2 className="w-2.5 h-2.5" />
                <span>{c}</span>
              </span>
            ))}
          </div>
        )}
      </div>

      <div className="pt-2.5 border-t border-slate-800/60 flex items-center justify-between text-[11px] font-mono text-slate-400">
        <span className="text-slate-400 font-medium">LeetCode Hard</span>
        <a
          href={problem.url}
          target="_blank"
          rel="noopener noreferrer"
          className="px-3 py-1.5 rounded-lg bg-amber-600 hover:bg-amber-500 text-black text-xs font-semibold font-mono flex items-center space-x-1 shadow-lg shadow-amber-600/20 transition whitespace-nowrap cursor-pointer"
        >
          <span>Solve</span>
          <ChevronRight className="w-3.5 h-3.5" />
        </a>
      </div>
    </div>
  );
};
