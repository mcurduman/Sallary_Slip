export async function sendEmployeeSlips(
  url: string,
  values: any,
  token?: string,
  idempotencyKey?: string
) {
  const response = await apiPost(url, values, token, idempotencyKey);
  return response;
}

export async function generateEmployeeSlip(
  url: string,
  values: any,
  token?: string,
  idempotencyKey?: string
) {
  const response = await apiPost(url, values, token, idempotencyKey);
  return response;
}
// src/utils/api.ts

export async function generateIdempotencyKey(username: string, payload: any): Promise<string> {
  const rawKey = `${username}-${JSON.stringify(payload)}`;
  const encoder = new TextEncoder();
  const data = encoder.encode(rawKey);
  const hashBuffer = await crypto.subtle.digest("SHA-256", data);
  return Array.from(new Uint8Array(hashBuffer)).map(b => b.toString(16).padStart(2, "0")).join("");
}

export async function apiPost(url: string, body: any, token?: string, idempotencyKey?: string) {
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
  };
  if (token) headers["Authorization"] = `Bearer ${token}`;
  if (idempotencyKey) headers["Idempotency-Key"] = idempotencyKey;
  const response = await fetch(url, {
    method: "POST",
    headers,
    body: JSON.stringify(body),
  });
  return response;
}

export async function apiGet(url: string, token?: string) {
  const headers: Record<string, string> = {};
  if (token) headers["Authorization"] = `Bearer ${token}`;
  const response = await fetch(url, {
    method: "GET",
    headers,
  });
  return response;
}
