from fastapi import FastAPI, UploadFile, File, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
import os
import shutil
import pandas as pd
import psycopg2
from psycopg2.extras import RealDictCursor
from image_processor import processar_imagem  # sua função de edição

# ------------------------
# Configurações do app
# ------------------------
app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Monta a pasta static
static_dir = os.path.join(BASE_DIR, "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# ------------------------
# Conexão com PostgreSQL
# ------------------------
DB_HOST = "dpg-d5sr59vpm1nc73cj6cf0-a.oregon-postgres.render.com"
DB_PORT = 5432
DB_NAME = "origem_iprq"
DB_USER = "origem_iprq_user"
DB_PASS = "NG5yCul6MVyipMEGwSTOf7kUdWPihWgB"

def get_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        cursor_factory=RealDictCursor
    )
    return conn

# ------------------------
# Rota para o HTML
# ------------------------
@app.get("/")
def home():
    return FileResponse(os.path.join(static_dir, "index.html"))

# ------------------------
# Rota para buscar origem
# ------------------------
@app.post("/buscar-origem")
async def buscar_origem(
    pais_suspeito: str = Form(...),
    sobrenomes: str = Form(...)
):
    conn = get_connection()
    cur = conn.cursor()

    # Aqui você pode consultar seus CSVs ou banco PostgreSQL
    # Exemplo: retornar resumo histórico básico
    resumo = f"Suspeita: {pais_suspeito}\nSobrenomes analisados: {sobrenomes}\n\nHistória encontrada baseada nos dados históricos."

    cur.close()
    conn.close()

    return {"resumo": resumo}

# ------------------------
# Rota para processar foto
# ------------------------
@app.post("/processar-foto")
async def processar_foto(foto: UploadFile = File(...)):
    # Salvar temporariamente
    caminho_temp = os.path.join(BASE_DIR, "temp_" + foto.filename)
    with open(caminho_temp, "wb") as buffer:
        shutil.copyfileobj(foto.file, buffer)

    # Processar usando sua função (ex: aplicar filtros, colocar bandeira)
    resultado_path = processar_imagem(caminho_temp)

    return {"imagem_final": resultado_path}


