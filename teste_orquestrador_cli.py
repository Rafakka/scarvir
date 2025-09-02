import os
from gerenciador_formulario import cadastrar_pessoa
from gerenciador_db import (
    get_pessoa_por_id_curto,
    get_pessoa_por_cpf
)
from scanners.qr_scanner import ler_qr_imagem
from scanners.qr_cam_scanner import ler_qr_camera
from utils.logger import log_event

def mostrar_pessoa_db(p):
    """p é a tupla retornada pelo DB: (id, nome, dob, id_documento, data_de_criacao, id_curto)"""
    if not p:
        print("❌ Usuário não encontrado no DB.")
        return
    pid, nome, dob, id_documento, data_de_criacao, id_curto = p
    print("\n👤 Usuário (do banco):")
    print(f"  ID banco: {pid}")
    print(f"  Nome: {nome}")
    print(f"  DOB: {dob}")
    print(f"  CPF: {id_documento}")
    print(f"  ID curto: {id_curto}")
    print(f"  Criado em: {data_de_criacao}")

def mostrar_payload_user(payload):
    """payload vindo do QR (dict). Pode conter id_curto, nome, cpf, etc."""
    if not payload:
        print("❌ Payload vazio.")
        return
    print("\n👤 Usuario (payload do QR):")
    for k, v in payload.items():
        print(f"  {k}: {v}")

def processar_qr_result(qr_result):
    """
    Recebe o retorno de ler_qr_imagem / ler_qr_camera:
    {'kind': <'user'|'vaccine'|...>, 'payload': {...}} ou None
    Retorna tuple (registro DB) ou dict (payload) ou None.
    """
    if not qr_result:
        return None

    kind = qr_result.get("kind")
    payload = qr_result.get("payload") or {}

    # Se for usuário, tente encontrar no DB por id_curto → cpf (fallback)
    if kind == "user":
        id_curto = payload.get("id_curto") or payload.get("idcurto")
        cpf = payload.get("cpf") or payload.get("id_documento")
        if id_curto:
            pessoa = get_pessoa_por_id_curto(id_curto)
            if pessoa:
                return pessoa
        if cpf:
            pessoa = get_pessoa_por_cpf(cpf)
            if pessoa:
                return pessoa
        # não encontrou no DB, retorna payload para exibição
        return payload

    # Se for vaccine, só retorna payload (ou você pode implementar busca por id_vacina)
    if kind == "vaccine":
        return {"vaccine_payload": payload}

    # Caso desconhecido, retorna raw payload
    return payload

def menu():
    print("\n=== Scarvir Orquestrador ===")
    print("1) Cadastrar pessoa")
    print("2) Ler QR (imagem)")
    print("3) Ler QR (câmera)")
    print("4) Buscar por CPF (fallback)")
    print("0) Sair")
    return input("Escolha: ").strip()

def main():
    while True:
        op = menu()
        if op == "1":
            usuario, qr_path = cadastrar_pessoa()  # cadastrar_pessoa já faz consentimento
            if usuario:
                print("\n✅ Cadastro OK.")
                print(f"QR salvo em: {qr_path}")
                log_event("cadastro_usuario", id_curto=usuario.get("id_curto"), origem="cli", success=True)
            else:
                print("❌ Cadastro não realizado (cancelado ou erro).")
                log_event("cadastro_usuario", origem="cli", success=False, err="canceled_or_error")
        elif op == "2":
            caminho = input("Caminho da imagem do QR: ").strip()
            if not os.path.exists(caminho):
                print("❌ Arquivo não encontrado:", caminho)
                log_event("ler_qr_imagem", origem="cli", success=False, err="file_not_found")
                continue
            qr_result = ler_qr_imagem(caminho)
            processed = processar_qr_result(qr_result)
            if processed is None:
                print("❌ Nenhum QR válido lido / usuário não encontrado.")
                log_event("ler_qr_imagem", origem="cli", success=False, err="qr_invalid_or_not_found")
            else:
                # Se retornou tupla DB → mostrar como pessoa do DB
                if isinstance(processed, tuple):
                    mostrar_pessoa_db(processed)
                    log_event("ler_qr_imagem", id_curto=processed[-1], origem="cli", success=True)
                else:
                    # dict payload (user info or vaccine info)
                    if isinstance(processed, dict) and processed.get("vaccine_payload"):
                        print("\n✅ QR de vacina lido:")
                        print(processed["vaccine_payload"])
                        log_event("ler_qr_imagem", origem="cli", success=True, extra={"vaccine": True})
                    else:
                        print("\n✅ Payload lido do QR (sem match DB):")
                        mostrar_payload_user(processed)
                        # tenta extrair id_curto para log
                        idc = processed.get("id_curto") if isinstance(processed, dict) else None
                        log_event("ler_qr_imagem", id_curto=idc, origem="cli", success=True)
        elif op == "3":
            print("Abrindo câmera para ler QR (pressione 'q' para cancelar)...")
            qr_result = ler_qr_camera()
            processed = processar_qr_result(qr_result)
            if processed is None:
                print("❌ Nenhum QR válido lido / usuário não encontrado.")
                log_event("ler_qr_camera", origem="cli", success=False, err="qr_invalid_or_not_found")
            else:
                if isinstance(processed, tuple):
                    mostrar_pessoa_db(processed)
                    log_event("ler_qr_camera", id_curto=processed[-1], origem="cli", success=True)
                else:
                    print("\n✅ Payload lido do QR (câmera):")
                    mostrar_payload_user(processed)
                    idc = processed.get("id_curto") if isinstance(processed, dict) else None
                    log_event("ler_qr_camera", id_curto=idc, origem="cli", success=True)
        elif op == "4":
            cpf = input("CPF para busca: ").strip()
            pessoa = get_pessoa_por_cpf(cpf)
            if pessoa:
                mostrar_pessoa_db(pessoa)
                log_event("busca_cpf", id_curto=pessoa[-1], origem="cli", success=True)
            else:
                print("❌ Usuário não encontrado via CPF.")
                log_event("busca_cpf", origem="cli", success=False, err="not_found")
        elif op == "0":
            print("Bye.")
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    main()
