# Análise de Observações do Telescópio Espacial Hubble (HST)

Projeto de BI e Análise de Dados — ADS Impacta  
Aluna: Gabriela

---

## Descrição

Análise exploratória e dashboard interativo de observações científicas do Telescópio Espacial Hubble (HST), utilizando metadados públicos disponibilizados pela ESA (European Space Agency) via serviço TAP (Table Access Protocol).

O projeto responde perguntas como:
- Quais instrumentos do Hubble foram mais utilizados ao longo dos anos?
- Como a distribuição de observações evoluiu por década?
- Quais filtros e bandas espectrais são mais comuns?
- Quais tipos de alvos astronômicos são mais observados?
- Como varia o tempo de exposição entre diferentes tipos de observação?

---

## Dataset

| Campo | Valor |
|---|---|
| **Fonte** | ESA HST TAP Service |
| **URL** | https://hst.esac.esa.int/tap-server/tap |
| **Tabelas** | `caom2.observation`, `caom2.plane` |
| **Volume** | 2.000 observações calibradas (nível 2), tipo imagem, intenção científica |
| **Atualização** | Dados públicos, acesso via protocolo ADQL (SQL astronômico) |

---

## Ferramentas Utilizadas

### Linguagem e Runtime
| Ferramenta | Versão | Uso |
|---|---|---|
| **Python** | 3.12.10 | Linguagem principal do projeto |

### Extração e Processamento de Dados
| Ferramenta | Versão | Uso |
|---|---|---|
| **Requests** | 2.34.2 | Requisições HTTP para a API ESA TAP |
| **Pandas** | 3.1.1 | Manipulação, limpeza e transformação do dataset |
| **Pillow** | — | Redimensionamento das imagens decorativas |

### Visualização e Dashboard
| Ferramenta | Versão | Uso |
|---|---|---|
| **Plotly** | 7.1.0 | Geração dos gráficos interativos |
| **Dash** | 4.5.1 | Framework do dashboard web (Flask-based) |

### Diagramação
| Ferramenta | Uso |
|---|---|
| **draw.io** (app.diagrams.net) | Criação do MER (Modelo Entidade-Relacionamento) |

### Versionamento e Repositório
| Ferramenta | Versão | Uso |
|---|---|---|
| **Git** | 2.56.1 | Controle de versão local |
| **GitHub** | — | Hospedagem do repositório remoto |

### Fonte de Dados
| Serviço | Uso |
|---|---|
| **ESA HST TAP Service** | Consulta ADQL ao catálogo de observações do Hubble |
| **Wikimedia Commons** | Imagens decorativas do telescópio e objetos observados |

---

## Estrutura do Projeto

```
ads-impacta-final-project/
├── assets/
│   ├── hubble_galaxy.jpg        # Galáxia NGC 4414
│   ├── hubble_pillars.jpg       # Pilares da Criação
│   ├── hubble_star.jpg          # Nebulosa do Caranguejo
│   └── hubble_telescope.jpg     # O telescópio HST em órbita
├── data/
│   └── hst_observations.csv    # Dataset extraído (2.000 registros)
├── diagrams/
│   └── MER.drawio               # Modelo Entidade-Relacionamento
├── scripts/
│   ├── extract.py               # Extração de dados via API ESA TAP
│   └── dashboard.py             # Dashboard interativo (Plotly Dash)
└── README.md
```

---

## Como Executar

### 1. Instalar dependências
```bash
pip install pandas requests plotly dash Pillow
```

### 2. Extrair os dados
```bash
python scripts/extract.py
```
Gera `data/hst_observations.csv` com 2.000 observações do Hubble.

### 3. Rodar o dashboard
```bash
python scripts/dashboard.py
```
Acesse em: **http://127.0.0.1:8050**

---

## Colunas do Dataset

| Coluna | Tipo | Descrição |
|---|---|---|
| id_observacao | VARCHAR | Identificador único da observação |
| id_proposta | VARCHAR | ID da proposta científica aprovada |
| pesquisador_principal | VARCHAR | Nome do PI (Principal Investigator) |
| instrumento | VARCHAR | Instrumento utilizado (ex: WFC3/IR, ACS/WFC) |
| instrumento_base | VARCHAR | Família do instrumento (ex: WFC3, ACS) |
| nome_alvo | VARCHAR | Nome do objeto astronômico observado |
| tipo_alvo | VARCHAR | Classificação do alvo (star, galaxy, nebula…) |
| telescopio | VARCHAR | Nome do telescópio (HST) |
| nivel_calibracao | INT | Nível de processamento (2 = calibrado) |
| tipo_dado | VARCHAR | Tipo do produto (image) |
| data_inicio_mjd | FLOAT | Data de início em Modified Julian Date |
| data_observacao | DATETIME | Data de início convertida para datetime |
| data_fim | DATETIME | Data de término da observação |
| ano | INT | Ano da observação |
| mes | INT | Mês da observação |
| decada | INT | Década da observação (ex: 2000, 2010) |
| tempo_exposicao_s | FLOAT | Tempo de exposição em segundos |
| filtro | VARCHAR | Filtro óptico utilizado (ex: F160W) |
| banda_espectral | VARCHAR | Banda do espectro (Infrared, Optical, UV…) |
| tamanho_campo_graus | FLOAT | Tamanho do campo de visão em graus |

---

## MER — Modelo Entidade-Relacionamento

Arquivo: `diagrams/MER.drawio`  
Abrir em: https://app.diagrams.net

**Entidades e relacionamentos:**
- `PROPOSTA` 1 ──→ N `OBSERVACAO`
- `INSTRUMENTO` 1 ──→ N `OBSERVACAO`
- `ALVO` 1 ──→ N `OBSERVACAO`

---

## Fonte das Imagens

As imagens utilizadas no dashboard são de domínio público, creditadas à NASA/ESA e disponíveis via Wikimedia Commons.
