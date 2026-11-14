# Tennis Career Match Analysis
Stat 159 Homework 3

## What this assignment is
This assignment builds off of HW 1 and HW 2, which is focused on retrieving and analyzing the dataset from Tennis Abstract 

I was able to grab the 

## Sources
- **Tennis Abstract:** https://www.tennisabstract.com/
Within the Tennis Abstract, I was able to parse through the different player's dataset in order get the female and male data. One of the challenges that I came across was when looking at the female and male datasets, the birthdates/age are in different formats, so I had to find different ways to format the data. This package was able to acknowledge these differences and format the dates accordingly.

## How to install it

The package can be installed directly from GitHub using pip
```bash
pip install git+https://github.com/UCB-stat159-f26/hw03-2-kandrachauu.git
```

## How to use it
After the installation of the package via pip, users are able to grab the match data and create a scatterplot (compared to opponents) for different players.

```python
from tennis_code import data_player_career, plot_player_age

# Serena Williams
serena = data_player_career("Serena Williams")
plot_player_age(serena) 
# SerenaWilliams
serena = data_player_career("SerenaWilliams")
plot_player_age(serena)
# serena williams
serena = data_player_career("serena williams")
plot_player_age(serena)

# Rafael Nadal
rafa = data_player_career("Rafael Nadal")
plot_player_age(rafa)

# Invalid player name
unknown_player = data_player_career("GastonSanchez")
```
In the example above, you are able to see that the function is accepts different variations of the the way a player's name is written. In the case that an unfamiliar name within the database is not recognized, an error will raise and a message for "Invalid Player name" will appear. 

## Project structure

```text
├── tennis_code/
│   ├── __init__.py
│   ├── data.py
│   └── plot.py
├── tests/
│   ├── test_data.py
│   └── test_plot.py
├── pyproject.toml
└── README.md
└── ai_documentation.txt
```
### Data processing

| Function | Description |
|---|---|
| `data_player_career()` | Grabs and processes career match data for a given player |
| `_download_player_data()` | Downloads the player's career Javascript file from Tennis Abstract |
| `_convert_java()` | Converts the Javascript into a pandas DataFrame |
| `_create_df()` | Selects and formats the necessary columns |
| `_covert_date()` | Converts match dates into datetime format |
| `_covert_age()` | Calculates the player's age at each match |
| `_opp_age_f()` | Finds female opponents' ages using birthdates |
| `_opp_age_m()` | Turns male opponents' ages into numeric values |
| `_age_diff()` | Finds the age difference between the player and opponent |

### Data visualization

| Function | Description |
|---|---|
| `plot_player_age()` | Creates a scatterplot showing player age against age difference, which is colorcoded by match result (blue for wins and purple for losses, similar to the NYT article visualization from previous homeworks) |

## Testing

The package uses `pytest` to test the data processing and plotting functions without the need to make request on the live website.

In order to run the tests, you must use:

```bash
python -m pytest tests/ -v
```

## Reflections
Throughout this assignment, I developed and established different learning objections in regards to becoming a stronger programmer. I was able to learn more about creating reusable functions that could be used on different players. I am glad to be able to apply different lessons from labs and lectures and be able to apply it within this homework, like .toml. Before this assignment, I did not feel the need of taking extra steps of creating a toml and test files. Overall, this assignment showed me how these small steps truly make a difference within the project. Going forward, I plan on implementing these extra steps and will try to pursue personal projects that focus on creating an installable python package. 