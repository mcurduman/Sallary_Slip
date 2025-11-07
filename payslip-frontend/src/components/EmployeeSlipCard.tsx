import React from "react";
import { toast } from "sonner";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "./ui/card";
import { Loader2, Download, Mail } from "lucide-react";
import { Form, FormField, FormItem, FormLabel, FormControl, FormMessage } from "./ui/form";
import { Input } from "./ui/input";
import { useForm } from "react-hook-form";
import { Button } from "./ui/button";

export interface MonthYearForm {
  month: number;
  year: number;
}

const EmployeeSlipCard: React.FC = () => {
  const [creatingEmployeeSlip, setCreatingEmployeeSlip] = React.useState(false);
  const [sendingEmployeeSlip, setSendingEmployeeSlip] = React.useState(false);
  const form = useForm<MonthYearForm>({
    defaultValues: { month: 1, year: new Date().getFullYear() },
    mode: "onSubmit",
  });

  const handleGenerateEmployeeSlip = async (values: MonthYearForm) => {
    setCreatingEmployeeSlip(true);
    try {
      const username = sessionStorage.getItem("username") || "unknown";
      const response = await fetch("http://localhost:5050/api/payrollRecord/generatePayrollReportsForEmployees", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Idempotency-Key": `generatePayrollReportsForEmployees-${values.month}-${values.year}-${username}`,
          Authorization: `Bearer ${sessionStorage.getItem("token")}`,
        },
        body: JSON.stringify(values),
      });
      if (!response.ok) {
        const errorBody = await response.text();
  toast.error("Error", { description: `Could not generate payroll reports.\n${errorBody}` });
        return;
      }
  toast.success("Payroll Reports", { description: "Payroll reports generated successfully." });
    } catch {
  toast.error("Error", { description: "Network error." });
    } finally {
      setCreatingEmployeeSlip(false);
    }
  };

  const handleSendEmployeeSlips = async (values: MonthYearForm) => {
    setSendingEmployeeSlip(true);
    try {

      const response = await fetch("http://localhost:5050/api/mail/sendPayslips", {
        method: "POST",
        headers: {
          "Idempotency-Key": `sendPayslips-${values.month}-${values.year}`,
          "Content-Type": "application/json",
          Authorization: `Bearer ${sessionStorage.getItem("token")}`,
        },
        body: JSON.stringify(values),
      });
      if (!response.ok) {
        const errorBody = await response.text();
  toast.error("Error", { description: `Could not send payslips.\n${errorBody}` });
        return;
      }
  toast.success("Payslips Sent", { description: "Payslips sent successfully." });
    } catch {
  toast.error("Error", { description: "Network error." });
    } finally {
      setSendingEmployeeSlip(false);
    }
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-xl font-bold">Employees Slip</CardTitle>
        <CardDescription>
          Generate and send individual employee slips
        </CardDescription>
      </CardHeader>
      <CardContent>
        <Form {...form}>
          <form className="space-y-4" onSubmit={form.handleSubmit(handleGenerateEmployeeSlip)}>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <FormField
                control={form.control}
                name="month"
                rules={{
                  required: "Month is required",
                  min: { value: 1, message: "Month must be between 1 and 12" },
                  max: { value: 12, message: "Month must be between 1 and 12" },
                }}
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Month</FormLabel>
                    <FormControl>
                      <Input
                        type="number"
                        min={1}
                        max={12}
                        inputMode="numeric"
                        {...field}
                        onChange={(e) => field.onChange(Number(e.target.value))}
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <FormField
                control={form.control}
                name="year"
                rules={{
                  required: "Year is required",
                  min: { value: 2000, message: "Year must be ≥ 2000" },
                  max: { value: 2100, message: "Year must be ≤ 2100" },
                }}
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Year</FormLabel>
                    <FormControl>
                      <Input
                        type="number"
                        min={2000}
                        max={new Date().getFullYear()}
                        inputMode="numeric"
                        {...field}
                        onChange={(e) => field.onChange(Number(e.target.value))}
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
            </div>
            <div className="flex flex-wrap gap-3">
              <Button type="submit" variant="outline" disabled={creatingEmployeeSlip}>
                {creatingEmployeeSlip ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Generating Slips…
                  </>
                ) : (
                  <>
                    <Download className="mr-2 h-4 w-4" />
                    Generate Slip
                  </>
                )}
              </Button>
              <Button
                type="button"
                onClick={form.handleSubmit(handleSendEmployeeSlips)}
                disabled={sendingEmployeeSlip}
              >
                {sendingEmployeeSlip ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Sending…
                  </>
                ) : (
                  <>
                    <Mail className="mr-2 h-4 w-4" />
                    Send Slip
                  </>
                )}
              </Button>
            </div>
          </form>
        </Form>
      </CardContent>
    </Card>
  );
};

export default EmployeeSlipCard;
