import logo from "../assets/logo.png";
function Navbar() {
  return (
    <div className="flex justify-start items-center mt-3 mx-auto max-w-screen-xl">
      {/* Logo */}
      <div className="flex gap-x-1 ml-10">
        <img src={logo} alt="StockView Logo" className="cursor-pointer" />
        <h1 className="font-[Gabarito] text-3xl pt-3 cursor-pointer">
          StockView
        </h1>
      </div>

      <div className="font-[Gabarito] text-xl ml-[20%]">
        <ul className="flex gap-x-10">
          <li>News</li>
          <li>Mutual Funds</li>
          <li>IPOs</li>
        </ul>
      </div>
    </div>
  );
}

export default Navbar;
