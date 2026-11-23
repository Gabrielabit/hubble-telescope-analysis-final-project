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
        html.Div(dcc.Graph(id="graf-instrumento"), style={"flex": "1", "backgroundColor": COR_PAINEL, "border": f"1px solid {COR_BORDA}", "borderRadius": "8px", "padding": "12px"}),
        html.Div(dcc.Graph(id="graf-ano"),         style={"flex": "1", "backgroundColor": COR_PAINEL, "border": f"1px solid {COR_BORDA}", "borderRadius": "8px", "padding": "12px"}),
    ], style={"display": "flex", "gap": "16px", "marginBottom": "20px"}),

    # Linha 2: rosca + barras filtros
    html.Div([
        html.Div(dcc.Graph(id="graf-banda"),   style={"flex": "1", "backgroundColor": COR_PAINEL, "border": f"1px solid {COR_BORDA}", "borderRadius": "8px", "padding": "12px"}),
        html.Div(dcc.Graph(id="graf-filtros"), style={"flex": "1", "backgroundColor": COR_PAINEL, "border": f"1px solid {COR_BORDA}", "borderRadius": "8px", "padding": "12px"}),
    ], style={"display": "flex", "gap": "16px", "marginBottom": "20px"}),

    # Linha 3: exposição + tipo alvo
    html.Div([
        html.Div(dcc.Graph(id="graf-exposicao"), style={"flex": "1", "backgroundColor": COR_PAINEL, "border": f"1px solid {COR_BORDA}", "borderRadius": "8px", "padding": "12px"}),
        html.Div(dcc.Graph(id="graf-alvo"),      style={"flex": "1", "backgroundColor": COR_PAINEL, "border": f"1px solid {COR_BORDA}", "borderRadius": "8px", "padding": "12px"}),
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

    def kpi(label, valor, cor=COR_DESTAQUE):
        return html.Div([
            html.P(label, style={"color": "#8b949e", "margin": "0 0 4px 0", "fontSize": "12px"}),
            html.P(str(valor), style={"color": cor, "margin": 0, "fontSize": "28px", "fontWeight": "700"}),
        ], style={"flex": "1", "backgroundColor": COR_PAINEL, "border": f"1px solid {COR_BORDA}",
                  "borderRadius": "8px", "padding": "16px 20px"})

    kpis = [
        kpi("Total de Observações", f"{total:,}"),
        kpi("Instrumentos Distintos", instrumentos, "#3fb950"),
        kpi("Exposição Mediana (s)", f"{exp_media:,.0f}", "#f78166"),
        kpi("Alvos Únicos", alvos, "#d2a8ff"),
    ]

    # ── Gráfico 1: Observações por instrumento ────────────────────────────────
    inst = d["instrumento_base"].value_counts().reset_index()
    inst.columns = ["instrumento_base", "total"]
    fig1 = px.bar(inst, x="total", y="instrumento_base", orientation="h",
                  color="instrumento_base", color_discrete_sequence=PALETA,
                  labels={"total": "Observações", "instrumento_base": ""})
    fig1.update_layout(**layout_grafico("Observações por Instrumento"))
    fig1.update_traces(showlegend=False)

    # ── Gráfico 2: Evolução por ano ───────────────────────────────────────────
    por_ano = d.groupby("ano").size().reset_index(name="total")
    fig2 = px.line(por_ano, x="ano", y="total",
                   markers=True, color_discrete_sequence=[COR_DESTAQUE],
                   labels={"ano": "Ano", "total": "Observações"})
    fig2.update_layout(**layout_grafico("Evolução de Observações por Ano"))

    # ── Gráfico 3: Distribuição por banda espectral ───────────────────────────
    banda = d["banda_espectral"].fillna("Desconhecida").value_counts().reset_index()
    banda.columns = ["banda_espectral", "total"]
    fig3 = px.pie(banda, names="banda_espectral", values="total", hole=0.45,
                  color_discrete_sequence=PALETA)
    fig3.update_layout(**layout_grafico("Distribuição por Banda Espectral"))

    # ── Gráfico 4: Top 10 filtros ─────────────────────────────────────────────
    filtros = d["filtro"].fillna("N/A").value_counts().head(10).reset_index()
    filtros.columns = ["filtro", "total"]
    fig4 = px.bar(filtros, x="filtro", y="total",
                  color="filtro", color_discrete_sequence=PALETA,
                  labels={"filtro": "Filtro", "total": "Observações"})
    fig4.update_layout(**layout_grafico("Top 10 Filtros Ópticos Utilizados"))
    fig4.update_traces(showlegend=False)

    # ── Gráfico 5: Distribuição do tempo de exposição ─────────────────────────
    exp = d["tempo_exposicao_s"].dropna()
    fig5 = px.histogram(exp, nbins=50, color_discrete_sequence=[COR_DESTAQUE],
                        labels={"value": "Tempo de Exposição (s)", "count": "Frequência"})
    fig5.update_layout(**layout_grafico("Distribuição do Tempo de Exposição"))

    # ── Gráfico 6: Top 10 tipos de alvo ──────────────────────────────────────
    alvo = d["tipo_alvo"].fillna("N/A").value_counts().head(10).reset_index()
    alvo.columns = ["tipo_alvo", "total"]
    fig6 = px.bar(alvo, x="tipo_alvo", y="total",
                  color="tipo_alvo", color_discrete_sequence=PALETA,
                  labels={"tipo_alvo": "Tipo de Alvo", "total": "Observações"})
    fig6.update_layout(**layout_grafico("Top 10 Tipos de Alvo Astronômico"))
    fig6.update_traces(showlegend=False)

    return kpis, fig1, fig2, fig3, fig4, fig5, fig6


if __name__ == "__main__":
    print("\nDashboard rodando em: http://127.0.0.1:8050\n")
    app.run(debug=False)
