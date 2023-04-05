import yfinance as yf 
import pandas as pd 
import db_actions as da
import datetime

def get_hist_actions(actions, inter):
    df = []
    for i in range(len(actions)):
        df.append(yf.download(actions['SYMBOLE'][i], start=str(actions.index[i]), end=None,  interval = inter))
        df[i] = df[i].set_axis([ 'Open'+str(i), 'High'+str(i),'Low'+str(i),'Close'+str(i),'Adj Close'+str(i),'Volume'+str(i)], axis='columns')
    return df

def get_full_hist(hist_actions, actions):
    ind = 0
    maxi = -1
    for i in range(len(actions)):
        if len(hist_actions[i]) > maxi:
            ind = i
    
    liste = list(range(len(actions)))
    del liste[ind]
    frame = hist_actions[ind]
    
    for i in liste:
        frame = pd.concat([frame, hist_actions[i]], axis=1)
        frame = frame.fillna(method="ffill")
        frame = frame.fillna(0)
    
    result = pd.DataFrame(columns=["Open","High","Low","Close"])

    result["Open"] = frame["Open0"]*actions['QUANTITY'][0]
    result["High"] = frame["High0"]*actions['QUANTITY'][0]
    result["Low"] = frame["Low0"]*actions['QUANTITY'][0]
    result["Close"] = frame["Close0"]*actions['QUANTITY'][0]


    for i in range(1,len(actions)):

        result["Open"] += frame["Open"+str(i)]*actions['QUANTITY'][i]
        result["High"] += frame["High"+str(i)]*actions['QUANTITY'][i]
        result["Low"] += frame["Low"+str(i)]*actions['QUANTITY'][i]
        result["Close"] += frame["Close"+str(i)]*actions['QUANTITY'][i]

    return result

def total_hist(inter, id):
    actions =  da.get_actions(id)  

    result = get_full_hist(get_hist_actions(actions, inter), actions)

    result['DATE'] = result.index
    
    return result

def get_last_value(actions):
    today = datetime.datetime.today()
    week = datetime.timedelta(weeks=1)
    date = str(today - week)[:10]
    df = []
    result = []
    for i in range(len(actions)):
        print(actions)
        df.append(yf.download(actions['SYMBOLE'][i], start=date, end=None))
        df[i] = df[i].set_axis([ 'Open'+str(i), 'High'+str(i),'Low'+str(i),'Close'+str(i),'Adj Close'+str(i),'Volume'+str(i)], axis='columns')
    
    for i in range(len(actions)):
        result.append(df[i]['Close'+str(i)][-1])
    return result

def action_exit(symbole):
    today = datetime.datetime.today()
    week = datetime.timedelta(weeks=1)
    date = str(today - week)[:10]
    result = yf.download(symbole, start=date, end=None)
    
    try:
        result['Open'][0]
        return 0
    
    except IndexError as err:
        return -1