import os
from typing import Optional, Dict, Any, List
from gerenciador_db import get_pessoa_por_qr_camera, get_pessoa_por_qr_imagem, get_pessoa_por_id_curto, get_pessoa_por_cpf

def consulta_pessoas():
    """Sistema de consulta de pessoas e vacinas"""
    
    print("🔍 SISTEMA DE CONSULTA DE PESSOAS E VACINAS")
    print("=" * 50)
    
    while True:
        pessoa = encontrar_pessoa_consulta()
        if not pessoa:
            break
        
        # Mostra dados da pessoa e vacinas
        mostrar_dados_completos(pessoa)
        
        # Pergunta se quer consultar outra pessoa
        if not perguntar_nova_consulta():
            break

def encontrar_pessoa_consulta() -> Optional[Dict[str, Any]]:
    """Encontra pessoa para consulta"""
    
    while True:
        print("\n🔍 Como deseja buscar a pessoa?")
        print("1 - QR Code (câmera)")
        print("2 - QR Code (imagem)")
        print("3 - ID Curto")
        print("4 - CPF")
        print("0 - Sair do sistema")
        
        opcao = input("Opção: ").strip()
        
        if opcao == '0':
            return None
        
        elif opcao == '1':
            pessoa = get_pessoa_por_qr_camera()
            if pessoa:
                return pessoa
            print("❌ Não encontrado via câmera. Tente outro método.")
        
        elif opcao == '2':
            caminho = input("Caminho da imagem QR: ").strip()
            pessoa = get_pessoa_por_qr_imagem(caminho)
            if pessoa:
                return pessoa
            print("❌ Não encontrado na imagem. Tente outro método.")
        
        elif opcao == '3':
            id_curto = input("ID Curto: ").strip()
            pessoa = get_pessoa_por_id_curto(id_curto)
            if pessoa:
                return pessoa
            print("❌ ID não encontrado. Tente outro método.")
        
        elif opcao == '4':
            cpf = input("CPF: ").strip()
            pessoa = get_pessoa_por_cpf(cpf)
            if pessoa:
                return pessoa
            print("❌ CPF não encontrado. Tente outro método.")
        
        else:
            print("❌ Opção inválida.")

def mostrar_dados_completos(pessoa: Dict[str, Any]):
    """Mostra dados da pessoa + vacinas tomadas"""
    
    print("\n" + "=" * 60)
    print("📋 DADOS DA PESSOA")
    print("=" * 60)
    print(f"👤 Nome: {pessoa['nome']}")
    print(f"🎂 Data de Nascimento: {pessoa['dob']}")
    print(f"📄 CPF: {pessoa['id_documento']}")
    print(f"🔖 ID Curto: {pessoa['id_curto']}")
    print(f"📅 Data de Cadastro: {pessoa['data_de_criacao']}")
    
    # Busca vacinas aplicadas
    vacinas = buscar_vacinas_pessoa(pessoa['id'])
    
    print(f"\n💉 VACINAS APLICADAS: {len(vacinas)} dose(s)")
    print("-" * 40)
    
    if vacinas:
        for i, vacina in enumerate(vacinas, 1):
            print(f"{i}. {vacina['nome_vacina']}")
            print(f"   Fabricante: {vacina['fabricante']}")
            print(f"   Lote: {vacina['lote']}")
            print(f"   Data: {vacina['data_de_aplicacao']}")
            print(f"   Vacinador: {vacina['vacinador']}")
            print(f"   Dose: {vacina['dose_numero']}")
            print()
    else:
        print("❌ Nenhuma vacina aplicada ainda.")
    
    # Estatísticas
    total_doses = sum(v['dose_numero'] for v in vacinas)
    print(f"📊 Total de doses: {total_doses}")
    print("=" * 60)

def buscar_vacinas_pessoa(pessoa_id: int) -> List[Dict[str, Any]]:
    """Busca todas as vacinas aplicadas a uma pessoa"""
    
    conn = conectar_bd()
    if not conn:
        return []
    
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT 
                v.nome as nome_vacina,
                v.fabricante,
                v.lote,
                da.data_de_aplicacao,
                da.vacinador,
                da.numero_doses as dose_numero
            FROM doses_aplicadas da
            JOIN vacinas v ON da.id_vacina = v.id
            WHERE da.id_pessoa = %s
            ORDER BY da.data_de_aplicacao DESC
        """, (pessoa_id,))
        
        vacinas = []
        for row in cur.fetchall():
            vacinas.append({
                "nome_vacina": row[0],
                "fabricante": row[1],
                "lote": row[2],
                "data_de_aplicacao": row[3].strftime("%d/%m/%Y %H:%M") if row[3] else "N/A",
                "vacinador": row[4],
                "dose_numero": row[5]
            })
        
        cur.close()
        conn.close()
        return vacinas
        
    except Exception as e:
        print(f"❌ Erro ao buscar vacinas: {e}")
        return []

def perguntar_nova_consulta() -> bool:
    """Pergunta se quer consultar outra pessoa"""
    
    while True:
        resposta = input("\n🔍 Consultar outra pessoa? (s/n): ").strip().lower()
        if resposta in ['s', 'sim']:
            return True
        elif resposta in ['n', 'não', 'nao', '0']:
            print("👋 Retornando ao menu...")
            return False
        else:
            print("❌ Resposta inválida. Digite 's' ou 'n'.")

def conectar_bd():
    """Conexão com banco de dados"""
    try:
        import psycopg2
        return psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST")
        )
    except Exception as e:
        print("❌ Erro ao conectar ao banco:", e)
        return None

def menu_consultas():
    """Menu principal do sistema de consultas"""
    
    while True:
        print("\n" + "=" * 50)
        print("🏥 SISTEMA DE CONSULTAS")
        print("=" * 50)
        print("1 - Consultar pessoa e vacinas")
        print("2 - Listar todas as vacinas cadastradas")
        print("3 - Estatísticas gerais")
        print("0 - Sair")
        
        opcao = input("Opção: ").strip()
        
        if opcao == '0':
            print("👋 Saindo...")
            break
        
        elif opcao == '1':
            consulta_pessoas()
        
        elif opcao == '2':
            listar_todas_vacinas()
        
        elif opcao == '3':
            mostrar_estatisticas()
        
        else:
            print("❌ Opção inválida")

def listar_todas_vacinas():
    """Lista todas as vacinas cadastradas no sistema"""
    
    conn = conectar_bd()
    if not conn:
        return
    
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT id, nome, fabricante, doses_necessarias, lote, validade
            FROM vacinas 
            ORDER BY nome
        """)
        
        vacinas = cur.fetchall()
        cur.close()
        conn.close()
        
        print(f"\n💉 VACINAS CADASTRADAS: {len(vacinas)}")
        print("=" * 50)
        
        for vacina in vacinas:
            print(f"ID: {vacina[0]}")
            print(f"Nome: {vacina[1]}")
            print(f"Fabricante: {vacina[2]}")
            print(f"Doses: {vacina[3]}")
            print(f"Lote: {vacina[4]}")
            print(f"Validade: {vacina[5]}")
            print("-" * 30)
            
    except Exception as e:
        print(f"❌ Erro ao listar vacinas: {e}")

def mostrar_estatisticas():
    """Mostra estatísticas gerais do sistema"""
    
    conn = conectar_bd()
    if not conn:
        return
    
    try:
        cur = conn.cursor()
        
        # Total de pessoas
        cur.execute("SELECT COUNT(*) FROM pessoas")
        total_pessoas = cur.fetchone()[0]
        
        # Total de vacinas aplicadas
        cur.execute("SELECT COUNT(*) FROM doses_aplicadas")
        total_doses = cur.fetchone()[0]
        
        # Total de vacinas cadastradas
        cur.execute("SELECT COUNT(*) FROM vacinas")
        total_vacinas = cur.fetchone()[0]
        
        # Pessoa com mais vacinas
        cur.execute("""
            SELECT p.nome, COUNT(da.id) as total_doses
            FROM pessoas p
            LEFT JOIN doses_aplicadas da ON p.id = da.id_pessoa
            GROUP BY p.id, p.nome
            ORDER BY total_doses DESC
            LIMIT 1
        """)
        pessoa_mais_vacinas = cur.fetchone()
        
        cur.close()
        conn.close()
        
        print("\n📊 ESTATÍSTICAS DO SISTEMA")
        print("=" * 40)
        print(f"👥 Total de pessoas: {total_pessoas}")
        print(f"💉 Total de doses aplicadas: {total_doses}")
        print(f"🏭 Total de vacinas cadastradas: {total_vacinas}")
        
        if pessoa_mais_vacinas and pessoa_mais_vacinas[1] > 0:
            print(f"👑 Pessoa com mais vacinas: {pessoa_mais_vacinas[0]} ({pessoa_mais_vacinas[1]} doses)")
        else:
            print("👑 Nenhuma vacina aplicada ainda")
            
    except Exception as e:
        print(f"❌ Erro ao buscar estatísticas: {e}")

# Execução principal
if __name__ == "__main__":
    menu_consultas()