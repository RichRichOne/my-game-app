import React, { useState, useMemo, useEffect, useCallback, useRef } from 'react';
import { 
  BarChart3Icon, DownloadIcon, Settings2Icon, SearchIcon, ChevronRightIcon,
  ActivityIcon, Edit2Icon, CheckIcon, HistoryIcon, RotateCcwIcon, ClockIcon,
  XIcon, FileUpIcon, FileTextIcon, FileSpreadsheetIcon, ChevronDownIcon, Loader2Icon
} from 'lucide-react';
import * as XLSX from 'xlsx';
import html2canvas from 'html2canvas';
import { jsPDF } from 'jspdf';
import { INITIAL_PROJECTS } from './data';
import { ProjectData, MetricType } from './types';
import { StatCard } from './components/StatCard';
import { ComparisonCharts } from './components/ComparisonCharts';
import { ProjectTable } from './components/ProjectTable';

interface HistoryEntry {
  id: string;
  projects: ProjectData[];
  dashboardTitle: string;
  tableTitle: string;
  janHeader: string;
  decHeader: string;
  timestamp: Date;
  actionLabel: string;
}

const MAX_HISTORY = 10;

const App: React.FC = () => {
  const [projects, setProjects] = useState<ProjectData[]>(INITIAL_PROJECTS);
  const [selectedMetric, setSelectedMetric] = useState<MetricType>('revenue');
  const [editingId, setEditingId] = useState<number | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  
  const [isExporting, setIsExporting] = useState(false);
  const [exportMenuOpen, setExportMenuOpen] = useState(false);
  const dashboardRef = useRef<HTMLDivElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const [dashboardTitle, setDashboardTitle] = useState('游戏项目核心数据看板');
  const [isEditingDashboardTitle, setIsEditingDashboardTitle] = useState(false);
  const [tempDashboardTitle, setTempDashboardTitle] = useState(dashboardTitle);

  const [tableTitle, setTableTitle] = useState('全项目明细对比 (1月 vs 12月)');
  const [janHeader, setJanHeader] = useState('1月基准数据');
  const [decHeader, setDecHeader] = useState('12月对比数据');

  const [history, setHistory] = useState<HistoryEntry[]>([]);
  const [isHistoryOpen, setIsHistoryOpen] = useState(false);

  const pushToHistory = useCallback((label: string, customProjects?: ProjectData[]) => {
    const newEntry: HistoryEntry = {
      id: Math.random().toString(36).substr(2, 9),
      projects: JSON.parse(JSON.stringify(customProjects || projects)),
      dashboardTitle,
      tableTitle,
      janHeader,
      decHeader,
      timestamp: new Date(),
      actionLabel: label,
    };
    setHistory(prev => [newEntry, ...prev].slice(0, MAX_HISTORY + 1));
  }, [projects, dashboardTitle, tableTitle, janHeader, decHeader]);

  const undo = useCallback(() => {
    if (history.length > 1) {
      const prev = history[1];
      setProjects(prev.projects);
      setDashboardTitle(prev.dashboardTitle);
      setTableTitle(prev.tableTitle);
      setJanHeader(prev.janHeader);
      setDecHeader(prev.decHeader);
      setHistory(prev => prev.slice(1));
    }
  }, [history]);

  useEffect(() => {
    if (history.length === 0) pushToHistory('初始版本');
  }, []);

  const handleExportExcel = () => {
    setIsExporting(true);
    const data = projects.map(p => ({
      '项目ID': p.id,
      '项目名称': p.name,
      '1月-新增': p.jan.newUsers, '1月-DAU': p.jan.dau, '1月-充值': p.jan.revenue,
      '12月-新增': p.dec.newUsers, '12月-DAU': p.dec.dau, '12月-充值': p.dec.revenue,
    }));
    const ws = XLSX.utils.json_to_sheet(data);
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, "核心数据对比");
    XLSX.writeFile(wb, `${dashboardTitle}.xlsx`);
    setIsExporting(false);
    setExportMenuOpen(false);
  };

  const handleExportPDF = async () => {
    if (!dashboardRef.current) return;
    setIsExporting(true);
    setExportMenuOpen(false);
    try {
      const canvas = await html2canvas(dashboardRef.current, { scale: 2 });
      const imgData = canvas.toDataURL('image/png');
      const pdf = new jsPDF('p', 'mm', 'a4');
      const pdfWidth = pdf.internal.pageSize.getWidth();
      const pdfHeight = (canvas.height * pdfWidth) / canvas.width;
      pdf.addImage(imgData, 'PNG', 0, 0, pdfWidth, pdfHeight);
      pdf.save(`${dashboardTitle}.pdf`);
    } finally {
      setIsExporting(false);
    }
  };

  const handleImportExcel = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = (evt) => {
      const bstr = evt.target?.result;
      const wb = XLSX.read(bstr, { type: 'binary' });
      const ws = wb.Sheets[wb.SheetNames[0]];
      const data: any[] = XLSX.utils.sheet_to_json(ws);
      const imported: ProjectData[] = data.map((item, idx) => ({
        id: item['项目ID'] || idx + 1,
        name: item['项目名称'] || `项目 ${idx + 1}`,
        jan: { newUsers: +item['1月-新增'] || 0, dau: +item['1月-DAU'] || 0, revenue: +item['1月-充值'] || 0 },
        dec: { newUsers: +item['12月-新增'] || 0, dau: +item['12月-DAU'] || 0, revenue: +item['12月-充值'] || 0 }
      }));
      setProjects(imported);
      pushToHistory(`导入 Excel 数据`, imported);
    };
    reader.readAsBinaryString(file);
  };

  const totals = useMemo(() => ({
    jan: {
      newUsers: projects.reduce((a, p) => a + p.jan.newUsers, 0),
      dau: projects.reduce((a, p) => a + p.jan.dau, 0),
      revenue: projects.reduce((a, p) => a + p.jan.revenue, 0),
    },
    dec: {
      newUsers: projects.reduce((a, p) => a + p.dec.newUsers, 0),
      dau: projects.reduce((a, p) => a + p.dec.dau, 0),
      revenue: projects.reduce((a, p) => a + p.dec.revenue, 0),
    }
  }), [projects]);

  const filtered = projects.filter(p => p.name.includes(searchTerm) || p.id.toString().includes(searchTerm));

  return (
    <div className="min-h-screen pb-20 relative bg-slate-50" ref={dashboardRef}>
      {isExporting && (
        <div className="fixed inset-0 z-[100] bg-white/60 backdrop-blur-sm flex flex-col items-center justify-center">
          <Loader2Icon className="animate-spin text-blue-600 mb-4" size={48} />
          <p className="text-slate-800 font-bold">正在生成报告...</p>
        </div>
      )}

      <header className="bg-white border-b border-slate-200 sticky top-0 z-10 shadow-sm px-6 h-20 flex items-center justify-between no-print">
        <div className="flex items-center space-x-3">
          <div className="bg-blue-600 p-2 rounded-lg text-white"><BarChart3Icon size={24} /></div>
          <div>
            <h1 className="text-xl font-bold text-slate-800">{dashboardTitle}</h1>
            <p className="text-xs text-slate-500 font-medium">1月 vs 12月 核心数据追踪</p>
          </div>
        </div>

        <div className="flex items-center space-x-4">
          <button onClick={undo} disabled={history.length <= 1} className="p-2 text-slate-500 hover:text-blue-600 transition-colors disabled:opacity-30"><RotateCcwIcon size={20}/></button>
          <button onClick={() => setIsHistoryOpen(true)} className="p-2 text-slate-500 hover:text-blue-600"><HistoryIcon size={20}/></button>
          <input type="file" ref={fileInputRef} onChange={handleImportExcel} className="hidden" />
          <button onClick={() => fileInputRef.current?.click()} className="flex items-center space-x-2 px-3 py-2 border rounded-lg text-sm bg-white hover:bg-slate-50"><FileUpIcon size={16}/><span>导入</span></button>
          <div className="relative">
            <SearchIcon className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" size={16} />
            <input type="text" placeholder="搜索项目..." className="pl-10 pr-4 py-2 bg-slate-100 border-none rounded-full text-sm w-40 focus:w-56 transition-all" value={searchTerm} onChange={e => setSearchTerm(e.target.value)} />
          </div>
          <button onClick={() => setExportMenuOpen(!exportMenuOpen)} className="flex items-center space-x-2 px-4 py-2 bg-slate-800 text-white rounded-lg text-sm font-medium hover:bg-slate-700">
            <DownloadIcon size={16} /><span>导出</span><ChevronDownIcon size={14} />
          </button>
          {exportMenuOpen && (
            <div className="absolute right-6 top-16 w-48 bg-white border rounded-xl shadow-xl py-2 z-30">
              <button onClick={handleExportExcel} className="w-full text-left px-4 py-2 text-sm hover:bg-slate-50 flex items-center space-x-2"><FileSpreadsheetIcon size={14} /><span>Excel</span></button>
              <button onClick={handleExportPDF} className="w-full text-left px-4 py-2 text-sm hover:bg-slate-50 flex items-center space-x-2"><FileTextIcon size={14} /><span>PDF</span></button>
            </div>
          )}
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-6 mt-8">
        <div className="flex justify-between items-center mb-8">
          <div className="flex items-center text-sm text-slate-500 space-x-2 font-medium">
            <span>首页</span><ChevronRightIcon size={14}/><span className="text-slate-800 font-bold uppercase">指标分析</span>
          </div>
          <div className="flex bg-slate-200 p-1 rounded-lg">
            {(['revenue', 'dau', 'newUsers'] as MetricType[]).map(m => (
              <button key={m} onClick={() => setSelectedMetric(m)} className={`px-4 py-1 rounded-md text-xs font-bold ${selectedMetric === m ? 'bg-white text-blue-600 shadow-sm' : 'text-slate-500'}`}>
                {m === 'revenue' ? '金额' : m === 'dau' ? 'DAU' : '新增'}
              </button>
            ))}
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-10">
          <StatCard title="累计充值" janValue={totals.jan.revenue} decValue={totals.dec.revenue} unit=" ₹" />
          <StatCard title="累计新增" janValue={totals.jan.newUsers} decValue={totals.dec.newUsers} />
          <StatCard title="平均 DAU" janValue={totals.jan.dau} decValue={totals.dec.dau} />
        </div>

        <ComparisonCharts projects={projects} selectedMetric={selectedMetric} />
        
        <ProjectTable 
          projects={filtered} 
          onUpdateName={(id, name) => {
            const updated = projects.map(p => p.id === id ? { ...p, name } : p);
            setProjects(updated);
            pushToHistory(`重命名: ${name}`, updated);
          }} 
          onUpdateMetric={(id, month, metric, value) => {
            const updated = projects.map(p => p.id === id ? { ...p, [month]: { ...p[month], [metric]: value } } : p);
            setProjects(updated);
            pushToHistory(`更新 ${month} 数据`, updated);
          }}
          editingId={editingId} setEditingId={setEditingId}
          tableTitle={tableTitle} onUpdateTableTitle={setTableTitle}
          janHeader={janHeader} onUpdateJanHeader={setJanHeader}
          decHeader={decHeader} onUpdateDecHeader={setDecHeader}
        />
      </main>

      {isHistoryOpen && (
        <div className="fixed inset-0 z-50 bg-black/20 backdrop-blur-sm" onClick={() => setIsHistoryOpen(false)}>
          <div className="absolute right-0 top-0 h-full w-80 bg-white shadow-2xl p-6 overflow-y-auto" onClick={e => e.stopPropagation()}>
            <div className="flex items-center justify-between mb-8">
              <h2 className="text-lg font-bold flex items-center space-x-2"><HistoryIcon size={20}/><span>历史记录</span></h2>
              <button onClick={() => setIsHistoryOpen(false)}><XIcon size={20}/></button>
            </div>
            {history.map((h, i) => (
              <div key={h.id} className="mb-6 pl-4 border-l-2 border-slate-100 hover:border-blue-500 transition-colors">
                <p className="text-[10px] text-slate-400 font-mono">{h.timestamp.toLocaleTimeString()}</p>
                <p className="text-sm font-bold text-slate-700">{h.actionLabel}</p>
                {i !== 0 && <button className="text-xs text-blue-600 mt-2" onClick={() => { setProjects(h.projects); setIsHistoryOpen(false); }}>恢复</button>}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default App;
