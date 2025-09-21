const API_BASE = import.meta.env.VITE_API_BASE || "http://127.0.0.1:8000/api";

export interface Region {
    id: string;
    name: string;
    icon?: string | null;
    description?: string;
}

export interface Skin {
    id: string;
    championId: string;
    name: string;
    splash?: string | null;
}

export interface Relationships {
    allies: string[];
    rivals: string[];
}

export interface ChampionSummary {
    id: string;
    name: string;
    region: string;
    icon?: string | null;
}

export interface ChampionDetail {
    id: string;
    name: string;
    region: Region;
    icon?: string | null;
    lore: string;
    abilities: { Q: string; W: string; E: string; R: string };
    skins: Skin[];
    relationships: Relationships;
}

export async function fetchChampions(): Promise<ChampionSummary[]> {
    const res = await fetch(`${API_BASE}/champions`);
    if (!res.ok) throw new Error("Failed to load champions");
    return res.json();
}

export async function fetchChampion(id: string): Promise<ChampionDetail> {
    const res = await fetch(`${API_BASE}/champions/${id}`);
    if (!res.ok) throw new Error("Champion not found");
    return res.json();
}