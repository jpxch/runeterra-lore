import React from "react";
import type { ChampionDetail } from "../lib/api";

interface Props {
  champion: ChampionDetail;
}

const ChampionSkins: React.FC<Props> = ({ champion }) => {
  if (!champion.skins || champion.skins.length === 0) {
    return <p>No skins available</p>;
  }

  return (
    <div>
      <h3>Skins</h3>
      <ul>
        {champion.skins.map((skin, idx) => (
          <li key={idx}>{skin}</li>
        ))}
      </ul>
    </div>
  );
};

export default ChampionSkins;
