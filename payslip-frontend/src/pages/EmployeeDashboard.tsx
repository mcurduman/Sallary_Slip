import { Button } from "@/components/ui/button";
import EmployeeDetailsCard from "@/components/EmployeeDetailsCard";
import { LogOut } from "lucide-react";
import PayrollRecordsTable from "@/components/PayrollRecordsTable";
import React from "react";
import { getUserEmail } from "@/utils/auth";

interface EmployeeDashboardProps {
  handleLogout: () => void; 
}

const EmployeeDashboard: React.FC<EmployeeDashboardProps> = ({ handleLogout }) => {
  // handleLogout is now received from props

  const token = sessionStorage.getItem("token") || "";

  return (
    <div className="min-h-screen bg-background">
      <header className="border-b-2 border-border bg-card">
        <div className="container mx-auto px-4 py-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold tracking-tight">Employee Dashboard</h1>
          <Button variant="outline" onClick={handleLogout} className="border-2">
            <LogOut className="mr-2 h-4 w-4" />
            Logout
          </Button>
        </div>
      </header>
      <main className="container mx-auto px-4 py-8 space-y-8">
        {/* My Info Section */}
        <EmployeeDetailsCard token={token} />
        {/* Payroll Slips Section */}
        <PayrollRecordsTable employeeEmail={getUserEmail()} token={token} />
      </main>
    </div>
  );
};

export default EmployeeDashboard;
