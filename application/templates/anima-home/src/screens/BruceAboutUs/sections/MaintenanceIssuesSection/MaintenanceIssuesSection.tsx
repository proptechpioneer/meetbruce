export const MaintenanceIssuesSection = (): JSX.Element => {
  const topCards = [
    {
      icon: "/img/vector-5.svg",
      iconAlt: "Vector",
      iconWidth: "26.67px",
      title: "Notify Landlords",
      description:
        "I can help notify your landlord about necessary repair and maintenance issues.",
      descriptionWidth: "w-[336px]",
      top: "top-[329px]",
      left: "left-5",
    },
    {
      icon: "/img/vector-8.svg",
      iconAlt: "Vector",
      iconWidth: "26.67px",
      title: "Track Progress",
      description:
        "I monitor the status of repairs to ensure they are addressed in a timely manner.",
      descriptionWidth: "w-[323px]",
      top: "top-[329px]",
      left: "left-[493px]",
    },
    {
      icon: "/img/vector-9.svg",
      iconAlt: "Vector",
      iconWidth: "29.33px",
      title: "Escalate Issues",
      description:
        "If your landlord doesn't respond, I can assist in escalating the matter to your local council and the Housing Ombudsman.",
      descriptionWidth: "w-[373px]",
      top: "top-[329px]",
      left: "left-[967px]",
    },
  ];

  const bottomCards = [
    {
      icon: "/img/vector-6.svg",
      iconAlt: "Vector",
      iconWidth: "27.08px",
      title: "Gather Evidence",
      description:
        "I help you collect and organize all relevant documents, including correspondence, photographs, receipts, and any other evidence to support your claim.",
      descriptionWidth: "w-[408px]",
      top: "top-[608px]",
      left: "left-5",
    },
    {
      icon: "/img/vector-7.svg",
      iconAlt: "Vector",
      iconWidth: "24px",
      title: "Present a Strong Case",
      description:
        "With comprehensive evidence, you can confidently present your case and ensure your rights as a tenant are upheld.",
      descriptionWidth: "w-[393px]",
      top: "top-[608px]",
      left: "left-[493px]",
    },
  ];

  return (
    <div className="absolute top-[3288px] left-[calc(50.00%_-_720px)] w-[1440px] h-[974px] bg-[#bfc29e]">
        <div className="absolute top-[104px] left-[calc(50.00% - 720px)] [font-family:'Inter',Helvetica] font-bold text-text text-7xl text-center tracking-[0] leading-[74px] whitespace-nowrap">
        Deal with Maintenance Issues
      </div>

      {topCards.map((card, index) => (
        <div
          key={index}
          className={`absolute ${card.top} ${card.left} w-[453px] h-[263px] flex flex-col bg-white rounded-2xl overflow-hidden`}
        >
          <div className="ml-[21px] w-8 h-8 mt-[22px] flex aspect-[1]">
            <img
              className="flex-1"
              style={{ width: card.iconWidth }}
              alt={card.iconAlt}
              src={card.icon}
            />
          </div>

          <div className="ml-[21px] w-[267px] h-[29px] mt-[59px] [font-family:'Inter',Helvetica] font-bold text-text text-2xl tracking-[0] leading-[normal]">
            {card.title}
          </div>

          <p
            className={`ml-[21px] ${card.descriptionWidth} h-[78px] mt-[13px] [font-family:'Inter',Helvetica] font-normal text-text text-lg tracking-[0] leading-[26px]`}
          >
            {card.description}
          </p>
        </div>
      ))}

      {bottomCards.map((card, index) => (
        <div
          key={index}
          className={`absolute ${card.top} ${card.left} w-[453px] h-[263px] flex flex-col bg-white rounded-2xl overflow-hidden`}
        >
          <div className="ml-[21px] w-8 h-8 mt-6 flex aspect-[1]">
            <img
              className="flex-1"
              style={{ width: card.iconWidth }}
              alt={card.iconAlt}
              src={card.icon}
            />
          </div>

          <div className="ml-[21px] w-[267px] h-[29px] mt-[33px] [font-family:'Inter',Helvetica] font-bold text-text text-2xl tracking-[0] leading-[normal]">
            {card.title}
          </div>

          <p
            className={`ml-[21px] ${card.descriptionWidth} h-[104px] mt-[13px] [font-family:'Inter',Helvetica] font-normal text-text text-lg tracking-[0] leading-[26px]`}
          >
            {card.description}
          </p>
        </div>
      ))}

      <div className="absolute top-[744px] left-[calc(50.00%_+_247px)] w-[452px] h-32">
        <img
          className="left-[calc(50.00%_-_226px)] w-[450px] h-32 absolute top-0"
          alt="Rectangle"
          src="/img/rectangle-1.svg"
        />

        <div className="absolute top-[calc(50.00%_-_48px)] left-[17px] w-8 h-8 flex rotate-[-180.00deg]">
          <img
            className="flex-1 w-[29.17px] rotate-[180.00deg]"
            alt="Vector"
            src="/img/vector-11.svg"
          />
        </div>

        <p className="absolute top-[22px] left-[65px] w-[363px] [font-family:'Inter',Helvetica] font-normal text-text text-2xl tracking-[0] leading-[normal]">
          With my help, you can ensure a safe and well-maintained living
          environment!
        </p>
      </div>

      <div className="top-[232px] left-[calc(50.00%_-_392px)] w-[976px] absolute h-16">
        <div className="left-[calc(50.00%_-_488px)] w-[974px] h-16 bg-[#ffffff1a] rounded-[16px_16px_0px_16px] backdrop-blur-[2.0px] backdrop-brightness-[100.0%] backdrop-saturate-[100.0%] [-webkit-backdrop-filter:blur(2.0px)_brightness(100.0%)_saturate(100.0%)] shadow-[inset_0_1px_0_rgba(255,255,255,0.40),inset_1px_0_0_rgba(255,255,255,0.32),inset_0_-1px_1px_rgba(0,0,0,0.13),inset_-1px_0_1px_rgba(0,0,0,0.11)] absolute top-0" />

        <p className="absolute top-[18px] left-[65px] [font-family:'Inter',Helvetica] font-normal text-text text-2xl tracking-[0] leading-[normal]">
          I can help notify your landlord about necessary repair and maintenance
          issues.
        </p>

        <div className="absolute top-[calc(50.00%_-_16px)] left-[17px] w-8 h-8 flex rotate-[-180.00deg]">
          <img
            className="flex-1 w-[29.17px] rotate-[180.00deg]"
            alt="Vector"
            src="/img/vector-11.svg"
          />
        </div>
      </div>
    </div>
  );
};
