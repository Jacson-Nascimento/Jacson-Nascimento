"""Cálculos agregados do processo seletivo IFMG 2027.

A base nominal não é armazenada neste repositório público. Os quantitativos
abaixo correspondem à apuração validada da lista oficial de inscrições efetivas.
"""

TOTAL_TECNOLOGIA_INOVACAO = 994
AMPLA_CONCORRENCIA = 868
VAGAS_TOTAIS = 20
VAGAS_AMPLA_CONCORRENCIA = 10
POSICAO_ALFABETICA_JACSON_AC = 377


def pct(numerador: int, denominador: int) -> float:
    return 100 * numerador / denominador


def main() -> None:
    demais_modalidades = TOTAL_TECNOLOGIA_INOVACAO - AMPLA_CONCORRENCIA

    resultados = {
        "inscritos_tecnologia_inovacao": TOTAL_TECNOLOGIA_INOVACAO,
        "ampla_concorrencia": AMPLA_CONCORRENCIA,
        "demais_modalidades": demais_modalidades,
        "participacao_ac_pct": pct(AMPLA_CONCORRENCIA, TOTAL_TECNOLOGIA_INOVACAO),
        "candidatos_por_vaga_ac": AMPLA_CONCORRENCIA / VAGAS_AMPLA_CONCORRENCIA,
        "probabilidade_simples_sorteio_ac_pct": pct(VAGAS_AMPLA_CONCORRENCIA, AMPLA_CONCORRENCIA),
        "probabilidade_simples_nao_selecao_ac_pct": 100 - pct(VAGAS_AMPLA_CONCORRENCIA, AMPLA_CONCORRENCIA),
        "candidatos_por_vaga_total": TOTAL_TECNOLOGIA_INOVACAO / VAGAS_TOTAIS,
        "relacao_vagas_inscritos_total_pct": pct(VAGAS_TOTAIS, TOTAL_TECNOLOGIA_INOVACAO),
        "posicao_alfabetica_jacson_na_ac": POSICAO_ALFABETICA_JACSON_AC,
    }

    for chave, valor in resultados.items():
        if isinstance(valor, float):
            print(f"{chave}: {valor:.4f}")
        else:
            print(f"{chave}: {valor}")


if __name__ == "__main__":
    main()
