import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { Navbar } from './components/common/Navbar';
import { HomePage } from './pages/HomePage';
import { CurriculumV2Page } from './pages/CurriculumV2Page';
import { CurriculumV2GuidePage } from './pages/CurriculumV2GuidePage';
import { CurriculumPage } from './pages/CurriculumPage';
import { LeetCodeHardsPage } from './pages/LeetCodeHardsPage';
import { VirtualContestsPage } from './pages/VirtualContestsPage';
import { MirrorPage } from './pages/MirrorPage';

export const App: React.FC = () => {
  return (
    <BrowserRouter basename="/competitive-programming">
      <div className="min-h-screen bg-dark-900 text-slate-100 flex flex-col selection:bg-indigo-500 selection:text-white">
        <Navbar />
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/curriculum-v2/guide/:topicId" element={<CurriculumV2GuidePage />} />
          <Route path="/curriculum-v2/guide" element={<CurriculumV2GuidePage />} />
          <Route path="/curriculum-v2" element={<CurriculumV2Page />} />
          <Route path="/curriculum-v2/*" element={<CurriculumV2Page />} />
          <Route path="/curriculum" element={<CurriculumPage />} />
          <Route path="/curriculum/*" element={<CurriculumPage />} />
          <Route path="/leetcode-hards" element={<LeetCodeHardsPage />} />
          <Route path="/leetcode-hards/*" element={<LeetCodeHardsPage />} />
          <Route path="/virtual-contests" element={<VirtualContestsPage />} />
          <Route path="/virtual-contests/*" element={<VirtualContestsPage />} />
          <Route path="/mirror" element={<MirrorPage />} />
          <Route path="/mirror/*" element={<MirrorPage />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
};

export default App;
