export const MainHeaderSection = (): JSX.Element => {
  return (
    <header className="absolute top-6 left-[calc(50.00%_-_720px)] w-[1440px] h-20 flex items-center bg-white rounded-[13px] overflow-hidden shadow-[0px_10px_33px_#b5b5b530]">
      <img className="h-10 w-[119px] ml-7" alt="Logo" src="/img/logo-1.png" />

      <nav className="flex items-center flex-1">
        <div className="mt-px h-[19px] w-[84px] ml-[407px] [font-family:'Inter',Helvetica] font-bold text-text text-base tracking-[0] leading-[normal] whitespace-nowrap">
          ABOUT US
        </div>

        <div className="mt-px h-[19px] w-[180px] ml-[33px] [font-family:'Inter',Helvetica] font-normal text-text text-base tracking-[0] leading-[normal] whitespace-nowrap">
          RENTERS REFORM BILL
        </div>
      </nav>

      <div className="flex items-center ml-auto mr-4">
        <div className="h-11 w-[79px] flex items-center justify-center rounded-[60px] overflow-hidden cursor-pointer">
          <div className="mt-px h-[19px] ml-px w-[42px] [font-family:'Inter',Helvetica] font-normal text-text text-base text-center tracking-[0] leading-[normal] whitespace-nowrap">
            Login
          </div>
        </div>

        <div className="h-12 w-[138px] ml-3 flex items-center justify-center bg-[#ff6e42] rounded-lg overflow-hidden cursor-pointer">
          <div className="mt-px h-[19px] w-[84px] [font-family:'Inter',Helvetica] font-bold text-text text-base text-center tracking-[0] leading-[normal] whitespace-nowrap">
            Try it FREE
          </div>
        </div>
      </div>
    </header>
  );
};
