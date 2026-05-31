# FastAPI Migration - Phase 1

This project now includes a parallel backend API using FastAPI.

## Added in this phase

- `backend/main.py`: FastAPI app entrypoint
- `backend/services/bible_service.py`: Bible data/language endpoints support
- `backend/services/ollama_service.py`: Ollama integration
- `backend/models.py`: Request/response schemas
- `start_api.bat`: Windows startup script for API mode

## Run API (Windows)

```bat
start_api.bat
```

## Base URLs

- Health: `http://localhost:8000/health`
- OpenAPI docs: `http://localhost:8000/docs`

## Initial endpoints

- `GET /health`
- `GET /api/meta/languages`
- `GET /api/bible/versions?lang=pt`
- `GET /api/bible/books?lang=pt&version=NVI`
- `GET /api/bible/chapter?lang=pt&version=NVI&book=Genesis&chapter=1`
- `POST /api/ai/exegesis`

Example body for exegesis:

```json
{
  "reference": "Joao 3:16",
  "text": "Porque Deus amou o mundo de tal maneira...",
  "model": "llama3.2:1b",
  "language": "pt"
}
```

## Notes

- Streamlit app remains intact.
- This is a parallel backend to start frontend migration in the next phase.
- Ollama must be running: `ollama serve`.
