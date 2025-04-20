import { useSearchParams } from "react-router-dom";
import { useEffect, useState } from "react";
import car from "../assets/car.png";
import rupee from "../assets/rupee.png";

function StockDetail() {
  const [searchParams] = useSearchParams();

  const [freqSelected, setFreqSelected] = useState("1D");

  const details = {
    "Previous Close": 268.0,
    "Market Cap": 2765.16,
    "52 Week High": 324.6,
    "52 Week Low": 208.5,
    "P/E Ratio": 22.32,
    "Dividend Ratio": 6,
  };

  const frequency = ["1D", "5D", "1M", "3M", "6M", "1Y", "5Y"];

  type Details = {
    previous_close: number | string;
    market_cap: string | number;
    week_high_52: number | string;
    week_low_52: number | string;
    pe_ratio: number | string;
    dividendRate: string | number;
  };
  const apiUrl = import.meta.env.VITE_API_URL;
  async function detailsApiCall() {
    try {
      const url = `${apiUrl}/docs/stock-details/{${userInput}}`;
      console.log("Calling:", url);

      const response = await fetch(url);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      const formattedData: Details[] = data.map((item: any) => ({
        previous_close:
          typeof item.previous_close === "number"
            ? item.previous_close.toFixed(2)
            : item.previous_close,
        market_cap:
          typeof item.market_cap === "number"
            ? item.market_cap.toFixed(2)
            : item.market_cap,
        week_high_52:
          typeof item.week_high_52 === "number"
            ? item.week_high_52.toFixed(2)
            : item.week_high_52,
        week_low_52:
          typeof item.week_low_52 === "number"
            ? item.week_low_52.toFixed(2)
            : item.week_low_52,
        pe_ratio:
          typeof item.pe_ratio === "number"
            ? item.pe_ratio.toFixed(2)
            : item.pe_ratio,
        dividendRate:
          typeof item.dividendRate === "number"
            ? item.dividendRate.toFixed(2)
            : item.dividendRate,
      }));
    } catch (e) {
      console.log(e);
    }
  }
  return (
    <div className="flex flex-col items-center justify-center">
      {/* Info */}
      <div className="flex gap-x-5 mr-[635px] mb-7">
        <div className="border-[1px] border-[#9B9B9B] rounded-full h-[100px] w-[100px]"></div>
        <div className="flex flex-col gap-y-1">
          <h3 className="text-[30px]">TITAN</h3>
          <h4 className="text-[25px]">Titan Company Ltd</h4>
        </div>
      </div>

      {/* Company details */}
      <div className="flex mb-[60px]">
        <div className="flex flex-col">
          <h5 className="text-[20px]">Stock Watchlists</h5>
          {/* Charts and Value */}
          <div className="flex  flex-col border-[1px] border-[#9B9B9B] h-[330px] w-[40rem] rounded-[10px] mr-[75px] items-center">
            <div className="flex items-center gap-4 mt-4">
              <img src={rupee} alt="Rupee" className="h-16 w-16" />
              <div className="flex flex-col">
                <h5 className="text-[30px]">290.06</h5>
                <h6 className="text-green-400">159.75 (+0.69%)</h6>
              </div>
              {/* Frequency Selection */}
              <div className="border-[#9B9B9B] border-[1px] h-8 w-[250px] flex justify-around mt-4 rounded-md">
                {frequency.map((item, index) => (
                  <button
                    key={index}
                    onClick={() => setFreqSelected(item)}
                    className={`px-2 text-sm cursor-pointer ${
                      freqSelected === item
                        ? "bg-[#FFB700] text-black"
                        : "text-[#D9D9D9]"
                    }`}
                  >
                    {item}
                  </button>
                ))}
              </div>
            </div>
          </div>
        </div>

        <div className="flex flex-col">
          {/* Details */}
          <h5 className="mb-2">Details</h5>
          <div className="border-[#9B9B9B] border-[1px] w-[15rem] rounded-[8px] h-[15rem] flex flex-col p-3 gap-y-3">
            {Object.entries(details).map(([key, value], index) => (
              <div key={index} className="flex justify-between items-center">
                <h5 className="text-[#9B9B9B]">{key}</h5>
                <h6 className="font-medium">{value}</h6>
              </div>
            ))}
          </div>
          {/* Sector */}
          <div className="border-[1px] border-[#9B9B9B] w-[15rem] h-14 rounded-[8px] flex justify-center items-center gap-x-5 mt-9">
            <div className="flex flex-col">
              <h5 className="text-[#666666] font-normal">Recommendation</h5>
              <h6>Buy Recommendation</h6>
            </div>
            <div className="bg-[#FFB700] w-12 h-12 opacity-20 cursor-pointer">
              <img src={car} alt="Car" className="opacity-25" />
            </div>
          </div>
        </div>
      </div>

      {/* Related News */}
      <div className="bg-[#FFB700] w-[60rem] h-[20rem] rounded-2xl flex justify-center items-center mb-12">
        <div className="grid grid-cols-4 grid-rows-2 gap-4">
          {Array.from({ length: 8 }).map((_, index) => (
            <div
              key={index}
              className="bg-white w-[12rem] h-[6rem] rounded-[8px]"
            ></div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default StockDetail;
