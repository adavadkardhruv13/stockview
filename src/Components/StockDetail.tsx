import car from "../assets/car.png";
function StockDetail() {
  const details = {
    "Previous Close": 268.0,
    "Market Cap": 2765.16,
    "52 Week High": 324.6,
    "52 Week Low": 208.5,
    "P/E Ratio": 22.32,
    "Dividend Ratio": 6,
  };
  return (
    <div>
      <div className="flex flex-col items-center justify-center">
        {/* Info */}
        <div className="flex gap-x-5 mr-[740px] mb-7">
          <img
            src=""
            alt=""
            className="border-[1px] border-[#9B9B9B] rounded-full h-16 w-16"
          />
          <div className="flex flex-col gap-y-2">
            <h3>TITAN</h3>
            <h4>Titan Company Ltd</h4>
          </div>
        </div>

        {/* Company details */}
        <div className="flex flex-col">
          <div></div>
          <div className="flex mb-[60px]">
            <div className="flex flex-col">
              <h5>Stock Watchlists</h5>
              <div className="border-[1px] border-[#9B9B9B] h-[330px] w-[40rem] rounded-[10px] mr-[75px] "></div>
            </div>

            <div className="flex flex-col">
              {/* Details */}
              <h5>Details</h5>
              <div className="flex border-[#9B9B9B] border-[1px] w-[15rem] rounded-[8px] h-[15rem] flex-col p-3 gap-y-3">
                {Object.entries(details).map(([key, value], index) => (
                  <div
                    key={index}
                    className="flex justify-between items-center"
                  >
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
                  <img src={car} alt="" className="opacity-25 " />
                </div>
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
    </div>
  );
}

export default StockDetail;
