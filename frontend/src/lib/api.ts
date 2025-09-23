export interface ChampionSummary {
    id: string;
    name: string;
    title: string;
    region?: string;
    roles: string[];
}

export interface ChampionDetail {
    id: string;
    name: string;
    title: string;
    region?: string;
    lore: string;
    abilities?: string[];
    skins?: string[];
}

const API_URL = import.meta.env.VITE_API_URL ?? "/api";

async function request<T>(path: string): Promise<T> {
    const res = await fetch(`${API_URL}${path}`);
    if (!res.ok) {
        throw new Error(`API request failed: ${res.status} ${res.statusText}`);
    }
    return res.json() as Promise<T>;
}

export async function getChampions(): Promise<ChampionSummary[]> {
    return request<ChampionSummary[]>("/champions");
}

export async function getChampion(id: string): Promise<ChampionDetail> {
    return request<ChampionDetail>(`/champions/${id}`);
}