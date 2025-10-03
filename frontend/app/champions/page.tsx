import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { getChampions, type ChampionSummary } from "../lib/api";

export default function ChampionsPage() {
  const [champs, setChamps] = useState<ChampionSummary[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    getChampions()
      .then(setChamps)
      .catch((e) => {
        console.error(e);
        setError("Failed to load champions.");
      })
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="loading">Loading champions...</div>;
  if (error) return <div className="error">{error}</div>;

  return (
    <main className="champions-page">
      <h1>Champions</h1>
      <div className="grid">
        {champs.map((c) => (
          <Link key={c.id} to={`/champions/${c.id}`} className="champion-link">
            <article className="champion-card">
              <h3 className="champion-name">{c.name}</h3>
              <span className="champion-region">
                {c.region ?? "Unknown region"}
              </span>
            </article>
          </Link>
        ))}
      </div>
    </main>
  );
}
