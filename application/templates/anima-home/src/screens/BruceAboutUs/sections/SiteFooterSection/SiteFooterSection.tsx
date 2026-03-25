export const SiteFooterSection = (): JSX.Element => {
  const socialIcons = [
    { src: "/img/vector.svg", alt: "Vector" },
    { src: "/img/vector-1.svg", alt: "Vector" },
    { src: "/img/vector-2.svg", alt: "Vector" },
  ];

  return (
    <div className="absolute w-full left-0 bottom-0 bg-[#201c1c] py-8">
      <div className="mx-auto max-w-[1440px] px-10">
        <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-6">
          {/* Left: Company Info */}
          <div className="flex flex-col gap-4">
            <p className="[font-family:'Inter',Helvetica] font-bold text-white text-sm tracking-[0] leading-6 max-w-xs">
              PRS IM Limited, 86 - 90 Paul Street, London EC2A 4NE
            </p>
            <p className="[font-family:'Inter',Helvetica] font-medium text-white text-sm tracking-[0] leading-6">
              © 2026, Bruce. All rights reserved
            </p>
          </div>

          {/* Center: Policy Links */}
          <p className="[font-family:'Inter',Helvetica] font-normal text-white text-sm tracking-[0] leading-6 whitespace-nowrap">
            <span className="font-bold">Terms of Service</span>
            <span className="text-[#4c4747]">&nbsp;&nbsp;|&nbsp;&nbsp;</span>
            <span className="font-bold">Privacy Policy</span>
          </p>

          {/* Right: Social Icons */}
          <div className="flex gap-4 items-center">
            {socialIcons.map((icon, index) => (
              <div key={index} className="w-[37px] h-[38px] flex items-center justify-center">
                <img src={icon.src} alt={icon.alt} className="w-6 h-6" />
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
