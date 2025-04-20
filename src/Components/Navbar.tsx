import logo from "../assets/logo.png";
import { useNavigate } from "react-router-dom";
function Navbar() {
  const navigate = useNavigate();
  return (
    <div className="flex justify-start items-center mt-3 mx-auto max-w-screen-xl">
      {/* Logo */}
      <div className="flex gap-x-1 ml-10" onClick={()=>navigate("/")}>
        <img
          src={logo}
          alt="StockView Logo"
          className="cursor-pointer w-13 h-13"
          
        />
        <h1 className="font-[Gabarito] text-3xl  pt-2 cursor-pointer">
          StockView
        </h1>
      </div>

      <div className="font-[Gabarito] text-xl ml-[20%]">
        <ul className="flex gap-x-10 cursor-pointer">
          <li>News</li>
          <li onClick={()=>navigate("/mutual-funds")}>Mutual Funds</li>
          <li onClick={()=>navigate("/ipo")}>IPOs</li>
        </ul>
      </div>
    </div>
  );
}

export default Navbar;
