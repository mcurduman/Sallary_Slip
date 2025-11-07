import { useState, useEffect } from "react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { Routes, Route, useNavigate } from "react-router-dom";
import { Toaster } from 'sonner';   
import Index from "./pages/Index";
import Login from "./pages/Login";
import AdminDashboard from "./pages/ManagerDashboard";
import EmployeeDashboard from "./pages/EmployeeDashboard";
import NotFound from "./pages/NotFound";
import { TooltipProvider } from "./components/ui/tooltip";

const queryClient = new QueryClient();

const removeToken = () => {
  sessionStorage.removeItem("token");
};

const getRoles = () => {
  const token = sessionStorage.getItem("token");
  if (!token) return null;
  try {
    const payload = JSON.parse(atob(token.split(".")[1]));
    return payload.roles;
  } catch {
    return null;
  }
};

const App = () => {
  const [roles, setRoles] = useState<string[] | null>(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();
  const handleLogout = () => {
    removeToken();
    navigate("/login", { replace: true });
  };

  // Callback to update roles after login
  const handleLoginSuccess = () => {
    const foundRoles = getRoles();
    setRoles(foundRoles);
    navigate("/dashboard", { replace: true });
  };

  // Session timeout: 30 minutes
  useEffect(() => {
    setLoading(true);
    const foundRoles = getRoles();
    setRoles(foundRoles);
    console.log("User roles set to:", foundRoles);
    setLoading(false);

    // Set up session timeout for 30 minutes (1800000 ms)
    const timeout = setTimeout(() => {
      removeToken();
      navigate("/login", { replace: true });
  globalThis.location.reload();
    }, 1800000);

    return () => clearTimeout(timeout);
  }, []);

  let dashboardElement;
  if (loading) {
    dashboardElement = <div className="flex items-center justify-center h-screen"><span>Loading...</span></div>;
  } else if (roles?.includes("MANAGER")) {
    dashboardElement = <AdminDashboard handleLogout={handleLogout} />;
  } else if (roles?.includes("EMPLOYEE")) {
    dashboardElement = <EmployeeDashboard handleLogout={handleLogout} />;
  } else {
    dashboardElement = <NotFound />;
  }

  return (
    <QueryClientProvider client={queryClient}>
      <TooltipProvider>
        <Toaster richColors theme="system" />
        <Routes>
          <Route path="/" element={<Index />} />
          <Route path="/login" element={<Login onLoginSuccess={handleLoginSuccess} />} />
          <Route path="/dashboard" element={dashboardElement} />
          <Route path="*" element={<NotFound />} />
        </Routes>
      </TooltipProvider>
    </QueryClientProvider>
  );
};

export default App;
