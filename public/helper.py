import nltk
#nltk.download('cmudict') #cmudict: real dictionary made by cmu; 처음한번 실행하면 다운로드됬으니 꺼나도됨
from nltk.corpus import cmudict
from nltk.metrics import jaccard_distance #gets similarity btw words
from nltk.corpus import stopwords
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

def is_acrostic(theme, poem):
    threshold = 0.1
    # return true if first letter of each line matches each letter in theme
    if not match_theme(theme, poem):
        return False
    if is_similar_theme(theme, poem) < threshold:
        return False
    return True

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

#functions for acrostic

#POEM -> poem
#Poem -> poem

def match_theme(theme, lines):
    theme = theme.lower()
    theme_index = 0;
    for line in lines:
        if line[0].islower():
            return False

        line = line.lower()
        if line[0] != theme[theme_index]:
            return False
        theme_index += 1
    return True

# NLP: Natural Language Processing, giving computer ability to understand the human language (modern tech)
# stopword: meaningless word eg. is, a, the, of, are, am, have, will, ...
def is_similar_theme(theme, lines):
    poem = " ".join(lines) # changing list to string
    poem = poem.lower()
    cleaned_poem = re.sub("[^\w\s]", "", poem) #\w -> alphabets, digits, _.; \s -> white space; ^ -> not
    # Hello my name is Serena
    list_word = cleaned_poem.split() #["Hello", "my", "name", ...]
    stopword_list = stopwords.words('english') #getting english stopwords
    no_stopword = [word for word in list_word if word not in stopword_list]
    # no_stopword => it contains the words in poem but x stopwords

    similarity_total = 0
    number_of_word = 0
    for word in no_stopword:
        similarity = 1 - jaccard_distance(set(theme), set(word))
        similarity_total += similarity
        number_of_word += 1

    avg_similarity = similarity_total / number_of_word
    return avg_similarity

lines = ["Cuddly", "Acrobatic", "Tenacious", "Softly purring"] #T
print(match_theme("cats",lines))
print(is_similar_theme("poem",lines))

lines = ["Paaaa", "Oaaaa", "Eaaaa", "Maaaa"] #F
print(match_theme("poem",lines))
print(is_similar_theme("poem",lines))

lines = ["Preserve the high honour of poems dear,", "Oh poor acrostic-writer: by design,", "Each line of verse that you will lay down here", "My name discover, line by singing line."] #T
print(match_theme("poem",lines))
print(is_similar_theme("poem",lines))

word1 = "king"
word2 = "ball"
similarity = 1 - jaccard_distance(set(word1), set(word2))
print(similarity)