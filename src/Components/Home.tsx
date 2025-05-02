import search_icon from "../assets/search_icon.png";
import loss from "../assets/loss.png";
import profit from "../assets/profit.png";
// import { createContext, useState, useEffect, useContext } from 'react';
import { useState } from "react";
import { useNavigate } from "react-router-dom";
function Home() {

  // const userContext = createContext();
  // export const userContext = () => useContext(userContext);

  
  const navigate = useNavigate();

  const arr = [
    {
      stock_name: "Stock name",
      company: "Company Name",
      icon: loss,
      amount: 290.6,
      percent: +1.81,
    },
    {
      stock_name: "Stock name",
      company: "Company Name",
      icon: profit,
      amount: 146.06,
      percent: +1.2,
    },
    {
      stock_name: "Stock name",
      icon: profit,
      company: "Company Name",
      amount: 310.06,
      percent: +1.2,
    },
  ];
  
  const [userInput, setUserInput] = useState("");
  function handleInput(e) {
    setUserInput(e.target.value);
  }
  function handleSearch() {
    console.log("Stock searched :", userInput);
    navigate("/stock-detail")
  }

  return (
    <div className="flex justify-center items-center mt-8 flex-col">
      <h2 className="font-[Gabarito] w-[40rem] text-center text-5xl">
        Make better investments with alternative data insights
      </h2>
      <h3 className="font-[Gabarito] text-[#9B9B9B] w-[22rem] text-center font-normal text-[18px] pt-4">
        See the market with unparalleled clarity. Power your decisions with
        StockView
      </h3>
      <div className="border-[#BABABA] border-[1px] h-12 w-[25rem] flex justify-between items-center rounded-[8px] mt-6">
        {/* search icon */}
        <img
          src={search_icon}
          alt="search icon"
          className="w-[23px] h-[23px] ml-3 cursor-pointer"
        />
        <input
          type="text"
          className="w-[280px] h-full outline-none"
          placeholder="Search Stock"
          onChange={handleInput}
        />
        <button
          className="bg-[#FFB700] font-[Gabarito] text-black h-full p-2 rounded-[9px] text-[15px] w-[70px] cursor-pointer"
          onClick={handleSearch}
        >
          Search
        </button>
      </div>

      <div className="flex mt-[87px]  gap-x-5">
        {arr.map((item, index) => (
          <div
            key={index}
            className="bg-black rounded-tl-2xl rounded-tr-2xl w-[268px] h-[125px] flex flex-col"
          >
            <div className="flex justify-center items-center gap-x-5 pt-5">
              {/* logo */}
              <img src="" alt="" className="bg-white rounded-full h-10 w-10" />
              <div className="flex flex-col text-white font-[Gabarito]">
                <h3 className="text-[13px]">{item.stock_name}</h3>
                <h4>{item.company}</h4>
              </div>
            </div>
            <div className="flex justify-center items-center text-white font-[Gabarito] pt-4">
              <div className="flex justify-center items-center">
                <h4 className="text-4xl">₹</h4>
                <h5 className="text-2xl pt-2 pl-1">{item.amount}</h5>
              </div>
              <div
                className={`rounded-[8px] p-1 gap-x-1 w-[80px] text-center ml-6 flex justify-center items-center ${
                  item.icon == profit ? "bg-green-500" : "bg-red-500"
                }`}
              >
                <img src={item.icon} alt="icon" className="w-5 h-5" />
                <h5 className="text-center text-black">{item.percent}%</h5>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Home;
