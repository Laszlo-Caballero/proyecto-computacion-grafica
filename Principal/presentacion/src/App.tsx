import { Route, Routes } from "react-router-dom";
import Landing from "./pages/Landing";
import Nav from "./components/nav/Nav";

function App() {
  return (
    <main className="w-full h-screen flex-1 flex flex-col bg-black-950 text-white">
      <Nav />
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/descargar" element={<div>descargar</div>} />
        <Route path="/preview" element={<div>preview</div>} />
        <Route path="/*" element={<div>404</div>} />
      </Routes>
    </main>
  );
}

export default App;
