import Navbar from "./Components/Navbar";
import Home from "./Components/Home";
import StockDetail from "./Components/StockDetail";
import MutualFunds from "./Components/MutualFunds";
import Ipo from "./Components/Ipo";
import { BrowserRouter, Route, Routes } from "react-router-dom";
function App() {
  return (
    <>
      <BrowserRouter>
      <Navbar/>
      <Routes>
        <Route  path="/" element={<Home />}/>
        <Route  path="/stock-detail" element={<StockDetail />}/>
        <Route  path="/mutual-funds" element={<MutualFunds />}/>
        <Route  path="/ipo" element={<Ipo />}/>
      </Routes>
      </BrowserRouter>
    </>
  );
}

export default App;
