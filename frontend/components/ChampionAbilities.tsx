type Ability = {
    id: string;
    name: string;
    description: string;
    icon: string;
    cooldown?: string | number[];
    cost?: string | number[];
    range?: string | number[];
};

export default function ChampionAbilities({
    abilities,
}: {
    abilities: Ability[];
}) {
    if (!abilities.length) {
        return <p>No abilities available.</p>;
    }

    return (
        <section className="champion-abilities">
            {abilities.map((ability) => (
                <article key={ability.id} className="ability-card">
                    <header className="ability-header">
                        <img
                            src={ability.icon}
                            alt={`${ability.name} icon`}
                            className="ability-icon"
                        />
                        <h3 className="ability-name">{ability.name}</h3>
                    </header>

                    <p
                        className="ability-description"
                        dangerouslySetInnerHTML={{
                            __html: ability.description,
                        }}
                    />

                    <ul className="ability-stats">
                        {ability.cooldown && (
                            <li>
                                <strong>Cooldown:</strong>{" "}
                                {Array.isArray(ability.cooldown)
                                    ? ability.cooldown.join(" / ")
                                    : ability.cooldown}
                            </li>
                        )}
                        {ability.cost && (
                            <li>
                                <strong>Cost:</strong>{" "}
                                {Array.isArray(ability.cost)
                                    ? ability.cost.join(" / ")
                                    : ability.cost}
                            </li>
                        )}
                        {ability.range && (
                            <li>
                                <strong>Range:</strong>{" "}
                                {Array.isArray(ability.range)
                                    ? ability.range.join(" / ")
                                    : ability.range}
                            </li>
                        )}
                    </ul>
                </article>
            ))}
        </section>
    );
}
