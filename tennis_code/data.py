 
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

def _convert_birthdate(i):
    value = str(i["Opponent DoB"])
    if "." not in value:
        return pd.to_datetime(value, format="%Y%m%d", errors="coerce")
    match_day = pd.to_datetime(str(i["Date"]), format="%Y%m%d")
    age = float(value)
    birthday = match_day - pd.to_timedelta(age * 365.25, unit="D")
    return birthday.round("D")

def _grab_birthdate(name, opponent):
    raw = _download_player_data(opponent)
    df = _create_df(_convert_java(raw))
    target = _player_names(name).lower()
    names = df["Opponent"].astype(str).map(lambda x: _player_names(x).lower())
    matches = df.loc[names == target]
    if matches.empty:
        return None
    return _convert_birthdate(matches.iloc[0])

def _get_player_birth(name, df):
    for opponent in df["Opponent"].dropna().unique()[:10]:
        try:
            birth = _grab_birthdate(name, opponent)
            if birth is not None and not pd.isna(birth):
                return birth
        except (ValueError, KeyError, requests.RequestException):
            continue
    raise ValueError(f"Couldn't find birthdate for {name}")


def data_player_career(n):
    raw_data = _download_player_data(n)
    data = _create_df(_convert_java(raw_data))
    data["Date"] = _covert_date(data["Date"])
    birthday = _get_player_birth(n, data)
    data = _covert_age(data, birthday)
    if "." in str(data["Opponent DoB"].dropna().iloc[0]):
        data = _opp_age_m(data)
    else:
        data = _opp_age_f(data)
    return _age_diff(data)

