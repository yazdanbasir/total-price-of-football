# Total Price of Football — Claude Guidelines

## Security & Privacy (Priority #1)
This project is committed to a **public GitHub repo** and will be **deployed for public use**. Every piece of code must be written with this in mind.

- **Never commit secrets.** API keys, tokens, and credentials always go in `.env` files which are gitignored. Always use `.env.example` with placeholder values as the committed reference.
- **Never log or expose sensitive data.** No API keys, user data, or file paths that reveal local machine structure in logs or error messages.
- **Cookies and browser data stay local.** The `cookiesfrombrowser` option in yt-dlp reads from the local machine at runtime and is never written to a file or committed.
- **Gitignore is a safety net, not the only defence.** Always think before adding a file — if it could contain sensitive data, it should be gitignored.
- **No hardcoded values.** Any value that differs between local dev and production (URLs, model names, credentials, paths) must come from environment variables.
- **Deployed app must not expose internal errors to users.** Backend errors are logged server-side; user-facing responses get generic messages.
- Before writing any script that touches external services, credentials, or user data — think about what could leak and prevent it proactively.

## Naming Conventions
- **camelCase** everywhere: variables, functions, file names
- **`ID`** (uppercase), never `Id` — e.g. `youtubeID`, `channelID`, `playlistID`
- These conventions apply to Python and JavaScript/TypeScript alike
- External API response keys are kept as-is (e.g. YouTube API returns `channelId` — do not rename those)

## Project Structure
```
total-price-of-football/
├── pipeline/       # Scraping, transcription, and analysis scripts (Python)
├── backend/        # FastAPI app (Python)
├── frontend/       # React app (JavaScript/TypeScript)
```

## Stack
- **Frontend:** React on Vercel
- **Backend:** Python FastAPI on Railway
- **Database:** PostgreSQL + pgvector on Railway
- **Transcription:** OpenAI Whisper (local)
- **LLM — bulk analysis:** Claude Haiku
- **LLM — chatbot:** Claude Sonnet
- **Scraping:** YouTube Data API v3 + yt-dlp

## Pipeline Data Directories (gitignored)
- `pipeline/data/` — JSON metadata files
- `pipeline/audio/` — downloaded MP3 files
- `pipeline/transcripts/` — Whisper transcript output
