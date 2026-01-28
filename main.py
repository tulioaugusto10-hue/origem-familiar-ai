from fastapi import FastAPI, Form, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI()

# 🔓 CORS (resolve OPTIONS / erro 404)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 📂 Arquivos estáticos (HTML, CSS, JS)
app.mount("/static", StaticFiles(directory="backend/static"), name="static")

# 🏠 Página inicial
@app.get("/")
def home():
    return FileResponse("backend/static/index.html")

# 🔎 API principal (POST)
@app.post("/descendencia")
async def descendencia(
    sobrenome: str = Form(...),
    foto: UploadFile | None = File(None)
):
    return {
        "sobrenome": sobrenome,
        "mensagem": f"O sobrenome {sobrenome} possui origem histórica registrada.",
        "foto_recebida": foto is not None
    }
