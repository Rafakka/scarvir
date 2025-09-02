from gerenciador_db import get_pessoa_por_qr


def testar_formato_qr():
    """Testa se o formato do QR está correto"""
    
    # Simula a leitura de um QR code
    conteudo_simulado = {
        "kind": "user",
        "payload": {
            "id_curto": "abc123",
            "nome": "João Silva",
            "cpf": "12345678909"
        }
    }
    
    print("Conteúdo do QR:", conteudo_simulado)
    
    # Testa a função ajustada
    pessoa = get_pessoa_por_qr(conteudo_simulado)
    
    if pessoa:
        print("✅ Formato correto - Pessoa encontrada:", pessoa["nome"])
    else:
        print("❌ Formato incorreto - Pessoa não encontrada")

# Execute para testar
testar_formato_qr()