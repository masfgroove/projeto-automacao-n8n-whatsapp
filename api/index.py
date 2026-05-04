from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import requests
import sqlite3

app = FastAPI()

# Permite que o seu cadastro.html (que roda em outra porta) acesse esta API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializa o banco de dados SQLite
def init_db():
    conn = sqlite3.connect('clientes.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            cpf TEXT,
            telefone TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.get("/")
def home():
    return {"message": "API Python com Banco de Dados e n8n Local!"}

@app.post("/api/enviar")
async def enviar_dados(request: Request):
    corpo = await request.json()
    nome = corpo.get("nome")
    cpf = corpo.get("cpf")
    telefone = corpo.get("telefone")
    
    # 1. Salva no banco de dados local (clientes.db)
    try:
        conn = sqlite3.connect('clientes.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO usuarios (nome, cpf, telefone) VALUES (?, ?, ?)", (nome, cpf, telefone))
        conn.commit()
        conn.close()
    except Exception as e:
        return {"erro": f"Erro ao salvar no banco: {str(e)}"}

    # 2. Envia para o n8n local (URL de Produção)
    # Note que agora usamos o endereço local do seu computador
    N8N_URL = "http://localhost:5678/webhook/registro-cliente"
    
    try:
        envio = requests.post(N8N_URL, json=corpo)
        return {
            "status": "Gravado no Banco e enviado ao n8n!",
            "resposta_n8n": envio.status_code,
            "dados": corpo
        }
    except Exception as e:
        return {"aviso": "Salvo no banco, mas o n8n não respondeu. Verifique se está 'Active'."}