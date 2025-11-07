import React, { useEffect, useState } from "react";
import { Card, CardHeader, CardTitle, CardContent } from "./ui/card";
import { Table, TableHeader, TableRow, TableHead, TableBody, TableCell } from "./ui/table";

export interface PayrollRecord {
  run_date: string;
  payroll_month: number;
  payroll_year: number;
}

interface PayrollRecordsTableProps {
  employeeEmail: string;
  token: string;
}

const PayrollRecordsTable: React.FC<PayrollRecordsTableProps> = ({ employeeEmail, token }) => {

  const [records, setRecords] = useState<PayrollRecord[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    console.log("Fetching payroll records for:", employeeEmail);
    const fetchRecords = async () => {

      setLoading(true);
      try {
        const response = await fetch(
          `http://localhost:5050/api/payrollRecord/myRecords`,
          {
            method: "GET",
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );
        if (response.ok) {
          const data = await response.json();
          setRecords(data);
        } else {
          setRecords([]);
        }
      } catch {
        setRecords([]);
      } finally {
        setLoading(false);
      }
    };
    if (employeeEmail && token) fetchRecords();
  }, [employeeEmail, token]);

  return (
    <Card>
      <CardHeader>
        <CardTitle>My Payroll Slips</CardTitle>
      </CardHeader>
      <CardContent>
        {loading && <div>Loading...</div>}
        {!loading && records.length === 0 && <div>No payroll slips found.</div>}
        {!loading && records.length > 0 && (
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Month</TableHead>
                <TableHead>Year</TableHead>
                <TableHead>Run Date</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {records.map((rec) => {
                const monthNames = [
                  "January", "February", "March", "April", "May", "June",
                  "July", "August", "September", "October", "November", "December"
                ];
                const isCurrent =
                  rec.payroll_year === new Date().getFullYear() &&
                  rec.payroll_month === new Date().getMonth() + 1;
                const key = `${rec.payroll_year}-${rec.payroll_month}-${rec.run_date || Math.random()}`;
                let runDateDisplay = "-";
                if (rec.run_date) {
                  try {
                    runDateDisplay = new Date(rec.run_date).toLocaleDateString();
                  } catch {
                    runDateDisplay = String(rec.run_date);
                  }
                }
                return (
                  <TableRow key={key} style={isCurrent ? { backgroundColor: "#e6f7ff" } : {}}>
                    <TableCell>{monthNames[rec.payroll_month - 1] || rec.payroll_month}</TableCell>
                    <TableCell>{rec.payroll_year}</TableCell>
                    <TableCell>{runDateDisplay}</TableCell>
                  </TableRow>
                );
              })}
            </TableBody>
          </Table>
        )}
      </CardContent>
    </Card>
  );
};

export default PayrollRecordsTable;
