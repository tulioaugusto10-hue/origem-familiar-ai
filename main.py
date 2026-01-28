from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI()

# 🔓 CORS (resolve o erro OPTIONS 404)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # depois você pode restringir
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 📂 Servir arquivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

# 🏠 Página inicial
@app.get("/")
def home():
    return FileResponse("static/index.html")

# 🔎 API
@app.get("/buscar-origem")
def buscar_origem(nome: str):
    return {
        "nome": nome,
        "origem": "Origem histórica simulada",
        "significado": "Significado simbólico do sobrenome",
        "regiao": "Região aproximada"
    }
