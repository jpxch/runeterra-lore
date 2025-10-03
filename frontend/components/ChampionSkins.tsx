type Props = {
  skins: { id: string; name: string; imageUrl?: string }[];
};

export default function ChampionSkins({ skins }: Props) {
  return (
    <div className="skins-list">
      {skins.map((s) => (
        <article key={s.id} className="skin-card">
          {s.imageUrl && (
            <img src={s.imageUrl} alt={s.name} className="skin-image" />
          )}
          <p className="skin-name">{s.name}</p>
        </article>
      ))}
    </div>
  );
}
