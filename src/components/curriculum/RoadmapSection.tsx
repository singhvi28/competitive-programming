import React, { useState } from 'react';
import { CalendarDays, ChevronDown, CheckCircle2 } from 'lucide-react';
import { CurriculumScheduleItem } from '../../types/curriculum';

interface RoadmapSectionProps {
  schedule: CurriculumScheduleItem[];
  solvedSet: Set<string>;
}

export const RoadmapSection: React.FC<RoadmapSectionProps> = ({ schedule, solvedSet }) => {
  const [isOpen, setIsOpen] = useState(false);

  if (!schedule || schedule.length === 0) return null;

  return (
    <section id="roadmap-section" className="mb-10">
      <div className="glass-panel rounded-2xl p-6 border border-slate-800">
        <div
          className="flex items-center justify-between cursor-pointer select-none"
          onClick={() => setIsOpen(!isOpen)}
        >
          <div className="flex items-center space-x-3">
            <div className="w-8 h-8 rounded-lg bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center text-emerald-400 flex-shrink-0">
              <CalendarDays className="w-4 h-4" />
            </div>
            <div>
              <h2 className="text-lg font-bold text-white">
                Recommended 6-Week Candidate Master Transition Sequence
              </h2>
              <p className="text-xs text-slate-400">
                Structured weekly drill path across all 8 transition modules
              </p>
            </div>
          </div>
          <ChevronDown
            className={`w-5 h-5 text-slate-400 transition-transform duration-200 ${
              isOpen ? 'rotate-180' : ''
            }`}
          />
        </div>

        {isOpen && (
          <div className="mt-6 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {schedule.map((item, idx) => {
              const total = item.problems.length;
              const solved = item.problems.filter((pid) => solvedSet.has(pid)).length;
              const pct = total > 0 ? Math.round((solved / total) * 100) : 0;
              const isAllDone = solved === total && total > 0;

              return (
                <div
                  key={idx}
                  className={`bg-slate-900/80 p-4 rounded-xl border ${
                    isAllDone ? 'border-emerald-500/40 bg-emerald-950/10' : 'border-slate-800'
                  } space-y-3 flex flex-col justify-between`}
                >
                  <div className="space-y-1.5">
                    <div className="flex items-center justify-between">
                      <span className="text-xs font-mono font-bold text-emerald-400 uppercase tracking-wider">
                        {item.week}
                      </span>
                      <span className="text-xs font-mono text-slate-400">
                        {solved} / {total}
                      </span>
                    </div>
                    <h3 className="text-sm font-bold text-white">{item.title}</h3>
                    <p className="text-xs text-slate-400 leading-relaxed">{item.summary}</p>
                  </div>

                  <div className="space-y-2 pt-2 border-t border-slate-800/80">
                    <div className="w-full bg-slate-800 rounded-full h-1.5 overflow-hidden">
                      <div
                        className={`h-1.5 rounded-full transition-all duration-300 ${
                          isAllDone
                            ? 'bg-emerald-400'
                            : 'bg-gradient-to-r from-emerald-500 to-indigo-400'
                        }`}
                        style={{ width: `${pct}%` }}
                      />
                    </div>
                    <div className="flex items-center justify-between text-[11px] font-mono text-slate-400">
                      <span>{pct}% complete</span>
                      {isAllDone && (
                        <span className="text-emerald-400 flex items-center space-x-1">
                          <CheckCircle2 className="w-3 h-3" />
                          <span>Finished</span>
                        </span>
                      )}
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </section>
  );
};
