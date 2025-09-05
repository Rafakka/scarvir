
from fluxo_vacinacao import menu_principal
from gerenciador_formulario import cadastrar_pessoa
from gerenciador_vacinas import aplicar_vacina
from sistema_consultas import consulta_pessoas
from utils.conector_bd import conectar_bd
from cadastro_vacinas import cadastrar_vacina


def main():
    conn = conectar_bd()
    if not conn:
        print("❌ Não foi possível conectar ao banco.")
        return

    print("\n--- MENU ---")
    print("1. Cadastrar pessoa")
    print("2. Cadastrar vacina")
    print("3. Aplicar vacina")
    print("4. Alterar registro")
    print("5. Consultas")
    escolha = input("Escolha: ").strip()

    if escolha == "1":
        cadastrar_pessoa(conn)
    elif escolha == "2":
        cadastrar_vacina(conn)
    elif escolha == "3":
        aplicar_vacina(conn)
    elif escolha == "4":
        menu_principal()
    elif escolha == "5":
        consulta_pessoas()

    conn.close()

if __name__ == "__main__":
    main()
