import pandas as pd
from moviepy.editor import *
import string
from fastDamerauLevenshtein import damerauLevenshtein
import streamlit as st

imbuhan = ['ter', 'te', 'se', 'per', 'peng', 
               'pen', 'pem', 'pe', 'men', 'mem', 
               'me', 'ke', 'di', 'ber', 'be']
list_animation = ["me","masak","apa","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
df = pd.read_csv('data/kbbi.txt',header=None, names=['kata'])
df = df.dropna()
df_akronim = pd.read_csv('data/persamaan.csv')


def hapus_angka(string_input):
    string_tanpa_angka = ''.join(char for char in string_input if not char.isdigit())
    return string_tanpa_angka

def case_folding(string_input):
    string_input = string_input.lower()
    return string_input

def hapus_tanda_baca(string_input):
    translator = str.maketrans("", "", string.punctuation)
    string_tanpa_tanda_baca = string_input.translate(translator)
    return string_tanpa_tanda_baca

def animation(word):
    video = [ VideoFileClip(fr'video/{i}.mp4') for i in word]
    # # join and write 
    # print('video',video)
    result = concatenate_videoclips(video)
    result.write_videofile('combined.mp4',20)

def damerau_levenshtein_distance(str1, str2):
    return damerauLevenshtein(str1, str2,similarity=False)

def spell_correction(kata, df):
    min_distance = float('inf')
    min_word = kata
    
    def calculate_distance(row):
        nonlocal min_distance, min_word
        distance_val = damerau_levenshtein_distance(kata, row['kata'])
        if distance_val < min_distance:
            min_distance = distance_val
            min_word = row['kata']
    
    df.apply(calculate_distance, axis=1)
    
    return min_word

def spell_suggest(kata, df):
    suggestions = []
    
    def calculate_distance(row):
        if damerau_levenshtein_distance(kata, row['kata']) == 1:
            suggestions.append(row['kata'])
    
    df.apply(calculate_distance, axis=1)
    
    return suggestions


def cek_kata(word,df):
    if df['kata'].isin([word]).any():
        return word 
    
    suggestions = spell_suggest(word, df)
    if suggestions:
        return suggestions[0]
    else:
        # Spell correction
        correction = spell_correction(word, df)
        # print(f"{word} ejaan21 yang salah. Mungkin yang dimaksud adalah: {correction}")
        return correction

def spell_check(word, word_list):
    if word in word_list:
        return True
    return False

def textToAnimation(word_sequence):
    # print(word_sequence)
    wordToAnimation = []
    for i in word_sequence: 
        if i in list_animation:
            wordToAnimation.append(i)
        elif i not in list_animation :
            for j in i :
                if j in list_animation:
                    wordToAnimation.append(j)
        if i not in imbuhan:
            wordToAnimation.append('idle')
    # print(wordToAnimation)
    return wordToAnimation

def trimKataImbuhan(word):
    word = hapus_angka(case_folding(hapus_tanda_baca(word)))
    li = list(filter(None, word.split(" ")))
    
    word_sequence = []
    
    for i in li:
        print(i)
        if i in df_akronim['singkatan'].values:
            kata = df_akronim.loc[df_akronim['singkatan'] == i, 'kata'].values[0]
            print(f"Kata untuk singkatan '{i}' adalah '{kata}'")
            word_sequence.append(kata)
        else:
            found = False
            for j in imbuhan:
                if i.startswith(j):
                    word_sequence.append(j)
                    word_sequence.append(df.loc[df['kata'] == i, 'kata'].values[0][len(j):])
                    found = True
                    break
            if not found:
                word_sequence.append(i)
    list_word_correction = [cek_kata(i, df) for i in word_sequence]
    return word_sequence, list_word_correction, li

def main():
    user_input = st.text_input("Enter some text")
    if len(user_input):
        word_input = user_input
        trim,correction,word_input  = trimKataImbuhan(word_input)
        text_toanimate = textToAnimation(trim )
        print('text_toanimate',text_toanimate)
        animation(text_toanimate)
        print(trim)
        print(correction)
        print(word_input)
        # Video file path or URL
        video_path = "combined.mp4"

        # Display the video
        st.video(video_path)

if __name__ == "__main__":
    main()