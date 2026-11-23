# Análise de Observações do Telescópio Espacial Hubble (HST)

Projeto de BI e Análise de Dados — ADS Impacta  
Aluna: Gabriela

---

## Descrição

Análise exploratória e dashboard de observações científicas do Telescópio Espacial Hubble (HST), utilizando metadados públicos disponibilizados pela ESA (European Space Agency) via serviço TAP (Table Access Protocol).

O projeto responde perguntas como:
- Quais instrumentos do Hubble foram mais utilizados ao longo dos anos?
- Como a distribuição de observações evoluiu por década?
- Quais filtros e bandas espectrais são mais comuns?
- Quais tipos de alvos astronômicos são mais observados?

---

## Dataset

**Fonte:** ESA HST TAP Service  
**URL:** https://hst.esac.esa.int/tap-server/tap  
**Tabelas utilizadas:** `caom2.observation`, `caom2.plane`  
**Volume:** 2.000 observações calibradas (nível 2), tipo imagem, intenção científica

---

## Tecnologias

- **Python 3.12** — extração e transformação dos dados
- **Pandas** — manipulação e limpeza
- **Power BI** — dashboard e visualizações

---

## Estrutura do Projeto

```
ads-impacta-final-project/
├── data/
│   └── hst_observations.csv     # Dataset extraído (2000 registros)
├── scripts/
│   └── extract.py               # Script de extração via API ESA TAP
├── diagrams/
│   └── MER.png                  # Modelo Entidade-Relacionamento
└── README.md
```

---

## Como executar

1. Instale as dependências:
```bash
pip install pandas requests
```

2. Execute o script de extração:
```bash
python scripts/extract.py
```

O arquivo `data/hst_observations.csv` será gerado automaticamente.

3. Abra o dashboard no Power BI Desktop conectando ao CSV gerado.

---

## Colunas do Dataset

| Coluna | Descrição |
|--------|-----------|
| id_observacao | Identificador único da observação |
| id_proposta | ID da proposta científica aprovada |
| pesquisador_principal | Nome do PI (Principal Investigator) |
| instrumento | Instrumento utilizado (ex: WFC3/IR, ACS/WFC) |
| instrumento_base | Família do instrumento (ex: WFC3, ACS) |
| nome_alvo | Nome do objeto astronômico observado |
| tipo_alvo | Classificação do alvo |
| telescopio | Nome do telescópio (HST) |
| nivel_calibracao | Nível de processamento dos dados |
| tipo_dado | Tipo do produto (image) |
| data_inicio_mjd | Data de início em Modified Julian Date |
| data_observacao | Data de início convertida para datetime |
| ano / mes / decada | Componentes temporais da observação |
| tempo_exposicao_s | Tempo de exposição em segundos |
| filtro | Filtro óptico utilizado (ex: F160W) |
| banda_espectral | Banda do espectro (ex: Infrared, Optical) |
| tamanho_campo_graus | Tamanho do campo de visão em graus |
