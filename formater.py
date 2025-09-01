import tkinter as tk
from tkinter import ttk
import random
import re

# Função para gerar ID aleatório
def gerar_id():
    return str(random.randint(1000, 9999))

# Função para formatar CPF automaticamente
def formatar_cpf(event):
    texto = entry_cpf.get().replace(".", "").replace("-", "")
    if texto.isdigit():
        novo_texto = ""
        if len(texto) > 3:
            novo_texto += texto[:3] + "."
            if len(texto) > 6:
                novo_texto += texto[3:6] + "."
                if len(texto) > 9:
                    novo_texto += texto[6:9] + "-"
                    novo_texto += texto[9:11]
                else:
                    novo_texto += texto[6:]
            else:
                novo_texto += texto[3:]
        else:
            novo_texto = texto
        entry_cpf.delete(0, tk.END)
        entry_cpf.insert(0, novo_texto)

# Função para formatar data automaticamente (DD/MM/AAAA)
def formatar_data(event):
    texto = entry_data.get().replace("/", "")
    if texto.isdigit():
        novo_texto = ""
        if len(texto) > 2:
            novo_texto += texto[:2] + "/"
            if len(texto) > 4:
                novo_texto += texto[2:4] + "/"
                novo_texto += texto[4:8]
            else:
                novo_texto += texto[2:]
        else:
            novo_texto = texto
        entry_data.delete(0, tk.END)
        entry_data.insert(0, novo_texto)

# Função para salvar dados
def salvar():
    print("ID:", entry_id.get())
    print("Nome:", entry_nome.get())
    print("CPF:", entry_cpf.get())
    print("Data de Nascimento:", entry_data.get())

# Criar janela principal
root = tk.Tk()
root.title("Formulário Expandido")

# Campo ID
tk.Label(root, text="ID:").grid(row=0, column=0, padx=5, pady=5)
entry_id = tk.Entry(root)
entry_id.insert(0, gerar_id())  # gera ID ao abrir
entry_id.grid(row=0, column=1, padx=5, pady=5)

# Campo Nome
tk.Label(root, text="Nome:").grid(row=1, column=0, padx=5, pady=5)
entry_nome = tk.Entry(root)
entry_nome.grid(row=1, column=1, padx=5, pady=5)

# Campo CPF
tk.Label(root, text="CPF:").grid(row=2, column=0, padx=5, pady=5)
entry_cpf = tk.Entry(root)
entry_cpf.grid(row=2, column=1, padx=5, pady=5)
entry_cpf.bind("<KeyRelease>", formatar_cpf)

# Campo Data de Nascimento
tk.Label(root, text="Data de Nascimento:").grid(row=3, column=0, padx=5, pady=5)
entry_data = tk.Entry(root)
entry_data.grid(row=3, column=1, padx=5, pady=5)
entry_data.bind("<KeyRelease>", formatar_data)

# Botão Salvar
btn_salvar = tk.Button(root, text="Salvar", command=salvar)
btn_salvar.grid(row=4, column=0, columnspan=2, pady=10)

root.mainloop()
