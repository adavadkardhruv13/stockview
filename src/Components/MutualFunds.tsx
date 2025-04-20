import { useEffect, useState } from "react";
import tata from "../assets/tata.png";
import star from "../assets/star.png";

type MutualFund = {
  fund_name: string;
  latest_nav: number | null;
  asset_size: number | null;
  star_rating: number | null;
  one_month_return: number | null;
  six_month_return: number | null;
  one_year_return: number | null;
  three_year_return: number | null;
  five_year_return: number | null;
  logo: string;
  fund_type: string;
};

const MutualFunds = () => {
  const btn = ["Equity", "Hybrid", "Index Funds"];
  const fund1 = ["1M", "6M", "1Y", "3Y", "5Y"];

  const [type, setType] = useState("Equity");
  const [activeIndex, setActiveIndex] = useState(0);
  const [apiResponse, setApiResponse] = useState<MutualFund[]>([]);

  const apiUrl = import.meta.env.VITE_API_URL;

  async function apiCall(name: string) {
    try {
      const url = `${apiUrl}/mutual_funds/?fund_type=${name}`;
      console.log("Calling:", url);

      const response = await fetch(url);

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      const formattedData: MutualFund[] = data.map((item: any) => ({
        fund_name: item.fund_name,
        latest_nav:
          typeof item.latest_nav === "number"
            ? parseFloat(item.latest_nav.toFixed(2))
            : null,
        asset_size:
          typeof item.asset_size === "number" ? item.asset_size : null,
        star_rating:
          typeof item.star_rating === "number" ? item.star_rating : null,
        one_month_return:
          typeof item.one_month_return === "number"
            ? item.one_month_return
            : null,
        six_month_return:
          typeof item.six_month_return === "number"
            ? item.six_month_return
            : null,
        one_year_return:
          typeof item.one_year_return === "number"
            ? item.one_year_return
            : null,
        three_year_return:
          typeof item.three_year_return === "number"
            ? item.three_year_return
            : null,
        five_year_return:
          typeof item.five_year_return === "number"
            ? item.five_year_return
            : null,
        logo: tata,
        fund_type: item.fund_type,
      }));

      setApiResponse(formattedData);
    } catch (error) {
      console.error("API call failed:", error);
      setApiResponse([]);
    }
  }

  useEffect(() => {
    apiCall(type);
  }, []);

  return (
    <div className="flex items-start justify-center">
      <div className="flex flex-col mt-12 items-start justify-center mr-[70px]">
        <h2 className="text-black text-[30px]">Mutual Funds</h2>
        <p className="text-[#666666]">
          Smart investing made simple—grow your wealth with the right mutual
          funds.
        </p>

        <div className="flex gap-x-6 mt-6">
          {btn.map((name, index) => (
            <button
              key={index}
              onClick={async () => {
                setActiveIndex(index);
                setType(name);
                await apiCall(name);
              }}
              className={`p-1 w-24 rounded-[6px] text-[16px] cursor-pointer ${
                activeIndex === index
                  ? "text-black bg-[#FFB700]"
                  : "text-[#9B9B9B] border-[#9B9B9B] border-[1px]"
              }`}
            >
              {name}
            </button>
          ))}
        </div>

        <div className="mt-5 p-3 rounded-[7px] bg-[#D9D9D9] flex items-center justify-around text-[#666666] font-semibold w-[1100px]">
          <h3 className="mr-[250px]">SCHEME NAME</h3>
          <div className="flex gap-x-10 items-center justify-between cursor-pointer">
            {fund1.map((item, index) => (
              <h4 key={index}>{item}</h4>
            ))}
          </div>
          <h4>Fund Size</h4>
          <h4>NAV</h4>
        </div>

        <div className="flex flex-col mb-10">
          {apiResponse.map((item, index) => (
            <div
              key={index}
              className="border-[#9B9B9B] border-[1px] w-[1100px] h-[110px] rounded-[7px] mt-8 flex justify-between items-center px-6"
            >
              <div className="flex items-center gap-x-4">
                <img
                  src={item.logo || tata}
                  alt="Logo"
                  className="w-[68px] h-[68px]"
                />
                <div className="flex flex-col">
                  <h3 className="font-semibold text-black">{item.fund_name}</h3>
                  <div className="flex gap-x-5">
                    <span className="text-[#8D6500] bg-[#FFB700] opacity-55 p-1">
                      {item.fund_type}
                    </span>
                    <div className="flex text-[#8D6500] bg-[#FFB700] opacity-85 p-1">
                      <img src={star} alt="rating" />
                      <span>{item.star_rating ?? ""}</span>
                    </div>
                  </div>
                </div>
              </div>

              <div className="flex gap-x-10 items-center justify-between cursor-pointer">
                {[
                  item.one_month_return,
                  item.six_month_return,
                  item.one_year_return,
                  item.three_year_return,
                  item.five_year_return,
                ].map((value, i) => (
                  <h4
                    key={i}
                    className={`mr-5 ${
                      typeof value === "number"
                        ? value > 0
                          ? "text-green-500"
                          : value < 0
                          ? "text-red-500"
                          : ""
                        : ""
                    }`}
                  >
                    {typeof value === "number" ? `${value.toFixed(2)}%` : ""}
                  </h4>
                ))}
                <h4>
                  {typeof item.asset_size === "number"
                    ? item.asset_size.toLocaleString()
                    : ""}
                </h4>
                <h4>
                  {typeof item.latest_nav === "number"
                    ? item.latest_nav.toFixed(2)
                    : ""}
                </h4>
              </div>
            </div>
          ))}

          {apiResponse.length === 0 && (
            <div className="text-gray-500 text-lg mt-6">
              No funds found for "{type}" type.
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default MutualFunds;
