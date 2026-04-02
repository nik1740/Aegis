import { useState } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { cn } from '@/lib/utils';
import { Input } from '@/components/ui/input';
import {
  LayoutDashboard, ClipboardList, ScrollText, Search, MessageSquare, PlusCircle, Settings, Shield, ChevronLeft, ChevronRight
} from 'lucide-react';

const navItems = [
  { label: 'Dashboard', icon: LayoutDashboard, path: '/' },
  { label: 'Expense Review', icon: ClipboardList, path: '/expenses' },
  { label: 'Policy Explorer', icon: ScrollText, path: '/policies' },
  { label: 'Audit Trail', icon: Search, path: '/audit' },
  { label: 'Negotiations', icon: MessageSquare, path: '/negotiations' },
  { label: 'Submit Expense', icon: PlusCircle, path: '/submit' },
];

export function AppSidebar() {
  const location = useLocation();
  const navigate = useNavigate();
  const [collapsed, setCollapsed] = useState(false);
  const [auditSearch, setAuditSearch] = useState('');

  const handleAuditSearch = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && auditSearch.trim()) {
      navigate(`/audit/${auditSearch.trim()}`);
      setAuditSearch('');
    }
  };

  return (
    <aside className={cn(
      'h-screen sticky top-0 flex flex-col border-r border-border bg-sidebar transition-all duration-300',
      collapsed ? 'w-16' : 'w-64'
    )}>
      <div className="flex items-center gap-2 p-4 border-b border-border">
        <div className="w-8 h-8 rounded-lg gradient-primary flex items-center justify-center flex-shrink-0">
          <Shield className="w-4 h-4 text-white" />
        </div>
        {!collapsed && (
          <div>
            <h1 className="text-base font-bold text-foreground tracking-tight">Aegis</h1>
            <p className="text-[10px] text-muted-foreground">AI Expense Management</p>
          </div>
        )}
      </div>

      <nav className="flex-1 py-3 space-y-1 px-2 overflow-y-auto">
        {navItems.map(item => {
          const isActive = item.path === '/'
            ? location.pathname === '/'
            : location.pathname.startsWith(item.path);
          return (
            <Link
              key={item.path}
              to={item.path === '/audit' ? '/audit/EXP-2026-10001' : item.path === '/negotiations' ? '/negotiations/EXP-2026-10001' : item.path}
              className={cn(
                'flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm transition-colors',
                isActive
                  ? 'bg-primary/15 text-primary font-medium'
                  : 'text-sidebar-foreground hover:bg-sidebar-accent hover:text-sidebar-accent-foreground'
              )}
            >
              <item.icon className="w-4 h-4 flex-shrink-0" />
              {!collapsed && <span>{item.label}</span>}
            </Link>
          );
        })}

        {!collapsed && (
          <div className="px-3 pt-2">
            <Input
              placeholder="Search Expense ID..."
              value={auditSearch}
              onChange={e => setAuditSearch(e.target.value)}
              onKeyDown={handleAuditSearch}
              className="h-8 text-xs bg-sidebar-accent border-sidebar-border"
            />
          </div>
        )}

        <div className="border-t border-border my-3" />

        <Link
          to="#"
          className="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm text-sidebar-foreground hover:bg-sidebar-accent"
        >
          <Settings className="w-4 h-4 flex-shrink-0" />
          {!collapsed && <span>Settings</span>}
        </Link>
      </nav>

      {!collapsed && (
        <div className="p-4 border-t border-border space-y-1.5">
          <p className="text-[10px] font-medium text-muted-foreground uppercase tracking-wider">System Status</p>
          {['Gateway', 'Agents', 'Neo4j'].map(s => (
            <div key={s} className="flex items-center gap-2 text-xs text-sidebar-foreground">
              <span className="w-2 h-2 rounded-full bg-success" />
              <span>{s}</span>
            </div>
          ))}
        </div>
      )}

      <button
        onClick={() => setCollapsed(!collapsed)}
        className="p-2 m-2 rounded-lg hover:bg-sidebar-accent text-muted-foreground transition-colors"
      >
        {collapsed ? <ChevronRight className="w-4 h-4" /> : <ChevronLeft className="w-4 h-4" />}
      </button>
    </aside>
  );
}
