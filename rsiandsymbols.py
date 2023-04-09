# #!/usr/bin/env python3
# # -*- coding: utf-8 -*-
# """
# Created on Fri Mar 10 14:36:18 2023

# @author: fnurakeshwer
# """

import yfinance
import pandas as pd
import requests
import yfinance as yf
# =============================================================================
# import statistics as st
# =============================================================================
import pandas_ta as pta
from reading_database import read_database




def getTicker(company_name):
    yfinance = "https://query2.finance.yahoo.com/v1/finance/search"
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    params = {"q": company_name, "quotes_count": 1, "country": "Germany"}

    res = requests.get(url=yfinance, params=params, headers={'User-Agent': user_agent})
    data = res.json()
    company_code = data['quotes'][0]['symbol']

    return company_code


def get_symbols(df_m1):
    symbols = []
    print("before databbase in sybmol")
    #
    # df_from_database = read_database()
    # df_1 = df_from_database[df_from_database['Indexes']=="DAX"]
    # df_2= df_from_database[df_from_database['Indexes']=="MDAX"]
    # df_3= df_from_database[df_from_database['Indexes']=="SDAX"]
    # df_4= df_from_database[df_from_database['Indexes']=="TecDAX"]
    # df_5= df_from_database[df_from_database['Indexes']=="CDAX"]
    # df_6= df_from_database[df_from_database['Indexes']=="Scale"]
    # df_7 =df_from_database[df_from_database['Indexes']=="Dow-Jones"]
    # df_14 =df_from_database[df_from_database['Indexes']=="EURO-STOXX-50"]
    # df_15 = df_from_database[df_from_database['Indexes']=="STOXX-Europe-600"]
    
    # # welt calculation
    # dd1 = df_7.append(df_14, ignore_index=True)
    # df_welt = dd1.append(df_15, ignore_index=True)
    
    # #calculation of deu
    # df_d1  = df_1.append(df_2, ignore_index=True)
    # df_d2 = df_d1.append(df_3, ignore_index=True)
    # df_d3 = df_d2.append(df_4, ignore_index=True)
    # df_deu = df_d3.append(df_5, ignore_index=True) 
    
    # #df_master 
    # df_master = df_deu.append(df_welt, ignore_index=True)
    
    # #start from here addition and 
    # df_master['points'] = df_master['dividend'] + df_master['high_growth'] + df_master['leverman']
    
    # #df_master=df_master.drop_duplicates(subset = "stockname")
    
    # #start from here addition and 
    # df_master['points'] = df_master['dividend'] + df_master['high_growth'] + df_master['leverman']
     
    # df_m1 =  df_master.sort_values(by=['points'])
    # #df_m1 = df_m1[df_m1['points']>20]
    # df_m1 = df_m1.iloc[:,[0,1,2,3,6,4,5]] #0,7,1,2,3,6,4,5
    
    # df_m1 = df_m1[df_m1['points']>20]    # get symbols of only who has more than 20 points
    print("after databbase in sybmol")

    # df_m1 = df_m1[df_m1['points']>20] 
    see = True
    for k in df_m1['stockname']:
        if k=='Klöckner & Co':
            k='Kloeckner'
        if k == "Hannover Rück":
            k = "Hannover"
        if k == "Hermès (Hermes International)":
            k = 'Hermes International SA'
        if k == "DWS (Deutsche Asset Management)":
            k = 'DWS Group GmbH & Co. KGaA'
        if k == "Neste Oil":
            k = 'Neste Oyj'
        if k == "KSB vz":
            k = 'KSB SE & Co. KGaA'
        if k == "BMW Vz":
            k = 'Bayerische Motoren Werke Aktiengesellschaft'  
        if k == "Mercedes-Benz Group (Daimler)":
            k = 'Mercedes-Benz Group AG'     
        if k == "LOréal":
            k = 'Loreal'
        if k == "Volkswagen VZ":
            k = 'Volkswagen AG'
        if k == "Muehl Prod.+serv.":
            k = 'Muehlhan AG'
        if k == "A.P. Møller-Mærsk":
            k = 'A.P.'        
        if k == "Kühne + Nagel International":
            k = 'Kuehne + Nagel International AG'
        if k == "TC Unterhaltungselektronik":
            k = 'TC Unterhaltungselek'
        if k == "Travel24com":
              k = 'Travel + Leisure Co'
        if k == "Metro Vz.":
              k = 'Metro AG'
        if k == "Hesse Newman":
              k = 'Hess Corporation'
        if k == "Teles Inform.tech.":
              k = 'Teles AG'
        if k == "Value Management & Research":
            k = 'E-mini Russell'
        if k == "TTL Information Technology":
            k = 'TTL Beteiligungs'
        if k == "Rhön Klinikum":
            k = 'RHK.DE'
        if k == "Pittler Maschinenfabik":
            k = 'Pittler Maschine' 
        if k == "Westag & Getalit vz":
            k = 'Westag'    
        if k == "1&1 Drillisch":
            k = '1&1 AG'     
        if k == "Drägerwerk":
            k = 'DRGN.DE'
        if k == "B.R.A.I.N.":
            k = 'BRAIN Biotech AG'
        if k == "Borussia Dortmund BVB":
            k = 'Borussia Dortmund'
           
        if k == "Eisen- und Hüttenwerke":
            k = 'Eisen- und'   
           
           
        if k == "Westag & Getalit":
            k = 'Westag AG'   
        
        
        if k == "SÜSS MicroTec":
            k = 'SÜSS'   
        
        if k == "Dr. Hönle":
            k = 'Dr. Hö'   
        
        if k == "Südzucker":
            k = 'Süd'   
        
        if k == "Fresenius Medical Care AG & Co. KGaA Sponsored ADR":
            k = 'Fresenius Medical Care AG'   
         
        if k == "Münchener Rück":
            k = 'Münc' 

        if k == "KAP-Beteiligungs-AG":
            k = 'KAP' 
        
        if k == "pbb (Deutsche Pfandbriefbank)":
            k = 'PBB.DE' 
        
        if k == "Ströer":
            k = 'Stratec SE'
           
        if k == "Deutsche Börse":
            k = 'Deutsche Bö'

        if k == "Porsche Holding Vz.":
            k = 'Porsche'
           
        if k == "Bastei Lübbe":
            k = 'Bastei'
        
        if k == "A.S. Création Tapeten":
            k = 'TAV Havalimanlari Holding'

    
        if k == "Müller - Die lila Logistik":
            k = 'Müll'
        
        if k == "IXX.DE":
            k = 'Init Innovation in Traffic Syst'
        
        if k == "Sixt vz":
            k = 'Sixt'
        
        if k == "New Work (Xing)":
            k = 'nwo.de'
           
        if k == "HHLA (Hamburger Hafen)":
            k = 'HHLA'
        
        if k == "Fuchs Petrolub ST":
            k = 'Fuchs Petrolub'
        
        if k == "Volkswagen St (VW)":
            k = 'Volkswagen'

        if k == "Wüstenrot & Württembergische AG":
            k = 'Wüste'      
          
        if k == "Ringmetall":
            k = 'HP3A.DE'      
        
        if k == "MPC Münchmeyer Petersen Capital":
            k = 'MPC'      
              
        if k == "ExxonMobil":
            k = 'Exxon'      
        if k == "Kiniksa Pharmaceuticals Ltd. Class A":
            k = 'Kiniksa Pharmaceuticals Ltd.'  
        
        if k == "Bel Fuse Inc. Class B":
            k = 'Bel Fuse Inc.' 
          
        if k == "Grupo Aeroportuario del Centro Norte SAB de CV Sponsored ADR Class B":
            k = 'Grupo Aeroportuario del Centro'
        
        if k == "VEON Ltd. Sponsored ADR":
            k = 'VEON Ltd.' 
        
        if k == "ChipMOS TECHNOLOGIES INC Sponsored ADR":
            k = 'ChipMOS'
        
        if k == "Bel Fuse Inc. Class A":
            k = 'Bel Fuse'
        
        if k == "Sociedad Quimica Y Minera De Chile S.A. Sponsored ADR Pfd Class B":
            k = 'Sociedad Quimica Y Minera'
         
        if k == "Petroleo Brasileiro SA ADR":
            k = 'Petroleo Brasileiro SA'  
         
        if k == "Gerdau S.A. Sponsored ADR Pfd":
            k = 'Gerdau S.A'     
        
        if k == "Bancolombia S.A. Sponsored ADR Pfd":
            k = 'Bancolombia S.A'     
       
        if k == "ASE Industrial Holding Co., Ltd. Sponsored ADR":
            k = 'ASE Industrial Holding Co'     
             
        if k == "ASE Industrial Holding Co":
            k = 'ASE'
             
        if k == "Grupo Aeroportuario del Pacifico SAB de CV Sponsored ADR Class B":
            k = 'Grupo Aeroportuario del Pacifico'
        if k == "Federal Agricultural Mortgage Corporation Class C":
            k = 'Federal Agricultural Mortgage Corporation'
        if k == "Enel Chile SA Sponsored ADR":
            k = 'Enel Chile SA'
        
        if k == "Brady Corporation Class A":
            k = 'Brady Corporation'
            
        if k == "Ciner Resources LP":
            k = 'Ciner'
        
        if k == "Hubbell Incorporated Class B":
            k = 'Hubbell Incorporated'
        if k == "LaZBoy Incorporated":
            k = 'Lazy'
        if k == "Coca-Cola FEMSA SAB de CV Sponsored ADR Class L":
            k = 'Coca-Cola FEMSA'
        
        if k == "United Microelectronics Corp. Sponsored ADR":
            k = 'United Microelectronics Corp.'
        
        if k == "Ternium S.A. Sponsored ADR":
            k = 'Ternium S.A.'
        
        if k == "Grupo Aeroportuario del Sureste SA de CV Sponsored ADR Class B":
            k = 'Grupo Aeroportuario del'
        if k == "Banco Santander (Brasil) S.A. Sponsored ADR":
            k = 'Banco Santander (Brasil)'
        if k == "Equinor ASA Sponsored ADR":
            k = 'Equinor ASA'
        if k == "Tenaris S.A. Sponsored ADR":
            k = 'Tenaris S.A'
        if k == "Banco Macro SA Sponsored ADR Class B":
            k = 'Banco Macro SA'
        if k == "BancorpSouth Bank":
            k = 'Bancorp'
        if k == "Cadence Bancorporation Class A":
            k = 'Cadence Ban'
        if k == "HollyFrontier Corporation":
            k = 'Holly'
        
        if k == "Triton International Ltd. Class A":
            k = 'Triton International Ltd.'

        if k == "Black Stone Minerals LP":
            k = 'Black Stone Minerals'        
             
        if k == "Bonanza Creek Energy Inc":
            k = 'Bonanza'  
        if k == "Teekay Tankers Ltd. Class A":
            k = 'Teekay Tankers Ltd.'  
        if k == "Arch Coal":
            k = 'Arch'             
        if k == "Banco de Chile Sponsored ADR":
            k = 'Banco de Chile'             
        if k == "KRUK Spólka Akcyjna":
           k = 'KRUK Spó'             
        if k == "Mitsui OSKLines":
           k = 'Mitsui'             
        if k == "Nippon Yusen KK (NYK line)":
           k = 'Nippon Yusen'             
        if k == "Kia Motors":
           k = 'kia corpo'             
      
        print('k : '+ k)
        name = getTicker(k)
        print('name : '+ name)
        symbols.append(name)
        print(len(symbols))
    
    df_m1['symbols'] = symbols
    return df_m1
    
    # rsi_inclusion
def rsi_tool(df_m1):
    rsi_list = []
    for p in df_m1['symbols']:
        ticker = yf.Ticker(p)
        df_prices = ticker.history(interval='1d')
        df1 = pta.rsi(df_prices['Close'], length = 14)  # fourteen days!
        print(p +"/n")
        rsi_list.append(df1[-1])
        
    df_m1['RSI'] = rsi_list
    
    df_rsi_limit1 = df_m1[df_m1['RSI'].between(30,70)]
    df_rsi_limit2 = df_m1[df_m1['RSI'].between(0,30)]
    df_rsi_limit3 = df_m1[df_m1['RSI'].between(70,100)]
    
    df_rsi_limit1['RSI_signal'] = 'Hold'
    df_rsi_limit2['RSI_signal'] = 'Buy_check_price'
    df_rsi_limit3['RSI_signal'] = 'Sell_with_price'
    
    df3 = pd.concat([df_rsi_limit1,df_rsi_limit2], ignore_index=True)
    df_rsi_signal = pd.concat([df3,df_rsi_limit3], ignore_index=True)
    
    df_m1 = df_rsi_signal # this dataframe is populated.
    return df_m1


