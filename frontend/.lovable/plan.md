

# Aegis Finance Dashboard — Implementation Plan

## Overview
A corporate expense management dashboard with AI-powered audit decisions, dark premium theme with glassmorphism, and 6 main pages. All data is mocked; API service stubs point to a FastAPI backend.

## Design System
- Dark slate background (#0F172A → #1E293B), glassmorphism cards with blur + white/10% borders
- Indigo/violet primary gradient, emerald/red/amber status colors
- Inter font, fade-in page transitions, hover scale effects on cards

## Sidebar Navigation
Collapsible sidebar with Aegis branding, nav links to all 6 pages, audit trail search input, settings placeholder, and live system status indicators (Gateway/Agents/Neo4j).

## Pages

### 1. Dashboard (`/`)
- 4 KPI cards (submissions, auto-approved %, fraud flags, avg processing time)
- Bar chart: Spend by Category (Recharts)
- Line chart: 30-day Approval Rate Trend
- Donut chart: Department Spend breakdown
- Recent Decisions table (last 10 expenses with colored status badges)

### 2. Expense Review (`/expenses`)
- Filter bar: status, category, date range, employee search
- Data table with fraud score color indicators
- Row click opens slide-over panel with receipt details, AI agent verdicts (Auditor, Fraud Detective, Compliance Judge), policy rule applied, and action buttons

### 3. Policy Explorer (`/policies`)
- Left sidebar: tree of policy rules grouped by category
- Main area: selected rule details (ID, description, limits, roles, locations)
- Visual relationship diagram showing roles → rules → categories

### 4. Audit Trail (`/audit/:expenseId`)
- Expense header with final decision badge
- Vertical timeline stepper (8 steps: Submitted → VLM Extraction → Entity Resolution → Policy Traversal → Auditor → Fraud Score → Compliance → Final Decision)
- Each step expandable to show full JSON payload, latency in ms on the right

### 5. Negotiation Chat (`/negotiations/:expenseId`)
- Left panel: expense summary card
- Right panel: chat UI with agent/employee messages, status badges, CRM validation inline cards, round counter
- Input field for simulating employee responses
- Pre-populated sample conversation

### 6. Submit Expense (`/submit`)
- Drag & drop file upload with preview
- Form: Employee ID, justification, category, auto-generated idempotency key
- Submit with loading state → success toast
- AI Processing animation (Extracting → Analyzing → Auditing → Decision)

## Infrastructure
- Mock data module with realistic British pound amounts, employee names, merchants, EXP-2026-XXXXX IDs
- API service stubs pointing to `localhost:8000/api/v1/`
- Skeleton loaders for loading states
- "Glass box: Every decision is fully traceable" badge

