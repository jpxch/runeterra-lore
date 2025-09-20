import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { fetchChampions, type ChampionSummary } from "../lib/api";

export default function ChampionsPage() {
  const [champs, setChamps] = useState<ChampionSummary[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchChampions()
      .then(setChamps)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div style={{ padding: 24 }}>Loading...</div>;
  if (error)
    return <div style={{ padding: 24, color: "red" }}>Error: {error}</div>;

  return (
    <main style={{ padding: 24, maxWidth: 1000, margin: "0 auto" }}>
      <h1 style={{ marginBottom: 16 }}>Champions</h1>
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fill, minmax(220px, 1fr))",
          gap: 16,
        }}
      >
        {champs.map((c) => (
          <Link
            key={c.id}
            to={`/champions/${c.id}`}
            style={{ textDecoration: "none", color: "inherit" }}
          >
            <article
              style={{
                border: "1px solid #2a2a2a",
                borderRadius: 12,
                padding: 16,
                background: "#111",
              }}
            >
              {c.icon ? (
                <img
                  src={c.icon}
                  alt={c.name}
                  style={{
                    width: "100%",
                    height: 120,
                    objectFit: "cover",
                    borderRadius: 8,
                  }}
                />
              ) : (
                <div
                  style={{
                    width: "100%",
                    height: 120,
                    background: "#222",
                    borderRadius: 8,
                  }}
                />
              )}
              <h3 style={{ margin: "12px 0 4px" }}>{c.name}</h3>
              <span style={{ opacity: 0.8 }}>{c.region}</span>
            </article>
          </Link>
        ))}
      </div>
    </main>
  );
}
