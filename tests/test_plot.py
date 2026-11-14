import pandas as pd
import matplotlib.pyplot as plt
from tennis_code.plot import plot_player_age
import tennis_code.data as tennis_data
import pytest

def test_plot_player_age():
    df= pd.DataFrame({"Player's Age":[16,20,25],
                    "Age Difference":[15,-5,3],
                     "Result":["W",'L','L']})
    fig=plot_player_age(df)
    assert isinstance(fig,plt.Figure)
    assert len(fig.axes)==1
    assert len(fig.axes[0].collections)==1
    plt.close(fig)

def test_invalid_player(monkeypatch):
    def invalid_player(name):
        raise ValueError("Invalid player name, please enter another tennis player")
    monkeypatch.setattr(tennis_data,"_download_player_data", invalid_player)
    with pytest.raises(ValueError, match="Invalid player"):
        tennis_data.data_player_career("GastonSanchez")