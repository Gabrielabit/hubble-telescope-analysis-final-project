"""
Dashboard — Observações do Telescópio Espacial Hubble (HST)
Projeto de BI — ADS Impacta
"""

import os
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

# ── Carrega dados ──────────────────────────────────────────────────────────────
DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "hst_observations.csv")
df = pd.read_csv(DATA_PATH, encoding="utf-8-sig")
df["data_observacao"] = pd.to_datetime(df["data_observacao"], errors="coerce")
df["ano"] = pd.to_numeric(df["ano"], errors="coerce")

ANOS = sorted(df["ano"].dropna().unique().astype(int))
ANO_MIN, ANO_MAX = int(min(ANOS)), int(max(ANOS))

# ── Paleta de cores ────────────────────────────────────────────────────────────
COR_FUNDO     = "#0d1117"
COR_PAINEL    = "#161b22"
COR_BORDA     = "#30363d"
COR_TEXTO     = "#e6edf3"
COR_DESTAQUE  = "#58a6ff"
PALETA        = px.colors.qualitative.Bold

# ── App ────────────────────────────────────────────────────────────────────────
app = Dash(__name__)
app.title = "HST Dashboard"


def painel(grafico_id, legenda_texto):
    """Envolve um grafico com uma legenda descritiva abaixo."""
    return html.Div([
        dcc.Graph(id=grafico_id),
        html.P(
            legenda_texto,
            style={
                "color": "#8b949e",
                "fontSize": "12px",
                "margin": "8px 4px 4px 4px",
                "lineHeight": "1.5",
                "borderTop": f"1px solid {COR_BORDA}",
                "paddingTop": "8px",
            }
        )
    ], style={
        "flex": "1",
        "backgroundColor": COR_PAINEL,
        "border": f"1px solid {COR_BORDA}",
        "borderRadius": "8px",
        "padding": "12px"
    })

app.layout = html.Div(style={"backgroundColor": COR_FUNDO, "minHeight": "100vh", "fontFamily": "Segoe UI, sans-serif", "padding": "24px"}, children=[

    # Cabeçalho
    html.Div([
        html.H1("🔭 Telescópio Espacial Hubble", style={"color": COR_DESTAQUE, "margin": 0, "fontSize": "28px"}),
        html.P("Análise de observações científicas — dataset ESA/MAST", style={"color": "#8b949e", "margin": "4px 0 0 0"}),
    ], style={"marginBottom": "24px"}),

    # Filtro de período
    html.Div([
        html.Label("Filtrar por período:", style={"color": COR_TEXTO, "fontWeight": "600", "marginBottom": "8px", "display": "block"}),
        dcc.RangeSlider(
            id="slider-ano",
            min=ANO_MIN, max=ANO_MAX,
            value=[ANO_MIN, ANO_MAX],
            marks={str(a): {"label": str(a), "style": {"color": "#8b949e", "fontSize": "11px"}}
                   for a in ANOS if a % 5 == 0},
            tooltip={"placement": "bottom", "always_visible": True},
            step=1
        ),
    ], style={"backgroundColor": COR_PAINEL, "border": f"1px solid {COR_BORDA}", "borderRadius": "8px", "padding": "20px", "marginBottom": "20px"}),

    # KPIs
    html.Div(id="kpis", style={"display": "flex", "gap": "16px", "marginBottom": "20px"}),

    # Linha 1: barras + linhas
    html.Div([
        painel("graf-instrumento",
               "Cada barra representa um instrumento cientifico instalado no Hubble (ex: WFC3, ACS). "
               "O comprimento indica quantas observacoes foram feitas com aquele instrumento no periodo selecionado."),
        painel("graf-ano",
               "Linha do tempo mostrando como o volume de observacoes cientificas variou a cada ano. "
               "Picos indicam periodos de alta atividade; quedas podem refletir manutencoes ou substituicao de instrumentos."),
    ], style={"display": "flex", "gap": "16px", "marginBottom": "20px"}),

    # Linha 2: rosca + barras filtros
    html.Div([
        painel("graf-banda",
               "O espectro eletromagnetico e dividido em regioes: Infravermelho (calor), Optico (luz visivel), "
               "Ultravioleta (energia alta) e Raio-X. O grafico mostra em qual regiao o Hubble mais observou no periodo."),
        painel("graf-filtros",
               "Filtros opticos sao como 'oculos coloridos' acoplados aos instrumentos — cada um deixa passar apenas "
               "um intervalo especifico de luz. Os mais usados revelam as linhas de emissao de hidrogenio, oxigenio e infravermelho proximo."),
    ], style={"display": "flex", "gap": "16px", "marginBottom": "20px"}),

    # Linha 3: exposição + tipo alvo
    html.Div([
        painel("graf-exposicao",
               "Tempo de exposicao e o quanto o sensor ficou aberto para captar luz de um alvo. "
               "Exposicoes curtas (menos de 500s) sao usadas para objetos brilhantes; exposicoes longas (acima de 2000s) "
               "capturam objetos muito distantes ou tenues, como galaxias primordiais."),
        painel("graf-alvo",
               "Classifica os objetos astronomicos observados: estrelas individuais, galaxias, nebulosas (nuvens de gas "
               "onde nascem estrelas), aglomerados estelares e campos (regioes do ceu sem alvo especifico, usados para mapeamento)."),
    ], style={"display": "flex", "gap": "16px"}),

    # Rodapé
    html.P("Fonte: ESA HST TAP Service — caom2.observation / caom2.plane",
           style={"color": "#484f58", "textAlign": "center", "marginTop": "32px", "fontSize": "12px"}),
])


def layout_grafico(title):
    return dict(
        title=dict(text=title, font=dict(color=COR_TEXTO, size=14)),
        paper_bgcolor=COR_PAINEL,
        plot_bgcolor=COR_PAINEL,
        font=dict(color=COR_TEXTO),
        margin=dict(l=40, r=20, t=50, b=40),
        xaxis=dict(gridcolor=COR_BORDA, linecolor=COR_BORDA),
        yaxis=dict(gridcolor=COR_BORDA, linecolor=COR_BORDA),
    )


def painel(grafico_id, legenda_texto):
    """Envolve um grafico com uma legenda descritiva abaixo."""
    return html.Div([
        dcc.Graph(id=grafico_id),
        html.P(
            legenda_texto,
            style={
                "color": "#8b949e",
                "fontSize": "12px",
                "margin": "8px 4px 4px 4px",
                "lineHeight": "1.5",
                "borderTop": f"1px solid {COR_BORDA}",
                "paddingTop": "8px",
            }
        )
    ], style={
        "flex": "1",
        "backgroundColor": COR_PAINEL,
        "border": f"1px solid {COR_BORDA}",
        "borderRadius": "8px",
        "padding": "12px"
    })


@app.callback(
    Output("kpis", "children"),
    Output("graf-instrumento", "figure"),
    Output("graf-ano", "figure"),
    Output("graf-banda", "figure"),
    Output("graf-filtros", "figure"),
    Output("graf-exposicao", "figure"),
    Output("graf-alvo", "figure"),
    Input("slider-ano", "value"),
)
def atualizar(periodo):
    ano_i, ano_f = periodo
    d = df[(df["ano"] >= ano_i) & (df["ano"] <= ano_f)].copy()

    # ── KPIs ──────────────────────────────────────────────────────────────────
    total      = len(d)
    instrumentos = d["instrumento_base"].nunique()
    exp_media  = d["tempo_exposicao_s"].median()
    alvos      = d["nome_alvo"].nunique()

    def kpi(label, valor, cor=COR_DESTAQUE, descricao=""):
        return html.Div([
            html.P(label, style={"color": "#8b949e", "margin": "0 0 4px 0", "fontSize": "12px", "fontWeight": "600"}),
            html.P(str(valor), style={"color": cor, "margin": "0 0 6px 0", "fontSize": "28px", "fontWeight": "700"}),
            html.P(descricao, style={"color": "#484f58", "margin": 0, "fontSize": "11px", "lineHeight": "1.4"}),
        ], style={"flex": "1", "backgroundColor": COR_PAINEL, "border": f"1px solid {COR_BORDA}",
                  "borderRadius": "8px", "padding": "16px 20px"})

    kpis = [
        kpi("Total de Observacoes", f"{total:,}", COR_DESTAQUE,
            "Numero de imagens cientificas registradas pelo Hubble no periodo filtrado."),
        kpi("Instrumentos Distintos", instrumentos, "#3fb950",
            "Quantidade de instrumentos diferentes utilizados nas observacoes."),
        kpi("Exposicao Mediana (s)", f"{exp_media:,.0f}", "#f78166",
            "Metade das observacoes durou menos que esse tempo (em segundos)."),
        kpi("Alvos Unicos", alvos, "#d2a8ff",
            "Numero de objetos astronomicos distintos observados no periodo."),
    ]

    # ── Gráfico 1: Observações por instrumento ────────────────────────────────
    inst = d["instrumento_base"].value_counts().reset_index()
    inst.columns = ["Instrumento", "Quantidade"]
    fig1 = px.bar(inst, x="Quantidade", y="Instrumento", orientation="h",
                  color="Instrumento", color_discrete_sequence=PALETA,
                  labels={"Quantidade": "Numero de Observacoes", "Instrumento": ""})
    fig1.update_layout(**layout_grafico("Numero de Observacoes por Instrumento do Hubble"))
    fig1.update_traces(showlegend=False)

    # ── Gráfico 2: Evolução por ano ───────────────────────────────────────────
    por_ano = d.groupby("ano").size().reset_index(name="Quantidade")
    por_ano.columns = ["Ano", "Quantidade"]
    fig2 = px.line(por_ano, x="Ano", y="Quantidade",
                   markers=True, color_discrete_sequence=[COR_DESTAQUE],
                   labels={"Ano": "Ano da Observacao", "Quantidade": "Numero de Observacoes"})
    fig2.update_layout(**layout_grafico("Evolucao do Volume de Observacoes ao Longo dos Anos"))

    # ── Gráfico 3: Distribuição por banda espectral ───────────────────────────
    TRADUCAO_BANDA = {
        "Infrared":    "Infravermelho",
        "Optical":     "Óptico (Luz Visível)",
        "UV":          "Ultravioleta",
        "EUV":         "UV Extremo",
        "X-ray":       "Raio-X",
        "Radio":       "Rádio",
        "Desconhecida":"Não Classificada",
    }
    banda = d["banda_espectral"].fillna("Não Classificada")
    banda = banda.map(lambda x: TRADUCAO_BANDA.get(x, x)).value_counts().reset_index()
    banda.columns = ["Banda Espectral", "Quantidade"]
    fig3 = px.pie(banda, names="Banda Espectral", values="Quantidade", hole=0.45,
                  color_discrete_sequence=PALETA)
    fig3.update_traces(textposition="inside", textinfo="percent+label")
    fig3.update_layout(**layout_grafico("Distribuicao por Regiao do Espectro Eletromagnetico"))

    # ── Gráfico 4: Top 10 filtros ─────────────────────────────────────────────
    filtros = d["filtro"].fillna("Sem filtro").value_counts().head(10).reset_index()
    filtros.columns = ["Filtro Optico", "Quantidade"]
    fig4 = px.bar(filtros, x="Filtro Optico", y="Quantidade",
                  color="Filtro Optico", color_discrete_sequence=PALETA,
                  labels={"Filtro Optico": "Filtro Optico", "Quantidade": "Numero de Observacoes"})
    fig4.update_layout(**layout_grafico("Top 10 Filtros Opticos Mais Utilizados"))
    fig4.update_layout(xaxis_tickangle=-35)
    fig4.update_traces(showlegend=False)

    # ── Gráfico 5: Distribuição do tempo de exposição ─────────────────────────
    exp = d["tempo_exposicao_s"].dropna().rename("Tempo de Exposicao (segundos)")
    fig5 = px.histogram(exp, nbins=50, color_discrete_sequence=[COR_DESTAQUE],
                        labels={"Tempo de Exposicao (segundos)": "Duracao da Exposicao (segundos)",
                                "count": "Numero de Observacoes"})
    fig5.update_layout(**layout_grafico("Distribuicao da Duracao das Exposicoes"))
    fig5.update_layout(showlegend=False)

    # ── Gráfico 6: Top 10 tipos de alvo ──────────────────────────────────────
    TRADUCAO_ALVO = {
        "field":          "Campo Estelar",
        "galaxy":         "Galaxia",
        "star":           "Estrela",
        "cluster":        "Aglomerado",
        "nebula":         "Nebulosa",
        "solar system":   "Sistema Solar",
        "quasar":         "Quasar",
        "supernova":      "Supernova",
        "globular":       "Aglomerado Globular",
        "calibration":    "Calibracao",
        "N/A":            "Nao Informado",
    }
    alvo = d["tipo_alvo"].fillna("Nao Informado")
    alvo = alvo.map(lambda x: TRADUCAO_ALVO.get(x, x)).value_counts().head(10).reset_index()
    alvo.columns = ["Tipo de Alvo", "Quantidade"]
    fig6 = px.bar(alvo, x="Tipo de Alvo", y="Quantidade",
                  color="Tipo de Alvo", color_discrete_sequence=PALETA,
                  labels={"Tipo de Alvo": "Tipo de Alvo Astronomico", "Quantidade": "Numero de Observacoes"})
    fig6.update_layout(**layout_grafico("Top 10 Tipos de Alvo Astronomico Observados"))
    fig6.update_layout(xaxis_tickangle=-25)
    fig6.update_traces(showlegend=False)

    return kpis, fig1, fig2, fig3, fig4, fig5, fig6


if __name__ == "__main__":
    print("\nDashboard rodando em: http://127.0.0.1:8050\n")
    app.run(debug=False)
