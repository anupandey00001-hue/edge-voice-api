from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import edge_tts
import base64
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AudioRequest(BaseModel):
    text: str
    voice: str = "hi-IN-SwaraNeural"

@app.post("/api/edge")
async def generate_edge_audio(req: AudioRequest):
    temp_file = "/tmp/temp_audio.mp3" 
    
    communicate = edge_tts.Communicate(req.text, req.voice)
    await communicate.save(temp_file)
    
    with open(temp_file, "rb") as f:
        audio_data = base64.b64encode(f.read()).decode("utf-8")
        
    os.remove(temp_file)
    return {"audio_base64": audio_data}
