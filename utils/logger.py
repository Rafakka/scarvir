import json, os
from datetime import datetime
import psycopg2
from dotenv import load_dotenv

# -----------------------------
# Carrega variáveis de ambiente
# -----------------------------
load_dotenv()
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")

# -----------------------------
# Logger para arquivo
# -----------------------------
LOG_PATH = os.path.join("logs", "app.log")
os.makedirs("logs", exist_ok=True)

def log_event(action: str, id_curto: str = None, origem: str = None, success: bool = True, extra: dict = None, err: str = None):
    """
    Registra um evento no arquivo de log e na tabela scanlog do banco.
    """
    rec = {
        "ts": datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "action": action,
        "id_curto": id_curto,
        "origem": origem,
        "success": success,
        "err": err,
        "extra": extra or {}
    }

    # --- Arquivo ---
    try:
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    except Exception as e:
        print(f"Erro ao gravar log em arquivo: {e}")

    # --- Banco ---
    try:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO scanlog (ts, action, id_curto, origem, success, err, extra)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            datetime.utcnow(),
            action,
            id_curto,
            origem,
            success,
            err,
            json.dumps(extra or {})
        ))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Erro ao gravar log no banco: {e}")
