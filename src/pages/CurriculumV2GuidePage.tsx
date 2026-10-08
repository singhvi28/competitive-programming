import React, { useState, useMemo } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { 
  CheckCircle2, 
  Circle, 
  ArrowLeft, 
  ArrowRight, 
  Copy, 
  Check, 
  Menu, 
  ExternalLink, 
  BrainCircuit, 
  Code2, 
  Zap, 
  AlertTriangle, 
  Sparkles, 
  Award, 
  ChevronRight,
  Target,
  Flame,
  Globe
} from 'lucide-react';
import curriculumV2DataRaw from '../data/curriculumV2Data.json';
import { CurriculumV2Data, CurriculumV2Topic, RoiTier } from '../types/curriculumV2';
import { useLocalStorageSet } from '../hooks/useLocalStorageSet';
import { useToast } from '../context/ToastContext';
import { GuideSidebar } from '../components/curriculum-v2/GuideSidebar';
import { MathRenderer } from '../components/common/MathRenderer';

const curriculumV2Data = curriculumV2DataRaw as unknown as CurriculumV2Data;

export const CurriculumV2GuidePage: React.FC = () => {
  const { topicId } = useParams<{ topicId?: string }>();
  const navigate = useNavigate();
  const { solvedSet, toggle } = useLocalStorageSet(
    'cf_curriculum_v2_solved',
    'codeforces_masterclass_v2_progress'
  );
  const { showToast } = useToast();

  const [isSidebarOpenMobile, setIsSidebarOpenMobile] = useState(false);
  const [codeLang, setCodeLang] = useState<'cpp' | 'py'>('cpp');
  const [copiedCode, setCopiedCode] = useState(false);
  const [copiedLink, setCopiedLink] = useState(false);

  // Flatten all topics for lookup and prev/next navigation
  const allTopics = useMemo(() => {
    const list: CurriculumV2Topic[] = [];
    curriculumV2Data.modules.forEach((m) => list.push(...m.topics));
    return list;
  }, []);

  // Find active topic or default to first topic
  const activeTopic = useMemo(() => {
    if (!topicId) return allTopics[0];
    const found = allTopics.find((t) => t.id === topicId);
    return found || allTopics[0];
  }, [topicId, allTopics]);

  // Current topic index for Prev / Next
  const currentIndex = useMemo(() => {
    return allTopics.findIndex((t) => t.id === activeTopic.id);
  }, [allTopics, activeTopic]);

  const prevTopic = currentIndex > 0 ? allTopics[currentIndex - 1] : null;
  const nextTopic = currentIndex < allTopics.length - 1 ? allTopics[currentIndex + 1] : null;

  // Active module
  const activeModule = useMemo(() => {
    return curriculumV2Data.modules.find((m) => m.sectionId === activeTopic.sectionId);
  }, [activeTopic]);

  const isSolved = solvedSet.has(activeTopic.id);

  const getRoiBadgeClass = (roi: RoiTier | string) => {
    if (roi.includes('S')) return 'bg-emerald-500/20 text-emerald-400 border-emerald-500/30';
    if (roi.includes('A')) return 'bg-indigo-500/20 text-indigo-400 border-indigo-500/30';
    if (roi.includes('B')) return 'bg-violet-500/20 text-violet-300 border-violet-500/30';
    if (roi.includes('C')) return 'bg-slate-700/40 text-slate-300 border-slate-600/40';
    return 'bg-amber-500/20 text-amber-300 border-amber-500/30';
  };

  const handleCopyCode = () => {
    const code = codeLang === 'cpp' ? activeTopic.templateCpp : activeTopic.templatePython;
    if (!code) return;
    navigator.clipboard.writeText(code);
    setCopiedCode(true);
    showToast('Code template copied to clipboard!', 'copy');
    setTimeout(() => setCopiedCode(false), 2000);
  };

  const handleCopyLink = () => {
    navigator.clipboard.writeText(window.location.href);
    setCopiedLink(true);
    showToast('Guide URL copied to clipboard!', 'success');
    setTimeout(() => setCopiedLink(false), 2000);
  };

  return (
    <div className="min-h-screen flex bg-[#07090e] text-slate-100">
      {/* Navigation Sidebar */}
      <GuideSidebar
        data={curriculumV2Data}
        activeTopicId={activeTopic.id}
        solvedSet={solvedSet}
        isOpenMobile={isSidebarOpenMobile}
        onCloseMobile={() => setIsSidebarOpenMobile(false)}
      />

      {/* Main Guide Content Container */}
      <div className="flex-1 flex flex-col min-w-0">
        {/* Top Control Bar */}
        <div className="sticky top-16 z-30 bg-slate-950/90 backdrop-blur-xl border-b border-slate-800/80 px-4 sm:px-8 py-3 flex items-center justify-between gap-4">
          <div className="flex items-center space-x-3 min-w-0">
            <button
              onClick={() => setIsSidebarOpenMobile(true)}
              className="lg:hidden p-2 rounded-lg bg-slate-800 text-slate-300 hover:text-white"
              title="Open Navigation Sidebar"
            >
              <Menu className="w-4 h-4" />
            </button>

            {/* Breadcrumb Trail */}
            <nav className="flex items-center space-x-1.5 text-xs font-mono text-slate-400 overflow-x-auto whitespace-nowrap">
              <Link to="/curriculum-v2" className="hover:text-emerald-400 transition">
                Curriculum V2
              </Link>
              <ChevronRight className="w-3 h-3 text-slate-600 flex-shrink-0" />
              <span className="text-indigo-400 truncate">
                §{activeTopic.sectionId} {activeModule?.shortTitle}
              </span>
              <ChevronRight className="w-3 h-3 text-slate-600 flex-shrink-0" />
              <span className="text-white font-bold truncate">
                {activeTopic.title}
              </span>
            </nav>
          </div>

          <div className="flex items-center space-x-2 flex-shrink-0">
            {/* Mark Mastered Toggle */}
            <button
              onClick={() => {
                toggle(activeTopic.id);
                showToast(
                  isSolved ? 'Topic unmarked' : 'Topic marked as mastered! 🎉',
                  isSolved ? 'rotate-ccw' : 'check-circle-2'
                );
              }}
              className={`px-3 py-1.5 rounded-lg text-xs font-mono font-medium transition cursor-pointer flex items-center space-x-1.5 border ${
                isSolved
                  ? 'bg-emerald-950/80 text-emerald-400 border-emerald-800/60'
                  : 'bg-slate-900 text-slate-300 border-slate-800 hover:border-slate-700'
              }`}
            >
              {isSolved ? (
                <>
                  <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
                  <span>Mastered</span>
                </>
              ) : (
                <>
                  <Circle className="w-3.5 h-3.5 text-slate-500" />
                  <span>Mark Mastered</span>
                </>
              )}
            </button>

            {/* Share / Copy Link */}
            <button
              onClick={handleCopyLink}
              className="p-1.5 sm:px-2.5 sm:py-1.5 rounded-lg bg-slate-900 hover:bg-slate-800 text-slate-300 border border-slate-800 transition cursor-pointer text-xs font-mono flex items-center space-x-1"
              title="Copy shareable guide link"
            >
              {copiedLink ? (
                <Check className="w-3.5 h-3.5 text-emerald-400" />
              ) : (
                <Copy className="w-3.5 h-3.5" />
              )}
              <span className="hidden sm:inline">Share</span>
            </button>
          </div>
        </div>

        {/* Reader Document Body */}
        <main className="max-w-4xl mx-auto w-full px-4 sm:px-8 py-8 sm:py-12 space-y-10">
          {/* Guide Header Banner */}
          <div className="space-y-4 border-b border-slate-800/80 pb-8">
            <div className="flex flex-wrap items-center gap-2">
              <span className="text-xs font-mono font-bold px-2.5 py-0.5 rounded bg-indigo-950 text-indigo-300 border border-indigo-800">
                §{activeTopic.sectionId} &bull; {activeTopic.sectionTitle}
              </span>

              <span
                className={`text-xs font-mono px-2.5 py-0.5 rounded-full border font-bold ${getRoiBadgeClass(
                  activeTopic.roi
                )}`}
              >
                {activeTopic.roi}
              </span>

              {activeTopic.ratingRange && (
                <span className="text-xs font-mono px-2.5 py-0.5 rounded bg-purple-950/60 text-purple-300 border border-purple-800/60">
                  Rating: {activeTopic.ratingRange}
                </span>
              )}

              {activeTopic.frequency && (
                <span className="text-xs font-mono px-2.5 py-0.5 rounded bg-slate-800 text-slate-300 border border-slate-700">
                  {activeTopic.frequency}
                </span>
              )}
            </div>

            <h1 className="text-2xl sm:text-4xl font-extrabold tracking-tight text-white leading-tight">
              <MathRenderer text={activeTopic.title} />
            </h1>

            {activeTopic.prerequisites && (
              <div className="text-xs sm:text-sm text-slate-400 bg-slate-900/60 px-4 py-2.5 rounded-xl border border-slate-800 flex items-center space-x-2">
                <Target className="w-4 h-4 text-emerald-400 flex-shrink-0" />
                <span>
                  <strong className="text-slate-300">Prerequisites:</strong> {activeTopic.prerequisites}
                </span>
              </div>
            )}
          </div>

          {/* Section 1: Why It Matters & Contest Payoff */}
          {activeTopic.whyItMatters && (
            <section className="space-y-3">
              <div className="flex items-center space-x-2 text-indigo-400">
                <Award className="w-5 h-5" />
                <h2 className="text-lg font-bold text-white tracking-tight uppercase font-mono text-sm">
                  1. Contest Payoff &amp; Why It Matters
                </h2>
              </div>
              <div className="text-sm sm:text-base text-slate-300 leading-relaxed bg-slate-900/50 p-5 rounded-xl border border-slate-800 whitespace-pre-wrap">
                <MathRenderer text={activeTopic.whyItMatters} />
              </div>
            </section>
          )}

          {/* Section 2: Core Intuition & Invariants */}
          {activeTopic.coreIntuition && (
            <section className="space-y-3">
              <div className="flex items-center space-x-2 text-emerald-400">
                <BrainCircuit className="w-5 h-5" />
                <h2 className="text-lg font-bold text-white tracking-tight uppercase font-mono text-sm">
                  2. Core Intuition &amp; Invariants
                </h2>
              </div>
              <div className="text-sm sm:text-base text-slate-200 leading-relaxed bg-slate-900/80 p-5 rounded-xl border border-slate-800/80 whitespace-pre-wrap">
                <MathRenderer text={activeTopic.coreIntuition} />
              </div>
            </section>
          )}

          {/* Section 3: Mathematical Derivations & Recurrences */}
          {activeTopic.derivation && (
            <section className="space-y-3">
              <div className="flex items-center space-x-2 text-purple-400">
                <Sparkles className="w-5 h-5" />
                <h2 className="text-lg font-bold text-white tracking-tight uppercase font-mono text-sm">
                  3. Mathematical Derivations &amp; Formulas
                </h2>
              </div>
              <div className="text-sm sm:text-base text-slate-200 leading-relaxed bg-slate-900/90 p-5 rounded-xl border border-purple-500/20 whitespace-pre-wrap overflow-x-auto">
                <MathRenderer text={activeTopic.derivation} />
              </div>
            </section>
          )}

          {/* Section 4: Contest-Ready Templates */}
          {(activeTopic.templateCpp || activeTopic.templatePython) && (
            <section className="space-y-3">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2 text-cyan-400">
                  <Code2 className="w-5 h-5" />
                  <h2 className="text-lg font-bold text-white tracking-tight uppercase font-mono text-sm">
                    4. Contest-Ready Implementation Templates
                  </h2>
                </div>

                <div className="flex items-center space-x-2">
                  {activeTopic.templateCpp && (
                    <button
                      onClick={() => setCodeLang('cpp')}
                      className={`text-xs font-mono px-3 py-1 rounded-md transition cursor-pointer ${
                        codeLang === 'cpp'
                          ? 'bg-indigo-600 text-white font-bold'
                          : 'bg-slate-800 text-slate-400 hover:text-white'
                      }`}
                    >
                      C++17
                    </button>
                  )}
                  {activeTopic.templatePython && (
                    <button
                      onClick={() => setCodeLang('py')}
                      className={`text-xs font-mono px-3 py-1 rounded-md transition cursor-pointer ${
                        codeLang === 'py'
                          ? 'bg-indigo-600 text-white font-bold'
                          : 'bg-slate-800 text-slate-400 hover:text-white'
                      }`}
                    >
                      Python 3.11
                    </button>
                  )}
                  <button
                    onClick={handleCopyCode}
                    className="flex items-center space-x-1.5 text-xs font-mono px-3 py-1 rounded-md bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 transition cursor-pointer"
                  >
                    {copiedCode ? (
                      <>
                        <Check className="w-3.5 h-3.5 text-emerald-400" />
                        <span className="text-emerald-400">Copied</span>
                      </>
                    ) : (
                      <>
                        <Copy className="w-3.5 h-3.5 text-slate-400" />
                        <span>Copy</span>
                      </>
                    )}
                  </button>
                </div>
              </div>

              <div className="rounded-xl bg-slate-950 border border-slate-800 overflow-hidden shadow-xl">
                <pre className="p-5 text-xs sm:text-sm font-mono text-slate-200 overflow-x-auto leading-relaxed max-h-[550px] scrollbar-thin">
                  <code>{codeLang === 'cpp' ? activeTopic.templateCpp : activeTopic.templatePython}</code>
                </pre>
              </div>

              {activeTopic.complexity && (
                <div className="text-xs font-mono text-slate-400 bg-slate-900/80 p-3 rounded-lg border border-slate-800/80">
                  <span className="text-amber-400 font-semibold uppercase tracking-wider">Complexity:</span>{' '}
                  <MathRenderer text={activeTopic.complexity} />
                </div>
              )}
            </section>
          )}

          {/* Section 5: Recognition Patterns */}
          {activeTopic.recognitionPatterns.length > 0 && (
            <section className="space-y-3">
              <div className="flex items-center space-x-2 text-indigo-400">
                <Zap className="w-5 h-5" />
                <h2 className="text-lg font-bold text-white tracking-tight uppercase font-mono text-sm">
                  5. Recognition Trigger Signals &amp; Heuristics
                </h2>
              </div>
              <ul className="space-y-2.5">
                {activeTopic.recognitionPatterns.map((p, idx) => (
                  <li
                    key={idx}
                    className="text-xs sm:text-sm text-slate-300 bg-slate-900/60 p-3.5 rounded-xl border border-slate-800 flex items-start space-x-3"
                  >
                    <span className="w-2 h-2 rounded-full bg-indigo-400 mt-1.5 flex-shrink-0" />
                    <span>
                      <MathRenderer text={p} />
                    </span>
                  </li>
                ))}
              </ul>
            </section>
          )}

          {/* Section 6: Contest Bug Traps */}
          {activeTopic.commonBugs.length > 0 && (
            <section className="space-y-3">
              <div className="flex items-center space-x-2 text-rose-400">
                <AlertTriangle className="w-5 h-5" />
                <h2 className="text-lg font-bold text-white tracking-tight uppercase font-mono text-sm">
                  6. Contest WA / TLE / RE Traps
                </h2>
              </div>
              <ul className="space-y-2.5">
                {activeTopic.commonBugs.map((bug, idx) => (
                  <li
                    key={idx}
                    className="text-xs sm:text-sm text-rose-200 bg-red-950/20 p-3.5 rounded-xl border border-red-900/30 flex items-start space-x-3"
                  >
                    <span className="w-2 h-2 rounded-full bg-rose-400 mt-1.5 flex-shrink-0" />
                    <span>
                      <MathRenderer text={bug} />
                    </span>
                  </li>
                ))}
              </ul>
            </section>
          )}

          {/* Section 7: Practice Problems Bank (Enriched from CP-Algorithms, CF, USACO) */}
          {activeTopic.curatedProblems && activeTopic.curatedProblems.length > 0 && (
            <section className="space-y-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2 text-emerald-400">
                  <Flame className="w-5 h-5" />
                  <h2 className="text-lg font-bold text-white tracking-tight uppercase font-mono text-sm">
                    7. Curated Practice Problem Bank
                  </h2>
                </div>
                <span className="text-xs font-mono text-slate-400">
                  {activeTopic.curatedProblems.length} High-Yield Drills
                </span>
              </div>

              <div className="grid grid-cols-1 gap-3.5">
                {activeTopic.curatedProblems.map((prob) => (
                  <div
                    key={prob.id}
                    className="bg-slate-900/80 p-4 rounded-xl border border-slate-800 hover:border-emerald-500/40 transition flex flex-col md:flex-row md:items-center justify-between gap-4"
                  >
                    <div className="space-y-1.5 flex-1">
                      <div className="flex flex-wrap items-center gap-2">
                        <span className="text-[11px] font-mono px-2 py-0.5 rounded bg-slate-800 text-slate-300 font-bold">
                          {prob.platform} &bull; {prob.id}
                        </span>
                        <span className="text-[11px] font-mono px-2 py-0.5 rounded bg-purple-950 text-purple-300 font-bold border border-purple-800">
                          {prob.rating}
                        </span>
                        {prob.tags.map((tag) => (
                          <span
                            key={tag}
                            className="text-[10px] font-mono px-1.5 py-0.2 rounded bg-slate-800/80 text-slate-400"
                          >
                            {tag}
                          </span>
                        ))}
                      </div>

                      <h3 className="text-sm font-bold text-white">
                        {prob.name}
                      </h3>

                      <p className="text-xs text-slate-300 leading-relaxed">
                        <strong className="text-emerald-400 font-mono">Insight:</strong> {prob.insight}
                      </p>
                    </div>

                    <a
                      href={prob.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="flex items-center space-x-1.5 px-3.5 py-2 rounded-lg bg-emerald-600/20 hover:bg-emerald-600 text-emerald-300 hover:text-white border border-emerald-500/30 text-xs font-mono font-bold transition flex-shrink-0 self-start md:self-center"
                    >
                      <span>Solve Problem</span>
                      <ExternalLink className="w-3.5 h-3.5" />
                    </a>
                  </div>
                ))}
              </div>
            </section>
          )}

          {/* Section 8: External High-Yield References */}
          {activeTopic.externalLinks && activeTopic.externalLinks.length > 0 && (
            <section className="space-y-3">
              <div className="flex items-center space-x-2 text-teal-400">
                <Globe className="w-5 h-5" />
                <h2 className="text-lg font-bold text-white tracking-tight uppercase font-mono text-sm">
                  8. External Theory &amp; Deep-Dive References
                </h2>
              </div>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                {activeTopic.externalLinks.map((link, idx) => (
                  <a
                    key={idx}
                    href={link.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="p-3.5 rounded-xl bg-slate-900/60 hover:bg-slate-900 border border-slate-800 hover:border-teal-500/40 transition flex items-center justify-between group"
                  >
                    <div className="space-y-0.5 min-w-0 flex-1 pr-2">
                      <span className="text-[10px] font-mono text-teal-400 uppercase font-bold">
                        {link.source}
                      </span>
                      <h3 className="text-xs font-bold text-white truncate group-hover:text-teal-300 transition">
                        {link.title}
                      </h3>
                    </div>
                    <ExternalLink className="w-4 h-4 text-slate-500 group-hover:text-teal-400 flex-shrink-0" />
                  </a>
                ))}
              </div>
            </section>
          )}

          {/* Bottom Prev / Next Navigation */}
          <div className="pt-8 border-t border-slate-800/80 grid grid-cols-1 sm:grid-cols-2 gap-4">
            {prevTopic ? (
              <button
                onClick={() => navigate(`/curriculum-v2/guide/${prevTopic.id}`)}
                className="p-4 rounded-xl bg-slate-900/60 hover:bg-slate-900 border border-slate-800 hover:border-slate-700 transition cursor-pointer text-left space-y-1 group"
              >
                <div className="flex items-center space-x-1 text-xs font-mono text-slate-400">
                  <ArrowLeft className="w-3.5 h-3.5 group-hover:-translate-x-1 transition" />
                  <span>Previous Guide</span>
                </div>
                <div className="text-sm font-bold text-white group-hover:text-emerald-400 transition truncate">
                  §{prevTopic.sectionId} {prevTopic.title}
                </div>
              </button>
            ) : (
              <div />
            )}

            {nextTopic ? (
              <button
                onClick={() => navigate(`/curriculum-v2/guide/${nextTopic.id}`)}
                className="p-4 rounded-xl bg-slate-900/60 hover:bg-slate-900 border border-slate-800 hover:border-slate-700 transition cursor-pointer text-right space-y-1 group"
              >
                <div className="flex items-center justify-end space-x-1 text-xs font-mono text-slate-400">
                  <span>Next Guide</span>
                  <ArrowRight className="w-3.5 h-3.5 group-hover:translate-x-1 transition" />
                </div>
                <div className="text-sm font-bold text-white group-hover:text-emerald-400 transition truncate">
                  §{nextTopic.sectionId} {nextTopic.title}
                </div>
              </button>
            ) : (
              <div />
            )}
          </div>
        </main>
      </div>
    </div>
  );
};
