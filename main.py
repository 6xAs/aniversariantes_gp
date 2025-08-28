import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import locale
locale.setlocale(locale.LC_TIME, "pt_BR.utf8")


st.set_page_config(page_title="Aniversariantes do GP", page_icon="🎉", layout="wide")

# Gerar avatar com base no nome da pessoa
def gerar_avatar(nome):
    return f"https://api.dicebear.com/7.x/adventurer/svg?seed={nome}"
    
# Carregar dados (sem cache para sempre recarregar)
def carregar_dados():
    df = pd.read_csv("database/membros_gp_fakes.csv", sep=',', encoding='utf-8')
    df["DATA NASCIMENTO"] = pd.to_datetime(df["DATA NASCIMENTO"], errors="coerce")
    df["AVATAR"] = df["NOME"].apply(gerar_avatar)
    df = df.dropna(how='all')
    return df

df = carregar_dados()
hoje = datetime.today()

# Cálculo do próximo aniversário
df["PRÓXIMO ANIVERSÁRIO"] = df["DATA NASCIMENTO"].apply(
    lambda d: d.replace(year=hoje.year) if pd.notnull(d) else pd.NaT
)
df["PRÓXIMO ANIVERSÁRIO"] = df["PRÓXIMO ANIVERSÁRIO"].apply(
    lambda d: d + timedelta(days=365) if pd.notnull(d) and d < hoje else d
)

df_ordenado = df.sort_values("PRÓXIMO ANIVERSÁRIO")

# 🔔 Notificação automática ao abrir, se houver aniversariante hoje
hoje_str = hoje.strftime('%d-%m')
aniversariantes_hoje = df[df['PRÓXIMO ANIVERSÁRIO'].dt.strftime('%d-%m') == hoje_str]

if not aniversariantes_hoje.empty:
    nomes = ", ".join(aniversariantes_hoje['NOME'])
    st.toast(f"🎉 Hoje é aniversário de {nomes}!", icon="🎂")

# Sidebar
st.sidebar.title("Filtrar")
pagina = st.sidebar.radio("Escolha uma opção:", [
    "✨ Aniversariante do dia",
    "🎊 Próximos aniversariantes",
    "🎂 Aniversariantes do mês",
    "📋 Lista Completa",
])

# CSS 
st.markdown(
    """
    <style>
    .card {
        background: #262730;
        padding: 10px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 30px;
        transition: transform 0.2s ease-in-out;
    }
    .card:hover {
        transform: scale(1.05);
        box-shadow: 0 8px 12px rgba(0,0,0,0.15);
    }
    .nome {
        font-weight: 700;
        font-size: 22px;
        margin-top: 12px;
        color: #FAFAFA;
    }
    .data-aniversario {
        font-size: 18px;
        color: #e67e22;
        margin-top: 8px;
    }
    .linha {
        display: flex;
        align-items: center;
        background: #262730;
        border-radius: 10px;
        padding: 12px 15px;
        margin-bottom: 10px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    }
    .avatar-pequeno {
        border-radius: 15px;
        margin-right: 10px;
    }
    .nome-linha {
        font-weight: 600;
        font-size: 18px;
        flex: 1;
        color: #FAFAFA;
    }
    .data-linha {
        font-size: 20px;
        color: #d35400;
        min-width: 120px;
        text-align: right;
    }
    </style>
    """, unsafe_allow_html=True
)

# Página: Próximos aniversariantes
if pagina == "🎊 Próximos aniversariantes":
    st.title("🎉 Aniversariantes mais próximos")
    proximos = df_ordenado.head(3)
    card_cols = st.columns(3)
    for idx, (_, row) in enumerate(proximos.iterrows()):
        with card_cols[idx]:
            st.markdown(
                f"""
                <div class="card">
                    <img src="{row['AVATAR']}" border-radius: 10px; margin-right: 15px; 
                         border: 3px solid #000000; background-color: #ffffff; width="170" 
                         style="border-radius: 22%;" />
                    <div class="nome">{row['NOME']}</div>
                    <div class="data-aniversario">🎂 {row['PRÓXIMO ANIVERSÁRIO'].strftime('%d/%m')}</div>
                </div>
                """, unsafe_allow_html=True
            )

# Página: Aniversariantes do mês
elif pagina == "🎂 Aniversariantes do mês":
    mes_atual = hoje.month
    aniversariantes_mes = df[df["DATA NASCIMENTO"].dt.month == mes_atual]

    st.title(f"🎂 Aniversariantes de {hoje.strftime('%B').capitalize()}")

    if aniversariantes_mes.empty:
        st.info("Não há aniversariantes neste mês.")
    else:
        for i in range(0, len(aniversariantes_mes), 3):
            cols = st.columns(3)
            for idx, (_, row) in enumerate(aniversariantes_mes.iloc[i:i+3].iterrows()):
                with cols[idx]:
                    st.markdown(
                        f"""
                        <div class="card">
                            <img src="{row['AVATAR']}" border-radius: 10px; margin-right: 15px; 
                                 border: 3px solid #000000; background-color: #ffffff; width="170" 
                                 style="border-radius: 22%;" />
                            <div class="nome">{row['NOME']}</div>
                            <div class="data-aniversario">🎂 {row['DATA NASCIMENTO'].strftime('%d/%m')}</div>
                        </div>
                        """, unsafe_allow_html=True
                    )

# Página: Lista completa
elif pagina == "📋 Lista Completa":
    st.title("Lista completa de Aniversariantes do GP")
    for _, row in df.iterrows():
        aniversario = row["DATA NASCIMENTO"].strftime("%d/%m/%Y") if pd.notnull(row["DATA NASCIMENTO"]) else "Data inválida"
        st.markdown(
            f"""
            <div class="linha">
                <img class="avatar-pequeno" src="{row['AVATAR']}" width="110" height="85" />
                <div class="nome-linha">{row['NOME']}</div>
                <div class="data-linha">🎂 {aniversario}</div>
            </div>
            """, unsafe_allow_html=True
        )

# Página de aniversariante do dia
elif pagina == "✨ Aniversariante do dia":
    if not aniversariantes_hoje.empty:
        st.title("🎉 FELIZ ANIVERSÁRIO!")
        st.balloons()
        if "mostrar_audio" not in st.session_state:
            st.session_state.mostrar_audio = False
        # Botão toggle
        if st.button("Tocar música"):
            st.session_state.mostrar_audio = not st.session_state.mostrar_audio

        # Exibir player se for verdadeiro
        if st.session_state.mostrar_audio:
            st.audio("Aniversario.mp3")

        if len(aniversariantes_hoje) == 1:
            row = aniversariantes_hoje.iloc[0]
            st.markdown(
                f"""
                <div style="display: flex; flex-direction: column; align-items: center; margin-top: 20px;">
                    <img src="{row['AVATAR']}" width="300" style="border-radius: 45%; border: 5px solid #daa520;" />
                    <h2 style="margin-top: 10px; color: #daa520;">{row['NOME']}</h2>
                    <p style="font-size: 18px;">🎂 {row['PRÓXIMO ANIVERSÁRIO'].strftime('%d/%m')}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            card_cols = st.columns(len(aniversariantes_hoje))
            for idx, (_, row) in enumerate(aniversariantes_hoje.iterrows()):
                with card_cols[idx]:
                    st.markdown(
                        f"""
                        <div style="text-align: center; margin-top: 10px;">
                            <img src="{row['AVATAR']}" width="190" style="border-radius: 50%; border: 4px solid #DAA520;" />
                            <div style="margin-top: 8px; font-size: 20px; color: #DAA520;"><strong>{row['NOME']}</strong></div>
                            <div style="font-size: 16px;">🎂 {row['PRÓXIMO ANIVERSÁRIO'].strftime('%d/%m')}</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
        # Formulário de felicitações
        st.subheader("💬 Envie sua mensagem de felicitações!")
        with st.form("form_felicitacoes"):
            mensagem = st.text_area("Digite sua mensagem de felicitações:")
            nome = st.text_input("Seu nome (opcional)")
            enviar = st.form_submit_button("Enviar 🎉")

        if enviar:
            if mensagem.strip():
                st.success("Mensagem enviada com sucesso! 🎈")
                st.write("📝 Sua mensagem:")
                st.write(f"💬 {mensagem}")
                if nome.strip():
                    st.write(f"👤 De: {nome}")
            else:
                st.warning("Por favor, digite uma mensagem antes de enviar.")
    else:
        st.markdown(
            """
            <div style="text-align: center; margin-top: 50px;">
                <h2>😢 Nenhum aniversariante hoje</h2>
                <p>Aguardamos o próximo para celebrar!</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        # Mostrar contador para o próximo aniversário
        df["aniversario_ano_atual"] = df["DATA NASCIMENTO"].apply(lambda x: x.replace(year=hoje.year))
        df["dias_para_aniversario"] = (df["aniversario_ano_atual"] - hoje).dt.days
        df["dias_para_aniversario"] = df["dias_para_aniversario"].apply(lambda x: x if x >= 0 else x + 365)

        # Filtra todos os aniversariantes com a menor quantidade de dias
        proximos = df[df["dias_para_aniversario"] == df["dias_para_aniversario"].min()]
        dias = int(proximos["dias_para_aniversario"].iloc[0])
        nomes = ", ".join(proximos["NOME"])
        data = proximos["DATA NASCIMENTO"].iloc[0].strftime('%d/%m')

        st.markdown("---")
        st.markdown(
            """
            <div style="text-align: center;">
               <h3>⏳ Contador para o próximo aniversário</h3>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div style="text-align: center; font-size: 18px; margin-top: 10px;">
            🎂 <strong>Faltam {dias} dias</strong> para o aniversário de {nomes}</strong>! No dia <strong>{data}</strong>.
         </div>
          """,
           unsafe_allow_html=True
        )
