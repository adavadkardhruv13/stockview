import Navbar from "./Components/Navbar";
import Home from "./Components/Home";
import StockDetail from "./Components/StockDetail";
import { BrowserRouter, Route, Routes } from "react-router-dom";
function App() {
  return (
    <>
      <BrowserRouter>
      <Navbar/>
      <Routes>
        <Route  path="/" element={<Home />}/>
        <Route  path="/stock-detail" element={<StockDetail />}/>
      </Routes>
      </BrowserRouter>
    </>
  );
}

export default App;
