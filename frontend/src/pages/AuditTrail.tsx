import { useState } from 'react';
import { useParams } from 'react-router-dom';
import { auditSteps, expenses } from '@/lib/mock-data';
import { StatusBadge } from '@/components/StatusBadge';
import { cn } from '@/lib/utils';
import { ChevronDown, ChevronRight } from 'lucide-react';

export default function AuditTrail() {
  const { expenseId } = useParams();
  const expense = expenses.find(e => e.id === expenseId) || expenses[0];
  const [expandedSteps, setExpandedSteps] = useState<Set<number>>(new Set());

  const toggleStep = (step: number) => {
    setExpandedSteps(prev => {
      const next = new Set(prev);
      next.has(step) ? next.delete(step) : next.add(step);
      return next;
    });
  };

  return (
    <div className="space-y-6 max-w-4xl">
      <div>
        <h1 className="text-2xl font-bold text-foreground">Audit Trail</h1>
        <p className="text-sm text-muted-foreground">Complete AI decision trace for {expense.id}</p>
      </div>

      <div className="glass-card p-5 flex flex-wrap items-center gap-6">
        <div>
          <p className="text-xs text-muted-foreground">Expense ID</p>
          <p className="text-sm font-mono text-foreground">{expense.id}</p>
        </div>
        <div>
          <p className="text-xs text-muted-foreground">Employee</p>
          <p className="text-sm text-foreground">{expense.employeeName}</p>
        </div>
        <div>
          <p className="text-xs text-muted-foreground">Amount</p>
          <p className="text-sm font-medium text-foreground">£{expense.amount.toFixed(2)}</p>
        </div>
        <div className="ml-auto">
          <StatusBadge status={expense.status} className="text-sm px-4 py-1" />
        </div>
      </div>

      <div className="space-y-0 relative">
        <div className="absolute left-6 top-0 bottom-0 w-px bg-border" />
        {auditSteps.map((step) => {
          const isExpanded = expandedSteps.has(step.step);
          return (
            <div key={step.step} className="relative pl-14 pb-6">
              <div className="absolute left-4 top-1 w-5 h-5 rounded-full bg-card border-2 border-primary flex items-center justify-center text-xs z-10">
                {step.icon}
              </div>
              <div className="glass-card p-4 cursor-pointer hover:bg-accent/30 transition-colors" onClick={() => toggleStep(step.step)}>
                <div className="flex items-start justify-between">
                  <div className="flex items-center gap-2">
                    {isExpanded ? <ChevronDown className="w-4 h-4 text-muted-foreground" /> : <ChevronRight className="w-4 h-4 text-muted-foreground" />}
                    <div>
                      <p className="text-sm font-medium text-foreground">{step.title}</p>
                      <p className="text-xs text-muted-foreground">{step.description}</p>
                    </div>
                  </div>
                  <div className="text-right flex-shrink-0">
                    {step.latencyMs > 0 && <span className="text-xs font-mono text-muted-foreground">{step.latencyMs}ms</span>}
                    <p className="text-[10px] text-muted-foreground">{new Date(step.timestamp).toLocaleTimeString()}</p>
                  </div>
                </div>
                {isExpanded && (
                  <pre className="mt-3 p-3 rounded-lg bg-secondary/50 text-xs text-muted-foreground overflow-x-auto font-mono">
                    {JSON.stringify(step.payload, null, 2)}
                  </pre>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
