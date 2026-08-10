r"""
Extrai os dados do painel "4 Pilares" a partir de SOMA NAO SALVA ENCIMA.xlsx
(aba "SOMAR 4 PILARES") e salva um dados.json pronto pro gerador de HTML
consumir.

Layout da aba (colunas, confirmado em 08/08): blocos por supervisor (linha
com nome do supervisor na col D + cabeçalho "POSITIVAÇÃO" na col E),
seguidos de 1 linha por RCA até a próxima linha de subtotal.

Por RCA:
- C=código, D=nome
- E/F/G/H = positivação meta/real/falta/%
- J/K/L   = margem meta/real/%
- N/O/P   = mix meta/real/%
- R/S/T   = financeiro meta/real/falta R$; V = financeiro % (real/meta)
- W       = tendência % de fechamento
- Y/Z/AA  = industrializado meta/realizado/margem % (pode ser negativa)
- AC/AD/AE= thermoprocessado meta/realizado/margem % (pode ser negativa)
- AG      = nº de pilares atingidos (0-4)

Tendência "projetado R$" = REAL(S) / TRABALHADOS * DIAS_UTEIS (globais no
topo da planilha, linhas 4-5).
"""

import json
import os

import openpyxl

CAMINHO_SOMA = r"C:\Users\edmar\Desktop\CONTAR 4 PILARES\SOMA NAO SALVA ENCIMA.xlsx"

PASTA_BASE = os.path.dirname(os.path.abspath(__file__))
CAMINHO_SAIDA = os.path.join(PASTA_BASE, "dados.json")


def extrair():
    wb = openpyxl.load_workbook(CAMINHO_SOMA, data_only=True)
    ws = wb["SOMAR 4 PILARES"]

    dias_uteis = ws.cell(row=4, column=6).value
    trabalhados = ws.cell(row=5, column=6).value

    rcas = []
    supervisor_atual = None
    for r in range(1, ws.max_row + 1):
        col_d = ws.cell(row=r, column=4).value
        col_e = ws.cell(row=r, column=5).value

        # Linha de cabeçalho de um novo bloco de supervisor.
        if col_d and col_e == "POSITIVAÇÃO":
            supervisor_atual = str(col_d).strip()
            continue

        codigo = ws.cell(row=r, column=3).value
        nome_bruto = col_d
        if supervisor_atual is None or codigo is None or nome_bruto is None:
            continue
        # Linha de subtotal do bloco (código vazio, mas nome preenchido) — pula.
        if str(codigo).strip() == "":
            continue

        codigo_str = str(int(float(str(codigo).strip())))
        # Nome vem como "23 - FABIO L. - GYN" — tira o prefixo de código
        # repetido; o que sobra depois do último " - " vira a "rota/praça"
        # exibida no card (ex: "GYN", "GYN RT 96 - HIDROLANDIA").
        nome_sem_codigo = str(nome_bruto).strip()
        prefixo = f"{codigo_str} - "
        if nome_sem_codigo.startswith(prefixo):
            nome_sem_codigo = nome_sem_codigo[len(prefixo):]
        if " - " in nome_sem_codigo:
            nome_rca, rota = nome_sem_codigo.rsplit(" - ", 1)
        else:
            nome_rca, rota = nome_sem_codigo, ""

        def val(col):
            v = ws.cell(row=r, column=col).value
            return v if isinstance(v, (int, float)) else 0

        real_financeiro = val(19)  # S
        meta_financeiro = val(18)  # R
        projetado = (real_financeiro / trabalhados * dias_uteis) if trabalhados else 0
        tendencia_pct = val(24)  # X = "TENTÊNCIA" (%) — bate com projetado/meta
        # U = "META DIA": quanto falta vender por dia útil restante pra bater a
        # meta do mês (vem negativo na planilha — é falta, não excedente).
        meta_dia = abs(val(21))

        # Layout confirmado em 09/08: colunas "PARTICIPAÇÃO" novas empurraram
        # margem/pilar/média/recompra pra direita — Z/AA/AB/AC = meta/real/
        # participação/margem (industrializado); AE/AF/AG/AH = idem (thermo).
        industrializado_real = val(27)
        thermo_real = val(32)

        rcas.append({
            "codigo": codigo_str,
            "nome": nome_rca,
            "rota": rota,
            "supervisor": supervisor_atual,
            "pilares": {
                "positivacao": {"meta": val(5), "real": val(6), "pct": val(8)},
                "margem": {"meta": val(10), "real": val(11), "pct": val(12)},
                "mix": {"meta": val(14), "real": val(15), "pct": val(16)},
                "financeiro": {"meta": meta_financeiro, "real": real_financeiro, "pct": val(22)},
            },
            "pilares_atingidos": int(val(36)),
            "tendencia": {"pct": tendencia_pct, "projetado": projetado, "meta": meta_financeiro, "meta_dia": meta_dia},
            "industrializado": {"meta": val(26), "real": industrializado_real, "participacao_pct": val(28), "margem_pct": val(29)},
            # margem % vem -1 (placeholder de erro) quando não teve venda ainda — trata como 0.
            "thermo": {"meta": val(31), "real": thermo_real, "participacao_pct": val(33), "margem_pct": val(34) if thermo_real else 0},
            "recompra_pct": val(40),  # AN = "RECOMPRA"
        })

    return rcas


def main():
    rcas = extrair()
    with open(CAMINHO_SAIDA, "w", encoding="utf-8") as f:
        json.dump(rcas, f, ensure_ascii=False, indent=2)
    print(f"{len(rcas)} RCAs extraídos. Salvo em: {CAMINHO_SAIDA}")


if __name__ == "__main__":
    main()
