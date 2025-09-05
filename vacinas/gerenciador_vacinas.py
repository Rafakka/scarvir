from datetime import date, datetime
from typing import Any, Dict, Optional
from dotenv import load_dotenv
from qr_vacinas import ler_qr_camera_vacina, ler_qr_imagem_vacina
from utils.conector_bd import conectar_bd

load_dotenv()

def _dict_vacina(row):
    if not row:
        return None
    
    validade = row[5]
    
    if isinstance(validade, date):
        validade = validade.isoformat()
    
    return {
        "id": row[0],
        "doses_necessarias": row[1],
        "lote": row[2],
        "nome": row[3],
        "fabricante": row[4],
        "validade": validade,
        "vacinador": row[6]
    }


def get_vacina_por_id(vacina_id):
    conn = conectar_bd()
    if not conn:
        return None
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT id, doses_necessarias, lote, nome, fabricante, validade, vacinador
            FROM vacinas
            WHERE id = %s
        """, (vacina_id,))
        row = cur.fetchone()
        cur.close()
        conn.close()
        return _dict_vacina(row)
    except Exception as e:
        print("Erro ao buscar vacina por ID:", e)
        return None

def get_vacina_por_nome(nome):
    conn = conectar_bd()
    if not conn:
        return None
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT id, doses_necessarias, lote, nome, fabricante, validade, vacinador
            FROM vacinas
            WHERE nome ILIKE %s
            LIMIT 1
        """, (nome,))
        row = cur.fetchone()
        cur.close()
        conn.close()
        return _dict_vacina(row)
    except Exception as e:
        print("Erro ao buscar vacina por nome:", e)
        return None
    
def registrar_dose(pessoa_id, vacina_id, nome_vacinador, data_aplicacao=None):
    if data_aplicacao is None:
        data_aplicacao = datetime.now()

    conn = conectar_bd()
    if not conn:
        return False
    try:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO doses_aplicadas (id_pessoa, id_vacina, numero_doses, data_de_aplicacao, qr_code, vacinador)
            VALUES (%s, %s, 1, %s, NULL, %s)
        """, (pessoa_id, vacina_id, data_aplicacao, nome_vacinador))
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print("Erro ao registrar dose:", e)
        return False

def encontrar_vacina() -> Optional[Dict[str, Any]]:
    """Encontra vacina por QR, ID ou nome"""
    
    while True:
        print("\n🔍 Buscar vacina por:")
        print("1 - QR Code (câmera)")
        print("2 - QR Code (imagem)")
        print("3 - ID da vacina")
        print("4 - Nome da vacina")
        print("0 - Voltar")
        
        opcao = input("Opção: ").strip()
        
        if opcao == '0':
            return None
        
        elif opcao == '1':
            # Usando sua função get_vacina_por_qr adaptada
            from vacinas.gerenciador_vacinas import get_vacina_por_qr
            conteudo_qr = ler_qr_camera_vacina()
            if conteudo_qr:
                vacina = get_vacina_por_qr(conteudo_qr)
                if vacina:
                    return vacina
            print("❌ Vacina não encontrada via QR.")
        
        elif opcao == '2':
            caminho = input("Caminho da imagem QR: ").strip()
            from vacinas.gerenciador_vacinas import get_vacina_por_qr
            conteudo_qr = ler_qr_imagem_vacina(caminho)
            if conteudo_qr:
                vacina = get_vacina_por_qr(conteudo_qr)
                if vacina:
                    return vacina
            print("❌ Vacina não encontrada na imagem.")
        
        elif opcao == '3':
            vacina_id = input("ID da vacina: ").strip()
            vacina = get_vacina_por_id(vacina_id)
            if vacina:
                return vacina
            print("❌ Vacina não encontrada.")
        
        elif opcao == '4':
            nome_vacina = input("Nome da vacina: ").strip()
            vacina = get_vacina_por_nome(nome_vacina)
            if vacina:
                return vacina
            print("❌ Vacina não encontrada.")
        
        else:
            print("❌ Opção inválida.")


def confirmar_aplicacao_vacina(vacina: Dict[str, Any], pessoa: Dict[str, Any]) -> bool:
    """Confirma aplicação da vacina"""
    
    print(f"\n💉 Vacina selecionada:")
    print(f"ID: {vacina['id']}")
    print(f"Nome: {vacina['nome']}")
    print(f"Fabricante: {vacina['fabricante']}")
    print(f"Lote: {vacina['lote']}")
    print(f"Validade: {vacina['validade']}")
    print(f"Vacinador: {vacina['vacinador']}")
    print(f"Doses necessárias: {vacina['doses_necessarias']}")
    print(f"Para: {pessoa['nome']}")
    
    while True:
        resposta = input("\nAplicar esta vacina? (s/n/0 para sair): ").strip().lower()
        if resposta in ['s', 'sim']:
            return True
        elif resposta in ['n', 'não', 'nao']:
            print("Busque outra vacina.")
            return False
        elif resposta == '0':
            return False
        else:
            print("Resposta inválida. Digite 's', 'n' ou '0'.")

def aplicar_vacina(vacina: Dict[str, Any], pessoa: Dict[str, Any]):
    """Registra a aplicação da vacina no banco"""
    
    vacinador = input("Nome do vacinador que está aplicando: ").strip()
    if not vacinador:
        print("❌ Nome do vacinador é obrigatório.")
        return
    
    # Usa sua função registrar_dose
    sucesso = registrar_dose(pessoa['id'], vacina['id'], vacinador)
    
    if sucesso:
        print(f"✅ Dose aplicada com sucesso!")
        print(f"📋 Registrado por: {vacinador}")
        print(f"💉 Vacina: {vacina['nome']}")
        print(f"👤 Paciente: {pessoa['nome']}")
    else:
        print("❌ Erro ao registrar dose no banco.")

def perguntar_aplicar_mais() -> bool:
    """Pergunta se quer aplicar mais vacinas"""
    while True:
        resposta = input("\nAplicar outra vacina para este usuário? (s/n): ").strip().lower()
        if resposta in ['s', 'sim']:
            return True
        elif resposta in ['n', 'não', 'nao']:
            print("Retornando ao menu principal...")
            return False
        else:
            print("Resposta inválida. Digite 's' ou 'n'.")