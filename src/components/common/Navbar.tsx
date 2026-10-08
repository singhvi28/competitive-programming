import { NavLink } from 'react-router-dom';
import { Award, Flame, Timer, Sparkles, Github, Terminal, CheckCircle2 } from 'lucide-react';

interface NavbarProps {
  progress?: {
    solved: number;
    total: number;
  };
}

export const Navbar: React.FC<NavbarProps> = ({ progress }) => {

  const navItems = [
    {
      to: '/',
      label: 'Home',
      icon: null,
      activeColor: 'text-white bg-slate-800 border-slate-700',
      hoverColor: 'hover:text-white hover:bg-slate-800',
    },
    {
      to: '/curriculum-v2',
      label: 'Curriculum V2',
      icon: Sparkles,
      activeColor: 'text-emerald-400 bg-emerald-950/60 border-emerald-800/60',
      hoverColor: 'hover:text-emerald-400 hover:bg-slate-800',
    },
    {
      to: '/curriculum',
      label: 'CF Candidate Master',
      icon: Award,
      activeColor: 'text-indigo-400 bg-indigo-950/60 border-indigo-800/60',
      hoverColor: 'hover:text-indigo-400 hover:bg-slate-800',
    },
    {
      to: '/leetcode-hards',
      label: 'LeetCode Hards',
      icon: Flame,
      activeColor: 'text-amber-400 bg-amber-950/60 border-amber-800/60',
      hoverColor: 'hover:text-amber-400 hover:bg-slate-800',
    },
    {
      to: '/virtual-contests',
      label: 'Virtuals',
      icon: Timer,
      activeColor: 'text-cyan-400 bg-cyan-950/60 border-cyan-800/60',
      hoverColor: 'hover:text-cyan-400 hover:bg-slate-800',
    },
    {
      to: '/mirror',
      label: 'Mirror',
      icon: Sparkles,
      activeColor: 'text-fuchsia-400 bg-fuchsia-950/60 border-fuchsia-800/60',
      hoverColor: 'hover:text-fuchsia-400 hover:bg-slate-800',
    },
  ];

  return (
    <header className="sticky top-0 z-40 backdrop-blur-xl bg-slate-950/80 border-b border-slate-800/80">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        {/* Logo */}
        <div className="flex items-center space-x-3">
          <NavLink to="/" className="flex items-center space-x-2.5 group">
            <div className="w-8 h-8 rounded-lg bg-gradient-to-tr from-indigo-600 via-purple-600 to-emerald-500 p-0.5 flex items-center justify-center shadow-lg shadow-indigo-500/20 group-hover:shadow-indigo-500/40 transition">
              <div className="w-full h-full bg-slate-950 rounded-[7px] flex items-center justify-center">
                <Terminal className="w-4 h-4 text-white group-hover:text-indigo-400 transition" />
              </div>
            </div>
            <div className="flex flex-col">
              <span className="font-bold text-sm tracking-tight text-white flex items-center space-x-1">
                <span>CP Mastery Hub</span>
                <span className="text-[10px] font-mono px-1.5 py-0.2 rounded bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
                  Portal
                </span>
              </span>
              <span className="text-[10px] font-mono text-slate-400">Competitive Programming</span>
            </div>
          </NavLink>
        </div>

        {/* Navigation Links */}
        <div className="flex items-center space-x-1.5 sm:space-x-2 overflow-x-auto py-1">
          {navItems.map((item) => {
            const Icon = item.icon;
            return (
              <NavLink
                key={item.to}
                to={item.to}
                end={item.to === '/'}
                className={({ isActive }) =>
                  `text-xs font-medium px-2.5 sm:px-3 py-1.5 rounded-lg transition flex items-center space-x-1.5 whitespace-nowrap border ${
                    isActive
                      ? `${item.activeColor} border font-bold`
                      : `text-slate-400 border-transparent ${item.hoverColor}`
                  }`
                }
              >
                {Icon && <Icon className="w-3.5 h-3.5" />}
                <span>{item.label}</span>
              </NavLink>
            );
          })}

          {progress && progress.total > 0 && (
            <div className="hidden xl:flex items-center space-x-2 px-3 py-1.5 rounded-full bg-slate-900 border border-slate-800">
              <CheckCircle2 className="w-4 h-4 text-emerald-400" />
              <span className="text-xs font-mono font-medium text-slate-300">
                {progress.solved} / {progress.total} (
                {Math.round((progress.solved / progress.total) * 100)}%)
              </span>
            </div>
          )}

          <a
            href="https://github.com/singhvi28/competitive-programming"
            target="_blank"
            rel="noopener noreferrer"
            className="p-2 text-slate-400 hover:text-white hover:bg-slate-800 rounded-lg transition ml-1"
            title="View on GitHub"
          >
            <Github className="w-4 h-4" />
          </a>
        </div>
      </div>
    </header>
  );
};
