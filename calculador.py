import streamlit as st
import pandas as pd
#import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Configuração da página
st.set_page_config(
    page_title="Calculadora de Juros Compostos",
    page_icon="📊",
    layout="centered"
)

# Título e descrição
st.title("📊 Calculadora de Juros Compostos")
st.markdown("""
Saiba quanto sua aplicação pode render de forma simples utilizando juros compostos.
**Juros compostos** são os juros calculados sobre o valor inicial e também sobre os juros acumulados anteriormente.
""")

# Divisão em colunas para melhor organização
col1, col2 = st.columns([2, 1])

with col1:
    # Entrada de dados com melhorias de UX
    st.subheader("Dados da Aplicação")
    
    # Usando expansores para organizar as entradas
    with st.expander("Valores", expanded=True):
        D = st.number_input(
            "Valor Inicial (R$)", 
            min_value=0.0, 
            value=1000.0, 
            step=100.0,
            format='%.2f',
            help="Valor inicial do investimento"
        )
        
        I = st.number_input(
            "Taxa de Juros Mensal (%)", 
            min_value=0.0, 
            value=5.0, 
            step=0.5,
            format='%.2f',
            help="Taxa de juros mensal em percentual"
        )
        
        T = st.number_input(
            "Período (meses)", 
            min_value=1, 
            value=12, 
            step=1,
            help="Tempo total da aplicação em meses"
        )
    
    # Informações adicionais
    with st.expander("Sobre a taxa de juros", expanded=False):
        st.info("""
        Lembre-se:
        - Taxa de poupança: ~0,5% ao mês
        - CDB: 0,8% a 1,2% ao mês
        - Tesouro Direto: 0,6% a 1,0% ao mês
        - Ações: variável (podendo ser negativa)
        """)

with col2:
    # Card de resultado
    st.subheader("Resultado")
    
    # Cálculo do montante
    if I > 0 and T > 0:
        I_decimal = I / 100  # Convertendo para decimal
        C = D * (1 + I_decimal) ** T
        juros = C - D
        
        st.metric("Valor Inicial", f"R$ {D:,.2f}".replace(',', '.'))
        st.metric("Total de Juros", f"R$ {juros:,.2f}".replace(',', '.'))
        st.metric("Montante Final", f"R$ {C:,.2f}".replace(',', '.'), 
                 delta=f"{I}% ao mês")
    else:
        st.warning("Informe valores positivos para taxa e período")

# Botão de calcular
if st.button("Calcular Projeção", type="primary"):
    if I <= 0 or T <= 0 or D <= 0:
        st.error("Por favor, insira valores válidos (maiores que zero).")
    else:
        # Cálculo da projeção mês a mês
        I_decimal = I / 100
        meses = []
        valores = []
        juros_acumulados = []
        
        for mes in range(T + 1):
            valor_mes = D * (1 + I_decimal) ** mes
            meses.append(mes)
            valores.append(valor_mes)
            juros_acumulados.append(valor_mes - D)
        
        # Criando DataFrame para exibição
        df = pd.DataFrame({
            'Mês': meses,
            'Valor': valores,
            'Juros Acumulados': juros_acumulados
        })
        
        # Formatando valores para exibição
        df_display = df.copy()
        df_display['Valor'] = df_display['Valor'].apply(lambda x: f'R$ {x:,.2f}'.replace(',', '.'))
        df_display['Juros Acumulados'] = df_display['Juros Acumulados'].apply(lambda x: f'R$ {x:,.2f}'.replace(',', '.'))
        
        # Exibindo tabela
        st.subheader("Projeção Mês a Mês")
        st.dataframe(df_display, hide_index=True, use_container_width=True)
        
        # Gráfico de projeção
        st.subheader("Evolução do Investimento")
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=df['Mês'], 
            y=df['Valor'],
            mode='lines+markers',
            name='Montante',
            line=dict(color='#4CAF50', width=3),
            marker=dict(size=6)
        ))
        
        fig.add_trace(go.Scatter(
            x=df['Mês'], 
            y=df['Juros Acumulados'],
            mode='lines',
            name='Juros Acumulados',
            line=dict(color='#FF9800', width=2, dash='dot'),
            fill='tozeroy',
            opacity=0.3
        ))
        
        fig.update_layout(
            xaxis_title="Meses",
            yaxis_title="Valor (R$)",
            hovermode="x unified",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            plot_bgcolor='rgba(0,0,0,0.05)'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Gráfico de composição
        st.subheader("Composição do Montante Final")
        
        fig_pie = px.pie(
            values=[D, juros],
            names=['Valor Principal', 'Juros'],
            color=['Valor Principal', 'Juros'],
            color_discrete_map={'Valor Principal':'lightblue', 'Juros':'orange'}
        )
        
        fig_pie.update_traces(textposition='inside', textinfo='percent+label+value')
        st.plotly_chart(fig_pie, use_container_width=True)

# Informações adicionais
st.divider()
st.subheader("💡 Sobre Juros Compostos")
st.markdown("""
Os juros compostos são considerados a **oitava maravilha do mundo** (segundo Albert Einstein) 
porque permitem que seu dinheiro cresça exponencialmente com o tempo.

**Fórmula utilizada:**  
`M = P × (1 + i)ⁿ`  
Onde:
- `M` = Montante final
- `P` = Principal (valor inicial)
- `i` = Taxa de juros (em decimal)
- `n` = Período de tempo

Quanto antes você começar a investir, mais você se beneficia do poder dos juros compostos!
""")

# Rodapé
st.divider()
st.caption("""
⚠️ Esta calculadora fornece apenas uma simulação teórica. 
Resultados reais podem variar de acordo com condições de mercado e tributações.
""")
