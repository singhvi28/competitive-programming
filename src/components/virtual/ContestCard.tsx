import React from 'react';
import { ExternalLink, Play, FileText, Trophy } from 'lucide-react';
import { VirtualContest } from '../../types/virtualContests';

interface ContestCardProps {
  contest: VirtualContest;
  isPracticed: boolean;
  onToggle: (id: string) => void;
}

export const ContestCard: React.FC<ContestCardProps> = ({
  contest,
  isPracticed,
  onToggle,
}) => {
  const getTypeBadge = (type: string) => {
    const styles: Record<string, string> = {
      'Div. 2': 'bg-cyan-950/80 text-cyan-300 border-cyan-800/60',
      'Educational': 'bg-emerald-950/80 text-emerald-300 border-emerald-800/60',
      'Combined / Global': 'bg-purple-950/80 text-purple-300 border-purple-800/60',
    };
    const style = styles[type] || 'bg-slate-800 text-slate-300 border-slate-700';
    return (
      <span className={`px-2 py-0.5 rounded text-[11px] font-mono font-semibold border ${style}`}>
        {type}
      </span>
    );
  };

  return (
    <div
      className={`problem-card glass-card rounded-xl p-4 flex flex-col justify-between space-y-3 transition ${
        isPracticed ? 'solved-card' : ''
      }`}
    >
      <div className="space-y-2">
        <div className="flex items-start justify-between gap-2">
          <div className="flex items-center space-x-2.5">
            <input
              type="checkbox"
              checked={isPracticed}
              onChange={() => onToggle(contest.id)}
              className="checkbox-custom w-4 h-4 flex-shrink-0 cursor-pointer"
              title="Mark contest as practiced"
            />
            <span className="text-xs font-mono font-bold px-2 py-0.5 rounded bg-slate-800 text-slate-200 border border-slate-700">
              #{contest.id}
            </span>
          </div>
          {getTypeBadge(contest.type)}
        </div>

        <h3 className="text-sm font-bold text-white leading-snug">
          <a
            href={contest.url}
            target="_blank"
            rel="noopener noreferrer"
            className="hover:text-cyan-400 transition flex items-center space-x-1.5"
          >
            <span>{contest.name}</span>
            <ExternalLink className="w-3 h-3 opacity-60 flex-shrink-0" />
          </a>
        </h3>
      </div>

      <div className="pt-3 border-t border-slate-800/80 flex items-center justify-between gap-2 text-xs font-mono">
        <a
          href={`https://codeforces.com/contest/${contest.id}/virtual`}
          target="_blank"
          rel="noopener noreferrer"
          className="flex-1 text-center py-1.5 px-2 rounded-lg bg-cyan-600 hover:bg-cyan-500 text-black font-semibold text-xs transition shadow-lg shadow-cyan-600/20 flex items-center justify-center space-x-1 cursor-pointer"
        >
          <Play className="w-3 h-3" />
          <span>Virtual</span>
        </a>
        <a
          href={`https://codeforces.com/contest/${contest.id}/problems`}
          target="_blank"
          rel="noopener noreferrer"
          className="py-1.5 px-2.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 transition"
          title="View Problems"
        >
          <FileText className="w-3.5 h-3.5" />
        </a>
        <a
          href={`https://codeforces.com/contest/${contest.id}/standings`}
          target="_blank"
          rel="noopener noreferrer"
          className="py-1.5 px-2.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 transition"
          title="View Standings"
        >
          <Trophy className="w-3.5 h-3.5" />
        </a>
      </div>
    </div>
  );
};
