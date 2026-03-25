export const RentersRightsDetailsSection = (): JSX.Element => {
  return (
    <div className="absolute top-[1280px] left-[calc(50.00%_-_720px)] w-[1440px] h-[648px] flex justify-center bg-[#f5f1e4]">
      <div className="w-[1403px] h-[648px] ml-[-37px] relative">
        <div className="absolute top-[194px] left-[calc(50.00%_+_146px)] [font-family:'Inter',Helvetica] font-bold text-text text-5xl tracking-[0] leading-[74px] whitespace-nowrap">
          The Renters&#39; Rights Act
        </div>

        <p className="absolute top-[153px] left-[850px] [font-family:'Inter',Helvetica] font-normal text-[#6c6c6c] text-[32px] tracking-[0] leading-[normal]">
          A New Era for Renters
        </p>

        <img
          className="absolute top-0 left-0 w-[709px] h-[648px] aspect-[1.09]"
          alt="Im"
          src="/img/im.png"
        />

        <p className="absolute top-[275px] left-[calc(50.00%_+_148px)] w-[508px] [font-family:'Inter',Helvetica] font-normal text-text text-lg tracking-[0] leading-[26px]">
          On 1 May 2026, the Renters&#39; Rights Act will become law in England.
          This landmark legislation represents the biggest shake-up of the
          English rental market in 40 years, granting tenants new powers to
          challenge unfair rental practices and assert their rights.
        </p>

        <div className="absolute top-[464px] left-[850px] w-[459px] h-8 flex gap-3.5">
          <p className="flex items-center mt-[5px] w-[411px] h-6 [font-family:'Inter',Helvetica] font-semibold text-text text-xl tracking-[-0.50px] leading-6 whitespace-nowrap">
            Find Out More About The Renters&#39; Rights Act
          </p>

          <div className="w-8 h-8 flex">
            <img
              className="flex-1 w-[26.67px]"
              alt="Vector"
              src="/img/vector-13.svg"
            />
          </div>
        </div>
      </div>
    </div>
  );
};
