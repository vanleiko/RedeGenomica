### Bibliotecas ###
import time
import flask
import pandas as pd
import json
from urllib.request import urlopen
import plotly.express as px
import plotly.graph_objects as go
import dash
from dash import dcc, html, dash_table
from dash_table.Format import Group
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from flask_caching import Cache
import ssl
import socket
import os
import sys
import _bz2
from _bz2 import BZ2Compressor, BZ2Decompressor
from OpenSSL import SSL

TIMEOUT = 60

### App ###
server = flask.Flask(__name__)
app = dash.Dash(__name__, server=server, meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1.0'}])
### fim App ###


### Datas a serem atualizadas ###
texto_atualizacao_voc ='Updated on Aug 22, 2023'
texto_atualizacao_omicron ='Updated on Apr 25, 2023'
texto_3card = 'Jul 2023'
### fim Datas a serem atualizadas ###

### Tradução PT/EN ###
dic_replace_regiao = {'Norte': 'North', 
                      'Nordeste': 'Northeast',
                      'Sudeste': 'Southeast', 
                      'Sul': 'South',
                      'Centro-oeste': 'Central-west'}
dic_regex = {'Fev': 'Feb', 'Abr': 'Apr', 'Mai': 'May',
             'Ago': 'Aug', 'Set': 'Sep', 'Out': 'Oct',
             'Dez': 'Dec', 'Gama': 'Gamma', 'Alfa': 'Alpha',
             'Outras': 'Others', 'Outra': 'Other'}
### fim Tradução ###


### Carregar datasets ###
df_genomasLaboratorio = pd.read_csv('datasets/dfGenomasLaboratorio.csv')
df_genomasLaboratorio = df_genomasLaboratorio.rename(columns={'Data': 'Date',
                                                              'Laboratório': 'Laboratory',
                                                              'Período': 'Period',
                                                              'Quantidade': 'Quantity',
                                                              'Acumulado': 'Cumullative'})
df_genomasLaboratorio = df_genomasLaboratorio.replace({'Outros': 'Others'})

df_linMes = pd.read_csv('datasets/dfLinhagensMes.csv')
df_linMes = df_linMes.replace({'Outras': 'Others'})

df_variantes = pd.read_csv('datasets/dfVariantes.csv')
df_variantes = df_variantes.replace(dic_replace_regiao)
df_variantes = df_variantes.replace(regex=dic_regex)
df_variantes = df_variantes.rename(columns={'Data': 'Date', 'Período': 'Period',
                                            'Região': 'Region', 'Estado': 'State',
                                            'Variante': 'Variant', 'Variantes relevantes': 'Relevant variants',
                                            'Quantidade': 'Quantity'})

df_linhagens = pd.read_csv('datasets/dfLinhagens.csv')
df_linhagens = df_linhagens.replace(dic_replace_regiao)
df_linhagens = df_linhagens.replace(regex=dic_regex)
df_linhagens = df_linhagens.rename(columns={'Data': 'Date', 'Período': 'Period',
                                            'Região': 'Region', 'Estado': 'State',
                                            'Variante': 'Variant', 'Linhagens relevantes': 'Relevant lineages',
                                            'Quantidade': 'Quantity'})

df_mapa = pd.read_csv('datasets/dfMapa.csv')
df_mapa = df_mapa.rename(columns={'Estado': 'State', 'Genomas sequenciados': 'Genomes sequenced',
                                  'Genomas/100 mil casos': 'Genomes/100K cases'})
### fim Carregar datasets ###


## Cards ###
## Card 1 - total de genomas sequenciados
total_genomas = df_genomasLaboratorio['Quantity'].sum()
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
tabela_dash_linhagens = df_linhagens.groupby(['Date', 'Period', 'Region', 'State', 'Laboratory', 'Relevant lineages']).sum().reset_index()
tabela_dash_linhagens = tabela_dash_linhagens.sort_values(['Date', 'Region', 'State', 'Laboratory', 'Relevant lineages'], \
                                                          ascending=[False, True, True, True, True]).drop('Date', axis=1)
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
colors_variantes = {
        'XBB.1.18.* (Omicron)': '#e377c2',
        'XBB.1.5.* (Omicron)': '#fc1cbf',
        'XBB.* (Omicron)': '#b00068',
        'FE.1.* (Omicron)': '#1f77b4',
        'Others': '#999999'}
orders_variantes = {'Relevant variants': ['Others',
                                          'FE.1.* (Omicron)',
                                          'XBB.* (Omicron)',
                                          'XBB.1.5.* (Omicron)',
                                          'XBB.1.18.* (Omicron)']}  

# Linhagens
colors_linhagens = {'B.1.617.2+AY.* (Delta)': '#750d86',
                    'B.1.1': '#fc6955', 
                    'B.1.1.28': '#e48f72', 
                    'B.1.1.33': '#f8a19f', 
                    'B.1.1.7 (Alpha)': '#ff0087', 
                    'BA.1.* (Omicron)': '#6c4516', 
                    'BA.2.* (Omicron)': '#b68e00',
                    'BA.4.* (Omicron)': '#feaf16',
                    'BA.5.* (Omicron)': '#fbe426',
                    'BE.* (Omicron)': '#b82e2e',
                    'BQ.1.* (Omicron)': '#ff7f0e',
                    'DL.1 (Omicron)': '#00cc96',
                    'XBB.* (Omicron)': '#da60ca',
                    'Others': '#999999',     
                    'P.1.* (Gamma)': '#109618',     
                    'P.2': '#862a16',
                    'FE.1.* (Omicron)': '#1f77b4',}          
orders_linhagens = {'Relevant lineages': ['B.1.1', 'B.1.1.28', 'B.1.1.33',                                             
                                          'Others',  'P.2',  'B.1.1.7 (Alpha)', 
                                          'P.1.* (Gamma)', 'B.1.617.2+AY.* (Delta)',  
                                          'BA.1.* (Omicron)', 'BA.2.* (Omicron)', 
                                          'BA.4.* (Omicron)', 'BA.5.* (Omicron)',
                                          'BE.* (Omicron)', 'BQ.1.* (Omicron)',
                                          'DL.1 (Omicron)', 'XBB.* (Omicron)',
                                          'FE.1.* (Omicron)']}                

# Genomas/Laboratório
colors_lab = {'Others': '#17becf', 
              'FIOCRUZ': '#e45756'}
orders_lab = {'Laboratory': ['Others', 'FIOCRUZ']}
# layout
layout_barplot = {'xaxis_title': '<b>Sampling period</b>', 
                  'yaxis_title': '<b>Genomes deposited</b>', 
                  'xaxis_title_font_size': 16, 
                  'yaxis_title_font_size': 16,
                  'title_x': 0.5, 
                  'title_font_size': 22, 
                  'title_font_family': 'sans-serif', 
                  'legend_font_size': 13, 
                  'plot_bgcolor': 'white', 
                  'paper_bgcolor': 'white'}
layout_area = {'xaxis_title': '<b>Sampling period</b>',
               'yaxis_title': '<b>Relative frequency (%)</b>', 
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
regiao_dropdown = [{"label": "Brazil", "value": "Brazil"},
                   {"label": "North", "value": "North"},
                   {"label": "Northeast", "value": "Northeast"},
                   {"label": "South", "value": "South"},
                   {"label": "Southeast", "value": "Southeast"},
                   {"label": "Central-west", "value": "Central-west"}]
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
  df_br = df.groupby(['Date', 'Period', coluna]).sum().reset_index()
  df_br = df_br.pivot_table(values='Quantity', index=coluna, 
                            columns=['Date', 'Period'], 
                            fill_value=0, aggfunc='sum')
  df_br.columns = df_br.columns.droplevel()
  df_br = df_br.stack().reset_index().rename(columns={0: 'Quantity'})
  return df_br
# Função para Regiões
def cria_df_regiao(df, coluna, regiao):
  df_reg = df.query('Region == @regiao').reset_index(drop=True)
  df_reg = df_reg.pivot_table(values='Quantity', index=coluna, 
                              columns=['Date', 'Period'], 
                              fill_value=0, aggfunc='sum')
  df_reg.columns = df_reg.columns.droplevel()
  df_reg = df_reg.stack().reset_index().rename(columns={0: 'Quantity'})
  return df_reg
# Função para Estados
def cria_df_estado(df, coluna, estado):
  df_estado = df.query('State == @estado').reset_index(drop=True)
  df_estado = df_estado.pivot_table(values='Quantity', index=coluna, 
                                    columns=['Data', 'Period'],
                                    fill_value=0, aggfunc='sum')
  df_estado.columns = df_estado.columns.droplevel()
  df_estado = df_estado.stack().reset_index().rename(columns={0: 'Quantity'})
  return df_estado
### fim Funções ###


### Cards ###
first_card = dbc.Card(
                  dbc.CardBody([html.H5('Genomes sequenced (total)', style=card_style_title), 
                               html.P(f'{total_genomas}', style=card_style_body)], 
                               className='card_container four columns'))
second_card = dbc.Card(
                  dbc.CardBody([html.H5('Genomes sequenced/100K cases', style=card_style_title), 
                                html.P(f'{genomas_100kcasos:.1f}', style=card_style_body)], 
                                className='card_container four columns'))
third_card = dbc.Card(
                  dbc.CardBody([html.H5(f'Most important genomes¹ in {texto_3card}', style=card_style_title), 
                                html.P(f'{top_lin_names[0]}: {top_lin_freq[0]} genomes ({top_lin_porc[0]}%)', style=third_card_style),
                                html.P(f'{top_lin_names[1]}: {top_lin_freq[1]} genomes ({top_lin_porc[1]}%)', style=third_card_style),
                                html.P(f'{top_lin_names[2]}: {top_lin_freq[2]} genomes ({top_lin_porc[2]}%)', style=third_card_style)]), 
                                className='card_container four columns') 
# salvar cards em uma lista
cards_list = [first_card, second_card, third_card]
### fim Cards ###


### DFs e gráficos Brasil VOC/VOI ###
df_brasil_variantes_barplot = cria_df_brasil(df_variantes, 'Relevant variants')
df_brasil_variantes_area = cria_df_brasil(df_variantes, 'Relevant variants')
df_brasil_linhagens_barplot = cria_df_brasil(df_linhagens, 'Relevant lineages')
df_brasil_linhagens_area = cria_df_brasil(df_linhagens, 'Relevant lineages')
## Gráfico 1 - Brasil - Barplot VOC/VOI
row1_bar_BR = px.bar(df_brasil_variantes_barplot,
                     x='Period', y='Quantity', color='Relevant variants',
                     hover_data={'Relevant variants': False,
                                 'Period': True,
                                 'Quantity': True},
                     hover_name='Relevant variants',
                     color_discrete_map=colors_variantes, category_orders=orders_variantes,
                     opacity=0.95, title=f'Brazil<br><sup>Relevant variants</sup>', height=550)
row1_bar_BR.update_layout(layout_barplot, margin={'l':0, 'r':0, 't':200, 'b':0},
                          legend=legend, legend_title_text=None)
row1_bar_BR.update_xaxes(tickangle=320, tickfont_size=14, showline=True, linewidth=0.5, linecolor='gray')
row1_bar_BR.update_yaxes(showgrid=True, gridcolor='lightgray', showline=True, linewidth=0.5, linecolor='gray')
## Gráfico 2 - Brasil - Area VOC/VOI
row1_area_BR = px.area(df_brasil_variantes_area,
                      x='Period', y='Quantity', text='Quantity',
                      color='Relevant variants', groupnorm='percent', 
                      title=f'Brazil<br><sup>Relevant variants</sup>',
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
                  x='Period', y='Quantity',
                  color='Laboratory',
                  color_discrete_map=colors_lab,
                  category_orders=orders_lab,
                  opacity=0.9, height=470)
row3_bar.update_layout(title='By sampling month', title_x=0.5,
                       title_font_size=20, title_font_family='sans-serif',
                       xaxis_title='<b>Sampling period</b>',
                       yaxis_title='<b>Genomes deposited on GISAID</b>',
                       xaxis_title_font_size=16, yaxis_title_font_size=16,
                       plot_bgcolor='white', paper_bgcolor='white',
                       margin={'l':0, 'r':0, 't':80, 'b':0}, 
                       legend=legend, legend_title_text='Laboratory:')
row3_bar.update_xaxes(nticks=20, tickangle=320, showline=True, linewidth=0.5, linecolor='gray')
row3_bar.update_yaxes(showgrid=True, gridcolor='lightgray', showline=True, linewidth=0.5, linecolor='gray')
# Area - acumulados
row3_area = px.area(df_genomasLaboratorio,
                    x='Period', y='Cumullative',
                    color='Laboratory',
                    color_discrete_map=colors_lab,
                    category_orders=orders_lab,
                    height=470, line_shape='spline')
row3_area.update_layout(title='Cumullative', title_x=0.5, 
                        title_font_size=20, title_font_family='sans-serif',
                        xaxis_title='<b>Sampling period</b>',
                        yaxis_title='<b>Genomes deposited on GISAID</b>',
                        xaxis_title_font_size=16, yaxis_title_font_size=16,
                        plot_bgcolor='white', paper_bgcolor='white',
                        margin={'l':0, 'r':0, 't':80, 'b':0}, 
                        legend=legend, legend_title_text='Laboratory:')
row3_area.update_traces(line={'width':0})
row3_area.update_xaxes(nticks=20, tickangle=320, showgrid=True, gridcolor='lightgray', showline=True, linewidth=0.5, linecolor='gray')
row3_area.update_yaxes(showgrid=True, gridcolor='lightgray', showline=True, linewidth=0.5, linecolor='gray')
### fim Gráficos - Quantidade de genomas sequenciados/Laboratório ###

### Gráfico quando nao há dados para a UF ###
grafico_nao_ha_dados = go.Figure() 
grafico_nao_ha_dados.add_annotation(showarrow=False,
                                    text='No data', 
                                    font={'size':30,
                                          'color':'gray'},
                                    align='center')
grafico_nao_ha_dados.update_layout(height=400,
                                   margin={'l':0, 'r':0, 't':50, 'b':50})
## Gráfico nao há dados suficientes (só 1 mes) para a UF
grafico_nao_ha_suficientes = go.Figure() 
grafico_nao_ha_suficientes.add_annotation(showarrow=False,
                                          text='Not enough data', 
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
                          locations='State', geojson=Brazil,
                          color='Genomes sequenced',
                          hover_name = 'State',
                          hover_data={'State': False, 
                                      'Genomes sequenced': True},
                          color_continuous_scale=px.colors.sequential.Teal,
                          width=550, height=350)
row4_map1.update_geos(fitbounds='locations', visible=False)
row4_map1.update_layout(title_text='<b>Genomes sequenced (total)<b>',
                        margin={'l':0, 'r':0, 't':30, 'b':0})
row4_map1.update_coloraxes(colorbar={'x':0.75, 'len':0.9}, colorbar_title={'text':'Genomes'})
row4_map1.update_traces(marker_line_color='gray')
# Mapa2
row4_map2 = px.choropleth(df_mapa,
                          locations='State', geojson=Brazil,
                          color='Genomes/100K cases',
                          hover_name = 'State',
                          hover_data={'State': False, 
                                      'Genomes/100K cases': True},
                          color_continuous_scale=px.colors.sequential.Teal,
                          width=550, height=350)
row4_map2.update_geos(fitbounds='locations', visible=False)
row4_map2.update_layout(title_text='<b>Genomes sequenced/100K cases</b>',
                        margin={'l':0, 'r':0, 't':30, 'b':0})
row4_map2.update_coloraxes(colorbar={'x':0.75, 'len':0.9}, colorbar_title={'text':'Genomes'})
row4_map2.update_traces(marker_line_color='gray')
### fim Mapas ###


### Dashboard ###
cache = Cache(app.server, config={
  'CACHE_TYPE': 'filesystem',
  'CACHE_DIR': 'cache-directory'})

app.layout = dbc.Container(fluid=True,
                           children=[html.H1('SARS-CoV-2 Genomic Surveillance in Brazil', style=h1_style),
                                     html.H6('''Following the international nomenclature standard for respiratory viruses,
                                             the place of collection of the clinical specimem is referred within the sample names.
                                             Therefore, samples from patients who have been transferred to other cities or travelers
                                             are represented in plots, tables and maps according to the location of sample collection.''', style=h6_style), 
                                     html.Br(),
                                     html.H6('''Genomes generated from samples collected in Brazil and deposited on GISAID by the Fiocruz Genomic Network or other institutions''',
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
                                     html.H6('''¹The ratios shown here do not necessarily represent the true ratios.
                                             Sample biases may have been introduced due to investigations of unusual cases, contact tracing, or sample selection due
                                             to inference protocols for detection of VOCs by RT-PCR''', style=texto_style),
                                     html.Br(),
                                     html.H2('VARIANTS IN CIRCULATION DURING THE POST HEALTH EMERGENCY PERIOD', style=h2_style),
                                     html.H5('Select region:', style=h5_style),
                                     html.Div(dcc.Dropdown(id='regiao_dropdown1', options=regiao_dropdown, value='Brazil', clearable=False)),
                                     html.Div([html.Div(dcc.Graph(id='row1_bar', figure={}), className='six columns'),
                                               html.Div(dcc.Graph(id='row1_area', figure={}), className='six columns')], className='row'),
                                     html.Br(), html.Br(),
                                     html.H5('Select state:', style=h5_style),
                                     html.Div(dcc.Dropdown(id='estado_dropdown1', options=estado_dropdown, value='Acre', clearable=False)),
                                     html.Div([html.Div(dcc.Graph(id='row2_bar', figure={}), className='six columns'),
                                               html.Div(dcc.Graph(id='row2_area', figure={}), className='six columns')], className='row'),
                                     html.Br(), html.Br(),                  
                                     html.Hr(),
                                     html.H2('NUMBER OF GENOMES UPLOADED AND AVAILABLE ON GISAID', style=h2_style),
                                     html.Div([html.Div(dcc.Graph(id='row3_bar', figure=row3_bar), className='six columns'),
                                               html.Div(dcc.Graph(id='row3_area', figure=row3_area), className='six columns')], className='row'),
                                     html.Br(), html.Br(), html.Br(),
                                     html.Div([html.Div(dcc.Graph(id='map1', figure=row4_map1), className='six columns'),
                                                html.Div(dcc.Graph(id='map2', figure=row4_map2), className='six columns')], className='row'),
                                     html.Br(),
                                     html.Hr(),
                                     html.H2('IMPORTANT LINEAGES BY SAMPLING PERIOD', style=h2_style),
                                     html.H5('Select region:', style=h5_style),
                                     html.Div(dcc.Dropdown(id='regiao_dropdown2', options=regiao_dropdown, value='Brazil', clearable=False)),
                                     html.Div([html.Div(dcc.Graph(id='row5_bar', figure={}), className='six columns'),
                                               html.Div(dcc.Graph(id='row5_area', figure={}), className='six columns')], className='row'),
                                     html.Br(),
                                     html.H5('Select state:', style=h5_style),
                                     html.Div(dcc.Dropdown(id='estado_dropdown2', options=estado_dropdown, value='Acre', clearable=False)),
                                     html.Div([html.Div(dcc.Graph(id='row6_bar', figure={}), className='six columns'),
                                               html.Div(dcc.Graph(id='row6_area', figure={}), className='six columns')], className='row'),
                                     html.Br(), html.Br(),
                                     html.H5('Data table:', style=h5_style),
                                     html.Div([html.Div(dash_table.DataTable(id='tabela3', columns=[{'name': i, 'id': i} for i in tabela_dash_linhagens.columns],
                                                                            data=tabela_dash_linhagens.to_dict('records'), fixed_rows={'headers': True},
                                                                            style_table=style_table, style_cell=style_cell, style_header=style_header,
                                                                            style_cell_conditional=[
                                                                                                    {'if': {'column_id': 'Period'},
                                                                                                            'width': '10%'},
                                                                                                    {'if': {'column_id': 'Region'},
                                                                                                             'width': '15%'},
                                                                                                    {'if': {'column_id': 'State'},
                                                                                                             'width': '15%'},
                                                                                                    {'if': {'column_id': 'Laboratory'},
                                                                                                             'width': '13%'},
                                                                                                    {'if': {'column_id': 'Relevant lineages'},
                                                                                                             'width': '22%'},
                                                                                                    {'if': {'column_id': 'Quantity'},
                                                                                                             'width': '15%'}],
                                                                                                    
                                                                              export_format="xlsx"), className='six columns')], className='row'),
                                                html.Hr(),
                                                html.H6('Genomes sequenced and deposited on:', style=h6_style2),
                                                html.Div(html.A(href='https://www.gisaid.org/', target='_blank',                                                                 
                                                                children=html.Img(
                                                                                title='GISAID webpage',
                                                                                width=200,
                                                                                alt='GISAID webpage',
                                                                                src='https://github.com/vanleiko/RedeGenomica/blob/main/gisaid-logo.jpg?raw=true'))),
                                                html.Br(),
                                                html.H6('Confirmed cases of COVID-19 in Brazil: Panel of COVID-19 disease cases in Brazil by the Ministry of Health.', style=h6_style2)])
                                                

### Callback 1 - VOCs/VOIs - Barplot - Região ###
@app.callback(Output(component_id='row1_bar', component_property='figure'),
              Input(component_id='regiao_dropdown1', component_property='value'))
def update_variantes_barplot(regiao1):
  time.sleep(2)
  if regiao1 == 'Brazil':
    return row1_bar_BR
  else:
    df_voc_barplot = cria_df_regiao(df_variantes, 'Relevant variants', regiao1)
  row1_bar = px.bar(df_voc_barplot,
                    x='Period', y='Quantity', color='Relevant variants',
                    hover_data={'Relevant variants': False,
                                'Period': True,
                                'Quantity': True},
                    hover_name='Relevant variants',
                    color_discrete_map=colors_variantes, category_orders=orders_variantes,
                    opacity=0.95, title=f'{regiao1}<br><sup>Relevant variants</sup>', height=550)
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
  if regiao1 == 'Brazil':
    return row1_area_BR
  else:
    df_voc_area = cria_df_regiao(df_variantes, 'Relevant variants', regiao1)
  row1_area = px.area(df_voc_area,
                      x='Period', y='Quantity', text='Quantity',
                      color='Relevant variants', groupnorm='percent', 
                      title=f'{regiao1}<br><sup>Relevant variants</sup>',
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
  df_estado_voc_barplot = cria_df_estado(df_variantes, 'Relevant variants', estado1)
  if df_estado_voc_barplot['Period'].nunique() == 0:
    return grafico_nao_ha_dados
  else:
    row2_bar = px.bar(df_estado_voc_barplot,
                    x='Period', y='Quantity', color='Relevant variants',
                    hover_name='Relevant variants',
                    hover_data={'Relevant variants': False,
                                'Period': True,
                                'Quantity': True}, 
                    color_discrete_map=colors_variantes, category_orders=orders_variantes, height=550,
                    opacity=0.95, title=f'{estado1}<br><sup>Relevant variants</sup>')
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
  df_estado_voc_area = cria_df_estado(df_variantes, 'Relevant variants', estado1)
  if df_estado_voc_area['Period'].nunique() == 0:
    return grafico_nao_ha_dados
  if df_estado_voc_area['Period'].nunique() == 1:
    return grafico_nao_ha_suficientes
  row2_area = px.area(df_estado_voc_area,
                      x='Period', y='Quantity', text='Quantity',
                      color='Relevant variants', groupnorm='percent', 
                      title=f'{estado1}<br><sup>Relevant variants</sup>',
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
  if regiao2 == 'Brazil':
    df_lin_barplot = df_brasil_linhagens_barplot
  else:
    df_lin_barplot = cria_df_regiao(df_linhagens, 'Relevant lineages', regiao2)
  row5_bar = px.bar(df_lin_barplot,
                    x='Period', y='Quantity', color='Relevant lineages',
                    hover_name='Relevant lineages',
                    hover_data={'Relevant lineages': False,
                                'Period': True,
                                'Quantity': True},                        
                    color_discrete_map=colors_linhagens, category_orders=orders_linhagens,
                    opacity=0.95, title=f'{regiao2}<br><sup>Relevant lineages</sup>', height=600)
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
  if regiao2 == 'Brazil':
    df_lin_area = df_brasil_linhagens_area
  else:
    df_lin_area = cria_df_regiao(df_linhagens, 'Relevant lineages', regiao2)
  row5_area = px.area(df_lin_area,
                      x='Period', y='Quantity', text='Quantity',
                      color='Relevant lineages', groupnorm='percent', 
                      title=f'{regiao2}<br><sup>Relevant lineages</sup>',
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
  df_estado_lin_barplot = cria_df_estado(df_linhagens, 'Relevant lineages', estado2)
  row6_bar = px.bar(df_estado_lin_barplot,
                    x='Period', y='Quantity', color='Relevant lineages',
                    hover_name='Relevant lineages',
                    hover_data={'Relevant lineages': False,
                                'Period': True,
                                'Quantity': True},
                    color_discrete_map=colors_linhagens, category_orders=orders_linhagens,
                    opacity=0.95, title=f'{estado2}<br><sup>Relevant lineages</sup>', height=600)
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
  df_estado_lin_area = cria_df_estado(df_linhagens, 'Relevant lineages', estado2)
  row6_area = px.area(df_estado_lin_area,
                      x='Period', y='Quantity', text='Quantity',
                      color='Relevant lineages', groupnorm='percent', 
                      title=f'{estado2}<br><sup>Relevant lineages</sup>',
                      color_discrete_map=colors_linhagens, category_orders=orders_linhagens, 
                      height=600, line_shape='spline')
  row6_area.update_layout(layout_area, margin={'l':0, 'r':0, 't':250, 'b':0}, 
                          legend=legend, legend_title_text=None, hovermode='x unified')
  row6_area.update_traces(line=dict(width=0), hovertemplate='%{text}' + ' (%{y:.1f}%)', mode='lines')
  row6_area.update_xaxes(nticks=20, tickangle=320, showgrid=True, gridcolor='lightgray', tickfont_size=14, showline=True, linewidth=0.5, linecolor='gray')
  row6_area.update_yaxes(range=[0,100], showgrid=True, gridcolor='lightgray', showline=True, linewidth=0.5, linecolor='gray')
  return row6_area
