"""
RentSmart - Sistema de Orçamento de Locação da R.M Imóveis
Disciplina: Algorithmic Thinking & Introduction to Object-Oriented Programming

Calcula o aluguel mensal de casas, apartamentos e estúdios, aplica as regras
comerciais da imobiliária e gera um CSV com a projeção dos 12 primeiros meses.
"""

import csv
from abc import ABC, abstractmethod


def formatar_reais(valor):
    """Formata um número no padrão brasileiro: R$ 1.234,56"""
    sinal = "- " if valor < 0 else ""
    texto = f"{abs(valor):,.2f}"
    texto = texto.replace(",", "X").replace(".", ",").replace("X", ".")
    return f"{sinal}R$ {texto}"


# ---------------------------------------------------------------------------
# Imóveis
# ---------------------------------------------------------------------------

class Imovel(ABC):
    """Classe base: guarda o que todo imóvel tem e define o cálculo do aluguel."""

    tipo = "Imóvel"
    aluguel_base = 0.0

    def __init__(self):
        # Cada item é (descrição, valor). Serve para mostrar como o valor foi formado.
        self.itens = []

    @abstractmethod
    def adicionar_itens(self):
        """Cada tipo de imóvel adiciona os seus próprios adicionais."""

    def calcular_desconto(self, subtotal):
        """Por padrão não há desconto. Apartamento sobrescreve este método."""
        return 0.0

    def calcular_aluguel(self):
        """Monta o detalhamento e devolve o valor final do aluguel mensal."""
        self.itens = [(f"Aluguel-base ({self.tipo})", self.aluguel_base)]
        self.adicionar_itens()

        subtotal = sum(valor for _, valor in self.itens)
        desconto = self.calcular_desconto(subtotal)
        if desconto > 0:
            self.itens.append(("Desconto de 5% (sem crianças)", -desconto))

        return round(subtotal - desconto, 2)


class ImovelComQuartos(Imovel):
    """Casas e apartamentos: podem ter 1 ou 2 quartos e 1 vaga de garagem."""

    adicional_segundo_quarto = 0.0
    valor_garagem = 300.0

    def __init__(self, quartos, tem_garagem):
        super().__init__()
        self.quartos = quartos
        self.tem_garagem = tem_garagem

    def adicionar_itens(self):
        if self.quartos == 2:
            self.itens.append(("Adicional de 2 quartos", self.adicional_segundo_quarto))
        if self.tem_garagem:
            self.itens.append(("Vaga de garagem", self.valor_garagem))


class Apartamento(ImovelComQuartos):
    tipo = "Apartamento"
    aluguel_base = 700.0
    adicional_segundo_quarto = 200.0
    percentual_desconto = 0.05

    def __init__(self, quartos, tem_garagem, tem_criancas):
        super().__init__(quartos, tem_garagem)
        self.tem_criancas = tem_criancas

    def calcular_desconto(self, subtotal):
        # Regra: sem crianças, 5% de desconto depois dos adicionais.
        if not self.tem_criancas:
            return round(subtotal * self.percentual_desconto, 2)
        return 0.0


class Casa(ImovelComQuartos):
    tipo = "Casa"
    aluguel_base = 900.0
    adicional_segundo_quarto = 250.0


class Estudio(Imovel):
    tipo = "Estúdio"
    aluguel_base = 1200.0
    valor_pacote_vagas = 250.0   # pacote inicial com 2 vagas
    vagas_no_pacote = 2
    valor_vaga_extra = 60.0

    def __init__(self, vagas):
        super().__init__()
        self.vagas = vagas

    def adicionar_itens(self):
        if self.vagas > 0:
            self.itens.append((f"Pacote de estacionamento ({self.vagas_no_pacote} vagas)",
                               self.valor_pacote_vagas))
            extras = max(0, self.vagas - self.vagas_no_pacote)
            if extras > 0:
                self.itens.append((f"Vagas adicionais ({extras} x {formatar_reais(self.valor_vaga_extra)})",
                                   extras * self.valor_vaga_extra))


# ---------------------------------------------------------------------------
# Contrato e orçamento
# ---------------------------------------------------------------------------

class Contrato:
    """Taxa contratual de R$ 2.000,00, paga em 1 a 5 parcelas."""

    TAXA = 2000.0
    MAX_PARCELAS = 5

    def __init__(self, parcelas):
        if not 1 <= parcelas <= self.MAX_PARCELAS:
            raise ValueError("O contrato pode ser pago em 1 a 5 parcelas.")
        self.parcelas = parcelas

    def valor_parcela(self):
        return round(self.TAXA / self.parcelas, 2)

    def parcela_do_mes(self, mes):
        """Valor da taxa contratual cobrado em um mês (0 depois da última parcela).

        A última parcela acerta os centavos, para a soma dar exatamente R$ 2.000,00
        (ex.: 3x fica 666,67 + 666,67 + 666,66)."""
        if mes < self.parcelas:
            return self.valor_parcela()
        if mes == self.parcelas:
            return round(self.TAXA - self.valor_parcela() * (self.parcelas - 1), 2)
        return 0.0


class Orcamento:
    """Junta imóvel e contrato: mostra o resumo e gera a projeção de 12 meses."""

    MESES = 12

    def __init__(self, imovel, contrato):
        self.imovel = imovel
        self.contrato = contrato
        self.aluguel_mensal = imovel.calcular_aluguel()

    def gerar_projecao(self):
        linhas = []
        for mes in range(1, self.MESES + 1):
            parcela = self.contrato.parcela_do_mes(mes)
            linhas.append({
                "mes": mes,
                "aluguel": self.aluguel_mensal,
                "parcela_contrato": parcela,
                "total_mes": round(self.aluguel_mensal + parcela, 2),
            })
        return linhas

    def exibir_resumo(self):
        print("\n" + "=" * 52)
        print("           ORÇAMENTO DE LOCAÇÃO - R.M IMÓVEIS")
        print("=" * 52)
        print("ALUGUEL MENSAL")
        for descricao, valor in self.imovel.itens:
            print(f"  {descricao:<38}{formatar_reais(valor):>12}")
        print("-" * 52)
        print(f"  {'Aluguel mensal':<38}{formatar_reais(self.aluguel_mensal):>12}")

        print("\nTAXA CONTRATUAL (separada do aluguel)")
        print(f"  {'Valor total':<38}{formatar_reais(Contrato.TAXA):>12}")
        print(f"  {'Parcelamento':<38}{str(self.contrato.parcelas) + 'x de ' + formatar_reais(self.contrato.valor_parcela()):>12}")

        total_ano = sum(linha["total_mes"] for linha in self.gerar_projecao())
        print(f"\nTotal previsto nos 12 primeiros meses: {formatar_reais(total_ano)}")
        print("=" * 52)

    def exportar_csv(self, caminho="projecao_12_meses.csv"):
        with open(caminho, "w", newline="", encoding="utf-8-sig") as arquivo:
            escritor = csv.writer(arquivo, delimiter=";")
            escritor.writerow(["Mês", "Aluguel (R$)", "Parcela do contrato (R$)", "Total do mês (R$)"])
            for linha in self.gerar_projecao():
                escritor.writerow([
                    linha["mes"],
                    f"{linha['aluguel']:.2f}".replace(".", ","),
                    f"{linha['parcela_contrato']:.2f}".replace(".", ","),
                    f"{linha['total_mes']:.2f}".replace(".", ","),
                ])
        return caminho


# ---------------------------------------------------------------------------
# Entrada de dados (com validação)
# ---------------------------------------------------------------------------

def ler_opcao(pergunta, opcoes):
    """Repete a pergunta até o usuário digitar uma das opções válidas."""
    while True:
        resposta = input(pergunta).strip().upper()
        if resposta in opcoes:
            return resposta
        print(f"  Opção inválida. Digite uma destas: {', '.join(opcoes)}")


def ler_inteiro(pergunta, minimo, maximo):
    """Repete a pergunta até o usuário digitar um número inteiro dentro do intervalo."""
    while True:
        resposta = input(pergunta).strip()
        if resposta.isdigit() and minimo <= int(resposta) <= maximo:
            return int(resposta)
        print(f"  Digite um número inteiro de {minimo} a {maximo}.")


def ler_sim_nao(pergunta):
    return ler_opcao(pergunta + " (S/N): ", ["S", "N"]) == "S"


def criar_imovel():
    print("\nTipos de imóvel:")
    print("  1 - Apartamento (R$ 700,00)")
    print("  2 - Casa        (R$ 900,00)")
    print("  3 - Estúdio     (R$ 1.200,00)")
    tipo = ler_opcao("Escolha o tipo (1, 2 ou 3): ", ["1", "2", "3"])

    if tipo in ("1", "2"):
        quartos = ler_inteiro("Quantidade de quartos (1 ou 2): ", 1, 2)
        garagem = ler_sim_nao("Deseja vaga de garagem (+ R$ 300,00)?")
        if tipo == "1":
            criancas = ler_sim_nao("Possui crianças?")
            return Apartamento(quartos, garagem, criancas)
        return Casa(quartos, garagem)

    vagas = ler_inteiro("Quantas vagas de estacionamento? (0 = nenhuma, pacote de 2 vagas = R$ 250,00, "
                        "vaga extra = R$ 60,00): ", 0, 20)
    return Estudio(vagas)


def main():
    print("=" * 52)
    print("   RentSmart - Orçamento de Locação | R.M Imóveis")
    print("=" * 52)

    imovel = criar_imovel()
    parcelas = ler_inteiro("Em quantas parcelas pagar a taxa de contrato de R$ 2.000,00 (1 a 5)? ", 1, 5)

    orcamento = Orcamento(imovel, Contrato(parcelas))
    orcamento.exibir_resumo()

    arquivo = orcamento.exportar_csv()
    print(f"\nProjeção de 12 meses salva em: {arquivo}")


if __name__ == "__main__":
    main()
