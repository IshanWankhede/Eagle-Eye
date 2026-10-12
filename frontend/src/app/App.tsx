import { useEffect, useState } from "react";
import { getHealth } from "../services/api";
import type { HealthResponse } from "../types/health";

// Scaffold only. Final visual design is intentionally undecided (see PROJECT_GUIDE.md).
export default function App() {
  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    getHealth().then(setHealth).catch((e: Error) => setError(e.message));
  }, []);

  return (
    <main className="p-6">
      <h1 className="text-2xl font-semibold">Eagle Eye - AI Vision for Cabinet QC</h1>
      <p className="mt-2">Scaffold only. Inspection features are not implemented yet.</p>
      <p className="mt-4">
        Backend: {error ? `unreachable (${error})` : health ? `${health.status} v${health.version}` : "checking..."}
      </p>
    </main>
  );
}
