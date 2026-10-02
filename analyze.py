from random_username.generate import generate_username
import re
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet, stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from wordcloud import WordCloud
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger_eng')
nltk.download('vader_lexicon')
wordLemmatizer = WordNetLemmatizer()
stopWords = set(stopwords.words('english'))
sentimentAnalyzer = SentimentIntensityAnalyzer()



# Welcome user
def welcomeUser():
    print("\nWelcome to the analysis tool, I will mine and analyze a body of text from a file you give me!")

# Get Username
def getUsername():

    maxAttempts = 3
    attempts = 0

    while attempts < maxAttempts:

        # Print message prompting user to input their name
        inputPrompt = ""
        if attempts == 0:
            inputPrompt = "\nTo begin, please enter your username:\n"
        else:
            inputPrompt = "\nPlease try again:\n"

        usernameFromInput = input(inputPrompt)

        # Vaalidate username
        if len(usernameFromInput) < 5 or not usernameFromInput.isidentifier():
            print("Your username must be at least 5 character long, alphanumeric only (a-z/A-Z/0-9), have no spaces and cannot start with a number")
        else:
            return usernameFromInput
        attempts += 1



    print("Exhausted all " + str(attempts) + " attempts, assigning username instead...")
    return generate_username()[0]   

# Greet the user
def greetUser(name):
    print("Hello, " + name)

# Get text from file
def  getArticleText():
    f = open("files/article.txt", "r")
    rawText = f.read()
    f.close()
    return rawText.replace("\n", " ").replace("\r", "")

# Extract sentences from raw text body
def tokenizeSentences(rawText):
    return sent_tokenize(rawText)

# Extract words from list of sentences
def tokenizeWords(sentences):        
    words = []
    for sentence in sentences:
        words.extend(word_tokenize(sentence))
    return words

# Get the key sentences based on search pattern of key words
def extractKeySentences(sentences, searchPattern):
    matchedSentences = []
    for sentence in sentences:
        # If sentence matches desired pattern, add to matchedSentences
        if  re.search(searchPattern, sentence.lower()):
            matchedSentences.append(sentence)
    return matchedSentences

# Get the average words per sentence, excluding punctuation
def getWordsPerSentence(sentences):
    totalWords = 0
    for sentence in sentences:
        totalWords += len(sentence.split(" "))
    return totalWords / len(sentences)

posToWordnetTag = {
    "J": wordnet.ADJ,
    "V": wordnet.VERB,
    "N": wordnet.NOUN,
    "R": wordnet.ADV
}

# Convert part of speech from pos_tag() funtion 
# into wordnet compatible pos tag 
def treebankPosToWordnetPos(partOfSpeech):
    posFirstChar = partOfSpeech[0]
    if posFirstChar in posToWordnetTag:
        return posToWordnetTag[posFirstChar]
    
    return wordnet.NOUN

# Convert raw list of (words, POS) tuple to a list of strings 
# that only include valid english words
def cleanseWordList(posTaggedWordTuples):
    cleanseWords = []
    invalidWordPattern = "[^a-zA-Z-+]"
    for posTaggedWordTuple in posTaggedWordTuples:
        word = posTaggedWordTuple[0]
        pos = posTaggedWordTuple[1]
        cleanseWord = word.replace(".", "").lower()
        if (not re.search(invalidWordPattern, cleanseWord)) and len(cleanseWord) >= 2 and cleanseWord not in stopWords:
            cleanseWords.append(wordLemmatizer.lemmatize(cleanseWord, treebankPosToWordnetPos(pos)))
    return cleanseWords

#Get user details
welcomeUser()
username = getUsername()
greetUser(username)

# Extract and tokenizetext
articleTextRaw =  getArticleText()
articleSentences = tokenizeSentences(articleTextRaw)
articleWords = tokenizeWords(articleSentences)

# Get sentence analytics
stockSearchPattern = "[0-9]|[%$£₤]|thousand|million|billion|thrillion|profit|loss"
keySentences = extractKeySentences(articleSentences, stockSearchPattern)
wordsPerSentence = getWordsPerSentence(articleSentences)

# Get word analytics
wordsPosTagged = nltk.pos_tag(articleWords)
articleWordsCleansed = cleanseWordList(wordsPosTagged)

# Generate word cloud
separator = " "
wordcloud = WordCloud(width= 1000, height=700, \
                      background_color="white", colormap="Set3", collocations=False).generate(separator.join(articleWordsCleansed))
wordcloud.to_file("results/wordcloud.png")

# Run sentiment analysis
sentimentResult = sentimentAnalyzer.polarity_scores(articleTextRaw)

# Print for testing
print(sentimentResult)