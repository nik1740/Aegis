const BASE_URL = 'http://localhost:8000/api/v1';

async function fetchApi<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE_URL}${endpoint}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  });
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json();
}

export const api = {
  getExpenses: (params?: Record<string, string>) => {
    const qs = params ? '?' + new URLSearchParams(params).toString() : '';
    return fetchApi(`/expenses${qs}`);
  },
  getExpense: (id: string) => fetchApi(`/expenses/${id}`),
  submitExpense: (data: FormData) => fetchApi('/expenses', { method: 'POST', body: data }),
  getAuditTrail: (expenseId: string) => fetchApi(`/expenses/${expenseId}/audit`),
  getNegotiation: (expenseId: string) => fetchApi(`/expenses/${expenseId}/negotiation`),
  sendNegotiationMessage: (expenseId: string, message: string) =>
    fetchApi(`/expenses/${expenseId}/negotiation`, { method: 'POST', body: JSON.stringify({ message }) }),
  getPolicies: () => fetchApi('/policies'),
  getDashboardStats: () => fetchApi('/dashboard/stats'),
};
