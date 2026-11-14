import pandas as pd
from tennis_code.data import _convert_java, _create_df, _covert_date, _opp_age_f, _opp_age_m

def test_convert_java():
    rawset='var morematchmx = [["19951030", "Canadian Open", "Carpet", "W", "L", "", "", "WC", "Q1", "6-1 6-1", "3", "Anne Miller", "149", "7", "", "R", "19770119"]];'
    df=_convert_java(rawset)
    assert isinstance(df, pd.DataFrame)
    assert df.shape[0]==1

def test_create_df():
    rawset='var morematchmx = [["19951030", "Canadian Open", "Carpet", "W", "L", "", "", "WC", "Q1", "6-1 6-1", "3", "Anne Miller", "149", "7", "", "R", "19770119"]];'
    df=_create_df(_convert_java(rawset))
    assert "Date" in df.columns
    assert "Opponent" in df.columns
    assert "Opponent DoB" in df.columns
    assert df.iloc[0]["Opponent"]=="Anne Miller"

def test_convert_date():
    date = pd.Series(["19951030", "19970307"])
    result = _covert_date(date)
    assert result.iloc[0] == pd.Timestamp("1995-10-30")
    assert result.iloc[1] == pd.Timestamp("1997-03-07")

def test_opp_age_female():
    df= pd.DataFrame({"Date":[pd.Timestamp("1995-10-30")],
                  "Opponent DoB":["19770119"]})
    result=_opp_age_f(df)

def test_opp_age_male():
    df= pd.DataFrame({"Date":[pd.Timestamp("1998-11-26")],
                  "Opponent DoB":["23.624523"]})
    result=_opp_age_m(df)

    assert "Opponent Age" in result.columns
    assert round(result.iloc[0]["Opponent Age"],2)==23.62