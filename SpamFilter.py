# A spam filter that utilizes probability and a training set to define
# spam messages.
# The training set used for this was found from the following website:
# https://archive.ics.uci.edu/ml/datasets/SMS+Spam+Collection
# Since the code is set up to utilize this dataset, please insure that
# future datasets are in the following format:
#   1. Indicates ham or spam as the first word in the line.
#   2. Each message is separated by a new line.

# Import
import math

# Function used to parse through training data and create a list of words
# found in the data.
def load_tokens(file):
    # Open file
    f = open(file, "r")
    messageList = f.readlines()
    hamList = []
    spamList = []
    totalList = [hamList,spamList]
    # Separates the words and adds them to a list depending on if
    # the message was spam or not. Also removes the ham and spam indicator.
    for i in messageList:
        temp = i.split()
        if temp.pop(0) == "ham":
            for j in temp:
                totalList[0].append(j)
        else:
            for j in temp:
                totalList[1].append(j)
    f.close()
    return totalList

# Creates a dictionary pairing each word up with their probability.
def log_probs(wordList, smoothing):
    wordDictCount = {}
    wordTotalCount = 0
    wordProb = {}
    for i in wordList:
        # If word is already in dict, increase count.
        if i in wordDictCount:
            wordDictCount[i] += 1
            wordTotalCount += 1
        # Else, add to dict.
        else:
            wordDictCount[i] = 1
            wordTotalCount += 1
    # For each word in dict, compute probability.
    for i in wordDictCount:
        wordProb[i] = math.log((wordDictCount[i]+smoothing)/(wordTotalCount+(smoothing*(len(wordDictCount)+1))))
    # Add <UNK> (probability of a missing word).
    wordProb["<UNK>"] = math.log(smoothing/(wordTotalCount+(smoothing*(len(wordDictCount)+1))))
    return wordProb

class SpamFilter(object):
    def __init__(self, file, smoothing):
        # Load words from training set.
        self.wordListTotal = load_tokens(file)
        self.smoothing = smoothing
        # Create probability dictionaries.
        self.spam_dict = log_probs(self.wordListTotal[1], self.smoothing)
        self.ham_dict = log_probs(self.wordListTotal[0], self.smoothing)
        self.full_dict = log_probs(self.wordListTotal[0]+self.wordListTotal[1], self.smoothing)
        # P(spam) and P(~spam), using simple percent based probability.
        self.p_spam = len(self.wordListTotal[1])/len(self.wordListTotal[0]+self.wordListTotal[1])
        self.p_not_spam = len(self.wordListTotal[0])/len(self.wordListTotal[0]+self.wordListTotal[1])

    # Checks if message is spam based on the training set.
    def is_spam(self, message):
        # Note: return of True means that message is spam.
        # Find word count.
        wordDictCount = {}
        wordList = message.split()
        for i in wordList:
            # If word is already in dict, increase count.
            if i in wordDictCount:
                wordDictCount[i] += 1
            # Else, add to dict.
            else:
                wordDictCount[i] = 1
        # Spam p and ~spam p.
        pSpamValue = math.log(self.p_spam)
        pNotSpamValue = math.log(self.p_not_spam)
        for i in wordDictCount:
            # Check spam.
            if i in self.spam_dict:
                pSpamValue += wordDictCount[i]*self.spam_dict[i]
            # Word not found, use <UNK>.
            else:
                pSpamValue += wordDictCount[i]*self.spam_dict["<UNK>"]
            # Check not spam.
            if i in self.ham_dict:
                pNotSpamValue += wordDictCount[i]*self.ham_dict[i]
            # Word not found, use <UNK>.
            else:
                pNotSpamValue += wordDictCount[i]*self.ham_dict["<UNK>"]
        # Return True if spam > ~spam.
        if pSpamValue > pNotSpamValue:
            return True
        else:
            return False

    # Returns the n words that are ranked to be most likely
    # from spam messages.
    def most_indicative_spam(self, n):
        indicDict = {}
        for i in self.spam_dict:
            # Remove words that only appear in spam.
            if i not in self.ham_dict:
                continue
            # Remove <UNK>.
            if i == "<UNK>":
                continue
            indicDict[i] = self.spam_dict[i]-self.full_dict[i]
        solution = []
        # Find top n results.
        for i in range(n):
            currMax = max(indicDict, key=indicDict.get)
            solution.append(currMax)
            indicDict.pop(currMax)
        return solution

    # Returns the n words that are ranked to be most likely
    # from ham messages.
    def most_indicative_ham(self, n):
        indicDict = {}
        for i in self.ham_dict:
            # Remove words that only appear in ham.
            if i not in self.spam_dict:
                continue
            # Remove <UNK>.
            if i == "<UNK>":
                continue
            indicDict[i] = self.ham_dict[i]-self.full_dict[i]
        solution = []
        # Find top n results.
        for i in range(n):
            currMax = max(indicDict, key=indicDict.get)
            solution.append(currMax)
            indicDict.pop(currMax)
        return solution

# Main body
spamChecker = SpamFilter("SMSSpamCollection.txt", 1e-5)
print("Words most indicative of spam: ", spamChecker.most_indicative_spam(5))
print("Words most indicative of ham: ", spamChecker.most_indicative_ham(5))
message = input("What message would you like to check for spam?\n")
if spamChecker.is_spam(message):
    print("This is spam!")
else:
    print("This is not spam!")
