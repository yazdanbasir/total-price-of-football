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

      <div className="bg-[#151514] p-4 sm:p-8 flex gap-4 sm:gap-8 items-start">
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
        <div className="flex flex-col gap-4 min-w-0 flex-1">
          <p className="text-[20px] font-semibold text-[#EDEBE6] leading-snug">
            Made with love by Yazdan Basir
          </p>
          <div className="flex flex-col gap-4 text-[14px] text-[#666560] leading-relaxed">
            <p>
              I grew up loving football and hating finance. For me, they were the antithesis of each other. Football: tangible, visceral, and evident. Finance: intangible, murky, and entirely made up. Since graduating college, I have been working as a developer at a fintech company and I have, begrudgingly, had to come to terms with many financial concepts and instruments in order to succeed in the basic functions of my role (and avoid getting the sack).
            </p>
            <p>
              What has been remarkably refreshing is how digestible and tolerable Keiran and Kevin manage to make this mazy, labyrinthine industry. I have enjoyed every second of this podcast over the past few years that I have been a regular listener. And I look forward to each episode with the same enthusiasm because I am certain I will walk away with some knowledge gained and some nuances better understood.
            </p>
            <p>
              The inception of this project is three-fold. Firstly and most importantly, I simply wanted to make the knowledge covered on this magnificent podcast more accessible and searchable for all. This is my version of Keiran&apos;s spreadsheets for the many clubs he keeps track of. Secondly (and selfishly), I wanted to make sure I am truly learning and absorbing concepts as I go. I will be honest with you: I still do not understand much of what is discussed on the pod, partly due to having never taken an economics or finance class, partly due to my hesitation to open up to it fully. This website is a reference point for me; when Keiran brings up parachute payments, I can quickly look up what that is. Thirdly (and again somewhat selfishly), I am trying to learn how to work with modern AI tools and models. I have always wanted to do a project like this and thought I could give myself a little challenge this way.
            </p>
            <p>
              The project is open source. The code and transcripts are available for all to peruse. If anyone is interested in helping me improve the quality of the project, feel free to drop an email if you are not a nerd like myself. And if you are, feel free to contribute to the repo and submit a Pull Request :)
            </p>
            <div>
              <p className="text-[#EDEBE6] font-medium mb-2">Things I will be adding soon:</p>
              <ul className="list-disc list-inside flex flex-col gap-1">
                <li>List-style episode summaries so fans/listeners can quickly glance which topics were covered when</li>
                <li>A search/chatbot at the top where you can engage in simple interactions to look up definitions, terms, profiles, or the number of episodes Keiran and Kevin were interrupted by the postman.</li>
                <li>Chronological history of terms and profiles. For example, the Chelsea entry would show a simple timeline of the stories covered on the podcast and major events like Abramovich&apos;s assets getting frozen or the sale of their women&apos;s team to themselves.</li>
              </ul>
            </div>
            <p>
              Much love to Keiran and Kevin. Thank you for making the pod a joy to listen to. God bless you.
            </p>
            <p>
              Disclaimer: all knowledge and content on this site belongs entirely to Keiran Maguire and Kevin Day. I have not created any of it — I have only built the tools to surface it. This project is not monetised in any way and exists purely as a fan-made resource.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
