import Link from "next/link";
import { getChampion } from "@/lib/api";
import ChampionAbilities from "@/components/ChampionAbilities";
import ChampionSkin from "@/components/ChampionSkins";

export default async function ChampionDetailPage({
    params,
}: {
    params: { id: string };
}) {
    const champion = await getChampion(params.id);

    if (!champion) {
        return <div className="error">Champion not found.</div>;
    }

    const abilities = Array.isArray(champion.abilities)
        ? champion.abilities
        : Object.entries(champion.abilities || {}).map(([id, name]) => ({ id, name }));

    return (
        <main className="champion-detail-page">
            <h1>{champion.name}</h1>
            <p>{champion.lore}</p>

            <section className="abilities-section">
                <h2 className="section-title">Abilities</h2>
                <ChampionAbilities abilities={champion.abilities ?? []} />
            </section>

            <section className="skins-section">
                <h2 className="section-title">Skins</h2>
                <ChampionSkins skins={champion.skins ?? []} />
            </section>

            <Link href="/champions" className="back-link">
                ← Back to Champions
            </Link>
        </main>
    );
}
