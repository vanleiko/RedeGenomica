### Bibliotecas ###
import time
import flask
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from urllib.request import urlopen
from plotly.subplots import make_subplots
import json
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output


TIMEOUT = 60

### App ###
server = flask.Flask(__name__)
app = dash.Dash(__name__, server=server,
                meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1.0'}])
### fim App ###


### Datas a serem atualizadas ###
texto_atualizacao_data ='Atualizado em 20/02/2024'
### fim Datas a serem atualizadas ###

### Carregar datasets ###
# aba GISAID
df0_mapa = pd.read_csv('/home/vanessaleiko/mysite/df0_mapa_dengue.csv')
df1_anoSorotipo = pd.read_csv('/home/vanessaleiko/mysite/df1_anoSorotipo.csv')
df1_acumulado = pd.read_csv('/home/vanessaleiko/mysite/df1_acumulado.csv')
df2_agrupado_periodo_brasil = pd.read_csv('/home/vanessaleiko/mysite/df2_agrupado_periodo_brasil.csv')
df2_agrupado_periodo_regiao = pd.read_csv('/home/vanessaleiko/mysite/df2_agrupado_periodo_regiao.csv')
df3_agrupado_periodo_estado = pd.read_csv('/home/vanessaleiko/mysite/df3_agrupado_periodo_estado.csv')
# aba PCR
# BR
df_pcr_br_ano = pd.read_csv('/home/vanessaleiko/mysite/df_dengue_pcr_ano.csv')
df_pcr_br_periodo = pd.read_csv('/home/vanessaleiko/mysite/df_dengue_pcr_periodo.csv')
# regiao
df_pcr_regiao_ano = pd.read_csv('/home/vanessaleiko/mysite/df_dengue_pcr_regiao_ano.csv')
df_pcr_regiao_periodo = pd.read_csv('/home/vanessaleiko/mysite/df_dengue_pcr_regiao_periodo.csv')
# uf
df_pcr_estado_ano = pd.read_csv('/home/vanessaleiko/mysite/df_dengue_pcr_estado_ano.csv')
df_pcr_estado_periodo = pd.read_csv('/home/vanessaleiko/mysite/df_dengue_pcr_estado_periodo.csv')


### Estilos dos textos ###
# estilo html.H2 - título principal
h1_style={'color':'#f0f0f0',
          'background-color': '#316395',
          'fontSize':50,
          'font-family':'sans-serif',
          'textAlign':'center',
          'font-weight':'bold'}

# estilo html.H2 - título dos gráficos
h2_style={'color':'#f0f0f0',
          'background-color': '#316395',
          'fontSize':34,
          'font-family':'sans-serif',
          'textAlign':'center',
          'font-weight':'bold'}

# estilo html.H6 - subtítulo do título principal
h6_style={'color':'#0d2a63',
          'fontSize':18,
          'font-family':'sans-serif',
          'textAlign':'center'}

# estilo do texto abaixo dos cards
texto_style = {'color':'#0d2a63',
               'fontSize':14,
               'font-family':'sans-serif',
               'textAlign':'justify'}

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
### fim Estilos dos textos ###


### Cores e layout dos gráficos ###
ordem_tipo = {'Tipo': ['DENV1:desconhecido',
                       'DENV1:II', 'DENV1:III', 'DENV1:V',
                       'DENV2:desconhecido',
                       'DENV2:I-American', 'DENV2:II-Cosmopolitan', 'DENV2:III-Asian-American', 'DENV2:IV-AsianII',
                       'DENV3:desconhecido',
                       'DENV3:I', 'DENV3:III', 'DENV3:V',
                       'DENV4:desconhecido'
                       'DENV4:I', 'DENV4:II']}

cor_tipo = {'DENV1:II': '#fcae91', 'DENV1:III': '#fb6a4a', 'DENV1:V': '#cb181d',
            'DENV1:desconhecido': '#fbb4ae' ,
            'DENV2:I-American': '#bdd7e7', 'DENV2:II-Cosmopolitan': '#6baed6',
            'DENV2:III-Asian-American':'#3182bd', 'DENV2:IV-AsianII': '#08519c',
            'DENV2:desconhecido': '#b3cde3',
            'DENV3:I': '#bae4b3', 'DENV3:III': '#74c476', 'DENV3:V': '#238b45',
            'DENV3:desconhecido': '#ccebc5' ,
            'DENV4:I': '#feaf16', 'DENV4:II': '#b68100',
            'DENV4:desconhecido': '#fed9a6'}

ordem_sorotipo = {'Sorotipo': ['DENV1', 'DENV2', 'DENV3', 'DENV4']}

cor_sorotipo = {'DENV1': '#cb181d', 'DENV2': '#08519c',
                'DENV3': '#238b45', 'DENV4': '#b68100'}

layout_fig1barplot = {'xaxis_title': '<b>Ano de amostragem</b>',
                      'yaxis_title': '<b>Genomas depositados</b>',
                      'xaxis_title_font_size': 14,
                      'yaxis_title_font_size': 14,
                      'xaxis_title_font_color': '#222a2a',
                      'yaxis_title_font_color': '#222a2a',
                      'legend_font_size': 12,
                      'plot_bgcolor': 'white',
                      'paper_bgcolor': 'white'}

layout_fig1acumulado = {'xaxis_title': '<b>Ano de amostragem</b>',
                        'yaxis_title': '<b>Genomas depositados</b>',
                        'xaxis_title_font_size': 14,
                        'yaxis_title_font_size': 14,
                        'title_font_size': 22}

layout_barplot = {'xaxis_title': '<b>Período de amostragem</b>',
                  'yaxis_title': '<b>Genomas depositados</b>',
                  'xaxis_title_font_size': 14,
                  'yaxis_title_font_size': 14,
                  'xaxis_title_font_color': '#222a2a',
                  'yaxis_title_font_color': '#222a2a',
                  'legend_font_size': 12,
                  'plot_bgcolor': 'white',
                  'paper_bgcolor': 'white'}

layout_area = {'xaxis_title': '<b>Ano de amostragem</b>',
               'yaxis_title': '<b>Frequência (%)</b>',
               'xaxis_title_font_size': 14,
               'yaxis_title_font_size': 14,
               'xaxis_title_font_color': '#222a2a',
               'yaxis_title_font_color': '#222a2a',
               'legend_font_size': 12}

layout_legenda={'orientation': 'h',
                'xanchor': 'center',
                'yanchor': 'bottom',
                'x': 0.5, 'y': 1.0,
                'font_color': '#222a2a'}

tabs_styles = {'height':'46px'}

tab_style = {'borderBottom':'8px solid #d6d6d6',
             'borderTop':'1px solid #d6d6d6',
             'borderRight':'4px solid #d6d6d6',
             'borderLeft':'4px solid #d6d6d6',
             'padding':'6px',
             'fontSize':18}

tab_selected_style = {'borderTop':'8px solid #d6d6d6',
                      'borderRight':'4px solid #d6d6d6',
                      'borderLeft':'4px solid #d6d6d6',
                      'borderBottom':'1px solid #d6d6d6',
                      'backgroundColor':'#119DFF',
                      'color':'white',
                      'padding':'6px',
                      'fontWeight':'bold',
                      'fontSize':18}
### fim Cores e layout gráficos ###


### Dropdowns ###
decada_dropdown_regiao = [{"label": "1980", "value": 1980},
                          {"label": "1990", "value": 1990},
                          {"label": "2000", "value": 2000},
                          {"label": "2010", "value": 2010},
                          {"label": "2020", "value": 2020}]

decada_dropdown_estado = [{"label": "1980", "value": 1980},
                          {"label": "1990", "value": 1990},
                          {"label": "2000", "value": 2000},
                          {"label": "2010", "value": 2010},
                          {"label": "2020", "value": 2020}]

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


### MAPA ###
with urlopen('https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson') as response:
   Brazil=json.load(response)
state_id_map = {}
for feature in Brazil['features']:
  # Nome do estado
  feature['id'] = feature['properties']['name']
  # sigla (chave): nome do estado (valor)
  state_id_map[feature['properties']['sigla']] = feature['id']

fig_mapa = px.choropleth(df0_mapa,
                         locations='Estado',
                         geojson=Brazil,
                         color='Quantidade',
                         hover_name = 'Estado',
                         hover_data={'Quantidade': True,
                                     'Estado': False},
                         color_continuous_scale=px.colors.sequential.Blues,
                         template='gridon')

fig_mapa.update_geos(fitbounds='locations', visible=False)

fig_mapa.update_layout(title_text='<b>Total de genomas depositados<b>',
                       font_size=14, margin={'l':0, 'r':0, 't':35, 'b':0})

fig_mapa.update_coloraxes(colorbar={'x':0.75, 'len':0.9},
                          colorbar_title={'text':'Quantidade'})

fig_mapa.update_traces(marker_line_color='gray')
### Fim MAPA ###

### Barplot total por sorotipo e aumulado ####
# barplot por Sorotipo
fig1_anoSorotipo = px.bar(df1_anoSorotipo,
                          x='Ano',
                          y='Quantidade',
                          color='Sorotipo',
                          template='gridon',
                          height=450,
                          width=750,
                          category_orders=ordem_sorotipo,
                          color_discrete_map=cor_sorotipo)

fig1_anoSorotipo.update_layout(layout_fig1barplot, legend_title_text=None, legend=layout_legenda)

fig1_anoSorotipo.update_xaxes(showgrid=False, tickangle=320, tickfont_size=14, nticks=24,
                              showline=True, linewidth=1, linecolor='#222a2a',
                              categoryorder='category ascending')

fig1_anoSorotipo.update_yaxes(showgrid=True, gridcolor='lightgray',
                              showline=True, linewidth=1, linecolor='#222a2a')

# Acumulado
fig1_acumulado = px.area(df1_acumulado,
                         x='Ano',
                         y='Acumulado',
                         height=450,
                         width=750,
                         template='gridon',
                         line_shape='spline',
                         title='Valores acumulados')

fig1_acumulado.update_layout(layout_fig1acumulado)

fig1_acumulado.update_xaxes(nticks=25, tickangle=320,
                            showgrid=False,
                            showline=True, linewidth=1, linecolor='#222a2a')

fig1_acumulado.update_yaxes(showgrid=True, gridcolor='lightgray',
                            showline=True, linewidth=1, linecolor='#222a2a')


### Gráfico quando nao há dados para a UF
fig_nao_ha_dados = go.Figure()
fig_nao_ha_dados.add_annotation(showarrow=False,
                                text='Não há dados',
                                font={'size':30,
                                      'color':'gray'},
                                align='center')
fig_nao_ha_dados.update_layout(height=400,
                               margin={'l':0, 'r':0, 't':50, 'b':50})


### ABA PCR ###
# dfs Brasil
df_pcr_br_ano['Sorotipo'] = df_pcr_br_ano['Sorotipo'].astype('str')
df_pcr_br_periodo['Sorotipo'] = df_pcr_br_periodo['Sorotipo'].astype('str')

df_sorotipo1_ano = df_pcr_br_ano.query('Sorotipo == "1"').reset_index(drop=True)
df_sorotipo2_ano = df_pcr_br_ano.query('Sorotipo == "2"').reset_index(drop=True)
df_sorotipo3_ano = df_pcr_br_ano.query('Sorotipo == "3"').reset_index(drop=True)
df_sorotipo4_ano = df_pcr_br_ano.query('Sorotipo == "4"').reset_index(drop=True)
df_sorotipo1_periodo = df_pcr_br_periodo.query('Sorotipo == "1"').reset_index(drop=True)
df_sorotipo2_periodo = df_pcr_br_periodo.query('Sorotipo == "2"').reset_index(drop=True)
df_sorotipo3_periodo = df_pcr_br_periodo.query('Sorotipo == "3"').reset_index(drop=True)
df_sorotipo4_periodo = df_pcr_br_periodo.query('Sorotipo == "4"').reset_index(drop=True)

# figura Brasil
fig_pcr_br = make_subplots(specs=[[{"secondary_y": True}]])
fig_pcr_br.add_trace(go.Bar(name='Sorotipo 1',
                            marker_color='cornflowerblue',
                            x=df_sorotipo1_periodo['Período'],
                            y=df_sorotipo1_periodo['CasosExtrap']),
                      secondary_y=False)
fig_pcr_br.add_trace(go.Bar(name='Sorotipo 2',
                            marker_color='orange',
                            x=df_sorotipo2_periodo['Período'],
                            y=df_sorotipo2_periodo['CasosExtrap']),
                      secondary_y=False)
fig_pcr_br.add_trace(go.Bar(name='Sorotipo 3',
                            marker_color='green',
                            x=df_sorotipo3_periodo['Período'],
                            y=df_sorotipo3_periodo['CasosExtrap']),
                      secondary_y=False)
fig_pcr_br.add_trace(go.Bar(name='Sorotipo 4',
                            marker_color='red',
                            x=df_sorotipo4_periodo['Período'],
                            y=df_sorotipo4_periodo['CasosExtrap']),
                      secondary_y=False)

# LINHA
fig_pcr_br.add_trace(go.Scatter(showlegend=False,
                                name='Sorotipo 1',
                                marker_color='cornflowerblue',
                                x=df_sorotipo1_ano['Ano'],
                                y=df_sorotipo1_ano['Porcentagem'],
                                hovertemplate = 'Frequência: %{y}%'),
                      secondary_y=True)
fig_pcr_br.add_trace(go.Scatter(showlegend=False,
                                name='Sorotipo 2',
                                marker_color='orange',
                                x=df_sorotipo2_ano['Ano'],
                                y=df_sorotipo2_ano['Porcentagem'],
                                hovertemplate = 'Frequência: %{y}%'),
                      secondary_y=True)
fig_pcr_br.add_trace(go.Scatter(showlegend=False,
                                name='Sorotipo 3',
                                marker_color='green',
                                x=df_sorotipo3_ano['Ano'],
                                y=df_sorotipo3_ano['Porcentagem'],
                                hovertemplate = 'Frequência: %{y}%'),
                      secondary_y=True)
fig_pcr_br.add_trace(go.Scatter(showlegend=False,
                                name='Sorotipo 4',
                                marker_color='red',
                                x=df_sorotipo4_ano['Ano'],
                                y=df_sorotipo4_ano['Porcentagem'],
                                hovertemplate = 'Frequência: %{y}%'),
                      secondary_y=True)
fig_pcr_br.update_layout(barmode='stack',
                         legend_font_size=16,
                         legend_traceorder='normal',
                         legend_orientation='h',
                         legend_xanchor = 'center',
                         legend_yanchor = 'bottom',
                         legend_x= 0.5, legend_y= 1.0,
                         plot_bgcolor='white',
                         title_text='Brasil',
                         xaxis_title='Período de amostragem',
                         yaxis_title='Casos de dengue')
fig_pcr_br.update_xaxes(showline=True, linewidth=1.5, linecolor='lightgray')
fig_pcr_br.update_yaxes(showline=True, linewidth=1.5, linecolor='lightgray', secondary_y=False)
fig_pcr_br.update_yaxes(secondary_y=True, showline=True, linewidth=1.5, linecolor='lightgray',
                        title_text='Sorotipos (%)', rangemode='tozero', range=[0,100])

## Funções para filtrar Região/Estado e extrapolar a frequência dos sorotipos para os casos
# função para criar um DF com a porcentagem de sorotipo por caso por ANO e por Região
def calcula_frequencia_sorotipo(df, col_name_tempo, col_name_local, local,):
  df_filtrado = df[df[f'{col_name_local}'] == local]
  # lista com os ANOS
  lista_tempo = df_filtrado[f'{col_name_tempo}'].unique()
  # cria df vazio
  df_final = pd.DataFrame(columns=[f'{col_name_local}', f'{col_name_tempo}', 'Sorotipo', 'Casos'])
  # percorrer cada período
  for t in lista_tempo:
    # filtrar o ANO
    df_filtrado_total = df_filtrado[df_filtrado[f'{col_name_tempo}'] == t]
    # filtrar o ANO e sorotipo
    df_filtrado_sorotipo = df_filtrado[df_filtrado[f'{col_name_tempo}'] == t]
    df_filtrado_sorotipo = df_filtrado_sorotipo.query('Sorotipo != "Sem informação"')
    # total de casos do período
    total_casos = df_filtrado_total['Casos'].sum()
    total_casos_sorotipo = df_filtrado_sorotipo['Casos'].sum()
    # porcentagem de cada sorotipo por ANO pelo total de casos do ANO
    df_filtrado_sorotipo['CasosExtrap'] = (df_filtrado_sorotipo['Casos']*total_casos)/total_casos_sorotipo
    df_filtrado_sorotipo['CasosExtrap'] = df_filtrado_sorotipo['CasosExtrap'].round(0)
    df_filtrado_sorotipo['Porcentagem'] = ((df_filtrado_sorotipo['CasosExtrap']/total_casos)*100).round(2)
    # juntar os períodos
    df_final = pd.concat([df_final, df_filtrado_sorotipo])
  df_final['Sorotipo'] = df_final['Sorotipo'].astype('str').str[0]
  df_sorotipo1 = df_final.query('Sorotipo == "1"').reset_index(drop=True)
  df_sorotipo2 = df_final.query('Sorotipo == "2"').reset_index(drop=True)
  df_sorotipo3 = df_final.query('Sorotipo == "3"').reset_index(drop=True)
  df_sorotipo4 = df_final.query('Sorotipo == "4"').reset_index(drop=True)
  return df_sorotipo1, df_sorotipo2, df_sorotipo3, df_sorotipo4
### fim ABA PCR ###


### Dashboard ###
# cache = Cache(app.server, config={
#   'CACHE_TYPE': 'filesystem',
#   'CACHE_DIR': 'cache-directory'})
app.layout = dbc.Container(fluid=True,
                           children=[html.H1('VIGILÂNCIA GENÔMICA DA DENGUE NO BRASIL', style=h1_style),
                                     html.H6('''Seguindo o padrão internacional de nomenclatura para viroses respiratórias,
                                     o nome da amostra faz referência ao local de coleta do espécime clínico.
                                     Portanto, amostras coletadas de pacientes transferidos ou viajantes entre estados são mostradas
                                     nos gráficos, tabelas e mapas de acordo com o local de coleta.''', style=h6_style),
                                     html.Br(),
                                     # TABS
                                     dcc.Tabs(style=tabs_styles,
                                              children=[
                                     dcc.Tab(label='Genomas depositados no GISAID',
                                             style=tab_style,
                                             selected_style=tab_selected_style,
                                             children=[
                                     html.Br(),
                                     html.H6('''Dados gerados pela Rede Genômica Fiocruz e/ou depositados na plataforma GISAID por outras instituições
                                     a partir de amostras brasileiras''',
                                             style={'color':'#0d2a63',
                                                    'fontSize':20,
                                                    'font-family':'sans-serif',
                                                    'textAlign':'center',
                                                    'fontWeight':'bold'}),
                                     html.Br(),
                                     html.H6(texto_atualizacao_data, style={'color':'#0d2a63',
                                                                            'fontSize':14,
                                                                            'font-family':'sans-serif',
                                                                            'textAlign':'right'}),
                                     html.H6('''¹As frequências mostradas não são necessariamente representativas.
                                     Pode haver viés de seleção com a inclusão de investigação genômica de casos
                                     inusitados, rastreio de contactantes e seleção de amostras através de protocolo
                                     de inferência de RT-PCR em tempo real pra detecção de potenciais VOCs.''', style=texto_style),
                                     html.Br(),
                                     html.H2('TOTAL DE GENOMAS DEPOSITADOS E DISPONÍVEIS NO GISAID', style=h2_style),
                                     html.Div([html.Div(dcc.Graph(id='fig1_anoSorotipo', figure=fig1_anoSorotipo), className='six columns'),
                                               html.Div(dcc.Graph(id='fig1_acumulado', figure=fig1_acumulado), className='six columns')], className='row'),
                                     html.Br(),
                                     html.Div([html.Div(dcc.Graph(id='mapa', figure=fig_mapa))], className='row'),
                                     html.Br(),
                                     html.Br(),
                                     html.H2('GENÓTIPOS EM CIRCULAÇÃO', style=h2_style),
                                     html.H5('Selecione a região:', style=h5_style),
                                     html.Div(dcc.Dropdown(id='regiao_dropdown', options=regiao_dropdown, value='Brasil', clearable=False)),
                                     html.Br(),
                                     html.H5('Selecione a década:', style=h5_style),
                                     html.Div(dcc.Dropdown(id='decada_dropdown_regiao', options=decada_dropdown_regiao, value=2020, clearable=False)),
                                     html.Div([html.Div(dcc.Graph(id='fig2_barplot', figure={}), className='six columns'),
                                               html.Div(dcc.Graph(id='fig2_area', figure={}), className='six columns')], className='row'),
                                     html.Br(),
                                     html.Br(),
                                     html.Br(),
                                     html.H5('Selecione o estado:', style=h5_style),
                                     html.Div(dcc.Dropdown(id='estado_dropdown', options=estado_dropdown, value='Acre', clearable=False)),
                                     html.Br(),
                                     html.H5('Selecione a década:', style=h5_style),
                                     html.Div(dcc.Dropdown(id='decada_dropdown_estado', options=decada_dropdown_estado, value=2020, clearable=False)),
                                     html.Div([html.Div(dcc.Graph(id='fig3_barplot', figure={}), className='six columns'),
                                               html.Div(dcc.Graph(id='fig3_area', figure={}), className='six columns')], className='row'),
                                     html.Br(),
                                     html.Br(),
                                     html.Br(),
                                     html.H6('Genomas sequenciados e depositados em:', style=h6_style2),
                                     html.Div(html.A(href='https://www.gisaid.org/',
                                                     target='_blank',
                                                     children=html.Img(title='GISAID webpage',
                                                                       width=200,
                                                                       alt='GISAID webpage',
                                                                       src='https://github.com/vanleiko/RedeGenomica/blob/main/gisaid-logo.jpg?raw=true')))
                                                                       ]),
                                     dcc.Tab(label='Sorotipos da dengue inferidos por testes de PCR',
                                             style=tab_style,
                                             selected_style=tab_selected_style,
                                             children=[
                                     html.Br(),
                                     html.H5('Selecione a região:', style=h5_style),
                                     html.Div(dcc.Dropdown(id='regiao_pcr_dropdown', options=regiao_dropdown, value='Brasil', clearable=False)),
                                     html.Div([html.Div(dcc.Graph(id='fig_pcr_regiao', figure={}), className='ten columns')], className='row'),
                                     html.Br(),
                                     html.H5('Selecione o estado:', style=h5_style),
                                     html.Div(dcc.Dropdown(id='estado_pcr_dropdown', options=estado_dropdown, value='Acre', clearable=False)),
                                     html.Div([html.Div(dcc.Graph(id='fig_pcr_estado', figure={}), className='ten columns')], className='row')
                                             ])
                                      ])])


### Callback 1 - tipo - Barplot - Região ###
@app.callback(Output(component_id='fig2_barplot', component_property='figure'),
              Input(component_id='regiao_dropdown', component_property='value'),
              Input(component_id='decada_dropdown_regiao', component_property='value'))
def update_regiao_barplot(regiao, decada):
  time.sleep(2)
  anos_lista_regiao = list(range(decada, decada+10))
  if regiao == 'Brasil':
    df_br_fig_barplot = df2_agrupado_periodo_brasil.query('Ano in @anos_lista_regiao')
    df_br_fig_barplot = df_br_fig_barplot.sort_values('Período2')
    fig2_barplot = px.bar(df_br_fig_barplot,
                          x='Período',
                          y='Quantidade',
                          color='Tipo',
                          hover_data={'Tipo': False,
                                      'Período': True,
                                      'Quantidade': True},
                          hover_name='Tipo',
                          color_discrete_map=cor_tipo,
                          category_orders=ordem_tipo,
                          opacity=0.95,
                          title='<b>Brasil</b>',
                          height=450,
                          width=680,)
    fig2_barplot.update_layout(layout_barplot, legend=layout_legenda, legend_title_text=None,
                               margin={'l':0, 'r':0, 't':150, 'b':0})
    fig2_barplot.update_xaxes(nticks=15, tickangle=320, tickfont_size=12,
                              showline=True, linewidth=1, linecolor='#222a2a',
                              categoryorder='array', categoryarray=list(df_br_fig_barplot['Período']),
                              type='category')
    fig2_barplot.update_yaxes(showgrid=True, gridcolor='lightgray',
                              showline=True, linewidth=1, linecolor='#222a2a')
    return fig2_barplot

  else:
    df_regiao_fig_barplot = df2_agrupado_periodo_regiao.query('Região == @regiao and Ano in @anos_lista_regiao')
    if df_regiao_fig_barplot['Ano'].nunique() == 0:
      return fig_nao_ha_dados
    else:
      df_regiao_fig_barplot = df_regiao_fig_barplot.sort_values('Período2')
      fig2_barplot = px.bar(df_regiao_fig_barplot,
                            x='Período',
                            y='Quantidade',
                            color='Tipo',
                            hover_data={'Tipo': False,
                                        'Período': True,
                                        'Quantidade': True},
                            hover_name='Tipo',
                            color_discrete_map=cor_tipo,
                            category_orders=ordem_tipo,
                            opacity=0.95,
                            title=f'<b>{regiao}</b>',
                            height=450,
                            width=680)
      fig2_barplot.update_layout(layout_barplot, legend=layout_legenda, legend_title_text=None,
                               margin={'l':0, 'r':0, 't':150, 'b':0})
      fig2_barplot.update_xaxes(nticks=15, tickangle=320, tickfont_size=12,
                              showline=True, linewidth=1, linecolor='#222a2a',
                              categoryorder='array', categoryarray=list(df_regiao_fig_barplot['Período']),
                              type='category')
      fig2_barplot.update_yaxes(showgrid=True, gridcolor='lightgray',
                                showline=True, linewidth=1, linecolor='#222a2a')

      return fig2_barplot

### Callback 2 - Área - Região ###
@app.callback(Output(component_id='fig2_area', component_property='figure'),
              Input(component_id='regiao_dropdown', component_property='value'),
              Input(component_id='decada_dropdown_regiao', component_property='value'))
def update_regiao_area(regiao, decada):
  time.sleep(2)
  anos_lista_regiao = list(range(decada, decada+10))
  if regiao == 'Brasil':
    df_br_fig_area = df2_agrupado_periodo_brasil.query('Ano in @anos_lista_regiao')
    df_br_fig_area = df_br_fig_area.groupby(['Ano', 'Tipo']).sum().reset_index().sort_values('Ano')
    fig2_area = px.area(df_br_fig_area,
                        x='Ano',
                        y='Quantidade',
                        text='Quantidade',
                        color='Tipo',
                        groupnorm='percent',
                        title='<b>Brasil<b>',
                        color_discrete_map=cor_tipo,
                        category_orders=ordem_tipo,
                        height=450,
                        width=680,
                        line_shape='spline')
    fig2_area.update_layout(layout_area, legend=layout_legenda, legend_title_text=None,
                            hovermode='x unified', margin={'l':0, 'r':0, 't':150, 'b':0})

    fig2_area.update_traces(line=dict(width=0), hovertemplate='%{y:.1f}%', mode='lines')
    fig2_area.update_xaxes(tickangle=320, showgrid=False, tickfont_size=12,
                           showline=True, linewidth=1, linecolor='#222a2a',
                           categoryorder='array', categoryarray=list(df_br_fig_area['Ano']),
                           type='category')
    fig2_area.update_yaxes(range=[0,100], showgrid=True, gridcolor='lightgray',
                           showline=True, linewidth=1, linecolor='#222a2a')
    return fig2_area

  else:
    df_regiao_fig_area = df2_agrupado_periodo_regiao.query('Região == @regiao and Ano in @anos_lista_regiao')
    if df_regiao_fig_area['Ano'].nunique() == 0:
      return fig_nao_ha_dados
    else:
      df_regiao_fig_area = df_regiao_fig_area.groupby(['Ano', 'Tipo']).sum().reset_index().sort_values('Ano')
      fig2_area = px.area(df_regiao_fig_area,
                          x='Ano',
                          y='Quantidade',
                          text='Quantidade',
                          color='Tipo',
                          groupnorm='percent',
                          title=f'<b>{regiao}</b>',
                          color_discrete_map=cor_tipo,
                          category_orders=ordem_tipo,
                          height=450,
                          width=680,
                          line_shape='spline')
      fig2_area.update_layout(layout_area, legend=layout_legenda, legend_title_text=None,
                              hovermode='x unified', margin={'l':0, 'r':0, 't':150, 'b':0})
      fig2_area.update_traces(line=dict(width=0), hovertemplate='%{y:.1f}%', mode='lines')
      fig2_area.update_xaxes(tickangle=320, showgrid=False, tickfont_size=12,
                             showline=True, linewidth=1, linecolor='#222a2a',
                             categoryorder='array', categoryarray=list(df_regiao_fig_area['Ano']),
                             type='category')
      fig2_area.update_yaxes(range=[0,100], showgrid=True, gridcolor='lightgray',
                           showline=True, linewidth=1, linecolor='#222a2a')

      return fig2_area

### Callback 3 - tipo - Barplot - Estado ###
@app.callback(Output(component_id='fig3_barplot', component_property='figure'),
              Input(component_id='estado_dropdown', component_property='value'),
              Input(component_id='decada_dropdown_estado', component_property='value'))
def update_estado_barplot(estado, decada):
  time.sleep(2)
  anos_lista_estado = list(range(decada, decada+10))
  df_estado_fig_barplot = df3_agrupado_periodo_estado.query('Estado == @estado and Ano in @anos_lista_estado')
  if df_estado_fig_barplot['Ano'].nunique() == 0:
    return fig_nao_ha_dados
  else:
    df_estado_fig_barplot = df_estado_fig_barplot.sort_values('Período2')
    fig3_barplot = px.bar(df_estado_fig_barplot,
                          x='Período',
                          y='Quantidade',
                          color='Tipo',
                          hover_data={'Tipo': False,
                                      'Período': True,
                                      'Quantidade': True},
                          hover_name='Tipo',
                          color_discrete_map=cor_tipo,
                          category_orders=ordem_tipo,
                          opacity=0.95,
                          title=f'<b>{estado}</b>',
                          height=450,
                          width=680)
    fig3_barplot.update_layout(layout_barplot, legend=layout_legenda, legend_title_text=None,
                               margin={'l':0, 'r':0, 't':150, 'b':0})
    fig3_barplot.update_xaxes(nticks=15, tickangle=320, tickfont_size=12,
                              showline=True, linewidth=1, linecolor='#222a2a',
                              categoryorder='array', categoryarray=list(df_estado_fig_barplot['Período']),
                              type='category')
    fig3_barplot.update_yaxes(showgrid=True, gridcolor='lightgray',
                              showline=True, linewidth=1, linecolor='#222a2a')

    return fig3_barplot

### Callback 4 - Área - Estado ###
@app.callback(Output(component_id='fig3_area', component_property='figure'),
              Input(component_id='estado_dropdown', component_property='value'),
              Input(component_id='decada_dropdown_estado', component_property='value'))
def update_estado_area(estado, decada):
  time.sleep(2)
  anos_lista_estado = list(range(decada, decada+10))
  df_estado_fig_area = df3_agrupado_periodo_estado.query('Estado == @estado and Ano in @anos_lista_estado')
  if df_estado_fig_area['Ano'].nunique() == 0:
    return fig_nao_ha_dados
  else:
    df_estado_fig_area = df_estado_fig_area.groupby(['Ano', 'Tipo']).sum().reset_index().sort_values('Ano')
    fig3_area = px.area(df_estado_fig_area,
                        x='Ano',
                        y='Quantidade',
                        text='Quantidade',
                        color='Tipo',
                        groupnorm='percent',
                        title=f'<b>{estado}</b>',
                        color_discrete_map=cor_tipo,
                        category_orders=ordem_tipo,
                        height=450,
                        width=680,
                        line_shape='spline')
    fig3_area.update_layout(layout_area, legend=layout_legenda, legend_title_text=None,
                            hovermode='x unified', margin={'l':0, 'r':0, 't':150, 'b':0})
    fig3_area.update_traces(line=dict(width=0), hovertemplate='%{y:.1f}%', mode='lines')
    fig3_area.update_xaxes(tickangle=320, showgrid=False, tickfont_size=12,
                           showline=True, linewidth=1, linecolor='#222a2a',
                           categoryorder='array', categoryarray=list(df_estado_fig_area['Ano']),
                           type='category')
    fig3_area.update_yaxes(range=[0,100], showgrid=True, gridcolor='lightgray',
                           showline=True, linewidth=1, linecolor='#222a2a')

    return fig3_area


### Callback 5 - PCR - Região ###
@app.callback(Output(component_id='fig_pcr_regiao', component_property='figure'),
              Input(component_id='regiao_pcr_dropdown', component_property='value'))
def update_pcr_regiao(regiao):
  time.sleep(2)
  if regiao == 'Brasil':
        return fig_pcr_br
  else:
    df_regiao1_ano, df_regiao2_ano, df_regiao3_ano, df_regiao4_ano = calcula_frequencia_sorotipo(df_pcr_regiao_ano, 'Ano', 'Região', regiao)
    df_regiao1_per, df_regiao2_per, df_regiao3_per, df_regiao4_per = calcula_frequencia_sorotipo(df_pcr_regiao_periodo, 'Período', 'Região', regiao)

    fig_pcr_regiao = make_subplots(specs=[[{"secondary_y": True}]])
    fig_pcr_regiao.add_trace(go.Bar(name='Sorotipo 1',
                                    marker_color='cornflowerblue',
                                    x=df_regiao1_per['Período'],
                                    y=df_regiao1_per['CasosExtrap']),
                              secondary_y=False)
    fig_pcr_regiao.add_trace(go.Bar(name='Sorotipo 2',
                                    marker_color='orange',
                                    x=df_regiao2_per['Período'],
                                    y=df_regiao2_per['CasosExtrap']),
                              secondary_y=False)
    fig_pcr_regiao.add_trace(go.Bar(name='Sorotipo 3',
                                    marker_color='green',
                                    x=df_regiao3_per['Período'],
                                    y=df_regiao3_per['CasosExtrap']),
                              secondary_y=False)
    fig_pcr_regiao.add_trace(go.Bar(name='Sorotipo 4',
                                    marker_color='red',
                                    x=df_regiao4_per['Período'],
                                    y=df_regiao4_per['CasosExtrap']),
                              secondary_y=False)

    # LINHA
    fig_pcr_regiao.add_trace(go.Scatter(showlegend=False,
                                        name='Sorotipo 1',
                                        marker_color='cornflowerblue',
                                        x=df_regiao1_ano['Ano'],
                                        y=df_regiao1_ano['Porcentagem'],
                                        hovertemplate = 'Frequência: %{y}%'),
                              secondary_y=True)
    fig_pcr_regiao.add_trace(go.Scatter(showlegend=False,
                                        name='Sorotipo 2',
                                        marker_color='orange',
                                        x=df_regiao2_ano['Ano'],
                                        y=df_regiao2_ano['Porcentagem'],
                                        hovertemplate = 'Frequência: %{y}%'),
                              secondary_y=True)
    fig_pcr_regiao.add_trace(go.Scatter(showlegend=False,
                                        name='Sorotipo 3',
                                        marker_color='green',
                                        x=df_regiao3_ano['Ano'],
                                        y=df_regiao3_ano['Porcentagem'],
                                        hovertemplate = 'Frequência: %{y}%'),
                              secondary_y=True)
    fig_pcr_regiao.add_trace(go.Scatter(showlegend=False,
                                        name='Sorotipo 4',
                                        marker_color='red',
                                        x=df_regiao4_ano['Ano'],
                                        y=df_regiao4_ano['Porcentagem'],
                                        hovertemplate = 'Frequência: %{y}%'),
                              secondary_y=True)
    fig_pcr_regiao.update_layout(barmode='stack',
                                 legend_font_size=16,
                                 legend_traceorder='normal',
                                 legend_orientation='h',
                                 legend_xanchor = 'center',
                                 legend_yanchor = 'bottom',
                                 legend_x= 0.5, legend_y= 1.0,
                                 plot_bgcolor='white',
                                 title_text=f'{regiao}',
                                 xaxis_title='Período de amostragem',
                                 yaxis_title='Casos de dengue',)
    fig_pcr_regiao.update_xaxes(showline=True, linewidth=1.5, linecolor='lightgray')
    fig_pcr_regiao.update_yaxes(showline=True, linewidth=1.5, linecolor='lightgray', secondary_y=False)
    fig_pcr_regiao.update_yaxes(secondary_y=True, showline=True, linewidth=1.5, linecolor='lightgray',
                                title_text='Sorotipos (%)', rangemode='tozero', range=[0,100])

    return fig_pcr_regiao

### Callback 6 - PCR - Estado ###
@app.callback(Output(component_id='fig_pcr_estado', component_property='figure'),
              Input(component_id='estado_pcr_dropdown', component_property='value'))
def update_pcr_estado(estado):
  time.sleep(2)
  df_estado1_ano, df_estado2_ano, df_estado3_ano, df_estado4_ano = calcula_frequencia_sorotipo(df_pcr_estado_ano, 'Ano', 'Estado', estado)
  df_estado1_per, df_estado2_per, df_estado3_per, df_estado4_per = calcula_frequencia_sorotipo(df_pcr_estado_periodo, 'Período', 'Estado', estado)

  fig_pcr_estado = make_subplots(specs=[[{"secondary_y": True}]])
  fig_pcr_estado.add_trace(go.Bar(name='Sorotipo 1',
                                  marker_color='cornflowerblue',
                                  x=df_estado1_per['Período'],
                                  y=df_estado1_per['CasosExtrap']),
                           secondary_y=False)
  fig_pcr_estado.add_trace(go.Bar(name='Sorotipo 2',
                                  marker_color='orange',
                                  x=df_estado2_per['Período'],
                                  y=df_estado2_per['CasosExtrap']),
                              secondary_y=False)
  fig_pcr_estado.add_trace(go.Bar(name='Sorotipo 3',
                                  marker_color='green',
                                  x=df_estado3_per['Período'],
                                  y=df_estado3_per['CasosExtrap']),
                           secondary_y=False)
  fig_pcr_estado.add_trace(go.Bar(name='Sorotipo 4',
                                  marker_color='red',
                                  x=df_estado4_per['Período'],
                                  y=df_estado4_per['CasosExtrap']),
                           secondary_y=False)

    # LINHA
  fig_pcr_estado.add_trace(go.Scatter(showlegend=False,
                                      name='Sorotipo 1',
                                      marker_color='cornflowerblue',
                                      x=df_estado1_ano['Ano'],
                                      y=df_estado1_ano['Porcentagem'],
                                      hovertemplate = 'Frequência: %{y}%'),
                           secondary_y=True)
  fig_pcr_estado.add_trace(go.Scatter(showlegend=False,
                                      name='Sorotipo 2',
                                      marker_color='orange',
                                      x=df_estado2_ano['Ano'],
                                      y=df_estado2_ano['Porcentagem'],
                                      hovertemplate = 'Frequência: %{y}%'),
                           secondary_y=True)
  fig_pcr_estado.add_trace(go.Scatter(showlegend=False,
                                      name='Sorotipo 3',
                                      marker_color='green',
                                      x=df_estado3_ano['Ano'],
                                      y=df_estado3_ano['Porcentagem'],
                                      hovertemplate = 'Frequência: %{y}%'),
                           secondary_y=True)
  fig_pcr_estado.add_trace(go.Scatter(showlegend=False,
                                      name='Sorotipo 4',
                                      marker_color='red',
                                      x=df_estado4_ano['Ano'],
                                      y=df_estado4_ano['Porcentagem'],
                                      hovertemplate = 'Frequência: %{y}%'),
                           secondary_y=True)
  fig_pcr_estado.update_layout(barmode='stack',
                               legend_font_size=16,
                               legend_traceorder='normal',
                               legend_orientation='h',
                               legend_xanchor = 'center',
                               legend_yanchor = 'bottom',
                               legend_x= 0.5, legend_y= 1.0,
                               plot_bgcolor='white',
                               title_text=f'{estado}',
                               xaxis_title='Período de amostragem',
                               yaxis_title='Casos de dengue',)
  fig_pcr_estado.update_xaxes(showline=True, linewidth=1.5, linecolor='lightgray')
  fig_pcr_estado.update_yaxes(showline=True, linewidth=1.5, linecolor='lightgray', secondary_y=False)
  fig_pcr_estado.update_yaxes(secondary_y=True, showline=True, linewidth=1.5, linecolor='lightgray',
                              title_text='Sorotipos (%)', rangemode='tozero', range=[0,100])

  return fig_pcr_estado

if __name__ == '__main__':
  app.run_server(debug=False)