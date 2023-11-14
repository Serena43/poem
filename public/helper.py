import nltk
#nltk.download('cmudict') #cmudict: real dictionary made by cmu; 처음한번 실행하면 다운로드됬으니 꺼나도됨
from nltk.corpus import cmudict
import re #re: regular expression (this library comes w/ python like random, x need to download)
#nltk: an open source library for NLP (Natural Language Processing)
#NLP: technique for giving computer an ability to understand human language

def cnt_word_syll(word): #count syllables for a single word
    pronounce_dict = cmudict.dict()
    word = word.lower() #change to lower case
    phonetics = pronounce_dict.get(word) #[['EH1', 'L', 'AH0', 'F', 'AH0', 'N', 'T']]

    syllable_cnt = 0
    if phonetics != None:
        for phoneme in phonetics[0]: #'EH1'
            for char in phoneme:
                if char.isdigit(): #guaranteed that digit is only attached to vowel
                    syllable_cnt += 1
    return syllable_cnt

#regular expression: pattern matching (eg. email has @, ., etc.)
def cnt_sent_syll(sentence):
    # ^ => not
    # \w => alphabets & digits
    # \s => whitespace (space)
    #re.sub("pattern","new word", given sent) -> sub: substitute
    #-> find "patterns" from given sent and replace them to "new word"
    cleaned_sent = re.sub("[^\w\s]", "", sentence)
    list_words = cleaned_sent.split() # ["Hello", "my", "name", "is", "Serena"]

    total_syll = 0
    for word in list_words:
        num = cnt_word_syll(word)
        total_syll += num
    return total_syll

def haiku_is_standard(poem):
    first_ln_syll = cnt_sent_syll(poem[0])
    second_ln_syll = cnt_sent_syll(poem[1])
    third_ln_syll = cnt_sent_syll(poem[2])
    if first_ln_syll != 5:
        return False
    elif second_ln_syll != 7:
        return False
    elif third_ln_syll != 5:
        return False
    return True

# eg1 = ["An old silent pond", "A frog jumps into the pond—", "Splash! Silence again."]
# print(haiku_is_standard(eg1))

# print(cnt_word_syll("Elephant")) #python, java -> both can print returned val

# sentence = "Hello, my name is Serena!"
# print(cnt_sent_syll(sentence))

def words_rhyme(word1, word2):
    pronounce_dict = cmudict.dict()
    word1 = word1.lower()
    phonetics1 = pronounce_dict.get(word1)
    syll1 = ""
    for i in range(len(phonetics1)-1, len(phonetics1)-3, -1):
        syll1 += phonetics1[0][i]
    word2 = word2.lower()
    phonetics2 = pronounce_dict.get(word2)
    syll2 = ""
    for i in range(len(phonetics2) - 1, len(phonetics2) - 3, -1):
        syll2 += phonetics2[0][i]

    if syll1 == syll2:
        return True
    else:
        return False