export interface ChampionSummary {
    id: string;
    name: string;
    title: string;
    region?: string;
    roles: string[];
}

export interface ChampionDetail extends ChampionSummary {
    lore?: string;
    abilities?: string[];
    skins?: string[];
}

export async function getChampions(): Promise<ChampionSummary[]> {
    const res = await fetch("/api/champions");
    if (!res.ok) throw new Error("Failed to fetch champions");
    return res.json();
}