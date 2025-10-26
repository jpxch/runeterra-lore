// frontend/lib/api.ts
const API_BASE =
    process.env.NEXT_PUBLIC_API_BASE || "http://127.0.0.1:8000";

async function fetchJSON<T>(url: string): Promise<T> {
    const res = await fetch(url);
    if (!res.ok) {
        throw new Error(`Request failed: ${res.status} ${res.statusText}`);
    }
    return res.json();
}

// Get all champions
export const getChampions = () =>
    fetchJSON(`${API_BASE}/api/champions`);

// Get one champion
export const getChampion = (id: string) =>
    fetchJSON(`${API_BASE}/api/champions/${id}`);

export const getRegions = () =>
    fetchJSON(`${API_BASE}/api/regions`);

export const getSkins = () =>
    fetchJSON(`${API_BASE}/api/skins`);