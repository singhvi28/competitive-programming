import React, { useState } from 'react';
import { 
  CheckCircle2, 
  Circle, 
  ChevronDown, 
  ChevronUp, 
  Copy, 
  Check, 
  Code2, 
  AlertTriangle, 
  Zap, 
  Activity, 
  BookOpen, 
  BrainCircuit,
  Lightbulb,
  Cpu
} from 'lucide-react';
import { CurriculumV2Topic, RoiTier } from '../../types/curriculumV2';
import { MathRenderer } from '../common/MathRenderer';

interface TopicCardProps {
  topic: CurriculumV2Topic;
  isSolved: boolean;
  onToggle: (id: string) => void;
}

export const TopicCard: React.FC<TopicCardProps> = ({ topic, isSolved, onToggle }) => {
  const [isExpanded, setIsExpanded] = useState(false);
  const [activeTab, setActiveTab] = useState<'intuition' | 'code' | 'recognition' | 'bugs' | 'problems'>('intuition');
  const [codeLang, setCodeLang] = useState<'cpp' | 'py'>('cpp');
  const [copied, setCopied] = useState(false);

  const getRoiBadge = (roi: RoiTier | string) => {
    if (roi.includes('S')) {
      return 'bg-emerald-500/15 text-emerald-400 border-emerald-500/30 glow-emerald';
    }
    if (roi.includes('A')) {
      return 'bg-indigo-500/15 text-indigo-400 border-indigo-500/30';
    }
    if (roi.includes('B')) {
      return 'bg-violet-500/15 text-violet-300 border-violet-500/30';
    }
    if (roi.includes('C')) {
      return 'bg-slate-700/40 text-slate-300 border-slate-600/40';
    }
    return 'bg-amber-500/15 text-amber-300 border-amber-500/30';
  };

  const handleCopyCode = () => {
    const code = codeLang === 'cpp' ? topic.templateCpp : topic.templatePython;
    if (!code) return;
    navigator.clipboard.writeText(code);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div
      className={`rounded-xl border transition-all duration-200 overflow-hidden ${
        isSolved
          ? 'bg-emerald-950/20 border-emerald-800/40'
          : isExpanded
          ? 'bg-slate-900/90 border-indigo-500/40 shadow-lg shadow-indigo-500/5'
          : 'bg-slate-900/60 border-slate-800 hover:border-slate-700'
      }`}
    >
      {/* Card Header */}
      <div className="p-4 sm:p-5 flex items-start justify-between gap-3">
        <div className="flex items-start space-x-3.5 flex-1 min-w-0">
          <button
            onClick={() => onToggle(topic.id)}
            className="mt-1 focus:outline-none transition cursor-pointer flex-shrink-0"
            title={isSolved ? 'Mark as to-learn' : 'Mark as mastered'}
          >
            {isSolved ? (
              <CheckCircle2 className="w-5 h-5 text-emerald-400" />
            ) : (
              <Circle className="w-5 h-5 text-slate-500 hover:text-slate-300" />
            )}
          </button>

          <div className="space-y-1.5 flex-1 min-w-0">
            <div className="flex flex-wrap items-center gap-2">
              <span className="font-mono text-xs px-2 py-0.5 rounded bg-slate-800 text-slate-300 border border-slate-700 font-semibold">
                §{topic.sectionId}
              </span>

              <span
                className={`text-[11px] font-mono px-2.5 py-0.5 rounded-full border font-bold ${getRoiBadge(
                  topic.roi
                )}`}
              >
                {topic.roi}
              </span>

              {topic.ratingRange && (
                <span className="text-[11px] font-mono px-2 py-0.5 rounded bg-purple-950/60 text-purple-300 border border-purple-800/60">
                  {topic.ratingRange}
                </span>
              )}

              {topic.frequency && (
                <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-slate-800/80 text-slate-400">
                  {topic.frequency}
                </span>
              )}
            </div>

            <h3 className="text-base sm:text-lg font-bold text-white tracking-tight leading-snug">
              <MathRenderer text={topic.title} />
            </h3>

            {topic.prerequisites && (
              <p className="text-xs text-slate-400 line-clamp-1">
                <span className="text-slate-500 font-medium">Prereqs:</span> {topic.prerequisites}
              </p>
            )}
          </div>
        </div>

        {/* Expand / Collapse Button */}
        <button
          onClick={() => setIsExpanded(!isExpanded)}
          className="p-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 transition cursor-pointer flex-shrink-0 flex items-center space-x-1 text-xs font-mono"
          title={isExpanded ? 'Collapse topic' : 'Expand deep dive'}
        >
          <span className="hidden sm:inline">{isExpanded ? 'Hide' : 'Deep Dive'}</span>
          {isExpanded ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
        </button>
      </div>

      {/* Quick Invariant / Recognition snippet if collapsed */}
      {!isExpanded && topic.recognitionPatterns.length > 0 && (
        <div className="px-5 pb-4 pt-0">
          <div className="flex items-center space-x-2 text-xs text-slate-400 bg-slate-950/40 px-3 py-2 rounded-lg border border-slate-800/60">
            <Lightbulb className="w-3.5 h-3.5 text-amber-400 flex-shrink-0" />
            <span className="truncate">
              <span className="text-slate-300 font-medium">Clue:</span>{' '}
              <MathRenderer text={topic.recognitionPatterns[0]} />
            </span>
          </div>
        </div>
      )}

      {/* Expanded Deep Dive Details */}
      {isExpanded && (
        <div className="border-t border-slate-800 bg-slate-950/70 p-4 sm:p-6 space-y-6">
          {/* Sub-Navigation Tabs */}
          <div className="flex items-center space-x-1 overflow-x-auto pb-2 border-b border-slate-800/80">
            <button
              onClick={() => setActiveTab('intuition')}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium transition cursor-pointer flex items-center space-x-1.5 whitespace-nowrap ${
                activeTab === 'intuition'
                  ? 'bg-indigo-600 text-white font-semibold shadow-sm'
                  : 'text-slate-400 hover:text-white hover:bg-slate-800'
              }`}
            >
              <BrainCircuit className="w-3.5 h-3.5" />
              <span>Core Intuition &amp; Derivations</span>
            </button>

            {(topic.templateCpp || topic.templatePython) && (
              <button
                onClick={() => setActiveTab('code')}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium transition cursor-pointer flex items-center space-x-1.5 whitespace-nowrap ${
                  activeTab === 'code'
                    ? 'bg-indigo-600 text-white font-semibold shadow-sm'
                    : 'text-slate-400 hover:text-white hover:bg-slate-800'
                }`}
              >
                <Code2 className="w-3.5 h-3.5" />
                <span>Contest Templates</span>
              </button>
            )}

            {topic.recognitionPatterns.length > 0 && (
              <button
                onClick={() => setActiveTab('recognition')}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium transition cursor-pointer flex items-center space-x-1.5 whitespace-nowrap ${
                  activeTab === 'recognition'
                    ? 'bg-indigo-600 text-white font-semibold shadow-sm'
                    : 'text-slate-400 hover:text-white hover:bg-slate-800'
                }`}
              >
                <Zap className="w-3.5 h-3.5" />
                <span>Recognition Patterns</span>
              </button>
            )}

            {topic.commonBugs.length > 0 && (
              <button
                onClick={() => setActiveTab('bugs')}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium transition cursor-pointer flex items-center space-x-1.5 whitespace-nowrap ${
                  activeTab === 'bugs'
                    ? 'bg-indigo-600 text-white font-semibold shadow-sm'
                    : 'text-slate-400 hover:text-white hover:bg-slate-800'
                }`}
              >
                <AlertTriangle className="w-3.5 h-3.5" />
                <span>Contest Bug Traps</span>
              </button>
            )}

            {(topic.problemPatterns || topic.recognitionExercises) && (
              <button
                onClick={() => setActiveTab('problems')}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium transition cursor-pointer flex items-center space-x-1.5 whitespace-nowrap ${
                  activeTab === 'problems'
                    ? 'bg-indigo-600 text-white font-semibold shadow-sm'
                    : 'text-slate-400 hover:text-white hover:bg-slate-800'
                }`}
              >
                <BookOpen className="w-3.5 h-3.5" />
                <span>Practice &amp; Invariants</span>
              </button>
            )}
          </div>

          {/* Tab 1: Intuition & Derivations */}
          {activeTab === 'intuition' && (
            <div className="space-y-5">
              {topic.whyItMatters && (
                <div className="space-y-1.5">
                  <h4 className="text-xs font-mono uppercase tracking-wider text-indigo-400 font-semibold flex items-center space-x-1.5">
                    <Activity className="w-3.5 h-3.5" />
                    <span>Contest Payoff &amp; Context</span>
                  </h4>
                  <div className="text-xs sm:text-sm text-slate-300 leading-relaxed bg-slate-900/60 p-3.5 rounded-lg border border-slate-800 whitespace-pre-wrap">
                    <MathRenderer text={topic.whyItMatters} />
                  </div>
                </div>
              )}

              {topic.coreIntuition && (
                <div className="space-y-1.5">
                  <h4 className="text-xs font-mono uppercase tracking-wider text-emerald-400 font-semibold flex items-center space-x-1.5">
                    <BrainCircuit className="w-3.5 h-3.5" />
                    <span>Core Intuition</span>
                  </h4>
                  <div className="text-xs sm:text-sm text-slate-200 leading-relaxed bg-slate-900/80 p-4 rounded-lg border border-slate-800/80 whitespace-pre-wrap">
                    <MathRenderer text={topic.coreIntuition} />
                  </div>
                </div>
              )}

              {topic.derivation && (
                <div className="space-y-1.5">
                  <h4 className="text-xs font-mono uppercase tracking-wider text-purple-400 font-semibold flex items-center space-x-1.5">
                    <Cpu className="w-3.5 h-3.5" />
                    <span>Mathematical Derivation &amp; Recurrences</span>
                  </h4>
                  <div className="text-xs sm:text-sm text-slate-200 leading-relaxed bg-slate-900/90 p-4 rounded-lg border border-purple-500/20 whitespace-pre-wrap overflow-x-auto">
                    <MathRenderer text={topic.derivation} />
                  </div>
                </div>
              )}

              {topic.complexity && (
                <div className="space-y-1.5">
                  <h4 className="text-xs font-mono uppercase tracking-wider text-amber-400 font-semibold">
                    Complexity &amp; Space Bounds
                  </h4>
                  <div className="text-xs font-mono text-slate-300 bg-slate-900 p-3 rounded-lg border border-slate-800 whitespace-pre-wrap">
                    <MathRenderer text={topic.complexity} />
                  </div>
                </div>
              )}
            </div>
          )}

          {/* Tab 2: Contest Templates */}
          {activeTab === 'code' && (
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  {topic.templateCpp && (
                    <button
                      onClick={() => setCodeLang('cpp')}
                      className={`text-xs font-mono px-3 py-1 rounded-md transition cursor-pointer ${
                        codeLang === 'cpp'
                          ? 'bg-indigo-600 text-white font-bold'
                          : 'bg-slate-800 text-slate-400 hover:text-white'
                      }`}
                    >
                      C++17 Template
                    </button>
                  )}
                  {topic.templatePython && (
                    <button
                      onClick={() => setCodeLang('py')}
                      className={`text-xs font-mono px-3 py-1 rounded-md transition cursor-pointer ${
                        codeLang === 'py'
                          ? 'bg-indigo-600 text-white font-bold'
                          : 'bg-slate-800 text-slate-400 hover:text-white'
                      }`}
                    >
                      Python 3.11 Template
                    </button>
                  )}
                </div>

                <button
                  onClick={handleCopyCode}
                  className="flex items-center space-x-1.5 text-xs font-mono px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 transition cursor-pointer"
                >
                  {copied ? (
                    <>
                      <Check className="w-3.5 h-3.5 text-emerald-400" />
                      <span className="text-emerald-400">Copied!</span>
                    </>
                  ) : (
                    <>
                      <Copy className="w-3.5 h-3.5 text-slate-400" />
                      <span>Copy Template</span>
                    </>
                  )}
                </button>
              </div>

              <div className="relative rounded-lg bg-slate-950 border border-slate-800 overflow-hidden">
                <pre className="p-4 text-xs font-mono text-slate-200 overflow-x-auto leading-relaxed max-h-[460px] scrollbar-thin">
                  <code>{codeLang === 'cpp' ? topic.templateCpp : topic.templatePython}</code>
                </pre>
              </div>
            </div>
          )}

          {/* Tab 3: Recognition Patterns */}
          {activeTab === 'recognition' && (
            <div className="space-y-4">
              <h4 className="text-xs font-mono uppercase tracking-wider text-indigo-400 font-semibold flex items-center space-x-1.5">
                <Zap className="w-3.5 h-3.5" />
                <span>Contest Recognition Clues &amp; Trigger Words</span>
              </h4>
              <ul className="space-y-2.5">
                {topic.recognitionPatterns.map((pattern, idx) => (
                  <li
                    key={idx}
                    className="text-xs sm:text-sm text-slate-300 bg-slate-900/70 p-3 rounded-lg border border-slate-800 flex items-start space-x-2.5"
                  >
                    <span className="w-1.5 h-1.5 rounded-full bg-indigo-400 mt-2 flex-shrink-0" />
                    <span>
                      <MathRenderer text={pattern} />
                    </span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Tab 4: Common Bug Traps */}
          {activeTab === 'bugs' && (
            <div className="space-y-4">
              <h4 className="text-xs font-mono uppercase tracking-wider text-rose-400 font-semibold flex items-center space-x-1.5">
                <AlertTriangle className="w-3.5 h-3.5" />
                <span>WA / TLE / RE Traps to Avoid</span>
              </h4>
              <ul className="space-y-2.5">
                {topic.commonBugs.map((bug, idx) => (
                  <li
                    key={idx}
                    className="text-xs sm:text-sm text-rose-200 bg-red-950/20 p-3 rounded-lg border border-red-900/30 flex items-start space-x-2.5"
                  >
                    <span className="w-1.5 h-1.5 rounded-full bg-rose-400 mt-2 flex-shrink-0" />
                    <span>
                      <MathRenderer text={bug} />
                    </span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Tab 5: Practice Problems & Variants */}
          {activeTab === 'problems' && (
            <div className="space-y-5">
              {topic.problemPatterns && (
                <div className="space-y-2">
                  <h4 className="text-xs font-mono uppercase tracking-wider text-teal-400 font-semibold">
                    Problem Archetypes &amp; Variations
                  </h4>
                  <div className="text-xs sm:text-sm text-slate-300 bg-slate-900/70 p-3.5 rounded-lg border border-slate-800 whitespace-pre-wrap leading-relaxed">
                    <MathRenderer text={topic.problemPatterns} />
                  </div>
                </div>
              )}

              {topic.variants && (
                <div className="space-y-2">
                  <h4 className="text-xs font-mono uppercase tracking-wider text-cyan-400 font-semibold">
                    Algorithmic Variants
                  </h4>
                  <div className="text-xs sm:text-sm text-slate-300 bg-slate-900/70 p-3.5 rounded-lg border border-slate-800 whitespace-pre-wrap leading-relaxed">
                    <MathRenderer text={topic.variants} />
                  </div>
                </div>
              )}

              {topic.recognitionExercises && (
                <div className="space-y-2">
                  <h4 className="text-xs font-mono uppercase tracking-wider text-amber-400 font-semibold">
                    Recognition Self-Test Exercises
                  </h4>
                  <div className="text-xs sm:text-sm text-slate-300 bg-slate-900/70 p-3.5 rounded-lg border border-slate-800 whitespace-pre-wrap leading-relaxed">
                    <MathRenderer text={topic.recognitionExercises} />
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
};
