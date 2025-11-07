import React from "react";
import { toast } from "sonner";
import { Button } from "./ui/button";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "./ui/card";
import { Loader2, Download, Mail } from "lucide-react";
import { Form, FormField, FormItem, FormLabel, FormControl, FormMessage } from "./ui/form";
import { Input } from "./ui/input";
import { useForm } from "react-hook-form";

export interface MonthYearForm {
  month: number;
  year: number;
}

const CreateSendCsvCard: React.FC = () => {
  const [creating, setCreating] = React.useState(false);
  const [sending, setSending] = React.useState(false);
  const form = useForm<MonthYearForm>({
    defaultValues: { month: 1, year: new Date().getFullYear() },
    mode: "onSubmit",
  });

  const handleCreateCSV = async (values: MonthYearForm) => {
    setCreating(true);
    try {
      const username = sessionStorage.getItem("username") || "unknown";
      const idempotencyKey = username + JSON.stringify(values);
      const response = await fetch("http://localhost:5050/api/employee/createAggregatedEmployeeData", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Idempotency-Key": idempotencyKey,
          Authorization: `Bearer ${sessionStorage.getItem("token")}`,
        },
        body: JSON.stringify(values),
      });
      if (!response.ok) {
        let errorText = "Could not create CSV.";
        try {
          const errorBody = await response.text();
          errorText += `\nBackend response: ${errorBody}`;
        } catch {}
  toast.error("Error", { description: errorText });
        return;
      }
      const blob = await response.blob();
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `employee_report_${values.month}_${values.year}.csv`;
      document.body.appendChild(a);
      a.click();
      a.remove();
      URL.revokeObjectURL(url);
  toast.success("CSV Created", { description: "Aggregated employee data CSV downloaded." });
    } catch {
  toast.error("Error", { description: "Network error." });
    } finally {
      setCreating(false);
    }
  };

  const handleSendMail = async (values: MonthYearForm) => {
    setSending(true);
    try {
      const username = sessionStorage.getItem("username") || "unknown";
      const idempotencyKey = username + JSON.stringify(values);
      const response = await fetch("http://localhost:5050/api/mail/sendAggregatedEmployeeData", {
        method: "POST",
        headers: {
          "Idempotency-Key": idempotencyKey,
          "Content-Type": "application/json",
          Authorization: `Bearer ${sessionStorage.getItem("token")}`,
        },
        body: JSON.stringify(values),
      });
      if (!response.ok) {
  toast.error("Error", { description: "Could not send email." });
        return;
      }
  toast.success("Email Sent", { description: "CSV sent by email successfully." });
    } catch {
  toast.error("Error", { description: "Network error." });
    } finally {
      setSending(false);
    }
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-xl font-bold">Aggregated Data CSV</CardTitle>
        <CardDescription>
          Create and send a CSV with aggregated employee data
        </CardDescription>
      </CardHeader>
      <CardContent>
        <Form {...form}>
          <form className="space-y-4" onSubmit={form.handleSubmit(handleCreateCSV)}>
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
              <Button type="submit" variant="outline" disabled={creating}>
                {creating ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Creating CSV…
                  </>
                ) : (
                  <>
                    <Download className="mr-2 h-4 w-4" />
                    Create CSV
                  </>
                )}
              </Button>
              <Button
                type="button"
                onClick={form.handleSubmit(handleSendMail)}
                disabled={sending}
              >
                {sending ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Sending…
                  </>
                ) : (
                  <>
                    <Mail className="mr-2 h-4 w-4" />
                    Send Mail
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

export default CreateSendCsvCard;
