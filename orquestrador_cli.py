import os
from gerenciador_formulario import cadastrar_pessoa
from gerenciador_db import get_pessoa_por_qr_camera, get_pessoa_por_cpf
from scanners.qr_scanner import ler_qr_imagem
from utils.logger import log_event

def menu():
    print("\n=== Scarvir Orquestrador ===")
    print("1) Cadastrar pessoa")
    print("2) Ler QR (imagem)")
    print("3) Ler QR (câmera)")
    print("4) Buscar por CPF (fallback)")
    print("0) Sair")
    return input("Escolha: ").strip()

def mostrar_pessoa(p):
    if not p:
        print("❌ Usuário não encontrado.")
        return
    pid, nome, dob, cpf, criado, id_curto = p
    print("\n👤 Usuário:")
    print(f"  ID banco: {pid}")
    print(f"  Nome: {nome}")
    print(f"  DOB: {dob}")
    print(f"  CPF: {cpf}")
    print(f"  ID curto: {id_curto}")
    print(f"  Criado em: {criado}")

def main():
    while True:
        op = menu()
        if op == "1":
            usuario, qr_path = cadastrar_pessoa()
            if usuario:
                log_event("cadastro_usuario", id_curto=usuario["id_curto"], origem="cli", success=True)
            else:
                log_event("cadastro_usuario", id_curto=None, origem="cli", success=False, err="falha_cadastro")
        elif op == "2":
            path = input("Caminho da imagem: ").strip()
            res = ler_qr_imagem(path)
            if res:
                mostrar_pessoa(res)
                log_event("leitura_qr_imagem", id_curto=res[-1], origem="cli", success=True)
            else:
                print("❌ Falha na leitura do QR.")
                log_event("leitura_qr_imagem", success=False, err="qr_invalido", origem="cli")
        elif op == "3":
            res = get_pessoa_por_qr_camera()
            if res:
                mostrar_pessoa(res)
                log_event("leitura_qr_camera", id_curto=res[-1], origem="cli", success=True)
            else:
                print("❌ Falha na leitura do QR.")
                log_event("leitura_qr_camera", success=False, err="qr_invalido", origem="cli")
        elif op == "4":
            cpf = input("CPF: ").strip()
            res = get_pessoa_por_cpf(cpf)
            if res:
                mostrar_pessoa(res)
                log_event("busca_cpf", id_curto=res[-1], origem="cli", success=True)
            else:
                print("❌ Usuário não encontrado via CPF.")
                log_event("busca_cpf", success=False, err="cpf_nao_encontrado", origem="cli")
        elif op == "0":
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    main()
