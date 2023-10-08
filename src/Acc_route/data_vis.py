#!/usr/bin/env python
# coding: utf-8

# import library
import pandas as pd
import plotly 
import plotly.graph_objs as go 
import json
from urllib.request import urlopen
import plotly.express as px 
import datetime
from joblib import load




def data_trait():
    df = pd.read_csv('Acc_route/data/data.csv')
    df.dropna(subset=["annee", "grav", "sexe", "an_nais", "dep"], inplace=True)
    df = df.astype({
        'annee': int,
        'dep': str,
        'sexe': int,
        'grav': int,
        'an_nais': int
    })
    return df

def nb_usagers(year, departement, gender, gravity, age1, age2):
  df = data_trait()
  year_now = datetime.datetime.now().year
  df['age'] =  year_now - df["an_nais"]
  if age1 != 0:
        df = df[df['age'] >= age1]
  if age2 != 0:
        df = df[df['age'] <= age2]
  df = df[df['annee'] == year]
  df = df[df['dep'] == departement]
  df = df[df['sexe'] == gender]  
  df = df[df['grav'] ==  gravity]
  df  = df.groupby(by=["age"])["grav"].size().reset_index(name="count_grav")
  df_temp = pd.DataFrame(df)
  return df_temp




def plot(year , departement, gender, gravity, age1, age2, name, color):

    df = nb_usagers(year, departement, gender, gravity, age1, age2)
    fig = go.Bar(
            x = df["age"],
            y = df["count_grav"],
            name = name,
            marker = dict(color = color ,
                            line = dict(color ='rgb(0,0,0)',width =1.5)))
    data = [fig]
    layout = go.Layout(barmode = "group",
                       title= "",
                       xaxis=dict(title='Age'),
                       yaxis=dict( title="Nombre D'usager"))
    fig = go.Figure(data = data, layout = layout)
    graphJSON = json.dumps (fig, cls = plotly.utils.PlotlyJSONEncoder)
    return graphJSON

def carte_france():

    with urlopen('https://france-geojson.gregoiredavid.fr/repo/departements.geojson') as response:
        geojson = json.load(response)
    df = data_trait()

    names=['code_departement', 'nom_departement', 'code_region', 'nom_region']
    df1 = pd.read_csv('Acc_route/data/departements-france.csv',
                                header=None, skiprows=[0], names=names)


    df['dep'] = df['dep'].str.replace(r'\D+', '', regex=True)
    df['dep'] = df['dep'].astype(int)
    df = df.sort_values(by='dep', ascending = True)

    # df['dep']=df.dep//10

    df1 = pd.DataFrame(df1[['code_departement','nom_departement','code_region',
                          'nom_region']])
    df1['code_departement'] = df1['code_departement'].str.lstrip('0')
    df1['code_departement'] = df1['code_departement'].str.replace(r'\D+', '', regex=True)
    df1['code_departement'] = df1['code_departement'].astype(int)
    # df2 = pd.concat([df, df1], axis =1)
    df2 = pd.merge(df,df1, left_on='dep', right_on='code_departement', how='inner')

    year_now = datetime.datetime.now().year
    df2["age"] = year_now - df["an_nais"]
    df2 = df2.fillna(0)
    df2['age'] = df2['age'].astype(int)
    
    df3  = df2.groupby(by=["age"])["grav"].size().reset_index(name="count_grav")
    df4 = pd.merge(df2,df3, left_on='age', right_on='age', how='inner')
    df_temp = pd.DataFrame(df4)
    return df_temp, geojson


def plot_carte_nb_acc():
    # Creat figure
    df, geojson = carte_france()
    fig = px.choropleth_mapbox(df,geojson= geojson
                           ,color=df["count_grav"]
                           ,locations=df["dep"]
                           ,featureidkey="properties.code"
                           ,hover_name = df['nom_departement']
                           , color_continuous_scale = [(0,"purple"), (1,"red")]
                           #,color_continuous_midpoint = 4
                           ,range_color = (0, 2000)
                           #,title="NOMBRE TOTALE D'USAGERS ACCIDENTÉS PAR DEPARTEMENT"
                           ,center={"lat": 46.3223, "lon": 1.2549}
                           ,mapbox_style="carto-positron", zoom=4.5)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    graphJSON = json.dumps (fig, cls = plotly.utils.PlotlyJSONEncoder)

    return graphJSON

def plot_carte_loc():

    df2, geojson = carte_france()
    df2['lat'] = df2['lat'].apply(lambda x: str(str(x).replace(',', '.')))
    df2['long'] = df2['long'].apply(lambda x: str(str(x).replace(',', '.')))
    df2['lat']= df2['lat'].astype(float, errors = 'ignore')
    df2['long'] =  pd.to_numeric(df2['long'], errors='coerce').abs()
    df2 = df2[df2['long'] != 0] 
    df2 = df2[df2['lat'] != 0]
    df3 = df2[df2['long'] > 10]
    df3['lat'] = df3['lat']/1000000      
    df2[df2['long'] > 10] = df3
    site_lat = df2['lat']
    site_lon = df2['long']
    locations_name = df2['nom_departement']
    fig = go.Figure()
    mapbox_access_token = "pk.eyJ1IjoiaGFjaGVtMTMiLCJhIjoiY2tiZ3Jxd2hjMTJjYTJyb293MWp2ZjN6NCJ9.6zbhZNrucd-yITpe6WIYsA"
    fig.add_trace(go.Scattermapbox(lat=site_lat,lon=site_lon,mode='markers',marker=go.scattermapbox.Marker(size=5,color='rgb(92, 189, 231)',opacity=0. ),text=locations_name,hoverinfo='text'))

    fig.add_trace(go.Scattermapbox(lat=site_lat,lon=site_lon,mode='markers', marker=go.scattermapbox.Marker(size=3, color='rgb(242, 177, 172)', opacity=0.7),hoverinfo='none'))

    fig.update_layout(title='',autosize=True,hovermode='closest',showlegend=False,mapbox=dict(accesstoken=mapbox_access_token, bearing=0, center=dict( lat=46.3223, lon=1.2549), pitch=0, zoom=3.5, style='light'),)
    graphJSON = json.dumps (fig, cls = plotly.utils.PlotlyJSONEncoder)
    return graphJSON

def prediction(year, gender, age, localisation, intersection, lumiere, departement):  
    files = 'Acc_route/data/rfc1_prediction_1.joblib' + 'Acc_route/data/rfc1_prediction_2.joblib' + 'Acc_route/data/rfc1_prediction_3.joblib' + 'Acc_route/data/rfc1_prediction_4.joblib' 
    rfc = load(files)
    X = [[year, gender, age, localisation, intersection, lumiere, departement]]
    pred = rfc.predict_proba(X)
    if pred[0][0] > pred[0][1]:
        if pred[0][0] > 0.6:
            predict = 1
        else :
            predict = 0
    elif pred[0][0] < pred[0][1]:
        if pred[0][1] > 0.6:
            predict = 2
        else:
            predict = 0
    return predict