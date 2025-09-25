import { useEffect, useState } from "react";

interface Champion {
  id: string;
  name: string;
  region: string;
}

export default function ChampionsPage() {
  const [champs, setChamps] = useState<Champion[]>([]);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/api/champions")
      .then((res) => res.json())
      .then((data: Champion[]) => setChamps(data));
  }, []);

  return (
    <div>
      <h1>Champions</h1>
      <ul>
        {champs.map((c) => (
          <li key={c.id}>
            {c.name} - {c.region}
          </li>
        ))}
      </ul>
    </div>
  );
}
