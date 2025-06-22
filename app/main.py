from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .event_fetcher import fetch_full_redacted_event

app = FastAPI(title="histrogussr")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/event")
def get_event():
    event = fetch_full_redacted_event()
    if not event:
        return {"error": "shit got fucked"}
    return event

