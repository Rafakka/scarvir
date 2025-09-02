# validators.py
from datetime import date, datetime

def limpar_cpf(cpf: str) -> str:
    return "".join(ch for ch in cpf if ch.isdigit())

def validar_cpf(cpf: str) -> bool:
    cpf = limpar_cpf(cpf)
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False

    def dv(cpf_parcial: str) -> int:
        tam = len(cpf_parcial) + 1
        soma = sum(int(d) * (tam - i) for i, d in enumerate(cpf_parcial))
        resto = soma % 11
        return 0 if resto < 2 else 11 - resto

    d1 = dv(cpf[:9])
    d2 = dv(cpf[:9] + str(d1))
    return cpf.endswith(f"{d1}{d2}")

def formatar_cpf(cpf: str) -> str:
    cpf = limpar_cpf(cpf)
    if len(cpf) != 11:
        return cpf
    return f"{cpf[0:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:11]}"

def validar_e_normalizar_dob(dob_str: str) -> str:
    # Entrada esperada: DD/MM/AAAA → saída: YYYY-MM-DD
    try:
        dt = datetime.strptime(dob_str.strip(), "%d/%m/%Y").date()
    except Exception:
        raise ValueError("Data inválida. Use o formato DD/MM/AAAA.")
    hoje = date.today()
    if dt > hoje:
        raise ValueError("Data de nascimento no futuro não é válida.")
    idade = hoje.year - dt.year - ((hoje.month, hoje.day) < (dt.month, dt.day))
    if idade < 0 or idade > 130:
        raise ValueError("Idade fora do intervalo plausível (0–130).")
    return dt.isoformat()  # YYYY-MM-DD
