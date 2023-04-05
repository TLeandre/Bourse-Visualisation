##import librairies 
import streamlit as st 
from streamlit_option_menu import option_menu

import matplotlib.pyplot as plt 
import plotly.graph_objects as go
import plotly.express as px

import datetime

##import py 
import login 
import db_actions as da
import actions_info 
import graph 



st.set_page_config(layout="wide")
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

c1, c2 = st.columns(2)

with c1:
    st.title('Visualisation de votre portefeuille boursier')
with c2:
    st.markdown('   ', unsafe_allow_html=False)
    st.markdown('   ', unsafe_allow_html=False)
    st.markdown('   ', unsafe_allow_html=False)
    selected = option_menu(
        menu_title=None,
        options=['Overview','Actions'],
        orientation="horizontal"
    )
st.markdown('--------------', unsafe_allow_html=False)

## LOGIN BAR 
with st.sidebar:
    st.title("Login")
    l_email = st.text_input("Email", key="l_email")
    l_password = st.text_input("Password", key="l_password", type="password")
    
    st.title("Sign in ")
    s_name = st.text_input("Name", key="s_name")
    s_surname = st.text_input("Surname", key="s_surname")
    s_email = st.text_input("Email", key="s_email")
    s_password = st.text_input("Password", key="s_password", type="password")
    if st.button("Sign in"):
        add = login.sign_in(s_name, s_surname, s_email, s_password)
        if add == 0:
            st.success("Votre compte a bien été créé")
        elif add == -1:
            st.warning("Malheureusement votre email est déjà utilisé")

if selected == "Overview":
    connect, id = login.connect(l_email, l_password)
    if connect:
        try: 
            ## Top 
            co1, co2 =  st.columns(2)

            hist = actions_info.total_hist('1d', id)
            with co1:
                st.metric(label="Date de dernière mise à jour", value=str(hist.iloc[-1]['DATE'])[0:10])
            with co2:
                st.metric(label="Evaluation", value=str(round(hist.iloc[-1]['Open'], 2)) + "€", delta=str(round(hist.iloc[-1]['Open']-graph.get_invest(id), 2)) + "€")
            
            st.markdown('--------------', unsafe_allow_html=False)

            ## Affichage des graphiques 
            collo1, collo2 =  st.columns(2)
            with collo1:
                frequency = st.selectbox(
                    "Interval",
                    ('1d','5d','1wk','1mo','3mo'))
            with collo2:
                option = st.selectbox(
                    'Diagramme',
                    ('Line chart', 'Japanese candlestick chart'))

            data = actions_info.total_hist(frequency, id)
            if option == 'Line chart':
                fig = graph.line_chart(data)
            else:
                fig = graph.candlestick(data)
            st.plotly_chart(fig, use_container_width=True)


            st.plotly_chart(graph.pie(id))

        except ValueError as err:
            print("ValueError", err)
            st.warning("Vous n'avez pas encore d'actions ! Allez en ajouter dans 'Actions'")

    else : 
        st.warning("merci de vous connecter ou de vous créer un compte")

if selected == "Actions":
    connect, id = login.connect(l_email, l_password)
    if connect:

        ## truc général pour ajouter / vendre une action 
        co1, co2, co3, co4 =  st.columns(4)
        with co1:
            symbole = st.text_input('Symbole', 'AAPL')
        with co2:
            price = st.number_input("Prix")
        with co3:
            quantity = st.number_input("Quantite", step=1)
        with co4:
            date = st.date_input("Date", datetime.date(2023, 5, 21))

        cl1, cl2 = st.columns(2)
        with cl1:
            if st.button('Acheter'):
                add = da.add_operation(symbole, date, price, int(quantity), id, 1)
                if add == 1:
                    st.success("L'action a été acheté ")
                
        with cl2:
            if st.button('Vendre'):
                add = da.add_operation(symbole, date, price, int(quantity), id, -1)
                if add == 1:
                    st.success("L'action a été vendu ")
                elif add == 0:
                    st.warning("Vous avez moins d'action que ce que vous essayez de vendre")
                elif add == -1: 
                    st.warning("Action introuvable il y a certainement une erreur dans le symbole, merci de verifier")

        try:
            actions = da.get_quantity_actions(id)  ## faire en sorte de concaténer les valeurs 
            actual_price = actions_info.get_last_value(actions)

            st.dataframe(actions)

            coll1, coll2, coll3, coll4 = st.columns(4)
            for i in range(len(actions)):
                if (i % 4) == 0:
                    with coll1:
                        st.metric(
                            label=actions['SYMBOLE'][i], 
                            value=str(round(actual_price[i],2)),
                            delta=str(round(actual_price[i] - actions['PRICE'][i], 2)) + "€",
                        )
                elif (i % 4) == 1:
                    with coll2:
                        st.metric(
                            label=actions['SYMBOLE'][i], 
                            value=str(round(actual_price[i],2)),
                            delta=str(round(actual_price[i] - actions['PRICE'][i], 2)) + "€",
                        )
                elif (i % 4) == 2:
                    with coll3:
                        st.metric(
                            label=actions['SYMBOLE'][i], 
                            value=str(round(actual_price[i],2)),
                            delta=str(round(actual_price[i] - actions['PRICE'][i], 2)) + "€",
                        )
                elif (i % 4) == 3:
                    with coll4:
                        st.metric(
                            label=actions['SYMBOLE'][i], 
                            value=str(round(actual_price[i],2)),
                            delta=str(round(actual_price[i] - actions['PRICE'][i], 2)) + "€",
                        )

        except ValueError as err:
            print("ValueError", err)
            st.warning("Vous n'avez pas encore d'actions! Allez les ajouter dans 'Actions' ")