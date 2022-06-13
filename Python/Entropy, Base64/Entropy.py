from numpy import log2
from os import stat
def Entropy(files, alphabet, result):
    for file in files:
        f = open(file, 'r', encoding="utf-8")
        text = f.read()
        f.close()
        text_len = len(text)
        
        punctuation = ".,:;!?«»()—-–…’' \n"
        symbols_frequency = []
        for letter in alphabet:
            if letter in text:
                letter_frequency = round(text.count(letter) / text_len, 4)
                symbols_frequency.append((letter, letter_frequency))
            big_letter = letter.upper()
            if not "Base64" in file:
                if big_letter in text:
                    letter_frequency = round(text.count(big_letter) / text_len, 4)
                    symbols_frequency.append((big_letter, letter_frequency))
        for punct in punctuation:
            if punct in text:
                punct_frequency = round(text.count(punct) / text_len, 4)
                symbols_frequency.append((punct, punct_frequency))
        H = 0
        for p_frequency in symbols_frequency:
            H += p_frequency[1] * log2(p_frequency[1])
        H_entropy = - H
        Info_count = H_entropy * text_len
        Info_size = round(Info_count / 8)
        File_size = stat(file).st_size
        Result = "//////////////////////////////////"
        Result += f"\nЧастоти появи символів у тексті {file} ({text_len} символів):"
        for symb_freq in symbols_frequency:
            Percent = round(symb_freq[1] * 100, 2)
            Result += f"\n {symb_freq[0]} - {symb_freq[1]} ({Percent}%)"
        Result += f"\nСередня ентропія алфавіту тексту - {H_entropy}"
        Result += f"\nКількість інформації в тексті - {Info_count} (в бітах)"
        Result += f"\nРозмір інформації в тексті - {Info_size}, а розмір файлу з цим "
        Result += f"текстом - {File_size} (в байтах), що в {round(File_size/Info_size, 2)} рази більше. \n\n"
        res = open(result, 'a', encoding="utf-8")
        res.write(Result)
        res.close()
        
files = ["1.txt","2.txt","3.txt"]
Base64_files = ["1.txt-Base64.txt","2.txt-Base64.txt","3.txt-Base64.txt"]
alphabet = 'абвгґдеєжзиіїйклмнопрстуфхцчшщьюя'
Base64_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
Base64_archives = ["1.tar.bz2-Base64.txt", "2.tar.bz2-Base64.txt", "3.tar.bz2-Base64.txt"]
archives = ["1.tar.bz2", "2.tar.bz2", "3.tar.bz2"]
Entropy(files, alphabet, "Result.txt")
#Entropy(Base64_files, Base64_alphabet, "Result-Base64.txt")
#Entropy(Base64_archives, Base64_alphabet, "Result-Base64-Archives.txt")