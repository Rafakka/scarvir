import glob
import os
from gerenciador_db import conectar_bd, get_pessoa_por_qr
from gerenciador_formulario import cadastrar_pessoa
from testes.teste_id_banco import verificar_id_no_banco

def testar_apenas_leitura_qr():
    """Testa apenas a leitura de QR codes existentes"""
    
    print("📸 TESTE APENAS DE LEITURA DE QR")
    print("=" * 50)
    
    while True:
        print("\nOpções de teste:")
        print("1. Ler QR code de uma imagem")
        print("2. Ler QR code da câmera") 
        print("3. Voltar ao menu anterior")
        
        opcao = input("\nEscolha uma opção: ").strip()
        
        if opcao == "1":
            testar_leitura_imagem()
        
        elif opcao == "2":
            testar_leitura_camera()
        
        elif opcao == "3":
            break
        
        else:
            print("❌ Opção inválida")

def testar_leitura_imagem():
    """Testa leitura de QR code de arquivo de imagem"""
    
    caminho = input("Digite o caminho da imagem QR (ou Enter para usar o último gerado): ").strip()
    
    # Se não digitou caminho, tenta usar o último do fluxo real
    if not caminho and hasattr(testar_apenas_leitura_qr, 'ultimo_qr_path'):
        caminho = testar_apenas_leitura_qr.ultimo_qr_path
        print(f"Usando último QR gerado: {caminho}")
    
    if not caminho or not os.path.exists(caminho):
        print("❌ Arquivo não encontrado. Execute primeiro o fluxo real para gerar um QR.")
        return
    
    print(f"🔍 Lendo QR code: {caminho}")
    
    # Lê o QR code
    from scanners.qr_scanner import ler_qr_imagem
    conteudo_qr = ler_qr_imagem(caminho)
    
    if not conteudo_qr:
        print("❌ Não foi possível ler o QR code")
        return
    
    print(f"✅ QR lido com sucesso!")
    print(f"📋 Conteúdo: {conteudo_qr}")
    
    # Busca no banco
    print("\n🔎 Buscando no banco...")
    pessoa = get_pessoa_por_qr(conteudo_qr)
    
    if pessoa:
        print(f"🎉 Pessoa encontrada!")
        print(f"   Nome: {pessoa['nome']}")
        print(f"   ID curto: {pessoa['id_curto']}")
        print(f"   CPF: {pessoa['id_documento']}")
    else:
        print("❌ Pessoa não encontrada no banco")

def testar_leitura_camera():
    """Testa leitura de QR code pela câmera"""
    
    print("📷 Preparando câmera...")
    print("Aproxime o QR code da câmera")
    print("Pressione 'q' para cancelar")
    
    # Lê da câmera
    from scanners.qr_cam_scanner import ler_qr_camera
    conteudo_qr = ler_qr_camera()
    
    if not conteudo_qr:
        print("❌ Não foi possível ler o QR code da câmera")
        return
    
    print(f"✅ QR lido com sucesso!")
    print(f"📋 Conteúdo: {conteudo_qr}")
    
    # Busca no banco
    print("\n🔎 Buscando no banco...")
    pessoa = get_pessoa_por_qr(conteudo_qr)
    
    if pessoa:
        print(f"🎉 Pessoa encontrada!")
        print(f"   Nome: {pessoa['nome']}")
        print(f"   ID curto: {pessoa['id_curto']}")
        print(f"   CPF: {pessoa['id_documento']}")
    else:
        print("❌ Pessoa não encontrada no banco")

# Modifique o testar_fluxo_real para guardar o caminho do QR
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
    
    # Guarda o caminho para usar depois nos testes de leitura
    testar_apenas_leitura_qr.ultimo_qr_path = qr_path
    
    id_curto_cadastro = usuario['id_curto']
    print(f"✅ Cadastrado: {usuario['nome']} - ID: {id_curto_cadastro}")
    print(f"📷 QR gerado: {qr_path}")

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

def testar_multiplos_qrs():
    """Testa leitura de TODOS os QR codes da pasta 'qrcodes'"""
    
    pasta_qrcodes = "qrcodes"
    
    # Verifica se a pasta existe
    if not os.path.exists(pasta_qrcodes):
        print(f"❌ Pasta '{pasta_qrcodes}' não encontrada!")
        return
    
    # Busca todos os arquivos PNG na pasta
    qrs_para_testar = glob.glob(os.path.join(pasta_qrcodes, "*.png"))
    
    # Se não encontrar PNGs, tenta outros formatos comuns
    if not qrs_para_testar:
        qrs_para_testar = glob.glob(os.path.join(pasta_qrcodes, "*.jpg"))
        qrs_para_testar += glob.glob(os.path.join(pasta_qrcodes, "*.jpeg"))
        qrs_para_testar += glob.glob(os.path.join(pasta_qrcodes, "*.bmp"))
    
    if not qrs_para_testar:
        print(f"❌ Nenhum arquivo de imagem encontrado na pasta '{pasta_qrcodes}'")
        return
    
    print(f"🧪 TESTANDO {len(qrs_para_testar)} QR CODES ENCONTRADOS")
    print("=" * 50)
    
    resultados = {
        'sucesso': 0,
        'falha_leitura': 0,
        'nao_encontrado': 0,
        'erro': 0
    }
    
    for i, qr_path in enumerate(qrs_para_testar, 1):
        print(f"\n🔍 [{i}/{len(qrs_para_testar)}] Testando: {os.path.basename(qr_path)}")
        
        try:
            # Lê o QR
            from scanners.qr_scanner import ler_qr_imagem
            conteudo = ler_qr_imagem(qr_path)
            
            if not conteudo:
                print("   ❌ Falha na leitura do QR code")
                resultados['falha_leitura'] += 1
                continue
            
            # Busca no banco
            pessoa = get_pessoa_por_qr(conteudo)
            
            if pessoa:
                print(f"   ✅ Encontrado: {pessoa['nome']} - {pessoa['id_curto']}")
                resultados['sucesso'] += 1
            else:
                print("   ❌ Não encontrado no banco")
                resultados['nao_encontrado'] += 1
                
        except Exception as e:
            print(f"   💥 Erro inesperado: {e}")
            resultados['erro'] += 1
    
    # Relatório final
    print("\n" + "=" * 50)
    print("📊 RELATÓRIO FINAL")
    print("=" * 50)
    print(f"Total de QR codes testados: {len(qrs_para_testar)}")
    print(f"✅ Sucesso: {resultados['sucesso']}")
    print(f"❌ Falha na leitura: {resultados['falha_leitura']}")
    print(f"❌ Não encontrado no banco: {resultados['nao_encontrado']}")
    print(f"💥 Erros: {resultados['erro']}")
    
    return resultados

def testar_multiplos_qrs_avancado(filtrar_por_extensao=None, max_testes=None):
    """
    Testa leitura de TODOS os QR codes da pasta 'qrcodes' com opções avançadas
    
    Args:
        filtrar_por_extensao: Lista de extensões para filtrar ['.png', '.jpg', etc]
        max_testes: Número máximo de arquivos para testar (útil para muitas imagens)
    """
    
    pasta_qrcodes = "qrcodes"
    
    if not os.path.exists(pasta_qrcodes):
        print(f"❌ Pasta '{pasta_qrcodes}' não encontrada!")
        return
    
    # Define extensões para buscar
    extensoes = filtrar_por_extensao or ['.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.webp']
    
    qrs_para_testar = []
    for ext in extensoes:
        qrs_para_testar.extend(glob.glob(os.path.join(pasta_qrcodes, f"*{ext}")))
        qrs_para_testar.extend(glob.glob(os.path.join(pasta_qrcodes, f"*{ext.upper()}")))
    
    # Remove duplicatas (caso haja)
    qrs_para_testar = list(set(qrs_para_testar))
    
    # Ordena por nome do arquivo
    qrs_para_testar.sort()
    
    # Limita se necessário
    if max_testes and len(qrs_para_testar) > max_testes:
        qrs_para_testar = qrs_para_testar[:max_testes]
        print(f"⚠️  Limitando teste aos primeiros {max_testes} arquivos")
    
    if not qrs_para_testar:
        print(f"❌ Nenhum arquivo encontrado na pasta '{pasta_qrcodes}'")
        return
    
    print(f"🧪 TESTANDO {len(qrs_para_testar)} QR CODES ENCONTRADOS")
    print("=" * 60)
    
    resultados = {
        'sucesso': [],
        'falha_leitura': [],
        'nao_encontrado': [],
        'erro': []
    }
    
    for i, qr_path in enumerate(qrs_para_testar, 1):
        nome_arquivo = os.path.basename(qr_path)
        print(f"\n🔍 [{i}/{len(qrs_para_testar)}] {nome_arquivo}")
        
        try:
            # Lê o QR
            from scanners.qr_scanner import ler_qr_imagem
            conteudo = ler_qr_imagem(qr_path)
            
            if not conteudo:
                print("   ❌ Falha na leitura do QR code")
                resultados['falha_leitura'].append(nome_arquivo)
                continue
            
            # Busca no banco
            pessoa = get_pessoa_por_qr(conteudo)
            
            if pessoa:
                print(f"   ✅ {pessoa['nome']} - ID: {pessoa['id_curto']}")
                resultados['sucesso'].append({
                    'arquivo': nome_arquivo,
                    'nome': pessoa['nome'],
                    'id_curto': pessoa['id_curto']
                })
            else:
                print("   ❌ Não encontrado no banco")
                resultados['nao_encontrado'].append(nome_arquivo)
                
        except Exception as e:
            print(f"   💥 Erro: {e}")
            resultados['erro'].append((nome_arquivo, str(e)))
    
    # Relatório final detalhado
    print("\n" + "=" * 60)
    print("📊 RELATÓRIO DETALHADO")
    print("=" * 60)
    print(f"Total testado: {len(qrs_para_testar)}")
    print(f"✅ Sucesso: {len(resultados['sucesso'])}")
    print(f"❌ Falha na leitura: {len(resultados['falha_leitura'])}")
    print(f"❌ Não encontrado no banco: {len(resultados['nao_encontrado'])}")
    print(f"💥 Erros: {len(resultados['erro'])}")
    
    # Detalhes dos sucessos
    if resultados['sucesso']:
        print(f"\n🎯 Pessoas encontradas:")
        for success in resultados['sucesso']:
            print(f"   📁 {success['arquivo']} → 👤 {success['nome']} ({success['id_curto']})")
    
    # Detalhes das falhas de leitura
    if resultados['falha_leitura']:
        print(f"\n⚠️  Falhas na leitura ({len(resultados['falha_leitura'])}):")
        for arquivo in resultados['falha_leitura'][:5]:  # Mostra só os 5 primeiros
            print(f"   ❌ {arquivo}")
        if len(resultados['falha_leitura']) > 5:
            print(f"   ... e mais {len(resultados['falha_leitura']) - 5} arquivos")
    
    return resultados

def menu_completo():
    """Menu com todas as opções"""
    
    while True:
        print("\n" + "=" * 50)
        print("🎯 SISTEMA COMPLETO DE TESTE QR")
        print("=" * 50)
        print("1. Fluxo completo (cadastro + QR + busca)")
        print("2. Apenas testar leitura de QR (imagem)")
        print("3. Apenas testar leitura de QR (câmera)")
        print("4. Testar TODOS os QRs da pasta")
        print("5. Testar QRs com opções avançadas")
        print("6. Ver IDs no banco")
        print("7. Sair")
        
        opcao = input("\nEscolha uma opção: ").strip()
        
        if opcao == "1":
            testar_fluxo_real()
        
        elif opcao == "2":
            testar_leitura_imagem()
        
        elif opcao == "3":
            testar_leitura_camera()
        
        elif opcao == "4":
            testar_multiplos_qrs()
        
        elif opcao == "5":
            print("Opções avançadas:")
            print("a - Testar apenas PNGs (máx 20)")
            print("b - Testar todos os formatos")
            sub_opcao = input("Escolha: ").strip().lower()
            
            if sub_opcao == 'a':
                testar_multiplos_qrs_avancado(
                    filtrar_por_extensao=['.png'],
                    max_testes=20
                )
            else:
                testar_multiplos_qrs_avancado()
        
        elif opcao == "6":
            verificar_id_no_banco()
        
        elif opcao == "7":
            print("👋 Saindo...")
            break
        
        else:
            print("❌ Opção inválida")

# Execute o menu completo
menu_completo()