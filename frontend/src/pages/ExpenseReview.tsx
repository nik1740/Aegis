import { useState } from 'react';
import { expenses, Expense, type Category, type ExpenseStatus } from '@/lib/mock-data';
import { StatusBadge, FraudScoreIndicator } from '@/components/StatusBadge';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Sheet, SheetContent, SheetHeader, SheetTitle } from '@/components/ui/sheet';
import { X } from 'lucide-react';

const allStatuses: ExpenseStatus[] = ['SUBMITTED', 'PROCESSING', 'APPROVED', 'REJECTED', 'NEEDS_REMEDIATION', 'ESCALATED', 'PENDING'];
const allCategories: Category[] = ['Meals', 'Transport', 'Accommodation', 'Office Supplies', 'Client Entertainment', 'Conference'];

export default function ExpenseReview() {
  const [statusFilter, setStatusFilter] = useState<string>('all');
  const [categoryFilter, setCategoryFilter] = useState<string>('all');
  const [search, setSearch] = useState('');
  const [selected, setSelected] = useState<Expense | null>(null);

  const filtered = expenses.filter(e => {
    if (statusFilter !== 'all' && e.status !== statusFilter) return false;
    if (categoryFilter !== 'all' && e.category !== categoryFilter) return false;
    if (search && !e.employeeName.toLowerCase().includes(search.toLowerCase()) && !e.id.toLowerCase().includes(search.toLowerCase())) return false;
    return true;
  });

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-foreground">Expense Review</h1>
        <p className="text-sm text-muted-foreground">Review and manage all expense submissions</p>
      </div>

      <div className="glass-card p-4 flex flex-wrap gap-3 items-center">
        <Select value={statusFilter} onValueChange={setStatusFilter}>
          <SelectTrigger className="w-44 bg-secondary border-border"><SelectValue placeholder="Status" /></SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All Statuses</SelectItem>
            {allStatuses.map(s => <SelectItem key={s} value={s}>{s.replace('_', ' ')}</SelectItem>)}
          </SelectContent>
        </Select>
        <Select value={categoryFilter} onValueChange={setCategoryFilter}>
          <SelectTrigger className="w-44 bg-secondary border-border"><SelectValue placeholder="Category" /></SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All Categories</SelectItem>
            {allCategories.map(c => <SelectItem key={c} value={c}>{c}</SelectItem>)}
          </SelectContent>
        </Select>
        <Input placeholder="Search employee or ID..." value={search} onChange={e => setSearch(e.target.value)} className="w-56 bg-secondary border-border" />
        <span className="text-xs text-muted-foreground ml-auto">{filtered.length} results</span>
      </div>

      <div className="glass-card overflow-hidden">
        <Table>
          <TableHeader>
            <TableRow className="border-border hover:bg-transparent">
              <TableHead className="text-muted-foreground">Expense ID</TableHead>
              <TableHead className="text-muted-foreground">Employee</TableHead>
              <TableHead className="text-muted-foreground">Merchant</TableHead>
              <TableHead className="text-muted-foreground">Amount</TableHead>
              <TableHead className="text-muted-foreground">Category</TableHead>
              <TableHead className="text-muted-foreground">Status</TableHead>
              <TableHead className="text-muted-foreground">Fraud Score</TableHead>
              <TableHead className="text-muted-foreground">Date</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {filtered.map(exp => (
              <TableRow key={exp.id} className="border-border cursor-pointer hover:bg-accent/50" onClick={() => setSelected(exp)}>
                <TableCell className="font-mono text-xs text-foreground">{exp.id}</TableCell>
                <TableCell className="text-foreground">{exp.employeeName}</TableCell>
                <TableCell className="text-muted-foreground">{exp.merchant}</TableCell>
                <TableCell className="text-foreground font-medium">£{exp.amount.toFixed(2)}</TableCell>
                <TableCell className="text-muted-foreground">{exp.category}</TableCell>
                <TableCell><StatusBadge status={exp.status} /></TableCell>
                <TableCell><FraudScoreIndicator score={exp.fraudScore} /></TableCell>
                <TableCell className="text-muted-foreground text-xs">{exp.submittedDate}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>

      <Sheet open={!!selected} onOpenChange={() => setSelected(null)}>
        <SheetContent className="w-full sm:max-w-lg bg-card border-border overflow-y-auto">
          {selected && (
            <>
              <SheetHeader>
                <SheetTitle className="text-foreground flex items-center justify-between">
                  {selected.id}
                  <StatusBadge status={selected.status} />
                </SheetTitle>
              </SheetHeader>
              <div className="space-y-6 mt-6">
                <div className="glass-card p-4 space-y-2">
                  <h4 className="text-xs font-medium text-muted-foreground uppercase tracking-wider">Receipt Details</h4>
                  <div className="grid grid-cols-2 gap-2 text-sm">
                    <span className="text-muted-foreground">Merchant</span><span className="text-foreground">{selected.merchant}</span>
                    <span className="text-muted-foreground">Amount</span><span className="text-foreground font-medium">£{selected.amount.toFixed(2)}</span>
                    <span className="text-muted-foreground">Date</span><span className="text-foreground">{selected.submittedDate}</span>
                    <span className="text-muted-foreground">Category</span><span className="text-foreground">{selected.category}</span>
                  </div>
                  {selected.lineItems && (
                    <Table>
                      <TableBody>
                        {selected.lineItems.map((li, i) => (
                          <TableRow key={i} className="border-border">
                            <TableCell className="text-sm text-foreground py-1">{li.item}</TableCell>
                            <TableCell className="text-sm text-foreground py-1 text-right">£{li.amount.toFixed(2)}</TableCell>
                          </TableRow>
                        ))}
                      </TableBody>
                    </Table>
                  )}
                </div>

                <div className="glass-card p-4 space-y-3">
                  <h4 className="text-xs font-medium text-muted-foreground uppercase tracking-wider">AI Agent Verdicts</h4>
                  <div className="space-y-3">
                    <div className="p-3 rounded-lg bg-secondary/50 space-y-1">
                      <div className="flex items-center justify-between">
                        <span className="text-xs font-medium text-foreground">✅ Contextual Auditor</span>
                        <span className="text-xs text-success">PASS — 92%</span>
                      </div>
                      <p className="text-xs text-muted-foreground">Expense within policy limits. Rule: MEAL-UK-002</p>
                    </div>
                    <div className="p-3 rounded-lg bg-secondary/50 space-y-1">
                      <div className="flex items-center justify-between">
                        <span className="text-xs font-medium text-foreground">🔎 Fraud Detective</span>
                        <FraudScoreIndicator score={selected.fraudScore} />
                      </div>
                      <p className="text-xs text-muted-foreground">No anomalies detected. Velocity check passed.</p>
                    </div>
                    <div className="p-3 rounded-lg bg-secondary/50 space-y-1">
                      <div className="flex items-center justify-between">
                        <span className="text-xs font-medium text-foreground">⚖️ Compliance Judge</span>
                        <StatusBadge status={selected.status} />
                      </div>
                      <p className="text-xs text-muted-foreground">Final decision rendered based on policy compliance and fraud assessment.</p>
                    </div>
                  </div>
                </div>

                <div className="flex gap-2">
                  <Button className="flex-1 bg-success hover:bg-success/90 text-success-foreground">Approve</Button>
                  <Button variant="destructive" className="flex-1">Reject</Button>
                  <Button variant="outline" className="flex-1">Escalate</Button>
                </div>
              </div>
            </>
          )}
        </SheetContent>
      </Sheet>
    </div>
  );
}
