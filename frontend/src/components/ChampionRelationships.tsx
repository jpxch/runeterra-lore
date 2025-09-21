import type { ChampionDetail } from "../lib/api";

export default function ChampionDetail({
  relationships,
}: {
  relationships: ChampionDetail["relationships"];
}) {
  return (
    <section style={{ marginTop: 20 }}>
      <h2>Relationships</h2>
      <div style={{ display: "flex", gap: 40 }}>
        <div>
          <h3>Allies</h3>
          <ul>
            {relationships.allies.map((ally) => (
              <li key={ally}>{ally}</li>
            ))}
          </ul>
        </div>
        <div>
          <h3>Rivals</h3>
          <ul>
            {relationships.rivals.map((rival) => (
              <li key={rival}>{rival}</li>
            ))}
          </ul>
        </div>
      </div>
    </section>
  );
}
