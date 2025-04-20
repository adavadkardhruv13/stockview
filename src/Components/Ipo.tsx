import { useState } from "react";
const Ipo = () => {
  const category = ["Active", "Listed", "Upcoming"];
  const [activeIndex, setActiveIndex] = useState(0);
  return (
    <div className="flex items-start justify-center">
      {/* Heading */}
      <div className="flex flex-col justify-center items-start mr-[42rem]">
        <div className="flex flex-col">
          <h1 className="font-semibold text-4xl">IPOs</h1>
          <p className="text-[#666666]">
            Navigate the IPO landscape: Clear insights, growth-focused
            decisions.
          </p>
        </div>
        {/* Category Buttons */}
        <div className="flex gap-x-6 mt-10">
          {category.map((name, index) => (
            <button
              key={index}
              onClick={async () => {
                setActiveIndex(index);
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
        <div></div>
      </div>
    </div>
  );
};

export default Ipo;
