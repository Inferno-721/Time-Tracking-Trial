import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Onboard from "./components/Onboard";
import Download from "./components/Download";

const App = () => (
  <BrowserRouter>
    <Routes>
      <Route path="/" element={<Onboard />} />
      <Route path="/download" element={<Download />} />
    </Routes>
  </BrowserRouter>
);

export default App;