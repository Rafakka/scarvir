import os
import json
from datetime import datetime
from security.fernet_key import get_cipher

# Importa suas funções existentes
from gerenciador_formulario import cadastrar_pessoa
from gerenciador_db import get_pessoa_por_cpf, get_pessoa_por_qr_imagem, get_pessoa_por_id_curto

def testar_fluxo_completo():
    """Fluxo completo: cadastro -> geração QR -> leitura QR -> busca no banco"""
    
    print("=" * 50)
    print("🚀 INICIANDO TESTE DO FLUXO COMPLETO")
    print("=" * 50)
    
    # 1. Cadastro da pessoa
    print("\n1. 📝 CADASTRANDO NOVA PESSOA")
    print("-" * 30)
    
    usuario, qr_path = cadastrar_pessoa()
    
    if not usuario or not qr_path:
        print("❌ Falha no cadastro. Abortando teste.")
        return False
    
    print(f"✅ Usuário cadastrado: {usuario['nome']}")
    print(f"📋 ID curto: {usuario['id_curto']}")
    print(f"📷 QR Code gerado: {qr_path}")
    
    # 2. Busca direta no banco (teste rápido)
    print("\n2. 🔍 TESTANDO BUSCA DIRETA NO BANCO")
    print("-" * 40)
    
    pessoa_direta = get_pessoa_por_id_curto(usuario['id_curto'])
    if pessoa_direta:
        print(f"✅ Busca direta funcionou: {pessoa_direta['nome']}")
    else:
        print("❌ Busca direta falhou")
        return False
    
    # 3. Leitura do QR code e busca
    print("\n3. 📸 LENDO QR CODE E BUSCANDO NO BANCO")
    print("-" * 45)
    
    pessoa_via_qr = get_pessoa_por_qr_imagem(qr_path)
    
    if pessoa_via_qr:
        print("✅ QR code lido e pessoa encontrada!")
        print(f"   Nome: {pessoa_via_qr['nome']}")
        print(f"   ID curto: {pessoa_via_qr['id_curto']}")
        print(f"   CPF: {pessoa_via_qr['id_documento']}")
        print(f"   Data nascimento: {pessoa_via_qr['dob']}")
    else:
        print("❌ Falha na leitura do QR ou busca no banco")
        return False
    
    # 4. Verificação dos dados
    print("\n4. ✅ VERIFICANDO INTEGRIDADE DOS DADOS")
    print("-" * 35)
    
    dados_consistentes = (
        usuario['id_curto'] == pessoa_via_qr['id_curto'] and
        usuario['nome'] == pessoa_via_qr['nome'] and
        usuario['id_documento'] == pessoa_via_qr['id_documento']
    )
    
    if dados_consistentes:
        print("✅ Todos os dados estão consistentes!")
        print("🎉 FLUXO COMPLETO TESTADO COM SUCESSO!")
        return True
    else:
        print("❌ Dados inconsistentes entre cadastro e busca")
        return False

def testar_multiplos_casos():
    """Testa vários cenários automaticamente"""
    
    testes = [
        {
            'nome': 'João Silva',
            'dob': '15/05/1990',
            'cpf': '12345678909'  # CPF válido
        },
        {
            'nome': 'Maria Santos', 
            'dob': '20/12/1985',
            'cpf': '98765432100'  # CPF válido
        }
    ]
    
    resultados = []
    
    for i, teste in enumerate(testes, 1):
        print(f"\n🧪 TESTE {i}: {teste['nome']}")
        print("-" * 30)
        
        # Simula entrada do usuário
        import builtins
        original_input = builtins.input
        
        def mock_input(prompt):
            if "Nome" in prompt:
                return teste['nome']
            elif "Data de nascimento" in prompt:
                return teste['dob']
            elif "ID do documento" in prompt:
                return teste['cpf']
            elif "consentimento" in prompt:
                return "s"
            return ""
        
        builtins.input = mock_input
        
        try:
            resultado = testar_fluxo_completo()
            resultados.append((teste['nome'], resultado))
        except Exception as e:
            print(f"❌ Erro durante o teste: {e}")
            resultados.append((teste['nome'], False))
        finally:
            builtins.input = original_input
    
    # Relatório final
    print("\n" + "=" * 50)
    print("📊 RELATÓRIO DE TESTES")
    print("=" * 50)
    
    for nome, sucesso in resultados:
        status = "✅ SUCESSO" if sucesso else "❌ FALHA"
        print(f"{nome}: {status}")

def menu_principal():
    """Menu interativo para testar o sistema"""
    
    while True:
        print("\n" + "=" * 50)
        print("🎯 MENU PRINCIPAL - SISTEMA DE CADASTRO")
        print("=" * 50)
        print("1. Testar fluxo completo (cadastro + QR + busca)")
        print("2. Testar múltiplos casos automaticamente")
        print("3. Buscar pessoa por ID curto")
        print("4. Buscar pessoa por CPF")
        print("5. Ler QR code da câmera")
        print("6. Ler QR code de imagem")
        print("7. Sair")
        
        opcao = input("\nEscolha uma opção: ").strip()
        
        if opcao == "1":
            testar_fluxo_completo()
        
        elif opcao == "2":
            testar_multiplos_casos()
        
        elif opcao == "3":
            id_curto = input("Digite o ID curto: ").strip()
            pessoa = get_pessoa_por_id_curto(id_curto)
            if pessoa:
                print(f"✅ Encontrado: {pessoa['nome']} - {pessoa['id_documento']}")
            else:
                print("❌ Pessoa não encontrada")
        
        elif opcao == "4":
            cpf = input("Digite o CPF: ").strip()
            pessoa = get_pessoa_por_cpf(cpf)
            if pessoa:
                print(f"✅ Encontrado: {pessoa['nome']} - {pessoa['id_curto']}")
            else:
                print("❌ Pessoa não encontrada")
        
        elif opcao == "5":
            from gerenciador_db import get_pessoa_por_qr_camera
            pessoa = get_pessoa_por_qr_camera()
            if pessoa:
                print(f"✅ Encontrado via câmera: {pessoa['nome']}")
            else:
                print("❌ Nenhuma pessoa encontrada")
        
        elif opcao == "6":
            caminho = input("Digite o caminho da imagem: ").strip()
            pessoa = get_pessoa_por_qr_imagem(caminho)
            if pessoa:
                print(f"✅ Encontrado via imagem: {pessoa['nome']}")
            else:
                print("❌ Nenhuma pessoa encontrada")
        
        elif opcao == "7":
            print("👋 Saindo...")
            break
        
        else:
            print("❌ Opção inválida")

# Execução principal
if __name__ == "__main__":
    # Teste rápido
    # testar_fluxo_completo()
    
    # Menu interativo
    menu_principal()