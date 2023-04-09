

from dash import Dash, dcc, html, dash_table
from dash.dependencies import Input, Output
import dash_auth
import pandas 

from reading_database import read_database
from rsiandsymbols import get_symbols, rsi_tool
from falk_str import inc_dec

from twitter_collection import reading_tweets

import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
import pandas as pd

from datetime import datetime
import time
import mysql
from mysql.connector import Error
import dash_daq as daq
import yfinance as yf
import pandas_ta as pta


from Bollinger_Band import bb,implement_bb_strategy, my_bb, sma
#from BB import bb, sma, implement_bb_strategy, my_bb
#import BB
import plotly.graph_objs as go
import fear_and_greed



# database 

def connection_to_database():
    server = "analysis-tool-nonprod.c4rbkrjinf7p.eu-central-1.rds.amazonaws.com" # replace with your server name
    database = "stocks-dev" # replace with your database name
    username = "admin" # replace with your username
    password = "nCk8Ll42KcLU5KdX631L" # replace with your password
    connection = mysql.connector.connect(host = server, user = username,password = password,database = database)
    
    cursor = connection.cursor()
    return connection


def read_query(query):
    connection =  connection_to_database()
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as err:
        print(f"Error: '{err}'")


    
results = read_query(''' SELECT * FROM dashaccount''')
username = results[0][0]
password =  results[0][1]



# df_master = read_database()
# df_master['points'] = df_master['dividend'] + df_master['high_growth'] + df_master['leverman']
# df_m1 = df_master



# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#DSatabase
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


# database initialization
def execute_query(connection, query):
      cursor = connection.cursor()
      try:
          print("execute")
          cursor.execute(query)
          print("before cimmit")
          connection.commit()
          print("Query successful")
      except Error as err:
          print(f"Error: '{err}'")

#globally aalled data base function
# df_m1, df_master = collect_data()

# def database_insetion():
    
#     create_stock_table = """
#       CREATE TABLE  stocklist_with_features (
#         stock_id INT PRIMARY KEY AUTO_INCREMENT,
#         stockname VARCHAR(200),
#         dividend INT ,
#         high_growth INT ,
#         leverman INT ,
#         P_E_from_aktien_gude INT,
#         points INT,
#         symbols VARCHAR(50),
#         Indexes VARCHAR(100),
#         stock_date DATE,
#         RSI_signal VARCHAR(50),
#         BB_signal VARCHAR(50),
#         Sentiments VARCHAR(100)
#         );
#       """
#     connection = connection_to_database()
#     cursor = connection.cursor()
#     print("before execution")
#     execute_query(connection, create_stock_table) # Execute our defined query
#     print("after execution")
   
#     for row in df_with_sentiments1.itertuples():
#           stockname = row[1]
#           dividend = row[2]
#           high_growth = row[3]
#           leverman = row[4]
#           P_E_from_aktien_gude = row[5]
#           points = row[6]
#           symbols = row[7]
#           Indexes = row[8]
#           datetimelist = row[9]
#           RSI_signal = row[10]
#           BB_signal  = row[11]
#           Sentiments = row[12]
         
#           pop_stocks = "INSERT INTO `stocklist_with_features` (`stockname`, `dividend`, `high_growth`, `leverman`, `P_E_from_aktien_gude`, `points`, `symbols`, `Indexes`,`stock_date`, `RSI_signal`, `BB_signal`,`Sentiments`) VALUES (%s, %s,%s, %s, %s, %s, %s, %s, %s,%s,%s,%s)"
#           cursor.execute(pop_stocks,(stockname,dividend,high_growth,leverman,P_E_from_aktien_gude,points,symbols, Indexes, datetimelist, RSI_signal,BB_signal, Sentiments))
#     connection.commit()  


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#Database Reading 
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


def read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as err:
        print(f"Error: '{err}'")
        

def read_database2():
    q1 = """
    SELECT *
    FROM stocklist_with_features; """
    conn = connection_to_database()
    results = read_query(conn, q1)
    df_from_database = pd.DataFrame()
    df_database = pd.DataFrame.from_records(results, columns=['stock_id','stockname', 'dividend', 'high_growth', 'leverman', 'P_E_from_aktien_gude', 'points', 'symbols', 'Indexes' ,'stock_date','RSI_signal','BB_signal', 'Sentiments'])
    return df_database

df_master = read_database2()
df_m1 = df_master

# reading dataframes to visualize the results of indexes

df_1 = df_master[df_master['Indexes']=="DAX"]
df_2= df_master[df_master['Indexes']=="MDAX"]
df_3= df_master[df_master['Indexes']=="SDAX"]
df_4= df_master[df_master['Indexes']=="TecDAX"]
df_5= df_master[df_master['Indexes']=="CDAX"]
df_6= df_master[df_master['Indexes']=="Scale"]
df_7 =df_master[df_master['Indexes']=="Dow-Jones"]
df_14 =df_master[df_master['Indexes']=="EURO-STOXX-50"]
df_15 = df_master[df_master['Indexes']=="STOXX-Europe-600"]

# welt calculation
dd1 = df_7.append(df_14, ignore_index=True)
df_welt = dd1.append(df_15, ignore_index=True)

#calculation of deu
df_d1  = df_1.append(df_2, ignore_index=True)
df_d2 = df_d1.append(df_3, ignore_index=True)
df_d3 = df_d2.append(df_4, ignore_index=True)
df_deu = df_d3.append(df_5, ignore_index=True) 

#df_master 
#df_master1 = df_deu.append(df_welt, ignore_index=True)
df_m2 = df_master[df_master['points']>20] 

# get symbols. 

# df_m2_symbols = get_symbols(df_m2) 

# df_m2_symbols=df_m2.loc[(df_m2_symbols['symbols'] != "CINERAD.BO") & (df_m2_symbols['symbols'] != "CCR-WI") & (df_m2_symbols['symbols'] != "FC9.MU")& (df_m2_symbols['symbols'] != "CR-WI")& (df_m2_symbols['symbols'] != "0GRX.L")]

# #df_m2_symbols = df_m2_symbols[(df_m2_symbols['symbols']!="CINERAD.BO") and (df_m2_symbols['symbols']!="CCR-WI")]
# # rsi 

# df_with_rsi = rsi_tool(df_m2_symbols)


df_with_rsi = df_master.iloc[:, [1,2,3,4,7,8,9,5,6,10]]

df_with_BB = df_master.iloc[:, [1,2,3,4,7,8,9,5,6,11]]

df_with_sentiments = df_master.iloc[:, [1,2,3,4,7,8,9,5,6,12]]

df_with_sentiments1 = df_master


# # remove 
# # BB 

# df_with_BB = my_bb(df_with_rsi)

# # sentiments

# df_with_sentiments = reading_tweets(df_with_BB)
# # insert into database 


# df_with_sentiments1 = df_with_sentiments.iloc[:, [1,2,3,4,7,8,9,5,6,11,12,13]]

# database_insetion()

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#Dash Board 
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++




app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

auth = dash_auth.BasicAuth(app, {
    username : password
})

tabs_styles = {
    'height': '30px',
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold',
  #  'postion' : 'relative'
    
    
}




tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    'color': 'yellow',
    'padding': '4px',
    
}

# styling the sidebar
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "10rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
    "clear" : "both",
#    'overflow-x': 'auto'
    
}

# padding for the page content
CONTENT_STYLE = {
    "margin-left": "6rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
   
}



sidebar = html.Div(
    [
        html.H2("Welcome Falk!", className="display-8"),
        html.Hr(),
        html.P(
            "Functinality to use", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("1d and 7d RSI", href="/rsi", active="exact"),
                dbc.NavLink("1d and 7d BB", href="/bb", active="exact"),
                dbc.NavLink("Sentiments", href="/sentiments", active="exact"),
                dbc.NavLink("feargreedindex", href="/feargreedindex", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

def get_label(value):
    label = ''
    #for k, v in labels.items():
    if ((value>0) and (value<21)):
        label = "ExtremeFear"
    elif ((value>21) and (value<41)):
        label = "Fearful"
    elif ((value>41) and (value<61)):
        label = "Neutral"
    elif ((value>61) and (value<80)):
        label = "Greed"
    elif (value>80):
        label = "Fearful"
    return label

labels = {
    '0': 'Extreme Fear',
    '20': 'Fearful',
    '40': 'Neutral',
    '60': 'Greed',
    '80': 'Extreme Greed'
}

# stock_tabs = html.Div(
#     [
#         dcc.Tabs(id="tabs-styled-with-inline", value='tab-1', children=[
#         dcc.Tab(label='Master', value='tab-master', style=tab_style, selected_style=tab_selected_style),
#         dcc.Tab(label='Deutschland', value='tab-deu', style=tab_style, selected_style=tab_selected_style),
#         dcc.Tab(label='DAX', value='tab-1', style=tab_style, selected_style=tab_selected_style),
#         dcc.Tab(label='MDAX', value='tab-2', style=tab_style, selected_style=tab_selected_style),
#         dcc.Tab(label='SDAX', value='tab-3', style=tab_style, selected_style=tab_selected_style),
#         dcc.Tab(label='TecDAX', value='tab-4', style=tab_style, selected_style=tab_selected_style),
#         dcc.Tab(label='CDAX', value='tab-5', style=tab_style, selected_style=tab_selected_style),
#         dcc.Tab(label='Scale', value='tab-6', style=tab_style, selected_style=tab_selected_style),
#         dcc.Tab(label='Welt', value='tab-welt', style=tab_style, selected_style=tab_selected_style),
#         dcc.Tab(label='DOW', value='tab-7', style=tab_style, selected_style=tab_selected_style),
#         dcc.Tab(label='EuroStoxx50', value='tab-14', style=tab_style, selected_style=tab_selected_style),
#         dcc.Tab(label='Stocks50:600', value='tab-15', style=tab_style, selected_style=tab_selected_style),
#         dcc.Tab(label='Sorted Results', value='tab-s', style=tab_style, selected_style=tab_selected_style)

#         ], style=tabs_styles),
#         html.Div(id='tabs-content-inline'), 
#   ], style = {'width':'auto', 'position': 'absolute'})

content = html.Div(id="page-content", children=[], style=CONTENT_STYLE)

# Fear and Greed Index Gauge
fig = go.Figure(go.Indicator(
    mode = "gauge+number",
    value = fear_and_greed.get()[0],
    #title = {'text': "Fear and Greed Index"},
    gauge = {
        'axis': {'range': [0, 100], 'tickwidth': 1},
        'bar': {'color': "darkblue"},
        'steps': [
            {'range': [0, 20], 'color': "red"},
            {'range': [20, 40], 'color': "orange"},
            {'range': [40, 60], 'color': "yellow"},
            {'range': [60, 80], 'color': "lightgreen"},
            {'range': [80, 100], 'color': "green"}],
        'threshold': {
            'line': {'color': "red", 'width': 4},
            'thickness': 0.75,
            'value': 90}
        }
    ))

# Add the label to the gauge chart
fig.update_layout(
    annotations=[{
        'x': 0.5,
        'y': 0.4,
        'text': get_label(fear_and_greed.get()[0]),
        'showarrow': True,
        'font': {'size': 20}
    }]
)




app.layout = html.Div([
    
        dcc.Location(id="url"),
        sidebar,
       # stock_tabs,
        content
        
])

@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")]
)
def render_page_content(pathname):
    if pathname == "/":
        return [
               
            
                html.Div([   
                html.H1('All data with tabs from database',
                        style={'textAlign':'center'}),
                html.Div(
                [
                    dcc.Tabs(id="tabs-styled-with-inline", value='tab-1', children=[
                    dcc.Tab(label='Master', value='tab-master', style=tab_style, selected_style=tab_selected_style),
                    dcc.Tab(label='Deutschland', value='tab-deu', style=tab_style, selected_style=tab_selected_style),
                    dcc.Tab(label='DAX', value='tab-1', style=tab_style, selected_style=tab_selected_style),
                    dcc.Tab(label='MDAX', value='tab-2', style=tab_style, selected_style=tab_selected_style),
                    dcc.Tab(label='SDAX', value='tab-3', style=tab_style, selected_style=tab_selected_style),
                    dcc.Tab(label='TecDAX', value='tab-4', style=tab_style, selected_style=tab_selected_style),
                    dcc.Tab(label='CDAX', value='tab-5', style=tab_style, selected_style=tab_selected_style),
                    dcc.Tab(label='Scale', value='tab-6', style=tab_style, selected_style=tab_selected_style),
                    dcc.Tab(label='Welt', value='tab-welt', style=tab_style, selected_style=tab_selected_style),
                    dcc.Tab(label='DOW', value='tab-7', style=tab_style, selected_style=tab_selected_style),
                    dcc.Tab(label='EuroStoxx50', value='tab-14', style=tab_style, selected_style=tab_selected_style),
                    dcc.Tab(label='Stocks50:600', value='tab-15', style=tab_style, selected_style=tab_selected_style),
                    dcc.Tab(label='Sorted Results', value='tab-s', style=tab_style, selected_style=tab_selected_style),
                    

                    ], style=tabs_styles),
                    html.Div(id='tabs-content-inline'),
                    
              ], style = {'width':'auto', 'float':'right'})
         ], style = {'width': 'auto'}),
                # download button
               
                    
               
            ]    
    
    elif pathname == "/rsi":
        return [
                html.H1('Single Dataframe',
                        style={'textAlign':'center'}),
                
                html.Div([
                    html.Div([
                    daq.ToggleSwitch(
                        label = "RSI",
                        id='my-toggle-switch',
                        value=False
                    ),
                    html.Div(id='my-toggle-switch-output'),
                    
                ], className="row",),
                    
             
                dash_table.DataTable(df_with_rsi.to_dict('records'),columns =[{"name": i, "id": i} for i in df_with_rsi.columns],id='tb_m1',
                                      style_data_conditional = [{
                                           'if': {
                                               'filter_query': '{points} > 19',
                                           },
                                           'backgroundColor': 'green',  
                                           'color': 'black'
                                       },
                                           {
                                           # 'if': {
                                           #     'filter_query': '{points} <19  && {points} > 13',
                                           # },
                                           'if': {
                                               'filter_query': '{dividend} > 9',
                                               'column_id' : 'dividend'
                                           },
                                               
                                           'backgroundColor': 'yellow',
                                           'color': 'black'
                                       },
                                           
                                         {  
                                               'if': {
                                               'filter_query': '{high_growth} > 9',
                                               'column_id' : 'high_growth'
                                           },
                                             
                                         
                                               
                                           'backgroundColor': 'yellow',
                                           'color': 'black'
                                       },
                                           
                                           {  
                                               'if': {
                                               'filter_query': '{leverman} > 2',
                                               'column_id' : 'leverman'
                                           },
                                             
                                         
                                               
                                           'backgroundColor': 'yellow',
                                           'color': 'black'
                                       },
                                           
                                           
                                           { 
                                           'if': {
                                               'filter_query': '{points} <13',
                                           },
                                           'backgroundColor': 'red',
                                           'color': 'black'
                                       },
                                           
                                       ],style_table={'overflowX': 'scroll'})    
             ],style={'width':1200, 'float':'right'}),
                 
                 
            

            
            ]
          
    elif pathname == "/bb":
        return [
                html.H1('With only Bollinger Band Signal',
                        style={'textAlign':'center'}),
                
                html.Div([
                    html.Div([
                    daq.ToggleSwitch(
                        label = "Current Bollinger Band of 1 day ",
                        id='my-toggle-switch_b',
                        value=False
                    ),
                    html.Div(id='my-toggle-switch-output_b'),
                    
                ], className="row",),
                    
             
                dash_table.DataTable(df_with_BB.to_dict('records'),columns =[{"name": i, "id": i} for i in df_with_BB.columns],id='tb_m1',
                                      style_data_conditional = [{
                                           'if': {
                                               'filter_query': '{points} > 19',
                                           },
                                           'backgroundColor': 'green',  
                                           'color': 'black'
                                       },
                                           {
                                           # 'if': {
                                           #     'filter_query': '{points} <19  && {points} > 13',
                                           # },
                                           'if': {
                                               'filter_query': '{dividend} > 9',
                                               'column_id' : 'dividend'
                                           },
                                               
                                           'backgroundColor': 'yellow',
                                           'color': 'black'
                                       },
                                           
                                         {  
                                               'if': {
                                               'filter_query': '{high_growth} > 9',
                                               'column_id' : 'high_growth'
                                           },
                                             
                                         
                                               
                                           'backgroundColor': 'yellow',
                                           'color': 'black'
                                       },
                                           
                                           {  
                                               'if': {
                                               'filter_query': '{leverman} > 2',
                                               'column_id' : 'leverman'
                                           },
                                             
                                         
                                               
                                           'backgroundColor': 'yellow',
                                           'color': 'black'
                                       },
                                           
                                           
                                           { 
                                           'if': {
                                               'filter_query': '{points} <13',
                                           },
                                           'backgroundColor': 'red',
                                           'color': 'black'
                                       },
                                           
                                       ],style_table={'overflowX': 'scroll'})    
             ],style={'width':1200, 'float':'right'}),
                 
            
            ]
      
   
    elif pathname == "/sentiments":
        return [
                html.H1('With only twitter',
                        style={'textAlign':'center'}),
                
                html.Div([
                    html.Div([
                    daq.ToggleSwitch(
                        label = "Current twitter tweets ",
                        id='my-toggle-switch_t',
                        value=False
                    ),
                    html.Div(id='my-toggle-switch-output_t'),
                    
                ], className="row",),
                    
             
                dash_table.DataTable(df_with_sentiments.to_dict('records'),columns =[{"name": i, "id": i} for i in df_with_sentiments.columns],id='tb_m1',
                                      style_data_conditional = [{
                                           'if': {
                                               'filter_query': '{points} > 19',
                                           },
                                           'backgroundColor': 'green',  
                                           'color': 'black'
                                       },
                                           {
                                           # 'if': {
                                           #     'filter_query': '{points} <19  && {points} > 13',
                                           # },
                                           'if': {
                                               'filter_query': '{dividend} > 9',
                                               'column_id' : 'dividend'
                                           },
                                               
                                           'backgroundColor': 'yellow',
                                           'color': 'black'
                                       },
                                           
                                         {  
                                               'if': {
                                               'filter_query': '{high_growth} > 9',
                                               'column_id' : 'high_growth'
                                           },
                                             
                                         
                                               
                                           'backgroundColor': 'yellow',
                                           'color': 'black'
                                       },
                                           
                                           {  
                                               'if': {
                                               'filter_query': '{leverman} > 2',
                                               'column_id' : 'leverman'
                                           },
                                             
                                         
                                               
                                           'backgroundColor': 'yellow',
                                           'color': 'black'
                                       },
                                           
                                           
                                           { 
                                           'if': {
                                               'filter_query': '{points} <13',
                                           },
                                           'backgroundColor': 'red',
                                           'color': 'black'
                                       },
                                           
                                       ],style_table={'overflowX': 'scroll'})    
             ],style={'width':1200, 'float':'right'}),
                 
            
            ]
    
    
    
    
    
    
    
    
    elif pathname == "/feargreedindex":
        
        return [
                html.H1('Fear and Greed Index',
                        style={'textAlign':'center'}),
                        
           html.Div([
            html.Div([
            dcc.Graph(
                id='gauge-chart',
                figure=fig,
                config={'displayModeBar': False}
            ), 
            html.Div([
                html.H1("Fear and Greed Index")
            ], style = {'text-align': 'center'}),
         html.Div([
                html.Table(
            # Create a new row for each key-value pair in the dictionary
            [html.Tr([html.Th(key), html.Td(value)]) for key, value in labels.items()]
        )
            ], style = {'float': 'right', 'width':'auto'}),
            
        ])
        ],style = {'width': 1200, 'float': 'right'})
                
                
                
                ]
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )

@app.callback(Output('tabs-content-inline', 'children'),
              Input('tabs-styled-with-inline', 'value'))


def render_content(tab):
    
    
    
    if tab == 'tab-1':
        return html.Div([
            dash_table.DataTable(df_1.to_dict('records'),[{"name": i, "id": i} for i in df_1.columns], id='tb1',
                                 style_data_conditional = [
                                     {
                                     'if': {
                                         'filter_query': '{points} > 19',
                                     },
                                     'backgroundColor': 'green',
                                     'color': 'black'
                                 },
                                     {
                                     'if': {
                                         'filter_query': '{points} <19  && {points} > 13',
                                     },
                                     'backgroundColor': 'yellow',
                                     'color': 'black'
                                 },
                                     {
                                     'if': {
                                         'filter_query': '{points} <13',
                                     },
                                     'backgroundColor': 'red',
                                     'color': 'black'
                                 },
                                     
                                 ],style_table={'overflowX': 'scroll'})
       ], style = {'width': 1200})        
    elif tab == 'tab-2':
        return html.Div([
            dash_table.DataTable(df_2.to_dict('records'),[{"name": i, "id": i} for i in df_2.columns], id='tb2',
                                 style_data_conditional = [
                                     {
                                     'if': {
                                         'filter_query': '{points} > 19',
                                     },
                                     'backgroundColor': 'green',
                                     'color': 'black'
                                 },
                                     {
                                     'if': {
                                         'filter_query': '{points} <19  && {points} > 13',
                                     },
                                     'backgroundColor': 'yellow',
                                     'color': 'black'
                                 },
                                     {
                                     'if': {
                                         'filter_query': '{points} <13',
                                     },
                                     'backgroundColor': 'red',
                                     'color': 'black'
                                 },
                                     
                                 ],style_table={'overflowX': 'scroll'})
       ], style = {'width': 1200})        
    elif tab == 'tab-3':
        return html.Div([
            dash_table.DataTable(df_3.to_dict('records'),[{"name": i, "id": i} for i in df_3.columns], id='tb3',
                                 style_data_conditional = [
                                     {
                                     'if': {
                                         'filter_query': '{points} > 19',
                                     },
                                     'backgroundColor': 'green',
                                     'color': 'black'
                                 },
                                     {
                                     'if': {
                                         'filter_query': '{points} <19  && {points} > 13',
                                     },
                                     'backgroundColor': 'yellow',
                                     'color': 'black'
                                 },
                                     {
                                     'if': {
                                         'filter_query': '{points} <13',
                                     },
                                     'backgroundColor': 'red',
                                     'color': 'black'
                                 },
                                     
                                 ],style_table={'overflowX': 'scroll'})
       ], style = {'width': 1200})        
    elif tab == 'tab-4':
        return html.Div([
            dash_table.DataTable(df_4.to_dict('records'),[{"name": i, "id": i} for i in df_4.columns], id='tb4',
                                 style_data_conditional = [
                                     {
                                     'if': {
                                         'filter_query': '{points} > 19',
                                     },
                                     'backgroundColor': 'green',
                                     'color': 'black'
                                 },
                                     {
                                     'if': {
                                         'filter_query': '{points} <19  && {points} > 13',
                                     },
                                     'backgroundColor': 'yellow',
                                     'color': 'black'
                                 },
                                     {
                                     'if': {
                                         'filter_query': '{points} <13',
                                     },
                                     'backgroundColor': 'red',
                                     'color': 'black'
                                 },
                                     
                                 ],style_table={'overflowX': 'scroll'})
       ], style = {'width': 1200})        
    elif tab == 'tab-5':
        return html.Div([
            dash_table.DataTable(df_5.to_dict('records'),[{"name": i, "id": i} for i in df_5.columns], id='tb5',
                                 style_data_conditional = [
                                     {
                                     'if': {
                                         'filter_query': '{points} > 19',
                                     },
                                     'backgroundColor': 'green',
                                     'color': 'black'
                                 },
                                     {
                                     'if': {
                                         'filter_query': '{points} <19  && {points} > 13',
                                     },
                                     'backgroundColor': 'yellow',
                                     'color': 'black'
                                 },
                                     {
                                     'if': {
                                         'filter_query': '{points} <13',
                                     },
                                     'backgroundColor': 'red',
                                     'color': 'black'
                                 },
                                     
                                 ],style_table={'overflowX': 'scroll'})
       ], style = {'width': 1200})        
    
    elif tab == 'tab-6':
        return html.Div([
            dash_table.DataTable(df_6.to_dict('records'),[{"name": i, "id": i} for i in df_6.columns], id='tb6',
                                 style_data_conditional = [
                                     {
                                     'if': {
                                         'filter_query': '{points} > 19',
                                     },
                                     'backgroundColor': 'green',
                                     'color': 'black'
                                 },
                                     {
                                     'if': {
                                         'filter_query': '{points} <19  && {points} > 13',
                                     },
                                     'backgroundColor': 'yellow',
                                     'color': 'black'
                                 },
                                     {
                                     'if': {
                                         'filter_query': '{points} <13',
                                     },
                                     'backgroundColor': 'red',
                                     'color': 'black'
                                 },
                                     
                                 ],style_table={'overflowX': 'scroll'})
       ], style = {'width': 1200})        
    elif tab == 'tab-welt':
        return html.Div([
            dash_table.DataTable(df_welt.to_dict('records'),[{"name": i, "id": i} for i in df_welt.columns], id='tb-welt',
                                 style_data_conditional = [
                                     {
                                     'if': {
                                         'filter_query': '{points} > 19',
                                     },
                                     'backgroundColor': 'green',
                                     'color': 'black'
                                 },
                                     {
                                     'if': {
                                         'filter_query': '{points} <19  && {points} > 13',
                                     },
                                     'backgroundColor': 'yellow',
                                     'color': 'black'
                                 },
                                     {
                                     'if': {
                                         'filter_query': '{points} <13',
                                     },
                                     'backgroundColor': 'red',
                                     'color': 'black'
                                 },
                                     
                                 ],style_table={'overflowX': 'scroll'})
       ], style = {'width': 1200})        

    elif tab == 'tab-7':
        return html.Div([
            dash_table.DataTable(df_7.to_dict('records'),[{"name": i, "id": i} for i in df_7.columns], id='tb7', 
                                 style_data_conditional = [
                                     {
                                     'if': {
                                         'filter_query': '{points} > 19',
                                     },
                                     'backgroundColor': 'green',
                                     'color': 'black'
                                 },
                                     {
                                     'if': {
                                         'filter_query': '{points} <19  && {points} > 13',
                                     },
                                     'backgroundColor': 'yellow',
                                     'color': 'black'
                                 },
                                     {
                                     'if': {
                                         'filter_query': '{points} <13',
                                     },
                                     'backgroundColor': 'red',
                                     'color': 'black'
                                 },
                                     
                                 ],style_table={'overflowX': 'scroll'})
       ], style = {'width': 1200})        


                                 
    elif tab == 'tab-14':
        return html.Div([
            dash_table.DataTable(df_14.to_dict('records'),[{"name": i, "id": i} for i in df_14.columns], id='tb14',
                                 style_data_conditional = [
                                     {
                                     'if': {
                                         'filter_query': '{points} > 19',
                                     },
                                     'backgroundColor': 'green',
                                     'color': 'black'
                                 },
                                     {
                                     'if': {
                                         'filter_query': '{points} <19  && {points} > 13',
                                     },
                                     'backgroundColor': 'yellow',
                                     'color': 'black'
                                 },
                                     {
                                     'if': {
                                         'filter_query': '{points} <13',
                                     },
                                     'backgroundColor': 'red',
                                     'color': 'black'
                                 },
                                     
                                 ],style_table={'overflowX': 'scroll'})
       ], style = {'width': 1200})        

                                 
                                 
    elif tab == 'tab-15':
        return html.Div([
            dash_table.DataTable(df_15.to_dict('records'),[{"name": i, "id": i} for i in df_15.columns], id='tb15',style_data_conditional = [
                              {
                              'if': {
                                  'filter_query': '{points} > 19',
                              },
                              'backgroundColor': 'green',
                              'color': 'black'
                          },
                              {
                              'if': {
                                  'filter_query': '{points} <19  && {points} > 13',
                              },
                              'backgroundColor': 'yellow',
                              'color': 'black'
                          },
                              {
                              'if': {
                                  'filter_query': '{points} <13',
                              },
                              'backgroundColor': 'red',
                              'color': 'black'
                          },
                              
                          ],style_table={'overflowX': 'scroll'})
], style = {'width': 1200})        


    elif tab == 'tab-deu':
        return html.Div([
            dash_table.DataTable(df_deu.to_dict('records'),[{"name": i, "id": i} for i in df_deu.columns], id='tb_deu', 
                            style_data_conditional = [
                                {
                                'if': {
                                    'filter_query': '{points} > 19',
                                },
                                'backgroundColor': 'green',
                                'color': 'black'
                            },
                                {
                                'if': {
                                    'filter_query': '{points} <19  && {points} > 13',
                                },
                                'backgroundColor': 'yellow',
                                'color': 'black'
                            },
                                {
                                'if': {
                                    'filter_query': '{points} <13',
                                },
                                'backgroundColor': 'red',
                                'color': 'black'
                            },
                                
                            ],style_table={'overflowX': 'scroll'})
  ], style = {'width': 1200})        

                                 
                                      
    elif tab == 'tab-master':
        return html.Div([
            dash_table.DataTable(df_master.to_dict('records'),columns =[{"name": i, "id": i} for i in df_master.columns],id='tb_master',
                                  style_data_conditional = [
                                      {
                                      'if': {
                                          'filter_query': '{points} > 19',
                                      },
                                      'backgroundColor': 'green',
                                      'color': 'black'
                                  },
                                      {
                                      'if': {
                                          'filter_query': '{points} <19  && {points} > 13',
                                      },
                                      'backgroundColor': 'yellow',
                                      'color': 'black'
                                  },
                                      {
                                      'if': {
                                          'filter_query': '{points} <13',
                                      },
                                      'backgroundColor': 'red',
                                      'color': 'black'
                                  },
                                      
                                  ],style_table={'overflowX': 'scroll'})
        ], style = {'width': 1200})        
      
    elif tab == 'tab-s':
        return html.Div([
            dash_table.DataTable(df_with_sentiments1.to_dict('records'),columns =[{"name": i, "id": i} for i in df_with_sentiments1.columns],id='tb_m1',
                                 style_data_conditional = [{
                                      'if': {
                                          'filter_query': '{points} > 19',
                                      },
                                      'backgroundColor': 'green',
                                      'color': 'black'
                                  },
                                      {
                                      # 'if': {
                                      #     'filter_query': '{points} <19  && {points} > 13',
                                      # },
                                      'if': {
                                          'filter_query': '{dividend} > 9',
                                          'column_id' : 'dividend'
                                      },
                                          
                                      'backgroundColor': 'yellow',
                                      'color': 'black'
                                  },
                                      
                                    {  
                                          'if': {
                                          'filter_query': '{high_growth} > 9',
                                          'column_id' : 'high_growth'
                                      },
                                        
                                    
                                          
                                      'backgroundColor': 'yellow',
                                      'color': 'black'
                                  },
                                      
                                      {  
                                          'if': {
                                          'filter_query': '{leverman} > 1',
                                          'column_id' : 'leverman'
                                      },
                                        
                                    
                                          
                                      'backgroundColor': 'yellow',
                                      'color': 'black'
                                  },
                                      
                                      
                                      { 
                                      'if': {
                                          'filter_query': '{points} <13',
                                      },
                                      'backgroundColor': 'red',
                                      'color': 'black'
                                  },
                                      
                                  ],style_table={'overflowX': 'scroll'}) ,
       # download button
       html.Div([
           dbc.Button(id ='btn_csv', children = [html.I(className="fa fa-download mr-1"), "Download"],
                      color = "info", 
                      className = "mt-1"
                      ),
           dcc.Download(id="download-dataframe-csv")
           
           ], style={'width':'auto', 'float':'right'}) 
       
        ],style={'width':1200})     


    
@app.callback(
    Output("download-dataframe-csv", "data"),
    Input("btn_csv", "n_clicks"),
    prevent_initial_call=True,
)
def func(n_clicks):
    return dcc.send_data_frame(df_m1.to_csv, "mydf.csv")


@app.callback(
    Output('my-toggle-switch-output', 'children'),
    Input('my-toggle-switch', 'value')
)

def update_output(value):
    rsi_list = []
    if value==True:
        for p in df_m1['symbols']:
            ticker = yf.Ticker(p)
            df_prices = ticker.history(interval='1d')
            df1 = pta.rsi(df_prices['Close'], length = 14)  # fourteen days!
            rsi_list.append(df1[-1])
        
        df_rsi = df_m1.iloc[:, [0,1,2,3,4,5,6,7]]
        df_rsi['1d_rsi'] = rsi_list
        
        return html.Div([
            dash_table.DataTable(df_rsi.to_dict('records'),columns =[{"name": i, "id": i} for i in df_rsi.columns],id='tb_m1',
                                 style_data_conditional = [{
                                      'if': {
                                          'filter_query': '{points} > 19',
                                      },
                                      'backgroundColor': 'green',
                                      'color': 'black'
                                  },
                                      {
                                      # 'if': {
                                      #     'filter_query': '{points} <19  && {points} > 13',
                                      # },
                                      'if': {
                                          'filter_query': '{dividend} > 9',
                                          'column_id' : 'dividend'
                                      },
                                          
                                      'backgroundColor': 'yellow',
                                      'color': 'black'
                                  },
                                      
                                    {  
                                          'if': {
                                          'filter_query': '{high_growth} > 9',
                                          'column_id' : 'high_growth'
                                      },
                                        
                                    
                                          
                                      'backgroundColor': 'yellow',
                                      'color': 'black'
                                  },
                                      
                                      {  
                                          'if': {
                                          'filter_query': '{leverman} > 2',
                                          'column_id' : 'leverman'
                                      },
                                        
                                    
                                          
                                      'backgroundColor': 'yellow',
                                      'color': 'black'
                                  },
                                      
                                      
                                      { 
                                      'if': {
                                          'filter_query': '{points} <13',
                                      },
                                      'backgroundColor': 'red',
                                      'color': 'black'
                                  },
                                      
                                  ],style_table={'overflowX': 'scroll'}) ,

        ])
    


@app.callback(
    Output('my-toggle-switch-output_b', 'children'),
    Input('my-toggle-switch_b', 'value')
)

def update_output(value):
    bb_list = []
    if value==True:
        for p in df_with_BB['symbols']:
            ticker = yf.Ticker(p)
            df_prices = ticker.history(interval='1d', period = "1mo")
            #time.sleep(10)
            df_prices['sma'] = sma(df_prices['Close'],14)
            df_prices['upper_bb'], df_prices['lower_bb'] = bb(df_prices['Close'], df_prices['sma'],14)
            df_prices = df_prices.dropna()
            buy_price, sell_price, bb_signal  = implement_bb_strategy(df_prices['Close'], df_prices['lower_bb'], df_prices['upper_bb'])
            df_prices['signal'] = bb_signal
            bb_list.append(df_prices['signal'][-1])
        
        df_bb = df_with_BB.iloc[:, [0,1,2,3,4,5,6,7]]
        df_bb['1d_bb'] = bb_list
        
        return html.Div([
            dash_table.DataTable(df_bb.to_dict('records'),columns =[{"name": i, "id": i} for i in df_bb.columns],id='tb_m1',
                                 style_data_conditional = [{
                                      'if': {
                                          'filter_query': '{points} > 19',
                                      },
                                      'backgroundColor': 'green',
                                      'color': 'black'
                                  },
                                      {
                                      # 'if': {
                                      #     'filter_query': '{points} <19  && {points} > 13',
                                      # },
                                      'if': {
                                          'filter_query': '{dividend} > 9',
                                          'column_id' : 'dividend'
                                      },
                                          
                                      'backgroundColor': 'yellow',
                                      'color': 'black'
                                  },
                                      
                                    {  
                                          'if': {
                                          'filter_query': '{high_growth} > 9',
                                          'column_id' : 'high_growth'
                                      },
                                        
                                    
                                          
                                      'backgroundColor': 'yellow',
                                      'color': 'black'
                                  },
                                      
                                      {  
                                          'if': {
                                          'filter_query': '{leverman} > 2',
                                          'column_id' : 'leverman'
                                      },
                                        
                                    
                                          
                                      'backgroundColor': 'yellow',
                                      'color': 'black'
                                  },
                                      
                                      
                                      { 
                                      'if': {
                                          'filter_query': '{points} <13',
                                      },
                                      'backgroundColor': 'red',
                                      'color': 'black'
                                  },
                                      
                                  ],style_table={'overflowX': 'scroll'}) ,

        ])
    


#twitter call back


@app.callback(
    Output('my-toggle-switch-output_t', 'children'),
    Input('my-toggle-switch_t', 'value')
)

def update_output(value):
    bb_list = []
    if value==True:
        # for p in df_m2_symbols['stockname']:
        #     ticker = yf.Ticker(p)
        #     df_prices = ticker.history(interval='1d', period = "1mo")
        #     #time.sleep(10)
        #     df_prices['sma'] = sma(df_prices['Close'],14)
        #     df_prices['upper_bb'], df_prices['lower_bb'] = bb(df_prices['Close'], df_prices['sma'],14)
        #     df_prices = df_prices.dropna()
        #     buy_price, sell_price, bb_signal  = implement_bb_strategy(df_prices['Close'], df_prices['lower_bb'], df_prices['upper_bb'])
        #     df_prices['signal'] = bb_signal
        #     bb_list.append(df_prices['signal'][-1])
        
        df_sent = reading_tweets(df_m1)
        # df_bb = df_m2_symbols.iloc[:, [0,1,2,3,4,5,6,7]]
        # df_bb['1d_bb'] = bb_list
        
        return html.Div([
            dash_table.DataTable(df_sent.to_dict('records'),columns =[{"name": i, "id": i} for i in df_sent.columns],id='tb_m1',
                                 style_data_conditional = [{
                                      'if': {
                                          'filter_query': '{points} > 19',
                                      },
                                      'backgroundColor': 'green',
                                      'color': 'black'
                                  },
                                      {
                                      # 'if': {
                                      #     'filter_query': '{points} <19  && {points} > 13',
                                      # },
                                      'if': {
                                          'filter_query': '{dividend} > 9',
                                          'column_id' : 'dividend'
                                      },
                                          
                                      'backgroundColor': 'yellow',
                                      'color': 'black'
                                  },
                                      
                                    {  
                                          'if': {
                                          'filter_query': '{high_growth} > 9',
                                          'column_id' : 'high_growth'
                                      },
                                        
                                    
                                          
                                      'backgroundColor': 'yellow',
                                      'color': 'black'
                                  },
                                      
                                      {  
                                          'if': {
                                          'filter_query': '{leverman} > 2',
                                          'column_id' : 'leverman'
                                      },
                                        
                                    
                                          
                                      'backgroundColor': 'yellow',
                                      'color': 'black'
                                  },
                                      
                                      
                                      { 
                                      'if': {
                                          'filter_query': '{points} <13',
                                      },
                                      'backgroundColor': 'red',
                                      'color': 'black'
                                  },
                                      
                                  ],style_table={'overflowX': 'scroll'}) ,

        ])
    


@app.callback(Output('gauge-chart', 'figure'), [Input('gauge-chart', 'value')])
def update_label(value):
    label = get_label(value)
    fig.update_layout(
        annotations=[{
            'x': 0.5,
            'y': 0.4,
            'text': label,
            'showarrow': True,
            'font': {'size': 20}
        }]
    )
    return fig


if __name__ == '__main__':
    app.run_server()


