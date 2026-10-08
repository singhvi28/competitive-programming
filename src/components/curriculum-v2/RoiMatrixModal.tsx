import React, { useState, useMemo } from 'react';
import { X, Search, Filter, Award } from 'lucide-react';
import { RoiMapEntry } from '../../types/curriculumV2';

interface RoiMatrixModalProps {
  isOpen: boolean;
  onClose: () => void;
  roiData: RoiMapEntry[];
}

export const RoiMatrixModal: React.FC<RoiMatrixModalProps> = ({
  isOpen,
  onClose,
  roiData,
}) => {
  const [search, setSearch] = useState('');
  const [selectedTier, setSelectedTier] = useState<string>('all');

  const filtered = useMemo(() => {
    const q = search.toLowerCase().trim();
    return roiData.filter((entry) => {
      const matchTier = selectedTier === 'all' || entry.roi.toLowerCase().includes(selectedTier.toLowerCase());
      const matchSearch =
        !q ||
        entry.topic.toLowerCase().includes(q) ||
        entry.prerequisites.toLowerCase().includes(q) ||
        entry.ratingRange.toLowerCase().includes(q) ||
        entry.frequency.toLowerCase().includes(q);

      return matchTier && matchSearch;
    });
  }, [search, selectedTier, roiData]);

  if (!isOpen) return null;

  const getRoiBadgeClass = (roi: string) => {
    if (roi.includes('S')) return 'bg-emerald-500/20 text-emerald-400 border-emerald-500/30';
    if (roi.includes('A')) return 'bg-indigo-500/20 text-indigo-400 border-indigo-500/30';
    if (roi.includes('B')) return 'bg-violet-500/20 text-violet-400 border-violet-500/30';
    if (roi.includes('C')) return 'bg-slate-700/40 text-slate-300 border-slate-600/40';
    return 'bg-amber-500/20 text-amber-400 border-amber-500/30';
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-6 bg-slate-950/80 backdrop-blur-md">
      <div className="bg-slate-900 border border-slate-800 rounded-2xl w-full max-w-5xl max-h-[90vh] flex flex-col shadow-2xl overflow-hidden">
        {/* Modal Header */}
        <div className="p-4 sm:p-6 border-b border-slate-800 flex items-center justify-between bg-slate-950/60">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 rounded-xl bg-indigo-500/10 border border-indigo-500/30 flex items-center justify-center text-indigo-400">
              <Award className="w-5 h-5" />
            </div>
            <div>
              <h2 className="text-lg sm:text-xl font-bold text-white">
                Contest ROI Matrix &amp; Skill Tiers
              </h2>
              <p className="text-xs text-slate-400">
                159 competitive programming techniques ranked by contest payoff and rating threshold
              </p>
            </div>
          </div>

          <button
            onClick={onClose}
            className="p-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 transition cursor-pointer"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Toolbar */}
        <div className="p-4 border-b border-slate-800 bg-slate-900/90 flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-3">
          <div className="relative flex-1">
            <Search className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Search technique, prerequisites, rating range..."
              className="w-full pl-9 pr-3 py-1.5 text-xs rounded-lg bg-slate-950 border border-slate-800 text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500"
            />
          </div>

          <div className="flex items-center space-x-1.5 overflow-x-auto pb-1 sm:pb-0">
            <Filter className="w-3.5 h-3.5 text-slate-400 mr-1 flex-shrink-0" />
            {(['all', 'S-tier', 'A-tier', 'B-tier', 'C-tier', 'Niche'] as const).map((tier) => (
              <button
                key={tier}
                onClick={() => setSelectedTier(tier)}
                className={`px-2.5 py-1 rounded-md text-xs font-mono transition cursor-pointer whitespace-nowrap ${
                  selectedTier === tier
                    ? 'bg-indigo-600 text-white font-bold'
                    : 'bg-slate-800 text-slate-400 hover:text-white'
                }`}
              >
                {tier === 'all' ? 'All Tiers' : tier}
              </button>
            ))}
          </div>
        </div>

        {/* Table Content */}
        <div className="flex-1 overflow-y-auto p-4 scrollbar-thin">
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs text-slate-300 border-collapse">
              <thead>
                <tr className="border-b border-slate-800 text-slate-400 font-mono uppercase text-[10px]">
                  <th className="py-2.5 px-3">Topic / Technique</th>
                  <th className="py-2.5 px-3">Contest ROI</th>
                  <th className="py-2.5 px-3">Frequency</th>
                  <th className="py-2.5 px-3">Difficulty</th>
                  <th className="py-2.5 px-3">Rating Range</th>
                  <th className="py-2.5 px-3">Prerequisites</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60 font-mono">
                {filtered.map((item, idx) => (
                  <tr key={idx} className="hover:bg-slate-800/40 transition">
                    <td className="py-2.5 px-3 text-white font-bold font-sans text-sm">
                      {item.topic}
                    </td>
                    <td className="py-2.5 px-3">
                      <span
                        className={`inline-block px-2 py-0.5 rounded border text-[11px] font-bold ${getRoiBadgeClass(
                          item.roi
                        )}`}
                      >
                        {item.roi}
                      </span>
                    </td>
                    <td className="py-2.5 px-3 text-slate-300">{item.frequency}</td>
                    <td className="py-2.5 px-3 text-slate-400">{item.difficulty}</td>
                    <td className="py-2.5 px-3 text-indigo-300 font-bold">{item.ratingRange}</td>
                    <td className="py-2.5 px-3 text-slate-400 text-[11px] max-w-xs truncate" title={item.prerequisites}>
                      {item.prerequisites || '—'}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {filtered.length === 0 && (
            <div className="text-center py-12 text-slate-400 text-sm">
              No techniques matched your search criteria.
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="p-3 bg-slate-950/60 border-t border-slate-800 text-right text-xs font-mono text-slate-400">
          Showing <span className="text-indigo-400 font-bold">{filtered.length}</span> / {roiData.length} techniques
        </div>
      </div>
    </div>
  );
};
