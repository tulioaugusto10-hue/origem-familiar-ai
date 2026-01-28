from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from sqlalchemy import create_engine, text
import pandas as pd
import os

app = FastAPI()

# 🔓 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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

# 🔗 Conexão com PostgreSQL (Render)
DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://origem_iprq_user:NG5yCul6MVyipMEGwSTOf7kUdWPihWgB@dpg-d5sr59vpm1nc73cj6cf0-a.oregon-postgres.render.com/origem_iprq"
)
engine = create_engine(DATABASE_URL)

# 🔎 API de busca de origem
@app.post("/buscar-origem")
def buscar_origem(
    pais_suspeito: str = Form(...),
    sobrenomes: str = Form(...)
):
    with engine.connect() as conn:
        # Exemplo: buscar continente pelo país
        query = text("SELECT * FROM historia_povos_de_cada_pais WHERE pais ILIKE :pais LIMIT 1")
        resultado = conn.execute(query, {"pais": pais_suspeito}).fetchone()

    if resultado:
        resumo = resultado["resumo"] if "resumo" in resultado.keys() else "Resumo não disponível"
    else:
        resumo = "Nenhum dado encontrado para esse país."

    return {
        "resumo": resumo,
        "pais_suspeito": pais_suspeito,
        "sobrenomes": sobrenomes
    }

# 🔎 API de processamento de foto (simulada)
@app.post("/processar-foto")
async def processar_foto(foto: UploadFile = File(...)):
    return {"status": "Imagem recebida com sucesso"}


