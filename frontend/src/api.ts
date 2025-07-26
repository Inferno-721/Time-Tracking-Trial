export async function createEmployee(data: { email: string; name: string; password: string }) {
    const res = await fetch("/api/employees/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
    if (!res.ok) throw new Error("Failed to create employee");
    return res.json();
  }
  