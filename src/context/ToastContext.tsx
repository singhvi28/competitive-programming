import React, { createContext, useContext, useState, useCallback, ReactNode } from 'react';
import { 
  Info, 
  CheckCircle2, 
  AlertCircle, 
  Copy, 
  Download, 
  Upload, 
  RotateCcw,
  RefreshCw
} from 'lucide-react';

export type ToastType =
  | 'info'
  | 'success'
  | 'error'
  | 'copy'
  | 'download'
  | 'upload'
  | 'reset'
  | 'rotate-ccw'
  | 'check-circle-2'
  | 'alert-circle'
  | 'sync'
  | 'refresh-cw';

interface ToastState {
  visible: boolean;
  message: string;
  type: ToastType;
}

interface ToastContextType {
  showToast: (message: string, type?: ToastType) => void;
}

const ToastContext = createContext<ToastContextType | undefined>(undefined);

export const ToastProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [toast, setToast] = useState<ToastState>({
    visible: false,
    message: '',
    type: 'info',
  });

  const showToast = useCallback((message: string, type: ToastType = 'info') => {
    setToast({ visible: true, message, type });
    setTimeout(() => {
      setToast((prev) => ({ ...prev, visible: false }));
    }, 3200);
  }, []);

  const getIcon = () => {
    switch (toast.type) {
      case 'success':
      case 'check-circle-2':
        return <CheckCircle2 className="w-4 h-4 text-emerald-400" />;
      case 'error':
      case 'alert-circle':
        return <AlertCircle className="w-4 h-4 text-rose-400" />;
      case 'copy':
        return <Copy className="w-4 h-4 text-cyan-400" />;
      case 'download':
        return <Download className="w-4 h-4 text-indigo-400" />;
      case 'upload':
        return <Upload className="w-4 h-4 text-amber-400" />;
      case 'reset':
      case 'rotate-ccw':
        return <RotateCcw className="w-4 h-4 text-rose-400" />;
      case 'sync':
      case 'refresh-cw':
        return <RefreshCw className="w-4 h-4 text-teal-400" />;
      default:
        return <Info className="w-4 h-4 text-indigo-400" />;
    }
  };

  return (
    <ToastContext.Provider value={{ showToast }}>
      {children}
      <div
        className={`fixed bottom-6 right-6 z-50 transition-all duration-300 pointer-events-none px-4 py-2.5 rounded-xl bg-slate-900 border border-slate-700 text-white text-xs font-mono shadow-2xl flex items-center space-x-2.5 ${
          toast.visible ? 'translate-y-0 opacity-100' : 'translate-y-12 opacity-0'
        }`}
      >
        {getIcon()}
        <span>{toast.message}</span>
      </div>
    </ToastContext.Provider>
  );
};

export const useToast = (): ToastContextType => {
  const context = useContext(ToastContext);
  if (!context) {
    throw new Error('useToast must be used within a ToastProvider');
  }
  return context;
};
