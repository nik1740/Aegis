import { useState, useCallback } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Label } from '@/components/ui/label';
import { toast } from 'sonner';
import { Upload, FileText, CheckCircle, Loader2 } from 'lucide-react';
import { cn } from '@/lib/utils';

const steps = ['Extracting', 'Analyzing', 'Auditing', 'Decision'];

export default function SubmitExpense() {
  const [dragOver, setDragOver] = useState(false);
  const [file, setFile] = useState<File | null>(null);
  const [submitting, setSubmitting] = useState(false);
  const [processingStep, setProcessingStep] = useState(-1);
  const [done, setDone] = useState(false);
  const idempotencyKey = useState(() => crypto.randomUUID())[0];

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setDragOver(false);
    const f = e.dataTransfer.files[0];
    if (f) setFile(f);
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);
    setProcessingStep(0);
    for (let i = 0; i < steps.length; i++) {
      await new Promise(r => setTimeout(r, 800));
      setProcessingStep(i);
    }
    await new Promise(r => setTimeout(r, 500));
    setSubmitting(false);
    setDone(true);
    toast.success('Expense submitted successfully!', {
      description: 'EXP-2026-10051 — Track it in Audit Trail',
    });
  };

  if (done) {
    return (
      <div className="max-w-2xl mx-auto space-y-6">
        <div className="glass-card p-12 text-center space-y-4">
          <div className="w-16 h-16 rounded-full bg-success/15 flex items-center justify-center mx-auto">
            <CheckCircle className="w-8 h-8 text-success" />
          </div>
          <h2 className="text-xl font-bold text-foreground">Expense Submitted</h2>
          <p className="text-sm text-muted-foreground">Your expense has been processed by our AI agents.</p>
          <p className="font-mono text-primary text-sm">EXP-2026-10051</p>
          <Button variant="outline" onClick={() => { setDone(false); setFile(null); }}>Submit Another</Button>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-foreground">Submit Expense</h1>
        <p className="text-sm text-muted-foreground">Upload a receipt and submit for AI processing</p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        <div
          className={cn('glass-card p-8 border-2 border-dashed text-center cursor-pointer transition-colors', dragOver ? 'border-primary bg-primary/5' : 'border-border')}
          onDragOver={e => { e.preventDefault(); setDragOver(true); }}
          onDragLeave={() => setDragOver(false)}
          onDrop={handleDrop}
          onClick={() => document.getElementById('file-upload')?.click()}
        >
          <input id="file-upload" type="file" accept="image/*,.pdf" className="hidden" onChange={e => e.target.files?.[0] && setFile(e.target.files[0])} />
          {file ? (
            <div className="flex items-center justify-center gap-3">
              <FileText className="w-8 h-8 text-primary" />
              <div className="text-left">
                <p className="text-sm text-foreground font-medium">{file.name}</p>
                <p className="text-xs text-muted-foreground">{(file.size / 1024).toFixed(1)} KB</p>
              </div>
            </div>
          ) : (
            <>
              <Upload className="w-8 h-8 text-muted-foreground mx-auto mb-2" />
              <p className="text-sm text-muted-foreground">Drag & drop receipt or <span className="text-primary">browse</span></p>
              <p className="text-xs text-muted-foreground mt-1">Images & PDFs accepted</p>
            </>
          )}
        </div>

        <div className="glass-card p-6 space-y-4">
          <div className="space-y-2">
            <Label className="text-foreground">Employee</Label>
            <Select>
              <SelectTrigger className="bg-secondary border-border"><SelectValue placeholder="Select employee" /></SelectTrigger>
              <SelectContent>
                {['E-1042 — Alice Johnson', 'E-1087 — Bob Smith', 'E-1123 — Carol Davis', 'E-1156 — David Wilson', 'E-1201 — Eva Martinez'].map(e => (
                  <SelectItem key={e} value={e}>{e}</SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
          <div className="space-y-2">
            <Label className="text-foreground">Business Justification</Label>
            <Textarea placeholder="Describe the business purpose..." className="bg-secondary border-border min-h-[80px]" />
          </div>
          <div className="space-y-2">
            <Label className="text-foreground">Category</Label>
            <Select>
              <SelectTrigger className="bg-secondary border-border"><SelectValue placeholder="Select category" /></SelectTrigger>
              <SelectContent>
                {['Meals', 'Transport', 'Accommodation', 'Office Supplies', 'Client Entertainment', 'Conference'].map(c => (
                  <SelectItem key={c} value={c}>{c}</SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
          <div className="space-y-2">
            <Label className="text-foreground">Idempotency Key</Label>
            <Input value={idempotencyKey} readOnly className="bg-secondary border-border font-mono text-xs text-muted-foreground" />
          </div>
        </div>

        <Button type="submit" disabled={submitting} className="w-full gradient-primary text-white h-11">
          {submitting ? <Loader2 className="w-4 h-4 animate-spin mr-2" /> : null}
          {submitting ? 'Processing...' : 'Submit Expense'}
        </Button>
      </form>

      {submitting && (
        <div className="glass-card p-6 space-y-3">
          <h3 className="text-sm font-semibold text-foreground">AI Processing</h3>
          {steps.map((step, i) => (
            <div key={step} className="flex items-center gap-3">
              <div className={cn('w-6 h-6 rounded-full flex items-center justify-center text-xs', i <= processingStep ? 'bg-success/15 text-success' : 'bg-secondary text-muted-foreground')}>
                {i <= processingStep ? '✓' : i}
              </div>
              <span className={cn('text-sm', i <= processingStep ? 'text-foreground' : 'text-muted-foreground')}>{step}</span>
              {i === processingStep && <Loader2 className="w-3 h-3 animate-spin text-primary" />}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
