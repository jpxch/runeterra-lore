import type { ChampionDetail } from "../lib/api";

export default function ChampionSkins({
  skins,
}: {
  skins: ChampionDetail["skins"];
}) {
  return (
    <section>
      <h2>Skins</h2>
      <div style={{ display: "flex", gap: 16, flexWrap: "wrap" }}>
        {skins.map((s) => (
          <article key={s.id} style={{ width: 200 }}>
            {s.splash ? (
              <img
                src={s.splash}
                alt={s.name}
                style={{ width: "100%", borderRadius: 8 }}
              />
            ) : (
              <div style={{ width: "100%", height: 120, background: "#222" }} />
            )}
            <p style={{ marginTop: 8 }}>{s.name}</p>
          </article>
        ))}
      </div>
    </section>
  );
}
