import psycopg2
from datetime import datetime

def get_connection():
    return psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="link217",
        host="localhost",
        port="5432"
    )

def find_person(cursor, method, value):
    if method == "cpf":
        cursor.execute("SELECT id, nome FROM pessoas WHERE cpf = %s", (value,))
    elif method == "qrcode":
        cursor.execute("SELECT id, nome FROM pessoas WHERE qrcode = %s", (value,))
    else:  # short_id
        cursor.execute("SELECT id, nome FROM pessoas WHERE short_id = %s", (value,))
    return cursor.fetchone()

def find_vaccine(cursor, method, value):
    if method == "nome":
        cursor.execute("SELECT id, nome FROM vacinas WHERE nome ILIKE %s", (f"%{value}%",))
    elif method == "qrcode":
        cursor.execute("SELECT id, nome FROM vacinas WHERE qrcode = %s", (value,))
    else:  # short_id
        cursor.execute("SELECT id, nome FROM vacinas WHERE short_id = %s", (value,))
    return cursor.fetchone()

def register_dose(cursor, pessoa_id, vacina_id):
    cursor.execute("""
        INSERT INTO doses_aplicadas (pessoa_id, vacina_id, data_aplicacao)
        VALUES (%s, %s, %s)
    """, (pessoa_id, vacina_id, datetime.now()))

def orquestrador_vacina():
    conn = get_connection()
    cur = conn.cursor()

    print("\n=== ORQUESTRADOR DE VACINA ===")

    # --- Identificação da pessoa ---
    metodo_pessoa = input("Identificar pessoa por [cpf/qrcode/id]: ").strip().lower()
    valor_pessoa = input(f"Digite o {metodo_pessoa}: ").strip()

    pessoa = find_person(cur, metodo_pessoa, valor_pessoa)
    if not pessoa:
        print("❌ Pessoa não encontrada.")
        return
    pessoa_id, pessoa_nome = pessoa
    print(f"✅ Pessoa encontrada: {pessoa_nome}")

    # --- Identificação da vacina ---
    metodo_vacina = input("Identificar vacina por [nome/qrcode/id]: ").strip().lower()
    valor_vacina = input(f"Digite o {metodo_vacina}: ").strip()

    vacina = find_vaccine(cur, metodo_vacina, valor_vacina)
    if not vacina:
        print("❌ Vacina não encontrada.")
        return
    vacina_id, vacina_nome = vacina
    print(f"💉 Vacina localizada: {vacina_nome}")

    # --- Registro ---
    register_dose(cur, pessoa_id, vacina_id)
    conn.commit()
    print(f"✅ Vacina {vacina_nome} aplicada com sucesso para {pessoa_nome}.")

    cur.close()
    conn.close()

if __name__ == "__main__":
    orquestrador_vacina()
