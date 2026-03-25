export const LeaseComplianceVerificationSection = (): JSX.Element => {
  const complianceItems = [
    {
      title: "Deposit Protection",
      description:
        "I can assist in verifying that your deposit is protected in a government-approved scheme, which is crucial for your security.",
      icon: "/img/vector-15.svg",
      iconAlt: "Vector",
      iconWidth: "25.33px",
      top: "247px",
    },
    {
      title: "Landlord Licenses",
      description:
        "I ensure your landlord holds the necessary licenses to operate legally, safeguarding your rights as a tenant.",
      icon: "/img/vector-16.svg",
      iconAlt: "Vector",
      iconWidth: "26.67px",
      top: "399px",
    },
    {
      title: "Safety Tests",
      description:
        "I help confirm that your landlord conducts required safety tests, such as gas and electrical inspections, ensuring a safe living environment.",
      icon: "/img/vector-17.svg",
      iconAlt: "Vector",
      iconWidth: "26.88px",
      top: "551px",
    },
    {
      title: "Peace of Mind",
      description:
        "By ensuring compliance, you can feel secure and confident in your rental arrangement.",
      icon: "/img/vector-18.svg",
      iconAlt: "Vector",
      iconWidth: "26.67px",
      top: "703px",
    },
  ];

  const descriptionWidths = ["561px", "561px", "592px", "494px"];

  return (
    <div className="absolute top-[4262px] left-[calc(50.00%_-_720px)] w-[1440px] h-[1744px] flex justify-center bg-[#1f1c1c]">
      <div className="mt-[99px] w-[1402px] h-[975px] ml-0.5 relative">
        <div className="absolute top-0 left-[calc(50.00%_-_320px)] [font-family:'Inter',Helvetica] font-semibold text-white text-7xl text-center tracking-[0] leading-[74px] whitespace-nowrap">
          Verify Compliance
        </div>

        <div className="top-28 left-[calc(50.00%_-_228px)] w-[775px] absolute h-16">
          <div className="left-[calc(50.00%_-_388px)] w-[773px] h-16 bg-[#ffffff1a] rounded-[16px_16px_0px_16px] backdrop-blur-[2.0px] backdrop-brightness-[100.0%] backdrop-saturate-[100.0%] [-webkit-backdrop-filter:blur(2.0px)_brightness(100.0%)_saturate(100.0%)] shadow-[inset_0_1px_0_rgba(255,255,255,0.40),inset_1px_0_0_rgba(255,255,255,0.32),inset_0_-1px_1px_rgba(0,0,0,0.13),inset_-1px_0_1px_rgba(0,0,0,0.11)] absolute top-0" />

          <p className="absolute top-[18px] left-[65px] [font-family:'Inter',Helvetica] font-normal text-white text-2xl tracking-[0] leading-[normal]">
            I can help ensure your landlord complies with all rental laws.
          </p>

          <div className="absolute top-[calc(50.00%_-_16px)] left-[17px] w-8 h-8 flex rotate-[-180.00deg]">
            <img
              className="flex-1 w-[29.17px] rotate-[180.00deg]"
              alt="Vector"
              src="/img/vector-19.svg"
            />
          </div>
        </div>

        <div className="absolute top-[255px] left-0 w-[690px] h-[584px] flex bg-[#dedede] rounded-2xl overflow-hidden">
          <img
            className="w-[690px] h-[584px] aspect-[1.18]"
            alt="Element image"
            src="/img/20260114-1551-image-generation-simple-compose-01keyk6g05ez3s32y7.png"
          />
        </div>

        {complianceItems.map((item, index) => (
          <div
            key={index}
            className="absolute left-[710px] w-[690px] h-[136px] rounded-2xl overflow-hidden"
            style={{ top: item.top }}
          >
            <div className="absolute top-[25px] left-[72px] w-[267px] [font-family:'Inter',Helvetica] font-bold text-white text-2xl tracking-[0] leading-[normal]">
              {item.title}
            </div>

            <p
              className="absolute top-[61px] left-[72px] [font-family:'Inter',Helvetica] font-light text-white text-lg tracking-[0] leading-[26px]"
              style={{ width: descriptionWidths[index] }}
            >
              {item.description}
            </p>

            <div
              className="absolute left-[22px] w-8 h-8 flex"
              style={{ top: index === 2 ? "24px" : "23px" }}
            >
              <img
                className="flex-1"
                style={{ width: item.iconWidth }}
                alt={item.iconAlt}
                src={item.icon}
              />
            </div>
          </div>
        ))}

        <div className="absolute top-[910px] left-[calc(50.00%_-_583px)] w-[933px] h-[65px]">
          <img
            className="left-[calc(50.00%_-_466px)] w-[931px] h-[65px] absolute top-0"
            alt="Rectangle"
            src="/img/rectangle-1-1.svg"
          />

          <div className="absolute top-[calc(50.00%_-_16px)] left-[17px] w-8 h-8 flex rotate-[-180.00deg]">
            <img
              className="flex-1 w-[29.17px] rotate-[180.00deg]"
              alt="Vector"
              src="/img/vector-19.svg"
            />
          </div>

          <p className="absolute top-[18px] left-[65px] [font-family:'Inter',Helvetica] font-normal text-white text-2xl tracking-[0] leading-[normal]">
            With my help, you can protect your rights and enjoy your home
            worry-free!
          </p>
        </div>
      </div>
    </div>
  );
};
