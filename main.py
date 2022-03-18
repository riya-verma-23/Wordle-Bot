import wordle
import pandas as pd

window = pd.read_csv('window.csv')
wordle.game('crane', 'slate')
