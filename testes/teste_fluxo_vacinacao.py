import os
from datetime import datetime
from scanners.qr_scanner import ler_qr_imagem 
from scanners.qr_cam_scanner import ler_qr_camera
from gerenciador_db import get_pessoa_por_id_curto, get_pessoa_por_cpf
from vacinas.gerenciador_vacinas import (
    get_vacina_por_id,
    get_vacina_por_nome,
    get_vacina_por_qr,
    registrar_dose
)

# -----------------------------
# Encontrar pessoa
# -----------------------------

def encontrar_pessoa():
    while True:
        metodo = input("Buscar pessoa por (1) Short ID, (2) CPF, (3) QR Code: ").strip()
        if metodo not in ("1", "2", "3"):
            print("Opção inválida.")
            continue

        pessoa = None
        if metodo == "1":
            valor = input("Digite o short ID da pessoa: ").strip()
            pessoa = get_pessoa_por_id_curto(valor)
        elif metodo == "2":
            valor = input("Digite o CPF da pessoa: ").strip()
            pessoa = get_pessoa_por_cpf(valor)
        elif metodo == "3":
            caminho = input("Digite o caminho do QR Code da pessoa ou 'c' para usar câmera: ").strip()
            conteudo_qr = ler_qr_imagem(caminho) if caminho.lower() != 'c' else ler_qr_camera()
            
            if not conteudo_qr:
                print("Nenhum QR Code detectado, tente novamente.")
                continue

            if conteudo_qr.get("kind") != "user":
                print(f"QR Code detectado não é de usuário, é: {conteudo_qr.get('kind')}")
                continue

            payload = conteudo_qr.get("payload", {})
            id_curto = payload.get("id_curto")
            if not id_curto:
                print("ID curto não encontrado no QR Code")
                continue

            pessoa = get_pessoa_por_id_curto(id_curto)

        if not pessoa:
            print("Pessoa não encontrada, tente novamente.")
            continue

        # Confirmação
        print(f"Encontrado: {pessoa['nome']} | DOB: {pessoa.get('dob')} | CPF: {pessoa.get('id_documento')}")
        confirmar = input("É essa pessoa? (s/n): ").strip().lower()
        if confirmar == "s":
            return pessoa

# -----------------------------
# Escolher vacina
# -----------------------------
def escolher_vacina():
    while True:
        metodo = input("Buscar vacina por (1) Nome, (2) ID, (3) QR Code): ").strip()
        if metodo not in ("1", "2", "3"):
            print("Opção inválida.")
            continue

        if metodo == "1":
            valor = input("Digite o nome da vacina: ").strip()
            vacina = get_vacina_por_nome(valor)
        elif metodo == "2":
            valor = input("Digite o ID da vacina: ").strip()
            vacina = get_vacina_por_id(valor)
        elif metodo == "3":
            caminho = input("Digite o caminho do QR Code da vacina ou 'c' para usar câmera: ").strip()
            conteudo_qr = ler_qr_imagem(caminho) if caminho.lower() != 'c' else ler_qr_camera()
            vacina = get_vacina_por_qr(conteudo_qr)
        if not vacina:
            print("Vacina não encontrada, tente novamente.")
            continue

        # Confirmação
        print(f"\nVacina: {vacina['nome']} | Fabricante: {vacina['fabricante']} | Validade: {vacina['validade']} | Lote: {vacina['lote']}")
        confirmar = input("É esta vacina? (s/n): ").strip().lower()
        if confirmar == "s":
            return vacina

# -----------------------------
# Fluxo principal
# -----------------------------
def orquestrador_vacinacao():
    print("=== Início do fluxo de vacinação ===\n")
    pessoa = encontrar_pessoa()
    
    while True:
        vacina = escolher_vacina()
        vacinador = input("Digite o nome do vacinador responsável: ").strip()
        data_aplicacao = datetime.now()

        # Registrar no banco
        sucesso = registrar_dose(
            pessoa_id=pessoa["id"],
            vacina_id=vacina["id"],
            nome_vacinador=vacinador,
            data_aplicacao=data_aplicacao
        )

        if sucesso:
            print(f"\n✅ Dose registrada: {vacina['nome']} aplicada em {pessoa['nome']} por {vacinador} em {data_aplicacao}\n")
        else:
            print("❌ Erro ao registrar a dose!\n")

        outra = input("Deseja aplicar outra vacina nesta pessoa? (s/n): ").strip().lower()
        if outra != "s":
            print("\n✅ Fluxo de vacinação concluído. Obrigado!")
            break

# -----------------------------
# Execução
# -----------------------------
if __name__ == "__main__":
    orquestrador_vacinacao()
