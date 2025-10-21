// frontend/lib/api.ts
const API_BASE =
    process.env.NEXT_PUBLIC_API_BASE || "http://127.0.0.1:8000/api";

console.log(
    "Loaded API base from .env:",
    process.env.NEXT_PUBLIC_API_BASE || "(default to 127.0.0.1:8000/api)"
);

// Get all champions
export async function getChampions() {
    const res = await fetch(`${API_BASE}/champions`);
    if (!res.ok) throw new Error("Failed to fetch champions");
    return res.json();
}

// Get one champion
export async function getChampion(id: string) {
    const res = await fetch(`${API_BASE}/champions/${id}`);
    if (!res.ok) throw new Error(`Failed to fetch champion ${id}`);
    return res.json();
}