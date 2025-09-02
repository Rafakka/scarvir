from gerenciador_db import conectar_bd


def verificar_id_no_banco():
    """Verifica todos os IDs curtos no banco"""
    conn = conectar_bd()
    if not conn:
        return
    
    try:
        cur = conn.cursor()
        cur.execute("SELECT id_curto, nome FROM pessoas")
        resultados = cur.fetchall()
        
        print("📊 IDs curtos no banco:")
        print("-" * 40)
        for id_curto, nome in resultados:
            print(f"{id_curto} - {nome}")
        
        cur.close()
        conn.close()
        
    except Exception as e:
        print("Erro ao buscar IDs:", e)

# Execute para ver o que está no banco
verificar_id_no_banco()