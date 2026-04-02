import { cn } from '@/lib/utils';
import { ExpenseStatus } from '@/lib/mock-data';

const statusConfig: Record<ExpenseStatus, { bg: string; text: string }> = {
  APPROVED: { bg: 'bg-success/15', text: 'text-success' },
  REJECTED: { bg: 'bg-destructive/15', text: 'text-destructive' },
  PENDING: { bg: 'bg-warning/15', text: 'text-warning' },
  SUBMITTED: { bg: 'bg-primary/15', text: 'text-primary' },
  PROCESSING: { bg: 'bg-primary/15', text: 'text-primary' },
  NEEDS_REMEDIATION: { bg: 'bg-warning/15', text: 'text-warning' },
  ESCALATED: { bg: 'bg-destructive/15', text: 'text-destructive' },
};

export function StatusBadge({ status, className }: { status: ExpenseStatus; className?: string }) {
  const config = statusConfig[status];
  return (
    <span className={cn('inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium', config.bg, config.text, className)}>
      {status.replace('_', ' ')}
    </span>
  );
}

export function FraudScoreIndicator({ score }: { score: number }) {
  const color = score < 0.3 ? 'text-success' : score < 0.6 ? 'text-warning' : 'text-destructive';
  const bg = score < 0.3 ? 'bg-success' : score < 0.6 ? 'bg-warning' : 'bg-destructive';
  return (
    <div className="flex items-center gap-2">
      <div className="w-12 h-1.5 rounded-full bg-muted overflow-hidden">
        <div className={cn('h-full rounded-full', bg)} style={{ width: `${score * 100}%` }} />
      </div>
      <span className={cn('text-xs font-mono', color)}>{score.toFixed(2)}</span>
    </div>
  );
}
