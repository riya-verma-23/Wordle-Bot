import wordle
import pandas as pd

print('slate', wordle.simulate_all_games('slate'))
print('least', wordle.simulate_all_games('least'))

count = 1
words = pd.read_csv('guess_list.csv')
window = pd.read_csv('window.csv')
actual_word = input('Enter actual word: ')
guessed_word = input('Enter guess:')
if(True):
    while(True):
        print(count, guessed_word)
        curr_state = wordle.check_word(actual_word, guessed_word)
        if curr_state == ['g', 'g', 'g', 'g', 'g']:
            break
        if (count > 6):
            count = 7
            break
        window = wordle.narrow_window_letters_contained(window, guessed_word , curr_state)
        window = wordle.narrow_window_yellow(curr_state, guessed_word, window)
        if (len(window) == 0):
            print('no words')
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
        count +=1
