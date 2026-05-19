cat << 'EOF' > app.py
import streamlit as st
import pandas as pd

st.set_page_config(page_title="ScaleAds Premium", page_icon="📈", layout="centered")

# CSS para customizar as fontes, remover o menu padrão do Streamlit e ajeitar a impressão do PDF
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    @media print {
        header, [data-testid="stSidebar"], button, .stButton, [data-testid="stHeader"] {
            display: none !important;
        }
        .main .block-container {
            padding-top: 0rem !important;
            padding-bottom: 0rem !important;
        }
    }
    </style>
""", unsafe_allow_html=True)

st.title("📈 ScaleAds - Dashboard Pro")
st.subheader("Simulador de Escala e Viabilidade de Campanha")

st.markdown("---")

st.sidebar.header("⚙️ Customizar Relatório")
nome_empresa = st.sidebar.text_input("Sua Marca / Agência", value="Minha Agência Digital")
nome_cliente = st.sidebar.text_input("Nome do Cliente / Projeto", value="Cliente Potencial")
st.sidebar.write("---")
st.sidebar.caption("Configurações do SaaS v1.4")

# Seção 1: Dados de Tráfego
st.write("### 📊 1. Configuração de Mídia (Tráfego):")
col_in1, col_in2, col_in3 = st.columns(3)

with col_in1:
    investimento = st.number_input("Orçamento Total (R$)", min_value=0.0, value=2500.0, step=100.0)
with col_in2:
    cpm = st.number_input("CPM Esperado (R$)", min_value=0.1, value=10.0, step=1.0)
with col_in3:
    ctr = st.number_input("CTR Alvo (%)", min_value=0.01, value=2.5, step=0.1)

# Seção 2: Dados de Conversão e Produto
st.write("### 🛍️ 2. Economia do Produto & Funil:")
col_in4, col_in5, col_in6 = st.columns(3)

with col_in4:
    preco_produto = st.number_input("Preço do Produto (R$)", min_value=0.0, value=150.0, step=10.0)
with col_in5:
    taxa_conversao = st.number_input("Conversão de Página (%)", min_value=0.01, value=1.5, step=0.5)
with col_in6:
    taxa_gateway = st.number_input("Custos de Gateway/Imposto (%)", min_value=0.0, value=5.0, step=0.5)

st.markdown("---")

if "calculado" not in st.session_state:
    st.session_state.calculado = False

if st.button("🔥 Rodar Simulação Estratégica"):
    st.session_state.calculado = True

if st.session_state.calculado:
    # Cálculos de Tráfego
    impressoes = (investimento / cpm) * 1000
    cliques = impressoes * (ctr / 100)
    cpc = investimento / cliques if cliques > 0 else 0.0
    
    # Cálculos de Vendas e Faturamento descontando o Gateway
    vendas = cliques * (taxa_conversao / 100)
    faturamento_bruto = vendas * preco_produto
    custos_gateway = faturamento_bruto * (taxa_gateway / 100)
    faturamento_liquido = faturamento_bruto - custos_gateway
    
    lucro = faturamento_liquido - investimento
    roi = (lucro / investimento) if investimento > 0 else 0.0
    
    # Cabeçalho Comercial que aparece após o cálculo (Perfeito para o PDF)
    with st.container():
        st.write(f"### 📄 Proposta Comercial Gerada por: **{nome_empresa}**")
        st.write(f"**Focado em:** {nome_cliente}")
        st.caption("Métricas estimadas baseadas no comportamento atual do mercado.")
    
    st.markdown("---")
    
    # Exibição - Bloco 1: Tráfego
    st.write("#### 🎯 Métricas de Atração (Anúncios):")
    col1, col2, col3 = st.columns(3)
    col1.metric("👥 Impressões", f"{impressoes:,.0f}".replace(",", "."))
    col2.metric("🎯 Cliques Gerados", f"{cliques:,.0f}".replace(",", "."))
    col3.metric("💰 CPC Máximo", f"R$ {cpc:.2f}")
    
    st.markdown("---")
    
    # Exibição - Bloco 2: Negócio (Vendas e Lucro)
    st.write("#### 💸 Métricas de Conversão & ROI:")
    col4, col5, col6 = st.columns(3)
    col4.metric("🛒 Conversões (Vendas)", f"{vendas:,.0f}".replace(",", "."))
    col5.metric("💵 Faturamento Líquido", f"R$ {faturamento_liquido:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
    
    if lucro >= 0:
        col6.metric("✅ Lucro Estimado", f"R$ {lucro:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        st.success(f"🚀 **Retorno de {roi:.2f}x (ROI):** Operação validada e altamente escalável para o cliente!")
    else:
        col6.metric("❌ Margem Negativa", f"R$ {lucro:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."), delta_color="inverse")
        st.error(f"⚠️ **Alerta de Inviabilidade:** Operação operando no vermelho com este orçamento. É preciso otimizar as taxas.")

    st.markdown("---")

    # Seção 3: Geração do Gráfico de Escala
    st.write("#### 📈 Rampa de Escala (Cenários de Lucro Líquido)")
    
valores_simulados = [investimento * f for f in [0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0]]
dados_grafico = []

for inv_simulado in valores_simulados:

        if inv_simulado == 0: continue
        imp_s = (inv_simulado / cpm) * 1000
        cli_s = imp_s * (ctr / 100)
        ven_s = cli_s * (taxa_conversao / 100)
        fat_b_s = ven_s * preco_produto
        fat_l_s = fat_b_s * (1 - (taxa_gateway / 100))
        luc_s = fat_l_s - inv_simulado
        
        dados_grafico.append({
            "Investimento (R$)": round(inv_simulado, 2),
            "Lucro Real (R$)": round(luc_s, 2)
        })
    
    df = pd.DataFrame(dados_grafico)
    st.line_chart(df.set_index("Investimento (R$)"))

    st.markdown("---")
    
    # Botão de Exportação de PDF
    st.write("#### 🖨️ Ações de Fechamento:")
    st.components.v1.html("""
        <button onclick="window.print()" style="
            background-color: #0066cc;
            color: white;
            border: none;
            padding: 14px 28px;
            font-size: 16px;
            font-weight: bold;
            border-radius: 8px;
            cursor: pointer;
            width: 100%;
            box-shadow: 0px 4px 6px rgba(0,0,0,0.1);
        ">
            📥 Gerar PDF do Relatório Comercial
        </button>
    """, height=60)

EOF

