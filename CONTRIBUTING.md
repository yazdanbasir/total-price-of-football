# Contributing to Total Price of Football

Thanks for your interest in contributing. Here's how to get the project running locally.

## Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL (or a Railway instance)
- An Apple Silicon Mac for the transcription pipeline (uses mlx-whisper with MLX)
- API keys — see the setup steps below

## Project structure

```
pipeline/   # Data pipeline: scraping, transcription, analysis
backend/    # FastAPI backend
frontend/   # Next.js frontend
```

## Setup

### 1. Clone and install dependencies

```bash
git clone https://github.com/your-username/total-price-of-football.git
cd total-price-of-football

# Backend
cd backend && pip install -r requirements.txt && cd ..

# Pipeline
cd pipeline && pip install -r requirements.txt && cd ..

# Frontend
cd frontend && npm install && cd ..
```

### 2. Configure environment variables

Each part of the project has its own `.env.example` file. Copy each one and fill in your own credentials:

```bash
cp pipeline/.env.example pipeline/.env
cp backend/.env.example backend/.env
cp frontend/.env.local.example frontend/.env.local
```

You'll need:
- A [YouTube Data API v3](https://console.cloud.google.com/) key (for scraping episode metadata)
- An [Anthropic API key](https://console.anthropic.com/) (for analysis and the chatbot)
- A PostgreSQL database (e.g. a free Railway instance)

### 3. Run the pipeline (optional — to build your own dataset)

The pipeline scripts run in order:

```bash
cd pipeline
python scrape/fetchEpisodes.py        # fetch episode metadata
python scrape/downloadAudio.py        # download MP3s
python transcribe/transcribeEpisodes.py  # transcribe with mlx-whisper (Apple Silicon only)
python analyze/analyzeEpisodes.py     # extract concepts/profiles/stories via Claude Haiku
python analyze/aggregateAnalysis.py   # merge into data/ output files
```

Each script is skip-safe — re-running it will skip already-completed episodes.

> **Note:** Transcription requires an Apple Silicon Mac. The project uses `mlx-whisper` with the `mlx-community/whisper-large-v3-turbo` model. `openai-whisper` and `faster-whisper` are not compatible due to MPS float64 issues on Apple Silicon.

### 4. Run locally

```bash
# Backend (from the backend/ directory)
uvicorn main:app --reload

# Frontend (from the frontend/ directory)
npm run dev
```

## Code conventions

- **camelCase** for all variable, function, and file names
- **`ID`** (uppercase) not `Id` — e.g. `youtubeID`, `channelID`
- No secrets in code — all credentials go in `.env` files

## Submitting changes

1. Fork the repo and create a branch from `main`
2. Make your changes
3. Open a pull request with a clear description of what you changed and why
