import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, LineChart, Line, PieChart, Pie, Cell } from 'recharts';
import { categorySpend, approvalTrend, departmentSpend, expenses } from '@/lib/mock-data';
import { StatusBadge } from '@/components/StatusBadge';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { TrendingUp, AlertTriangle, Clock, FileText } from 'lucide-react';

const kpis = [
  { label: 'Total Submissions', value: '1,247', sub: 'This month', icon: FileText, color: 'text-primary' },
  { label: 'Auto-Approved', value: '892', sub: '71.5%', icon: TrendingUp, color: 'text-success' },
  { label: 'Fraud Flags', value: '23', sub: 'Active alerts', icon: AlertTriangle, color: 'text-destructive' },
  { label: 'Avg Processing', value: '4.2s', sub: 'Per expense', icon: Clock, color: 'text-warning' },
];

const CustomTooltip = ({ active, payload, label }: any) => {
  if (!active || !payload?.length) return null;
  return (
    <div className="glass-card p-2 text-xs">
      <p className="text-foreground font-medium">{label}</p>
      {payload.map((p: any, i: number) => (
        <p key={i} className="text-muted-foreground">{p.name}: {typeof p.value === 'number' && p.name !== 'rate' ? `£${p.value.toLocaleString()}` : `${p.value}%`}</p>
      ))}
    </div>
  );
};

export default function Dashboard() {
  const recentExpenses = expenses.slice(0, 10);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-foreground">Dashboard</h1>
          <p className="text-sm text-muted-foreground">AI-powered expense management overview</p>
        </div>
        <div className="glass-card px-3 py-1.5 text-xs text-muted-foreground flex items-center gap-1.5">
          🔍 <span className="font-medium text-foreground">Glass Box</span> — Every decision is fully traceable
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {kpis.map(kpi => (
          <div key={kpi.label} className="glass-card p-5 hover:scale-[1.02] transition-transform cursor-default">
            <div className="flex items-start justify-between">
              <div>
                <p className="text-xs text-muted-foreground">{kpi.label}</p>
                <p className="text-2xl font-bold text-foreground mt-1">{kpi.value}</p>
                <p className={`text-xs mt-1 ${kpi.color}`}>{kpi.sub}</p>
              </div>
              <kpi.icon className={`w-5 h-5 ${kpi.color}`} />
            </div>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <div className="glass-card p-5">
          <h3 className="text-sm font-semibold text-foreground mb-4">Spend by Category</h3>
          <ResponsiveContainer width="100%" height={240}>
            <BarChart data={categorySpend}>
              <XAxis dataKey="category" tick={{ fill: 'hsl(215,20%,65%)', fontSize: 11 }} axisLine={false} tickLine={false} />
              <YAxis tick={{ fill: 'hsl(215,20%,65%)', fontSize: 11 }} axisLine={false} tickLine={false} tickFormatter={v => `£${(v/1000).toFixed(0)}k`} />
              <Tooltip content={<CustomTooltip />} />
              <Bar dataKey="amount" fill="hsl(239,84%,67%)" radius={[6, 6, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="glass-card p-5">
          <h3 className="text-sm font-semibold text-foreground mb-4">Approval Rate Trend (30 days)</h3>
          <ResponsiveContainer width="100%" height={240}>
            <LineChart data={approvalTrend}>
              <XAxis dataKey="day" tick={{ fill: 'hsl(215,20%,65%)', fontSize: 11 }} axisLine={false} tickLine={false} interval={4} />
              <YAxis domain={[60, 90]} tick={{ fill: 'hsl(215,20%,65%)', fontSize: 11 }} axisLine={false} tickLine={false} tickFormatter={v => `${v}%`} />
              <Tooltip content={<CustomTooltip />} />
              <Line type="monotone" dataKey="rate" stroke="hsl(160,84%,39%)" strokeWidth={2} dot={false} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        <div className="glass-card p-5">
          <h3 className="text-sm font-semibold text-foreground mb-4">Department Spend</h3>
          <ResponsiveContainer width="100%" height={240}>
            <PieChart>
              <Pie data={departmentSpend} dataKey="value" nameKey="name" cx="50%" cy="50%" innerRadius={50} outerRadius={90} strokeWidth={0}>
                {departmentSpend.map((entry, i) => (
                  <Cell key={i} fill={entry.fill} />
                ))}
              </Pie>
              <Tooltip content={<CustomTooltip />} />
            </PieChart>
          </ResponsiveContainer>
          <div className="flex flex-wrap gap-3 mt-2">
            {departmentSpend.map(d => (
              <div key={d.name} className="flex items-center gap-1.5 text-xs text-muted-foreground">
                <span className="w-2 h-2 rounded-full" style={{ background: d.fill }} />
                {d.name}
              </div>
            ))}
          </div>
        </div>

        <div className="lg:col-span-2 glass-card p-5">
          <h3 className="text-sm font-semibold text-foreground mb-4">Recent Decisions</h3>
          <Table>
            <TableHeader>
              <TableRow className="border-border hover:bg-transparent">
                <TableHead className="text-muted-foreground">ID</TableHead>
                <TableHead className="text-muted-foreground">Employee</TableHead>
                <TableHead className="text-muted-foreground">Merchant</TableHead>
                <TableHead className="text-muted-foreground">Amount</TableHead>
                <TableHead className="text-muted-foreground">Category</TableHead>
                <TableHead className="text-muted-foreground">Status</TableHead>
                <TableHead className="text-muted-foreground">Date</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {recentExpenses.map(exp => (
                <TableRow key={exp.id} className="border-border">
                  <TableCell className="font-mono text-xs text-foreground">{exp.id}</TableCell>
                  <TableCell className="text-foreground">{exp.employeeName}</TableCell>
                  <TableCell className="text-muted-foreground">{exp.merchant}</TableCell>
                  <TableCell className="text-foreground font-medium">£{exp.amount.toFixed(2)}</TableCell>
                  <TableCell className="text-muted-foreground">{exp.category}</TableCell>
                  <TableCell><StatusBadge status={exp.status} /></TableCell>
                  <TableCell className="text-muted-foreground text-xs">{exp.submittedDate}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>
      </div>
    </div>
  );
}
