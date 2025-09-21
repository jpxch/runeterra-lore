import React from "react";
import type { ChampionDetail } from "../lib/api";

interface Props {
  champion: ChampionDetail;
}

const ChampionAbilities: React.FC<Props> = ({ champion }) => {
  if (!champion.abilities || champion.abilities.length === 0) {
    return <p>No abilities available</p>;
  }

  return (
    <div>
      <h3>Abilities</h3>
      <ul>
        {champion.abilities.map((ability, idx) => (
          <li key={idx}>{ability}</li>
        ))}
      </ul>
    </div>
  );
};

export default ChampionAbilities;
