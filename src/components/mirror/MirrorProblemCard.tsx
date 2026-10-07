import React from 'react';
import { ExternalLink, ChevronRight, CheckCheck, Code2 } from 'lucide-react';
import { MirrorRawProblem } from '../../types/mirror';

interface MirrorProblemCardProps {
  problem: MirrorRawProblem;
  isSolved: boolean;
  onToggle: (id: string) => void;
}

export const MirrorProblemCard: React.FC<MirrorProblemCardProps> = ({
  problem,
  isSolved,
  onToggle,
}) => {
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

  const tagList = problem.tags
    ? problem.tags.split(',').map((t) => t.trim()).filter(Boolean)
    : [];

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
              onChange={() => onToggle(problem.problem_id)}
              className="checkbox-custom w-4 h-4 flex-shrink-0 cursor-pointer"
              title="Mark as solved"
            />
            <span className="text-xs font-mono font-bold px-2 py-0.5 rounded bg-slate-800 text-slate-200 border border-slate-700">
              #{problem.problem_id}
            </span>
          </div>
          {getRatingBadge(problem.rating)}
        </div>

        <h3 className="text-sm sm:text-base font-bold text-white leading-snug">
          <a
            href={problem.problem_link}
            target="_blank"
            rel="noopener noreferrer"
            className="hover:text-fuchsia-400 transition flex items-center space-x-1.5"
          >
            <span>{problem.name}</span>
            <ExternalLink className="w-3.5 h-3.5 opacity-60 flex-shrink-0" />
          </a>
        </h3>

        {/* Solver Submissions */}
        <div className="flex flex-wrap items-center gap-1.5 pt-1">
          <span className="text-[11px] font-mono text-slate-400 flex items-center mr-1">
            <CheckCheck className="w-3 h-3 mr-1 text-slate-400" /> Solved by:
          </span>
          {problem.solved_by.map((solver) => {
            const subUrl = problem.submissions?.[solver];
            const isAout = solver === 'a.out';
            const badgeStyle = isAout
              ? 'bg-purple-950/70 text-purple-300 border-purple-800/60 hover:bg-purple-900/80 hover:border-purple-600'
              : 'bg-teal-950/70 text-teal-300 border-teal-800/60 hover:bg-teal-900/80 hover:border-teal-600';

            return subUrl ? (
              <a
                key={solver}
                href={subUrl}
                target="_blank"
                rel="noopener noreferrer"
                className={`inline-flex items-center space-x-1 px-2 py-0.5 rounded text-[11px] font-mono font-semibold border transition ${badgeStyle}`}
                title={`View ${solver}'s AC submission`}
              >
                <Code2 className="w-3 h-3" />
                <span>{solver}</span>
              </a>
            ) : (
              <span
                key={solver}
                className={`inline-flex items-center space-x-1 px-2 py-0.5 rounded text-[11px] font-mono font-semibold border ${badgeStyle}`}
              >
                <span>{solver}</span>
              </span>
            );
          })}
        </div>
      </div>

      <div className="pt-3 border-t border-slate-800/80 flex items-center justify-between gap-2">
        <div className="flex flex-wrap gap-1">
          {tagList.map((tag) => (
            <span
              key={tag}
              className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-slate-900 text-slate-400 border border-slate-800"
            >
              #{tag}
            </span>
          ))}
        </div>
        <a
          href={problem.problem_link}
          target="_blank"
          rel="noopener noreferrer"
          className="px-3 py-1.5 rounded-lg bg-fuchsia-600 hover:bg-fuchsia-500 text-white text-xs font-medium font-mono flex items-center space-x-1 shadow-lg shadow-fuchsia-600/20 transition whitespace-nowrap cursor-pointer"
        >
          <span>Solve</span>
          <ChevronRight className="w-3 h-3" />
        </a>
      </div>
    </div>
  );
};
