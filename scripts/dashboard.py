"""
Dashboard — Observacoes do Telescopio Espacial Hubble (HST)
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

ANOS    = sorted(df["ano"].dropna().unique().astype(int))
ANO_MIN = int(min(ANOS))
ANO_MAX = int(max(ANOS))

# ── Paleta ────────────────────────────────────────────────────────────────────
COR_FUNDO    = "#0d1117"
COR_PAINEL   = "#161b22"
COR_BORDA    = "#30363d"
COR_TEXTO    = "#e6edf3"
COR_DESTAQUE = "#58a6ff"
COR_LEGENDA  = "#adbac7"
PALETA       = px.colors.qualitative.Bold

# ── Helpers ───────────────────────────────────────────────────────────────────
def layout_grafico(title):
    return dict(
        title=dict(text=title, font=dict(color=COR_TEXTO, size=15)),
        paper_bgcolor=COR_PAINEL,
        plot_bgcolor=COR_PAINEL,
        font=dict(color=COR_TEXTO, size=13),
        margin=dict(l=40, r=20, t=50, b=40),
        xaxis=dict(gridcolor=COR_BORDA, linecolor=COR_BORDA),
        yaxis=dict(gridcolor=COR_BORDA, linecolor=COR_BORDA),
    )


def painel(grafico_id, legenda_texto):
    return html.Div([
        dcc.Graph(id=grafico_id),
        html.P(legenda_texto, style={
            "color": COR_LEGENDA,
            "fontSize": "14px",
            "margin": "10px 4px 4px 4px",
            "lineHeight": "1.6",
            "borderTop": f"1px solid {COR_BORDA}",
            "paddingTop": "10px",
            "fontStyle": "italic",
        })
    ], style={
        "flex": "1",
        "backgroundColor": COR_PAINEL,
        "border": f"1px solid {COR_BORDA}",
        "borderRadius": "8px",
        "padding": "12px",
    })


def foto(src, titulo, descricao):
    return html.Div([
        html.Img(src=src, style={
            "width": "100%",
            "height": "200px",
            "objectFit": "cover",
            "borderRadius": "6px",
            "display": "block",
        }),
        html.P(titulo, style={
            "color": COR_DESTAQUE,
            "fontSize": "14px",
            "fontWeight": "700",
            "margin": "10px 0 4px 0",
        }),
        html.P(descricao, style={
            "color": COR_LEGENDA,
            "fontSize": "13px",
            "margin": 0,
            "lineHeight": "1.5",
            "fontStyle": "italic",
        }),
    ], style={
        "flex": "1",
        "backgroundColor": COR_PAINEL,
        "border": f"1px solid {COR_BORDA}",
        "borderRadius": "8px",
        "padding": "12px",
    })


# ── App ───────────────────────────────────────────────────────────────────────
app = Dash(__name__, assets_folder=os.path.join(os.path.dirname(__file__), "..", "assets"))
app.title = "HST Dashboard"

app.layout = html.Div(style={
    "backgroundColor": COR_FUNDO,
    "minHeight": "100vh",
    "fontFamily": "Segoe UI, sans-serif",
    "padding": "24px",
}, children=[

    # ── Cabecalho ──────────────────────────────────────────────────────────────
    html.Div([
        html.Div([
            html.H1("Telescopio Espacial Hubble", style={
                "color": COR_DESTAQUE, "margin": 0, "fontSize": "30px", "fontWeight": "700",
            }),
            html.P(
                "Dashboard de analise das observacoes cientificas registradas pelo HST — fonte: ESA/MAST",
                style={"color": "#8b949e", "margin": "6px 0 0 0", "fontSize": "15px"}
            ),
        ], style={"flex": "1"}),
        html.Img(src="/assets/hubble_telescope.jpg", style={
            "height": "80px", "borderRadius": "8px", "objectFit": "cover",
            "border": f"2px solid {COR_BORDA}",
        }),
    ], style={"display": "flex", "alignItems": "center", "gap": "20px", "marginBottom": "24px"}),

    # ── Galeria de imagens ─────────────────────────────────────────────────────
    html.Div([
        foto("/assets/hubble_pillars.jpg",
             "Pilares da Criacao",
             "Fotografia iconica capturada pelo Hubble em 1995 e refeita em 2014 com o instrumento WFC3. "
             "Sao colunas de gas e poeira na Nebulosa da Aguia (M16) onde novas estrelas estao se formando."),
        foto("/assets/hubble_galaxy.jpg",
             "Galaxia NGC 4414",
             "Galaxia espiral a cerca de 60 milhoes de anos-luz da Terra, fotografada pelo Hubble para medir "
             "a taxa de expansao do universo (constante de Hubble)."),
        foto("/assets/hubble_star.jpg",
             "Nebulosa do Caranguejo (M1)",
             "Remanescente de uma supernova observada em 1054 d.C. O Hubble revelou filamentos de gas em "
             "expansao a 1.500 km/s — o que restou de uma explosao estelar."),
        foto("/assets/hubble_telescope.jpg",
             "O Telescopio Hubble",
             "Lancado em 1990, o HST orbita a Terra a 547 km de altitude. Ja realizou mais de 1,5 milhao de "
             "observacoes e ajudou a descobrir que o universo tem 13,8 bilhoes de anos."),
    ], style={"display": "flex", "gap": "16px", "marginBottom": "20px"}),

    # ── Filtro de periodo ─────────────────────────────────────────────────────
    html.Div([
        html.Label("Filtrar por periodo de observacao:", style={
            "color": COR_TEXTO, "fontWeight": "600", "marginBottom": "8px",
            "display": "block", "fontSize": "15px",
        }),
        dcc.RangeSlider(
            id="slider-ano",
            min=ANO_MIN, max=ANO_MAX,
            value=[ANO_MIN, ANO_MAX],
            marks={str(a): {"label": str(a), "style": {"color": "#8b949e", "fontSize": "12px"}}
                   for a in ANOS if a % 5 == 0},
            tooltip={"placement": "bottom", "always_visible": True},
            step=1,
        ),
    ], style={
        "backgroundColor": COR_PAINEL,
        "border": f"1px solid {COR_BORDA}",
        "borderRadius": "8px",
        "padding": "20px",
        "marginBottom": "20px",
    }),

    # ── KPIs ───────────────────────────────────────────────────────────────────
    html.Div(id="kpis", style={"display": "flex", "gap": "16px", "marginBottom": "20px"}),

    # ── Linha 1 ────────────────────────────────────────────────────────────────
    html.Div([
        painel("graf-instrumento",
               "Cada barra representa um instrumento cientifico instalado no Hubble (WFC3, ACS, NICMOS, etc.). "
               "O comprimento mostra quantas observacoes foram registradas com aquele instrumento no periodo selecionado."),
        painel("graf-ano",
               "Linha do tempo do volume de observacoes por ano. Picos indicam periodos de alta atividade; "
               "quedas podem refletir missoes de manutencao do telescopio ou substituicao de instrumentos."),
    ], style={"display": "flex", "gap": "16px", "marginBottom": "20px"}),

    # ── Linha 2 ────────────────────────────────────────────────────────────────
    html.Div([
        painel("graf-banda",
               "O espectro eletromagnetico e dividido em regioes por comprimento de onda. Infravermelho detecta "
               "calor e atravessa nuvens de poeira; Optico e a luz visivel; Ultravioleta revela estrelas jovens e quentes."),
        painel("graf-filtros",
               "Filtros opticos funcionam como 'oculos coloridos' — cada um deixa passar apenas uma faixa estreita de luz. "
               "Exemplo: F160W captura infravermelho proximo (1,6 micrometros), ideal para observar galaxias distantes."),
    ], style={"display": "flex", "gap": "16px", "marginBottom": "20px"}),

    # ── Linha 3 ────────────────────────────────────────────────────────────────
    html.Div([
        painel("graf-exposicao",
               "Tempo de exposicao e a duracao que o sensor ficou captando luz. Objetos brilhantes exigem exposicoes "
               "curtas (menos de 500s); galaxias e nebulosas distantes precisam de exposicoes longas (acima de 2000s) "
               "para acumular fotons suficientes."),
        painel("graf-alvo",
               "Classifica os objetos astronomicos alvo das observacoes: estrelas individuais, galaxias (sistemas de "
               "bilhoes de estrelas), nebulosas (nuvens de gas e poeira), aglomerados estelares e campos (mapeamentos "
               "de regioes do ceu sem alvo especifico)."),
    ], style={"display": "flex", "gap": "16px"}),

    # ── Rodape ─────────────────────────────────────────────────────────────────
    html.P(
        "Fonte dos dados: ESA HST TAP Service (caom2.observation / caom2.plane) | "
        "Imagens: NASA/ESA Hubble Space Telescope | Projeto ADS Impacta",
        style={"color": "#484f58", "textAlign": "center", "marginTop": "32px", "fontSize": "13px"},
    ),
])


# ── Callback ──────────────────────────────────────────────────────────────────
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

    total        = len(d)
    instrumentos = d["instrumento_base"].nunique()
    exp_mediana  = d["tempo_exposicao_s"].median()
    alvos        = d["nome_alvo"].nunique()

    def kpi(label, valor, cor=COR_DESTAQUE, descricao=""):
        return html.Div([
            html.P(label, style={
                "color": "#8b949e", "margin": "0 0 4px 0",
                "fontSize": "13px", "fontWeight": "600",
            }),
            html.P(str(valor), style={
                "color": cor, "margin": "0 0 8px 0",
                "fontSize": "30px", "fontWeight": "700",
            }),
            html.P(descricao, style={
                "color": COR_LEGENDA, "margin": 0,
                "fontSize": "13px", "lineHeight": "1.5", "fontStyle": "italic",
            }),
        ], style={
            "flex": "1",
            "backgroundColor": COR_PAINEL,
            "border": f"1px solid {COR_BORDA}",
            "borderRadius": "8px",
            "padding": "16px 20px",
        })

    kpis = [
        kpi("Total de Observacoes", f"{total:,}", COR_DESTAQUE,
            "Numero de imagens cientificas registradas pelo Hubble no periodo filtrado."),
        kpi("Instrumentos Distintos", instrumentos, "#3fb950",
            "Quantidade de instrumentos diferentes usados nas observacoes."),
        kpi("Exposicao Mediana", f"{exp_mediana:,.0f} s", "#f78166",
            "Metade das observacoes durou menos que esse tempo. Quanto maior, mais objetos tenues foram estudados."),
        kpi("Alvos Unicos", alvos, "#d2a8ff",
            "Quantidade de objetos astronomicos distintos observados no periodo selecionado."),
    ]

    # Graf 1 — Instrumento
    inst = d["instrumento_base"].value_counts().reset_index()
    inst.columns = ["Instrumento", "Quantidade"]
    fig1 = px.bar(inst, x="Quantidade", y="Instrumento", orientation="h",
                  color="Instrumento", color_discrete_sequence=PALETA,
                  labels={"Quantidade": "Numero de Observacoes", "Instrumento": ""})
    fig1.update_layout(**layout_grafico("Observacoes por Instrumento Cientifico"))
    fig1.update_traces(showlegend=False)

    # Graf 2 — Evolucao por ano
    por_ano = d.groupby("ano").size().reset_index(name="Quantidade")
    por_ano.columns = ["Ano", "Quantidade"]
    fig2 = px.line(por_ano, x="Ano", y="Quantidade", markers=True,
                   color_discrete_sequence=[COR_DESTAQUE],
                   labels={"Ano": "Ano", "Quantidade": "Numero de Observacoes"})
    fig2.update_layout(**layout_grafico("Volume de Observacoes por Ano"))

    # Graf 3 — Banda espectral
    BANDA = {
        "Infrared": "Infravermelho", "Optical": "Optico (Luz Visivel)",
        "UV": "Ultravioleta", "EUV": "UV Extremo",
        "X-ray": "Raio-X", "Radio": "Radio",
    }
    banda = d["banda_espectral"].fillna("Nao Classificada")
    banda = banda.map(lambda x: BANDA.get(x, x)).value_counts().reset_index()
    banda.columns = ["Banda Espectral", "Quantidade"]
    fig3 = px.pie(banda, names="Banda Espectral", values="Quantidade", hole=0.45,
                  color_discrete_sequence=PALETA)
    fig3.update_traces(textposition="inside", textinfo="percent+label",
                       textfont=dict(size=13))
    fig3.update_layout(**layout_grafico("Distribuicao por Regiao do Espectro"))

    # Graf 4 — Filtros
    filtros = d["filtro"].fillna("Sem filtro").value_counts().head(10).reset_index()
    filtros.columns = ["Filtro", "Quantidade"]
    fig4 = px.bar(filtros, x="Filtro", y="Quantidade",
                  color="Filtro", color_discrete_sequence=PALETA,
                  labels={"Filtro": "Filtro Optico", "Quantidade": "Numero de Observacoes"})
    fig4.update_layout(**layout_grafico("Top 10 Filtros Opticos Mais Utilizados"))
    fig4.update_layout(xaxis_tickangle=-35)
    fig4.update_traces(showlegend=False)

    # Graf 5 — Tempo de exposicao
    exp = d["tempo_exposicao_s"].dropna().rename("Duracao da Exposicao (segundos)")
    fig5 = px.histogram(exp, nbins=50, color_discrete_sequence=[COR_DESTAQUE],
                        labels={"Duracao da Exposicao (segundos)": "Duracao (segundos)",
                                "count": "Numero de Observacoes"})
    fig5.update_layout(**layout_grafico("Distribuicao da Duracao das Exposicoes"))
    fig5.update_layout(showlegend=False)

    # Graf 6 — Tipo de alvo
    ALVO = {
        "field": "Campo Estelar", "galaxy": "Galaxia", "star": "Estrela",
        "cluster": "Aglomerado", "nebula": "Nebulosa",
        "solar system": "Sistema Solar", "quasar": "Quasar",
        "supernova": "Supernova", "globular": "Aglomerado Globular",
        "calibration": "Calibracao",
    }
    alvo = d["tipo_alvo"].fillna("Nao Informado")
    alvo = alvo.map(lambda x: ALVO.get(x, x)).value_counts().head(10).reset_index()
    alvo.columns = ["Tipo de Alvo", "Quantidade"]
    fig6 = px.bar(alvo, x="Tipo de Alvo", y="Quantidade",
                  color="Tipo de Alvo", color_discrete_sequence=PALETA,
                  labels={"Tipo de Alvo": "Tipo de Alvo", "Quantidade": "Numero de Observacoes"})
    fig6.update_layout(**layout_grafico("Top 10 Tipos de Alvo Astronomico"))
    fig6.update_layout(xaxis_tickangle=-25)
    fig6.update_traces(showlegend=False)

    return kpis, fig1, fig2, fig3, fig4, fig5, fig6


if __name__ == "__main__":
    print("\nDashboard rodando em: http://127.0.0.1:8050\n")
    app.run(debug=False)
