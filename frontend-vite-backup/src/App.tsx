import { Routes, Route } from "react-router-dom";
import ChampionsPage from "./pages/champions";
import ChampionDetailPage from "./pages/ChampionDetail";

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<ChampionsPage />} />
      <Route path="/champions/:id" element={<ChampionDetailPage />} />
    </Routes>
  );
}
