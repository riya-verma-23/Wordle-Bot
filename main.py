import wordle
import pandas as pd

#window = pd.read_csv('window.csv')         
#wordle.game('alert','slate')

count = 0
words = pd.read_csv('guess_list.csv')
window = pd.read_csv('window.csv')
print("For current state, use g - green, y - yellow, b - gray")
while(True):
    guessed_word = input('Enter your guess:')
    curr_state = list(input('Enter curr state: '))
    print(count, guessed_word)
    if curr_state == ['g', 'g', 'g', 'g', 'g']:
        break
    if (count > 6):
        count = 7
        break
    window = wordle.narrow_window_letters_contained(window, guessed_word , curr_state)
    window = wordle.narrow_window_yellow(curr_state, guessed_word, window)
    if (len(window) == 0):
        print('no words found in list')
        count = 7
        break
    else:
        possible_chars = ''
        for i in range(len(window)):
            w = window['words'][i]
            if not(w[0] in possible_chars): possible_chars += w[0]
        if ((curr_state == ['b', 'g', 'g', 'g', 'g']) | (curr_state == ['y', 'g', 'g', 'g', 'g'])) & (len(possible_chars) >= 3):
            guessed_word = wordle.four_green(possible_chars, window, words)
            print(possible_chars)
        else:
            guessed_word = window[window.freq == max(window.freq)]['words'][0]
            print("Wordle Bot recommends the word: ", guessed_word)
    count +=1