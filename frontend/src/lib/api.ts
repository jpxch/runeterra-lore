const API_BASE = import.meta.env.VITE_API_BASE || "http://127.0.0.1:8000/api";

export interface ChampionSummary {
    id: string;
    name: string;
    region: string;
    icon?: string | null;
}

export interface ChampionDetail extends ChampionSummary {
    lore: string;
    abilities: { Q: string; W: string; E: string; R: string };
    skins: string[];
}

export async function fetchChampions(): Promise<ChampionSummary[]> {
    const res = await fetch(`${API_BASE}/champions`);
    if (!res.ok) throw new Error("Failed to load champions");
    return res.json();
}

export async function fetchChampion(id: string): Promise<ChampionDetail> {
    const res = await fetch(`${API_BASE}/${id}`);
    if (!res.ok) throw new Error("Champion not found");
    return res.json();
}