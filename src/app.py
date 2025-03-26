import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from dash import Dash, html, dcc, callback, Output, Input, dash_table, development
import plotly.express as px
from dash.dependencies import Input, Output, State
import base64
import io
import scipy as sp
from scipy.optimize import minimize
import math
import os
from os.path import join
from statistics import mean
from samooskrba_fun import samooskrba
from rezanje_konic_fun import rezanje_konic
import xml.etree.ElementTree as ET
import locale

main=os.path.abspath(os.getcwd())
logo='\\LEST_logo.png'
config = "\\config_cene.xml"
path_logo=main+logo
path_config = main+config
test_base64 = base64.b64encode(open(path_logo, 'rb').read()).decode('ascii')
data = ET.parse(path_config).getroot()

# cene omreznin ELES 1.1.2024 za gospodinjstva/odjem na NN 
ET_o = float(data.find("./cene/ET_o").text)
VT_o = float(data.find("./cene/VT_o").text)
MT_o = float(data.find("./cene/MT_o").text)

VT_m_2500_NN = float(data.find("./cene/VT_m_2500_NN").text)
MT_m_2500_NN = float(data.find("./cene/MT_m_2500_NN").text)
VT_v_2500_NN = float(data.find("./cene/VT_v_2500_NN").text)
MT_v_2500_NN = float(data.find("./cene/MT_v_2500_NN").text)

VT_m_2500_z_NN = float(data.find("./cene/VT_m_2500_z_NN").text)
MT_m_2500_z_NN = float(data.find("./cene/MT_m_2500_z_NN").text)
VT_v_2500_z_NN = float(data.find("./cene/VT_v_2500_z_NN").text)
MT_v_2500_z_NN = float(data.find("./cene/MT_v_2500_z_NN").text)

VT_m_2500_SN = float(data.find("./cene/VT_m_2500_SN").text)
MT_m_2500_SN = float(data.find("./cene/MT_m_2500_SN").text)
VT_v_2500_SN = float(data.find("./cene/VT_v_2500_SN").text)
MT_v_2500_SN = float(data.find("./cene/MT_v_2500_SN").text)

VT_m_2500_z_SN = float(data.find("./cene/VT_m_2500_z_SN").text)
MT_m_2500_z_SN = float(data.find("./cene/MT_m_2500_z_SN").text)
VT_v_2500_z_SN = float(data.find("./cene/VT_v_2500_z_SN").text)
MT_v_2500_z_SN = float(data.find("./cene/MT_v_2500_z_SN").text)

# Obracunska moc ELES 1.1.2024
obracunska_moc_cena = float(data.find("./moc/obracunska_moc").text)

obrm_m_2500_NN = float(data.find("./moc/obrm_m_2500_NN").text)
obrm_v_2500_NN = float(data.find("./moc/obrm_v_2500_NN").text)

obrm_m_2500_z_NN = float(data.find("./moc/obrm_m_2500_z_NN").text)
obrm_v_2500_z_NN = float(data.find("./moc/obrm_v_2500_z_NN").text)

obrm_m_2500_SN = float(data.find("./moc/obrm_m_2500_SN").text)
obrm_v_2500_SN = float(data.find("./moc/obrm_v_2500_SN").text)

obrm_m_2500_z_SN = float(data.find("./moc/obrm_m_2500_z_SN").text)
obrm_v_2500_z_SN = float(data.find("./moc/obrm_v_2500_z_SN").text)

# Cene energije in moči po posameznih blokih
cene_bloki_moc = [None, None, None, None]
cene_bloki_energija = [None, None, None, None]

cene_bloki_moc_0 = [
    data.find("./cene_bloki_moc/cene_bloki_moc_0/blok1").text,
    data.find("./cene_bloki_moc/cene_bloki_moc_0/blok2").text,
    data.find("./cene_bloki_moc/cene_bloki_moc_0/blok3").text,
    data.find("./cene_bloki_moc/cene_bloki_moc_0/blok4").text,
    data.find("./cene_bloki_moc/cene_bloki_moc_0/blok5").text
]

cene_bloki_energija_0 = [
    data.find("./cene_bloki_energija/cene_bloki_energija_0/blok1").text,
    data.find("./cene_bloki_energija/cene_bloki_energija_0/blok2").text,
    data.find("./cene_bloki_energija/cene_bloki_energija_0/blok3").text,
    data.find("./cene_bloki_energija/cene_bloki_energija_0/blok4").text,
    data.find("./cene_bloki_energija/cene_bloki_energija_0/blok5").text
]

cene_bloki_moc_1 = [
    data.find("./cene_bloki_moc/cene_bloki_moc_1/blok1").text,
    data.find("./cene_bloki_moc/cene_bloki_moc_1/blok2").text,
    data.find("./cene_bloki_moc/cene_bloki_moc_1/blok3").text,
    data.find("./cene_bloki_moc/cene_bloki_moc_1/blok4").text,
    data.find("./cene_bloki_moc/cene_bloki_moc_1/blok5").text
]

cene_bloki_energija_1 = [
    data.find("./cene_bloki_energija/cene_bloki_energija_1/blok1").text,
    data.find("./cene_bloki_energija/cene_bloki_energija_1/blok2").text,
    data.find("./cene_bloki_energija/cene_bloki_energija_1/blok3").text,
    data.find("./cene_bloki_energija/cene_bloki_energija_1/blok4").text,
    data.find("./cene_bloki_energija/cene_bloki_energija_1/blok5").text
]

cene_bloki_moc_2 = [
    data.find("./cene_bloki_moc/cene_bloki_moc_2/blok1").text,
    data.find("./cene_bloki_moc/cene_bloki_moc_2/blok2").text,
    data.find("./cene_bloki_moc/cene_bloki_moc_2/blok3").text,
    data.find("./cene_bloki_moc/cene_bloki_moc_2/blok4").text,
    data.find("./cene_bloki_moc/cene_bloki_moc_2/blok5").text
]

cene_bloki_energija_2 = [
    data.find("./cene_bloki_energija/cene_bloki_energija_2/blok1").text,
    data.find("./cene_bloki_energija/cene_bloki_energija_2/blok2").text,
    data.find("./cene_bloki_energija/cene_bloki_energija_2/blok3").text,
    data.find("./cene_bloki_energija/cene_bloki_energija_2/blok4").text,
    data.find("./cene_bloki_energija/cene_bloki_energija_2/blok5").text
]

cene_bloki_moc_3 = [
    data.find("./cene_bloki_moc/cene_bloki_moc_3/blok1").text,
    data.find("./cene_bloki_moc/cene_bloki_moc_3/blok2").text,
    data.find("./cene_bloki_moc/cene_bloki_moc_3/blok3").text,
    data.find("./cene_bloki_moc/cene_bloki_moc_3/blok4").text,
    data.find("./cene_bloki_moc/cene_bloki_moc_3/blok5").text
]

cene_bloki_energija_3 = [
    data.find("./cene_bloki_energija/cene_bloki_energija_3/blok1").text,
    data.find("./cene_bloki_energija/cene_bloki_energija_3/blok2").text,
    data.find("./cene_bloki_energija/cene_bloki_energija_3/blok3").text,
    data.find("./cene_bloki_energija/cene_bloki_energija_3/blok4").text,
    data.find("./cene_bloki_energija/cene_bloki_energija_3/blok5").text
]

cene_bloki_moc_4 = [
    data.find("./cene_bloki_moc/cene_bloki_moc_4/blok1").text,
    data.find("./cene_bloki_moc/cene_bloki_moc_4/blok2").text,
    data.find("./cene_bloki_moc/cene_bloki_moc_4/blok3").text,
    data.find("./cene_bloki_moc/cene_bloki_moc_4/blok4").text,
    data.find("./cene_bloki_moc/cene_bloki_moc_4/blok5").text
]

cene_bloki_energija_4 = [
    data.find("./cene_bloki_energija/cene_bloki_energija_4/blok1").text,
    data.find("./cene_bloki_energija/cene_bloki_energija_4/blok2").text,
    data.find("./cene_bloki_energija/cene_bloki_energija_4/blok3").text,
    data.find("./cene_bloki_energija/cene_bloki_energija_4/blok4").text,
    data.find("./cene_bloki_energija/cene_bloki_energija_4/blok5").text
]


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
#branje podatkov
izkoristek_razsmenrika= 0.85
zavarovanje=1.05/100 
dela_prosti_dnevi = ('01-01', '01-02', '02-08', '04-27', '05-01', '05-02', '06-25', '08-15', '10-31', '11-01', '12-25', '12-26')


#začetek aplikacije
app = Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.config.suppress_callback_exceptions = True
locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8')


def razsiri_podatke(contents,filename):
    df_result = pd.DataFrame(columns=['Datum in cas', 'Soncno sevanje (W/m2)', 'Temperatura (2 m) (°C)'])
    izbrani_stolpci = []

        # Decode the contents
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        if 'xls' in filename:
            # Assume that the user uploaded an excel file
            #df = pd.read_excel(io.BytesIO(decoded))
            data=pd.read_table(io.BytesIO(decoded),index_col=0, header=[0],encoding='cp1250')

    except Exception as e:
        
        return html.Div([
            'Napaka pri branju datoteke.'
        ])

    stara_vrednost_cas = None
    stara_vrednost_osv = None
    stara_vrednost_temp = 10
    popvprečje = 0
    povprecje_temp = 10
    first = 1
    count = 0

    data.reset_index(inplace=True)
    formats = ["%d.%m.%Y %H:%M", "%Y-%m-%d %H:%M:%S"]

    # Preveri, kateri format deluje za prvi datum v prvi vrstici prvega stolpca
    first_date = data.iloc[0, 0]

    for fmt in formats:
        try:
            # Poskusimo pretvoriti datum s trenutnim formatom
            pd.to_datetime(first_date, format=fmt)
            format_used = fmt
            break
        except ValueError:
            # Če pretvorba ne uspe, nadaljuj z naslednjim formatom
            continue
    # Iterate over rows in the file
    for indeks, vrstica in data.iterrows():
        # Ločimo vrednosti po zavihkih

        if pd.notna(vrstica.iloc[11]) and pd.notna(vrstica.iloc[2]):
        #if len(podatki) >= 12:
            # Calculate rolling mean
            if pd.notna(stara_vrednost_osv):
                popvprečje = (pd.to_numeric(vrstica.iloc[11]) + stara_vrednost_osv) / 2
                povprecje_temp = (pd.to_numeric(vrstica.iloc[2].replace(",",".")) + stara_vrednost_temp) / 2
            if first != 1:
                izbrani_stolpci.append([stara_vrednost_cas, popvprečje, povprecje_temp])

            # Append current row to the list
            izbrani_stolpci.append([pd.to_datetime(vrstica.iloc[0], format=format_used), pd.to_numeric(vrstica.iloc[11]),pd.to_numeric(vrstica.iloc[2].replace(",","."))])

            # Update previous timestamp and value
            stara_vrednost_cas = pd.to_datetime(vrstica.iloc[0], format=format_used) + pd.Timedelta(minutes=15)
            stara_vrednost_temp = pd.to_numeric(vrstica.iloc[2].replace(",","."))
            stara_vrednost_osv = pd.to_numeric(vrstica.iloc[11])
            first = 0
            count = 0
        else:
            if pd.notna(stara_vrednost_osv):
                popvprečje = (0 + stara_vrednost_osv) / 2
            if count >= 3:
                popvprečje = 0
            count += 1
            if pd.isna(stara_vrednost_temp):
                stara_vrednost_temp = 10

            if stara_vrednost_cas is not None:
                izbrani_stolpci.append([stara_vrednost_cas, popvprečje, povprecje_temp])
            # Append current row to the list
            izbrani_stolpci.append([pd.to_datetime(vrstica.iloc[0], format=format_used), popvprečje, stara_vrednost_temp])
            stara_vrednost_cas = pd.to_datetime(vrstica.iloc[0], format=format_used) + pd.Timedelta(minutes=15)

    izbrani_stolpci.append([pd.to_datetime(stara_vrednost_cas, format=format_used), 0, stara_vrednost_temp])
    # Reset index for the final DataFrame
    #df_result.reset_index(drop=True, inplace=True)
    df_result= pd.DataFrame(izbrani_stolpci,columns=['Datum in cas', 'Soncno sevanje (W/m2)', "Temperatura"])

    return html.Div([
        html.H3('Prebrana datoteka:', style={'display': 'block', 'text-align': 'center', 'marginTop': '10px'}),
        html.H4(filename),
        dcc.Store(id='stored-data', data=df_result.to_dict('records')),
        dcc.Store(id='Arso_click', data=1),
    ])

def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')
    
    try:
        # Decode the Base64 string
        decoded = base64.b64decode(content_string)
        zeljeni_stolpci = ['Časovna značka', 'Energija A+', 'Merilno mesto', "GSRN MM"]

        # Handle Excel files
        if filename.endswith('.xlsx'):
            df = pd.read_excel(io.BytesIO(decoded))

        # Handle CSV files
        elif filename.endswith('.csv'):
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))  # Assuming UTF-8 encoding

        else:
            return html.Div(['Nepodprta vrsta datoteke. Prosimo, naložite Excel ali CSV.'])

        # Check if all required columns are present
        mankajoci_stolpci = [stolpec for stolpec in zeljeni_stolpci if stolpec not in df.columns]
        if mankajoci_stolpci:
            return html.Div([
                f'Napaka: Manjkajoči stolpci - {", ".join(mankajoci_stolpci)}'
            ])

        return html.Div([
        html.H3('Prebrana datoteka:', style={'display': 'block', 'text-align': 'center', 'marginTop': '10px'}),
        html.H4(filename),
        dcc.Store(id='stored-data-2', data=df.to_dict('records')),
        dcc.Store(id='Elektro_click', data=1),
        ])

    except Exception as e:
        return html.Div([f'Napaka pri branju datoteke: {str(e)}'])



def pokazi_drugi_del_aplikacije(prvi_file, drugi_file):
    if prvi_file == 1 and drugi_file == 1:
        return html.Div([
        html.Div([
            html.H2(children='Lastnosti panela', style={'display': 'block', 'text-align': 'center'}, className='heading2'),
            html.Div([
                html.Div([
                    html.Label('Dolžina panela (m):', style={'display': 'block', 'text-align': 'center'}),
                    dcc.Input(id='panel_length', value=2, type='number', placeholder='Vnesite dolžino', style={'width': '10%', 'margin': '0 auto', 'display': 'block'}),
                    
                    html.Label('Širina panela (m):', style={'display': 'block', 'text-align': 'center'}),
                    dcc.Input(id='panel_width', value=1, type='number', placeholder='Vnesite širino', style={'width': '10%', 'margin': '0 auto', 'display': 'block'}),
                    
                    html.Label('Moč panela (W):', style={'display': 'block', 'text-align': 'center'}),
                    dcc.Input(id='panel_power', value=450, type='number', placeholder='Vnesite moč', style={'width': '10%', 'margin': '0 auto', 'display': 'block'}),
                    
                    html.Label('Izkoristek panela (%):', style={'display': 'block', 'text-align': 'center'}),
                    dcc.Input(id='panel_eff', value=22, type='number', placeholder='Vnesite izkoristek', style={'width': '10%', 'margin': '0 auto', 'display': 'block'}),
                    
                ], style={'text-align': 'center'})
            ], style={'text-align': 'center'}),
        ], style={'text-align': 'center'}),

        html.Hr(style={'color': '#1156A3'}, className='hr-style'),

        html.Div([
            html.H2(children='Podatki za izračun omrežnine in cene', style={'text-align': 'center', 'color': 'black'}, className='heading2'),
            html.Button('Pomoč!', id='pomoc_1-button', n_clicks=0,
                    style={'border': 'none', 'font-size': '12px',
                            'top': '10px', 'right': '10px'}, className='my-button'),
            html.Div(id='pomoc_1', children=["Vsi podatki so obvezni!!!",html.Br(),
                        "Pri vrednostih VT, MT in ET morajo biti cene obvezno vpisane.",html.Br(),
                        "Če imate dvo-tarifni sistem, je \"ET=0\", če pa imate eno-tarifnega, pa sta \"VT=0 in MT=0\""],
                        style={'display': 'block', 'text-align': 'center', 'marginBottom': '10px', 'font-size': '12px'}),
            html.Div([
                html.Label('Cena elektrarne[€/kW]:', style={'display': 'block', 'text-align': 'center'}),
                dcc.Input(id="cena_elektrarne", value=850, type='number', placeholder='Vnesite vrednost', style={'width': '10%', 'margin': '0 auto', 'display': 'block', 'marginBottom': '10px'}),
                
                html.Label('Cena električne en. MT[€/kWh]:', style={'display': 'block', 'text-align': 'center'}),
                dcc.Input(id="MT", value=0.145, type='number', placeholder='Vnesite vrednost', style={'width': '10%', 'margin': '0 auto', 'display': 'block', 'marginBottom': '10px'}),
                #0.0887
                html.Label('Cena električne en. VT[€/kWh]:', style={'display': 'block', 'text-align': 'center'}),
                dcc.Input(id="VT", value=0.163, type='number', placeholder='Vnesite vrednost', style={'width': '10%', 'margin': '0 auto', 'display': 'block', 'marginBottom': '10px'}),
                #0.12459
                html.Label('Cena električne en. ET[€/kWh]:', style={'display': 'block', 'text-align': 'center'}),
                dcc.Input(id="ET", value=0, type='number', placeholder='Vnesite vrednost', style={'width': '10%', 'margin': '0 auto', 'display': 'block', 'marginBottom': '10px'}),
                
                html.Label('Obračunska moč[kW]:', style={'display': 'block', 'text-align': 'center'}),
                html.Button('Pomoč!', id='pomoc_2-button', n_clicks=0,
                    style={'border': 'none', 'font-size': '12px',
                            'top': '10px', 'right': '10px'}, className='my-button'),
                html.Div(id='pomoc_2', children=["Obračunska moč je dogovorjena moč z dobaviteljem el. energije,",html.Br(),
                            "ki se uporablja za izračun omrežnine.",html.Br(),
                            "Najdete jo na mesečnem računu.",html.Br(),
                            "Za poslovne odjemalce pa velja povprečje 12ih vrednosti je številka, ki jo vpišete tukaj."],
                        style={'display': 'block', 'text-align': 'center', 'marginBottom': '10px', 'font-size': '12px'}),
                dcc.Input(id="obracunska_moc", value=0, type='number', placeholder='Vnesite vrednost', style={'width': '10%', 'margin': '0 auto', 'display': 'block', 'marginBottom': '10px'}),
                
                html.Label('Priključna moč[kW]:', style={'display': 'block', 'text-align': 'center'}),
                dcc.Input(id="prikljucna_moc", value=0, type='number', placeholder='Vnesite vrednost', style={'width': '10%', 'margin': '0 auto', 'display': 'block', 'marginBottom': '10px'}),
                html.Button('Pomoč!', id='pomoc_6-button', n_clicks=0,
                    style={'border': 'none', 'font-size': '12px',
                            'top': '10px', 'right': '10px'}, className='my-button'),
                html.Div(id='pomoc_6', children=["Dogovorjena obračunska moč za novo omrežnino je odvisna tudi od priključne moči. Bloki so omejeni z procenti priključne moči.", html.Br(),
                            "Z implementacijo sončne elektrarne in BHEE se nam zgodi, da se nam priključna moč zniža in posledično lahko zaprosimo za novo obračunsko moč.", html.Br(),
                            "Pri izračunih se bo nova priključna moč poznala pri omrežnini po stari kot tudi novi metodi."],
                        style={'display': 'block', 'text-align': 'center', 'marginBottom': '10px', 'font-size': '12px'}),
                dcc.Checklist(
                    id="nova_prikljucna_moc",
                    options=[
                        {'label': 'Pri izračunih upoštevaj novo priključno moč', 'value': 'MOC_YES'},
                    ],
                    value=['MOC_YES'],
                    labelStyle={'display': 'inline-block', 'margin-right': '20px','margin-bottom': '10px'}
                ),
                html.Label('Tip merilnega mesta:', style={'display': 'block', 'text-align': 'center'}),
                html.Button('Pomoč!', id='pomoc_3-button', n_clicks=0,
                    style={'border': 'none', 'font-size': '12px',
                            'top': '10px', 'right': '10px'}, className='my-button'),
                html.Div(id='pomoc_3', children=["Določitev tipa merilnega mesta vpliva na izračun omrežnine uporabnika po stari metodi obračunavanja.", html.Br(),
                            "Podatke o tipu merilnega mesta lahko najdete na svojem mesečnem računu, ki vam pa pošlje dobavitelj el. energije.", html.Br(),
                            "Polje se bo obarvalo rdeče, če boste napačno izbrali enotarifno/dvotarifo gospodinjstvo, glede na izpolnjene podatke VT, MT in ET."],
                        style={'display': 'block', 'text-align': 'center', 'marginBottom': '10px', 'font-size': '12px'}),
                dcc.Dropdown(
                    id='tip_merilnega_mesta_dropdown',
                    options=[
                        {'label': 'Gospodinjstvo - Enotarifni', 'value': 'Gospodinjstvo_enotarifni'},
                        {'label': 'Gospodinjstvo - Dvotarifni', 'value': 'Gospodinjstvo_dvotarifni'},
                        {'label': 'Poslovni odjem - NN - T<2500', 'value': 'Poslovni_odjem_NN_T<2500'},
                        {'label': 'Poslovni odjem - NN - T≥2500', 'value': 'Poslovni_odjem_NN_T≥2500'},
                        {'label': 'Poslovni odjem - NN zbiralke - T<2500', 'value': 'Poslovni_odjem_NN_zbiralke_T<2500'},
                        {'label': 'Poslovni odjem - NN zbiralke - T≥2500', 'value': 'Poslovni_odjem_NN_zbiralke_T≥2500'},
                        {'label': 'Poslovni odjem - SN - T<2500', 'value': 'Poslovni_odjem_SN_T<2500'},
                        {'label': 'Poslovni odjem - SN - T≥2500', 'value': 'Poslovni_odjem_SN_T≥2500'},
                        {'label': 'Poslovni odjem - SN zbiralke - T<2500', 'value': 'Poslovni_odjem_SN_zbiralke_T<2500'},
                        {'label': 'Poslovni odjem - SN zbiralke - T≥2500', 'value': 'Poslovni_odjem_SN_zbiralke_T≥2500'}
                    ],
                    style={'width': '400px', 'margin': '0 auto', 'display': 'block'}
                ),

                html.Label('Bloki[kW]:', style={'display': 'block', 'text-align': 'center', 'marginTop': '10px'}),
                html.Button('Pomoč!', id='pomoc_4-button', n_clicks=0,
                    style={'border': 'none', 'font-size': '12px',
                            'top': '10px', 'right': '10px'}, className='my-button'),
                html.Div(id='pomoc_4', children=["Bloki se uporabljajo za izračun omrežnine po novi metodi. Prvi blok ne sme biti višji od drugega, drgi ne sme biti višji od tretjega itd.", html.Br(),
                            "Če želite bloke vnesti ročno, morate obkljukati kvadratek s katerim se vam bloki odklenejo.", html.Br(),
                            "Ti bloki bodo uporabljeni za izračun omrežnine brez FV elektrarne po novi metodi. Za izračun omrežnine z FV el. pa bodo izračunani novi bloki, glede na mesečne konice."],
                        style={'display': 'block', 'text-align': 'center', 'marginBottom': '10px', 'font-size': '12px'}),
               
                dcc.Checklist(
                    id="bloki",
                    options=[
                        {'label': 'Odkleni in upoštevaj ročno vnesene bloke', 'value': 'BLOKI_YES'},
                    ],
                    labelStyle={'display': 'inline-block', 'margin-right': '20px'}
                ),
                html.Div(
                    style={
                        'display': 'block',
                        'text-align': 'center',  # Flexbox for the inner container
                        'gap': '20px',
                    },
                    children=[
                        dcc.Input(
                            id='BLOK1',
                            type='number',
                            placeholder='BLOK1',
                            disabled = True,
                            style={'width': '80px', 'padding': '8px', 'border': '1px solid #ccc', 'border-radius': '5px', 'text-align': 'center'},
                        ),
                        dcc.Input(
                            id='BLOK2',
                            type='number',
                            placeholder='BLOK2',
                            disabled = True,
                            style={'width': '80px', 'padding': '8px', 'border': '1px solid #ccc', 'border-radius': '5px', 'text-align': 'center',}
                        ),
                        dcc.Input(
                            id='BLOK3',
                            type='number',
                            placeholder='BLOK3',
                            disabled = True,
                            style={'width': '80px', 'padding': '8px', 'border': '1px solid #ccc', 'border-radius': '5px', 'text-align': 'center'}
                        ),
                        dcc.Input(
                            id='BLOK4',
                            type='number',
                            placeholder='BLOK4',
                            disabled = True,
                            style={'width': '80px', 'padding': '8px', 'border': '1px solid #ccc', 'border-radius': '5px', 'text-align': 'center'}
                        ),
                        dcc.Input(
                            id='BLOK5',
                            type='number',
                            placeholder='BLOK5',
                            disabled = True,
                            style={'width': '80px', 'padding': '8px', 'border': '1px solid #ccc', 'border-radius': '5px', 'text-align': 'center'}
                        ),
                    ],
                ),

 



                dcc.Store(id='stored_povrsina'),
                dcc.Store(id='stored_panel_eff'),
                dcc.Store(id='stored_panel_power'),
                dcc.Store(id='stored_bloki_check'),
                dcc.Store(id='stored_bloki_values'),
                dcc.Store(id='stored_vrednost'),
                dcc.Store(id="stored_nacin_izracuna"),
                dcc.Store(id='izvoz-podatki', storage_type='memory'),
                dcc.Store(id="stored_MT"),
                dcc.Store(id='stored_VT'),
                dcc.Store(id='stored_ET'),
                dcc.Store(id='stored_obracunska_moc'),
                dcc.Store(id='stored_prikljucna_moc'),
                dcc.Store(id='stored_nova_prikljucna_moc'),
                dcc.Store(id='stored_cena_elektrarne'),

                dcc.Store(id='stored_tip_merilnega_mesta'),
                dcc.Store(id="stored_VT_omrez"),
                dcc.Store(id="stored_MT_omrez"),
                dcc.Store(id="stored_ET_omrez"),
                dcc.Store(id="stored_obracunska_cena"),
                dcc.Store(id="stored_cena_blok_moc"),
                dcc.Store(id="stored_cena_blok_energija"),
                dcc.Store(id="stored_baterija-button"),
                dcc.Store(id="stored_baterija2-button"),
                dcc.Store(id="stored_velikost_bat"),
                dcc.Store(id="stored_kapaciteta_baterije_rezanje_konic"),
                dcc.Store(id="izvoz-podatki_bat"),
                dcc.Store(id="stored_cena_baterije"),


                html.Button('Shrani podatke', id="lock_button", style={
                    'backgroundColor': '#000000',  # Green background
                    'color': 'white',              # White text
                    'padding': '10px 20px',        # Padding around the text
                    'textAlign': 'center',         # Center text
                    'textDecoration': 'none',      # Remove underline
                    'display': 'inline-block',     # Inline-block element
                    'fontSize': '12px',            # Font size
                    'margin': '2px 1px',           # Margin
                    'cursor': 'pointer',
                    'verticalAlign': 'middle',     # Center text vertically
                    'lineHeight': '20px',
                    'marginTop': '20px'
                }),
                html.Div(id='dinamicni_vhodni_podatki_opozorilo',
                    style={'text-align': 'center'}),
                html.Div(id='dinamicni_vhodni_podatki_tretji_del',
                    style={'text-align': 'center'})
            ], style={'text-align': 'center'}),
        ], style={'text-align': 'center'}),

        html.Hr(style={'color': '#1156A3'}, className='hr-style'),
        ])
    else:
        return

def izračun_cene_el_energije(obracunska_moc, VT, MT, ET, all, VT_omrez, MT_omrez, ET_omrez, obracunska_moc_cena, stolpeci):
    procent_VT_OLD = all[all['Tarifa']=='V']["Energija A+"].sum()/all["Energija A+"].sum()
    procent_MT_OLD = all[all['Tarifa']=='N']["Energija A+"].sum()/all["Energija A+"].sum()
    if ET_omrez == 0 or ET_omrez is None or ET == 0:
        omreznina_ET_OLD = procent_VT_OLD*VT_omrez + procent_MT_OLD*MT_omrez + 12*obracunska_moc*obracunska_moc_cena/all["Energija A+"].sum()
        CET_OLD = procent_VT_OLD*VT + procent_MT_OLD*MT

    else:
        omreznina_ET_OLD = 1*ET_omrez + 12*obracunska_moc*obracunska_moc_cena/all["Energija A+"].sum()
        CET_OLD = 1*ET

    ostale_dajatve_OLD = 0.00013 + 0.0008 + 0.001530 + 12*obracunska_moc*4.1703/all["Energija A+"].sum()
    DDV = 22/100
    O_ET_OLD= omreznina_ET_OLD  + ostale_dajatve_OLD
    C_ET_OLD = (O_ET_OLD+CET_OLD)*(1+DDV)


    procent_VT_NEW = all[(all['Tarifa'] == 'V') & (all[stolpeci] > 0)][stolpeci].sum() / all[all[stolpeci] > 0][stolpeci].sum()
    procent_MT_NEW = all[(all['Tarifa'] == 'N') & (all[stolpeci] > 0)][stolpeci].sum() / all[all[stolpeci] > 0][stolpeci].sum()
    
    if ET_omrez == 0 or ET_omrez is None:
        omreznina_ET_NEW = procent_VT_NEW*VT_omrez + procent_MT_NEW*MT_omrez + 12*obracunska_moc*obracunska_moc_cena/all[all[stolpeci]>0][stolpeci].sum()
        CET_NEW = procent_VT_NEW*VT + procent_MT_NEW*MT
    else:
        omreznina_ET_NEW = 1*ET_omrez + 12*obracunska_moc*obracunska_moc_cena/all[all[stolpeci]>0][stolpeci].sum()
        CET_NEW = 1*ET


    ostale_dajatve_NEW = 0.00013 + 0.0008 + 0.001530 + 12*obracunska_moc*4.1703/all[all[stolpeci]>0][stolpeci].sum()
    O_ET_NEW= omreznina_ET_NEW  + ostale_dajatve_NEW
    C_ET_NEW = (O_ET_NEW+CET_NEW)*(1+DDV)
    return C_ET_OLD, C_ET_NEW, omreznina_ET_OLD*1.22*all["Energija A+"].sum(), omreznina_ET_NEW*1.22*all[all[stolpeci]>0][stolpeci].sum()

def objective_fun(x,cena_elektrarne, obracunska_moc, VT, MT, ET, all, VT_omrez, MT_omrez, ET_omrez, obracunska_moc_cena):
    all["razlika"]=all["Energija A+"]-all["proizvodnja_15_norm"]*x
    C_ET_OLD, C_ET_NEW, omreznina_stara,stran_dej  = izračun_cene_el_energije(obracunska_moc, VT, MT, ET, all, VT_omrez, MT_omrez, ET_omrez,  obracunska_moc_cena,"razlika")
    stosek_old = all["Energija A+"].sum()*C_ET_OLD
    strosek_new = all[all["razlika"]>0]["razlika"].sum() * C_ET_NEW
    prihranek = stosek_old - strosek_new
    if prihranek == 0:
        return print("napaka") # To avoid division by zero
    return x * cena_elektrarne/15 + strosek_new
    #return x * cena_elektrarne / prihranek

def bess_spec(med,avg, base_bess=100, inv_power=50):
    x=int(abs(min(0,med,avg)))
    batt_cap=base_bess * round(x/base_bess)
    batt_power=math.ceil(batt_cap/200)*inv_power  
    return batt_cap, batt_power

def dela_prost_dan(data):    
    data['Časovna značka'] = pd.to_datetime(data['Časovna značka'])   
    data.set_index('Časovna značka', drop=False, inplace=True)
    data['Month']=data.index.month
    data['Hour']=data.index.hour
    data['Day']=data.index.weekday+1  #1 - Monday, 7 - Sunday
    data['Sezona']=data['Month'].isin([1,2,11,12]).astype(int)  #Višja sezona
    data['Dela prost dan']=data.index.strftime('%m-%d').isin(dela_prosti_dnevi).astype(int)
    data.loc[(data['Day'].isin([6,7])),'Dela prost dan']=1
    return data

def tarifa(data):  # Stara omreznina
    # Initialize 'Tarifa' column with an object dtype to handle strings
    data['Tarifa'] = pd.NA
    
    # Nizka tarifa
    data.loc[data[(data['Dela prost dan'] == 1)].index, 'Tarifa'] = 'N'
    data.loc[data[(data['Dela prost dan'] == 0) & (data['Hour'].isin([0, 1, 2, 3, 4, 5, 23]))].index, 'Tarifa'] = 'N'
    
    # Visoka Tarifa
    data.loc[data[(data['Dela prost dan'] == 0) & (data['Hour'].isin([6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22]))].index, 'Tarifa'] = 'V'
    
    # Ensure the 'Tarifa' column is of type 'object' to hold strings
    data['Tarifa'] = data['Tarifa'].astype('object')
    
    return data

def bloki(df):  #Nova omrežnina
     df['Blok']=0
     #Blok 1
     df.loc[df[(df['Sezona']==1) & (df['Dela prost dan']==0) & (df['Hour'].isin([7,8,9,10,11,12,13,16,17,18,19]))].index,'Blok']=1
     #Blok 2
     df.loc[df[(df['Sezona']==1) & (df['Dela prost dan']==0) & (df['Hour'].isin([6,14,15,20,21]))].index,'Blok']=2
     df.loc[df[(df['Sezona']==1) & (df['Dela prost dan']==1) & (df['Hour'].isin([7,8,9,10,11,12,13,16,17,18,19]))].index,'Blok']=2
     df.loc[df[(df['Sezona']==0) & (df['Dela prost dan']==0) & (df['Hour'].isin([7,8,9,10,11,12,13,16,17,18,19]))].index,'Blok']=2
     #Blok 3
     df.loc[df[(df['Sezona']==1) & (df['Dela prost dan']==0) & (df['Hour'].isin([0,1,2,3,4,5,22,23]))].index,'Blok']=3
     df.loc[df[(df['Sezona']==1) & (df['Dela prost dan']==1) & (df['Hour'].isin([6,14,15,20,21]))].index,'Blok']=3
     df.loc[df[(df['Sezona']==0) & (df['Dela prost dan']==0) & (df['Hour'].isin([6,14,15,20,21]))].index,'Blok']=3
     df.loc[df[(df['Sezona']==0) & (df['Dela prost dan']==1) & (df['Hour'].isin([7,8,9,10,11,12,13,16,17,18,19]))].index,'Blok']=3
     #Blok 4
     df.loc[df[(df['Sezona']==1) & (df['Dela prost dan']==1) & (df['Hour'].isin([0,1,2,3,4,5,22,23]))].index,'Blok']=4
     df.loc[df[(df['Sezona']==0) & (df['Dela prost dan']==0) & (df['Hour'].isin([0,1,2,3,4,5,22,23]))].index,'Blok']=4
     df.loc[df[(df['Sezona']==0) & (df['Dela prost dan']==1) & (df['Hour'].isin([6,14,15,20,21]))].index,'Blok']=4
     #Blok 5
     df.loc[df[(df['Sezona']==0) & (df['Dela prost dan']==1) & (df['Hour'].isin([0,1,2,3,4,5,22,23]))].index,'Blok']=5
     return df

def obracunska_moc_fun(data, prikljucna_moc, delez, stolpec):
    dogovorjena_moc=[]

    for blok in range (1,6):    
        moc_blok_sorted=data[stolpec].iloc[np.where(data['Blok']==blok)].sort_values(ascending=False)*4
        obracunska_moc_blok_n=mean([moc_blok_sorted.iloc[0],moc_blok_sorted.iloc[1],moc_blok_sorted.iloc[2]])
        dogovorjena_moc.append(obracunska_moc_blok_n)
    #Min vrednost Blok 1    
    if dogovorjena_moc[0]>=prikljucna_moc*delez/100:
        dogovorjena_moc[0]=dogovorjena_moc[0]
    else:
        dogovorjena_moc[0]=max(prikljucna_moc*delez/100, 3.5) #vzame višjo izmed vrednosti
    
    #Min vrednost Blok 2    
    if dogovorjena_moc[1]>=dogovorjena_moc[0]:
        dogovorjena_moc[1]=dogovorjena_moc[1]
    else:
        dogovorjena_moc[1]=dogovorjena_moc[0]
        
    #Min vrednost Blok 3    
    if dogovorjena_moc[2]>=dogovorjena_moc[1]:
        dogovorjena_moc[2]=dogovorjena_moc[2]
    else:
        dogovorjena_moc[2]=dogovorjena_moc[1]  
        
    #Min vrednost Blok 4    
    if dogovorjena_moc[3]>=dogovorjena_moc[2]:
        dogovorjena_moc[3]=dogovorjena_moc[3]
    else:
        dogovorjena_moc[3]=dogovorjena_moc[2]  
        
    #Min vrednost Blok 5    
    if dogovorjena_moc[4]>=dogovorjena_moc[3]:
        dogovorjena_moc[4]=dogovorjena_moc[4]
    else:
        dogovorjena_moc[4]=dogovorjena_moc[3] 
        
    dogovorjena_moc=[round(elem,1) for elem in dogovorjena_moc ]   
    return dogovorjena_moc

def obracunska_moc_fun_nova_prikljucna_moc(data, delez, stolpec):
    dogovorjena_moc=[]

    for blok in range (1,6):    
        moc_blok_sorted=data[stolpec].iloc[np.where(data['Blok']==blok)].sort_values(ascending=False)*4
        obracunska_moc_blok_n=mean([moc_blok_sorted.iloc[0],moc_blok_sorted.iloc[1],moc_blok_sorted.iloc[2]])
        dogovorjena_moc.append(obracunska_moc_blok_n)

    dogovorjena_moc[0]=max(dogovorjena_moc[0], 3.5) #vzame višjo izmed vrednosti
    
    nova_prikljucna_moc_value = "Da. Prilagodili smo priključno moč za nižje bloke."
    #Min vrednost Blok 2    
    if dogovorjena_moc[1]>=dogovorjena_moc[0]:
        dogovorjena_moc[1]=dogovorjena_moc[1]
    else:
        dogovorjena_moc[1]=dogovorjena_moc[0]
        
    #Min vrednost Blok 3    
    if dogovorjena_moc[2]>=dogovorjena_moc[1]:
        dogovorjena_moc[2]=dogovorjena_moc[2]
    else:
        dogovorjena_moc[2]=dogovorjena_moc[1]  
        
    #Min vrednost Blok 4    
    if dogovorjena_moc[3]>=dogovorjena_moc[2]:
        dogovorjena_moc[3]=dogovorjena_moc[3]
    else:
        dogovorjena_moc[3]=dogovorjena_moc[2]  
        
    #Min vrednost Blok 5    
    if dogovorjena_moc[4]>=dogovorjena_moc[3]:
        dogovorjena_moc[4]=dogovorjena_moc[4]
    else:
        dogovorjena_moc[4]=dogovorjena_moc[3] 
        
    dogovorjena_moc=[round(elem,1) for elem in dogovorjena_moc ]   
    return dogovorjena_moc, nova_prikljucna_moc_value

def omreznina_moc(dogovorjena_moc,cene_bloki_moc):
    omreznina_moc_1=float(dogovorjena_moc[0])*float(cene_bloki_moc[0])*4  #koliko mesecov v letu moramo prišteti omrežnimo bloka
    omreznina_moc_2=float(dogovorjena_moc[1])*float(cene_bloki_moc[1])*12
    omreznina_moc_3=float(dogovorjena_moc[2])*float(cene_bloki_moc[2])*12
    omreznina_moc_4=float(dogovorjena_moc[3])*float(cene_bloki_moc[3])*12
    omreznina_moc_5=float(dogovorjena_moc[4])*float(cene_bloki_moc[4])*8
    
    omreznina_moc=omreznina_moc_1+omreznina_moc_2+omreznina_moc_3+omreznina_moc_4+omreznina_moc_5
      
    return omreznina_moc

def omreznina_energija(df, cene_bloki_energija, stolpec):
    df["omreznina_energija"]=0.0
    df.loc[df['Blok']==1,"omreznina_energija"]=df.loc[df['Blok']==1,stolpec]*float(cene_bloki_energija[0])
    df.loc[df['Blok']==2,"omreznina_energija"]=df.loc[df['Blok']==2,stolpec]*float(cene_bloki_energija[1])
    df.loc[df['Blok']==3,"omreznina_energija"]=df.loc[df['Blok']==3,stolpec]*float(cene_bloki_energija[2])
    df.loc[df['Blok']==4,"omreznina_energija"]=df.loc[df['Blok']==4,stolpec]*float(cene_bloki_energija[3])
    df.loc[df['Blok']==5,"omreznina_energija"]=df.loc[df['Blok']==5,stolpec]*float(cene_bloki_energija[4])
    strosek_omreznine_energija = df["omreznina_energija"].sum()
    return df, strosek_omreznine_energija

def izracun_cene_nova(data, prikljucna_moc, nova_prikljucna_moc, obracunska_moc, VT, MT, ET, delez, stolpec, cena_blok_moc, cena_blok_energija, bloki_check, bloki_values):
    if stolpec == "Energija A+":
        VT_en = data[data['Tarifa']=='V'][stolpec].sum()
        MT_en = data[data['Tarifa']=='N'][stolpec].sum()
        ET_en = data[stolpec].sum()
    elif stolpec == "razlika":
        VT_en = data[(data['Tarifa']=='V') & (data[stolpec]>0)][stolpec].sum()
        MT_en = data[(data['Tarifa']=='N') & (data[stolpec]>0)][stolpec].sum()
        ET_en = data[data[stolpec]>0][stolpec].sum()
    elif stolpec == "BESS":
        VT_en = data[(data['Tarifa']=='V') & (data[stolpec]>0)][stolpec].sum()
        MT_en = data[(data['Tarifa']=='N') & (data[stolpec]>0)][stolpec].sum()
        ET_en = data[data[stolpec]>0][stolpec].sum()

    nova_prikljucna_moc_value = "Ne. Nismo prilagodili blokov."
    if (bloki_check == ["BLOKI_YES"]) and (stolpec == "Energija A+"):
        obracunska_moc_bloki = bloki_values
    elif (nova_prikljucna_moc == ["MOC_YES"]) and (stolpec == "Energija A+"):
        obracunska_moc_bloki = obracunska_moc_fun(data, prikljucna_moc, delez, stolpec)
    elif (nova_prikljucna_moc == ["MOC_YES"]) and (stolpec == "razlika"):
        obracunska_moc_bloki, nova_prikljucna_moc_value = obracunska_moc_fun_nova_prikljucna_moc(data, delez, stolpec)
    elif (nova_prikljucna_moc == ["MOC_YES"]) and (stolpec == "BESS"):
        obracunska_moc_bloki, nova_prikljucna_moc_value = obracunska_moc_fun_nova_prikljucna_moc(data, delez, stolpec)
    else:
        obracunska_moc_bloki = obracunska_moc_fun(data, prikljucna_moc, delez, stolpec)


    strosek_omreznine_moc=omreznina_moc(obracunska_moc_bloki, cena_blok_moc)
    data, strosek_omreznine_energija = omreznina_energija(data, cena_blok_energija, stolpec)
    omreznina_skupno = strosek_omreznine_moc + strosek_omreznine_energija
    ostale_dajatve = (0.00013 + 0.0008 + 0.001530)*ET_en + 12*obracunska_moc*4.1703
    if ET == 0 or ET is None:
        energija = VT_en * VT + MT_en * MT

    else:
        energija = ET_en*ET

    DDV = 22/100
    cena = (omreznina_skupno + energija + ostale_dajatve)*(1+DDV)

    return obracunska_moc_bloki, omreznina_skupno*1.22, cena, nova_prikljucna_moc_value

def izračun_batt_osnovna(batt_cap, data, VT, MT, ET, BEES_price, cena_elektrarne):
    samooskrba = Samooskrba(data['Energija A+']*4,data['proizvodnja_15']*4)
    data['Battery power'], data["SoC"] = samooskrba.profil_samooskrbe(batt_cap, batt_cap*0.1, batt_cap/2, -batt_cap/2)
    #data['Battery power']=battProfile(data['Energija A+']*4,data['proizvodnja_15']*4, batt_cap,0,batt_cap/2, -batt_cap/2)#funkcija vzame profile moči in ne energije zatp *4
    #print(data['Battery power'])
    data['BESS']=data['Energija A+']-data['proizvodnja_15']-data['Battery power']/4
    data['Koncni_profil']=data['Energija A+']-data['proizvodnja_15']-data['Battery power']/4 # ker je moč in ne energija
    data.loc[data['BESS'] < 0, 'BESS'] = float(0)
    
    ##############################################################################
    #Cena elektrike
    ##############################################################################
    #Strošek električne energije s PV & BESS
    data['Strosek PV & BESS']=""
    if VT!=0 and MT!=0:
        data.loc[data['Tarifa'] == 'V', 'Strosek PV & BESS'] = data.loc[data['Tarifa'] == 'V', 'BESS'] * VT
        data.loc[data['Tarifa'] == 'N', 'Strosek PV & BESS'] = data.loc[data['Tarifa'] == 'N', 'BESS'] * MT
    elif ET !=0:
        data['Strosek PV & BESS'] = data['BESS'] * ET
    else:
        strosek_energije_PV_BESS=0


    strosek_energije_PV_BESS = data['Strosek PV & BESS'].sum()


    #############################################################################
    pv_power=(data['proizvodnja_15']/data['proizvodnja_15_norm']).mean()
    investicija_PV = pv_power*cena_elektrarne
    investicija_BHEE = batt_cap*BEES_price
    skupaj_investicija = (investicija_BHEE+investicija_PV)/15

    return skupaj_investicija + strosek_energije_PV_BESS + skupaj_investicija*zavarovanje

def izračun_batt_rezanje_konic(batt_cap, data, VT, MT, ET, BEES_price, cena_elektrarne):
    rezanje_konic = Rezanje_konic(data['Energija A+']*4,data['proizvodnja_15']*4)
    data['Battery power'], data["SoC"] = rezanje_konic.profil_rezanja_konic(batt_cap, 0, batt_cap/2, -batt_cap/2)
    data['BESS']=data['Energija A+']-data['proizvodnja_15']+data['Battery power']/4
    data['Koncni_profil']=data['Energija A+']-data['proizvodnja_15']+data['Battery power']/4 # ker je moč in ne energija
    data.loc[data['BESS'] < 0, 'BESS'] = float(0)
    
    ##############################################################################
    #Cena elektrike
    ##############################################################################
    #Strošek električne energije s PV & BESS
    data['Strosek PV & BESS']=""
    if VT!=0 and MT!=0:
        data.loc[data['Tarifa'] == 'V', 'Strosek PV & BESS'] = data.loc[data['Tarifa'] == 'V', 'BESS'] * VT
        data.loc[data['Tarifa'] == 'N', 'Strosek PV & BESS'] = data.loc[data['Tarifa'] == 'N', 'BESS'] * MT
    elif ET !=0:
        data['Strosek PV & BESS'] = data['BESS'] * ET
    else:
        strosek_energije_PV_BESS=0


    strosek_energije_PV_BESS = data['Strosek PV & BESS'].sum()


    #############################################################################
    pv_power=(data['proizvodnja_15']/data['proizvodnja_15_norm']).mean()
    investicija_PV = pv_power*cena_elektrarne
    investicija_BHEE = batt_cap*BEES_price
    skupaj_investicija = (investicija_BHEE+investicija_PV)/10

    return batt_cap, data #skupaj_investicija + strosek_energije_PV_BESS + skupaj_investicija*zavarovanje

#izgled aplikacije
app.layout = html.Div(children=[
    html.H1(children='LEST kalkulator za postavitev FV elektrarne', style={'text-align': 'center', 'color': '#1156A3'}, className = 'heading1'),
    html.Div(children=[
            html.Img(src='data:image/jpg;base64,{}'.format(test_base64),
                     alt="LEST logo",
                     style={"width": "30%", "height": "30%", "margin": "0 auto"}),
        ],
        style={'text-align': 'center'}

    ),

    # Info Button
    html.Div([
        html.Button('Info: ℹ️', id='info-button', n_clicks=0,
                    style={'border': 'none', 'font-size': '24px',
                           'position': 'absolute', 'top': '10px', 'right': '10px'}, className='my-button'),
        html.Div(id='info-content', children=[],
                 style={'margin-top': '10px', 'margin-bottom': '10px', 'display': 'none'}),
            ], style={'position': 'center'}),

    # Info Content
    html.Div(id='info-explanation', children=[
        html.P("Razlaga za uporabo kalkulatorja:", style={'font-family': 'Arial', 'padding-left': '10px'}),
        html.P(
            "Kalkulator je namenjen izračunu velikosti sončne elektrarne, glede na sončno obsevanje in porabnikov odjem. Te podatke lahko pridobite iz spletne strani Agrometeorološki portal in pa iz portala MojElektro. "
            "Pri nalaganju datotek morate biti pozorni, da sta leto obsevanja in leto odjema ENAKA, drugače kalkulator ne zna povezati podatkov. Namesto datoteke o sončni obsevanosti kalkulator ponuja tudi izbor povprečne obsevanosti večjih krajev po Sloveniji. "
            "Potrebujete tudi podatke sončnih modulov, ki so za izračune obvezni. Za ekonomski del programa pa so tudi obvezni podatki o cenah elektrike in same investicije. "
            "S pomočjo teh podatkov lahko dimenzionirate željeno velikost elektrarne na več različnih načinov (\"Optimalna velikost\", \"Površina elektrarne\", \"Število panelov\" in \"Odstotek samozadostnosti\"). "
            "Na podlagi teh podatkov vam kalkulator vrne moč elektrarne, poroizvodnjo el. energije, viške energije, odstotek samozadostnosti in površino sončne elektrarne. "
            "Če želite lahko izračunane profile FV elektrarne shranite v xlsx datoteko ali pa nadaljujete z eno od dveh možnosti. "
            "Izračunate lahko ekonomiko vaše dimenzionirane FV elektrarne ali pa ji dodate baterijski hranilnik el. energije(BHEE). "
            "Ekonomika elektrarne vam bo izračunala cene el. energije brez in z FV elektrarno, izračunala prihranek in vračilno dobo investicije. "
            "Izračuni bodo narejeni za oba načina obračunavanja omrežnine za star in nov model. "
            "Če pa boste hoteli dodati baterijo, bo kalkulator dodal BHEE optimalne velikosti in ponovno izračunal ekonomiko investicije po starem in novem načinu obračunavanja omrežnine. Prav tako lahko baterijo vodimo tako, da zmanjšamo konice odjema. Pri tem vodenju baterije si uporabnik sam izbere kapaciteto BHEE. "
            "Pri izračunih ekonomike je upoštevano tudi zavarovanje v velikosti 1.05 % celotne investicije.",
             style={'font-family': 'Arial', 'padding-left': '10px'}),
        html.P("Stara metoda obračunavanja omrežnine:", style={'font-family': 'Arial', 'padding-left': '10px'}),
        html.P(
            "Stara metoda obračunavanja omrežnine temelji na dveh časovnih blokih(mali in veliki tarifi). Porabljena energija v MT in VT se obračuna po določenih cenah za obe tarifi. Poleg storška energije v tarifah pa se doda še strošek obračunske moči. "
            "Celoten strošek omrežnine je torej sestavljen iz dela obračunske moči in energije porabljene v VT in MT. "
            "Cene za tarifi in obračunsko moč se spreminjajo glede na tip merilnega mesta. Cene so torej različlne za gospodijstva, obrate na nizki napetosti, obrate na srednji napetosti itd.",
              style={'font-family': 'Arial', 'padding-left': '10px'}),
        html.P("Nova metoda obračunavanja omrežnine:", style={'font-family': 'Arial', 'padding-left': '10px'}),
        html.P(
            "Nova metoda obračunavanja omrežnine temelji na petih časovnih blokih. V posameznem dnevu lahko nastopijo trije različni časovni bloki. Najdražji bo časovni blok 1, ta se pojavi le v višji sezoni, najcenejša bo uporaba omrežja v časovnem bloku 5, ki nastopi le v nižji sezoni. V višji sezoni so meseci november, december, januar in februar. "
            "V blokih se bo obračunala dogovorjena moč, ki bo določena iz strani odjemalca ali pa izračunana iz mesečnih konic. Poleg obračuna dogovorjene moči pa se bo obračunala tudi energija. Cene za moč in energijo za posamezni blok lahko najdemo na spletni strani Agencije za energijo. Strošek moči in energije petih blokov na koncu predstavlja končno ceno omrežnine izračunane po novi metodi. ",
              style={'font-family': 'Arial', 'padding-left': '10px'}),
            ], style={'border': '3px solid #1156A3'}),


    html.Div([
        html.H2(children='ARSO datoteka o sončni obsevanosti', style={'text-align': 'center', 'color': 'black'}, className='heading2'),
        dcc.Dropdown(
            id='upload_arso_all',
            options=[
                {'label': 'Naloži datoteko', 'value': 'nalozi_datoteko'},
                {'label': 'Povprečna obsevanost - Bežigrad', 'value': 'Bežigrad'},
                {'label': 'Povprečna obsevanost - Celje', 'value': 'Celje'},
                {'label': 'Povprečna obsevanost - Maribor', 'value': 'Maribor'},
                {'label': 'Povprečna obsevanost - Lesce', 'value': 'Lesce'},
                {'label': 'Povprečna obsevanost - Novo mesto', 'value': 'Novo mesto'},
                {'label': 'Povprečna obsevanost - Portorož', 'value': 'Portoroz'},
                {'label': 'Povprečna obsevanost - Murska Sobota', 'value': 'Murska Sobota'},
                {'label': 'Povprečna obsevanost - Postojna', 'value': 'Postojna'},
                {'label': 'Povprečna obsevanost - Ilirska Bistrica', 'value': 'Ilirska Bistrica'},
            ],
            value = 'nalozi_datoteko',
            style={'width': '400px', 'margin': '0 auto', 'display': 'block', 'margin-bottom': '10px'}
        ),
        html.P('ALI', style={'text-align': 'center', 'color': 'black'}, className='heading2'),
        dcc.Upload(
            id='upload-data',
            children=html.Div([
                'Povleci in spusti ali ',
                html.A('Izberi datoteko')
            ]),    
            style={
            'width': '60%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '0 auto'  # Centers the div horizontally
            },
            multiple=False
        ),
        dcc.Loading(html.Div(id='output-datatable'),id="loading_ARSO",type="circle"),
        dcc.Loading(html.Div(id='output-datatable_3'),id="loading_ARSO_all",type="circle"),
    ], style={'text-align': 'center'}),
    
    html.Hr(style={'color': '#1156A3'}, className='hr-style'),

    html.Div([
        html.H2(children='Moj elektro datoteka', style={'text-align': 'center', 'color': 'black'}, className='heading2'),
        dcc.Upload(
            id='upload-data-2',
            children=html.Div([
                'Povleci in spusti ali ',
                html.A("Izberi datoteko")
            ]),    
            style={
            'width': '60%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '0 auto'  # Centers the div horizontally
            },
            multiple=False
        ),
        dcc.Loading(html.Div(id='output-datatable-2'),id="loading_MOJELEKTRO",type="circle"),
    ], style={'text-align': 'center'}),

    html.Hr(style={'color': '#1156A3'}, className='hr-style'),
    dcc.Store(id="Elektro_click", data=0),#daj na nulo potem
    dcc.Store(id="Arso_click", data=0),


    html.Div(id='output-2'),
])

#callback info gumb
@app.callback(
    Output('info-explanation', 'style'),
    [Input('info-button', 'n_clicks')]
)
def toggle_info_content(n_clicks):
    if n_clicks % 2 == 1:
        return {'display': 'block', 'border': '3px solid #1156A3', 'margin': '3px'}
    else:
        return {'display': 'none'}
    
    
#callback pomoč gumb podatki so obvezni in VT MT
@app.callback(
    Output('pomoc_1', 'style'),
    [Input('pomoc_1-button', 'n_clicks')]
)
def toggle_info_content(n_clicks):
    if n_clicks % 2 == 1:
        return {'display': 'block', 'border': '3px solid #1156A3', 'margin': '3px', 'width': '600px', 'margin': '0 auto', "margin-bottom":"10px"}
    else:
        return {'display': 'none'}

#callback pomoč gumb obracunska moc
@app.callback(
    Output('pomoc_2', 'style'),
    [Input('pomoc_2-button', 'n_clicks')]
)
def toggle_info_content(n_clicks):
    if n_clicks % 2 == 1:
        return {'display': 'block', 'border': '3px solid #1156A3', 'margin': '3px', 'width': '500px', 'margin': '0 auto', "margin-bottom":"10px"}
    else:
        return {'display': 'none'}
    
#callback pomoč gumb za tip merilnega mesta
@app.callback(
    Output('pomoc_3', 'style'),
    [Input('pomoc_3-button', 'n_clicks')]
)
def toggle_info_content(n_clicks):
    if n_clicks % 2 == 1:
        return {'display': 'block', 'border': '3px solid #1156A3', 'margin': '3px', 'width': '900px', 'margin': '0 auto', "margin-bottom":"10px"}
    else:
        return {'display': 'none'}
    
#callback pomoč gumb za bloke
@app.callback(
    Output('pomoc_4', 'style'),
    [Input('pomoc_4-button', 'n_clicks')]
)
def toggle_info_content(n_clicks):
    if n_clicks % 2 == 1:
        return {'display': 'block', 'border': '3px solid #1156A3', 'margin': '3px', 'width': '1200px', 'margin': '0 auto', "margin-bottom":"10px"}
    else:
        return {'display': 'none'}
    
#callback pomoč gumb razlaga dimenzioniranja baterije
@app.callback(
    Output('pomoc_5', 'style'),
    [Input('pomoc_5-button', 'n_clicks')]
)
def toggle_info_content(n_clicks):
    if n_clicks % 2 == 1:
        return {'display': 'block', 'border': '3px solid #1156A3', 'margin': '3px', 'width': '1000px', 'margin': '0 auto', "margin-bottom":"10px"}
    else:
        return {'display': 'none'}
    
#callback pomoč gumb zakaj nova priključna moč
@app.callback(
    Output('pomoc_6', 'style'),
    [Input('pomoc_6-button', 'n_clicks')]
)
def toggle_info_content(n_clicks):
    if n_clicks % 2 == 1:
        return {'display': 'block', 'border': '3px solid #1156A3', 'margin': '3px', 'width': '1000px', 'margin': '0 auto', "margin-bottom":"10px"}
    else:
        return {'display': 'none'}

#CALLBACK MOJELEKTRO    
@app.callback(Output('output-datatable-2', 'children'),
              Input('upload-data-2', 'contents'),
              State('upload-data-2', 'filename'),)
def update_output(contents, name):
    if contents is not None:
        children = [
            parse_contents(contents, name)]
        return children

#callback ARSO Dropdpwn
@app.callback(
    Output('output-datatable', 'children'),
    Output("upload-data", "style"),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename'),
    Input('upload_arso_all', 'value')
)
def branje_datotek(contents, name, value):
    if contents is not None and value == "nalozi_datoteko":
        children = [
            razsiri_podatke(contents, name)]
        return [children, {'display': 'none'}]
    if value == "nalozi_datoteko":
        return [html.Div([
        dcc.Store(id='Arso_click', data=0),
        ]),{'width': '60%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '0 auto',
            }]
    elif value == "Bežigrad":
        filename = "osvetljitev_15_bezigrad.xlsx"
        df_result = pd.read_excel("osvetljitev_15_bezigrad.xlsx")

        return [html.Div([
        html.H3('Prebrana datoteka:', style={'display': 'block', 'text-align': 'center', 'marginTop': '10px'}),
        html.H4(filename),
        dcc.Store(id='stored-data', data=df_result.to_dict('records')),
        dcc.Store(id='Arso_click', data=1),
        ]),{'display': 'none'}]

    elif value == "Celje":
        filename = "osvetljitev_15_celje.xlsx"
        df_result = pd.read_excel("osvetljitev_15_celje.xlsx")

        return [html.Div([
        html.H3('Prebrana datoteka:', style={'display': 'block', 'text-align': 'center', 'marginTop': '10px'}),
        html.H4(filename),
        dcc.Store(id='stored-data', data=df_result.to_dict('records')),
        dcc.Store(id='Arso_click', data=1),
        ]),{'display': 'none'}]
    
    elif value == "Maribor":
        filename = "osvetljitev_15_maribor.xlsx"
        df_result = pd.read_excel("osvetljitev_15_maribor.xlsx")

        return [html.Div([
        html.H3('Prebrana datoteka:', style={'display': 'block', 'text-align': 'center', 'marginTop': '10px'}),
        html.H4(filename),
        dcc.Store(id='stored-data', data=df_result.to_dict('records')),
        dcc.Store(id='Arso_click', data=1),
        ]),{'display': 'none'}]
    
    elif value == "Ilirska Bistrica":

        filename = "osvetljitev_15_ilirska_bistrica.xlsx"
        df_result = pd.read_excel("osvetljitev_15_ilirska_bistrica.xlsx")

        return [html.Div([
        html.H3('Prebrana datoteka:', style={'display': 'block', 'text-align': 'center', 'marginTop': '10px'}),
        html.H4(filename),
        dcc.Store(id='stored-data', data=df_result.to_dict('records')),
        dcc.Store(id='Arso_click', data=1),
        ]),{'display': 'none'}]
    
    elif value == "Murska Sobota":
        filename = "osvetljitev_15_murska_sobota.xlsx"
        df_result = pd.read_excel("osvetljitev_15_murska_sobota.xlsx")

        return [html.Div([
        html.H3('Prebrana datoteka:', style={'display': 'block', 'text-align': 'center', 'marginTop': '10px'}),
        html.H4(filename),
        dcc.Store(id='stored-data', data=df_result.to_dict('records')),
        dcc.Store(id='Arso_click', data=1),
        ]),{'display': 'none'}]
    
    elif value == "Lesce":
        filename = "osvetljitev_15_lesce.xlsx"
        df_result = pd.read_excel("osvetljitev_15_lesce.xlsx")

        return [html.Div([
        html.H3('Prebrana datoteka:', style={'display': 'block', 'text-align': 'center', 'marginTop': '10px'}),
        html.H4(filename),
        dcc.Store(id='stored-data', data=df_result.to_dict('records')),
        dcc.Store(id='Arso_click', data=1),
        ]),{'display': 'none'}]
    
    elif value == "Postojna":
        filename = "osvetljitev_15_postojna.xlsx"
        df_result = pd.read_excel("osvetljitev_15_postojna.xlsx")

        return [html.Div([
        html.H3('Prebrana datoteka:', style={'display': 'block', 'text-align': 'center', 'marginTop': '10px'}),
        html.H4(filename),
        dcc.Store(id='stored-data', data=df_result.to_dict('records')),
        dcc.Store(id='Arso_click', data=1),
        ]),{'display': 'none'}]
    
    elif value == "Novo mesto":
        filename = "osvetljitev_15_novo_mesto.xlsx"
        df_result = pd.read_excel("osvetljitev_15_novo_mesto.xlsx")

        return [html.Div([
        html.H3('Prebrana datoteka:', style={'display': 'block', 'text-align': 'center', 'marginTop': '10px'}),
        html.H4(filename),
        dcc.Store(id='stored-data', data=df_result.to_dict('records')),
        dcc.Store(id='Arso_click', data=1),
        ]),{'display': 'none'}]
    
    elif value == "Portoroz":
        filename = "osvetljitev_15_portoroz.xlsx"
        df_result = pd.read_excel("osvetljitev_15_portoroz.xlsx")

        return [html.Div([
        html.H3('Prebrana datoteka:', style={'display': 'block', 'text-align': 'center', 'marginTop': '10px'}),
        html.H4(filename),
        dcc.Store(id='stored-data', data=df_result.to_dict('records')),
        dcc.Store(id='Arso_click', data=1),
        ]),{'display': 'none'}]




#callback za prikaz ostle aplikacije ko se naložita obe datoteki    
@app.callback(Output('output-2', 'children'),
              Input('Elektro_click', 'data'),
              Input('Arso_click', 'data'),)
def update_output(prvi_file, drugi_file):
    children = [
        pokazi_drugi_del_aplikacije(prvi_file, drugi_file)]
    return children

#callback za VT in MT
@app.callback(
    Output("stored_cena_elektrarne", "data"),
    Output("stored_MT", "data"),
    Output("stored_VT", "data"),
    Output("stored_ET", "data"),
    Output("stored_obracunska_moc", "data"),
    Output("stored_prikljucna_moc", "data"),
    Output("stored_nova_prikljucna_moc", "data"),
    Output("stored_tip_merilnega_mesta", "data"),
    Output("stored_povrsina", "data"),
    Output("stored_panel_eff", "data"),
    Output("stored_panel_power", "data"),
    Output("stored_bloki_check", "data"),
    Output("stored_bloki_values", "data"),

    Output("cena_elektrarne", "disabled"),
    Output("MT", "disabled"),
    Output("VT", "disabled"),
    Output("ET", "disabled"),
    Output("obracunska_moc", "disabled"),
    Output("prikljucna_moc", "disabled"),
    Output("tip_merilnega_mesta_dropdown", "disabled"),
    Output("panel_length", "disabled"),
    Output("panel_width", "disabled"),
    Output("panel_eff", "disabled"),
    Output("panel_power", "disabled"),
    Output("nova_prikljucna_moc", "options"),
    Output("bloki", "options"),
    
    Output("lock_button", "style"),
    Output("lock_button", "n_clicks"),
    Output("dinamicni_vhodni_podatki_opozorilo", "children"),
    Output("dinamicni_vhodni_podatki_tretji_del", "children"),

    State(component_id="cena_elektrarne", component_property="value"),
    State(component_id="VT", component_property="value"),
    State(component_id="MT", component_property="value"),
    State(component_id="ET", component_property="value"),
    State(component_id="obracunska_moc", component_property="value"),
    State(component_id="prikljucna_moc", component_property="value"),
    State(component_id="nova_prikljucna_moc", component_property="value"),
    State(component_id="tip_merilnega_mesta_dropdown", component_property="value"),
    State(component_id="panel_length", component_property="value"),
    State(component_id="panel_width", component_property="value"),
    State(component_id="panel_eff", component_property="value"),
    State(component_id="panel_power", component_property="value"),
    State(component_id="bloki", component_property="value"),
    State(component_id="BLOK1", component_property="value"),
    State(component_id="BLOK2", component_property="value"),
    State(component_id="BLOK3", component_property="value"),
    State(component_id="BLOK4", component_property="value"),
    State(component_id="BLOK5", component_property="value"),
    Input(component_id="lock_button", component_property="n_clicks"),
    prevent_initial_call=True,

)  
def shranitev_cen(cena_elektrarne, VT, MT, ET, obracunska_moc, prikljucna_moc, nova_prikljucna_moc, tip_merilnega_mesta, panel_length, panel_width, panel_eff, panel_power, bloki_check, BLOK1, BLOK2, BLOK3, BLOK4, BLOK5, n_clicks):
    if MT is None or VT is None or ET is None or obracunska_moc is None or cena_elektrarne is None or prikljucna_moc is None or tip_merilnega_mesta is None or panel_length is None or panel_width is None or panel_power is None or panel_eff is None or n_clicks is None:#or n_clicks is None
        return 0,0,0,0,0,0,0,0,0,0,0,0,[],False,False,False,False,False,False,False,False,False,False,False,[{'label': 'Pri izračunih upoštevaj novo priključno moč', 'value': 'MOC_YES', "disabled": False}],[{'label': 'Odkleni in upoštevaj ročno vnesene bloke', 'value': 'BLOKI_YES', "disabled": False}], {
                'backgroundColor': '#000000',  # Green background
                'color': 'white',              # White text
                'padding': '10px 20px',        # Padding around the text
                'textAlign': 'center',         # Center text
                'textDecoration': 'none',      # Remove underline
                'display': 'inline-block',     # Inline-block element
                'fontSize': '12px',            # Font size
                'margin': '2px 1px',           # Margin
                'cursor': 'pointer',
                'verticalAlign': 'middle',     # Center text vertically
                'lineHeight': '20px',
                'marginTop': '20px'
            },n_clicks-1, [html.Label('IZPOLNI VSE ZAHTEVANE PODATKE!!!', style={'display': 'block', 'text-align': 'center'}),], []
    if n_clicks % 2 == 1 and (MT is not None and VT is not None and ET is not None and obracunska_moc != 0 and cena_elektrarne != 0 and prikljucna_moc !=0 and tip_merilnega_mesta !=0 and panel_length !=0 and panel_width !=0 and panel_eff !=0 and panel_power !=0):
        if bloki_check == ["BLOKI_YES"]:
            if (BLOK1 is not None and BLOK2 is not None and BLOK3 is not None and BLOK4 is not None and BLOK5 is not None) and (BLOK1 <= BLOK2 <= BLOK3 <= BLOK4 <= BLOK5):
                BLOKI = [BLOK1,BLOK2,BLOK2,BLOK4,BLOK5]  
                return cena_elektrarne, MT, VT, ET, obracunska_moc, prikljucna_moc, nova_prikljucna_moc, tip_merilnega_mesta, panel_length*panel_width, panel_eff, panel_power, bloki_check,BLOKI, True, True,True,True,True,True,True,True,True,True,True,[{'label': 'Pri izračunih upoštevaj novo priključno moč', 'value': 'MOC_YES', "disabled": True}],[{'label': 'Odkleni in upoštevaj ročno vnesene bloke', 'value': 'BLOKI_YES', "disabled": True}], {
                        'backgroundColor': 'green',  # Green background
                        'color': 'white',              # White text
                        'padding': '10px 20px',        # Padding around the text
                        'textAlign': 'center',         # Center text
                        'textDecoration': 'none',      # Remove underline
                        'display': 'inline-block',     # Inline-block element
                        'fontSize': '12px',            # Font size
                        'margin': '2px 1px',           # Margin
                        'cursor': 'pointer',
                        'verticalAlign': 'middle',     # Center text vertically
                        'lineHeight': '20px',
                        'marginTop': '20px'
                    },n_clicks, [], [
                        html.Hr(style={'color': '#1156A3'}, className='hr-style'),
                        html.Div([
                            html.H2(children='Način izračuna', style={'text-align': 'center', 'color': 'black'}, className='heading2'),
                            dcc.RadioItems(
                                options=["Optimalna velikost", "Površina elektrarne[m2]", "Število panelov", "Odstotek samozadostnosti[%]"],
                                value="Število panelov",
                                id="nacin_izracuna"
                            ),
                            html.Div(id='dinamicni_vhodni_podatki',
                                    style={'text-align': 'center'})
                        ], style={'text-align': 'center'}),


                        html.Hr(style={'color': '#1156A3'}, className='hr-style'),

                        html.Div([
                        html.H2(children='Rezultati proizvodnje', style={'text-align': 'center', 'color': 'black'}, className='heading2'),
                        html.Label('DC moč elektrarne[kW]:', style={'display': 'block', 'text-align': 'center'}),
                        html.Div(
                            children="",
                            id= "moc_elektrarne-out"
                        ),
                        html.Label('Celotna poraba[MWh]:', style={'display': 'block', 'text-align': 'center'}),
                        html.Div(
                            children="",
                            id= "celotna_poraba-out"
                        ),
                        html.Label('Proizvodnja brez viškov[MWh]:', style={'display': 'block', 'text-align': 'center'}),
                        html.Div(
                            children="",
                            id= "proizvodnja_brez-out"
                        ),
                        html.Label('Viški[MWh]:', style={'display': 'block', 'text-align': 'center'}),
                        html.Div(
                            children="",
                            id= "viski-out"
                        ),
                        html.Label('Odstotek samozadnostnosti[%]:', style={'display': 'block', 'text-align': 'center'}),
                        html.Div(
                            children="",
                            id= "odstotek_samozadostnosti-out"
                        ),
                        html.Label('Površina elektrarne[m2]:', style={'display': 'block', 'text-align': 'center'}),
                        html.Div(
                            children="",
                            id= "povrsina_elektrarne-out"
                        ),
                        html.Label('Število panelov:', style={'display': 'block', 'text-align': 'center'}),
                        html.Div(
                            children="",
                            id= "stevilo_panelov-out"
                        ),
                        html.Button('Save to Excel', id='save-button', style={
                        'backgroundColor': '#3F9CFF',  # Green background
                        'color': 'white',              # White text
                        'padding': '10px 20px',        # Padding around the text
                        'textAlign': 'center',         # Center text
                        'textDecoration': 'none',      # Remove underline
                        'display': 'inline-block',     # Inline-block element
                        'fontSize': '12px',            # Font size
                        'margin': '2px 1px',           # Margin
                        'cursor': 'pointer',
                        'verticalAlign': 'middle',     # Center text vertically
                        'lineHeight': '20px'   
                    }),
                    dcc.Download(id="download")
                    ], style={'text-align': 'center'}),
                    html.Hr(style={'color': '#1156A3'}, className='hr-style'),
                    html.Div(id='button-container', children=[
                        html.Button('Ekonomika elektrarne', id='ekonomika1-button', style={
                            'backgroundColor': '#000000',  # Black background
                            'color': 'white',              # White text
                            'padding': '10px 20px',        # Padding around the text
                            'textAlign': 'center',         # Center text
                            'textDecoration': 'none',      # Remove underline
                            'display': 'inline-block',     # Inline-block element
                            'fontSize': '12px',            # Font size
                            'margin': '2px 1px',           # Margin
                            'cursor': 'pointer',
                            'verticalAlign': 'middle',     # Center text vertically
                            'lineHeight': '20px',
                        }),
                        html.Button('Dodaj baterijo - osnovno vodenje', id='baterija-button', style={
                            'backgroundColor': '#000000',  # Black background
                            'color': 'white',              # White text
                            'padding': '10px 20px',        # Padding around the text
                            'textAlign': 'center',         # Center text
                            'textDecoration': 'none',      # Remove underline
                            'display': 'inline-block',     # Inline-block element
                            'fontSize': '12px',            # Font size
                            'margin': '2px 1px',           # Margin
                            'cursor': 'pointer',
                            'verticalAlign': 'middle',     # Center text vertically
                            'lineHeight': '20px',
                        }),
                        html.Button('Dodaj baterijo - rezanje konic', id='baterija2-button', style={
                            'backgroundColor': '#000000',  # Black background
                            'color': 'white',              # White text
                            'padding': '10px 20px',        # Padding around the text
                            'textAlign': 'center',         # Center text
                            'textDecoration': 'none',      # Remove underline
                            'display': 'inline-block',     # Inline-block element
                            'fontSize': '12px',            # Font size
                            'margin': '2px 1px',           # Margin
                            'cursor': 'pointer',
                            'verticalAlign': 'middle',     # Center text vertically
                            'lineHeight': '20px',
                        })
                    ], style={
                            'display': 'flex',              # Flexbox layout
                            'justifyContent': 'center',     # Center horizontally
                            'alignItems': 'center',         # Center vertically
                            'gap': '10px'     
                    }),
                    html.Div(id='heading-container'),
                    ]
            else:
                return 0,0,0,0,0,0,0,0,0,0,0,0,[],False,False,False,False,False,False,False,False,False,False,False,[{'label': 'Pri izračunih upoštevaj novo priključno moč', 'value': 'MOC_YES', "disabled": False}],[{'label': 'Odkleni in upoštevaj ročno vnesene bloke', 'value': 'BLOKI_YES', "disabled": False}], {
                    'backgroundColor': '#000000',  # Green background
                    'color': 'white',              # White text
                    'padding': '10px 20px',        # Padding around the text
                    'textAlign': 'center',         # Center text
                    'textDecoration': 'none',      # Remove underline
                    'display': 'inline-block',     # Inline-block element
                    'fontSize': '12px',            # Font size
                    'margin': '2px 1px',           # Margin
                    'cursor': 'pointer',
                    'verticalAlign': 'middle',     # Center text vertically
                    'lineHeight': '20px',
                    'marginTop': '20px'
                },n_clicks-1, [html.Label('PREGLEJ VREDNOSTI BLOKOV!!!', style={'display': 'block', 'text-align': 'center'}),], []
        else:
            return  cena_elektrarne, MT, VT, ET, obracunska_moc, prikljucna_moc, nova_prikljucna_moc, tip_merilnega_mesta, panel_length*panel_width, panel_eff, panel_power, bloki_check,[], True, True, True,True,True,True,True,True,True,True,True,[{'label': 'Pri izračunih upoštevaj novo priključno moč', 'value': 'MOC_YES', "disabled": True}],[{'label': 'Odkleni in upoštevaj ročno vnesene bloke', 'value': 'BLOKI_YES', "disabled": True}], {
                        'backgroundColor': 'green',  # Green background
                        'color': 'white',              # White text
                        'padding': '10px 20px',        # Padding around the text
                        'textAlign': 'center',         # Center text
                        'textDecoration': 'none',      # Remove underline
                        'display': 'inline-block',     # Inline-block element
                        'fontSize': '12px',            # Font size
                        'margin': '2px 1px',           # Margin
                        'cursor': 'pointer',
                        'verticalAlign': 'middle',     # Center text vertically
                        'lineHeight': '20px',
                        'marginTop': '20px'
                    },n_clicks, [], [
                        html.Hr(style={'color': '#1156A3'}, className='hr-style'),
                        html.Div([
                            html.H2(children='Način izračuna', style={'text-align': 'center', 'color': 'black'}, className='heading2'),
                            dcc.RadioItems(
                                options=["Optimalna velikost", "Površina elektrarne[m2]", "Število panelov", "Odstotek samozadostnosti[%]"],
                                value="Število panelov",
                                id="nacin_izracuna"
                            ),
                            html.Div(id='dinamicni_vhodni_podatki',
                                    style={'text-align': 'center'})
                        ], style={'text-align': 'center'}),


                        html.Hr(style={'color': '#1156A3'}, className='hr-style'),

                        dcc.Loading([html.Div([
                        html.H2(children='Rezultati proizvodnje', style={'text-align': 'center', 'color': 'black'}, className='heading2'),
                        html.Label('DC moč elektrarne[kW]:', style={'display': 'block', 'text-align': 'center'}),
                        html.Div(
                            children="",
                            id= "moc_elektrarne-out"
                        ),
                        html.Label('Celotna poraba[MWh]:', style={'display': 'block', 'text-align': 'center'}),
                        html.Div(
                            children="",
                            id= "celotna_poraba-out"
                        ),
                        html.Label('Proizvodnja brez viškov[MWh]:', style={'display': 'block', 'text-align': 'center'}),
                        html.Div(
                            children="",
                            id= "proizvodnja_brez-out"
                        ),
                        html.Label('Viški[MWh]:', style={'display': 'block', 'text-align': 'center'}),
                        html.Div(
                            children="",
                            id= "viski-out"
                        ),
                        html.Label('Odstotek samozadnostnosti[%]:', style={'display': 'block', 'text-align': 'center'}),
                        html.Div(
                            children="",
                            id= "odstotek_samozadostnosti-out"
                        ),
                        html.Label('Površina elektrarne[m2]:', style={'display': 'block', 'text-align': 'center'}),
                        html.Div(
                            children="",
                            id= "povrsina_elektrarne-out"
                        ),
                        html.Label('Število panelov:', style={'display': 'block', 'text-align': 'center'}),
                        html.Div(
                            children="",
                            id= "stevilo_panelov-out"
                        ),
                        html.Button('Save to Excel', id='save-button', style={
                        'backgroundColor': '#3F9CFF',  # Green background
                        'color': 'white',              # White text
                        'padding': '10px 20px',        # Padding around the text
                        'textAlign': 'center',         # Center text
                        'textDecoration': 'none',      # Remove underline
                        'display': 'inline-block',     # Inline-block element
                        'fontSize': '12px',            # Font size
                        'margin': '2px 1px',           # Margin
                        'cursor': 'pointer',
                        'verticalAlign': 'middle',     # Center text vertically
                        'lineHeight': '20px'   
                    }),
                    dcc.Download(id="download")
                    ], style={'text-align': 'center'}),],id="loading_izračun_proizvodnje", overlay_style={"visibility":"visible"},type="dot"),
                    html.Hr(style={'color': '#1156A3'}, className='hr-style'),
                    html.Div(id='button-container', children=[
                        html.Button('Ekonomika elektrarne', id='ekonomika1-button', style={
                            'backgroundColor': '#000000',  # Black background
                            'color': 'white',              # White text
                            'padding': '10px 20px',        # Padding around the text
                            'textAlign': 'center',         # Center text
                            'textDecoration': 'none',      # Remove underline
                            'display': 'inline-block',     # Inline-block element
                            'fontSize': '12px',            # Font size
                            'margin': '2px 1px',           # Margin
                            'cursor': 'pointer',
                            'verticalAlign': 'middle',     # Center text vertically
                            'lineHeight': '20px',
                        }),
                        html.Button('Dodaj baterijo - osnovno vodenje', id='baterija-button', style={
                            'backgroundColor': '#000000',  # Black background
                            'color': 'white',              # White text
                            'padding': '10px 20px',        # Padding around the text
                            'textAlign': 'center',         # Center text
                            'textDecoration': 'none',      # Remove underline
                            'display': 'inline-block',     # Inline-block element
                            'fontSize': '12px',            # Font size
                            'margin': '2px 1px',           # Margin
                            'cursor': 'pointer',
                            'verticalAlign': 'middle',     # Center text vertically
                            'lineHeight': '20px',
                        }),
                        html.Button('Dodaj baterijo - rezanje konic', id='baterija2-button', style={
                            'backgroundColor': '#000000',  # Black background
                            'color': 'white',              # White text
                            'padding': '10px 20px',        # Padding around the text
                            'textAlign': 'center',         # Center text
                            'textDecoration': 'none',      # Remove underline
                            'display': 'inline-block',     # Inline-block element
                            'fontSize': '12px',            # Font size
                            'margin': '2px 1px',           # Margin
                            'cursor': 'pointer',
                            'verticalAlign': 'middle',     # Center text vertically
                            'lineHeight': '20px',
                        })
                    ], style={
                            'display': 'flex',              # Flexbox layout
                            'justifyContent': 'center',     # Center horizontally
                            'alignItems': 'center',         # Center vertically
                            'gap': '10px'     
                    }),
                    html.Div(id='heading-container'),
                    ]                
    elif n_clicks % 2 == 0 and (MT is not None and VT is not None and ET is not None and obracunska_moc != 0 and cena_elektrarne != 0 and prikljucna_moc !=0 and tip_merilnega_mesta !=0 and panel_length !=0 and panel_width !=0 and panel_eff !=0 and panel_power !=0):
        return 0,0,0,0,0,0,0,0,0,0,0,0,[],False,False,False,False,False,False,False,False,False,False,False,[{'label': 'Pri izračunih upoštevaj novo priključno moč', 'value': 'MOC_YES', "disabled": False}],[{'label': 'Odkleni in upoštevaj ročno vnesene bloke', 'value': 'BLOKI_YES', "disabled": False}], {
                'backgroundColor': '#000000',  # Green background
                'color': 'white',              # White text
                'padding': '10px 20px',        # Padding around the text
                'textAlign': 'center',         # Center text
                'textDecoration': 'none',      # Remove underline
                'display': 'inline-block',     # Inline-block element
                'fontSize': '12px',            # Font size
                'margin': '2px 1px',           # Margin
                'cursor': 'pointer',
                'verticalAlign': 'middle',     # Center text vertically
                'lineHeight': '20px',
                'marginTop': '20px'
            },n_clicks, [html.Label('PREGLEJ IN KLIKNI ŠE ENKRAT', style={'display': 'block', 'text-align': 'center'}),],[]
    else:
        return 0,0,0,0,0,0,0,0,0,0,0,0,[],False,False,False,False,False,False,False,False,False,False,False,[{'label': 'Pri izračunih upoštevaj novo priključno moč', 'value': 'MOC_YES', "disabled": False}],[{'label': 'Odkleni in upoštevaj ročno vnesene bloke', 'value': 'BLOKI_YES', "disabled": False}], {
                'backgroundColor': '#000000',  # Green background
                'color': 'white',              # White text
                'padding': '10px 20px',        # Padding around the text
                'textAlign': 'center',         # Center text
                'textDecoration': 'none',      # Remove underline
                'display': 'inline-block',     # Inline-block element
                'fontSize': '12px',            # Font size
                'margin': '2px 1px',           # Margin
                'cursor': 'pointer',
                'verticalAlign': 'middle',     # Center text vertically
                'lineHeight': '20px',
                'marginTop': '20px'
            }, n_clicks-1,[html.Label('PREGLEJ PODATKE!!!', style={'display': 'block', 'text-align': 'center'}),], []


#callback za zaklepanje blokov
@app.callback(
    Output("BLOK1", "disabled"),
    Output("BLOK2", "disabled"),
    Output("BLOK3", "disabled"),
    Output("BLOK4", "disabled"),
    Output("BLOK5", "disabled"),

    Input(component_id="bloki", component_property="value"),
    Input(component_id="lock_button", component_property="n_clicks"),
    prevent_initial_call=True,

)
def zaklepanje_blokov(bloki_check, n_clicks):
    if n_clicks is None or n_clicks % 2 == 0:
        if bloki_check == ["BLOKI_YES"]:
            return False, False, False, False, False  
        else:
            return True, True, True, True, True
    else:
        return True, True, True, True, True




#callback za tip odjema
@app.callback(
    Output("stored_VT_omrez", "data"),
    Output("stored_MT_omrez", "data"),
    Output("stored_ET_omrez", "data"),
    Output("stored_obracunska_cena", "data"),
    Output("stored_cena_blok_moc", "data"),
    Output("stored_cena_blok_energija", "data"),
    Input(component_id="stored_tip_merilnega_mesta", component_property="data"),
)
def določitev_tarife(tip_merilnega_mesta):
    if  tip_merilnega_mesta == "Gospodinjstvo_dvotarifni":
        return VT_o, MT_o, 0, obracunska_moc_cena, cene_bloki_moc_0, cene_bloki_energija_0
    elif tip_merilnega_mesta == "Gospodinjstvo_enotarifni":
        return 0, 0, ET_o, obracunska_moc_cena, cene_bloki_moc_0, cene_bloki_energija_0
    elif  tip_merilnega_mesta == "Poslovni_odjem_NN_T≥2500":
            return VT_v_2500_NN, MT_v_2500_NN, 0, obrm_v_2500_NN, cene_bloki_moc_0, cene_bloki_energija_0
    elif tip_merilnega_mesta == "Poslovni_odjem_NN_T<2500":
            return VT_m_2500_NN, MT_m_2500_NN, 0, obrm_m_2500_NN, cene_bloki_moc_0, cene_bloki_energija_0
    elif tip_merilnega_mesta == "Poslovni_odjem_NN_zbiralke_T≥2500":
            return VT_v_2500_z_NN, MT_v_2500_z_NN, 0, obrm_v_2500_z_NN, cene_bloki_moc_1, cene_bloki_energija_1
    elif tip_merilnega_mesta == "Poslovni_odjem_NN_zbiralke_T<2500":
            return VT_m_2500_z_NN, MT_m_2500_z_NN, 0, obrm_m_2500_z_NN, cene_bloki_moc_1, cene_bloki_energija_1
    elif tip_merilnega_mesta == "Poslovni_odjem_SN_T≥2500":
            return VT_v_2500_SN, MT_v_2500_SN, 0, obrm_v_2500_SN, cene_bloki_moc_2, cene_bloki_energija_2
    elif tip_merilnega_mesta == "Poslovni_odjem_SN_T<2500":
            return VT_m_2500_SN, MT_m_2500_SN, 0, obrm_m_2500_SN, cene_bloki_moc_2, cene_bloki_energija_2
    elif tip_merilnega_mesta == "Poslovni_odjem_SN_zbiralke_T≥2500":
            return VT_v_2500_z_SN, MT_v_2500_z_SN, 0, obrm_v_2500_z_SN, cene_bloki_moc_3, cene_bloki_energija_3
    elif tip_merilnega_mesta == "Poslovni_odjem_SN_zbiralke_T<2500":
            return VT_m_2500_z_SN, MT_m_2500_z_SN, 0, obrm_m_2500_z_SN, cene_bloki_moc_3, cene_bloki_energija_3
    else:
        return 0,0,0,0,0,0
    
#callback za obravnaje gumba v rdeče, če ni izpolnjen pogoj vt mt
@app.callback(
    Output('tip_merilnega_mesta_dropdown', 'style'),
    #Output("vrednost", "value"),
    Input('tip_merilnega_mesta_dropdown', 'value'),
    Input(component_id="VT", component_property="value"),
    Input(component_id="MT", component_property="value"),
    Input(component_id="ET", component_property="value"),
    prevent_initial_call=True,   
)
def rdec_gumb(tip_merilnega_mesta, VT, MT, ET):
    if tip_merilnega_mesta == "Gospodinjstvo_enotarifni" and ET == 0:
        return {'width': "400px", 'margin': '0 auto', 'display': 'block','background-color': 'red'}
    elif tip_merilnega_mesta == "Gospodinjstvo_dvotarifni" and (VT == 0 or MT == 0):
        return {'width': '400px', 'margin': '0 auto', 'display': 'block', 'background-color': 'red'}
    else: 
        return {'width': '400px', 'margin': '0 auto', 'display': 'block', 'background-color': 'white'}

    

#callback za določitev katerie vhodne podatke potrebujemo
@app.callback(
    Output('dinamicni_vhodni_podatki', 'children'),
    #Output("vrednost", "value"),
    Input('nacin_izracuna', 'value')
)
def display_dynamic_input(nacin_izracuna):
    if nacin_izracuna == 'Optimalna velikost':
        return [html.Label(["Način \"Optimalna velikost\" dimenzionira velikost FV elektrarne tako, da z algoritmom linearnga programiranja poišče najnižji mesečni strošek za naslednjih 15 let.", html.Br(), "Rezultat je torej odvisen od cene lektrične energije in cene investicije v FV elektrarno.", html.Br(), "Omeniti je potrebno, da ta minimumu ni najkrajša vračilna doba investicije."],
                            style={'display': 'block', 'text-align': 'center','border': '3px solid #1156A3', 'width': '1100px', 'margin': '0 auto'})]
    else:
        return [html.Label('Vrednost:', style={'display': 'block', 'text-align': 'center'}), dcc.Input(id='vrednost', value=0, type='number', placeholder='Vnesite vrednost', style={'width': '10%', 'margin': '0 auto', 'display': 'block'}),]

#callback za vrednost
@app.callback(
    Output("stored_vrednost", "data"),
    #Output("vrednost-out", "children"),
    Input(component_id="vrednost", component_property="value")
)  
def vrednost(vrednost):
    if vrednost is None:
        vrednost = 0.1#mogoče je lahko bolje
        return vrednost
    else:    
        return vrednost#, f'Vnesena vrednost: {vrednost}'



#callback za nacin izračuna
@app.callback(
    Output("stored_nacin_izracuna", "data"),
    #Output("vrednost-out", "children"),
    Input(component_id="nacin_izracuna", component_property="value")
)  
def vrednost2(nacin_izracuna):
    if nacin_izracuna is None:
        nacin_izracuna = 0
    return nacin_izracuna

#callback za reset vrednosti
@app.callback(
    Output("vrednost", "value"),
    Input("vrednost", "value"),
    Input("stored_nacin_izracuna", "data"),
    Input(component_id="nacin_izracuna", component_property="value")
)  
def osvezi(vrednost, nacin_izracuna, stored_nacin_izracuna):
    if nacin_izracuna == stored_nacin_izracuna:
        return vrednost
    else:
        return 0#, f'Vnesena vrednost: {vrednost}'
    
    
#callback za prenos podatkov v exel od sončne
@callback(
    Output("download", "data"),
    Input("save-button", "n_clicks"),
    State("izvoz-podatki", "data"),
    prevent_initial_call=True,      
)
def shrani_excel(n_clicks, data):
    if n_clicks:
        # Convert the data to a pandas DataFrame
        df = pd.DataFrame(data)
        df = df.rename(columns={
            'Energija A+': 'Odjem[kWh]',
            'razlika': 'Razlika odjem-proizvodnja_15[kWh]',
            'proizvodnja_15': 'proizvodnja_15[kWh]',
        })
        df = df.drop(columns=['proizvodnja_15_norm'])
    return dcc.send_data_frame(df.to_excel, "data_PV.xlsx", index=False)

    
#callback za prenos podatkov v exel od baterije
@callback(
    Output("download_bat", "data"),
    Input("save-batery-button", "n_clicks"),
    State("izvoz-podatki_bat", "data"),
    prevent_initial_call=True,      
)
def shrani_excel_bat(n_clicks, data):
    if n_clicks:
        # Convert the data to a pandas DataFrame
        df = pd.DataFrame(data)
        df['Battery power'] = df['Battery power'] / 4
        df = df.rename(columns={
            'Energija A+': 'Odjem[kWh]',
            'razlika': 'Razlika odjem-proizvodnja_15[kWh]',
            'proizvodnja_15': 'proizvodnja_15[kWh]',
            "Battery power":"Delovanje_baterije[kWh]",
            "Koncni_profil":"Razlika odjem-proizvodnja_15-delovanje_baterije[kWh]",
        })
        df = df.drop(columns=["Month","Hour","Day","Sezona","Dela prost dan","Tarifa","Blok",'proizvodnja_15_norm',"Strosek PV & BESS","BESS", "SoC"])# izbriši SoC
    return dcc.send_data_frame(df.to_excel, "data_batery.xlsx", index=False)


# Define the callback
@app.callback(
    #Output('button-container', 'children'),
    Output('stored_baterija-button', 'data'),
    Output('stored_baterija2-button', 'data'),
    Output('ekonomika1-button', 'n_clicks'),
    Output('baterija-button', 'n_clicks'),
    Output('baterija2-button', 'n_clicks'),
    Output('heading-container', 'children'),
    Input('ekonomika1-button', 'n_clicks'),
    Input('baterija-button', 'n_clicks'),
    Input('baterija2-button', 'n_clicks'),
    allow_duplicate=True

)
def update_buttons(n_clicks_ekonomika, n_clicks_baterija, n_clicks_baterija2):
    # Check which button was clicked and update the layout accordingly
    if n_clicks_ekonomika :
        return (0,0,0,0,0,
            html.Div([
                html.H2('Rezultati ekonomika', style={'text-align': 'center', 'color': 'black'}, className='heading2'),
                html.Label('Cena investicije v FV elektrarno[€]:', style={'display': 'block', 'text-align': 'center'}),
                html.Div(id="investicija-out"),
                html.H4('Izračun cene po stari metodi', style={'text-align': 'center', 'color': 'black'}),
                html.Label('Cena stare omreznine z davkom[€]:', style={'display': 'block', 'text-align': 'center'}),
                html.Div(id="omreznina_stara_brez-out"),
                html.Label('Celoten letni strošek brez FV elektrarne[€]:', style={'display': 'block', 'text-align': 'center'}),
                html.Div(id="let_strosek_stara-out"),
                html.Label('Prihranek ko dodamo FV elektrarno[€]:', style={'display': 'block', 'text-align': 'center'}),
                html.Div(id="prihranek_stara-out"),
                html.Label('Enostavna vračilna doba po stari metodi[Leta]:', style={'display': 'block', 'text-align': 'center'}),
                html.Div(id="vracilna_doba_stara-out"),
                html.H4('Izračun cene po novi metodi', style={'text-align': 'center', 'color': 'black'}),
                html.Label('Dogovorjene moči po blokih brez elektrarne[kW]:', style={'display': 'block', 'text-align': 'center'}),
                dash_table.DataTable(
                    id='tabela_blokov_stari',
                    columns=[
                        {'name': 'Blok 1', 'id': 'Column 1'},
                        {'name': 'Blok 2', 'id': 'Column 2'},
                        {'name': 'Blok 3', 'id': 'Column 3'},
                        {'name': 'Blok 4', 'id': 'Column 4'},
                        {'name': 'Blok 5', 'id': 'Column 5'}
                    ],
                    #data=initial_data,
                    style_table={'width': '250px', 'margin': '0 auto'},
                    style_cell={
                        'textAlign': 'left',
                        'minWidth': '50px', 'width': '50px', 'maxWidth': '50px',  # Fixed width for all columns
                        'whiteSpace': 'normal',
                        'padding': '2px',         # Reduced padding
                        'lineHeight': '15px',
                    },
                    style_header={
                        'backgroundColor': 'white',  # Header background color
                        'color': 'black',            # Header text color
                        'border': '1px solid black',      
                        'lineHeight': '10px',  # Header border
                    },style_data={
                        'backgroundColor': 'white',  # Data cell background color
                        'color': 'black',            # Data cell text color
                        'border': '1px solid black', # Data cell border
                    },
                    style_data_conditional=[
                        {
                            'if': {'state': 'selected'},
                            'backgroundColor': 'white',  # Cell background color when selected
                            'color': 'black',
                            'border': '1px solid black'           # Cell text color when selected
                        }
                    ],
                ),
                html.Label('Dogovorjene moči po blokih z elektrarno[kW]:', style={'display': 'block', 'text-align': 'center'}),
                dash_table.DataTable(
                    id='tabela_blokov_novi',
                    columns=[
                        {'name': 'Blok 1', 'id': 'Column 1'},
                        {'name': 'Blok 2', 'id': 'Column 2'},
                        {'name': 'Blok 3', 'id': 'Column 3'},
                        {'name': 'Blok 4', 'id': 'Column 4'},
                        {'name': 'Blok 5', 'id': 'Column 5'}
                    ],
                    #data=initial_data,
                    style_table={'width': '250px', 'margin': '0 auto'},
                    style_cell={
                        'textAlign': 'left',
                        'minWidth': '50px', 'width': '50px', 'maxWidth': '50px',  # Fixed width for all columns
                        'whiteSpace': 'normal',
                        'padding': '2px',         # Reduced padding
                        'lineHeight': '10px',
                    },
                    style_header={
                        'backgroundColor': 'white',  # Header background color
                        'color': 'black',            # Header text color
                        'border': '1px solid black',      
                        'lineHeight': '10px',  # Header border
                    },style_data={
                        'backgroundColor': 'white',  # Data cell background color
                        'color': 'black',            # Data cell text color
                        'border': '1px solid black', # Data cell border
                    },
                    style_data_conditional=[
                        {
                            'if': {'state': 'selected'},
                            'backgroundColor': 'white',  # Cell background color when selected
                            'color': 'black',
                            'border': '1px solid black'           # Cell text color when selected
                        }
                    ],
                ),
                html.Label('Nova priključna moč:', style={'display': 'block', 'text-align': 'center'}),
                html.Div(id="nova_prikljucna_moc_PV-out"),
                html.Label('Cena nove omreznine z davkom brez FV elektrarne[€]:', style={'display': 'block', 'text-align': 'center'}),
                html.Div(id="omreznina_nova_brez-out"),
                html.Label('Celoten letni strošek brez FV elektrarne[€]:', style={'display': 'block', 'text-align': 'center'}),
                html.Div(id="let_strosek_nova-out"),
                html.Label('Prihranek ko dodamo FV elektrarno[€]:', style={'display': 'block', 'text-align': 'center'}),
                html.Div(id="prihranek_nova-out"),
                html.Label('Enostavna vračilna doba FV elektrarne[Leta]:', style={'display': 'block', 'text-align': 'center'}),
                html.Div(id="vracilna_doba_nova-out")
            ], style={'text-align': 'center'}),  # Heading content
    
        )
    elif n_clicks_baterija:
        return(1,0,0,0,0,
            dcc.Loading([html.Div([
                html.Div(id="velikost_bat",style={'display': 'none'}),#skriti div da deluje dcc.Loading za baterijo
                html.Label('Cena BHEE[€/kWh]:', style={'display': 'block', 'text-align': 'center', 'marginTop': '10px'}),
                dcc.Input(id="cena_baterije", value=400, type='number', placeholder='Vnesite vrednost', style={'width': '10%', 'margin': 'auto', 'display': 'block', 'text-align': 'center'}),
                html.Label(
                    ['POČAKAJ NEKAJ TRENUTKOV!!!'],
                    style={'whiteSpace': 'pre-line', 'text-align': 'center', 'marginTop': '10px', 'font-size': '24px'}
                ),
                html.Label(
                    ['Algoritem izračuna oprimalne velikosti baterije potrebuje nekaj sekund, včasih več minut.'],
                    style={'whiteSpace': 'pre-line', 'text-align': 'center', 'font-size': '16px'}
                ),

                html.H2('Rezultati dodane baterije - osnovno vodenje', style={'text-align': 'center', 'color': 'black'}, className='heading2'),               
                html.Button('Pomoč!', id='pomoc_5-button', n_clicks=0,
                    style={'border': 'none', 'font-size': '12px',
                            'top': '10px', 'right': '10px'}, className='my-button'),
                html.Div(id='pomoc_5', children=['BHEE je dimenzioniran na velikost, ki zagotovi najnižjo mesečno ceno investicije in stroškov za naslednjih 10 let.', html.Br(),
                        'Najmanjša vrednost BHEE je 50 kWh, moč baterije pa je vedno polovica njene kapacitete.'],
                        style={'display': 'block', 'text-align': 'center', 'marginBottom': '10px', 'font-size': '12px'}),
                html.Label('Kapaciteta baterije[kWh]:', style={'display': 'block', 'text-align': 'center'}),
                html.Div(id="kapaciteta_bat-out"),
                html.Label('Moč baterije[kW]:', style={'display': 'block', 'text-align': 'center'}),
                html.Div(id="moc_bat-out"),
                html.Label('Cena investicije FV el. in BHEE[€]:', style={'display': 'block', 'text-align': 'center'}),
                html.Div(id="investicija_skupno-out"),
                html.H4('Izračun cene po stari metodi', style={'text-align': 'center', 'color': 'black'}),
                html.Label('Letna cena el. energije brez FV el. in BHEE[€]:', style={'display': 'block', 'text-align': 'center'}),
                html.Div(id="cena_stara-out"),
                html.Label('Letna cena el. energije z FV el. in BHEE[€]:', style={'display': 'block', 'text-align': 'center'}),
                html.Div(id="cena_skupen_stara-out"),
                html.Label('Prihranek obračunan po stari metodi[€]:', style={'display': 'block', 'text-align': 'center'}),
                html.Div(id="prihranek_skupen_stara-out"),
                html.Label('Enostavna vračilna doba po stari metodi[Leta]:', style={'display': 'block', 'text-align': 'center'}),
                html.Div(id="vracilna_doba_skupna_stara-out"),
                html.H4('Izračun cene po novi metodi', style={'text-align': 'center', 'color': 'black'}),
                html.Label('Dogovorjene moči po blokih z FV el. in BHEE[kW]:', style={'display': 'block', 'text-align': 'center'}),
                dash_table.DataTable(
                    id='tabela_blokov_baterija',
                    columns=[
                        {'name': 'Blok 1', 'id': 'Column 1'},
                        {'name': 'Blok 2', 'id': 'Column 2'},
                        {'name': 'Blok 3', 'id': 'Column 3'},
                        {'name': 'Blok 4', 'id': 'Column 4'},
                        {'name': 'Blok 5', 'id': 'Column 5'}
                    ],
                    #data=initial_data,
                    style_table={'width': '250px', 'margin': '0 auto'},
                    style_cell={
                        'textAlign': 'left',
                        'minWidth': '50px', 'width': '50px', 'maxWidth': '50px',  # Fixed width for all columns
                        'whiteSpace': 'normal',
                        'padding': '2px',         # Reduced padding
                        'lineHeight': '15px',
                    },
                    style_header={
                        'backgroundColor': 'white',  # Header background color
                        'color': 'black',            # Header text color
                        'border': '1px solid black',      
                        'lineHeight': '10px',  # Header border
                    },style_data={
                        'backgroundColor': 'white',  # Data cell background color
                        'color': 'black',            # Data cell text color
                        'border': '1px solid black', # Data cell border
                    },
                    style_data_conditional=[
                        {
                            'if': {'state': 'selected'},
                            'backgroundColor': 'white',  # Cell background color when selected
                            'color': 'black',
                            'border': '1px solid black'           # Cell text color when selected
                        }
                    ],
                ),
                html.Label('Nova priključna moč:', style={'display': 'block', 'text-align': 'center'}),
                html.Div(id="nova_prikljucna_moc-out"),
                html.Label('Letna cena el. energije z FV el. in BHEE[€]:', style={'display': 'block', 'text-align': 'center'}),
                html.Div(id="cena_skupen_nova-out"),
                html.Label('Prihranek obračunan po novi metodi[€]:', style={'display': 'block', 'text-align': 'center'}),
                html.Div(id="prihranek_skupen_nova-out"),
                html.Label('Enostavna vračilna doba po novi metodi[Leta]:', style={'display': 'block', 'text-align': 'center'}),
                html.Div(id="vracilna_doba_skupna_nova-out"),

                html.Hr(style={'color': '#1156A3'}, className='hr-style'),
                html.Label('Shrani profile baterije v excel', style={'display': 'block', 'text-align': 'center'}),
                html.Button('Save to Excel', id='save-batery-button', style={
                'backgroundColor': '#3F9CFF',  # Green background
                'color': 'white',              # White text
                'padding': '10px 20px',        # Padding around the text
                'textAlign': 'center',         # Center text
                'textDecoration': 'none',      # Remove underline
                'display': 'inline-block',     # Inline-block element
                'fontSize': '12px',            # Font size
                'margin': '2px 1px',           # Margin
                'cursor': 'pointer',
                'verticalAlign': 'middle',     # Center text vertically
                'lineHeight': '20px'   
            }),
            dcc.Download(id="download_bat"),
            ], style={'text-align': 'center'})],id="loading_izračun_baterija", type="dot",overlay_style={"visibility":"visible"}),  # Heading content
        )
    elif n_clicks_baterija2:
        return(0,1,0,0,0,
            dcc.Loading([html.Div([
                html.Div(id="velikost_bat",style={'display': 'none'}),#skriti div da deluje dcc.Loading za baterijo
                html.Label('Cena BHEE[€/kWh]:', style={'display': 'block', 'text-align': 'center', 'marginTop': '10px'}),
                dcc.Input(id="cena_baterije", value=400, type='number', placeholder='Vnesite vrednost', style={'width': '10%', 'margin': 'auto', 'display': 'block', 'text-align': 'center'}),
                html.Label('Kapaciteta BHEE[kWh]:', style={'display': 'block', 'text-align': 'center', 'marginTop': '10px'}),
                dcc.Input(id="kapaciteta_baterije_rezanje_konic", value=50, type='number', placeholder='Vnesite vrednost', style={'width': '10%', 'margin': 'auto', 'display': 'block', 'text-align': 'center'}),
                html.Label(
                    ['POČAKAJ NEKAJ TRENUTKOV!!!'],
                    style={'whiteSpace': 'pre-line', 'text-align': 'center', 'marginTop': '10px', 'font-size': '24px'}
                ),
                html.Label(
                    ['Algoritem izračuna oprimalne velikosti baterije potrebuje nekaj sekund, včasih več minut.'],
                    style={'whiteSpace': 'pre-line', 'text-align': 'center', 'font-size': '16px'}
                ),

                html.H2('Rezultati dodane baterije - rezanje konic', style={'text-align': 'center', 'color': 'black'}, className='heading2'),               
                html.Button('Pomoč!', id='pomoc_5-button', n_clicks=0,
                    style={'border': 'none', 'font-size': '12px',
                            'top': '10px', 'right': '10px'}, className='my-button'),
                html.Div(id='pomoc_5', children=['BHEE je dimenzioniran na velikost, ki zagotovi najnižjo mesečno ceno investicije in stroškov za naslednjih 10 let.', html.Br(),
                        'Najmanjša vrednost BHEE je 50 kWh, moč baterije pa je vedno polovica njene kapacitete.'],
                        style={'display': 'block', 'text-align': 'center', 'marginBottom': '10px', 'font-size': '12px'}),
                html.Label('Kapaciteta baterije[kWh]:', style={'display': 'block', 'text-align': 'center'}),
                html.Div(id="kapaciteta_bat-out"),
                html.Label('Moč baterije[kW]:', style={'display': 'block', 'text-align': 'center'}),
                html.Div(id="moc_bat-out"),
                html.Label('Cena investicije FV el. in BHEE[€]:', style={'display': 'block', 'text-align': 'center'}),
                html.Div(id="investicija_skupno-out"),
                html.H4('Izračun cene po stari metodi', style={'text-align': 'center', 'color': 'black'}),
                html.Label('Letna cena el. energije brez FV el. in BHEE[€]:', style={'display': 'block', 'text-align': 'center'}),
                html.Div(id="cena_stara-out"),
                html.Label('Letna cena el. energije z FV el. in BHEE[€]:', style={'display': 'block', 'text-align': 'center'}),
                html.Div(id="cena_skupen_stara-out"),
                html.Label('Prihranek obračunan po stari metodi[€]:', style={'display': 'block', 'text-align': 'center'}),
                html.Div(id="prihranek_skupen_stara-out"),
                html.Label('Enostavna vračilna doba po stari metodi[Leta]:', style={'display': 'block', 'text-align': 'center'}),
                html.Div(id="vracilna_doba_skupna_stara-out"),
                html.H4('Izračun cene po novi metodi', style={'text-align': 'center', 'color': 'black'}),
                html.Label('Dogovorjene moči po blokih z FV el. in BHEE[kW]:', style={'display': 'block', 'text-align': 'center'}),
                dash_table.DataTable(
                    id='tabela_blokov_baterija',
                    columns=[
                        {'name': 'Blok 1', 'id': 'Column 1'},
                        {'name': 'Blok 2', 'id': 'Column 2'},
                        {'name': 'Blok 3', 'id': 'Column 3'},
                        {'name': 'Blok 4', 'id': 'Column 4'},
                        {'name': 'Blok 5', 'id': 'Column 5'}
                    ],
                    #data=initial_data,
                    style_table={'width': '250px', 'margin': '0 auto'},
                    style_cell={
                        'textAlign': 'left',
                        'minWidth': '50px', 'width': '50px', 'maxWidth': '50px',  # Fixed width for all columns
                        'whiteSpace': 'normal',
                        'padding': '2px',         # Reduced padding
                        'lineHeight': '15px',
                    },
                    style_header={
                        'backgroundColor': 'white',  # Header background color
                        'color': 'black',            # Header text color
                        'border': '1px solid black',      
                        'lineHeight': '10px',  # Header border
                    },style_data={
                        'backgroundColor': 'white',  # Data cell background color
                        'color': 'black',            # Data cell text color
                        'border': '1px solid black', # Data cell border
                    },
                    style_data_conditional=[
                        {
                            'if': {'state': 'selected'},
                            'backgroundColor': 'white',  # Cell background color when selected
                            'color': 'black',
                            'border': '1px solid black'           # Cell text color when selected
                        }
                    ],
                ),
                html.Label('Nova priključna moč:', style={'display': 'block', 'text-align': 'center'}),
                html.Div(id="nova_prikljucna_moc-out"),
                html.Label('Letna cena el. energije z FV el. in BHEE[€]:', style={'display': 'block', 'text-align': 'center'}),
                html.Div(id="cena_skupen_nova-out"),
                html.Label('Prihranek obračunan po novi metodi[€]:', style={'display': 'block', 'text-align': 'center'}),
                html.Div(id="prihranek_skupen_nova-out"),
                html.Label('Enostavna vračilna doba po novi metodi[Leta]:', style={'display': 'block', 'text-align': 'center'}),
                html.Div(id="vracilna_doba_skupna_nova-out"),

                html.Hr(style={'color': '#1156A3'}, className='hr-style'),
                html.Label('Shrani profile baterije v excel', style={'display': 'block', 'text-align': 'center'}),
                html.Button('Save to Excel', id='save-batery-button', style={
                'backgroundColor': '#3F9CFF',  # Green background
                'color': 'white',              # White text
                'padding': '10px 20px',        # Padding around the text
                'textAlign': 'center',         # Center text
                'textDecoration': 'none',      # Remove underline
                'display': 'inline-block',     # Inline-block element
                'fontSize': '12px',            # Font size
                'margin': '2px 1px',           # Margin
                'cursor': 'pointer',
                'verticalAlign': 'middle',     # Center text vertically
                'lineHeight': '20px'   
            }),
            dcc.Download(id="download_bat"),
            ], style={'text-align': 'center'})],id="loading_izračun_baterija", type="dot",overlay_style={"visibility":"visible"}),  # Heading content
        )
    else:
        return (0,0,0,0,0,
        
        '', # No heading text initially

    )

#callback za ceno baterije
@app.callback(
    Output("stored_cena_baterije", "data"),
    Input("cena_baterije", "value"),
)  
def stored_baterija(cena_baterije):
    if cena_baterije is not None:
        return cena_baterije
    else:
        return 0
    
#callback za kapaciteto baterije
@app.callback(
    Output("stored_kapaciteta_baterije_rezanje_konic", "data"),
    Input("kapaciteta_baterije_rezanje_konic", "value"),
)  
def stored_baterija(kapaciteta_baterije_rezanje_konic):
    if kapaciteta_baterije_rezanje_konic is not None:
        return kapaciteta_baterije_rezanje_konic
    else:
        return 0


@app.callback(
    Output("moc_elektrarne-out", "children"),
    Output("celotna_poraba-out", "children"),
    Output("proizvodnja_brez-out", "children"),
    Output("viski-out", "children"),
    Output("odstotek_samozadostnosti-out", "children"),
    Output("povrsina_elektrarne-out", "children"),
    Output("stevilo_panelov-out", "children"),
    Output("izvoz-podatki", "data"),
    Input(component_id="nacin_izracuna", component_property="value"),
    State(component_id="stored_panel_power", component_property="data"),
    State(component_id="stored_povrsina", component_property="data"),
    State(component_id="stored_panel_eff", component_property="data"),
    Input(component_id="stored_vrednost", component_property="data"),#mogoče je lahko bolje
    State(component_id="stored_cena_elektrarne", component_property="data"),
    State(component_id="stored_VT", component_property="data"),
    State(component_id="stored_MT", component_property="data"),
    State(component_id="stored_ET", component_property="data"),
    State(component_id="stored_VT_omrez", component_property="data"),
    State(component_id="stored_MT_omrez", component_property="data"),
    State(component_id="stored_ET_omrez", component_property="data"),
    State(component_id="stored_obracunska_cena", component_property="data"),
    State(component_id="stored_obracunska_moc", component_property="data"),
    State(component_id="stored-data", component_property="data"),       
    State(component_id="stored-data-2", component_property="data"),
    prevent_initial_call=True

)
def izracun_moci(nacin_izracuna, moč_panela, povrsina_panela, eff_panela, vrednost, cena_elektrarne, VT, MT, ET, VT_omrez, MT_omrez, ET_omrez, obracunska_moc_cena, obracunska_moc, osvetljenost, poraba):
    if (moč_panela == 0) or (povrsina_panela ==0) or (eff_panela == 0) or (vrednost is None) or (moč_panela == 0) or (povrsina_panela == 0) or (eff_panela == 0)  or (MT is None) or (VT is None)  or (ET is None) or (obracunska_moc == 0):
        return 0,0,0,0,0,0,0,0
    osvetljenost = pd.DataFrame.from_dict(osvetljenost)
    poraba = pd.DataFrame.from_dict(poraba)
    osvetljenost["Datum in cas"] = pd.to_datetime(osvetljenost['Datum in cas'])
    poraba['Časovna značka'] = pd.to_datetime(poraba['Časovna značka'])
    leto_osvetljenost = osvetljenost["Datum in cas"].iloc[0].year
    leto_poraba = poraba['Časovna značka'].iloc[0].year

    if leto_osvetljenost == 2000:
        osvetljenost["Datum in cas"] = osvetljenost["Datum in cas"].apply(
        lambda x: x.replace(year=leto_poraba))


    stevilo_panelov_1kW = 1000/moč_panela
    moc_15=povrsina_panela*stevilo_panelov_1kW*osvetljenost['Soncno sevanje (W/m2)']*eff_panela/100*izkoristek_razsmenrika
    osvetljenost["proizvodnja_15_norm"] = moc_15*0.25/1000# v kWh

    all = pd.merge(poraba, osvetljenost, left_on="Časovna značka", right_on="Datum in cas")
    all["index_dneva"] = all["Časovna značka"].dt.date
    all=dela_prost_dan(all)
    all=tarifa(all)
    all=bloki(all)
    celotna_poraba = all["Energija A+"].sum()

    if nacin_izracuna == "Število panelov":
        multiplikator = vrednost*moč_panela/1000
        all["proizvodnja_15"] = all["proizvodnja_15_norm"]*multiplikator
        all["razlika"]=all["Energija A+"]-all["proizvodnja_15"]

    elif nacin_izracuna == "Površina elektrarne[m2]":
        zeljeno_stevilo_panelov = vrednost/povrsina_panela
        multiplikator = zeljeno_stevilo_panelov*moč_panela/1000
        all["proizvodnja_15"] = all["proizvodnja_15_norm"]*multiplikator
        all["razlika"]=all["Energija A+"]-all["proizvodnja_15"]

    elif nacin_izracuna == "Odstotek samozadostnosti[%]":
        
        potrebna_proizvodnja = vrednost/100*celotna_poraba
        multiplikator = 1
        j = -1
        dejanska_proizvodnja = 0

        all["proizvodnja_15"] = all["proizvodnja_15_norm"]*multiplikator
        while j < 0:
            if potrebna_proizvodnja > dejanska_proizvodnja and multiplikator < 3000:
                multiplikator += 1
                all["proizvodnja_15"] = all["proizvodnja_15_norm"]*multiplikator
                all["razlika"]= all["Energija A+"] - all["proizvodnja_15"]
                pozit_razlika =  all["razlika"][all["razlika"] > 0].dropna().sum()
                dejanska_proizvodnja = all["Energija A+"].sum() - pozit_razlika
            else:
                j = 1
                break
    elif  nacin_izracuna == "Optimalna velikost":
        bounds_x1 = (1,3000)
        x0 = np.array([300])
        result = minimize(objective_fun, x0, method="SLSQP", bounds=[bounds_x1], args=(cena_elektrarne, obracunska_moc, VT, MT, ET, all, VT_omrez, MT_omrez, ET_omrez, obracunska_moc_cena))
        # Print the result
        multiplikator = result.x[0]
        multiplikator = int(multiplikator)
        
        all["proizvodnja_15"] = all["proizvodnja_15_norm"]*multiplikator
        all["razlika"]=all["Energija A+"]-all["proizvodnja_15"]

    pozit_razlika =  all["razlika"][all["razlika"] > 0].dropna().sum()
    celotna_poraba = all["Energija A+"].sum()

    pozitivna_proizvodnja = celotna_poraba - pozit_razlika

    viski = all["razlika"][all["razlika"] < 0].dropna().sum()

    procent = pozitivna_proizvodnja/celotna_poraba*100


    povrsina_elektrarne = multiplikator*1000/moč_panela*povrsina_panela

    stevilo_panelov = multiplikator*1000/450

    selected_columns = ['Časovna značka', 'index_dneva', "Month", "Hour", "Day", "Sezona", "Dela prost dan", "Tarifa", "Blok", 'Energija A+', 'proizvodnja_15_norm', 'proizvodnja_15', 'razlika']
    df_result = all[selected_columns]
    df_result_dict = df_result.to_dict('records')
    return round(multiplikator,1), round(celotna_poraba/1000,2), round(pozitivna_proizvodnja/1000,2), round(viski/1000,2), round(procent,2),  round(povrsina_elektrarne,0), round(stevilo_panelov,0), df_result_dict #


@app.callback(
    Output("investicija-out", "children"),
    Output("omreznina_stara_brez-out", "children"),
    Output("let_strosek_stara-out", "children"),
    Output("prihranek_stara-out", "children"),
    Output("vracilna_doba_stara-out", "children"),
    Input(component_id="izvoz-podatki", component_property="data"),
    State(component_id="stored_VT", component_property="data"),
    State(component_id="stored_MT", component_property="data"),
    State(component_id="stored_ET", component_property="data"),
    State(component_id="stored_cena_elektrarne", component_property="data"),
    State(component_id="stored_obracunska_moc", component_property="data"),
    State(component_id="stored_VT_omrez", component_property="data"),
    State(component_id="stored_MT_omrez", component_property="data"),
    State(component_id="stored_ET_omrez", component_property="data"),
    State(component_id="stored_obracunska_cena", component_property="data"),
)
def ekonomika_FV_stara(data, VT, MT, ET, cena_elektrarne, obracunska_moc, VT_omrez, MT_omrez, ET_omrez, obracunska_moc_cena):
    data = pd.DataFrame.from_dict(data)
    cena_old, cena_new, omreznina_stara, stran_dej= izračun_cene_el_energije(obracunska_moc, VT, MT, ET, data, VT_omrez, MT_omrez, ET_omrez, obracunska_moc_cena, "razlika")
    strosek_old = data["Energija A+"].sum()*cena_old
    strosek_new = data[data["razlika"]>0]["razlika"].sum() * cena_new
    pv_power=(data['proizvodnja_15']/data['proizvodnja_15_norm']).mean()
    investicija = pv_power*cena_elektrarne
    strosek_new_zavarovanje = strosek_new + investicija*1.05/100
    prihranek = strosek_old - (strosek_new_zavarovanje)#nekisneki
    vracilna_doba = investicija/prihranek

    if prihranek < 0:
        vracilna_doba = "Prihrankek je manjši od zavarovanja(1.05% procenta investicije)"
    else:
        vracilna_doba = round(investicija/prihranek,1)
        if vracilna_doba > 20:
            vracilna_doba = "Investicija ni upravičena."


    return locale.format_string("%d", round(investicija,0), grouping=True), locale.format_string("%d", round(omreznina_stara,0), grouping=True), locale.format_string("%d", round(strosek_old,0), grouping=True), locale.format_string("%d", round(prihranek,0), grouping=True), vracilna_doba

@app.callback(
    Output("tabela_blokov_stari", "data"),
    Output("tabela_blokov_novi", "data"),
    Output("nova_prikljucna_moc_PV-out", "children"),
    Output("omreznina_nova_brez-out", "children"),
    Output("let_strosek_nova-out", "children"),
    Output("prihranek_nova-out", "children"),
    Output("vracilna_doba_nova-out", "children"),
    Input(component_id="izvoz-podatki", component_property="data"),
    State(component_id="stored_prikljucna_moc", component_property="data"),
    State(component_id="stored_nova_prikljucna_moc", component_property="data"),
    State(component_id="stored_obracunska_moc", component_property="data"),
    State(component_id="stored_VT", component_property="data"),
    State(component_id="stored_MT", component_property="data"),
    State(component_id="stored_ET", component_property="data"),
    State(component_id="stored_cena_elektrarne", component_property="data"),
    State(component_id="stored_cena_blok_moc", component_property="data"),
    State(component_id="stored_cena_blok_energija", component_property="data"),
    State(component_id="stored_bloki_check", component_property="data"),
    State(component_id="stored_bloki_values", component_property="data"),
    

)
def ekonomika_FV_nova(data, prikljucna_moc, nova_prikljucna_moc, obracunska_moc, VT, MT, ET, cena_elektrarne, cena_blok_moc, cena_blok_energija, bloki_check, bloki_values):
    data = pd.DataFrame.from_dict(data)

    if prikljucna_moc <= 17:
        delez = 27
    elif prikljucna_moc > 17 and prikljucna_moc <=43:
        delez = 34
    elif prikljucna_moc > 43:
        delez = 25

    pv_power=(data['proizvodnja_15']/data['proizvodnja_15_norm']).mean()
    investicija = pv_power*cena_elektrarne
    bloki_brez, omreznina_nova_brez, koncna_cena_brez, nova_prikljucna_moc_value_old = izracun_cene_nova(data, prikljucna_moc, nova_prikljucna_moc, obracunska_moc, VT, MT, ET, delez, "Energija A+", cena_blok_moc, cena_blok_energija, bloki_check, bloki_values)
    bloki_z_PV, omreznina_nova_z_PV, koncna_cena_z_PV, nova_prikljucna_moc_value = izracun_cene_nova(data, prikljucna_moc, nova_prikljucna_moc, obracunska_moc, VT, MT, ET, delez, "razlika", cena_blok_moc, cena_blok_energija, bloki_check, bloki_values)
    koncna_cena_z_PV_zavarovanje = koncna_cena_z_PV + investicija*1.05/100
    prihranek = koncna_cena_brez - (koncna_cena_z_PV_zavarovanje)
    vracilna_doba = investicija/prihranek

    if prihranek < 0:
        vracilna_doba = "Prihrankek je manjši od zavarovanja(1.05% procenta investicije)"
    else:
        vracilna_doba = round(investicija/prihranek,1)
        if vracilna_doba > 20:
            vracilna_doba = "Investicija ni upravičena."

    return [{"Column 1" : bloki_brez[0],"Column 2" :bloki_brez[1],"Column 3" : bloki_brez[2],"Column 4" : bloki_brez[3],"Column 5" : bloki_brez[4]}], [{"Column 1" : bloki_z_PV[0],"Column 2" :bloki_z_PV[1],"Column 3" : bloki_z_PV[2],"Column 4" : bloki_z_PV[3],"Column 5" : bloki_z_PV[4]}],nova_prikljucna_moc_value, locale.format_string("%d", round(omreznina_nova_brez,0), grouping=True), locale.format_string("%d", round(koncna_cena_brez), grouping=True), locale.format_string("%d", round(prihranek), grouping=True), vracilna_doba



#callback za velikost baterije
@app.callback(
    Output("stored_velikost_bat", "data"),
    Output("velikost_bat", "value"),
    Output("izvoz-podatki_bat","data"),
    State(component_id="stored_baterija-button", component_property='data'),
    State(component_id="stored_baterija2-button", component_property='data'),
    State(component_id="izvoz-podatki", component_property="data"),
    State(component_id="stored_MT", component_property="data"),
    State(component_id="stored_VT", component_property="data"),
    State(component_id="stored_ET", component_property="data"),
    Input(component_id="stored_cena_baterije", component_property="data"),
    Input(component_id="stored_kapaciteta_baterije_rezanje_konic", component_property="data"),
    State(component_id="stored_cena_elektrarne", component_property="data"),
    State(component_id="stored_prikljucna_moc", component_property="data"),
    prevent_initial_call=True
)
def velikost_bat(baterija1, baterija2, data, VT, MT, ET, BEES_price, kapaciteta_baterije_rezanje_konic, cena_elektrarne, prikljucna_moc):
    data = pd.DataFrame.from_dict(data)
    kapaciteta = 0
    if data is None or VT is None or MT is None or ET is None or BEES_price is None or cena_elektrarne is None:
        return 0,0,0
    else:

        if prikljucna_moc <= 17:
            bounds_x1 = (2,50)

        elif prikljucna_moc > 17 and prikljucna_moc <=43:
            bounds_x1 = (20,80)

        elif prikljucna_moc > 43:
            bounds_x1 = (50,1500)

        if baterija1:
            x0 = np.array([50])
            result = minimize(izračun_batt_osnovna,x0, method="L-BFGS-B",  bounds=[bounds_x1], args=(data, VT, MT, ET, BEES_price, cena_elektrarne))#, constraints=[constrain1])
            kapaciteta = result.x[0]
        elif baterija2:
            kapaciteta, data = izračun_batt_rezanje_konic(kapaciteta_baterije_rezanje_konic, data, VT, MT, ET, BEES_price, cena_elektrarne)

        data_dict = data.to_dict('records')
    data_dict = data.to_dict('records')
    return kapaciteta, kapaciteta, data_dict


#callback za ekonomiko baterije po stari metodi
@app.callback(
    Output("kapaciteta_bat-out", "children"),
    Output("moc_bat-out", "children"),
    Output("investicija_skupno-out", "children"),
    Output("cena_stara-out", "children"),
    Output("cena_skupen_stara-out", "children"),
    Output("prihranek_skupen_stara-out", "children"),
    Output("vracilna_doba_skupna_stara-out", "children"),
    State(component_id="izvoz-podatki_bat", component_property="data"),
    State(component_id="stored_VT", component_property="data"),
    State(component_id="stored_MT", component_property="data"),
    State(component_id="stored_ET", component_property="data"),
    State(component_id="stored_cena_baterije", component_property="data"),
    State(component_id="stored_cena_elektrarne", component_property="data"),
    Input(component_id="stored_velikost_bat", component_property="data"),
    State(component_id="stored_obracunska_moc", component_property="data"),
    State(component_id="stored_VT_omrez", component_property="data"),
    State(component_id="stored_MT_omrez", component_property="data"),
    State(component_id="stored_ET_omrez", component_property="data"),
    State(component_id="stored_obracunska_cena", component_property="data"),
    prevent_initial_call=True
)
def ekonomika_stara_baterija(data, VT, MT, ET, BEES_price, cena_elektrarne, kapaciteta,  obracunska_moc, VT_omrez, MT_omrez, ET_omrez, obracunska_moc_cena):
    data = pd.DataFrame.from_dict(data)
    cena_old, cena_new, omreznina_stara, omreznina_nova_old = izračun_cene_el_energije(obracunska_moc, VT, MT, ET, data, VT_omrez, MT_omrez, ET_omrez, obracunska_moc_cena, "BESS")
    strosek_old = data["Energija A+"].sum()*cena_old
    strosek_new = data[data["BESS"]>0]["BESS"].sum() * cena_new
    pv_power=(data['proizvodnja_15']/data['proizvodnja_15_norm']).mean()
    investicija = pv_power*cena_elektrarne + BEES_price*kapaciteta
    strosek_new_zavarovanje = strosek_new + investicija*1.05/100
    prihranek = strosek_old - (strosek_new_zavarovanje)
    if prihranek < 0:
        vracilna_doba = "Prihrankek je manjši od zavarovanja(1.05% procenta investicije)"
    else:
        vracilna_doba = round(investicija/prihranek,1)
        if vracilna_doba > 20:
            vracilna_doba = "Investicija ni upravičena."

    return locale.format_string("%d", round(kapaciteta,0), grouping=True), locale.format_string("%d", round(kapaciteta/2,0), grouping=True), locale.format_string("%d", round(investicija,0), grouping=True), locale.format_string("%d", round(strosek_old,0), grouping=True), locale.format_string("%d", round(strosek_new_zavarovanje,0), grouping=True), locale.format_string("%d", round(prihranek,0), grouping=True),  vracilna_doba


#callback omrežnina nova z baterijo
@app.callback(
    Output("tabela_blokov_baterija", "data"),
    Output("nova_prikljucna_moc-out", "children"),
    Output("cena_skupen_nova-out", "children"),
    Output("prihranek_skupen_nova-out", "children"),
    Output("vracilna_doba_skupna_nova-out", "children"),
    Input(component_id="izvoz-podatki_bat", component_property="data"),
    State(component_id="stored_prikljucna_moc", component_property="data"),
    State(component_id="stored_nova_prikljucna_moc", component_property="data"),
    State(component_id="stored_obracunska_moc", component_property="data"),
    State(component_id="stored_VT", component_property="data"),
    State(component_id="stored_MT", component_property="data"),
    State(component_id="stored_ET", component_property="data"),
    State(component_id="stored_cena_elektrarne", component_property="data"),
    State(component_id="stored_cena_blok_moc", component_property="data"),
    State(component_id="stored_cena_blok_energija", component_property="data"),
    State(component_id="stored_cena_baterije", component_property="data"),
    Input(component_id="stored_velikost_bat", component_property="data"),
    State(component_id="stored_bloki_check", component_property="data"),
    State(component_id="stored_bloki_values", component_property="data"),
)
def ekonomika_baterija_nova(data, prikljucna_moc, nova_prikljucna_moc, obracunska_moc, VT, MT, ET, cena_elektrarne, cena_blok_moc, cena_blok_energija, cena_baterije, velikost_bat, bloki_check, bloki_values):
    data = pd.DataFrame.from_dict(data)

    if prikljucna_moc <= 17:
        delez = 27
    elif prikljucna_moc > 17 and prikljucna_moc <=43:
        delez = 34
    elif prikljucna_moc > 43:
        delez = 25

    pv_power=(data['proizvodnja_15']/data['proizvodnja_15_norm']).mean()
    investicija = pv_power*cena_elektrarne + velikost_bat*cena_baterije
    

    bloki_brez, omreznina_nova_brez, koncna_cena_brez, nova_prikljucna_moc_value_old= izracun_cene_nova(data, prikljucna_moc, nova_prikljucna_moc, obracunska_moc, VT, MT, ET, delez, "Energija A+", cena_blok_moc, cena_blok_energija, bloki_check, bloki_values)
    bloki_z_BHEE, omreznina_nova_z_PV, koncna_cena_z_BHEE, nova_prikljucna_moc_value = izracun_cene_nova(data, prikljucna_moc, nova_prikljucna_moc, obracunska_moc, VT, MT, ET, delez, "BESS", cena_blok_moc, cena_blok_energija, bloki_check, bloki_values)
    koncna_cena_z_BHEE_zavaro = koncna_cena_z_BHEE + investicija*1.05/100    
    prihranek = koncna_cena_brez - (koncna_cena_z_BHEE_zavaro)
    if prihranek < 0:
        vracilna_doba = "Prihrankek je manjši od zavarovanja(1.05% procenta investicije)"
    else:
        vracilna_doba = round(investicija/prihranek,1)
        if vracilna_doba > 20:
            vracilna_doba = "Investicija ni upravičena."


    return [{"Column 1" : bloki_z_BHEE[0],"Column 2" :bloki_z_BHEE[1],"Column 3" : bloki_z_BHEE[2],"Column 4" : bloki_z_BHEE[3],"Column 5" : bloki_z_BHEE[4]}], nova_prikljucna_moc_value, locale.format_string("%d", round(koncna_cena_z_BHEE_zavaro), grouping=True), locale.format_string("%d", round(prihranek), grouping=True), vracilna_doba
    

#pogon aplikacije
if __name__ == '__main__':
    app.run(debug=False) #port added MP open http://127.0.0.1:8054/ in browser