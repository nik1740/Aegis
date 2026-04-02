import { useState } from 'react';
import { useParams } from 'react-router-dom';
import { expenses, sampleChat, ChatMessage } from '@/lib/mock-data';
import { StatusBadge } from '@/components/StatusBadge';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Send, CheckCircle } from 'lucide-react';
import { cn } from '@/lib/utils';

export default function NegotiationChat() {
  const { expenseId } = useParams();
  const expense = expenses.find(e => e.id === expenseId) || expenses[0];
  const [messages, setMessages] = useState<ChatMessage[]>(sampleChat);
  const [input, setInput] = useState('');

  const sendMessage = () => {
    if (!input.trim()) return;
    setMessages(prev => [...prev, {
      id: String(prev.length + 1),
      sender: 'employee',
      message: input,
      timestamp: new Date().toISOString(),
      type: 'text',
    }]);
    setInput('');
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-foreground">Negotiation</h1>
        <p className="text-sm text-muted-foreground">Remediation flow for {expense.id}</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 h-[calc(100vh-12rem)]">
        <div className="glass-card p-5 space-y-4">
          <h3 className="text-sm font-semibold text-foreground">Expense Summary</h3>
          <div className="space-y-3 text-sm">
            <div><p className="text-xs text-muted-foreground">ID</p><p className="font-mono text-foreground">{expense.id}</p></div>
            <div><p className="text-xs text-muted-foreground">Amount</p><p className="text-foreground font-medium">£{expense.amount.toFixed(2)}</p></div>
            <div><p className="text-xs text-muted-foreground">Merchant</p><p className="text-foreground">{expense.merchant}</p></div>
            <div><p className="text-xs text-muted-foreground">Category</p><p className="text-foreground">{expense.category}</p></div>
            <div><p className="text-xs text-muted-foreground">Status</p><StatusBadge status="NEEDS_REMEDIATION" /></div>
            <div><p className="text-xs text-muted-foreground">Discrepancy</p><p className="text-destructive text-xs">Exceeds £45 daily meal limit by £12</p></div>
          </div>
          <div className="glass-card p-3 text-center">
            <p className="text-xs text-muted-foreground">Round</p>
            <p className="text-lg font-bold text-foreground">1 <span className="text-sm text-muted-foreground font-normal">of 3</span></p>
          </div>
        </div>

        <div className="lg:col-span-2 glass-card flex flex-col">
          <div className="p-4 border-b border-border flex items-center justify-between">
            <h3 className="text-sm font-semibold text-foreground">Remediation Chat</h3>
            <StatusBadge status="PENDING" />
          </div>

          <div className="flex-1 overflow-y-auto p-4 space-y-4">
            {messages.map(msg => (
              <div key={msg.id} className={cn('flex gap-3', msg.sender === 'employee' ? 'justify-end' : 'justify-start')}>
                {msg.sender === 'agent' && <span className="w-8 h-8 rounded-full bg-primary/20 flex items-center justify-center text-sm flex-shrink-0">🤖</span>}
                <div className={cn('max-w-[75%] space-y-2', msg.sender === 'employee' ? 'items-end' : 'items-start')}>
                  {msg.type === 'validation' && msg.validationResult ? (
                    <div className={cn('rounded-xl p-3 text-sm', msg.validationResult.success ? 'bg-success/15 border border-success/30' : 'bg-destructive/15 border border-destructive/30')}>
                      <div className="flex items-center gap-1.5 mb-1">
                        <CheckCircle className={cn('w-4 h-4', msg.validationResult.success ? 'text-success' : 'text-destructive')} />
                        <span className={cn('text-xs font-medium', msg.validationResult.success ? 'text-success' : 'text-destructive')}>
                          CRM Validation
                        </span>
                      </div>
                      <p className="text-xs text-muted-foreground">{msg.validationResult.detail}</p>
                    </div>
                  ) : (
                    <div className={cn('rounded-xl px-4 py-2.5 text-sm', msg.sender === 'agent' ? 'bg-secondary text-foreground' : 'gradient-primary text-white')}>
                      {msg.message}
                    </div>
                  )}
                  <p className="text-[10px] text-muted-foreground">{new Date(msg.timestamp).toLocaleTimeString()}</p>
                </div>
                {msg.sender === 'employee' && <span className="w-8 h-8 rounded-full bg-accent flex items-center justify-center text-sm flex-shrink-0">👤</span>}
              </div>
            ))}
          </div>

          <div className="p-4 border-t border-border flex gap-2">
            <Input
              value={input}
              onChange={e => setInput(e.target.value)}
              onKeyDown={e => e.key === 'Enter' && sendMessage()}
              placeholder="Type a response..."
              className="bg-secondary border-border"
            />
            <Button onClick={sendMessage} className="gradient-primary text-white"><Send className="w-4 h-4" /></Button>
          </div>
        </div>
      </div>
    </div>
  );
}
