import { useState } from 'react';
import { policyRules, PolicyRule } from '@/lib/mock-data';
import { cn } from '@/lib/utils';
import { ScrollText, ArrowRight } from 'lucide-react';

const grouped = policyRules.reduce<Record<string, PolicyRule[]>>((acc, r) => {
  (acc[r.category] = acc[r.category] || []).push(r);
  return acc;
}, {});

export default function PolicyExplorer() {
  const [selected, setSelected] = useState<PolicyRule>(policyRules[0]);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-foreground">Policy Explorer</h1>
        <p className="text-sm text-muted-foreground">Interactive view of corporate expense policies</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        <div className="glass-card p-4 space-y-4">
          <h3 className="text-sm font-semibold text-foreground">Policy Rules</h3>
          {Object.entries(grouped).map(([cat, rules]) => (
            <div key={cat} className="space-y-1">
              <p className="text-xs font-medium text-muted-foreground uppercase tracking-wider flex items-center gap-1.5">
                <ScrollText className="w-3 h-3" /> {cat}
              </p>
              {rules.map(r => (
                <button
                  key={r.id}
                  onClick={() => setSelected(r)}
                  className={cn(
                    'w-full text-left px-3 py-2 rounded-lg text-sm transition-colors',
                    selected.id === r.id ? 'bg-primary/15 text-primary' : 'text-foreground hover:bg-accent'
                  )}
                >
                  <span className="font-mono text-xs">{r.id}</span>
                  <span className="block text-xs text-muted-foreground mt-0.5">£{r.limitAmount}/{r.period}</span>
                </button>
              ))}
            </div>
          ))}
        </div>

        <div className="lg:col-span-2 space-y-4">
          <div className="glass-card p-6 space-y-4">
            <div className="flex items-center justify-between">
              <h3 className="text-lg font-bold text-foreground">{selected.id}</h3>
              <span className="glass-card px-3 py-1 text-xs text-primary font-medium">£{selected.limitAmount} / {selected.period}</span>
            </div>
            <p className="text-sm text-muted-foreground">{selected.description}</p>
            <div className="grid grid-cols-2 gap-4 text-sm">
              <div>
                <p className="text-xs text-muted-foreground uppercase tracking-wider mb-1">Currency</p>
                <p className="text-foreground">{selected.currency}</p>
              </div>
              <div>
                <p className="text-xs text-muted-foreground uppercase tracking-wider mb-1">Period</p>
                <p className="text-foreground capitalize">{selected.period.replace('_', ' ')}</p>
              </div>
              <div>
                <p className="text-xs text-muted-foreground uppercase tracking-wider mb-1">Applicable Roles</p>
                <div className="flex flex-wrap gap-1">
                  {selected.applicableRoles.map(r => (
                    <span key={r} className="px-2 py-0.5 rounded-full bg-primary/15 text-primary text-xs">{r}</span>
                  ))}
                </div>
              </div>
              <div>
                <p className="text-xs text-muted-foreground uppercase tracking-wider mb-1">Locations</p>
                <div className="flex flex-wrap gap-1">
                  {selected.applicableLocations.map(l => (
                    <span key={l} className="px-2 py-0.5 rounded-full bg-accent text-accent-foreground text-xs">{l}</span>
                  ))}
                </div>
              </div>
            </div>
          </div>

          <div className="glass-card p-6">
            <h3 className="text-sm font-semibold text-foreground mb-4">Policy Relationship</h3>
            <div className="flex items-center justify-center gap-3 flex-wrap">
              {selected.applicableRoles.map(role => (
                <div key={role} className="flex items-center gap-2">
                  <div className="px-3 py-2 rounded-lg bg-primary/15 text-primary text-xs font-medium">{role}</div>
                  <ArrowRight className="w-4 h-4 text-muted-foreground" />
                </div>
              ))}
              <div className="px-3 py-2 rounded-lg gradient-primary text-white text-xs font-medium">{selected.id}</div>
              <ArrowRight className="w-4 h-4 text-muted-foreground" />
              <div className="px-3 py-2 rounded-lg bg-success/15 text-success text-xs font-medium">{selected.category}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
