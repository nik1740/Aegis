export type ExpenseStatus = 'APPROVED' | 'REJECTED' | 'PENDING' | 'SUBMITTED' | 'PROCESSING' | 'NEEDS_REMEDIATION' | 'ESCALATED';
export type Category = 'Meals' | 'Transport' | 'Accommodation' | 'Office Supplies' | 'Client Entertainment' | 'Conference';

export interface Expense {
  id: string;
  employeeName: string;
  employeeId: string;
  merchant: string;
  amount: number;
  category: Category;
  status: ExpenseStatus;
  fraudScore: number;
  submittedDate: string;
  description: string;
  lineItems?: { item: string; amount: number }[];
}

export interface PolicyRule {
  id: string;
  description: string;
  category: string;
  limitAmount: number;
  currency: string;
  period: string;
  applicableRoles: string[];
  applicableLocations: string[];
}

export interface AuditStep {
  step: number;
  icon: string;
  title: string;
  description: string;
  timestamp: string;
  latencyMs: number;
  payload: Record<string, unknown>;
}

export interface ChatMessage {
  id: string;
  sender: 'agent' | 'employee';
  message: string;
  timestamp: string;
  type?: 'text' | 'validation';
  validationResult?: { success: boolean; detail: string };
}

const employees = ['Alice Johnson', 'Bob Smith', 'Carol Davis', 'David Wilson', 'Eva Martinez'];
const employeeIds = ['E-1042', 'E-1087', 'E-1123', 'E-1156', 'E-1201'];
const merchants = ['Pret A Manger', 'Uber', 'Wagamama', 'Dishoom', "Nando's", 'Premier Inn', 'Amazon Business'];
const categories: Category[] = ['Meals', 'Transport', 'Accommodation', 'Office Supplies', 'Client Entertainment', 'Conference'];
const statuses: ExpenseStatus[] = ['APPROVED', 'REJECTED', 'PENDING', 'SUBMITTED', 'PROCESSING', 'NEEDS_REMEDIATION', 'ESCALATED'];

function rand(min: number, max: number) { return Math.floor(Math.random() * (max - min + 1)) + min; }

export const expenses: Expense[] = Array.from({ length: 50 }, (_, i) => {
  const empIdx = i % 5;
  const cat = categories[i % categories.length];
  const statusIdx = i < 30 ? (i % 3 < 2 ? 0 : 1) : i % statuses.length;
  return {
    id: `EXP-2026-${String(10001 + i).padStart(5, '0')}`,
    employeeName: employees[empIdx],
    employeeId: employeeIds[empIdx],
    merchant: merchants[i % merchants.length],
    amount: parseFloat((rand(8, 250) + Math.random()).toFixed(2)),
    category: cat,
    status: statuses[statusIdx],
    fraudScore: parseFloat((Math.random() * 0.9).toFixed(2)),
    submittedDate: `2026-03-${String(rand(1, 31)).padStart(2, '0')}`,
    description: `${cat} expense at ${merchants[i % merchants.length]}`,
    lineItems: [
      { item: 'Main item', amount: parseFloat((rand(5, 150) + Math.random()).toFixed(2)) },
      { item: 'Tax/Service', amount: parseFloat((rand(1, 30) + Math.random()).toFixed(2)) },
    ],
  };
});

export const policyRules: PolicyRule[] = [
  { id: 'MEAL-UK-001', description: 'Daily meal allowance for Junior Analysts in UK offices', category: 'Meals', limitAmount: 35, currency: 'GBP', period: 'daily', applicableRoles: ['Junior Analyst'], applicableLocations: ['London', 'Manchester', 'Edinburgh'] },
  { id: 'MEAL-UK-002', description: 'Daily meal allowance for Senior Analysts in UK offices', category: 'Meals', limitAmount: 45, currency: 'GBP', period: 'daily', applicableRoles: ['Senior Analyst'], applicableLocations: ['London', 'Manchester', 'Edinburgh'] },
  { id: 'MEAL-UK-003', description: 'Daily meal allowance for Managers in UK offices', category: 'Meals', limitAmount: 60, currency: 'GBP', period: 'daily', applicableRoles: ['Manager', 'Director'], applicableLocations: ['London', 'Manchester', 'Edinburgh'] },
  { id: 'TRANSPORT-GLOBAL-001', description: 'Transport allowance per trip for all roles globally', category: 'Transport', limitAmount: 100, currency: 'GBP', period: 'per_trip', applicableRoles: ['All'], applicableLocations: ['Global'] },
  { id: 'ACCOM-UK-001', description: 'Nightly accommodation limit for London stays', category: 'Accommodation', limitAmount: 200, currency: 'GBP', period: 'per_night', applicableRoles: ['All'], applicableLocations: ['London'] },
  { id: 'CLIENT-ENT-001', description: 'Client entertainment limit per event for Senior+ roles', category: 'Client Entertainment', limitAmount: 150, currency: 'GBP', period: 'per_event', applicableRoles: ['Senior Analyst', 'Manager', 'Director'], applicableLocations: ['Global'] },
];

export const auditSteps: AuditStep[] = [
  { step: 1, icon: '📥', title: 'Submitted', description: 'Expense submitted by Alice Johnson', timestamp: '2026-03-15T09:23:14Z', latencyMs: 0, payload: { employeeId: 'E-1042', employeeName: 'Alice Johnson', submittedAt: '2026-03-15T09:23:14Z' } },
  { step: 2, icon: '🔍', title: 'VLM Extraction', description: 'Receipt parsed using Gemini 1.5 Pro', timestamp: '2026-03-15T09:23:15Z', latencyMs: 1240, payload: { model: 'gemini-1.5-pro', confidence: 0.97, extractedFields: { merchant: 'Dishoom', amount: 57.0, currency: 'GBP', date: '2026-03-14', items: [{ name: 'Lamb Raan', qty: 1, price: 24.5 }, { name: 'Black Daal', qty: 1, price: 12.5 }, { name: 'Naan Bread', qty: 2, price: 7.0 }, { name: 'Service Charge', qty: 1, price: 13.0 }] } } },
  { step: 3, icon: '🏢', title: 'Entity Resolution', description: 'Merchant resolved to canonical vendor', timestamp: '2026-03-15T09:23:15Z', latencyMs: 180, payload: { rawMerchant: 'DISHOOM KINGS CROSS', canonicalVendor: 'Dishoom', vendorId: 'V-0847', matchMethod: 'fuzzy', confidence: 0.94 } },
  { step: 4, icon: '📊', title: 'Policy Traversal', description: 'Graph traversal to find applicable rule', timestamp: '2026-03-15T09:23:16Z', latencyMs: 320, payload: { cypherQuery: "MATCH (e:Employee {id:'E-1042'})-[:HAS_ROLE]->(r:Role)-[:SUBJECT_TO]->(p:PolicyRule)-[:APPLIES_TO]->(c:Category {name:'Meals'}) RETURN p", path: 'Employee(E-1042) → Role(Senior Analyst) → PolicyRule(MEAL-UK-002)', matchedRule: 'MEAL-UK-002', limit: 45.0 } },
  { step: 5, icon: '✅', title: 'Auditor Verdict', description: 'Contextual Auditor analysis', timestamp: '2026-03-15T09:23:17Z', latencyMs: 890, payload: { model: 'gpt-4o-mini', verdict: 'FAIL', confidence: 0.88, reasoning: 'Expense of £57.00 exceeds the daily meal limit of £45.00 for Senior Analysts (MEAL-UK-002). Overage: £12.00. No pre-approved exemption on file.', citedRule: 'MEAL-UK-002' } },
  { step: 6, icon: '🔎', title: 'Fraud Score', description: 'Fraud detection analysis', timestamp: '2026-03-15T09:23:18Z', latencyMs: 450, payload: { fraudScore: 0.12, flags: [], duplicateCheck: { isDuplicate: false, nearestMatch: null }, velocityCheck: { isAnomaly: false, dailyCount: 1 }, model: 'fraud-detector-v2' } },
  { step: 7, icon: '⚖️', title: 'Compliance Decision', description: 'Final compliance review', timestamp: '2026-03-15T09:23:19Z', latencyMs: 670, payload: { model: 'claude-3.5-sonnet', decision: 'NEEDS_REMEDIATION', reasoning: 'The expense exceeds policy limits but shows no fraud indicators. Recommend negotiation flow to verify if a client meeting exemption applies before final rejection.', confidence: 0.91 } },
  { step: 8, icon: '📝', title: 'Final Decision', description: 'Routed to negotiation', timestamp: '2026-03-15T09:23:19Z', latencyMs: 50, payload: { finalDecision: 'NEEDS_REMEDIATION', totalLatencyMs: 3800, routedTo: 'negotiation-agent' } },
];

export const sampleChat: ChatMessage[] = [
  { id: '1', sender: 'agent', message: 'Your meal expense of £57 at Dishoom exceeds the £45 daily limit for Senior Analysts by £12. Policy MEAL-UK-002 allows exemptions for client meetings. Can you provide the client name and company?', timestamp: '2026-03-15T10:00:00Z', type: 'text' },
  { id: '2', sender: 'employee', message: 'This was a lunch meeting with Jane Doe from Acme Corp to discuss Q2 partnership renewal.', timestamp: '2026-03-15T10:05:00Z', type: 'text' },
  { id: '3', sender: 'agent', message: 'Thank you. Validating against CRM records...', timestamp: '2026-03-15T10:05:30Z', type: 'text' },
  { id: '4', sender: 'agent', message: '', timestamp: '2026-03-15T10:06:00Z', type: 'validation', validationResult: { success: true, detail: 'Client "Jane Doe, Acme Corp" confirmed in Salesforce. Active account, last interaction: 2026-03-10.' } },
  { id: '5', sender: 'agent', message: 'CRM validation successful. Your expense has been approved under the client meeting exemption. Policy override applied: MEAL-UK-002 → CLIENT-MEETING-EXEMPT.', timestamp: '2026-03-15T10:06:30Z', type: 'text' },
];

export const departmentSpend = [
  { name: 'Engineering', value: 45200, fill: 'hsl(239, 84%, 67%)' },
  { name: 'Sales', value: 38700, fill: 'hsl(270, 70%, 60%)' },
  { name: 'Marketing', value: 28400, fill: 'hsl(200, 80%, 55%)' },
  { name: 'Finance', value: 15800, fill: 'hsl(160, 84%, 39%)' },
  { name: 'HR', value: 12300, fill: 'hsl(38, 92%, 50%)' },
];

export const categorySpend = [
  { category: 'Meals', amount: 42350 },
  { category: 'Transport', amount: 31200 },
  { category: 'Accommodation', amount: 28900 },
  { category: 'Office Supplies', amount: 15600 },
  { category: 'Client Entertainment', amount: 22400 },
];

export const approvalTrend = Array.from({ length: 30 }, (_, i) => ({
  day: `Mar ${i + 1}`,
  rate: parseFloat((68 + Math.random() * 14).toFixed(1)),
}));
