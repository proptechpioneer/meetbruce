import heroScreenImage from "../../../../assets/hero-screen.png";

export const RentersRightsOverviewSection = (): JSX.Element => {
  const paragraphs = [
    "Hello! I'm Bruce, your dedicated AI-powered Tenant Advocate.",
    "My mission is to help you, the tenant, confidently navigate your relationship with your landlord and make the most of your renting experience.",
    "With the new Renters Rights Act, I'm here to empower you to understand your rights and get the most benefits, ensuring you enjoy a fair and fulfilling renting journey!",
  ];

  return (
    <div className="absolute top-[830px] left-[calc(50.00%_-_720px)] w-[1440px] h-[450px] flex bg-[#ff6e42]">
      <div className="mt-[26px] w-[1402px] h-[400px] ml-5 relative">
        <div className="absolute top-0 left-0 w-[1400px] h-[400px] bg-[#fbfbfb1a] rounded-2xl backdrop-blur-[2.0px] backdrop-brightness-[100.0%] backdrop-saturate-[100.0%] [-webkit-backdrop-filter:blur(2.0px)_brightness(100.0%)_saturate(100.0%)] shadow-[inset_0_1px_0_rgba(255,255,255,0.40),inset_1px_0_0_rgba(255,255,255,0.32),inset_0_-1px_1px_rgba(0,0,0,0.13),inset_-1px_0_1px_rgba(0,0,0,0.11)]" />

        <div className="flex flex-col items-start gap-6 absolute w-[760px] h-[309px] top-[57px] left-[126px]">
          {paragraphs.map((text, index) => (
            <p
              key={index}
              className="relative self-stretch [font-family:'Inter',Helvetica] font-normal text-text text-[32px] tracking-[0] leading-[normal]"
            >
              <span className="[font-family:'Inter',Helvetica] font-normal text-[#21201c] text-[32px] tracking-[0]">
                {text}
              </span>
            </p>
          ))}
        </div>

        <img
          className="absolute top-[39px] left-[928px] w-[430px] h-[322px] object-cover rounded-xl"
          alt="Hero screen"
          src={heroScreenImage}
        />

        <div className="absolute top-[calc(50.00%_-_154px)] left-[50px] w-12 h-12 flex rotate-[-180.00deg]">
          <img
            className="flex-1 w-[43.76px] rotate-[180.00deg]"
            alt="Vector"
            src="/img/vector-12.svg"
          />
        </div>
      </div>
    </div>
  );
};
