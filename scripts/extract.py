"""
Extração de metadados de observações do Telescópio Espacial Hubble (HST)
Fonte: ESA HST TAP Service (https://hst.esac.esa.int/tap-server/tap)
"""

import requests
import pandas as pd
import json
import os

TAP_URL = "https://hst.esac.esa.int/tap-server/tap/sync"

QUERY = """
SELECT TOP 2000
    o.observationid,
    o.proposal_id,
    o.proposal_pi,
    o.instrument_name,
    o.target_name,
    o.target_type,
    o.intent,
    o.telescope_name,
    p.calibrationlevel,
    p.dataproducttype,
    p.time_bounds_lower,
    p.time_bounds_upper,
    p.time_exposure,
    p.energy_bandpassname,
    p.energy_energybands,
    p.position_bounds_size
FROM caom2.observation o
JOIN caom2.plane p ON p.obsid = o.obsid
WHERE o.collection = 'HST'
AND o.intent = 'science'
AND p.calibrationlevel = 2
AND p.dataproducttype = 'image'
"""

def fetch_observations():
    print("Consultando ESA HST TAP Service...")
    params = {
        "REQUEST": "doQuery",
        "LANG": "ADQL",
        "FORMAT": "json",
        "QUERY": QUERY.strip()
    }
    response = requests.get(TAP_URL, params=params, timeout=120)
    response.raise_for_status()
    data = response.json()

    cols = [m["name"] for m in data["metadata"]]
    rows = data["data"]
    print(f"Registros retornados: {len(rows)}")
    return pd.DataFrame(rows, columns=cols)


def transform(df):
    rename = {
        "observationid":        "id_observacao",
        "proposal_id":          "id_proposta",
        "proposal_pi":          "pesquisador_principal",
        "instrument_name":      "instrumento",
        "target_name":          "nome_alvo",
        "target_type":          "tipo_alvo",
        "intent":               "intencao",
        "telescope_name":       "telescopio",
        "calibrationlevel":     "nivel_calibracao",
        "dataproducttype":      "tipo_dado",
        "time_bounds_lower":    "data_inicio_mjd",
        "time_bounds_upper":    "data_fim_mjd",
        "time_exposure":        "tempo_exposicao_s",
        "energy_bandpassname":  "filtro",
        "energy_energybands":   "banda_espectral",
        "position_bounds_size": "tamanho_campo_graus"
    }
    df = df.rename(columns={k: v for k, v in rename.items() if k in df.columns})

    # Converte MJD para data legível
    for col_mjd, col_dt in [("data_inicio_mjd", "data_observacao"), ("data_fim_mjd", "data_fim")]:
        if col_mjd in df.columns:
            df[col_mjd] = pd.to_numeric(df[col_mjd], errors="coerce")
            df[col_dt] = pd.to_datetime(
                df[col_mjd], unit="D", origin="1858-11-17", errors="coerce"
            )

    if "data_observacao" in df.columns:
        df["ano"]       = df["data_observacao"].dt.year
        df["mes"]       = df["data_observacao"].dt.month
        df["decada"]    = (df["ano"] // 10 * 10).astype("Int64")

    # Extrai instrumento base (ex: "ACS/WFC" -> "ACS")
    if "instrumento" in df.columns:
        df["instrumento_base"] = df["instrumento"].str.split("/").str[0]

    return df


def save(df, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False, encoding="utf-8-sig")
    print(f"CSV salvo: {path}")
    print(f"Shape: {df.shape}")


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(__file__), "..", "data", "hst_observations.csv")

    df = fetch_observations()
    df = transform(df)

    print("\nAmostra:")
    print(df[["id_observacao", "instrumento", "nome_alvo", "filtro", "data_observacao", "tempo_exposicao_s"]].head(5).to_string())

    print("\nInstrumentos mais usados:")
    print(df["instrumento_base"].value_counts().head(10))

    save(df, out)
    print("\nExtração concluída!")
