type Skin = {
    id: string;
    num: number;
    name: string;
    chromas?: boolean;
    splash?: string;
    loading?: string;
    lore?: string;
};

export default function ChampionSkins({ skins }: { skins: Skin[] }) {
    if (!skins.length) {
        return <p>No skins available.</p>;
    }

    return (
        <section className="champion-skins">
            {skins.map((skin) => (
                <article key={skin.id} className="skin-card">
                    <h3 className="skin-name">{skin.name}</h3>
                    {skin.loading && (
                        <img
                            src={skin.splash}
                            alt={`${skin.name} splash art`}
                            className="skin-splash"
                        />
                    )}
                    {skin.lore && <p className="skin-lore">{skin.lore}</p>}
                    {skin.chromas && (
                        <p className="skin-chromas">Includes Chromas</p>
                    )}
                </article>
            ))}
        </section>
    );
}
