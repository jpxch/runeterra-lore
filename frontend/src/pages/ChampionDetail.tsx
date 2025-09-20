import { useParams, Link } from "react-router-dom";
import { useEffect, useState } from "react";
import { fetchChampion, type ChampionDetail } from "../lib/api";

export default function ChampionDetailPage() {
  const { id } = useParams<{ id: string }>();
  const [champ, setChamp] = useState<ChampionDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!id) return;
    fetchChampion(id)
      .then(setChamp)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, [id]);

  if (loading) return <div style={{ padding: 24 }}>Loading champion_</div>;
  if (error)
    return <div style={{ padding: 24, color: "red" }}>Error: {error}</div>;
  if (!champ) return <div style={{ padding: 24 }}>No champion found.</div>;

  return (
    <main style={{ padding: 24, maxWidth: 800, margin: "0 auto" }}>
      <Link to="/" style={{ display: "inline-block", marginBottom: 16 }}>
        &larr; Back
      </Link>

      <h1 style={{ marginBottom: 4 }}>{champ.name}</h1>
      <p style={{ opacity: 0.8, marginBottom: 16 }}>{champ.region}</p>

      <section style={{ marginBottom: 20 }}>
        <h2>Lore</h2>
        <p>{champ.lore}</p>
      </section>

      <section style={{ marginBottom: 20 }}>
        <h2>Abilities</h2>
        <ul>
          <li>
            <strong>Q:</strong> {champ.abilities.Q}
          </li>
          <li>
            <strong>W:</strong> {champ.abilities.W}
          </li>
          <li>
            <strong>E:</strong> {champ.abilities.E}
          </li>
          <li>
            <strong>R:</strong> {champ.abilities.R}
          </li>
        </ul>
      </section>

      <section>
        <h2>Skins</h2>
        <ul>
          {champ.skins.map((s) => (
            <li key={s}>{s}</li>
          ))}
        </ul>
      </section>
    </main>
  );
}
