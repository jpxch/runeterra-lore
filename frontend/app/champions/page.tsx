import Link from "next/link";
import { getChampions } from "@/lib/api";

export default async function ChampionsPage() {
    const champions = await getChampions();

    return (
        <main className="champions-page">
            <h1>Champions</h1>
            <ul>
                {champions.map((c: any) => (
                    <li key={c.id}>
                        <Link href={`/champions/${c.id}`}>{c.name}</Link>
                    </li>
                ))}
            </ul>
        </main>
    );
}
