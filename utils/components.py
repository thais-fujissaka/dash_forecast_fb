import pandas as pd
import streamlit as st
from utils.functions.date_functions import *
import io

def input_periodo_datas(key):
    today = get_today()
    jan_this_year = get_jan_this_year(today)
    first_day_this_month_this_year = get_first_day_this_month_this_year(today)
    last_day_this_month_this_year = get_last_day_this_month_this_year(today)

    # Inicializa o input com o mês atual
    date_input = st.date_input("Período",
                            value=(first_day_this_month_this_year, last_day_this_month_this_year),
                            min_value=jan_this_year,
                            format="DD/MM/YYYY",
                            key=key
                            )
    return date_input

def input_selecao_casas(key):
    
    df_casas = st.session_state["df_casas"]

    lista_casas_validas = df_casas["Casa"].to_list()
    df_validas = pd.DataFrame(lista_casas_validas, columns=["Casa"])
    casa = st.selectbox("Casa", lista_casas_validas, key=key)

    df = df_casas.merge(df_validas, on="Casa", how="inner")
    # Definindo um dicionário para mapear nomes de casas a IDs de casas
    mapeamento_ids = dict(zip(df["Casa"], df["ID_Casa"]))
    # Definindo um dicionário para mapear IDs de casas a IDs da Zigpay
    mapeamento_zigpay = dict(zip(df["Casa"], df["ID_Zigpay"]))

    # Obtendo o ID da casa selecionada
    id_casa = mapeamento_ids[casa]
    # Obtendo o ID da Zigpay correspondente ao ID da casa
    id_zigpay = mapeamento_zigpay[casa]

    return id_casa, casa, id_zigpay


def button_download(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Planilha")
    excel_data = output.getvalue()

    st.download_button(
        label="📥 Download Excel",
        data=excel_data,
        file_name="data.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )



    
