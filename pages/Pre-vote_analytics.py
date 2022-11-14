import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

chart_colors = ["#bd7ebe", "#b2e061", "#7eb0d5", "#fd7f6f", "#ffb55a", "#ffee65", "#beb9db",
                "#fdcce5", "#8bd3c7"]

st.title("Análise Demográfica")

## Buscando os dois Datasets

election_ids=pd.read_csv("election_ids.csv")
regions=pd.read_csv("region_dataset.csv")

## Análise por rede
voters_regions = pd.merge(election_ids, regions, left_on='region', right_on='microregion')
macroreg = pd.DataFrame(voters_regions['macroregion'].value_counts())
macroreg = macroreg.reset_index()
macroreg.columns = ['region', 'count']

fig, ax = plt.subplots()

chart_colors_network = ["#bd7ebe", "#b2e061", "#7eb0d5"]
ax.bar(macroreg['region'], macroreg['count'], color=chart_colors_network)
ax.set_title("Votos aptos por Rede")

st.pyplot(fig)

## Análise por Grupo
mesoreg = pd.DataFrame(voters_regions['mesoregion'].value_counts())
mesoreg = mesoreg.reset_index()
mesoreg.columns = ['region', 'count']

fig2, ax2 = plt.subplots()

chart_colors_group = ["#bd7ebe", "#7eb0d5", "#b2e061", "#fd7f6f"]
ax2.bar(mesoreg['region'], mesoreg['count'], color=chart_colors_group)
ax2.set_title("Votos aptos por Grupo Eleitoral")

st.pyplot(fig2)

## Análise por pote
option = st.selectbox("Dados de pote por Grupo Eleitoral", macroreg['region'])

microreg = voters_regions.loc[voters_regions['macroregion'] == option]
microreg = pd.DataFrame(microreg['region'].value_counts())
microreg = microreg.reset_index()
microreg.columns = ['region', 'count']

fig4, ax4 = plt.subplots()
ax4.pie(microreg['count'], labels=microreg['region'] ,autopct='%1.1f%%', colors=chart_colors)

st.pyplot(fig4)

fig3, ax3 = plt.subplots()
ax3.bar(microreg['region'], microreg['count'], color=chart_colors)
ax3.set_title("Votos aptos por pote")

st.pyplot(fig3)