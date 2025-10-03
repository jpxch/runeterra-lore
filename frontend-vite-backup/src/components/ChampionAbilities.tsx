type Props = {
  abilities: { id: string; name: string; description: string }[];
};

export default function ChampionAbilities({ abilities }: Props) {
  return (
    <div className="abilities-list">
      {abilities.map((a) => (
        <article key={a.id} className="ability-card">
          <h3 className="ability-name">{a.name}</h3>
          <p className="ability-desc">{a.description}</p>
        </article>
      ))}
    </div>
  );
}
