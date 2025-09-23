import { useParams, Link } from "react-router-dom";
import { useEffect, useState } from "react";
import { getChampion, type ChampionDetail } from "../lib/api";
import ChampionAbilities from "../components/ChampionAbilities";
import ChampionSkins from "../components/ChampionSkins";

export default function ChampionDetailPage() {
  const { id } = useParams<{ id: string }>();
  const [champ, setChamp] = useState<ChampionDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!id) return;
    getChampion(id)
      .then(setChamp)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, [id]);

  if (loading) return <div style={{ padding: 24 }}>Loading champion...</div>;
  if (error) return <div style={{ padding: 24, color: "red" }}>Error: {error}</div>;
  if (!champ) return <div style={{ padding: 24 }}>No champion found.</div>;

  return (
    <main style={{ padding: 24, maxWidth: 800, margin: "0 auto" }}>
      <Link to="/" style={{ display: "inline-block", marginBottom: 16 }}>
        &larr; Back
      </Link>

      <h1>{champ.name}</h1>
      <p style={{ opacity: 0.8 }}>{champ.region ?? "Unknown region"}</p>

      <section style={{ marginBottom: 20 }}>
        <h2>Lore</h2>
        <p>{champ.lore}</p>
      </section>

      {champ.abilities && <ChampionAbilities abilities={champ.abilities} />}
      {champ.skins && <ChampionSkins skins={champ.skins} />}
    </main>
  );
}
