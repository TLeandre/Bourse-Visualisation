import db_actions as da

import matplotlib.pyplot as plt 
import plotly.graph_objects as go
import plotly.express as px

def get_invest(id):
    df = da.get_actions(id)

    sum = 0
    for i in range(len(df)):
        sum += df['QUANTITY'][i] * df['PRICE'][i]
    
    return sum

def candlestick(data):
    fig = go.Figure(data=[go.Candlestick(x=data['DATE'],
                    open=data['Open'],
                    high=data['High'],
                    low=data['Low'],
                    close=data['Close'],
                    name="symbol")])

    fig.update_xaxes(type='category')
    fig.update_layout(height=800)

    return fig

def line_chart(data):
    return px.line(data, x="DATE", y="Close", title='Line chart de votre portefeuille boursier')

def pie(id):
    data = da.get_actions(id)
    data['INVEST'] = data['PRICE'] * data['QUANTITY']
    pie = px.pie(data, values='INVEST', names='NAME', color_discrete_sequence=px.colors.sequential.RdBu, title="Répartition d'investissement sur le portefeuille")
    return pie