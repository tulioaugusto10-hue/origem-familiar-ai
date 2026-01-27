from fastapi import FastAPI, UploadFile, File, Form
import pandas as pd

app = FastAPI()

# Carregar CSVs (quando você subir eles, o caminho será 'backend/data/sobrenomes.csv')
df_sobrenomes = pd.DataFrame()  # placeholder
df_paises = pd.DataFrame()
df_continentes = pd.DataFrame()

@app.post("/descendencia")
async def descendencia(sobrenome: str = Form(...), foto: UploadFile = File(...)):
    # Exemplo mínimo, ainda sem dados
    return {"mensagem": f"Sobrenome recebido: {sobrenome}"}
