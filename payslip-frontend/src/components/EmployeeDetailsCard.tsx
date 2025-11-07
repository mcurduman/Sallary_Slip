import React, { useEffect, useState } from "react";
import { Card, CardHeader, CardTitle, CardContent, CardDescription } from "./ui/card";

export interface EmployeeDetails {
  email: string;
  fullName: string;
  discipline?: string;
  position?: string;
}

interface EmployeeDetailsCardProps {
  token: string;
}

const EmployeeDetailsCard: React.FC<EmployeeDetailsCardProps> = ({ token }) => {
  const [details, setDetails] = useState<EmployeeDetails | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchDetails = async () => {
      setLoading(true);
      setError(null);
      try {
        const response = await fetch("http://localhost:5050/api/employee/getMyDetails", {
          method: "GET",
          headers: {
            "Idempotency-Key": `${token}-getMyDetails`,
            Authorization: `Bearer ${token}`,
          },
        });
        if (response.ok) {
          const data = await response.json();
          setDetails(data);
        } else {
          const err = await response.json();
          setError(err.detail || "Could not fetch details.");
        }
      } catch {
        setError("Network error.");
      } finally {
        setLoading(false);
      }
    };
    if (token) fetchDetails();
  }, [token]);

  return (
    <Card className="border-2 border-border">
      <CardHeader>
        <CardTitle className="text-xl font-bold">Your Details</CardTitle>
        <CardDescription>Your personal information</CardDescription>
      </CardHeader>
      <CardContent>
        {loading && <div>Loading...</div>}
        {error && <div className="text-red-500">{error}</div>}
        {details && (
          <div className="space-y-2">
            <div><span className="font-semibold">Full Name:</span> {details.fullName}</div>
            <div><span className="font-semibold">Email:</span> {details.email}</div>
            <div><span className="font-semibold">Discipline:</span> {details.discipline || "-"}</div>
            <div><span className="font-semibold">Position:</span> {details.position || "-"}</div>
          </div>
        )}
      </CardContent>
    </Card>
  );
};

export default EmployeeDetailsCard;
