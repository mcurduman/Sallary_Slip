import { LogOut } from "lucide-react";
import { Button } from "@/components/ui/button";
import CreateSendCsvCard from "@/components/CreateSendCsvCard";
import MyEmployeesTable from "@/components/MyEmployeesTable";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card";
import EmployeeSlipCard from "@/components/EmployeeSlipCard";
import EmployeeDetailsCard from "@/components/EmployeeDetailsCard";
import PayrollRecordsTable from "@/components/PayrollRecordsTable";
import { getUserEmail } from "@/utils/auth";
import React from "react";

interface ManagerDashboardProps {
  handleLogout: () => void;
}

const ManagerDashboard: React.FC<ManagerDashboardProps> = ({ handleLogout }) => {
  const token = sessionStorage.getItem("token") || "";
  const managerEmail = getUserEmail();

  return (
    <div className="min-h-screen bg-background">
      <header className="border-b bg-card">
        <div className="container mx-auto px-4 py-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold tracking-tight">Manager Dashboard</h1>
          <Button variant="outline" onClick={handleLogout}>
            <LogOut className="mr-2 h-4 w-4" />
            Logout
          </Button>
        </div>
      </header>

      <main className="container mx-auto px-4 py-8 space-y-8">
        {/* Manager Details at the top */}
        <EmployeeDetailsCard token={token} />

        <div className="flex flex-col md:flex-row gap-8">
          <div className="w-full md:w-1/2">
            <CreateSendCsvCard />
          </div>
          <div className="w-full md:w-1/2">
            <EmployeeSlipCard />
          </div>
        </div>

        {/* My Employees Section */}
        <Card>
          <CardHeader>
            <CardTitle className="text-xl font-bold">My Employees</CardTitle>
            <CardDescription>View and manage your employees</CardDescription>
          </CardHeader>
          <CardContent>
      <MyEmployeesTable token={token} />
          </CardContent>
        </Card>

        {/* Manager's Payroll Records at the end */}
        <PayrollRecordsTable employeeEmail={managerEmail} token={token} />
      </main>
    </div>
  );
};

export default ManagerDashboard;
