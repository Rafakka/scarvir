import os
from typing import Optional, Dict, Any
from datetime import datetime
from vacinas.qr_vacinas import gerar_qr_vacina
from vacinas.gerenciador_vacinas import aplicar_vacina, confirmar_aplicacao_vacina, encontrar_vacina, get_vacina_por_qr, get_vacina_por_id, get_vacina_por_nome, perguntar_aplicar_mais, registrar_dose
from gerenciador_db import get_pessoa_por_qr_camera, get_pessoa_por_qr_imagem, get_pessoa_por_id_curto, get_pessoa_por_cpf

def fluxo_vacinacao():
    """Fluxo principal de aplicação de vacinas"""
    
    print("💉 SISTEMA DE APLICAÇÃO DE VACINAS")
    print("=" * 40)
    
    while True:
        # 1. Pergunta se quer vacinar
        if not perguntar_se_quer_vacinar():
            print("👋 Encerrando sistema...")
            break
        
        # 2. Encontra o usuário
        pessoa = encontrar_usuario()
        if not pessoa:
            continue
        
        # 3. Confirma os dados do usuário
        if not confirmar_usuario(pessoa):
            continue
        
        # 4. Fluxo de aplicação de vacinas
        aplicar_vacinas_usuario(pessoa)

def perguntar_se_quer_vacinar() -> bool:
    """Pergunta se o usuário quer iniciar vacinação"""
    while True:
        resposta = input("\nDeseja aplicar uma vacina? (s/n/0 para sair): ").strip().lower()
        if resposta in ['s', 'sim']:
            return True
        elif resposta in ['n', 'não', 'nao']:
            print("Operação cancelada.")
            return False
        elif resposta == '0':
            return False
        else:
            print("Resposta inválida. Digite 's', 'n' ou '0'.")

def encontrar_usuario() -> Optional[Dict[str, Any]]:
    """Encontra usuário por QR, ID curto ou CPF"""
    
    while True:
        print("\n🔍 Como deseja buscar o usuário?")
        print("1 - QR Code (câmera)")
        print("2 - QR Code (imagem)")
        print("3 - ID Curto")
        print("4 - CPF")
        print("0 - Cancelar")
        
        opcao = input("Opção: ").strip()
        
        if opcao == '0':
            return None
        
        elif opcao == '1':
            pessoa = get_pessoa_por_qr_camera()
            if pessoa:
                return pessoa
            print("❌ Não encontrado via câmera. Tente outro método.")
        
        elif opcao == '2':
            caminho = input("Caminho da imagem: ").strip()
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

def confirmar_usuario(pessoa: Dict[str, Any]) -> bool:
    """Confirma se é o usuário correto"""
    
    print(f"\n📋 Dados encontrados:")
    print(f"Nome: {pessoa['nome']}")
    print(f"Data Nascimento: {pessoa['dob']}")
    print(f"CPF: {pessoa['id_documento']}")
    print(f"ID Curto: {pessoa['id_curto']}")
    
    while True:
        resposta = input("\nÉ este usuário? (s/n/0 para sair): ").strip().lower()
        if resposta in ['s', 'sim']:
            return True
        elif resposta in ['n', 'não', 'nao']:
            print("Busque o usuário novamente.")
            return False
        elif resposta == '0':
            return False
        else:
            print("Resposta inválida. Digite 's', 'n' ou '0'.")

def aplicar_vacinas_usuario(pessoa: Dict[str, Any]):
    """Aplica vacinas para um usuário específico"""
    
    print(f"\n💉 APLICAÇÃO DE VACINAS PARA {pessoa['nome']}")
    
    while True:
        # Busca a vacina
        vacina = encontrar_vacina()
        if not vacina:
            break
        
        # Confirma aplicação
        if not confirmar_aplicacao_vacina(vacina, pessoa):
            continue
        
        # Aplica a vacina
        aplicar_vacina(vacina, pessoa)
        
        # Pergunta se quer aplicar mais
        if not perguntar_aplicar_mais():
            break



# Menu principal para escolher entre cadastrar vacina ou aplicar
def menu_principal():
    """Menu principal do sistema de vacinação"""
    
    while True:
        print("\n" + "=" * 50)
        print("🏥 SISTEMA DE VACINAÇÃO")
        print("=" * 50)
        print("1 - Aplicar vacinas")
        print("2 - Cadastrar nova vacina")
        print("3 - Gerar QR code para vacina existente")
        print("0 - Sair")
        
        opcao = input("Opção: ").strip()
        
        if opcao == '0':
            print("👋 Saindo...")
            break
        
        elif opcao == '1':
            fluxo_vacinacao()
        
        elif opcao == '2':
            from vacinas.cadastro_vacinas import cadastrar_vacina
            vacina_id = cadastrar_vacina()
            if vacina_id:
                print(f"✅ Vacina cadastrada com ID: {vacina_id}")
        
        elif opcao == '3':
            vacina_id = input("ID da vacina para gerar QR: ").strip()
            vacina_dict, qr_path = gerar_qr_vacina(vacina_id)
            if vacina_dict:
                print(f"✅ QR code gerado: {qr_path}")
            else:
                print("❌ Erro ao gerar QR code")
        
        else:
            print("❌ Opção inválida")
