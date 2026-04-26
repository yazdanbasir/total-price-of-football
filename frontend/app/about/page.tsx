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
          <p className="text-[24px] font-semibold text-[#EDEBE6] leading-snug">
            Made with love by Yazdan Basir
          </p>
          <div className="flex flex-col gap-4 text-[17px] text-[#666560] leading-relaxed">
            <p>
              I grew up loving football and hating finance. For me, they were the antithesis of each other. Football: tangible, visceral, and evident. Finance: intangible, murky, and entirely made up. Since graduating college, I have been working as a developer at a fintech company and I have, begrudgingly, had to come to terms with many financial concepts and instruments in order to succeed in the basic functions of my role (and avoid getting the sack).
            </p>
            <p>
              What has been remarkably refreshing is how digestible and tolerable Kieran and Kevin manage to make this mazy, labyrinthine industry. I have enjoyed every second of this podcast over the past few years that I have been a regular listener. And I look forward to each episode with the same enthusiasm because I am certain I will walk away with some knowledge gained and some nuances better understood.
            </p>
            <p>
              The inception of this project is three-fold. Firstly and most importantly, I simply wanted to make the knowledge covered on this magnificent podcast more accessible and searchable for all. This is my version of Kieran&apos;s spreadsheets for the many clubs he keeps track of. Secondly (and selfishly), I wanted to make sure I am truly learning and absorbing concepts as I go. I will be honest with you: I still do not understand much of what is discussed on the pod, partly due to having never taken an economics or finance class, partly due to my hesitation to open up to it fully. This website is a reference point for me; when Kieran brings up parachute payments, I can quickly look up what that is. Thirdly (and again somewhat selfishly), I am trying to learn how to work with modern AI tools and models. I have always wanted to do a project like this and thought I could give myself a little challenge this way.
            </p>
            <p>
              The project is open source. The code and transcripts are available for all to peruse. If anyone is interested in helping me improve the quality of the project, feel free to drop an email if you are not a nerd like myself. And if you are, feel free to contribute to the repo and submit a Pull Request :)
            </p>
            <div>
              <p className="text-[#EDEBE6] font-medium mb-2">Things I will be adding soon:</p>
              <ul className="list-disc list-inside flex flex-col gap-1">
                <li>List-style episode summaries so fans/listeners can quickly glance which topics were covered when</li>
                <li>A search/chatbot at the top where you can engage in simple interactions to look up definitions, terms, profiles, or the number of episodes Kieran and Kevin were interrupted by the postman.</li>
                <li>Chronological history of terms and profiles. For example, the Chelsea entry would show a simple timeline of the stories covered on the podcast and major events like Abramovich&apos;s assets getting frozen or the sale of their women&apos;s team to themselves.</li>
              </ul>
            </div>
            <p>
              Much love to Kieran and Kevin. Thank you for making the pod a joy to listen to. God bless you.
            </p>
            <p>
              Disclaimer: all knowledge and content on this site belongs entirely to Kieran Maguire and Kevin Day. I have not created any of it — I have only built the tools to surface it. This project is not monetised in any way and exists purely as a fan-made resource.
            </p>
            <a
              href="https://github.com/yazdanbasir/total-price-of-football"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-2 text-[#CA9B52] hover:text-[#FFE200] transition-colors"
            >
              <svg viewBox="0 0 24 24" fill="currentColor" className="w-5 h-5 shrink-0" aria-hidden="true">
                <path d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0 1 12 6.844a9.59 9.59 0 0 1 2.504.337c1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.02 10.02 0 0 0 22 12.017C22 6.484 17.522 2 12 2z"/>
              </svg>
              github.com/yazdanbasir/total-price-of-football
            </a>
          </div>
        </div>
      </div>
    </div>
  );
}
