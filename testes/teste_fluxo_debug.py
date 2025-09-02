from gerenciador_db import get_pessoa_por_id_curto, get_pessoa_por_qr
from gerenciador_formulario import cadastrar_pessoa


def testar_fluxo_real():
    """Testa o fluxo completo com dados reais"""
    
    print("🎯 TESTE DO FLUXO REAL")
    print("=" * 50)
    
    # 1. Cadastra uma pessoa REAL
    print("1. 📝 Cadastrando pessoa...")
    usuario, qr_path = cadastrar_pessoa()
    
    if not usuario or not qr_path:
        print("❌ Falha no cadastro")
        return
    
    id_curto_cadastro = usuario['id_curto']
    print(f"✅ Cadastrado: {usuario['nome']} - ID: {id_curto_cadastro}")
    print(f"📷 QR gerado: {qr_path}")
    
    # 2. Verifica se realmente está no banco
    print("\n2. 🔍 Verificando banco...")
    pessoa_direta = get_pessoa_por_id_curto(id_curto_cadastro)
    
    if pessoa_direta:
        print(f"✅ Encontrado no banco: {pessoa_direta['nome']}")
    else:
        print("❌ NÃO encontrado no banco!")
        print("   Isso indica problema na inserção no banco")
        return
    
    # 3. Lê o QR code gerado
    print("\n3. 📖 Lendo QR code...")
    from scanners.qr_scanner import ler_qr_imagem
    conteudo_qr = ler_qr_imagem(qr_path)
    
    if not conteudo_qr:
        print("❌ Falha na leitura do QR")
        return
    
    print(f"📋 Conteúdo do QR: {conteudo_qr}")
    
    # 4. Busca usando o QR
    print("\n4. 🔎 Buscando via QR...")
    pessoa_via_qr = get_pessoa_por_qr(conteudo_qr)
    
    if pessoa_via_qr:
        print(f"✅ Sucesso! Encontrado via QR: {pessoa_via_qr['nome']}")
        
        # 5. Verifica consistência
        if (pessoa_via_qr['id_curto'] == id_curto_cadastro and 
            pessoa_via_qr['nome'] == usuario['nome']):
            print("🎉 FLUXO COMPLETO FUNCIONANDO!")
        else:
            print("⚠️  Dados inconsistentes!")
    else:
        print("❌ Falha na busca via QR")
        print("   Problema pode ser:")
        print("   - Formato do conteúdo do QR")
        print("   - Função get_pessoa_por_qr")
        print("   - ID curto diferente no QR vs Banco")

# Execute o teste real
testar_fluxo_real()