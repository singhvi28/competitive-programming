import React from 'react';
import { 
  Compass, 
  Layers, 
  Network, 
  Boxes, 
  Share2, 
  Cpu, 
  Binary, 
  Hash, 
  Zap,
  Target
} from 'lucide-react';
import { CurriculumV2Phase, CurriculumV2Track } from '../../types/curriculumV2';

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

interface PhaseRoadmapProps {
  phases: CurriculumV2Phase[];
  tracks: CurriculumV2Track[];
  selectedPhase: number | 'all';
  onSelectPhase: (phaseId: number | 'all') => void;
  selectedTrack: string | 'all';
  onSelectTrack: (trackId: string | 'all') => void;
  topicCountsByPhase: Record<number, { total: number; solved: number }>;
}

export const PhaseRoadmap: React.FC<PhaseRoadmapProps> = ({
  phases,
  tracks,
  selectedPhase,
  onSelectPhase,
  selectedTrack,
  onSelectTrack,
  topicCountsByPhase,
}) => {
  return (
    <div className="space-y-6 mb-8">
      {/* Study Tracks Selector */}
      <div className="glass-panel p-4 sm:p-5 rounded-xl border border-slate-800">
        <div className="flex items-center space-x-2 mb-3">
          <Target className="w-4 h-4 text-indigo-400" />
          <h3 className="text-sm font-bold text-white uppercase tracking-wider font-mono">
            Targeted Rating Study Tracks
          </h3>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
          {tracks.map((track) => {
            const isSelected = selectedTrack === track.id;
            return (
              <button
                key={track.id}
                onClick={() => onSelectTrack(isSelected ? 'all' : track.id)}
                className={`p-3.5 rounded-xl border text-left transition cursor-pointer flex flex-col justify-between space-y-2 ${
                  isSelected
                    ? 'bg-indigo-950/80 border-indigo-500 ring-1 ring-indigo-500 shadow-md shadow-indigo-500/10'
                    : 'bg-slate-900/60 border-slate-800 hover:border-slate-700 hover:bg-slate-900/90'
                }`}
              >
                <div className="flex items-center justify-between">
                  <span className="text-[11px] font-mono font-bold px-2 py-0.5 rounded bg-slate-800 text-slate-300 border border-slate-700">
                    {track.ratingRange}
                  </span>
                  <span className="text-[10px] font-mono text-indigo-400 font-semibold">
                    {track.badge}
                  </span>
                </div>

                <div>
                  <h4 className="text-xs sm:text-sm font-bold text-white">{track.name}</h4>
                  <p className="text-[11px] text-slate-300 line-clamp-2 mt-1 leading-snug">
                    {track.description}
                  </p>
                </div>

                <div className="text-[10px] font-mono text-slate-400 pt-1 border-t border-slate-800/80">
                  Sections: {track.sections.map((s) => `§${s}`).join(', ')}
                </div>
              </button>
            );
          })}
        </div>
      </div>

      {/* 8 Pedagogical Phases Grid */}
      <div className="space-y-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <Zap className="w-4 h-4 text-emerald-400" />
            <h3 className="text-sm font-bold text-white uppercase tracking-wider font-mono">
              8 Pedagogical Learning Phases
            </h3>
          </div>

          <button
            onClick={() => onSelectPhase('all')}
            className={`text-xs font-mono px-3 py-1 rounded-md transition cursor-pointer ${
              selectedPhase === 'all'
                ? 'bg-indigo-600 text-white font-bold'
                : 'bg-slate-800 text-slate-400 hover:text-white'
            }`}
          >
            Show All Phases
          </button>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
          {phases.map((phase) => {
            const Icon = PHASE_ICONS[phase.id] || Layers;
            const isSelected = selectedPhase === phase.id;
            const stats = topicCountsByPhase[phase.id] || { total: 0, solved: 0 };
            const pct = stats.total > 0 ? Math.round((stats.solved / stats.total) * 100) : 0;

            return (
              <button
                key={phase.id}
                onClick={() => onSelectPhase(isSelected ? 'all' : phase.id)}
                className={`p-3.5 rounded-xl border text-left transition cursor-pointer flex flex-col justify-between space-y-2.5 ${
                  isSelected
                    ? 'bg-indigo-950/80 border-indigo-500 ring-1 ring-indigo-500 shadow-md shadow-indigo-500/10'
                    : 'bg-slate-900/60 border-slate-800 hover:border-slate-700 hover:bg-slate-900/90'
                }`}
              >
                <div className="flex items-center justify-between">
                  <div className="w-7 h-7 rounded-lg bg-indigo-500/10 border border-indigo-500/20 flex items-center justify-center text-indigo-400">
                    <Icon className="w-4 h-4" />
                  </div>
                  <span className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-slate-800 text-indigo-300 font-bold border border-slate-700">
                    Phase {phase.number}
                  </span>
                </div>

                <div>
                  <h4 className="text-xs font-bold text-white line-clamp-1">{phase.shortName}</h4>
                  <p className="text-[10px] text-slate-300 line-clamp-2 mt-1 leading-snug">
                    {phase.description}
                  </p>
                </div>

                <div className="space-y-1.5 pt-1 border-t border-slate-800/80">
                  <div className="flex items-center justify-between text-[10px] font-mono text-slate-400">
                    <span>{phase.sections.map((s) => `§${s}`).join(', ')}</span>
                    <span className="text-slate-300">
                      {stats.solved}/{stats.total} ({pct}%)
                    </span>
                  </div>
                  <div className="w-full bg-slate-800 rounded-full h-1 overflow-hidden">
                    <div
                      className="bg-emerald-400 h-1 rounded-full transition-all duration-300"
                      style={{ width: `${pct}%` }}
                    />
                  </div>
                </div>
              </button>
            );
          })}
        </div>
      </div>
    </div>
  );
};
