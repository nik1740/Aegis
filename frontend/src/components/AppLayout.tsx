import { Outlet } from 'react-router-dom';
import { AppSidebar } from '@/components/AppSidebar';

export default function AppLayout() {
  return (
    <div className="flex min-h-screen w-full gradient-bg">
      <AppSidebar />
      <main className="flex-1 overflow-auto">
        <div className="p-6 animate-fade-in">
          <Outlet />
        </div>
      </main>
    </div>
  );
}
