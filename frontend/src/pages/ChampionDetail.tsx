import { useParams, Link } from "react-router-dom";
import { useEffect, useState } from "react";
import { getChampion, type ChampionDetail } from "../lib/api";
import ChampionAbilities from "../components/ChampionAbilities";
import ChampionSkins from "../components/ChampionSkins";

export default function ChampionDetailPage() {
  const { id } = useParams<{ id: string }>();
  const [champion, setChampion] = useState<ChampionDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!id) return;
    getChampion(id)
      .then(setChampion)
      .catch((e) => {
        console.error(e);
        setError("Failed to load champion.");
      })
      .finally(() => setLoading(false));
  }, [id]);

  if (loading) return <div className="loading">Loading champion...</div>;
  if (error) return <div className="error">{error}</div>;
  if (!champion) return <div className="error">Champion not found.</div>;

  return (
    <main className="champion-detail-page">
      <h1 className="champion-name">{champion.name}</h1>
      <p className="champion-lore">{champion.lore}</p>

      <section className="abiliies-section">
        <h2 className="section-title">Abilities</h2>
        <ChampionAbilities abilities={champion.abilities ?? []} />
      </section>

      <section className="skins-sectin">
        <h2 className="section-title">Skins</h2>
        <ChampionSkins skins={champion.skins ?? []} />
      </section>

      <Link to="/champions" className="back-link">
        &larr; Back to Champions
      </Link>
    </main>
  );
}
