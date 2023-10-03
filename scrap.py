import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv
import os

def url():
# Faire une requête HTTP
    url = 'https://www.data.gouv.fr/fr/datasets/bases-de-donnees-annuelles-des-accidents-corporels-de-la-circulation-routiere-annees-de-2005-a-2021/#/resources'
    response = requests.get(url)
    return response


def scraping():
    # Analyser le HTML avec Beautiful Soup
    soup = BeautifulSoup(url().content, 'html.parser')

    #Trouver la balise meta avec l'attribut name="description"
    soup.find_all('script')

    # Search within the script tags for the desired URL
    target_url_usagers = "https://static.data.gouv.fr/resources/bases-de-donnees-annuelles-des-accidents-corporels-de-la-circulation-routiere-annees-de-2005-a-2021/20230131-221725/usagers.csv"
    # target_url_vehicules = "https://static.data.gouv.fr/resources/bases-de-donnees-annuelles-des-accidents-corporels-de-la-circulation-routiere-annees-de-2005-a-2021/20230131-222049/vehicules.csv"
    # target_url_lieux = "https://static.data.gouv.fr/resources/bases-de-donnees-annuelles-des-accidents-corporels-de-la-circulation-routiere-annees-de-2005-a-2021/20230131-222049/vehicules.csv"
    target_url_caracteristiques = "https://static.data.gouv.fr/resources/bases-de-donnees-annuelles-des-accidents-corporels-de-la-circulation-routiere-annees-de-2005-a-2021/20230131-221944/caracteristiques.csv"


    # Read the CSV file from the web link
    df_usagers = pd.read_csv(target_url_usagers, encoding='latin-1', low_memory=False)
    # df_vehicules = pd.read_csv(target_url_vehicules)
    # df_lieux = pd.read_csv(target_url_lieux)
    df_caracteristiques = pd.read_csv(target_url_caracteristiques, encoding='latin-1', low_memory=False)

    return df_usagers, df_caracteristiques


def write_csv_usagers():
    usagers, caracteristiques = scraping()
    with open('Acc_route/data/usagers.csv', 'w', newline='', encoding='latin-1') as f:
        csv_writer = csv.writer(f)
        
        # Écrire les en-têtes de colonnes
        csv_writer.writerow(usagers.columns)
        
        # Écrire les données
        for index, data in usagers.iterrows():
            csv_writer.writerow(data)
def write_csv_caracteristiques():
    usagers, caracteristiques = scraping()
    with open('Acc_route/data/caracteristiques.csv', 'w', newline='', encoding='latin-1') as f:
        csv_writer = csv.writer(f)
        
        # Écrire les en-têtes de colonnes
        csv_writer.writerow(caracteristiques.columns)
        
        # Écrire les données
        for index, data in caracteristiques.iterrows():
            csv_writer.writerow(data)

def data_usagers():
    df = pd.read_csv('../src/Acc_route/data/usagers.csv',encoding='latin-1', low_memory=False)
    usagers = df[["num_acc","grav","sexe","an_nais","annee"]]
    return usagers
def data_caracteristiques():
    df = pd.read_csv('../src/Acc_route/data/caracteristiques.csv',encoding='latin-1', low_memory=False)
    df["num_acc"] = df["num_acc"].astype(int)
    caracteristiques = df[["num_acc","lum","agg","int","atm","lat","loc","long","dep","annee"]]
    return caracteristiques

def merge():
    df1 = data_usagers()
    df2 = data_caracteristiques()
    merged_df = pd.merge(df1, df2, on='num_acc', how='inner')
    merged_df.drop(columns=['annee_y'], inplace=True)
    merged_df.rename(columns={'annee_x': 'annee'}, inplace=True)
    merged_df.to_csv('../src/Acc_route/data/data.csv', index=False)
    


# write_csv_usagers()
# write_csv_caracteristiques()
merge()


