import streamlit as st
import pandas as pd
from datetime import datetime

# --------------------------
# Tradução de meses para PT
# --------------------------
MESES_PT = {
    "January": "Janeiro",
    "February": "Fevereiro",
    "March": "Março",
    "April": "Abril",
    "May": "Maio",
    "June": "Junho",
    "July": "Julho",
    "August": "Agosto",
    "September": "Setembro",
    "October": "Outubro",
    "November": "Novembro",
    "December": "Dezembro",
}

# --------------------------
# Carregar dados
# --------------------------
df = pd.read_excel("aniversariantes.xlsx")
df["DATA NASCIMENTO"] = pd.to_datetime(df["DATA NASCIMENTO"], format="%d/%m/%Y")
hoje = datetime.today()

# --------------------------
# CSS customizado
# --------------------------
st.markdown("""
    <style>
        .card {
            background-color: #ffffff;
            padding: 15px;
            border-radius: 20px;
            box-shadow: 0px 4px 12px rgba(0,0,0,0.15);
            text-align: center;
            margin-bottom: 15px;
        }
        .card img {
            border-radius: 22%;
            margin-bottom: 10px;
            border: 3px solid #000000;
            width: 170px;
        }
        .nome {
            font-size: 20px;
            font-weight: bold;
            margin: 5px 0;
        }
        .data-aniversario {
            font-size: 16px;
            color: #555;
        }
        .linha {
            display: flex;
            align-items: center;
            margin-bottom: 12px;
            background-color: #f8f8f8;
            padding: 8px;
            border-radius: 12px;
            box-shadow: 0px 2px 6px rgba(0,0,0,0.1);
        }
        .linha img {
            border-radius: 20%;
            margin-right: 15px;
            border: 2px solid #000000;
        }
        .nome-linha {
            font-size: 18px;
            font-weight: bold;
            flex: 1;
        }
        .data-linha {
            font-size: 16px;
            color: #444;
        }
    </style>
""", unsafe_allow_html=True)

# --------------------------
# Sidebar
# --------------------------
st.sidebar.title("Filtrar")
pagina = st.sidebar.radio("Escolha uma opção:", [
    "✨ Aniversariante do dia",
    "🎊 Próximos aniversariantes",
    "🎂 Aniversariantes do mês",
    "📋 Lista Completa",
])

# --------------------------
# Página: Aniversariante do dia
# --------------------------
if pagina == "✨ Aniversariante do dia":
    aniversariantes_hoje = df[
        (df["DATA NASCIMENTO"].dt.day == hoje.day) & 
        (df["DATA NASCIMENTO"].dt.month == hoje.month)
    ]
    st.title("✨ Aniversariante(s) de hoje")

    if aniversariantes_hoje.empty:
        st.info("Nenhum aniversariante hoje.")
    else:
        for _, row in aniversariantes_hoje.iterrows():
            st.markdown(f"""
                <div class="card">
                    <img src="{row['AVATAR']}" />
                    <div class="nome">{row['NOME']}</div>
                    <div class="data-aniversario">🎂 {row['DATA NASCIMENTO'].strftime('%d/%m')}</div>
                </div>
            """, unsafe_allow_html=True)

# --------------------------
# Página: Próximos aniversariantes
# --------------------------
elif pagina == "🎊 Próximos aniversariantes":
    df["PROXIMO_ANIVERSARIO"] = df["DATA NASCIMENTO"].apply(
        lambda x: x.replace(year=hoje.year) if x.replace(year=hoje.year) >= hoje 
        else x.replace(year=hoje.year+1)
    )
    proximos = df.sort_values("PROXIMO_ANIVERSARIO").head(6)

    st.title("🎊 Próximos aniversariantes")

    for i in range(0, len(proximos), 3):
        cols = st.columns(3)
        for idx, (_, row) in enumerate(proximos.iloc[i:i+3].iterrows()):
            with cols[idx]:
                st.markdown(f"""
                    <div class="card">
                        <img src="{row['AVATAR']}" />
                        <div class="nome">{row['NOME']}</div>
                        <div class="data-aniversario">🎂 {row['DATA NASCIMENTO'].strftime('%d/%m')}</div>
                    </div>
                """, unsafe_allow_html=True)

# --------------------------
# Página: Aniversariantes do mês
# --------------------------
elif pagina == "🎂 Aniversariantes do mês":
    mes_atual = hoje.month
    aniversariantes_mes = df[df["DATA NASCIMENTO"].dt.month == mes_atual]

    mes_nome_en = hoje.strftime("%B")
    mes_nome_pt = MESES_PT[mes_nome_en]

    st.title(f"🎂 Aniversariantes de {mes_nome_pt}")

    if aniversariantes_mes.empty:
        st.info("Não há aniversariantes neste mês.")
    else:
        for i in range(0, len(aniversariantes_mes), 3):
            cols = st.columns(3)
            for idx, (_, row) in enumerate(aniversariantes_mes.iloc[i:i+3].iterrows()):
                with cols[idx]:
                    st.markdown(f"""
                        <div class="card">
                            <img src="{row['AVATAR']}" />
                            <div class="nome">{row['NOME']}</div>
                            <div class="data-aniversario">🎂 {row['DATA NASCIMENTO'].strftime('%d/%m')}</div>
                        </div>
                    """, unsafe_allow_html=True)

# --------------------------
# Página: Lista completa
# --------------------------
elif pagina == "📋 Lista Completa":
    st.title("📋 Lista completa de aniversariantes")

    for _, row in df.sort_values("DATA NASCIMENTO").iterrows():
        aniversario = row["DATA NASCIMENTO"].strftime("%d/%m")
        st.markdown(f"""
            <div class="linha">
                <img src="{row['AVATAR']}" width="110" height="85" />
                <div class="nome-linha">{row['NOME']}</div>
                <div class="data-linha">🎂 {aniversario}</div>
            </div>
        """, unsafe_allow_html=True)
