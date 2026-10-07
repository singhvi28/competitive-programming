import React from 'react';
import { Link } from 'react-router-dom';
import { Award, Flame, Timer, Sparkles, ArrowRight } from 'lucide-react';

export const HomePage: React.FC = () => {
  return (
    <div className="min-h-screen flex flex-col justify-between">
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-10 sm:pt-14 pb-16 flex-1 flex flex-col justify-center">
        {/* Header Hero */}
        <div className="text-center max-w-3xl mx-auto mb-10">
          <div className="inline-flex items-center space-x-2 px-3.5 py-1 rounded-full bg-indigo-500/10 border border-indigo-500/30 text-indigo-400 text-xs font-mono mb-4">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
            <span>Curated High-Impact Algorithm Portfolios</span>
          </div>
          <h1 className="text-3xl sm:text-5xl font-extrabold tracking-tight text-white mb-4 leading-tight">
            Master Advanced Algorithms &amp; High-Frequency Interviews
          </h1>
          <p className="text-slate-300 text-sm sm:text-base leading-relaxed">
            Choose your training path: master modern Codeforces Candidate Master transition problems (1900–2300), solve the 301 classified LeetCode Hard classics, drill 237 timed virtual rounds, or study 321 problems solved by competitive masters.
          </p>
        </div>

        {/* Four Main Tracks Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5 max-w-7xl mx-auto w-full">
          {/* Track 1: Codeforces Curriculum */}
          <Link
            to="/curriculum"
            className="track-card track-cf rounded-2xl p-5 flex flex-col justify-between group relative overflow-hidden glass-card"
          >
            <div className="absolute -right-12 -bottom-12 w-40 h-40 bg-indigo-500/10 rounded-full blur-2xl group-hover:bg-indigo-500/20 transition duration-500" />

            <div className="relative z-10 space-y-3.5">
              <div className="flex items-center justify-between">
                <div className="w-10 h-10 rounded-xl bg-indigo-500/10 border border-indigo-500/30 flex items-center justify-center text-indigo-400 group-hover:scale-110 transition">
                  <Award className="w-5 h-5" />
                </div>
                <span className="text-[11px] font-mono px-2.5 py-0.5 rounded-full bg-indigo-950 text-indigo-400 border border-indigo-800">
                  144 Problems
                </span>
              </div>

              <div>
                <h2 className="text-lg font-bold text-white group-hover:text-indigo-300 transition">
                  CF Candidate Master Curriculum
                </h2>
                <div className="text-[11px] font-mono text-purple-400 font-semibold mb-1.5">
                  1900–2300 Transition
                </div>
                <p className="text-slate-300 text-xs leading-relaxed">
                  Targeted transition techniques: Euler tour, DSU on tree, HLD, Cartesian tree DP, 2-SAT, min-cost flow, and geometry.
                </p>
              </div>

              <div className="grid grid-cols-2 gap-1.5 text-[10px] font-mono text-slate-400 pt-2 border-t border-slate-800">
                <div>&bull; 8 Modules</div>
                <div>&bull; 6-Wk Plan</div>
                <div>&bull; Cheat Sheet</div>
                <div>&bull; Backup Sync</div>
              </div>
            </div>

            <div className="relative z-10 pt-5 flex items-center justify-between text-indigo-400 text-xs font-semibold group-hover:translate-x-1 transition">
              <span>Launch CF Track</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </div>
          </Link>

          {/* Track 2: LeetCode Hards Guide */}
          <Link
            to="/leetcode-hards"
            className="track-card track-lc rounded-2xl p-5 flex flex-col justify-between group relative overflow-hidden glass-card"
          >
            <div className="absolute -right-12 -bottom-12 w-40 h-40 bg-amber-500/10 rounded-full blur-2xl group-hover:bg-amber-500/20 transition duration-500" />

            <div className="relative z-10 space-y-3.5">
              <div className="flex items-center justify-between">
                <div className="w-10 h-10 rounded-xl bg-amber-500/10 border border-amber-500/30 flex items-center justify-center text-amber-400 group-hover:scale-110 transition">
                  <Flame className="w-5 h-5" />
                </div>
                <span className="text-[11px] font-mono px-2.5 py-0.5 rounded-full bg-amber-950 text-amber-400 border border-amber-800">
                  301 Problems
                </span>
              </div>

              <div>
                <h2 className="text-lg font-bold text-white group-hover:text-amber-300 transition">
                  LeetCode Hards Guide
                </h2>
                <div className="text-[11px] font-mono text-amber-400 font-semibold mb-1.5">
                  3-Tier Interview Signals
                </div>
                <p className="text-slate-300 text-xs leading-relaxed">
                  44 Direct Classics (Google/Meta staples), 128 Niche Concept Lessons, and 129 CP-tier Hard Problems with company tags.
                </p>
              </div>

              <div className="grid grid-cols-2 gap-1.5 text-[10px] font-mono text-slate-400 pt-2 border-t border-slate-800">
                <div>&bull; 3 Signal Tiers</div>
                <div>&bull; Company Tags</div>
                <div>&bull; Concepts</div>
                <div>&bull; Checklists</div>
              </div>
            </div>

            <div className="relative z-10 pt-5 flex items-center justify-between text-amber-400 text-xs font-semibold group-hover:translate-x-1 transition">
              <span>Launch LeetCode</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </div>
          </Link>

          {/* Track 3: Virtual Contests Library */}
          <Link
            to="/virtual-contests"
            className="track-card track-vc rounded-2xl p-5 flex flex-col justify-between group relative overflow-hidden glass-card"
          >
            <div className="absolute -right-12 -bottom-12 w-40 h-40 bg-cyan-500/10 rounded-full blur-2xl group-hover:bg-cyan-500/20 transition duration-500" />

            <div className="relative z-10 space-y-3.5">
              <div className="flex items-center justify-between">
                <div className="w-10 h-10 rounded-xl bg-cyan-500/10 border border-cyan-500/30 flex items-center justify-center text-cyan-400 group-hover:scale-110 transition">
                  <Timer className="w-5 h-5" />
                </div>
                <span className="text-[11px] font-mono px-2.5 py-0.5 rounded-full bg-cyan-950 text-cyan-400 border border-cyan-800">
                  237 Contests
                </span>
              </div>

              <div>
                <h2 className="text-lg font-bold text-white group-hover:text-cyan-300 transition">
                  CF Virtual Contests
                </h2>
                <div className="text-[11px] font-mono text-cyan-400 font-semibold mb-1.5">
                  Timed Simulation Drills
                </div>
                <p className="text-slate-300 text-xs leading-relaxed">
                  237 modern Codeforces rounds: 154 Div 2, 49 Educational, and 34 Global rounds with 1-click virtual links.
                </p>
              </div>

              <div className="grid grid-cols-2 gap-1.5 text-[10px] font-mono text-slate-400 pt-2 border-t border-slate-800">
                <div>&bull; 154 Div. 2</div>
                <div>&bull; 49 Educational</div>
                <div>&bull; 34 Global</div>
                <div>&bull; 1-Click Virtual</div>
              </div>
            </div>

            <div className="relative z-10 pt-5 flex items-center justify-between text-cyan-400 text-xs font-semibold group-hover:translate-x-1 transition">
              <span>Launch Virtuals</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </div>
          </Link>

          {/* Track 4: Master Mirror */}
          <Link
            to="/mirror"
            className="track-card track-mirror rounded-2xl p-5 flex flex-col justify-between group relative overflow-hidden glass-card"
          >
            <div className="absolute -right-12 -bottom-12 w-40 h-40 bg-fuchsia-500/10 rounded-full blur-2xl group-hover:bg-fuchsia-500/20 transition duration-500" />

            <div className="relative z-10 space-y-3.5">
              <div className="flex items-center justify-between">
                <div className="w-10 h-10 rounded-xl bg-fuchsia-500/10 border border-fuchsia-500/30 flex items-center justify-center text-fuchsia-400 group-hover:scale-110 transition">
                  <Sparkles className="w-5 h-5" />
                </div>
                <span className="text-[11px] font-mono px-2.5 py-0.5 rounded-full bg-fuchsia-950 text-fuchsia-400 border border-fuchsia-800">
                  321 Problems
                </span>
              </div>

              <div>
                <h2 className="text-lg font-bold text-white group-hover:text-fuchsia-300 transition">
                  CF Master Mirror
                </h2>
                <div className="text-[11px] font-mono text-fuchsia-400 font-semibold mb-1.5">
                  a.out &amp; Queue Solved
                </div>
                <p className="text-slate-300 text-xs leading-relaxed">
                  321 modern problems (1900–2300, ID &gt; 1300) solved by masters with direct links to AC submissions.
                </p>
              </div>

              <div className="grid grid-cols-2 gap-1.5 text-[10px] font-mono text-slate-400 pt-2 border-t border-slate-800">
                <div>&bull; 21 Both Solved</div>
                <div>&bull; 204 a.out AC</div>
                <div>&bull; 138 Queue AC</div>
                <div>&bull; Live CF Sync</div>
              </div>
            </div>

            <div className="relative z-10 pt-5 flex items-center justify-between text-fuchsia-400 text-xs font-semibold group-hover:translate-x-1 transition">
              <span>Launch Mirror Track</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </div>
          </Link>
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-800/80 py-6 text-center text-xs text-slate-400 font-mono">
        <p>
          Competitive Programming Hub &bull; Built &amp; Deployed by{' '}
          <a
            href="https://github.com/singhvi28"
            target="_blank"
            rel="noopener noreferrer"
            className="text-indigo-400 hover:underline"
          >
            @singhvi28
          </a>
        </p>
      </footer>
    </div>
  );
};
