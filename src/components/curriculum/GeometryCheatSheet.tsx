import React, { useState } from 'react';
import { Compass, ChevronDown, Repeat, Maximize2, Grid, Disc } from 'lucide-react';
import { MathRenderer } from '../common/MathRenderer';

export const GeometryCheatSheet: React.FC = () => {
  const [isOpen, setIsOpen] = useState(true);

  return (
    <section id="geometry-section" className="mb-10">
      <div className="glass-panel rounded-2xl p-6 border border-indigo-500/20">
        <div
          className="flex items-center justify-between cursor-pointer select-none"
          onClick={() => setIsOpen(!isOpen)}
        >
          <div className="flex items-center space-x-3">
            <div className="w-8 h-8 rounded-lg bg-indigo-500/10 border border-indigo-500/20 flex items-center justify-center text-indigo-400 flex-shrink-0">
              <Compass className="w-4 h-4" />
            </div>
            <div>
              <h2 className="text-lg font-bold text-white">Competitive Geometry Reference (1900–2300)</h2>
              <p className="text-xs text-slate-400">
                Essential mathematical primitives, coordinate rotations, and lattice theorems
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
          <div className="mt-6 grid grid-cols-1 md:grid-cols-2 gap-4 text-xs font-sans">
            {/* Card 1 */}
            <div className="bg-slate-900/80 p-4 rounded-xl border border-slate-800">
              <div className="flex items-center space-x-2 text-indigo-400 font-bold mb-2">
                <Repeat className="w-3.5 h-3.5" />
                <span>1. Manhattan ↔ Chebyshev Transformation</span>
              </div>
              <p className="text-slate-300 leading-relaxed mb-2">
                <MathRenderer text="Transform coordinates via $(x, y) \to (x+y, x-y)$." />
              </p>
              <div className="p-2 rounded bg-slate-950/80 font-mono text-[11px] text-slate-300 border border-slate-800/80 overflow-x-auto">
                <MathRenderer text="$$|x_1 - x_2| + |y_1 - y_2| = \max(|X_1 - X_2|, |Y_1 - Y_2|)$$" />
              </div>
              <p className="text-slate-400 mt-2 leading-relaxed">
                <MathRenderer text="Converts diamond $L_1$ metrics into axis-aligned squares, enabling 1D/2D Segment Trees & Sparse Tables." />
              </p>
            </div>

            {/* Card 2 */}
            <div className="bg-slate-900/80 p-4 rounded-xl border border-slate-800">
              <div className="flex items-center space-x-2 text-purple-400 font-bold mb-2">
                <Maximize2 className="w-3.5 h-3.5" />
                <span>2. 2D Vector Cross Product & Orientation</span>
              </div>
              <p className="text-slate-300 leading-relaxed mb-2">
                <MathRenderer text="For vectors $\vec{u}=(x_1, y_1)$ and $\vec{v}=(x_2, y_2)$:" />
              </p>
              <div className="p-2 rounded bg-slate-950/80 font-mono text-[11px] text-slate-300 border border-slate-800/80 overflow-x-auto">
                <MathRenderer text="$$\vec{u} \times \vec{v} = x_1 y_2 - x_2 y_1 = 2 \times \text{Area}(\triangle)$$" />
              </div>
              <p className="text-slate-400 mt-2 leading-relaxed">
                <MathRenderer text="$> 0$: Counter-Clockwise (Left Turn); $< 0$: Clockwise (Right Turn); $= 0$: Collinear." />
              </p>
            </div>

            {/* Card 3 */}
            <div className="bg-slate-900/80 p-4 rounded-xl border border-slate-800">
              <div className="flex items-center space-x-2 text-emerald-400 font-bold mb-2">
                <Grid className="w-3.5 h-3.5" />
                <span>3. Pick's Theorem on Lattice Polygons</span>
              </div>
              <p className="text-slate-300 leading-relaxed mb-2">
                <MathRenderer text="Relates polygon area, strictly interior points ($I$), and boundary points ($B$):" />
              </p>
              <div className="p-2 rounded bg-slate-950/80 font-mono text-[11px] text-slate-300 border border-slate-800/80 overflow-x-auto">
                <MathRenderer text="$$\text{Area} = I + \frac{B}{2} - 1, \quad B = \sum_{i} \gcd(|\Delta x_i|, |\Delta y_i|)$$" />
              </div>
              <p className="text-slate-400 mt-2 leading-relaxed">
                <MathRenderer text="Allows evaluating parity invariants $\pmod 2$ in $O(1)$ by grouping coordinate residues." />
              </p>
            </div>

            {/* Card 4 */}
            <div className="bg-slate-900/80 p-4 rounded-xl border border-slate-800">
              <div className="flex items-center space-x-2 text-amber-400 font-bold mb-2">
                <Disc className="w-3.5 h-3.5" />
                <span>4. Angular Sweep Line on Circles</span>
              </div>
              <p className="text-slate-300 leading-relaxed mb-2">
                <MathRenderer text="Binary search on radius $R$. Each point within $2R$ defines a valid polar angle interval on circle $C(0, R)$." />
              </p>
              <div className="p-2 rounded bg-slate-950/80 font-mono text-[11px] text-slate-300 border border-slate-800/80 overflow-x-auto">
                <MathRenderer text="$$\alpha = \text{atan2}(y_i, x_i), \quad \Delta = \arccos(d_i / 2R)$$" />
              </div>
              <p className="text-slate-400 mt-2 leading-relaxed">
                <MathRenderer text="Split wrap-around intervals at $2\pi$ and find maximum interval overlap using a sweep line." />
              </p>
            </div>
          </div>
        )}
      </div>
    </section>
  );
};
