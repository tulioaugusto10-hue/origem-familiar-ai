from fastapi import FastAPI, Form, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files
app.mount("/static", StaticFiles(directory="backend/static"), name="static")

@app.get("/")
def home():
    return FileResponse("backend/static/index.html")

@app.post("/descendencia")
async def descendencia(
    sobrenome: str = Form(...),
    foto: UploadFile | None = File(None)
):
    return {
        "sobrenome": sobrenome,
        "origem": "Origem histórica simulada",
        "foto_recebida": foto is not None
    }

