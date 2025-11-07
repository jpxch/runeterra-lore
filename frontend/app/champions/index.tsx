// frontend/app/champions/index.tsx
import Link from "next/link";
import Image from "next/image";
import { getChampions } from "@/lib/api";

interface Champion {
    id: string;
    name: string;
    title?: string;
    icon?: string;
    tags?: string[];
}

export default async function ChampionsPage() {
    const champions: Champion[] =await getChampions();

    return (
        <main className="fsl-surface champions-page">
            <header className="page-header">
                <h1 className="page-title glow-text">Champions</h1>
            </header>
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
