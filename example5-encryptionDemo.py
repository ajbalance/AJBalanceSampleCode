# 6.00x Problem Set 5
#
# Part 1 - HAIL CAESAR!

import string
import random

WORDLIST_FILENAME = "words.txt"

def loadWords():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print "Loading word list from file..."
    inFile = open(WORDLIST_FILENAME, 'r')
    wordList = inFile.read().split()
    print "  ", len(wordList), "words loaded."
    return wordList

def isWord(wordList, word):
    """
    Determines if word is a valid word.

    wordList: list of words in the dictionary.
    word: a possible word.
    returns True if word is in wordList.

    Example:
    >>> isWord(wordList, 'bat') returns
    True
    >>> isWord(wordList, 'asdf') returns
    False
    """
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\\:;'<>?,./\"")
    return word in wordList

def randomWord(wordList):
    """
    Returns a random word.

    wordList: list of words  
    returns: a word from wordList at random
    """
    return random.choice(wordList)

def randomString(wordList, n):
    """
    Returns a string containing n random words from wordList

    wordList: list of words
    returns: a string of random words separated by spaces.
    """
    return " ".join([randomWord(wordList) for _ in range(n)])

def randomScrambled(wordList, n):
    """
    Generates a test string by generating an n-word random string
    and encrypting it with a sequence of random shifts.

    wordList: list of words
    n: number of random words to generate and scamble
    returns: a scrambled string of n random words

    NOTE:
    This function will ONLY work once you have completed your
    implementation of applyShifts!
    """
    s = randomString(wordList, n) + " "
    shifts = [(i, random.randint(0, 25)) for i in range(len(s)) if s[i-1] == ' ']
    return applyShifts(s, shifts)[:-1]

def getStoryString():
    """
    Returns a story in encrypted text.
    """
    return open("story.txt", "r").read()

def buildCoder(shift):
    """
    Returns a dict that can apply a Caesar cipher to a letter.
    The cipher is defined by the shift value. Ignores non-letter characters
    like punctuation, numbers and spaces.

    shift: 0 <= int < 26
    returns: dict
    """
    upperstring = string.ascii_uppercase + string.ascii_uppercase
    lowerstring = string.ascii_lowercase + string.ascii_lowercase

    cipherdict = {}
    iupper = 0
    ilower = 0

    while iupper < 26:
        cipherdict[upperstring[iupper]] = upperstring[iupper + shift]
        iupper += 1

    while ilower < 26:
        cipherdict[lowerstring[ilower]] = lowerstring[ilower + shift]
        ilower  += 1

    return cipherdict
    #print cipherdict
    

def applyCoder(text, coder):
    """
    Applies the coder to the text. Returns the encoded text.

    text: string
    coder: dict with mappings of characters to shifted characters
    returns: text after mapping coder chars to original text
    """
    
    outputstring = ''

    for character in text:
        if character in string.ascii_uppercase or character in string.ascii_lowercase: 
            outputstring += coder[character]
        else:
            outputstring += character

    return outputstring
    

def applyShift(text, shift):
    """
    Given a text, returns a new text Caesar shifted by the given shift
    offset. Lower case letters should remain lower case, upper case
    letters should remain upper case, and all other punctuation should
    stay as it is.

    text: string to apply the shift to
    shift: amount to shift the text (0 <= int < 26)
    returns: text after being shifted by specified amount.
    """
    ### TODO.
    buildCoder(shift)
    return applyCoder(text, buildCoder(shift))
    #print applyCoder(text, buildCoder(shift))


def findBestShift(wordList, text):
    """
    Finds a shift key that can decrypt the encoded text.

    text: string
    returns: 0 <= int < 26
    """
    ### 1. Set the maximum number of real words found to 0.
    ### 2. Set the best shift to 0.

    maxwords = 0
    bestshift = 0

    ### 3. For each possible shift from 0 to 26:

    for shift in range(0,26):

        validwords = 0

        ### 4. Shift the entire text by this shift.

        shifted = applyShift(text, shift)        

        ### 5. Split the text up into a list of the individual words.

        shiftedlist = shifted.split(' ')

        ### 6. Count the number of valid words in this list.

        for word in shiftedlist:
            if isWord(wordList, word) == True:
                validwords += 1

        ### 7. If this number of valid words is more than the largest number of real words found, then:

        if validwords > maxwords:

        ###     8. Record the number of valid words.

            maxwords = validwords
               
        ###     9. Set the best shift to the current shift.
            bestshift = shift

        ### 10. Increment the current possible shift by 1. Repeat the loop starting at line 3.
    ### 11. Return the best shift .

    return bestshift

def decryptStory():
    """
    Using the methods you created in this problem set,
    decrypt the story given by the function getStoryString().
    Use the functions getStoryString and loadWords to get the
    raw data you need.

    returns: string - story in plain text
    """
    ### TODO.
    bestshift = findBestShift(wordList, getStoryString())
    print applyShift(getStoryString(), bestshift)



if __name__ == '__main__':
    wordList = loadWords()
    decryptStory()



