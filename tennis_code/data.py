
import pandas as pd
import requests
import json

def _player_names(n):
    if pd.isna(n):
        return n
    return "".join(i.capitalize() for i in n.split())



def _download_player_data(n):
    format_name= _player_names(n)
    link= f"https://www.tennisabstract.com/jsmatches/{format_name}Career.js"
    request_result= requests.get(link, timeout=20)

    if not request_result.ok:
        raise ValueError(f"The player you entered is invalid, we were not able to find data for '{n}'" 
                         f"(HTTP{request_result.status_code})")
        
    return request_result.text


def _convert_java(raw):
    new_data= raw.split("=",1)[1].strip().rstrip(";")
    convert_str= json.loads(new_data)
    return pd.DataFrame(convert_str)

def _create_df(df):
#point is to take the converted df and grab the relevant details
#We want date of match, dob of the player + all opponents + win/loss + tournament name
    data = df.rename(columns={0: "Date", 1: "Tournament", 2: "Surface", 4: "Result"
                             , 11: "Opponent", 16: "Opponent DoB"})
    data=data[['Date','Tournament','Surface','Result','Opponent','Opponent DoB']]
    return data


def _covert_date(date):
    pd.to_DateTime(date, format='%Y%m%d', errors='coerce')
    return date


def data_player_career(n):
    raw_data= _download_player_data(n)
    data= _convert_java(raw_data)
    data= _create_df(data)
    data= _covert_date(data)
    return data
