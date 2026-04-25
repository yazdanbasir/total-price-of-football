# Total Price of Football

A searchable knowledge base built from the [Total Football Analysis](https://www.youtube.com/@TotalFootballAnalysis) podcast, hosted by Keiran Maguire and Kevin Day.

## About the Project

I grew up loving football and hating finance. For me, they were the antithesis of each other. Football: tangible, visceral, and evident. Finance: intangible, murky, and entirely made up. Since graduating college, I have been working as a developer at a fintech company and I have, begrudgingly, had to come to terms with many financial concepts and instruments in order to succeed in the basic functions of my role (and avoid getting the sack).

What has been remarkably refreshing is how digestible and tolerable Keiran and Kevin manage to make this mazy, labyrinthine industry. I have enjoyed every second of this podcast over the past few years that I have been a regular listener. And I look forward to each episode with the same enthusiasm because I am certain I will walk away with some knowledge gained and some nuances better understood.

The inception of this project is three-fold. Firstly and most importantly, I simply wanted to make the knowledge covered on this magnificent podcast more accessible and searchable for all. This is my version of Keiran's spreadsheets for the many clubs he keeps track of. Secondly (and selfishly), I wanted to make sure I am truly learning and absorbing concepts as I go. I will be honest with you: I still do not understand much of what is discussed on the pod, partly due to having never taken an economics or finance class, partly due to my hesitation to open up to it fully. This website is a reference point for me; when Keiran brings up parachute payments, I can quickly look up what that is. Thirdly (and again somewhat selfishly), I am trying to learn how to work with modern AI tools and models. I have always wanted to do a project like this and thought I could give myself a little challenge this way.

The project is open source. The code and transcripts are available for all to peruse. If anyone is interested in helping me improve the quality of the project, feel free to drop an email if you are not a nerd like myself. And if you are, feel free to contribute to the repo and submit a Pull Request :)

### Coming Soon

- List-style episode summaries so fans/listeners can quickly glance which topics were covered when
- A search/chatbot at the top where you can engage in simple interactions to look up definitions, terms, profiles, or the number of episodes Keiran and Kevin were interrupted by the postman.
- Chronological history of terms and profiles. For example, the Chelsea entry would show a simple timeline of the stories covered on the podcast and major events like Abramovich's assets getting frozen or the sale of their women's team to themselves.

## Stack

- **Frontend:** React / Next.js on Vercel
- **Backend:** Python FastAPI on Railway
- **Database:** PostgreSQL + pgvector on Railway
- **Transcription:** mlx-whisper (`mlx-community/whisper-large-v3-turbo`)
- **LLM:** Claude Haiku (bulk analysis) + Claude Sonnet (chatbot)
- **Scraping:** YouTube Data API v3 + yt-dlp

## Contributing

Feel free to open an issue or submit a Pull Request. All contributions welcome.
