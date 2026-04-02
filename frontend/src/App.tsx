import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { Toaster } from "@/components/ui/toaster";
import { TooltipProvider } from "@/components/ui/tooltip";
import AppLayout from "@/components/AppLayout";
import Dashboard from "@/pages/Dashboard";
import ExpenseReview from "@/pages/ExpenseReview";
import PolicyExplorer from "@/pages/PolicyExplorer";
import AuditTrail from "@/pages/AuditTrail";
import NegotiationChat from "@/pages/NegotiationChat";
import SubmitExpense from "@/pages/SubmitExpense";
import NotFound from "@/pages/NotFound";

const queryClient = new QueryClient();

const App = () => (
  <QueryClientProvider client={queryClient}>
    <TooltipProvider>
      <Toaster />
      <Sonner />
      <BrowserRouter>
        <Routes>
          <Route element={<AppLayout />}>
            <Route path="/" element={<Dashboard />} />
            <Route path="/expenses" element={<ExpenseReview />} />
            <Route path="/policies" element={<PolicyExplorer />} />
            <Route path="/audit/:expenseId" element={<AuditTrail />} />
            <Route path="/negotiations/:expenseId" element={<NegotiationChat />} />
            <Route path="/submit" element={<SubmitExpense />} />
          </Route>
          <Route path="*" element={<NotFound />} />
        </Routes>
      </BrowserRouter>
    </TooltipProvider>
  </QueryClientProvider>
);

export default App;
