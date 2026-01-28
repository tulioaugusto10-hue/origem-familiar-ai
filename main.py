from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import shutil
import os

from backend.image_processor import envelhecer_foto

# =====================================================
# PATHS
# =====================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

# =====================================================
# APP
# =====================================================
app = FastAPI(title="API Origem Familiar")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# =====================================================
# CARREGAR BASES CSV
# =====================================================
sobrenomes_pais = pd.read_csv(os.path.join(DATA_DIR, "sobrenomes-por-pais.csv"))
hist_sobrenomes = pd.read_csv(os.path.join(DATA_DIR, "historia-por-tras-de-cada-sobrenome.csv"))
povos_paises = pd.read_csv(os.path.join(DATA_DIR, "povos_origem_paises.csv"))
hist_povos = pd.read_csv(os.path.join(DATA_DIR, "historia-povos-de-cada-pais.csv"))
datas_paises = pd.read_csv(os.path.join(DATA_DIR, "paises_datas_surgimento.csv"))
hist_continentes = pd.read_csv(os.path.join(DATA_DIR, "historia-continentes.csv"))
brasil = pd.read_csv(os.path.join(DATA_DIR, "por-pais-brasil.csv"))

# =====================================================
# MODELS
# =====================================================
class Consulta(BaseModel):
    pais_suspeito: str | None = None
    sobrenomes: str

# =====================================================
# HEALTH CHECK (OBRIGATÓRIO NO RENDER)
# =====================================================
@app.get("/")
def health():
    return {"status": "API Origem Familiar online"}

# =====================================================
# ENDPOINT HISTÓRICO
# =====================================================
@app.post("/buscar-origem")
def buscar_origem(dados: Consulta):

    sobrenomes = [s.strip().title() for s in dados.sobrenomes.split(",")]

    encontrados = sobrenomes_pais[
        sobrenomes_pais["sobrenome"].isin(sobrenomes)
    ]

    if encontrados.empty:
        return {"mensagem": "Nenhum sobrenome encontrado na base histórica."}

    paises_origem = encontrados["pais_origem"].unique().tolist()

    povos = povos_paises[
        povos_paises["pais"].isin(paises_origem)
    ]["povo"].unique().tolist()

    datas = datas_paises[
        datas_paises["pais"].isin(paises_origem)
    ].to_dict(orient="records")

    continentes = hist_continentes[
        hist_continentes["pais"].isin(paises_origem)
    ].to_dict(orient="records")

    historias_sobrenomes = hist_sobrenomes[
        hist_sobrenomes["sobrenome"].isin(sobrenomes)
    ].to_dict(orient="records")

    presenca_brasil = brasil[
        brasil["pais_origem"].isin(paises_origem)
    ].to_dict(orient="records")

    resumo = (
        f"Com base nos registros históricos, há fortes indícios de que sua família "
        f"possui origem em {', '.join(paises_origem)}. "
        f"Os povos historicamente associados a essas regiões incluem: "
        f"{', '.join(povos)}."
    )

    return {
        "resumo": resumo,
        "sobrenomes_consultados": sobrenomes,
        "paises_origem": paises_origem,
        "povos_originarios": povos,
        "datas_surgimento_paises": datas,
        "historia_continentes": continentes,
        "historia_sobrenomes": historias_sobrenomes,
        "presenca_no_brasil": presenca_brasil
    }

# =====================================================
# ENDPOINT DE IMAGEM
# =====================================================
@app.post("/processar-foto")
async def processar_foto(foto: UploadFile = File(...)):

    upload_dir = os.path.join(BASE_DIR, "dados", "uploads")
    output_dir = os.path.join(BASE_DIR, "dados", "processadas")

    os.makedirs(upload_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

    caminho_original = os.path.join(upload_dir, foto.filename)
    caminho_final = os.path.join(output_dir, f"envelhecida_{foto.filename}")

    with open(caminho_original, "wb") as buffer:
        shutil.copyfileobj(foto.file, buffer)

    envelhecer_foto(caminho_original, caminho_final)

    return {
        "mensagem": "Foto processada com sucesso",
        "arquivo_processado": caminho_final
    }


