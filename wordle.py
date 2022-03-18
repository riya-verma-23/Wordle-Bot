import numpy as np
import pandas as pd
import string
import random

def check_word(actual_word, guessed_word): #simulates what is returned by wordle
    curr_state = list('00000')
    
    for i in range(len(guessed_word)):
        if guessed_word[i] in actual_word:
            if actual_word[i] == guessed_word[i]:
                curr_state[i] = 'g'
            else:
                curr_state[i] = 'y'
        else:
            curr_state[i] = 'b'

    return curr_state
    
def get_indices(curr_state, char):
    indices = []
    for i in range(len(curr_state)):
        if curr_state[i] == char:
            indices.append(i)
    return indices

def narrow_window_letters_contained(df, guessed_word, curr_state):
    green_indices = get_indices(curr_state, 'g')
    green_chars = ''
    for a in range(len(green_indices)):
        green_chars += guessed_word[green_indices[a]]
    
    yellow_indices = get_indices(curr_state, 'y')
    gray_indices = get_indices(curr_state, 'b')
    window_data = []
    for i in range(len(df)):
        marker = True
        w = df['words'][i]
        for j in range(len(green_indices)):
            if w[green_indices[j]] != guessed_word[green_indices[j]]:
                marker = False
        for k in range(len(yellow_indices)):
            if (not (guessed_word[yellow_indices[k]] in w)):
                marker = False
        for l in range(len(gray_indices)):
            if (guessed_word[gray_indices[l]] in w) & (not(guessed_word[gray_indices[l]] in green_chars)):
                marker = False
        if marker:
            d = {'words' : w, 'freq' : df.at[i, 'freq']}
            window_data.append(d)
    
    window_df = pd.DataFrame(window_data)
    window_df = narrow_duplicate_green_gray(guessed_word, gray_indices, green_chars, window_df)
    return window_df

def narrow_duplicate_green_gray(guessed_word, gray_indices, green_chars, window_df):
    window_data = []
    for i in range(len(gray_indices)):
        dup_green = (guessed_word[gray_indices[i]] in green_chars)
        if dup_green:
            for j in range(len(window_df)):
                w = window_df['words'][j]
                if not(w[gray_indices[i]] == guessed_word[gray_indices[i]]):
                    d = {'words' : w, 'freq' : window_df.at[i, 'freq']}
                    window_data.append(d)
            window_df = pd.DataFrame(window_data)
    return window_df

def narrow_window_yellow(curr_state, guessed_word, window_df):
    yellow_indices = get_indices(curr_state, 'y')
    window_data = []

    for i in range(len(window_df)):
        w = window_df['words'][i]
        marker = True
        for j in range(len(yellow_indices)):
            yellow_char = guessed_word[yellow_indices[j]]
            if w[yellow_indices[j]] == yellow_char:
                marker = False
        if marker:
            d = {'words' : w, 'freq' : window_df.at[i, 'freq']}
            window_data.append(d)

    new_window_df = pd.DataFrame(window_data)
    return new_window_df

def common_positions(char, window_df):
    frequencies = [0, 0, 0, 0, 0]
    for i in range(len(window_df)):
        w = window_df['words'][i]
        for j in range(len(w)):
            if w[j] == char:
                frequencies[j]+=1
    return frequencies

def potential_words_freq(guessed_word, curr_state, window_df):
    yellow_pos = get_indices(curr_state, 'y')
    window_data = []
    for i in range(len(window_df)):
        marker = True
        w = window_df['words'][i]
        for j in range(len(yellow_pos)):
            freq = common_positions(guessed_word[yellow_pos[j]], window_df)
            max_value = max(freq)
            most_common_ind = freq.index(max_value)
            if w[most_common_ind] != guessed_word[yellow_pos[j]]:
                marker = False
        if marker:
            window_data.append(w)

    if(len(window_data) > 0): new_window_df = pd.DataFrame({'words': window_data})
    else: new_window_df = window_df

    return new_window_df
    
def game(actual_word, initial_guess, window):
    count = 1
    words = pd.read_csv('window.csv')
    window = words
    guessed_word = initial_guess
    while(True):
        if (count > 6):
            count = 7
            break
        curr_state = check_word(actual_word, guessed_word)
        if curr_state == ['g', 'g', 'g', 'g', 'g']:
            break

        window = narrow_window_letters_contained(window, guessed_word , curr_state)
        window = narrow_window_yellow(curr_state, guessed_word, window)
        if (len(window) == 0):
            print(actual_word)
            count = 7
            break
        else:
            possible_chars = ''
            for i in range(len(window)):
                w = window['words'][i]
                if not(w[0] in possible_chars): possible_chars += w[0]
            if ((curr_state == ['b', 'g', 'g', 'g', 'g']) | (curr_state == ['y', 'g', 'g', 'g', 'g'])) & (len(possible_chars) >= 3):
                guessed_word = four_green(possible_chars, window, words)
                print(possible_chars)
            else:
                guessed_word = window[window.freq == max(window.freq)]['words'][0]
        count +=1

    return count

def simulate_all_games(initial_guess):
    df = pd.read_csv("window.csv")
    #sample = 5000
    success = 0
    #df_ind = random.sample(range(0, len(df)), sample)
    total = 0
    for i in range(len(df)):
        actual_word = df['words'][i]
        count = game(actual_word, initial_guess, df)
        if count <= 6:
            success+=1
        else:
            print(actual_word)
        total += count
    
    average = total / len(df)
    print("success %: ", success/len(df))
    return average

def four_green(possible_chars, window_df, words_df):
    rec_word = ''
    max = 0
    for k in range(len(words_df)):
        w = words_df['words'][k]
        count = 0

        for j in range(len(w)):
            rest_word = ''
            for i in range(len(w)):
                if not(i == j):
                    rest_word += w[i]
            
            if (w[j] in possible_chars) & (not(w[j] in rest_word)):
                count+=1
        if count > max:
            max = count
            rec_word = w
    return rec_word 
