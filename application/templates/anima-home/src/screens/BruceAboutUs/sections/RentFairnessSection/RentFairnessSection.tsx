export const RentFairnessSection = (): JSX.Element => {
  const cards = [
    {
      id: 1,
      title: "Challenge with Confidence",
      description:
        "If your landlord proposes a rent increase, I can help you bring a case to the Tribunal for free, ensuring you know if the increase is fair.",
      titleLeft: true,
      titleTop: 33,
      descTop: 189,
      textLeft: 32,
      textWidth: 291,
      descWidth: 291,
      imgSrc:
        "/img/young-family-with-little-daughter-moving-into-new-house-1.png",
      imgLeft: 354,
      imgAlt: "Young family with",
      top: 424,
      left: 20,
    },
    {
      id: 2,
      title: "Delay on Increases",
      description:
        "If you challenge the proposed increase, it won't take effect until the Tribunal makes its decision, allowing you to delay any increase for several months.",
      titleLeft: true,
      titleTop: 33,
      descTop: 189,
      textLeft: 32,
      textWidth: 267,
      descWidth: 293,
      imgSrc:
        "/img/young-family-with-little-daughter-moving-into-new-house-1-1.png",
      imgLeft: 355,
      imgAlt: "Young family with",
      top: 424,
      left: 730,
    },
    {
      id: 3,
      title: "No Risk of Higher Increases",
      description:
        "The Tribunal can only approve your landlord's proposed amount, so you won't face a higher increase.",
      titleLeft: false,
      titleTop: 33,
      descTop: 213,
      textLeft: 367,
      textWidth: 267,
      descWidth: 293,
      imgSrc: "/img/2026-01-13-16-10-54-1.png",
      imgLeft: 0,
      imgAlt: "Element",
      top: 784,
      left: 20,
    },
    {
      id: 4,
      title: "Support for Hardship",
      description:
        "The Tribunal can defer any increase by up to two months to help prevent undue financial pressure on you.",
      titleLeft: false,
      titleTop: 33,
      descTop: 213,
      textLeft: 367,
      textWidth: 267,
      descWidth: 293,
      imgSrc: "/img/18296-1.png",
      imgLeft: 0,
      imgAlt: "Element",
      top: 784,
      left: 730,
    },
  ];

  return (
    <div className="absolute top-[1928px] left-[calc(50.00%_-_720px)] w-[1440px] h-[1360px] bg-[#201c1c]">
        <p className="absolute top-[121px] left-[calc(50.00% - 720px)] [font-family:'Inter',Helvetica] font-bold text-white text-7xl text-center tracking-[0] leading-[74px] whitespace-nowrap">
        Get a Fairer Deal on your Rent
      </p>

      <div className="absolute top-[312px] left-[calc(50.00%_-_99px)] w-[577px] h-16">
        <div className="left-[calc(50.00%_-_288px)] w-[575px] h-16 bg-[#ffffff1a] rounded-[16px_16px_0px_16px] backdrop-blur-[2.0px] backdrop-brightness-[100.0%] backdrop-saturate-[100.0%] [-webkit-backdrop-filter:blur(2.0px)_brightness(100.0%)_saturate(100.0%)] shadow-[inset_0_1px_0_rgba(255,255,255,0.40),inset_1px_0_0_rgba(255,255,255,0.32),inset_0_-1px_1px_rgba(0,0,0,0.13),inset_-1px_0_1px_rgba(0,0,0,0.11)] absolute top-0" />

        <p className="absolute top-[18px] left-[65px] [font-family:'Inter',Helvetica] font-normal text-white text-2xl tracking-[0] leading-[normal]">
          I can help you get a fairer deal on your rent.
        </p>

        <div className="absolute top-[calc(50.00%_-_16px)] left-[17px] w-8 h-8 flex rotate-[-180.00deg]">
          <img
            className="flex-1 w-[29.17px] rotate-[180.00deg]"
            alt="Vector"
            src="/img/vector-19.svg"
          />
        </div>
      </div>

      {cards.map((card) => (
        <div
          key={card.id}
          className="absolute w-[690px] h-[344px] bg-white rounded-2xl overflow-hidden"
          style={{ top: `${card.top}px`, left: `${card.left}px` }}
        >
          <div
            className="absolute [font-family:'Inter',Helvetica] font-bold text-text text-2xl tracking-[0] leading-[normal] w-[267px]"
            style={{ top: `${card.titleTop}px`, left: `${card.textLeft}px` }}
          >
            {card.title}
          </div>

          <p
            className="absolute [font-family:'Inter',Helvetica] font-normal text-text text-lg tracking-[0] leading-[26px]"
            style={{
              top: `${card.descTop}px`,
              left: `${card.textLeft}px`,
              width: `${card.descWidth}px`,
            }}
          >
            {card.description}
          </p>

          <img
            className="absolute top-0 h-[344px] aspect-[0.98]"
            style={{
              left: `${card.imgLeft}px`,
              width:
                card.imgLeft === 0
                  ? "335px"
                  : card.id === 1
                    ? "336px"
                    : "335px",
              aspectRatio: card.imgLeft === 0 ? "0.97" : "0.98",
            }}
            alt={card.imgAlt}
            src={card.imgSrc}
          />
        </div>
      ))}

      <p className="absolute top-[212px] left-[calc(50.00%_-_278px)] w-[556px] [font-family:'Inter',Helvetica] font-light text-white text-xl text-center tracking-[0] leading-7">
        Starting May 1st next year, every private renter will have the power to
        challenge any unfair rent increase.
      </p>

      <div className="absolute top-[1202px] left-[calc(50.00%_-_582px)] w-[994px] h-16">
        <div className="left-[calc(50.00%_-_497px)] w-[992px] h-16 bg-[#ffffff1a] rounded-[16px_16px_0px_16px] backdrop-blur-[2.0px] backdrop-brightness-[100.0%] backdrop-saturate-[100.0%] [-webkit-backdrop-filter:blur(2.0px)_brightness(100.0%)_saturate(100.0%)] shadow-[inset_0_1px_0_rgba(255,255,255,0.40),inset_1px_0_0_rgba(255,255,255,0.32),inset_0_-1px_1px_rgba(0,0,0,0.13),inset_-1px_0_1px_rgba(0,0,0,0.11)] absolute top-0" />

        <p className="absolute top-[18px] left-[66px] w-[923px] [font-family:'Inter',Helvetica] font-normal text-white text-2xl tracking-[0] leading-[normal]">
          With my help, you can confidently navigate rent reviews and protect
          your rights!
        </p>

        <div className="absolute top-[calc(50.00%_-_16px)] left-[17px] w-[33px] h-8 flex rotate-[-180.00deg]">
          <img
            className="flex-1 w-[29.71px] rotate-[180.00deg]"
            alt="Vector"
            src="/img/vector-4.svg"
          />
        </div>
      </div>
    </div>
  );
};
