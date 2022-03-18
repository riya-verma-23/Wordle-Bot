import wordle
import pandas as pd

window = pd.read_csv('window.csv')         
wordle.game(actual_word='crane', initial_guess='slate')
