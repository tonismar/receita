from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.services import Receita

app = FastAPI()

class Fisica(BaseModel):
    cpf: str
    nasc: str

@app.post("/cpf")
async def get_cpf(fisica: Fisica):
    try:
        query = Receita(fisica.cpf, fisica.nasc)
        result = await query.check_cpf()
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))