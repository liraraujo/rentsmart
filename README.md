# RentSmart – Orçamento de Locação (R.M Imóveis)

Aplicação em Python que calcula o orçamento de locação de imóveis da R.M Imóveis, aplicando automaticamente as regras comerciais da imobiliária, e gera um arquivo CSV com a projeção dos 12 primeiros meses de contrato.

Projeto da disciplina **Algorithmic Thinking & Introduction to Object-Oriented Programming** – Bacharelado em Ciência da Computação, UniFECAF.
Autora: **Lira Cristina Rodrigues de Araújo**

## Regras implementadas

| Imóvel | Aluguel-base | Adicionais | Desconto |
| --- | --- | --- | --- |
| Apartamento | R$ 700,00 | 2 quartos: + R$ 200,00 · Garagem: + R$ 300,00 | 5% para quem não tem crianças, calculado depois dos adicionais |
| Casa | R$ 900,00 | 2 quartos: + R$ 250,00 · Garagem: + R$ 300,00 | — |
| Estúdio | R$ 1.200,00 | Pacote de 2 vagas: + R$ 250,00 · Cada vaga extra: + R$ 60,00 | — |

- **Taxa contratual:** R$ 2.000,00, em 1 a 5 parcelas, exibida separada do aluguel. Quando a divisão não é exata, a última parcela acerta os centavos (ex.: 3x = 666,67 + 666,67 + 666,66).
- **Projeção:** o CSV mostra, para cada um dos 12 meses, o aluguel, a parcela do contrato (nos meses em que houver) e o total do mês.

## Requisitos

- Python 3.8 ou superior. Não usa bibliotecas externas (só `csv` e `abc`, que já vêm com o Python).

## Como executar

```bash
git clone https://github.com/SEU-USUARIO/rentsmart.git
cd rentsmart
python rentsmart.py
```

No Linux/macOS, pode ser necessário usar `python3` no lugar de `python`.

Responda às perguntas no terminal:

1. Tipo de imóvel (1 – Apartamento, 2 – Casa, 3 – Estúdio)
2. Quartos e garagem (casa e apartamento) ou número de vagas (estúdio)
3. Se possui crianças (apenas apartamento)
4. Número de parcelas da taxa contratual (1 a 5)

Entradas inválidas (letras, números fora do intervalo, opções inexistentes) são recusadas e a pergunta é repetida.

## Exemplo de execução

Apartamento de 2 quartos, com garagem, sem crianças, contrato em 3x:

```
ALUGUEL MENSAL
  Aluguel-base (Apartamento)               R$ 700,00
  Adicional de 2 quartos                   R$ 200,00
  Vaga de garagem                          R$ 300,00
  Desconto de 5% (sem crianças)           - R$ 60,00
----------------------------------------------------
  Aluguel mensal                         R$ 1.140,00

TAXA CONTRATUAL (separada do aluguel)
  Valor total                            R$ 2.000,00
  Parcelamento                          3x de R$ 666,67

Total previsto nos 12 primeiros meses: R$ 15.680,00
```

Ao final é criado o arquivo `projecao_12_meses.csv` na mesma pasta. Ele usa `;` como separador e vírgula decimal, para abrir direto no Excel em português.

## Estrutura de classes

- `Imovel` (abstrata): aluguel-base, lista de itens do orçamento e o método `calcular_aluguel()`, que segue sempre a mesma sequência: base → adicionais → desconto.
- `ImovelComQuartos` (herda de `Imovel`): regra comum de casa e apartamento (2º quarto e garagem).
  - `Apartamento`: sobrescreve `calcular_desconto()` com a regra dos 5%.
  - `Casa`: só define seus valores.
- `Estudio` (herda de `Imovel`): regra própria de estacionamento (pacote + vagas extras).
- `Contrato`: taxa de R$ 2.000,00, número de parcelas e valor da parcela de cada mês.
- `Orcamento`: junta um imóvel e um contrato, exibe o resumo, gera a projeção e exporta o CSV.

## Arquivos

| Arquivo | Conteúdo |
| --- | --- |
| `rentsmart.py` | Código-fonte da aplicação |
| `projecao_12_meses.csv` | Exemplo de projeção gerada pelo sistema |
| `README.md` | Este arquivo |
