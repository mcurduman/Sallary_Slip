import React, { useEffect, useState } from "react";
import { toast } from "sonner";
import {
  Table,
  TableHeader,
  TableRow,
  TableHead,
  TableBody,
  TableCell,
} from "./ui/table";

type MyEmployeesTableProps = {
  token: string;
};

const MyEmployeesTable: React.FC<MyEmployeesTableProps> = ({ token }) => {
  const [employees, setEmployees] = useState<Array<{
    id?: string;
    email?: string;
    fullName?: string;
    full_name?: string;
    discipline?: string;
    position?: string;
  }>>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const fetchEmployees = async () => {
      setLoading(true);
      try {
        const username = sessionStorage.getItem("username") || "unknown";
        const response = await fetch("http://localhost:5050/api/employee/byManager", {
          method: "GET",
          headers: {
            "Idempotency-Key": `fetch-${username}-employees`,
            Authorization: `Bearer ${token}`,
          },
        });
        if (response.ok) {
          const data = await response.json();
          setEmployees(data);
        } else {
          toast.error("Error", { description: "Could not fetch employees." });
          setEmployees([]);
        }
      } catch {
        toast.error("Error", { description: "Network error." });
        setEmployees([]);
      } finally {
        setLoading(false);
      }
    };
    if (token) fetchEmployees();
  }, [token]);

  let tableRows;
  if (loading) {
    tableRows = (
      <TableRow>
        <TableCell colSpan={3} className="text-center">Loading…</TableCell>
      </TableRow>
    );
  } else if (employees.length === 0) {
    tableRows = (
      <TableRow>
        <TableCell colSpan={3} className="text-center">No employees found.</TableCell>
      </TableRow>
    );
  } else {
    tableRows = employees.map((emp) => (
      <TableRow key={emp.id || emp.email}>
        <TableCell className="font-medium">{emp.fullName || emp.full_name}</TableCell>
        <TableCell>{emp.discipline || '-'}</TableCell>
        <TableCell>{emp.position || '-'}</TableCell>
      </TableRow>
    ));
  }

  return (
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead className="font-bold">Employee Name</TableHead>
          <TableHead className="font-bold">Department</TableHead>
          <TableHead className="font-bold">Position</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {tableRows}
      </TableBody>
    </Table>
  );
};

export default MyEmployeesTable;
