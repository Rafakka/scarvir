import psycopg2

def get_pessoa_por_id(pessoa_id):
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="link217",
            host="localhost"
        )
        cur = conn.cursor()
        cur.execute("""
            SELECT id, nome, dob, id_documento, data_de_criacao
            FROM pessoas
            WHERE id = %s
        """, (pessoa_id,))
        pessoa = cur.fetchone()
        cur.close()
        conn.close()
        return pessoa
    except Exception as e:
        print("Erro ao buscar pessoa:", e)
        return None
