export default function AboutPage() {
  return (
    <div className="max-w-6xl mx-auto px-6 py-12">
      <div className="mb-10">
        <h1
          className="text-[clamp(30px,6vw,72px)] font-black uppercase leading-[0.9] text-[#EDEBE6]"
          style={{ fontFamily: "var(--font-barlow)" }}
        >
          About
        </h1>
        <p className="text-[12px] uppercase tracking-[0.18em] text-[#444440] mt-4">
          The story behind the project
        </p>
      </div>

      <div className="bg-[#151514] p-4 sm:p-8 flex gap-4 sm:gap-8 items-center">
        <div
          className="shrink-0 bg-[#FFE200] flex items-center justify-center w-12 h-12 sm:w-16 sm:h-16"
        >
          <span
            className="text-[22px] sm:text-[28px] font-black text-black tabular-nums leading-none"
            style={{ fontFamily: "var(--font-barlow)" }}
          >
            1
          </span>
        </div>
        <div className="flex flex-col gap-2 min-w-0 flex-1">
          <p className="text-[20px] font-semibold text-[#EDEBE6] leading-snug">
            About the Project
          </p>
          <p className="text-[14px] text-[#666560] leading-relaxed">
            The story behind Total Price of Football.
          </p>
        </div>
      </div>
    </div>
  );
}
