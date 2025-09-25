type Props = {
  skins: string[];
};

export default function ChampionSkins({ skins }: Props) {
  if (!skins || skins.length === 0) {
    return <p>No skins available</p>;
  }

  return (
    <section style={{ marginBottom: 20 }}>
      <h3>Skins</h3>
      <ul>
        {skins.map((skin, idx) => (
          <li key={idx}>{skin}</li>
        ))}
      </ul>
    </section>
  );
}
