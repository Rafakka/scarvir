
from dotenv import load_dotenv
from utils.conector_bd import conectar_bd

load_dotenv()

def cadastrar_vacina():
    """Cadastra uma vacina manualmente no banco."""
    nome = input("Nome da vacina: ").strip()
    fabricante = input("Fabricante: ").strip()
    lote = input("Lote: ").strip()
    validade = input("Validade (AAAA-MM-DD): ").strip()
    vacinador = input("Vacinador responsável: ").strip()
    doses_necessarias = input("Número total de doses necessárias: ").strip()

    conn = conectar_bd()
    if not conn:
        return None

    try:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO vacinas (nome, fabricante, lote, validade, vacinador, doses_necessarias)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id;
        """, (nome, fabricante, lote, validade, vacinador, doses_necessarias))
        vac_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        print(f"\n✅ Vacina cadastrada com sucesso! ID: {vac_id}")
        return vac_id
    except Exception as e:
        print("Erro ao cadastrar vacina:", e)
        return None