### Bibliotecas ###
import time
import flask
import pandas as pd
import json
from urllib.request import urlopen
import plotly.express as px
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
# from dash.dash_table.Format import Group
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
# from flask_caching import Cache
# import ssl
# import socket
# import os
# import sys
# import _bz2
# from _bz2 import BZ2Compressor, BZ2Decompressor
# from OpenSSL import SSL

TIMEOUT = 60

### App ###
server = flask.Flask(__name__)
app = dash.Dash(__name__, server=server, meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1.0'}])
### fim App ###


### Datas a serem atualizadas ###
texto_atualizacao_voc ='Atualizado em 11/03/2024'
texto_atualizacao_omicron ='Atualizado em 25/04/2023'
texto_3card = 'Fev 2024'
### fim Datas a serem atualizadas ###


### Carregar datasets ###
df_genomasLaboratorio = pd.read_csv('script-dashboard/dfGenomasLaboratorio_PT.csv')
df_linMes = pd.read_csv('script-dashboard/dfLinhagensMes_PT.csv')
df_variantes = pd.read_csv('script-dashboard/dfVariantes_PT.csv')
df_linhagens = pd.read_csv('script-dashboard/dfLinhagens_PT.csv')
df_mapa = pd.read_csv('script-dashboard/dfMapa_PT.csv')
### fim Carregar datasets ###


## Cards ###
## Card 1 - total de genomas sequenciados
total_genomas = df_genomasLaboratorio['Quantidade'].sum()
## Card 2 - total de genomas por 100k casos confirmados
confirmados_100k = df_mapa['Casos'].sum()/100000
genomas_100kcasos = total_genomas/confirmados_100k
## Card 3
# lista com os nomes das variantes
top_lin_names = [df_linMes.Linhagem[0], df_linMes.Linhagem[1], df_linMes.Linhagem[2]]
# lista com as frequências
top_lin_freq = [df_linMes.Frequencia[0], df_linMes.Frequencia[1], df_linMes.Frequencia[2]]
# lista com as porcentagem
top_lin_porc = [df_linMes.Porcentagem[0], df_linMes.Porcentagem[1], df_linMes.Porcentagem[2]]
### fim Cards ###


### Tabelas para o dashboard ###
# Tabela
tabela_dash_linhagens = df_linhagens.groupby(['Data', 'Período', 'Região', 'Estado', 'Laboratório', 'Linhagens relevantes']).sum().reset_index()
tabela_dash_linhagens = tabela_dash_linhagens.sort_values(['Data', 'Região', 'Estado', 'Laboratório', 'Linhagens relevantes'], \
                                                          ascending=[False, True, True, True, True]).drop('Data', axis=1)
### fim Tabelas para o dashboard ###


### Estilos dos textos ###
# estilo html.H2 - título principal
h1_style={'color':'#0d2a63',
          'fontSize':50,
          'font-family':'sans-serif',
          'textAlign':'center',
          'font-weight':'bold'}
# estilo html.H6 - subtítulo do título principal
h6_style={'color':'#0d2a63',
          'fontSize':18,
          'font-family':'sans-serif',
          'textAlign':'center'}
# Cards 1, 2 e 3 - estilo do título
card_style_title={'color':'#0d2a63', 
                  'fontSize':18, 
                  'font-family':'sans-serif', 
                  'textAlign':'center'}
# Card 1 e 2 - estilo do corpo
card_style_body={'color':'#0d2a63', 
                 'fontSize':60, 
                 'font-family':'sans-serif', 
                 'textAlign':'center', 
                 'font-weight':'bold'}
# Card 3 - estilo do corpo
third_card_style={'color':'#0d2a63', 
                  'fontSize':15, 
                  'font-family':'sans-serif', 
                  'textAlign':'center', 
                  'font-weight':'bold'}
# estilo do texto abaixo dos cards
texto_style = {'color':'#0d2a63', 
               'fontSize':14, 
               'font-family':'sans-serif', 
               'textAlign':'justify'}
# estilo html.H2 - título dos gráficos
h2_style={'color':'#0d2a63', 
           'fontSize':34, 
           'font-family':'sans-serif',
           'textAlign':'center', 
           'font-weight':'bold'}
# estilo html.H5 - Selecione a região e Tabela de dados
h5_style={'color':'#0d2a63', 
          'fontSize':16, 
          'font-family':'sans-serif', 
          'font-weight':'bold'}
# estilo html.H6 - GISAID e BRASIL.IO - final do dashboard
h6_style2={'color':'#0d2a63', 
           'fontSize':14, 
           'font-family':'sans-serif', 
           'textAlign':'left',
           'font-weight':'bold'}
# estilo das tabelas
style_table={'height':170, 'width':'100%'}
style_cell={'textAlign':'left', 'fontSize':14, 'font-family':'sans-serif'}
style_header={'backgroundColor':'#0d2a63', 'fontWeight':'bold',
              'color':'white', 'fontSize':14, 'font-family':'sans-serif'}
### fim Estilos dos textos ###

### Cores e layout dos gráficos ###
# VOC/VOI
# XBB.1.5.70 + GK.* 
# XBB.1.5.*
# FE.1.* 
# HA.1.* 
# EG.5.*
# JD.1.*
# JN.1
colors_variantes = {
        'HA.1.* (Omicron)': '#dc3912', 
        'JD.1.* (Omicron)': '#66aa00',
        'JN.1.*+BA.2.86.* (Omicron)': '#1c8356',
        'EG.5.* (Omicron)': '#fecb52',
        'XBB.1.5.* (Omicron)': '#e377c2',
        'XBB.1.5.70.*+GK.* (Omicron)': '#fc1cbf',
        'FE.1.* (Omicron)': '#1f77b4',
        'Outras': '#999999'}
orders_variantes = {'Variantes relevantes': ['Outras',
                                             'EG.5.* (Omicron)',
                                             'FE.1.* (Omicron)',
                                             'HA.1.* (Omicron)',
                                             'JD.1.* (Omicron)',
                                             'JN.1.*+BA.2.86.* (Omicron)',
                                             'XBB.1.5.* (Omicron)',
                                             'XBB.1.5.70+GK.* (Omicron)']}  

# Linhagens
colors_linhagens = {'B.1.617.2+AY.* (Delta)': '#750d86',
                    'B.1.1': '#fc6955', 
                    'B.1.1.28': '#e48f72', 
                    'B.1.1.33': '#f8a19f', 
                    'B.1.1.7 (Alfa)': '#b82e2e', 
                    'P.1.* (Gama)': '#109618',     
                    'P.2': '#862a16',
                    'BA.1.* (Omicron)': '#6c4516', 
                    'BA.2.* (Omicron)': '#b68e00',
                    'BA.4.* (Omicron)': '#feaf16',
                    'BA.5.* (Omicron)': '#fbe426',
                    'XBB.1.5.70.*+GK.* (Omicron)': '#fc1cbf',
                    'XBB.* (Omicron)': '#e377c2',
                    'Outras': '#999999',     
                    'FE.1.* (Omicron)': '#1f77b4',
                    'JD.1.* (Omicron)': '#66aa00',
                    'JN.1.*+BA.2.86.* (Omicron)': '#1c8356'}          
orders_linhagens = {'Linhagens relevantes': ['Outras',
                                             'B.1.1', 'B.1.1.28', 'B.1.1.33',                                             
                                             'P.2',  'B.1.1.7 (Alfa)', 
                                             'P.1.* (Gama)', 'B.1.617.2+AY.* (Delta)',  
                                             'BA.1.* (Omicron)', 'BA.2.* (Omicron)', 
                                             'BA.4.* (Omicron)', 'BA.5.* (Omicron)',
                                             'FE.1.* (Omicron)',
                                             'JD.1.* (Omicron)',
                                             'JN.1.*+BA.2.86.* (Omicron)',
                                             'XBB.* (Omicron)', 
                                             'XBB.1.5.70.*+GK.* (Omicron)']}                

# Genomas/Laboratório
colors_lab = {'Outros': '#17becf', 
              'FIOCRUZ': '#e45756'}
orders_lab = {'Laboratório': ['Outros', 'FIOCRUZ']}
# layout
layout_barplot = {'xaxis_title': '<b>Período de amostragem</b>', 
                  'yaxis_title': '<b>Genomas depositados</b>', 
                  'xaxis_title_font_size': 16, 
                  'yaxis_title_font_size': 16,
                  'title_x': 0.5, 
                  'title_font_size': 22, 
                  'title_font_family': 'sans-serif', 
                  'legend_font_size': 13, 
                  'plot_bgcolor': 'white', 
                  'paper_bgcolor': 'white'}
layout_area = {'xaxis_title': '<b>Período de amostragem</b>',
               'yaxis_title': '<b>Frequência (%)</b>', 
               'xaxis_title_font_size': 16, 
               'yaxis_title_font_size': 16,
               'title_x': 0.5, 
               'title_font_size': 22, 
               'title_font_family': 'sans-serif',
               'legend_font_size': 13, 
               'legend_title_font_size': 12}
legend={'orientation': 'h', 
        'xanchor': 'center', 
        'yanchor': 'bottom', 
        'x': 0.5, 'y': 1.0}
### fim Cores e layout gráficos ###


### Dropdowns ###
regiao_dropdown = [{"label": "Brasil", "value": "Brasil"},
                   {"label": "Norte", "value": "Norte"},
                   {"label": "Nordeste", "value": "Nordeste"},
                   {"label": "Sul", "value": "Sul"},
                   {"label": "Sudeste", "value": "Sudeste"},
                   {"label": "Centro-oeste", "value": "Centro-oeste"}]
estado_dropdown = [{"label": "Acre", "value": "Acre"},
                   {"label": "Alagoas", "value": "Alagoas"},
                   {"label": "Amapá", "value": "Amapá"},
                   {"label": "Amazonas", "value": "Amazonas"},
                   {"label": "Bahia", "value": "Bahia"},
                   {"label": "Ceará", "value": "Ceará"},
                   {"label": "Distrito Federal", "value": "Distrito Federal"},
                   {"label": "Espírito Santo", "value": "Espírito Santo"},
                   {"label": "Goiás", "value": "Goiás"},
                   {"label": "Maranhão", "value": "Maranhão"},
                   {"label": "Mato Grosso", "value": "Mato Grosso"},
                   {"label": "Mato Grosso do Sul", "value": "Mato Grosso do Sul"},
                   {"label": "Minas Gerais", "value": "Minas Gerais"},
                   {"label": "Pará", "value": "Pará"},
                   {"label": "Paraíba", "value": "Paraíba"},
                   {"label": "Paraná", "value": "Paraná"},
                   {"label": "Pernambuco", "value": "Pernambuco"},
                   {"label": "Piauí", "value": "Piauí"},
                   {"label": "Rio de Janeiro", "value": "Rio de Janeiro"},
                   {"label": "Rio Grande do Norte", "value": "Rio Grande do Norte"},
                   {"label": "Rio Grande do Sul", "value": "Rio Grande do Sul"},
                   {"label": "Rondônia", "value": "Rondônia"},
                   {"label": "Roraima", "value": "Roraima"},
                   {"label": "Santa Catarina", "value": "Santa Catarina"},
                   {"label": "São Paulo", "value": "São Paulo"},
                   {"label": "Sergipe", "value": "Sergipe"},
                   {"label": "Tocantins", "value": "Tocantins"}]
### fim Dropdown ###


### Funções ###
# BRASIL
def cria_df_brasil(df, coluna):
  df_br = df.groupby(['Data', 'Período', coluna]).sum().reset_index()
  df_br = df_br.pivot_table(values='Quantidade', index=coluna, 
                            columns=['Data', 'Período'], 
                            fill_value=0, aggfunc='sum')
  df_br.columns = df_br.columns.droplevel()
  df_br = df_br.stack().reset_index().rename(columns={0: 'Quantidade'})
  return df_br
# Função para Regiões
def cria_df_regiao(df, coluna, regiao):
  df_reg = df.query('Região == @regiao').reset_index(drop=True)
  df_reg = df_reg.pivot_table(values='Quantidade', index=coluna, 
                              columns=['Data', 'Período'], 
                              fill_value=0, aggfunc='sum')
  df_reg.columns = df_reg.columns.droplevel()
  df_reg = df_reg.stack().reset_index().rename(columns={0: 'Quantidade'})
  return df_reg
# Função para Estados
def cria_df_estado(df, coluna, estado):
  df_estado = df.query('Estado == @estado').reset_index(drop=True)
  df_estado = df_estado.pivot_table(values='Quantidade', index=coluna, 
                                    columns=['Data', 'Período'],
                                    fill_value=0, aggfunc='sum')
  df_estado.columns = df_estado.columns.droplevel()
  df_estado = df_estado.stack().reset_index().rename(columns={0: 'Quantidade'})
  return df_estado
### fim Funções ###


### Cards ###
first_card = dbc.Card(
                  dbc.CardBody([html.H5('Total de genomas sequenciados', style=card_style_title), 
                               html.P(f'{total_genomas}', style=card_style_body)], 
                               className='card_container four columns'))
second_card = dbc.Card(
                  dbc.CardBody([html.H5('Genomas sequenciados/100 mil casos', style=card_style_title), 
                                html.P(f'{genomas_100kcasos:.1f}', style=card_style_body)], 
                                className='card_container four columns'))
third_card = dbc.Card(
                  dbc.CardBody([html.H5(f'Principais genomas sequenciados¹ em {texto_3card}', style=card_style_title), 
                                html.P(f'{top_lin_names[0]}: {top_lin_freq[0]} genomas ({top_lin_porc[0]}%)', style=third_card_style),
                                html.P(f'{top_lin_names[1]}: {top_lin_freq[1]} genomas ({top_lin_porc[1]}%)', style=third_card_style),
                                html.P(f'{top_lin_names[2]}: {top_lin_freq[2]} genomas ({top_lin_porc[2]}%)', style=third_card_style)]), 
                                className='card_container four columns') 
# salvar cards em uma lista
cards_list = [first_card, second_card, third_card]
### fim Cards ###


### DFs e gráficos Brasil VOC/VOI ###
df_brasil_variantes_barplot = cria_df_brasil(df_variantes, 'Variantes relevantes')
df_brasil_variantes_area = cria_df_brasil(df_variantes, 'Variantes relevantes')
df_brasil_linhagens_barplot = cria_df_brasil(df_linhagens, 'Linhagens relevantes')
df_brasil_linhagens_area = cria_df_brasil(df_linhagens, 'Linhagens relevantes')
## Gráfico 1 - Brasil - Barplot VOC/VOI
row1_bar_BR = px.bar(df_brasil_variantes_barplot,
                     x='Período', y='Quantidade', color='Variantes relevantes',
                     hover_data={'Variantes relevantes': False,
                                 'Período': True,
                                 'Quantidade': True},
                     hover_name='Variantes relevantes',
                     color_discrete_map=colors_variantes, category_orders=orders_variantes,
                     opacity=0.95, title=f'Brasil<br><sup>Variantes relevantes</sup>', height=550)
row1_bar_BR.update_layout(layout_barplot, margin={'l':0, 'r':0, 't':200, 'b':0},
                          legend=legend, legend_title_text=None)
row1_bar_BR.update_xaxes(tickangle=320, tickfont_size=14, showline=True, linewidth=0.5, linecolor='gray')
row1_bar_BR.update_yaxes(showgrid=True, gridcolor='lightgray', showline=True, linewidth=0.5, linecolor='gray')
## Gráfico 2 - Brasil - Area VOC/VOI
row1_area_BR = px.area(df_brasil_variantes_area,
                      x='Período', y='Quantidade', text='Quantidade',
                      color='Variantes relevantes', groupnorm='percent', 
                      title=f'Brasil<br><sup>Variantes relevantes</sup>',
                      color_discrete_map=colors_variantes, category_orders=orders_variantes, 
                      height=550, line_shape='spline')
row1_area_BR.update_layout(layout_area, margin={'l':0, 'r':0, 't':200, 'b':0}, 
                          legend=legend, legend_title_text=None, hovermode='x unified')
row1_area_BR.update_traces(line=dict(width=0), hovertemplate='%{text}' + ' (%{y:.1f}%)', mode='lines')
row1_area_BR.update_xaxes(tickangle=320, showgrid=True, gridcolor='lightgray', tickfont_size=14, showline=True, linewidth=0.5, linecolor='gray')
row1_area_BR.update_yaxes(range=[0,100], showgrid=True, gridcolor='lightgray', showline=True, linewidth=0.5, linecolor='gray')
### fim DFs e gráficos Brasil VOC/VOI###

### Gráficos - Quantidade de genomas sequenciados/Laboratório ###
# Barplot
row3_bar = px.bar(df_genomasLaboratorio,
                  x='Período', y='Quantidade',
                  color='Laboratório',
                  color_discrete_map=colors_lab,
                  category_orders=orders_lab,
                  opacity=0.9, height=470)
row3_bar.update_layout(title='Por mês de coleta', title_x=0.5,
                       title_font_size=20, title_font_family='sans-serif',
                       xaxis_title='<b>Período de amostragem</b>',
                       yaxis_title='<b>Genomas depositados</b>',
                       xaxis_title_font_size=16, yaxis_title_font_size=16,
                       plot_bgcolor='white', paper_bgcolor='white',
                       margin={'l':0, 'r':0, 't':80, 'b':0}, 
                       legend=legend, legend_title_text='Laboratório:')
row3_bar.update_xaxes(nticks=20, tickangle=320, showline=True, linewidth=0.5, linecolor='gray')
row3_bar.update_yaxes(showgrid=True, gridcolor='lightgray', showline=True, linewidth=0.5, linecolor='gray')
# Area - acumulados
row3_area = px.area(df_genomasLaboratorio,
                    x='Período', y='Acumulado',
                    color='Laboratório',
                    color_discrete_map=colors_lab,
                    category_orders=orders_lab,
                    height=470, line_shape='spline')
row3_area.update_layout(title='Valores acumulados', title_x=0.5, 
                        title_font_size=20, title_font_family='sans-serif',
                        xaxis_title='<b>Período de amostragem</b>',
                        yaxis_title='<b>Genomas depositados</b>',
                        xaxis_title_font_size=16, yaxis_title_font_size=16,
                        plot_bgcolor='white', paper_bgcolor='white',
                        margin={'l':0, 'r':0, 't':80, 'b':0}, 
                        legend=legend, legend_title_text='Laboratório:')
row3_area.update_traces(line={'width':0})
row3_area.update_xaxes(nticks=20, tickangle=320, showgrid=True, gridcolor='lightgray', showline=True, linewidth=0.5, linecolor='gray')
row3_area.update_yaxes(showgrid=True, gridcolor='lightgray', showline=True, linewidth=0.5, linecolor='gray')
### fim Gráficos - Quantidade de genomas sequenciados/Laboratório ###

### Gráfico quando nao há dados para a UF ###
grafico_nao_ha_dados = go.Figure() 
grafico_nao_ha_dados.add_annotation(showarrow=False,
                                    text='Não há dados para o estado', 
                                    font={'size':30,
                                          'color':'gray'},
                                    align='center')
grafico_nao_ha_dados.update_layout(height=400,
                                   margin={'l':0, 'r':0, 't':50, 'b':50})
### Gráfico nao há dados suficientes (só 1 mes) para a UF
grafico_nao_ha_suficientes = go.Figure() 
grafico_nao_ha_suficientes.add_annotation(showarrow=False,
                                          text='Não há dados suficientes', 
                                          font={'size':30,
                                                'color':'gray'},
                                          align='center')
grafico_nao_ha_suficientes.update_layout(height=550,
                                         margin={'l':0, 'r':0, 't':200, 'b':100})
### fim Gráfico quando nao há dados para a UF ###


### Mapas ###
# baixar mapa do Brasil
with urlopen('https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson') as response:
   Brazil=json.load(response)
state_id_map = {}
for feature in Brazil['features']:
  # Nome do estado
  feature['id'] = feature['properties']['name']
  # sigla (chave): nome do estado (valor)
  state_id_map[feature['properties']['sigla']] = feature['id']
# Mapa1
row4_map1 = px.choropleth(df_mapa,
                          locations='Estado', geojson=Brazil,
                          color='Genomas sequenciados',
                          hover_name = 'Estado',
                          hover_data={'Estado': False, 
                                      'Genomas sequenciados': True},
                          color_continuous_scale=px.colors.sequential.Teal,
                          width=550, height=350)
row4_map1.update_geos(fitbounds='locations', visible=False)
row4_map1.update_layout(title_text='<b>Total de genomas sequenciados<b>',
                        margin={'l':0, 'r':0, 't':30, 'b':0})
row4_map1.update_coloraxes(colorbar={'x':0.75, 'len':0.9}, colorbar_title={'text':'Genomas'})
row4_map1.update_traces(marker_line_color='gray')
# Mapa2
row4_map2 = px.choropleth(df_mapa,
                          locations='Estado', geojson=Brazil,
                          color='Genomas/100 mil casos',
                          hover_name = 'Estado',
                          hover_data={'Estado': False, 
                                      'Genomas/100 mil casos': True},
                          color_continuous_scale=px.colors.sequential.Teal,
                          width=550, height=350)
row4_map2.update_geos(fitbounds='locations', visible=False)
row4_map2.update_layout(title_text='<b>Genomas sequenciados/100 mil casos</b>',
                        margin={'l':0, 'r':0, 't':30, 'b':0})
row4_map2.update_coloraxes(colorbar={'x':0.75, 'len':0.9}, colorbar_title={'text':'Genomas'})
row4_map2.update_traces(marker_line_color='gray')
### fim Mapas ###


### Dashboard ###
# cache = Cache(app.server, config={
#   'CACHE_TYPE': 'filesystem',
#   'CACHE_DIR': 'cache-directory'})

app.layout = dbc.Container(fluid=True,
                           children=[html.H1('VIGILÂNCIA GENÔMICA DO SARS-CoV-2 NO BRASIL', style=h1_style),
                                     html.H6('''Seguindo o padrão internacional de nomenclatura para viroses respiratórias,
                                     o nome da amostra faz referência ao local de coleta do espécime clínico.
                                     Portanto, amostras coletadas de pacientes transferidos ou viajantes entre estados são mostradas
                                     nos gráficos, tabelas e mapas de acordo com o local de coleta.''', style=h6_style), 
                                     html.Br(),
                                     html.H6('''Dados gerados pela Rede Genômica Fiocruz e/ou depositados na plataforma GISAID por outras instituições
                                     a partir de amostras brasileiras''',
                                             style={'color':'#0d2a63',
                                                    'fontSize':20,
                                                    'font-family':'sans-serif',
                                                    'textAlign':'center',
                                                    'fontWeight':'bold'}),
                                     html.H6(texto_atualizacao_voc, style={'color':'#0d2a63',
                                                                           'fontSize':14,
                                                                           'font-family':'sans-serif',
                                                                           'textAlign':'right'}),
                                     html.Div(dbc.Row(cards_list), style={'background-color':'LightSteelBlue'}),
                                     html.H6('''¹As frequências mostradas não são necessariamente representativas.
                                     Pode haver viés de seleção com a inclusão de investigação genômica de casos
                                     inusitados, rastreio de contactantes e seleção de amostras através de protocolo
                                     de inferência de RT-PCR em tempo real pra detecção de potenciais VOCs.''', style=texto_style),
                                     html.Br(),
                                     html.H2('VARIANTES EM CIRCULAÇÃO NO PERÍODO PÓS EMERGÊNCIA SANITÁRIA', style=h2_style),
                                     html.H5('Selecione a região:', style=h5_style),
                                     html.Div(dcc.Dropdown(id='regiao_dropdown1', options=regiao_dropdown, value='Brasil', clearable=False)),
                                     html.Div([html.Div(dcc.Graph(id='row1_bar', figure={}), className='six columns'),
                                               html.Div(dcc.Graph(id='row1_area', figure={}), className='six columns')], className='row'),
                                     html.Br(), html.Br(),
                                     html.H5('Selecione o estado:', style=h5_style),
                                     html.Div(dcc.Dropdown(id='estado_dropdown1', options=estado_dropdown, value='Acre', clearable=False)),
                                     html.Div([html.Div(dcc.Graph(id='row2_bar', figure={}), className='six columns'),
                                               html.Div(dcc.Graph(id='row2_area', figure={}), className='six columns')], className='row'),
                                     html.Br(), html.Br(),                  
                                     html.Hr(),
                                     html.H2('QUANTIDADE DE GENOMAS DEPOSITADOS E DISPONÍVEIS NO GISAID', style=h2_style),
                                     html.Div([html.Div(dcc.Graph(id='row3_bar', figure=row3_bar), className='six columns'),
                                               html.Div(dcc.Graph(id='row3_area', figure=row3_area), className='six columns')], className='row'),
                                     html.Br(), html.Br(), html.Br(),
                                     html.Div([html.Div(dcc.Graph(id='map1', figure=row4_map1), className='six columns'),
                                                html.Div(dcc.Graph(id='map2', figure=row4_map2), className='six columns')], className='row'),
                                     html.Br(),
                                     html.Hr(),
                                     html.H2('PRINCIPAIS LINHAGENS POR PERÍODO DE AMOSTRAGEM', style=h2_style),
                                     html.H5('Selecione a região:', style=h5_style),
                                     html.Div(dcc.Dropdown(id='regiao_dropdown2', options=regiao_dropdown, value='Brasil', clearable=False)),
                                     html.Div([html.Div(dcc.Graph(id='row5_bar', figure={}), className='six columns'),
                                               html.Div(dcc.Graph(id='row5_area', figure={}), className='six columns')], className='row'),
                                     html.Br(),
                                     html.H5('Selecione o estado:', style=h5_style),
                                     html.Div(dcc.Dropdown(id='estado_dropdown2', options=estado_dropdown, value='Acre', clearable=False)),
                                     html.Div([html.Div(dcc.Graph(id='row6_bar', figure={}), className='six columns'),
                                               html.Div(dcc.Graph(id='row6_area', figure={}), className='six columns')], className='row'),
                                     html.Br(), html.Br(),
                                     html.H5('Tabela de dados:', style=h5_style),
                                     html.Div([html.Div(dash_table.DataTable(id='tabela3', columns=[{'name': i, 'id': i} for i in tabela_dash_linhagens.columns],
                                                                            data=tabela_dash_linhagens.to_dict('records'), fixed_rows={'headers': True},
                                                                            style_table=style_table, style_cell=style_cell, style_header=style_header,
                                                                            style_cell_conditional=[
                                                                                                    {'if': {'column_id': 'Período'},
                                                                                                            'width': '10%'},
                                                                                                    {'if': {'column_id': 'Região'},
                                                                                                             'width': '15%'},
                                                                                                    {'if': {'column_id': 'Estado'},
                                                                                                             'width': '15%'},
                                                                                                    {'if': {'column_id': 'Laboratório'},
                                                                                                             'width': '13%'},
                                                                                                    {'if': {'column_id': 'Linhagens relevantes'},
                                                                                                             'width': '22%'},
                                                                                                    {'if': {'column_id': 'Quantidade'},
                                                                                                             'width': '15%'}],
                                                                                                    
                                                                              export_format="xlsx"), className='six columns')], className='row'),
                                                html.Hr(),
                                                html.H6('Genomas sequenciados e depositados em:', style=h6_style2),
                                                html.Div(html.A(href='https://www.gisaid.org/', target='_blank',                                                                 
                                                                children=html.Img(
                                                                                title='GISAID webpage',
                                                                                width=200,
                                                                                alt='GISAID webpage',
                                                                                src='https://github.com/vanleiko/RedeGenomica/blob/main/gisaid-logo.jpg?raw=true'))),
                                                html.Br(),
                                                html.H6('Casos confirmados de COVID-19 no Brasil: Painel de casos de doença pelo COVID-19 no Brasil pelo Ministério da Saúde.', style=h6_style2)])
                                                

### Callback 1 - VOCs/VOIs - Barplot - Região ###
@app.callback(Output(component_id='row1_bar', component_property='figure'),
              Input(component_id='regiao_dropdown1', component_property='value'))
def update_variantes_barplot(regiao1):
  time.sleep(2)
  if regiao1 == 'Brasil':
    return row1_bar_BR
  else:
    df_voc_barplot = cria_df_regiao(df_variantes, 'Variantes relevantes', regiao1)
  row1_bar = px.bar(df_voc_barplot,
                    x='Período', y='Quantidade', color='Variantes relevantes',
                    hover_data={'Variantes relevantes': False,
                                'Período': True,
                                'Quantidade': True},
                    hover_name='Variantes relevantes',
                    color_discrete_map=colors_variantes, category_orders=orders_variantes,
                    opacity=0.95, title=f'{regiao1}<br><sup>Variantes relevantes</sup>', height=550)
  row1_bar.update_layout(layout_barplot, margin={'l':0, 'r':0, 't':200, 'b':0},
                         legend=legend, legend_title_text=None)
  row1_bar.update_xaxes(nticks=15, tickangle=320, tickfont_size=14, showline=True, linewidth=0.5, linecolor='gray')
  row1_bar.update_yaxes(showgrid=True, gridcolor='lightgray', showline=True, linewidth=0.5, linecolor='gray')
  return row1_bar

### Callback 2 - VOCs/VOIs - Area - Região ###
@app.callback(Output(component_id='row1_area', component_property='figure'),
              Input(component_id='regiao_dropdown1', component_property='value'))
def update_variantes_area(regiao1):
  time.sleep(2)
  if regiao1 == 'Brasil':
    return row1_area_BR
  else:
    df_voc_area = cria_df_regiao(df_variantes, 'Variantes relevantes', regiao1)
  row1_area = px.area(df_voc_area,
                      x='Período', y='Quantidade', text='Quantidade',
                      color='Variantes relevantes', groupnorm='percent', 
                      title=f'{regiao1}<br><sup>Variantes relevantes</sup>',
                      color_discrete_map=colors_variantes, category_orders=orders_variantes, 
                      height=550, line_shape='spline')
  row1_area.update_layout(layout_area, margin={'l':0, 'r':0, 't':200, 'b':0}, 
                          legend=legend, legend_title_text=None, hovermode='x unified')
  row1_area.update_traces(line=dict(width=0), hovertemplate='%{text}' + ' (%{y:.1f}%)', mode='lines')
  row1_area.update_xaxes(nticks=15, tickangle=320, showgrid=True, gridcolor='lightgray', tickfont_size=14, showline=True, linewidth=0.5, linecolor='gray')
  row1_area.update_yaxes(range=[0,100], showgrid=True, gridcolor='lightgray', showline=True, linewidth=0.5, linecolor='gray')
  return row1_area

### Callback 3 - VOCs/VOIs - Barplot - UF ###
@app.callback(Output(component_id='row2_bar', component_property='figure'),
              Input(component_id='estado_dropdown1', component_property='value'))
def update_variantes_barplot(estado1):
  time.sleep(2)
  df_estado_voc_barplot = cria_df_estado(df_variantes, 'Variantes relevantes', estado1)
  if df_estado_voc_barplot['Período'].nunique() == 0:
    return grafico_nao_ha_dados
  else:
    row2_bar = px.bar(df_estado_voc_barplot,
                    x='Período', y='Quantidade', color='Variantes relevantes',
                    hover_name='Variantes relevantes',
                    hover_data={'Variantes relevantes': False,
                                'Período': True,
                                'Quantidade': True}, 
                    color_discrete_map=colors_variantes, category_orders=orders_variantes, height=550,
                    opacity=0.95, title=f'{estado1}<br><sup>Variantes relevantes</sup>')
    row2_bar.update_layout(layout_barplot, margin={'l':0, 'r':0, 't':200, 'b':0}, 
                         legend=legend, legend_title_text=None)
    row2_bar.update_xaxes(tickangle=320, tickfont_size=14, showline=True, linewidth=0.5, linecolor='gray')
    row2_bar.update_yaxes(showgrid=True, gridcolor='lightgray', showline=True, linewidth=0.5, linecolor='gray')
    return row2_bar

### Callback 4 - VOCs/VOIs - Area - UF ###
@app.callback(Output(component_id='row2_area', component_property='figure'),
                Input(component_id='estado_dropdown1', component_property='value'))
def update_variantes_area(estado1):
  time.sleep(2)
  df_estado_voc_area = cria_df_estado(df_variantes, 'Variantes relevantes', estado1)
  if df_estado_voc_area['Período'].nunique() == 0:
    return grafico_nao_ha_dados
  if df_estado_voc_area['Período'].nunique() == 1:
    return grafico_nao_ha_suficientes
  row2_area = px.area(df_estado_voc_area,
                      x='Período', y='Quantidade', text='Quantidade',
                      color='Variantes relevantes', groupnorm='percent', 
                      title=f'{estado1}<br><sup>Variantes relevantes</sup>',
                      color_discrete_map=colors_variantes, category_orders=orders_variantes, 
                      height=550, line_shape='spline')
  row2_area.update_layout(layout_area, margin={'l':0, 'r':0, 't':200, 'b':0}, 
                          legend=legend, legend_title_text=None, hovermode='x unified')
  row2_area.update_traces(line=dict(width=0), hovertemplate='%{text}' + ' (%{y:.1f}%)', mode='lines')
  row2_area.update_xaxes(tickangle=320, showgrid=True, gridcolor='lightgray', tickfont_size=14, showline=True, linewidth=0.5, linecolor='gray')
  row2_area.update_yaxes(range=[0,100], showgrid=True, gridcolor='lightgray', showline=True, linewidth=0.5, linecolor='gray')
  return row2_area


### Callback 5 - Linhagens - Barplot - Regiao ###
@app.callback(Output(component_id='row5_bar', component_property='figure'),
              Input(component_id='regiao_dropdown2', component_property='value'))
def update_linhagens(regiao2): 
  time.sleep(4)
  ### REGIÃO ###
  if regiao2 == 'Brasil':
    df_lin_barplot = df_brasil_linhagens_barplot
  else:
    df_lin_barplot = cria_df_regiao(df_linhagens, 'Linhagens relevantes', regiao2)
  row5_bar = px.bar(df_lin_barplot,
                    x='Período', y='Quantidade', color='Linhagens relevantes',
                    hover_name='Linhagens relevantes',
                    hover_data={'Linhagens relevantes': False,
                                'Período': True,
                                'Quantidade': True},                        
                    color_discrete_map=colors_linhagens, category_orders=orders_linhagens,
                    opacity=0.95, title=f'{regiao2}<br><sup>Linhagens relevantes</sup>', height=600)
  row5_bar.update_layout(layout_barplot, margin={'l':0, 'r':0, 't':270, 'b':0}, 
                         legend=legend, legend_title_text=None)
  row5_bar.update_xaxes(nticks=20, tickangle=320, tickfont_size=14, showline=True, linewidth=0.5, linecolor='gray')
  row5_bar.update_yaxes(showgrid=True, gridcolor='lightgray', showline=True, linewidth=0.5, linecolor='gray')
  return row5_bar

### Callback 6 - Linhagens - Area - Regiao ###
@app.callback(Output(component_id='row5_area', component_property='figure'),
              Input(component_id='regiao_dropdown2', component_property='value'))
def update_linhagens(regiao2): 
  time.sleep(4)
  if regiao2 == 'Brasil':
    df_lin_area = df_brasil_linhagens_area
  else:
    df_lin_area = cria_df_regiao(df_linhagens, 'Linhagens relevantes', regiao2)
  row5_area = px.area(df_lin_area,
                      x='Período', y='Quantidade', text='Quantidade',
                      color="Linhagens relevantes", groupnorm="percent", 
                      title=f'{regiao2}<br><sup>Linhagens relevantes</sup>',
                      color_discrete_map=colors_linhagens, category_orders=orders_linhagens, 
                      height=600, line_shape='spline')
  row5_area.update_layout(layout_area, margin={'l':0, 'r':0, 't':270, 'b':0}, 
                          legend=legend, legend_title_text=None, hovermode='x unified')
  row5_area.update_traces(line=dict(width=0), hovertemplate='%{text}' + ' (%{y:.1f}%)', mode='lines')
  row5_area.update_xaxes(nticks=20, tickangle=320, showgrid=True, gridcolor='lightgray', tickfont_size=14, showline=True, linewidth=0.5, linecolor='gray')
  row5_area.update_yaxes(range=[0,100], showgrid=True, gridcolor='lightgray', showline=True, linewidth=0.5, linecolor='gray')
  return row5_area

### Callback 7 - Linhagens - Barplot - UF ###
@app.callback(Output(component_id='row6_bar', component_property='figure'),
              Input(component_id='estado_dropdown2', component_property='value'))
def update_linhagens(estado2): 
  time.sleep(4)
  df_estado_lin_barplot = cria_df_estado(df_linhagens, 'Linhagens relevantes', estado2)
  row6_bar = px.bar(df_estado_lin_barplot,
                    x='Período', y='Quantidade', color='Linhagens relevantes',
                    hover_name='Linhagens relevantes',
                    hover_data={'Linhagens relevantes': False,
                                'Período': True,
                                'Quantidade': True},
                    color_discrete_map=colors_linhagens, category_orders=orders_linhagens,
                    opacity=0.95, title=f'{estado2}<br><sup>Linhagens relevantes</sup>', height=600)
  row6_bar.update_layout(layout_barplot, margin={'l':0, 'r':0, 't':250, 'b':0}, 
                         legend=legend, legend_title_text=None)
  row6_bar.update_xaxes(nticks=20, tickangle=320, tickfont_size=14, showline=True, linewidth=0.5, linecolor='gray')
  row6_bar.update_yaxes(showgrid=True, gridcolor='lightgray', showline=True, linewidth=0.5, linecolor='gray')
  return row6_bar

### Callback 8 - Linhagens - Area - UF ###
@app.callback(Output(component_id='row6_area', component_property='figure'),
              Input(component_id='estado_dropdown2', component_property='value'))
def update_linhagens(estado2): 
  time.sleep(4)
  df_estado_lin_area = cria_df_estado(df_linhagens, 'Linhagens relevantes', estado2)
  row6_area = px.area(df_estado_lin_area,
                      x='Período', y='Quantidade', text='Quantidade',
                      color='Linhagens relevantes', groupnorm='percent', 
                      title=f'{estado2}<br><sup>Linhagens relevantes</sup>',
                      color_discrete_map=colors_linhagens, category_orders=orders_linhagens, 
                      height=600, line_shape='spline')
  row6_area.update_layout(layout_area, margin={'l':0, 'r':0, 't':250, 'b':0}, 
                          legend=legend, legend_title_text=None, hovermode='x unified')
  row6_area.update_traces(line=dict(width=0), hovertemplate='%{text}' + ' (%{y:.1f}%)', mode='lines')
  row6_area.update_xaxes(nticks=20, tickangle=320, showgrid=True, gridcolor='lightgray', tickfont_size=14, showline=True, linewidth=0.5, linecolor='gray')
  row6_area.update_yaxes(range=[0,100], showgrid=True, gridcolor='lightgray', showline=True, linewidth=0.5, linecolor='gray')
  return row6_area

if __name__ == '__main__':
  app.run_server(debug=True)