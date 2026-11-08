import requests

def _player_names(n):
    if pd.isna(n):
        return n
    return "".join(i.capitalize() for i in n.split())



def _download_player_data(n):
    format_name= _player_names(n)
    link= f"https://www.tennisabstract.com/jsmatches/{format_name}Career.js"
    request_result= requests.get(link, timeout=20)

    if not request_result.ok:
        raise ValueError(f"The player you entered is invalid, we were not able to find data for '{n}'")
    return request_result.text


def data_player_career(n):
    data= _download_player_data(n)
    return data
