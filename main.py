import psycopg2

def get_conn():
    return psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="link217",
        host="localhost",
        port="5432"
    )

# teste
if __name__ == "__main__":
    conn = get_conn()
    print("Conectado ao banco com sucesso!")
    conn.close()
