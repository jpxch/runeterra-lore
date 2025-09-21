import type { ChampionDetail } from "../lib/api";

export default function ChampionAbilities({
  abilities,
}: {
  abilities: ChampionDetail["abilities"];
}) {
  return (
    <section style={{ marginBottom: 20 }}>
      <h2>Abilities</h2>
      <ul>
        <li>
          <strong>Q:</strong> {abilities.Q}
        </li>
        <li>
          <strong>W:</strong> {abilities.W}
        </li>
        <li>
          <strong>E:</strong> {abilities.E}
        </li>
        <li>
          <strong>R:</strong> {abilities.R}
        </li>
      </ul>
    </section>
  );
}
