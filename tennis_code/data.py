
import pandas as pd
import requests
import json
import re

def _player_names(n):
    if pd.isna(n):
        return n
    else:
        return re.sub(r"(?<=[a-z])(?=[A-Z])", " ", str(n)).title().replace(" ","")



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
    date=pd.to_datetime(date, format='%Y%m%d', errors='coerce')
    return date

def _covert_age(df,birth):
    birth=pd.to_datetime(birth)
    df["Player's Age"]=((df['Date']-birth).dt.days/365)
    return df


def _opp_age_f(df):
    opp_birth= pd.to_datetime(df['Opponent DoB'], format="%Y%m%d",errors='coerce')
    df["Opponent Age"]= (df['Date']-opp_birth).dt.days/365
    return df

def _age_diff(df):
    df['Age Difference']= df["Player's Age"]-df['Opponent Age']
    return df


def _opp_age_m(df):
    df["Opponent Age"]= pd.to_numeric(df['Opponent DoB'],errors='coerce')
    return df



#serena['Serena Age']=((serena['Date']-serenabirth).dt.days/365)
#serena['Opponent Age']=((serena['Date'] - serena['Opponent DoB']).dt.days/365)


#serena['Age Gap']=(serena['Serena Age'] - serena['Opponent Age'])

def data_player_career(n):
    raw_data= _download_player_data(n)
    data= _convert_java(raw_data)
    data= _create_df(data)
    data["Date"] = _covert_date(data["Date"])

    if n.lower().replace(" ", "") == "serenawilliams":
        data = _covert_age(data, "1981-09-26")
        data = _opp_age_f(data)

    elif n.lower().replace(" ", "") == "rafaelnadal":
        data = _covert_age(data, "1986-06-03")
        data = _opp_age_m(data)

    else:
        raise ValueError("Player birthday and data format not configured")

    return _age_diff(data)

