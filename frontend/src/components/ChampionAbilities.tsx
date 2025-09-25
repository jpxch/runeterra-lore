type Props = {
  abilities: string[];
};

export default function ChampionAbilities({ abilities }: Props) {
  if (!abilities || abilities.length === 0) {
    return <p>No abilities available</p>;
  }

  return (
    <section style={{ marginBottom: 20 }}>
      <h3>Abilities</h3>
      <ul>
        {abilities.map((ability, idx) => (
          <li key={idx}>{ability}</li>
        ))}
      </ul>
    </section>
  );
}
