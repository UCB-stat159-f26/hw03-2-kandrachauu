import matplotlib.pyplot as plt

def plot_player_age(df):
    fig, ax = plt.subplots()
    ax.grid(axis='both',alpha=0.3)
    ax.set_axisbelow(True)
    ax.scatter(x=df["Player's Age"], y=df['Age Difference'], c=df['Result'].map({'W': 'lightblue', 'L': 'purple'}), s=9)
    ax.xaxis.tick_top()
    ax.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
    plt.xlabel("Player's Age")
    plt.ylabel("Age Difference")
    plt.title('Professional Matches, by Player Age', fontsize=14)
    return fig
